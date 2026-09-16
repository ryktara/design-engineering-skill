#!/usr/bin/env python3
"""Re-run the skill steps (inspect → requirements → guidance → direction) for every Phase 5 real-project task on the
current build and score them mechanically against each task's pre-registered 00-expectation.json. Also scores the
recorded c1 outputs (02-requirements.json / 03-guidance.json) with the same function so the two builds are compared
by one yardstick. Implementation/render outcomes are NOT re-run; they belong to the round that produced them.

usage: python evals/rescore_projects.py --label c2 [--tasks p5-01,p5-02] [--out research/runs/phase5-c2-projects-rescore.json]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parent
P5 = ROOT / "research" / "phase5-projects"
P6 = ROOT / "research" / "phase6-projects"
PY = sys.executable


def project_dir(codebase: str):
    if codebase.startswith("p3-"):
        return ROOT / "research" / "phase3-projects" / codebase / "project"
    if codebase.startswith("p6-"):
        return P6 / codebase / "project"
    return P5 / codebase / "project"


def run(args, cwd=SKILL):
    return subprocess.run([PY, *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")


def tasks_table(phase: int = 5):
    out = {}
    root = P6 if phase == 6 else P5
    for line in (root / "TASKS.md").read_text(encoding="utf-8").splitlines():
        if phase == 6:
            m = re.match(r"\|\s*(p6-\d\d)\s*\|\s*([a-z0-9-]+)\s*\|\s*([a-z() ]+?)\s*\|\s*[^|]*\|\s*[^|]*\|\s*(.+?)\s*\|\s*$", line)
        else:
            m = re.match(r"\|\s*(p5-\d\d)\s*\|\s*([a-z0-9-]+)\s*\|\s*([a-z]+)\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            tid, codebase, plat, sentence = m.groups()
            out[tid] = {"codebase": codebase, "platform": plat.strip(), "sentence": sentence, "project": project_dir(codebase)}
    return out


def score(exp: dict, req: dict, g: dict) -> dict:
    plats = [p for p in req.get("platform", []) if p != "tablet"]
    missing_plat = any((m.get("field") == "platform") if isinstance(m, dict) else str(m).startswith("platform") for m in req.get("missing", []))
    want = exp.get("platform")
    if want in plats and all(p == want or (want == "kiosk" and p == "web") for p in plats):
        pc = "yes"
    elif not plats and missing_plat:
        pc = "unknown"
    elif want in plats:
        pc = "extra"   # right platform present but another one asserted too
    else:
        pc = "wrong"
    bundle = (g.get("core") or []) + (g.get("guardrails") or [])
    delivered = sorted(set().union(*(set(it.get("concepts", [])) for it in bundle)) if bundle else set())
    expc = exp.get("expected_concepts", []); crit = exp.get("critical_concepts", []); forb = exp.get("forbidden_concepts", [])
    top2 = (req.get("mode") or [])[:2]
    acc = set(exp.get("acceptable_modes", []))
    mode_ok = "yes" if top2 and top2[0] in acc else ("acceptable" if set(top2) & acc else "no")
    return {
        "platform_expected": want, "platform_resolved": plats, "platform_correct": pc, "missing_platform_entry": missing_plat,
        "artifact_state_expected": exp.get("artifact_state"), "artifact_state_resolved": (req.get("intent") or {}).get("artifact_state"),
        "artifact_state_correct": (req.get("intent") or {}).get("artifact_state") == exp.get("artifact_state"),
        "mode_expected": sorted(acc), "mode_resolved": top2, "mode_correct": mode_ok,
        "scope_kind_expected": exp.get("scope_kind", "in-scope"), "scope_kind_resolved": (req.get("scope") or {}).get("kind"),
        "scope_correct": (req.get("scope") or {}).get("kind") == exp.get("scope_kind", "in-scope"),
        "status": g.get("status"), "bundle_ids": [it["id"] for it in bundle], "bundle_tokens": (g.get("metrics") or {}).get("bundle_tokens"),
        "expected_concepts": expc, "critical_concepts": crit, "delivered_concepts": delivered,
        "concept_recall": round(sum(1 for c in expc if c in delivered) / len(expc), 3) if expc else None,
        "critical_recall": round(sum(1 for c in crit if c in delivered) / len(crit), 3) if crit else None,
        "forbidden_delivered": sorted(set(forb) & set(delivered)),
        "change_budget": req.get("change_budget"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="c2")
    ap.add_argument("--tasks", default="")
    ap.add_argument("--out", default=None)
    ap.add_argument("--phase", type=int, default=5)
    args = ap.parse_args(argv)
    table = tasks_table(args.phase)
    base = P6 if args.phase == 6 else P5
    build = run(["evals/build_hash.py"]).stdout.strip()
    only = set(args.tasks.split(",")) if args.tasks else None
    results = []
    for tid, t in sorted(table.items()):
        if only and tid not in only:
            continue
        d = base / tid
        if not (d / "00-expectation.json").exists():
            continue
        exp = json.loads((d / "00-expectation.json").read_text(encoding="utf-8"))
        # c1 as recorded
        c1 = None
        try:
            req1 = json.loads((d / "02-requirements.json").read_text(encoding="utf-8"))
            g1 = json.loads((d / "03-guidance.json").read_text(encoding="utf-8"))
            c1 = score(exp, req1, g1)
        except (OSError, json.JSONDecodeError):
            pass
        # current build
        outdir = d / args.label
        outdir.mkdir(exist_ok=True)
        insp = run(["scripts/inspect_project.py", str(t["project"]), "--json"])
        (outdir / "01-inspect.json").write_text(insp.stdout, encoding="utf-8")
        req_p = run(["scripts/advise.py", "requirements", t["sentence"], "--project", str(outdir / "01-inspect.json"), "--pretty", "--explain"])
        (outdir / "02-requirements.json").write_text(req_p.stdout, encoding="utf-8")
        g_p = run(["scripts/advise.py", "guidance", t["sentence"], "--project", str(outdir / "01-inspect.json"), "--json", "--explain"])
        (outdir / "03-guidance.json").write_text(g_p.stdout, encoding="utf-8")
        g_md = run(["scripts/advise.py", "guidance", t["sentence"], "--project", str(outdir / "01-inspect.json"), "--explain"])
        (outdir / "03-guidance.md").write_text(g_md.stdout, encoding="utf-8")
        run(["scripts/advise.py", "direction", t["sentence"], "--project", str(outdir / "01-inspect.json"), "--out", str(outdir / "04-direction.json")])
        try:
            req2 = json.loads(req_p.stdout); g2 = json.loads(g_p.stdout)
            c2 = score(exp, req2, g2)
        except json.JSONDecodeError as e:
            c2 = {"error": f"{e}: {req_p.stderr[-300:]} {g_p.stderr[-300:]}"}
        (outdir / "score.json").write_text(json.dumps({"task": tid, "build": build, "c1_recorded": c1, args.label: c2}, indent=1), encoding="utf-8")
        results.append({"task": tid, "codebase": t["codebase"], "c1": c1, args.label: c2})
        print(tid, "c1", (c1 or {}).get("platform_correct"), (c1 or {}).get("scope_correct"), (c1 or {}).get("mode_correct"), (c1 or {}).get("concept_recall"), (c1 or {}).get("critical_recall"),
              "|", args.label, c2.get("platform_correct"), c2.get("scope_correct"), c2.get("mode_correct"), c2.get("concept_recall"), c2.get("critical_recall"), c2.get("forbidden_delivered"))

    def agg(key):
        rows = [r[key] for r in results if r.get(key) and "error" not in r[key]]
        def tally(f):
            o = {}
            for r in rows: o[str(r.get(f))] = o.get(str(r.get(f)), 0) + 1
            return o
        rec = [r["concept_recall"] for r in rows if r["concept_recall"] is not None]; cr = [r["critical_recall"] for r in rows if r["critical_recall"] is not None]
        return {"tasks": len(rows), "platform_correct": tally("platform_correct"), "artifact_state_correct": tally("artifact_state_correct"), "mode_correct": tally("mode_correct"),
                "scope_correct": tally("scope_correct"), "mean_concept_recall": round(sum(rec) / len(rec), 3) if rec else None, "mean_critical_recall": round(sum(cr) / len(cr), 3) if cr else None,
                "tasks_critical_recall_1": sum(1 for c in cr if c >= 0.999), "tasks_with_forbidden": sum(1 for r in rows if r["forbidden_delivered"]),
                "empty_bundles": sum(1 for r in rows if not r["bundle_ids"]), "mean_bundle_tokens": round(sum(r["bundle_tokens"] or 0 for r in rows) / len(rows), 1) if rows else None}
    report = {"build": build, "label": args.label, "method": "same scorer applied to the recorded c1 outputs and to a fresh run of inspect/requirements/guidance/direction on the current build; projects are inspected in their post-round state (the round's implementations are in place)",
              "aggregate": {"c1_recorded": agg("c1"), args.label: agg(args.label)}, "per_task": results}
    out = Path(args.out) if args.out else ROOT / "research" / "runs" / f"phase{args.phase}-{args.label}-projects-rescore.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report["aggregate"], indent=1))


if __name__ == "__main__":
    main()
