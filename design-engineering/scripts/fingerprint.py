#!/usr/bin/env python3
"""Design fingerprint: encode the structural character of a screen/brand system and compare systems.

  python fingerprint.py init [--brand NAME] > brand-a.json     # skeleton with allowed values
  python fingerprint.py validate brand-a.json
  python fingerprint.py compare brand-a.json brand-b.json [brand-c.json ...] [--json] [--threshold 0.7]

A fingerprint is deterministic metadata about *structure* (navigation model, layout topology,
density, grid, surfaces, imagery, metadata, CTA) plus cosmetic axes (corners, colour, icons).
It cannot be read from pixels by this script; it is produced by advise.py direction, by the
model after inspecting a screen or screenshot, or by hand. The comparison is then exact.

Verdicts:
  DISTINCT       structural similarity below threshold
  COSMETIC-ONLY  cosmetic axes differ but structural axes are (almost) identical  -> FAIL for brand differentiation
  NEAR-DUPLICATE both structural and cosmetic axes nearly identical             -> FAIL
"""

from __future__ import annotations

import argparse
import io
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from de_core import FINGERPRINT_AXES, STRUCTURAL_AXES  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ALLOWED = {
    "navigation_model": ["top-bar", "left-rail", "left-drawer", "bottom-tabs", "tab-bar", "hub-and-spoke",
                         "tv-side-nav", "tv-top-tabs", "command-palette", "breadcrumb-tree", "wizard", "single-screen", "menu-bar"],
    "layout_topology": ["single-column", "two-pane", "three-pane", "master-detail", "dashboard-grid", "rails",
                        "immersive-hero-rails", "feed", "canvas", "form-stack", "table-first", "split-view", "grid-catalog", "editorial-columns"],
    "content_density": ["low", "medium", "high"],
    "grid_behavior": ["fixed", "fluid", "responsive-columns", "masonry", "horizontal-scroll", "virtualized", "none"],
    "card_geometry": ["none", "flat-tile", "bordered", "elevated", "poster-portrait", "poster-landscape", "row-item", "list-row"],
    "corner_language": ["sharp", "small", "medium", "large", "pill", "mixed-intentional"],
    "typography_character": ["neutral-sans", "geometric-sans", "humanist-sans", "grotesk-display", "serif-editorial",
                             "serif-display", "monospace-technical", "condensed-display", "rounded-friendly", "system-native"],
    "color_strategy": ["neutral-plus-accent", "dominant-brand", "dark-with-accent", "duotone", "multicolour-semantic",
                       "monochrome", "image-derived", "material-tonal"],
    "surface_strategy": ["flat", "bordered", "elevated", "tonal-layers", "glass", "imagery-backed", "mixed"],
    "image_strategy": ["none", "hero-imagery", "poster-art", "immersive-backdrop", "thumbnails", "illustration", "iconography-only", "data-graphics"],
    "icon_strategy": ["outline", "filled", "duotone", "text-only", "system", "custom-glyphs"],
    "motion_character": ["none", "functional-minimal", "spring", "cinematic", "focus-scale", "crossfade", "expressive"],
    "focus_strategy": ["browser-default", "ring", "scale", "glow", "underline", "background-shift", "border-plus-scale", "none-touch-only"],
    "metadata_density": ["minimal", "moderate", "rich", "inline-badges", "hover-reveal", "focus-reveal"],
    "cta_strategy": ["single-primary", "primary-plus-secondary", "contextual-inline", "sticky-bar", "focus-selects", "toolbar-commands", "fab", "none"],
}


def load(path: str) -> dict:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"error: cannot read {path}: {e}")
    fp = doc.get("fingerprint", doc)
    return {"name": doc.get("brand") or doc.get("name") or Path(path).stem, "fingerprint": fp, "path": path}


def validate(fp: dict) -> list[str]:
    errs = []
    for axis, weight in FINGERPRINT_AXES.items():
        if axis not in fp:
            errs.append(f"missing axis '{axis}' (allowed: {', '.join(ALLOWED[axis])})")
        elif fp[axis] not in ALLOWED[axis]:
            errs.append(f"axis '{axis}' has unknown value '{fp[axis]}' (allowed: {', '.join(ALLOWED[axis])})")
    for axis in fp:
        if axis not in FINGERPRINT_AXES:
            errs.append(f"unknown axis '{axis}'")
    return errs


