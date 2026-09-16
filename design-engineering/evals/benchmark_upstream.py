#!/usr/bin/env python3
"""Benchmark harness (method v2): upstream ui-ux-pro-max retrieval vs design-engineering.

  python evals/benchmark_upstream.py --upstream <clone> --out-json research/benchmark-results.json [--reps 7] [--report research/BENCHMARK-RESULTS.md]
  python evals/benchmark_upstream.py --render research/benchmark-results.json --report research/BENCHMARK-RESULTS.md   # regenerate Markdown only

Canonical output is the JSON; Markdown is rendered from it (validate_skill.py checks the two agree).

Scoring (methodology v2): for each query, the fraction of human-listed relevant terms present in the
returned guidance text (higher is better) and the fraction of off-target terms present (lower is
better). Term lists live in evals/development/benchmark.json and were written by the skill author;
this measures topical fit, not final UI quality.

Timing: `cold` = one subprocess per query (interpreter start + load + search + exit), both systems
measured the same way; `warm` = in-process search with records already loaded (ours only; upstream
exposes no stable in-process API and its caches are per process). Median and p95 over --reps.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

METHOD = "v2"
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def coverage(text: str, terms: list[str]) -> float:
    if not terms:
        return 0.0
    low = text.lower()
    return sum(1 for t in terms if t.lower() in low) / len(terms)


def timed_subprocess(cmd: list[str], reps: int) -> tuple[dict, str]:
    times, out = [], ""
    for _ in range(reps):
        t = time.perf_counter()
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=ENV)
        times.append(time.perf_counter() - t)
        out = proc.stdout
    times.sort()
    return {"median_ms": round(statistics.median(times) * 1000), "p95_ms": round(times[max(0, int(len(times) * 0.95) - 1)] * 1000), "n": reps}, out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def run(upstream: Path, reps: int) -> dict:
    search_py = upstream / "src" / "ui-ux-pro-max" / "scripts" / "search.py"
    if not search_py.exists():
        sys.exit(f"error: {search_py} not found")
    cases = json.loads((SKILL / "evals" / "development" / "benchmark.json").read_text(encoding="utf-8"))["cases"]
    records = core.load_records()
    upstream_rev = subprocess.run(["git", "-C", str(upstream), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"
    queries = []
    for c in cases:
        up_t, up_out = timed_subprocess([sys.executable, str(search_py), c["query"], "--json"], reps)
        try:
            up_data = json.loads(up_out)
        except json.JSONDecodeError:
            up_data = {}
        up_text = json.dumps(up_data.get("results", []), ensure_ascii=False)
        our_cold_t, our_out = timed_subprocess([sys.executable, str(SKILL / "scripts" / "advise.py"), "search", c["query"], "--json", "--exit-zero"], reps)
        warm = []
        for _ in range(reps):
            t = time.perf_counter()
            res = core.search(c["query"], records, k=5)
            warm.append(time.perf_counter() - t)
        warm.sort()
        our_text = json.dumps(res["results"], ensure_ascii=False)
        gwarm = []
        for _ in range(reps):
            t = time.perf_counter()
            g = core.guidance(c["query"], records)
            gwarm.append(time.perf_counter() - t)
        gwarm.sort()
        g_items = g["core"] + g["guardrails"]
        g_text = json.dumps([{k: v for k, v in it.items() if k in ("title", "guidance", "use_when", "avoid_when", "implementation", "covers")} for it in g_items], ensure_ascii=False)
        queries.append({
            "id": c["id"], "category": c["category"], "query": c["query"],
            "upstream": {"domain": up_data.get("domain"), "top": [next(iter(r.values())) for r in up_data.get("results", [])][:3] if up_data else [],
                         "relevant": round(coverage(up_text, c["relevant_terms"]), 3), "offtarget": round(coverage(up_text, c.get("offtarget_terms", [])), 3),
                         "empty": not up_data.get("results"), "cold": up_t},
            "ours": {"platforms": res["signals"]["platforms"], "modes": res["signals"]["modes"][:1], "top": [r["id"] for r in res["results"]][:3],
                     "relevant": round(coverage(our_text, c["relevant_terms"]), 3), "offtarget": round(coverage(our_text, c.get("offtarget_terms", [])), 3),
                     "empty": res["count"] == 0, "status": res["status"], "facet_coverage": res["coverage"]["facet_coverage"],
                     "cold": our_cold_t, "warm": {"median_ms": round(statistics.median(warm) * 1000, 1), "p95_ms": round(warm[max(0, int(len(warm) * 0.95) - 1)] * 1000, 1), "n": reps}},
            "ours_guidance": {"top": [it["id"] for it in g_items][:4], "relevant": round(coverage(g_text, c["relevant_terms"]), 3),
                              "offtarget": round(coverage(g_text, c.get("offtarget_terms", [])), 3), "empty": not g_items, "status": g["status"],
                              "bundle_size": g["metrics"]["bundle_size"], "concern_coverage": g["metrics"]["coverage_ratio"], "bytes": len(g_text),
                              "warm": {"median_ms": round(statistics.median(gwarm) * 1000, 1), "p95_ms": round(gwarm[max(0, int(len(gwarm) * 0.95) - 1)] * 1000, 1), "n": reps}},
        })
    n = len(queries)

    def mean(key, side):
        return round(sum(q[side][key] for q in queries) / n, 3)

    def med(side, kind):
        return round(statistics.median(q[side][kind]["median_ms"] for q in queries))

    agg = {
        "queries": n,
        "upstream": {"mean_relevant": mean("relevant", "upstream"), "mean_offtarget": mean("offtarget", "upstream"),
                     "empty_results": sum(q["upstream"]["empty"] for q in queries), "cold_median_ms": med("upstream", "cold"),
                     "cold_p95_ms": max(q["upstream"]["cold"]["p95_ms"] for q in queries)},
        "ours": {"mean_relevant": mean("relevant", "ours"), "mean_offtarget": mean("offtarget", "ours"),
                 "empty_results": sum(q["ours"]["empty"] for q in queries), "cold_median_ms": med("ours", "cold"),
                 "cold_p95_ms": max(q["ours"]["cold"]["p95_ms"] for q in queries), "warm_median_ms": med("ours", "warm"),
                 "mean_facet_coverage": round(sum(q["ours"]["facet_coverage"] for q in queries) / n, 3)},
        "ours_guidance": {"mean_relevant": mean("relevant", "ours_guidance"), "mean_offtarget": mean("offtarget", "ours_guidance"),
                          "empty_results": sum(q["ours_guidance"]["empty"] for q in queries), "warm_median_ms": med("ours_guidance", "warm"),
                          "mean_bundle_size": round(sum(q["ours_guidance"]["bundle_size"] for q in queries) / n, 2),
                          "mean_concern_coverage": round(sum(q["ours_guidance"]["concern_coverage"] for q in queries) / n, 3),
                          "mean_bytes": round(sum(q["ours_guidance"]["bytes"] for q in queries) / n)},
        "upstream_higher": [q["id"] for q in queries if q["upstream"]["relevant"] > q["ours"]["relevant"]],
        "ties": [q["id"] for q in queries if q["upstream"]["relevant"] == q["ours"]["relevant"]],
    }
    by_cat = {}
    for q in queries:
        d = by_cat.setdefault(q["category"], {"n": 0, "upstream": 0.0, "ours": 0.0})
        d["n"] += 1; d["upstream"] += q["upstream"]["relevant"]; d["ours"] += q["ours"]["relevant"]
    for d in by_cat.values():
        d["upstream"] = round(d["upstream"] / d["n"], 3); d["ours"] = round(d["ours"] / d["n"], 3)
    return {
        "schema": "benchmark-results/v1", "benchmark_method": METHOD, "date": dt.date.today().isoformat(),
        "versions": {"python": platform.python_version(), "os": platform.platform(), "upstream_revision": upstream_rev,
                     "records": len(records), "de_core_sha": sha(SKILL / "scripts" / "de_core.py"), "cases_sha": sha(SKILL / "evals" / "development" / "benchmark.json")},
        "timing_method": {"cold": "subprocess per query incl. interpreter start, both systems identically", "warm": "in-process, records preloaded, ours only (search k=5 and guidance bundle)", "reps": reps},
        "queries": queries, "aggregate": agg, "by_category": by_cat, "failures": [q["id"] for q in queries if q["ours"]["empty"]],
    }


def render(data: dict) -> str:
    a = data["aggregate"]
    L = [f"# Benchmark: upstream ui-ux-pro-max vs design-engineering (method {data['benchmark_method']})", "",
         f"Generated {data['date']} from `research/benchmark-results.json` by `evals/benchmark_upstream.py --render`; do not edit numbers by hand.",
         f"Upstream revision `{data['versions']['upstream_revision']}`; ours: {data['versions']['records']} records, de_core `{data['versions']['de_core_sha']}`, cases `{data['versions']['cases_sha']}`; Python {data['versions']['python']}.", "",
         "Scoring: fraction of human-listed relevant terms present in returned guidance (higher better) and fraction of off-target terms present (lower better). Term lists were authored by the skill author; this measures topical fit, not final UI quality.",
         f"Timing: cold = {data['timing_method']['cold']}; warm = {data['timing_method']['warm']}; {data['timing_method']['reps']} repetitions, median and p95.", "",
         "## Aggregate", "", "| Metric | Upstream | Ours |", "|---|---|---|",
         f"| mean relevant-term coverage | {a['upstream']['mean_relevant']:.3f} | {a['ours']['mean_relevant']:.3f} |",
         f"| mean off-target-term coverage | {a['upstream']['mean_offtarget']:.3f} | {a['ours']['mean_offtarget']:.3f} |",
         f"| empty results | {a['upstream']['empty_results']} | {a['ours']['empty_results']} |",
         f"| cold latency median / p95 (ms) | {a['upstream']['cold_median_ms']} / {a['upstream']['cold_p95_ms']} | {a['ours']['cold_median_ms']} / {a['ours']['cold_p95_ms']} |",
         f"| warm latency median (ms) | n/a | {a['ours']['warm_median_ms']} |",
         f"| mean required-facet coverage | n/a | {a['ours']['mean_facet_coverage']:.3f} |", "",
         "Guidance bundle (Phase 3 `advise.py guidance`, same terms and scoring; additive column, method unchanged):", "",
         "| metric | ours (guidance bundle) |", "|---|---|",
         f"| mean relevant-term coverage | {a['ours_guidance']['mean_relevant']:.3f} |",
         f"| mean off-target-term coverage | {a['ours_guidance']['mean_offtarget']:.3f} |",
         f"| empty results | {a['ours_guidance']['empty_results']} |",
         f"| warm latency median (ms) | {a['ours_guidance']['warm_median_ms']} |",
         f"| mean bundle size / concern coverage / bytes | {a['ours_guidance']['mean_bundle_size']} / {a['ours_guidance']['mean_concern_coverage']:.3f} / {a['ours_guidance']['mean_bytes']} |", "",
         "## By category (relevant-term coverage)", "", "| Category | n | Upstream | Ours |", "|---|---|---|---|"]
    for cat, d in sorted(data["by_category"].items()):
        L.append(f"| {cat} | {d['n']} | {d['upstream']:.3f} | {d['ours']:.3f} |")
    L += ["", "## Per query", "", "| Query | Upstream domain / top | rel ↑ | off ↓ | Ours signals / top | rel ↑ | off ↓ | status |", "|---|---|---|---|---|---|---|---|"]
    for q in data["queries"]:
        u, o = q["upstream"], q["ours"]
        L.append(f"| {q['query']} | {u['domain']}: {', '.join(map(str, u['top'])) or '—'} | {u['relevant']:.2f} | {u['offtarget']:.2f} | "
                 f"{list(o['platforms'])}/{o['modes']}: {', '.join(o['top']) or '—'} | {o['relevant']:.2f} | {o['offtarget']:.2f} | {o['status']} |")
    L += ["", "## Where upstream scored higher", ""] + ([f"- {i}" for i in a["upstream_higher"]] or ["- none in this set"])
    L += ["", "## Ties", ""] + ([f"- {i}" for i in a["ties"]] or ["- none"])
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--upstream")
    ap.add_argument("--out-json", default=str(SKILL.parent / "research" / "benchmark-results.json"))
    ap.add_argument("--report", default=str(SKILL.parent / "research" / "BENCHMARK-RESULTS.md"))
    ap.add_argument("--reps", type=int, default=7)
    ap.add_argument("--render", help="render Markdown from an existing JSON instead of running")
    args = ap.parse_args(argv)
    if args.render:
        data = json.loads(Path(args.render).read_text(encoding="utf-8"))
    else:
        if not args.upstream:
            sys.exit("error: --upstream <clone> is required unless --render is given")
        data = run(Path(args.upstream), args.reps)
        Path(args.out_json).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out_json}")
    Path(args.report).write_text(render(data), encoding="utf-8")
    print(f"wrote {args.report}")
    a = data["aggregate"]
    print(f"relevant {a['upstream']['mean_relevant']} vs {a['ours']['mean_relevant']}; offtarget {a['upstream']['mean_offtarget']} vs {a['ours']['mean_offtarget']}; "
          f"cold ms {a['upstream']['cold_median_ms']} vs {a['ours']['cold_median_ms']}; warm ms {a['ours']['warm_median_ms']}")


if __name__ == "__main__":
    main()
