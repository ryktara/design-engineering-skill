#!/usr/bin/env python3
"""Concept failure decomposition over development cases with expected concept ids.

For every expected concept that is not in the delivered bundle, classify the earliest failing layer:
  1 absent_from_ontology  2 not_demanded  3 demanded_no_record  4 record_not_candidate  5 candidate_dropped_by_selector
  python evals/concept_diagnostics.py [--json] [--cases path ...]
"""
import io, json, sys
from collections import Counter
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402
import de_semantic as sem  # noqa: E402
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    args = sys.argv[1:]
    files = [a for a in args if a.endswith(".json")] or [str(SKILL / "evals" / "development" / "guidance.json")]
    records = core.load_records(); by_rec = {r["id"]: r for r in records}
    layers = Counter(); examples = {}
    total = hits = 0
    for f in files:
        for c in json.loads(Path(f).read_text(encoding="utf-8"))["cases"]:
            exp = c.get("expect_concepts") or c.get("required_concepts") or []
            if not exp:
                continue
            q = c.get("query") or c.get("prompt")
            req = core.build_requirements(q); concerns = core.derive_concerns(req)
            g = core.guidance(q, records, requirements=req, explain=True)
            bundle = g["core"] + g["guardrails"]; got = set().union(*(set(it.get("concepts", [])) for it in bundle)) if bundle else set()
            demanded = {x["concept"] for x in concerns["required_concepts"]} | {x["concept"] for x in concerns["recommended_concepts"]}
            trace = {t["concept"]: t for t in g.get("concept_trace", [])}
            for cid in exp:
                total += 1
                if cid in got:
                    hits += 1; continue
                if cid not in sem.CONCEPTS:
                    layer = "1_absent_from_ontology"
                elif cid not in demanded:
                    layer = "2_not_demanded"
                elif not any(cid in r.get("concepts", []) for r in records):
                    layer = "3_demanded_no_record"
                elif not trace.get(cid, {}).get("candidate_records"):
                    layer = "4_record_not_candidate"
                else:
                    layer = "5_candidate_dropped_by_selector"
                layers[layer] += 1
                examples.setdefault(layer, []).append({"case": c["id"], "concept": cid, "why": trace.get(cid, {}).get("why")})
    out = {"expected": total, "hit": hits, "recall": round(hits / total, 3) if total else None, "misses_by_layer": dict(layers), "examples": {k: v[:6] for k, v in examples.items()}}
    if "--json" in args:
        print(json.dumps(out, indent=1))
    else:
        print(f"expected {total}, hit {hits} (recall {out['recall']}); misses by layer: {dict(layers)}")
        for k, v in examples.items():
            for e in v[:4]:
                print(f"  {k}: {e['case']} {e['concept']} {e['why'] or ''}")
    return out


if __name__ == "__main__":
    main()
