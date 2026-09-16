#!/usr/bin/env python3
"""Deterministic colour / token tooling (WCAG 2.x contrast, semantic token validation, type scale).

  python tokens.py contrast "#1E293B" "#F8FAFC"            # ratio + pass/fail table
  python tokens.py validate tokens.json [--platform web|mobile|desktop|tv] [--json]
  python tokens.py scale --base 16 --ratio 1.25 --platform web|tv|desktop|mobile
  python tokens.py init > tokens.json                      # semantic skeleton to fill in

tokens.json shape (any depth of nesting; leaf values are hex colours):
{
  "light": {"color": {"bg": {"canvas": "#…", "surface": "#…", "elevated": "#…"},
                      "text": {"primary": "#…", "secondary": "#…", "disabled": "#…", "on-action": "#…"},
                      "action": {"primary": "#…", "primary-hover": "#…", "primary-pressed": "#…"},
                      "border": {"default": "#…", "strong": "#…"},
                      "focus": {"ring": "#…"},
                      "feedback": {"success": "#…", "warning": "#…", "error": "#…", "info": "#…"}}},
  "dark": { same }
}
Contrast rules are WCAG 2.2 (1.4.3, 1.4.6, 1.4.11). Alpha channels are not composited; pass opaque colours.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def parse_hex(value: str) -> tuple[int, int, int]:
    m = HEX_RE.match(str(value).strip())
    if not m:
        raise ValueError(f"not a hex colour: {value!r}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:
        h = h[:6]  # alpha ignored (documented)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(parse_hex(a)), relative_luminance(parse_hex(b))
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def hue_family(hex_color: str) -> str:
    r, g, b = (c / 255 for c in parse_hex(hex_color))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 0.08:
        return "neutral"
    d = mx - mn
    if mx == r:
        h = (60 * ((g - b) / d) + 360) % 360
    elif mx == g:
        h = 60 * ((b - r) / d) + 120
    else:
        h = 60 * ((r - g) / d) + 240
    for name, lo, hi in (("red", 0, 15), ("orange", 15, 45), ("yellow", 45, 70), ("green", 70, 165),
                         ("cyan", 165, 200), ("blue", 200, 250), ("indigo", 250, 265), ("violet", 265, 290),
                         ("purple", 290, 320), ("magenta", 320, 345), ("red", 345, 361)):
        if lo <= h < hi:
            return name
    return "neutral"


def judge(ratio: float) -> dict:
    return {"ratio": ratio, "AA_normal_text": ratio >= 4.5, "AA_large_text": ratio >= 3.0,
            "AAA_normal_text": ratio >= 7.0, "AAA_large_text": ratio >= 4.5, "non_text_ui": ratio >= 3.0}


# ---------------------------------------------------------------------------
# Semantic token validation
# ---------------------------------------------------------------------------

REQUIRED_ROLES = [
    "color.bg.canvas", "color.bg.surface", "color.text.primary", "color.text.secondary",
    "color.action.primary", "color.text.on-action", "color.border.default", "color.focus.ring",
    "color.feedback.error", "color.feedback.success", "color.feedback.warning",
]
RECOMMENDED_ROLES = [
    "color.bg.elevated", "color.text.disabled", "color.action.primary-hover", "color.action.primary-pressed",
    "color.border.strong", "color.feedback.info", "color.action.destructive", "color.selection.bg",
]
# (foreground, background, minimum, label, level)
PAIRS = [
    ("color.text.primary", "color.bg.canvas", 4.5, "body text on canvas", "AA 1.4.3"),
    ("color.text.primary", "color.bg.surface", 4.5, "body text on surface", "AA 1.4.3"),
    ("color.text.secondary", "color.bg.canvas", 4.5, "secondary text on canvas", "AA 1.4.3"),
    ("color.text.secondary", "color.bg.surface", 4.5, "secondary text on surface", "AA 1.4.3"),
    ("color.text.on-action", "color.action.primary", 4.5, "label on primary action", "AA 1.4.3"),
    ("color.text.on-action", "color.action.primary-hover", 4.5, "label on hovered action", "AA 1.4.3"),
    ("color.text.on-action", "color.action.primary-pressed", 4.5, "label on pressed action", "AA 1.4.3"),
    ("color.action.primary", "color.bg.canvas", 3.0, "primary action against canvas", "AA 1.4.11"),
    ("color.border.default", "color.bg.canvas", 3.0, "default border against canvas (if it conveys a boundary)", "AA 1.4.11 (advisory)"),
    ("color.border.strong", "color.bg.canvas", 3.0, "strong border against canvas", "AA 1.4.11"),
    ("color.focus.ring", "color.bg.canvas", 3.0, "focus ring against canvas", "AA 1.4.11 / 2.4.13"),
    ("color.focus.ring", "color.bg.surface", 3.0, "focus ring against surface", "AA 1.4.11 / 2.4.13"),
    ("color.feedback.error", "color.bg.canvas", 4.5, "error text on canvas", "AA 1.4.3 (when used as text)"),
    ("color.feedback.success", "color.bg.canvas", 3.0, "success indicator on canvas", "AA 1.4.11"),
    ("color.feedback.warning", "color.bg.canvas", 3.0, "warning indicator on canvas", "AA 1.4.11"),
    ("color.bg.elevated", "color.bg.canvas", 1.05, "elevated surface distinguishable from canvas (heuristic)", "heuristic"),
]
ADVISORY_PAIRS = {"color.border.default", "color.bg.elevated"}

TV_EXTRA = [
    ("color.text.primary", "color.bg.canvas", 7.0, "TV body text (10-foot viewing) target", "heuristic: viewing distance"),
    ("color.focus.ring", "color.bg.surface", 4.5, "TV focus indicator must be obvious from 3 m", "heuristic: 10-foot UI"),
]


def flatten(node, prefix="") -> dict:
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(node, str):
        out[prefix] = node
    return out


def validate_tokens(doc: dict, platform: str = "web") -> dict:
    themes = {k: v for k, v in doc.items() if isinstance(v, dict) and k in ("light", "dark", "high-contrast")}
    if not themes:
        themes = {"light": doc}
    report = {"platform": platform, "themes": {}, "errors": 0, "warnings": 0}
    for theme, node in themes.items():
        flat = flatten(node)
        t = {"missing_required": [], "missing_recommended": [], "pairs": [], "invalid": [],
             "hue_families": {}}
        for role in REQUIRED_ROLES:
            if role not in flat:
                t["missing_required"].append(role)
        for role in RECOMMENDED_ROLES:
            if role not in flat:
                t["missing_recommended"].append(role)
        for role, val in flat.items():
            if role.startswith("color.") and not HEX_RE.match(val):
                t["invalid"].append(f"{role}={val!r} is not hex")
        pairs = PAIRS + (TV_EXTRA if platform == "tv" else [])
        for fg, bg, minimum, label, level in pairs:
            if fg in flat and bg in flat and HEX_RE.match(flat[fg]) and HEX_RE.match(flat[bg]):
                ratio = contrast_ratio(flat[fg], flat[bg])
                ok = ratio >= minimum
                severity = "warning" if (fg in ADVISORY_PAIRS or "heuristic" in level) else "error"
                t["pairs"].append({"pair": f"{fg} on {bg}", "ratio": ratio, "min": minimum, "ok": ok,
                                   "rule": level, "label": label, "severity": None if ok else severity})
                if not ok:
                    report[severity + "s"] += 1
        for role in ("color.action.primary", "color.action.destructive", "color.feedback.error",
                     "color.feedback.success", "color.feedback.warning", "color.feedback.info"):
            if role in flat and HEX_RE.match(flat[role]):
                t["hue_families"][role] = hue_family(flat[role])
        # semantic sanity: feedback colours must be distinguishable from each other and from primary
        fam = t["hue_families"]
        for a, b in (("color.feedback.error", "color.feedback.success"), ("color.feedback.error", "color.feedback.warning"),
                     ("color.feedback.error", "color.action.primary")):
            if a in fam and b in fam and fam[a] == fam[b]:
                t.setdefault("semantic_warnings", []).append(f"{a} and {b} share hue family '{fam[a]}'; roles may be confused")
                report["warnings"] += 1
        if "color.feedback.error" in fam and fam["color.feedback.error"] not in ("red", "magenta", "orange"):
            t.setdefault("semantic_warnings", []).append("error colour is not in the red family; document why")
            report["warnings"] += 1
        # disabled must be lower contrast than secondary, not higher (otherwise disabled reads as enabled)
        if all(r in flat for r in ("color.text.disabled", "color.text.secondary", "color.bg.canvas")):
            cd = contrast_ratio(flat["color.text.disabled"], flat["color.bg.canvas"])
            cs = contrast_ratio(flat["color.text.secondary"], flat["color.bg.canvas"])
            if cd >= cs:
                t.setdefault("semantic_warnings", []).append(f"disabled text ({cd}:1) is not visibly weaker than secondary text ({cs}:1)")
                report["warnings"] += 1
        # hover/pressed must differ from rest
        for state in ("primary-hover", "primary-pressed"):
            role = f"color.action.{state}"
            if role in flat and flat.get("color.action.primary", "").lower() == flat[role].lower():
                t.setdefault("semantic_warnings", []).append(f"{role} is identical to color.action.primary; state change is invisible")
                report["warnings"] += 1
        report["errors"] += len(t["missing_required"]) + len(t["invalid"])
        report["warnings"] += len(t["missing_recommended"])
        report["themes"][theme] = t
    if "dark" not in themes:
        report["notes"] = ["no dark theme supplied; if the product has one, validate it too"]
        report["warnings"] += 1
    report["ok"] = report["errors"] == 0
    return report


def format_report(rep: dict) -> str:
    lines = [f"tokens.py validate — platform {rep['platform']} — {'OK' if rep['ok'] else 'FAIL'} "
             f"({rep['errors']} errors, {rep['warnings']} warnings)"]
    for theme, t in rep["themes"].items():
        lines.append(f"\n[{theme}]")
        for m in t["missing_required"]:
            lines.append(f"  ERROR missing required role {m}")
        for m in t["invalid"]:
            lines.append(f"  ERROR {m}")
        for p in t["pairs"]:
            mark = "ok  " if p["ok"] else ("WARN" if p["severity"] == "warning" else "FAIL")
            lines.append(f"  {mark} {p['ratio']:>6}:1 (min {p['min']}) {p['label']} [{p['rule']}]")
        for w in t.get("semantic_warnings", []):
            lines.append(f"  WARN {w}")
        for m in t["missing_recommended"]:
            lines.append(f"  note missing recommended role {m}")
        if t["hue_families"]:
            lines.append("  hues: " + ", ".join(f"{k.split('.')[-1]}={v}" for k, v in t["hue_families"].items()))
    for n in rep.get("notes", []):
        lines.append(f"note: {n}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Type scale
# ---------------------------------------------------------------------------

# Base sizes reflect platform reading distance and density conventions.
# web/mobile 16 (1rem body), desktop 14 (Windows type ramp body 14 epx / macOS 13pt),
# tv 24 (Android TV body ~24-28 sp at 3 m), kiosk 20.
PLATFORM_BASE = {"web": 16, "mobile": 16, "desktop": 14, "tv": 24, "kiosk": 20}
ROLE_STEPS = [("display", 5), ("heading", 3), ("title", 2), ("body-large", 1), ("body", 0),
              ("label", -1), ("caption", -2)]
LINE_HEIGHT = {"display": 1.1, "heading": 1.2, "title": 1.25, "body-large": 1.5, "body": 1.5,
               "label": 1.4, "caption": 1.4}


def type_scale(base: float, ratio: float, platform: str) -> dict:
    scale = {}
    for role, step in ROLE_STEPS:
        size = base * (ratio ** step)
        size = round(size / 2) * 2 if platform in ("tv", "kiosk") else round(size)
        scale[role] = {"size": size, "line_height": LINE_HEIGHT[role],
                       "weight": 600 if role in ("display", "heading", "title") else 400}
    scale["numeric"] = {"size": scale["body"]["size"], "line_height": 1.3, "weight": 500,
                        "font_features": "tnum, lnum", "note": "tabular figures for tables and KPIs"}
    minimum = {"web": 12, "mobile": 12, "desktop": 11, "tv": 20, "kiosk": 16}[platform]
    for role, v in scale.items():
        if v["size"] < minimum:
            v["size_unclamped"] = v["size"]; v["size"] = minimum
    warnings = [f"{role} was {v['size_unclamped']}px, clamped to the {platform} floor of {minimum}px" for role, v in scale.items() if "size_unclamped" in v]
    _unused = [f"{role} {v['size']}px is below the {platform} floor of {minimum}px" for role, v in scale.items()
                if v["size"] < minimum]
    return {"platform": platform, "base": base, "ratio": ratio, "roles": scale, "warnings": warnings,
            "unit_note": {"web": "px shown; emit rem = px/16", "mobile": "pt/sp", "desktop": "epx/pt",
                          "tv": "sp/pt; verify at 3 m on a real panel", "kiosk": "px at native panel scale"}[platform]}


SKELETON = {
    "light": {"color": {
        "bg": {"canvas": "#F7F8FA", "surface": "#FFFFFF", "elevated": "#FFFFFF"},
        "text": {"primary": "#1B1F24", "secondary": "#4B5563", "disabled": "#9CA3AF", "on-action": "#FFFFFF"},
        "action": {"primary": "#0B57D0", "primary-hover": "#0847AD", "primary-pressed": "#063A8E", "destructive": "#B3261E"},
        "border": {"default": "#D0D5DD", "strong": "#667085"},
        "focus": {"ring": "#0B57D0"},
        "selection": {"bg": "#DCE7FB"},
        "feedback": {"success": "#1B7F3B", "warning": "#8A5A00", "error": "#B3261E", "info": "#0B57D0"}}},
    "dark": {"color": {
        "bg": {"canvas": "#0F1115", "surface": "#171A21", "elevated": "#1F2330"},
        "text": {"primary": "#ECEEF2", "secondary": "#B3B9C6", "disabled": "#6B7280", "on-action": "#0F1115"},
        "action": {"primary": "#8AB4F8", "primary-hover": "#A5C4FA", "primary-pressed": "#C2D7FC", "destructive": "#F2B8B5"},
        "border": {"default": "#2C3140", "strong": "#7A8399"},
        "focus": {"ring": "#8AB4F8"},
        "selection": {"bg": "#243B63"},
        "feedback": {"success": "#6FD38B", "warning": "#F5C451", "error": "#F2B8B5", "info": "#8AB4F8"}}},
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("contrast"); p.add_argument("fg"); p.add_argument("bg"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("validate"); p.add_argument("file"); p.add_argument("--platform", default="web", choices=sorted(PLATFORM_BASE)); p.add_argument("--json", action="store_true")
    p = sub.add_parser("scale"); p.add_argument("--base", type=float); p.add_argument("--ratio", type=float, default=1.25); p.add_argument("--platform", default="web", choices=sorted(PLATFORM_BASE)); p.add_argument("--json", action="store_true")
    sub.add_parser("init")
    args = ap.parse_args(argv)

    if args.cmd == "contrast":
        try:
            ratio = contrast_ratio(args.fg, args.bg)
        except ValueError as e:
            sys.exit(f"error: {e}")
        j = judge(ratio)
        if args.json:
            print(json.dumps(j))
        else:
            print(f"{args.fg} on {args.bg}: {ratio}:1  "
                  f"AA text {'pass' if j['AA_normal_text'] else 'FAIL'} · AA large/UI {'pass' if j['AA_large_text'] else 'FAIL'} · "
                  f"AAA text {'pass' if j['AAA_normal_text'] else 'fail'}  hues {hue_family(args.fg)}/{hue_family(args.bg)}")
        return
    if args.cmd == "validate":
        try:
            doc = json.loads(open(args.file, encoding="utf-8").read())
        except (OSError, json.JSONDecodeError) as e:
            sys.exit(f"error: cannot read {args.file}: {e}")
        rep = validate_tokens(doc, args.platform)
        print(json.dumps(rep, indent=2) if args.json else format_report(rep))
        sys.exit(0 if rep["ok"] else 1)
    if args.cmd == "scale":
        base = args.base or PLATFORM_BASE[args.platform]
        sc = type_scale(base, args.ratio, args.platform)
        if args.json:
            print(json.dumps(sc, indent=2))
        else:
            print(f"type scale — {args.platform}, base {base}, ratio {args.ratio} ({sc['unit_note']})")
            for role, v in sc["roles"].items():
                extra = f"  {v.get('font_features')}" if v.get("font_features") else ""
                print(f"  {role:<11} {v['size']:>4}  lh {v['line_height']}  w{v['weight']}{extra}")
            for w in sc["warnings"]:
                print("  WARN " + w)
        return
    if args.cmd == "init":
        print(json.dumps(SKELETON, indent=2))


if __name__ == "__main__":
    main()
