#!/usr/bin/env python3
"""Mode confusion matrix over the mode development suites (expected primary-any vs predicted primary/secondary).

  python evals/mode_confusion.py [--json]
"""
import io, json, sys
from collections import Counter, defaultdict
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    cases = []
    for f in ("mode.json", "mode-intent.json"):
        p = SKILL / "evals" / "development" / f
        if p.exists():
            cases += json.loads(p.read_text(encoding="utf-8"))["cases"]
    matrix = defaultdict(Counter); primary_ok = secondary_ok = 0; n = 0; fundamental = 0
    for c in cases:
        exp = c.get("expect_primary_any") or ([c["expect_primary"]] if c.get("expect_primary") else [])
        if not exp:
            continue
        req = core.build_requirements(c["query"]); pred = req["mode"]
        n += 1
        key = "/".join(sorted(exp))
        matrix[key][pred[0]] += 1
        if pred[0] in exp:
            primary_ok += 1
        elif set(pred[:2]) & set(exp):
            secondary_ok += 1
        elif pred[0] == "create" and "create" not in exp:
            fundamental += 1
    confusions = Counter()
    for exp, preds in matrix.items():
        for p_, k in preds.items():
            if p_ not in exp.split("/"):
                confusions[f"{exp} -> {p_}"] += k
    out = {"cases": n, "primary_correct": primary_ok, "secondary_credit": secondary_ok, "incorrect": n - primary_ok - secondary_ok,
           "fundamental_create_misses": fundamental, "matrix": {k: dict(v) for k, v in matrix.items()}, "top_confusions": confusions.most_common(12)}
    if "--json" in sys.argv:
        print(json.dumps(out, indent=1))
    else:
        print(f"cases {n}: primary {primary_ok}, secondary credit {secondary_ok}, incorrect {n - primary_ok - secondary_ok}, fundamental create-misses {fundamental}")
        for k, v in out["top_confusions"]:
            print(f"  {k}: {v}")
    return out


if __name__ == "__main__":
    main()
