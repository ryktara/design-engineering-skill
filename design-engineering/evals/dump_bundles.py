#!/usr/bin/env python3
"""Dump prompt + bundle guidance text (record ids stripped) for a blind bundle-quality review.

  python evals/dump_bundles.py evals/heldout-v3/cases.json --out research/runs/heldout-v3-bundles.json [--start 0 --count 100]
"""
import argparse, io, json, sys
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cases"); ap.add_argument("--out", required=True); ap.add_argument("--start", type=int, default=0); ap.add_argument("--count", type=int, default=10 ** 6)
    a = ap.parse_args()
    cases = json.loads(Path(a.cases).read_text(encoding="utf-8"))["cases"][a.start:a.start + a.count]
    records = core.load_records(); out = []
    for c in cases:
        g = core.guidance(c["prompt"], records)
        if g["status"] == "ABSTAIN":
            out.append({"id": c["id"], "prompt": c["prompt"], "status": "ABSTAIN", "reason": g.get("scope", {}).get("reason") or g.get("note"), "guidance": []})
            continue
        items = []
        for it in g["core"] + g["guardrails"]:
            layer = "CORE" if it["role"] == "core" else ("OPTIONAL NOTES" if str(it.get("selected_for", "")).startswith("recommended coverage") else "CRITICAL GUARDRAILS")
            items.append({"layer": layer, "role": it["role"], "title": it["title"], "guidance": it["guidance"], "covers": it.get("covers", []),
                          "implementation": it.get("implementation", {})})
        out.append({"id": c["id"], "prompt": c["prompt"], "status": g["status"], "requirements": {k: g["requirements"][k] for k in ("mode", "platform", "change_budget")},
                    "uncovered": g["metrics"].get("uncovered_required_concepts", []), "guidance": items})
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(out)} bundles to {a.out}")

if __name__ == "__main__":
    main()
