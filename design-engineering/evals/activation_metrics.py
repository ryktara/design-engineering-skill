#!/usr/bin/env python3
"""Activation metrics over evals/activation/cases.json (180 frozen prompts).

  python evals/activation_metrics.py [--real] [--model claude-haiku-4-5-20251001] [--json] [--out path]

Proxy mode (default): the deterministic activation heuristic in de_core (kept honest against the
description's vocabulary). --real asks the installed `claude` CLI per prompt with the skill's
description; it aborts with status SKIPPED when the CLI is not authenticated for non-interactive use.

Metrics (ambiguous cases excluded from precision/recall; their behaviour is reported separately):
  precision = TP / (TP + FP)   recall = TP / (TP + FN)
  false_positive_rate = FP / (FP + TN)   false_negative_rate = FN / (FN + TP)
Exit: 0 computed · 6 real probe skipped (not authenticated) · 1 tool failure.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def description() -> str:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def real_decision(model: str, desc: str, prompt: str) -> str | None:
    q = (f"You are a coding agent deciding whether to load a skill. Skill description:\n\n{desc}\n\n"
         f"User request: \"{prompt}\"\n\nLoad this skill for that request? Answer exactly one word: YES or NO.")
    try:
        proc = subprocess.run(["claude", "-p", "--model", model, "--output-format", "text", q],
                              capture_output=True, text=True, encoding="utf-8", timeout=120, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = (proc.stdout or "") + (proc.stderr or "")
    if "Not logged in" in out or not re.search(r"\b(YES|NO)\b", out, re.I):
        return None
    return "activate" if re.search(r"\bYES\b", out, re.I) else "skip"


def compute(cases: list[dict], decide) -> dict:
    tp = fp = tn = fn = 0
    amb = {"activate": 0, "skip": 0, "ambiguous": 0}
    per_group = {}
    false_pos, false_neg = [], []
    for c in cases:
        got = decide(c["prompt"])
        g = per_group.setdefault(c["group"], {"n": 0, "correct": 0})
        g["n"] += 1
        if c["expect"] == "ambiguous":
            amb[got] = amb.get(got, 0) + 1
            g["correct"] += 1 if got != "activate" else 0  # deferring (skip/ambiguous) counts as acceptable for ambiguous prompts
            continue
        positive = c["expect"] == "activate"
        fired = got == "activate"
        if positive and fired:
            tp += 1; g["correct"] += 1
        elif positive and not fired:
            fn += 1; false_neg.append({"id": c["id"], "prompt": c["prompt"], "got": got})
        elif not positive and fired:
            fp += 1; false_pos.append({"id": c["id"], "prompt": c["prompt"]})
        else:
            tn += 1; g["correct"] += 1
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": round(prec, 3), "recall": round(rec, 3),
            "false_positive_rate": round(fp / (fp + tn), 3) if fp + tn else 0.0,
            "false_negative_rate": round(fn / (fn + tp), 3) if fn + tp else 0.0,
            "ambiguous_behaviour": amb, "per_group": per_group, "false_positives": false_pos, "false_negatives": false_neg}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)
    cases = json.loads((SKILL / "evals" / "activation" / "cases.json").read_text(encoding="utf-8"))["cases"]
    if args.limit:
        cases = cases[: args.limit]
    report = {"cases": len(cases), "proxy": compute(cases, lambda p: core.build_requirements(p)["activation"]["decision"])}
    if args.real:
        desc = description()
        first = real_decision(args.model, desc, cases[0]["prompt"])
        if first is None:
            report["real"] = {"status": "SKIPPED", "reason": "claude CLI not authenticated for non-interactive use or did not answer YES/NO"}
        else:
            cache = {cases[0]["prompt"]: first}

            def decide(p):
                if p not in cache:
                    cache[p] = real_decision(args.model, desc, p) or "skip"
                return cache[p]
            report["real"] = {"status": "OK", "model": args.model, **compute(cases, decide)}
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for mode in ("proxy", "real"):
            if mode not in report:
                continue
            r = report[mode]
            if r.get("status") == "SKIPPED":
                print(f"REAL_ACTIVATION: SKIPPED — {r['reason']}")
                continue
            print(f"{mode}: precision {r['precision']} recall {r['recall']} FPR {r['false_positive_rate']} FNR {r['false_negative_rate']} "
                  f"(TP {r['tp']} FP {r['fp']} TN {r['tn']} FN {r['fn']}); ambiguous→{r['ambiguous_behaviour']}")
            for g, v in r["per_group"].items():
                print(f"   {g:<10} {v['correct']}/{v['n']}")
            if r["false_positives"]:
                print("   false positives: " + "; ".join(f"{x['id']} '{x['prompt']}'" for x in r["false_positives"][:12]))
            if r["false_negatives"]:
                print("   false negatives: " + "; ".join(f"{x['id']} '{x['prompt']}' ({x['got']})" for x in r["false_negatives"][:12]))
    if args.real and report.get("real", {}).get("status") == "SKIPPED":
        sys.exit(6)


if __name__ == "__main__":
    main()