def similarity(a: dict, b: dict) -> dict:
    total_w = sum(FINGERPRINT_AXES.values())
    struct_w = sum(w for ax, w in FINGERPRINT_AXES.items() if ax in STRUCTURAL_AXES)
    cos_w = total_w - struct_w
    same_total = same_struct = same_cos = 0.0
    shared, differing = [], []
    for axis, w in FINGERPRINT_AXES.items():
        eq = a.get(axis) == b.get(axis) and a.get(axis) is not None
        if eq:
            same_total += w
            shared.append(axis)
            if axis in STRUCTURAL_AXES:
                same_struct += w
            else:
                same_cos += w
        else:
            differing.append(axis)
    return {"overall": round(same_total / total_w, 3), "structural": round(same_struct / struct_w, 3),
            "cosmetic": round(same_cos / cos_w, 3), "shared_axes": shared, "differing_axes": differing}


def verdict(sim: dict, threshold: float) -> str:
    if sim["structural"] >= threshold and sim["cosmetic"] >= threshold:
        return "NEAR-DUPLICATE"
    if sim["structural"] >= threshold:
        return "COSMETIC-ONLY"
    return "DISTINCT"


def compare(docs: list[dict], threshold: float) -> dict:
    pairs = []
    for a, b in itertools.combinations(docs, 2):
        sim = similarity(a["fingerprint"], b["fingerprint"])
        v = verdict(sim, threshold)
        pairs.append({"a": a["name"], "b": b["name"], **sim, "verdict": v,
                      "structural_shared": [ax for ax in sim["shared_axes"] if ax in STRUCTURAL_AXES]})
    failing = [p for p in pairs if p["verdict"] != "DISTINCT"]
    return {"threshold": threshold, "systems": [d["name"] for d in docs], "pairs": pairs,
            "pass": not failing, "failing_pairs": len(failing)}


def format_compare(rep: dict) -> str:
    lines = [f"fingerprint compare — threshold {rep['threshold']} — {'PASS' if rep['pass'] else 'FAIL'} "
             f"({rep['failing_pairs']} pair(s) too similar)"]
    for p in rep["pairs"]:
        lines.append(f"\n{p['a']} vs {p['b']}: {p['verdict']}  structural {p['structural']}  cosmetic {p['cosmetic']}  overall {p['overall']}")
        if p["verdict"] != "DISTINCT":
            lines.append("  shared structure: " + ", ".join(p["structural_shared"]))
            lines.append("  to differentiate, change at least two of: navigation_model, layout_topology, "
                         "content_density, surface_strategy, image_strategy, metadata_density, cta_strategy")
        else:
            lines.append("  differs on: " + ", ".join(p["differing_axes"]))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--brand", default="brand-name")
    p = sub.add_parser("validate"); p.add_argument("file")
    p = sub.add_parser("compare"); p.add_argument("files", nargs="+"); p.add_argument("--json", action="store_true")
    p.add_argument("--threshold", type=float, default=0.7, help="structural similarity at/above which two systems are 'the same layout architecture' (default 0.7 = about 70%% of structural weight shared)")
    args = ap.parse_args(argv)

    if args.cmd == "init":
        print(json.dumps({"brand": args.brand, "fingerprint": {ax: "" for ax in FINGERPRINT_AXES},
                          "_allowed_values": ALLOWED}, indent=2))
        return
    if args.cmd == "validate":
        errs = validate(load(args.file)["fingerprint"])
        if errs:
            print("\n".join("ERROR " + e for e in errs))
            sys.exit(1)
        print("ok")
        return
    if args.cmd == "compare":
        if len(args.files) < 2:
            sys.exit("error: compare needs at least two fingerprint files")
        docs = [load(f) for f in args.files]
        bad = False
        for d in docs:
            for e in validate(d["fingerprint"]):
                print(f"ERROR {d['path']}: {e}")
                bad = True
        if bad:
            sys.exit(1)
        rep = compare(docs, args.threshold)
        print(json.dumps(rep, indent=2) if args.json else format_compare(rep))
        sys.exit(0 if rep["pass"] else 2)


if __name__ == "__main__":
    main()
