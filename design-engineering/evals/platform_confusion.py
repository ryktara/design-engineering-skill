"""Platform confusion matrix (Phase 6, Workstream D).

For every platform-evidence case: expected platform(s) vs what resolve_platform returned.
Outcomes per case: resolved-correct (a resolved platform is expected or acceptable and nothing forbidden),
unresolved (UNKNOWN; correct only when the case expects UNKNOWN), resolved-wrong (a forbidden or unexpected
platform resolved). Prints the matrix expected x resolved and the resolution rate.

Usage: python evals/platform_confusion.py [--files evals/development/platform-situational.json ...] [--json out.json]
"""
import argparse, json, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import de_semantic as sem  # noqa: E402

DEFAULT_FILES = ["evals/development/platform-situational.json", "evals/development/platform-evidence.json", "evals/development/platform.json"]
PLATFORMS = ["web", "mobile", "tablet", "desktop", "tv", "kiosk"]


def classify(case: dict, resolved: list[str]) -> str:
    exp = set(case.get("expect_platforms") or [])
    acc = set(case.get("acceptable") or [])
    forbid = set(case.get("forbid_platforms") or [])
    got = set(resolved)
    if case.get("expect_unknown"):
        return "unresolved" if not got else "resolved-wrong"
    if not got:
        return "unresolved"
    if got & forbid or (exp and not (got & (exp | acc))) or (not exp and got - acc):
        return "resolved-wrong"
    return "resolved-correct"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*", default=DEFAULT_FILES)
    ap.add_argument("--json")
    a = ap.parse_args()
    matrix = defaultdict(Counter); outcomes = Counter(); rows = []
    for f in a.files:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        for c in d.get("cases", []):
            if "expect_platforms" not in c and not c.get("expect_unknown"):
                continue
            ev = sem.resolve_platform(c["query"], None)
            resolved = sorted((ev.get("resolved") or {}).keys())
            expected = "UNKNOWN" if c.get("expect_unknown") else ",".join(sorted(c.get("expect_platforms") or [])) or "any"
            got = ",".join(resolved) or "UNKNOWN"
            outcome = classify(c, resolved)
            matrix[expected][got] += 1; outcomes[outcome] += 1
            rows.append({"id": c["id"], "file": f, "expected": expected, "resolved": got, "outcome": outcome})
    total = sum(outcomes.values()) or 1
    known = [r for r in rows if r["expected"] != "UNKNOWN"]
    resolution_rate = round(sum(1 for r in known if r["resolved"] != "UNKNOWN") / max(len(known), 1), 3)
    print(f"cases={total} resolved-correct={outcomes['resolved-correct']} unresolved={outcomes['unresolved']} resolved-wrong={outcomes['resolved-wrong']}")
    print(f"platform correctness (resolved-correct / all)={round(outcomes['resolved-correct'] / total, 3)} "
          f"false platform (resolved-wrong / all)={round(outcomes['resolved-wrong'] / total, 3)} resolution rate (known cases)={resolution_rate}")
    cols = sorted({g for m in matrix.values() for g in m})
    print("expected \\ resolved | " + " | ".join(cols))
    for e in sorted(matrix):
        print(f"{e:20s} | " + " | ".join(str(matrix[e].get(g, 0)) for g in cols))
    wrong = [r for r in rows if r["outcome"] == "resolved-wrong"]
    for r in wrong[:20]:
        print(f"  WRONG {r['id']}: expected {r['expected']} resolved {r['resolved']}")
    if a.json:
        json.dump({"outcomes": dict(outcomes), "platform_correctness": round(outcomes['resolved-correct'] / total, 3), "false_platform": round(outcomes['resolved-wrong'] / total, 3),
                   "resolution_rate": resolution_rate, "matrix": {e: dict(m) for e, m in matrix.items()}, "rows": rows}, open(a.json, "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
