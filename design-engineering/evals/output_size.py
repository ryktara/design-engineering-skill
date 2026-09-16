"""Output-size measurement (token estimate = chars/4) over the development guidance queries plus held-out v1 prompts,
mirroring the Phase 3-5 measurement. Usage: python evals/output_size.py --out research/runs/phase6-output-size.json"""
import argparse, io, json, statistics, subprocess, sys, time
from pathlib import Path
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def pct(vals, p):
    vals = sorted(vals); return vals[min(len(vals) - 1, int(round(p * (len(vals) - 1))))] if vals else None


def stats(vals):
    return {"n": len(vals), "mean": round(statistics.mean(vals), 1), "median": round(statistics.median(vals), 1), "p95": pct(vals, 0.95), "max": max(vals)} if vals else {}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); a = ap.parse_args()
    queries = []
    for f in ("evals/development/guidance.json", "evals/development/p5r-guidance.json", "evals/development/purity.json"):
        p = SKILL / f
        if p.exists():
            queries += [c["query"] for c in json.loads(p.read_text(encoding="utf-8"))["cases"]]
    hv1 = SKILL / "evals" / "heldout" / "cases.json"
    if hv1.exists():
        queries += [c["prompt"] for c in json.loads(hv1.read_text(encoding="utf-8"))["cases"] if c.get("prompt")]
    queries = list(dict.fromkeys(queries))
    recs = core.load_records(); t0 = time.time()
    md, js, bsize, btok, dmd = [], [], [], [], []
    for q in queries:
        g = core.guidance(q, recs)
        md.append(len(core.format_guidance_md(g)) / 4); js.append(len(json.dumps(g, ensure_ascii=False)) / 4)
        bsize.append(g["metrics"].get("bundle_size", 0)); btok.append(g["metrics"].get("bundle_tokens", 0))
        try:
            d = core.direction(q, records=recs); dmd.append(len(core.format_direction_md(d)) / 4)
        except Exception:
            pass
    build = subprocess.run([sys.executable, str(SKILL / "evals" / "build_hash.py")], capture_output=True, text=True).stdout.strip()
    out = {"note": "token estimate = chars/4; development guidance + purity + held-out v1 queries; frozen Phase 6 build c4", "build": build,
           "stats": {"guidance_md_tokens": stats(md), "guidance_json_tokens": stats(js), "direction_md_tokens": stats(dmd), "bundle_size": stats(bsize), "bundle_tokens": stats(btok),
                     "empty_bundles": sum(1 for b in bsize if b == 0), "queries": len(queries)}, "elapsed_s": round(time.time() - t0, 1)}
    print(json.dumps(out["stats"], indent=1))
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
