#!/usr/bin/env python3
"""Release check: one command that runs everything a release must pass.

  python evals/release_check.py [--heldout-v1] [--heldout-v2] [--projects] [--real-activation] [--json]

--heldout-v1  historical, non-blind held-out set (report only)     --heldout   alias for --heldout-v1
--heldout-v2  blind held-out set with pre-registered thresholds (evals/heldout-v2/THRESHOLDS.md); reported,
              and the threshold verdict is printed, but it is not a release gate
--projects    aggregates research/phase3-projects/*/artifacts.json (torture tests)

Runs: validate_skill.py · development evals · regression evals · tool contracts (part of development)
· activation proxy metrics · benchmark JSON/Markdown consistency (via the validator) · optional
held-out run (--heldout; reported, not tuned against) · optional real-model activation probe
(--real-activation; reports REAL_ACTIVATION: SKIPPED when the CLI is not authenticated).
Exit 0 when every mandatory gate passes; 1 otherwise. Performance sanity thresholds are loose
(load < 2 s, search < 0.5 s, direction < 1.5 s) and only catch accidental regressions.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, *cmd], capture_output=True, text=True, encoding="utf-8", cwd=str(SKILL))
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--heldout", "--heldout-v1", dest="heldout", action="store_true")
    ap.add_argument("--heldout-v2", action="store_true")
    ap.add_argument("--heldout-v3", action="store_true")
    ap.add_argument("--heldout-v4", action="store_true")
    ap.add_argument("--heldout-v5", action="store_true")
    ap.add_argument("--human-review", help="JSON file with bundle-quality verdicts for held-out v3 ({id: GOOD|PARTIAL|BAD|ABSTAIN-CORRECT})")
    ap.add_argument("--projects", action="store_true")
    ap.add_argument("--real-activation", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    report: dict = {"gates": {}}
    ok_all = True

    code, out = run(["scripts/validate_skill.py"])
    report["gates"]["validator"] = {"ok": code == 0, "summary": out.strip().splitlines()[0] if out.strip() else ""}
    ok_all &= code == 0

    code, out = run(["evals/run_evals.py", "--group", "development", "--group", "regression", "--json"])
    try:
        ev = json.loads(out[out.index("{"):])
        report["gates"]["development+regression"] = {"ok": code == 0, "passed": ev["passed"], "total": ev["total"],
                                                     "failing": [r["id"] for s in ev["suites"].values() for r in s if not r["ok"]]}
    except (ValueError, KeyError):
        report["gates"]["development+regression"] = {"ok": False, "error": out[-500:]}
    ok_all &= code == 0

    code, out = run(["evals/activation_metrics.py", "--json"])
    try:
        am = json.loads(out[out.index("{"):])["proxy"]
        report["gates"]["activation_proxy"] = {"ok": code == 0 and am["precision"] >= 0.9, "precision": am["precision"], "recall": am["recall"],
                                               "fpr": am["false_positive_rate"], "fnr": am["false_negative_rate"]}
    except (ValueError, KeyError):
        report["gates"]["activation_proxy"] = {"ok": False, "error": out[-300:]}
    ok_all &= report["gates"]["activation_proxy"]["ok"]

    import de_core as core
    t = time.perf_counter(); recs = core.load_records(); t_load = time.perf_counter() - t
    t = time.perf_counter(); core.search("WinUI desktop ERP data grid with keyboard shortcuts", recs); t_search = time.perf_counter() - t
    t = time.perf_counter(); core.direction("IPTV home screen for Android TV", records=recs); t_dir = time.perf_counter() - t
    perf_ok = t_load < 2 and t_search < 0.5 and t_dir < 1.5
    report["gates"]["performance_sanity"] = {"ok": perf_ok, "load_ms": round(t_load * 1000), "search_ms": round(t_search * 1000), "direction_ms": round(t_dir * 1000)}
    ok_all &= perf_ok

    if args.heldout:
        code, out = run(["evals/run_evals.py", "--group", "heldout", "--json"])
        try:
            ev = json.loads(out[out.index("{"):])
            report["heldout"] = {"passed": ev["passed"], "total": ev["total"], "summary": ev.get("heldout_summary", {})}
        except (ValueError, KeyError):
            report["heldout"] = {"error": out[-500:]}
    if args.heldout_v2:
        code, out = run(["evals/run_evals.py", "--group", "heldout-v2", "--json"])
        try:
            ev = json.loads(out[out.index("{"):])
            summ = next(iter(ev.get("heldout_summary", {}).values()))
            n = max(1, summ.get("cases", 0))
            verdict = {
                "acceptable_ge_40pct": summ.get("acceptable", 0) / n >= 0.40,
                "mean_concept_recall_ge_0.40": (summ.get("mean_concept_recall") or 0) >= 0.40,
                "required_concern_coverage_ge_0.85": summ.get("mean_concern_coverage", 0) >= 0.85,
                "mean_offtarget_le_0.20": summ.get("mean_offtarget_rate", 1) <= 0.20,
                "abstain_correct_ge_80pct": (summ.get("abstain_correct", 0) / max(1, summ.get("abstain_cases", 0))) >= 0.80 if summ.get("abstain_cases") else None,
                "platform_correct_ge_85pct": summ.get("platform_correct", 0) / n >= 0.85,
                "mode_correct_ge_75pct": summ.get("mode_correct", 0) / n >= 0.75,
                "empty_le_2pct": summ.get("empty_results", 0) / n <= 0.02,
            }
            report["heldout_v2"] = {"passed": ev["passed"], "total": ev["total"], "summary": summ, "thresholds": verdict,
                                    "thresholds_met": all(v for v in verdict.values() if v is not None)}
        except (ValueError, KeyError, StopIteration):
            report["heldout_v2"] = {"error": out[-500:]}
    if args.heldout_v3:
        code, out = run(["evals/run_evals.py", "--group", "heldout-v3", "--json"])
        try:
            ev = json.loads(out[out.index("{"):])
            summ = next(iter(ev.get("heldout_summary", {}).values()))
            non = max(1, summ["cases"] - summ["abstain_cases"])
            human = None
            if args.human_review and Path(args.human_review).exists():
                hv = json.loads(Path(args.human_review).read_text(encoding="utf-8"))
                verdicts = [v.upper() for v in (hv.get("verdicts", hv)).values()] if isinstance(hv, dict) else []
                hn = len([v for v in verdicts if v in ("GOOD", "PARTIAL", "BAD")]) or 1
                human = {"n": len(verdicts), "good": verdicts.count("GOOD"), "partial": verdicts.count("PARTIAL"), "bad": verdicts.count("BAD"), "abstain_correct": verdicts.count("ABSTAIN-CORRECT"),
                         "good_plus_partial_rate": round((verdicts.count("GOOD") + verdicts.count("PARTIAL")) / hn, 3), "bad_rate": round(verdicts.count("BAD") / hn, 3)}
            verdict = {
                "platform_ge_0.92": summ["platform_correct"] / non >= 0.92, "mode_ge_0.80": summ["mode_correct"] / non >= 0.80,
                "scope_ge_0.90": summ["scope_correct"] / max(1, summ["cases"]) >= 0.90,
                "concern_coverage_ge_0.90": (summ["mean_required_concern_coverage"] or 0) >= 0.90,
                "concept_recall_ge_0.60": (summ["mean_concept_recall"] or 0) >= 0.60,
                "forbidden_rate_le_0.08": summ["forbidden_violation_cases"] / non <= 0.08,
                "empty_le_0.02": summ["empty_results"] / non <= 0.02,
                "human_good_plus_partial_ge_0.80": (human["good_plus_partial_rate"] >= 0.80) if human else None,
                "human_bad_le_0.20": (human["bad_rate"] <= 0.20) if human else None,
                "acceptable_ge_0.50 (secondary)": summ["acceptable"] / max(1, summ["cases"]) >= 0.50,
            }
            primary = [k for k in verdict if "secondary" not in k]
            met = sum(1 for k in primary if verdict[k])
            report["heldout_v3"] = {"passed": ev["passed"], "total": ev["total"], "summary": summ, "human_review": human, "thresholds": verdict,
                                    "primary_met": met, "primary_total": len(primary), "thresholds_met": all(verdict[k] for k in primary if verdict[k] is not None)}
        except (ValueError, KeyError, StopIteration) as e:
            report["heldout_v3"] = {"error": out[-500:] + f" ({e})"}
    if args.heldout_v4:
        code, out = run(["evals/run_evals.py", "--group", "heldout-v4", "--json"])
        try:
            ev = json.loads(out[out.index("{"):])
            summ = next(iter(ev.get("heldout_summary", {}).values()))
            non = max(1, summ["cases"] - summ["abstain_cases"]); claims = max(1, summ["platform_claims"])
            human = None
            if args.human_review and Path(args.human_review).exists():
                hv = json.loads(Path(args.human_review).read_text(encoding="utf-8"))
                verdicts = [v.upper() for v in (hv.get("verdicts", hv)).values()] if isinstance(hv, dict) else []
                hn = len([v for v in verdicts if v in ("GOOD", "PARTIAL", "BAD")]) or 1
                human = {"n": len(verdicts), "good": verdicts.count("GOOD"), "partial": verdicts.count("PARTIAL"), "bad": verdicts.count("BAD"),
                         "correct_abstain": verdicts.count("CORRECT_ABSTAIN") + verdicts.count("ABSTAIN-CORRECT"), "wrong_abstain": verdicts.count("WRONG_ABSTAIN") + verdicts.count("ABSTAIN-WRONG"),
                         "good_plus_partial_rate": round((verdicts.count("GOOD") + verdicts.count("PARTIAL")) / hn, 3), "bad_rate": round(verdicts.count("BAD") / hn, 3)}
            verdict = {
                "1_platform_ge_0.88": summ["platform_correct"] / claims >= 0.88,
                "2_false_platform_le_0.05": summ["platform_false_assignment"] / claims <= 0.05,
                "3_mode_ge_0.75": summ["mode_correct"] / non >= 0.75,
                "4_scope_ge_0.92": summ["scope_correct"] / max(1, summ["cases"]) >= 0.92,
                "5_concern_coverage_ge_0.90": (summ["mean_required_concern_coverage"] or 0) >= 0.90,
                "6_concept_recall_ge_0.58": (summ["mean_concept_recall"] or 0) >= 0.58,
                "7_critical_recall_ge_0.80": (summ["mean_critical_recall"] or 0) >= 0.80,
                "8_forbidden_le_0.05": summ["forbidden_violation_cases"] / non <= 0.05,
                "9_human_good_plus_partial_ge_0.82": (human["good_plus_partial_rate"] >= 0.82) if human else None,
                "10_human_bad_le_0.18": (human["bad_rate"] <= 0.18) if human else None,
            }
            secondary = {"empty_le_0.01": summ["empty_results"] / non <= 0.01, "acceptable_ge_0.50": summ["acceptable"] / max(1, summ["cases"]) >= 0.50,
                         "fundamental_mode_miss_le_0.10": summ["mode_fundamental_miss"] / non <= 0.10, "mean_tokens_le_1200": (summ["mean_bundle_tokens"] or 0) <= 1200}
            mandatory = ["4_scope_ge_0.92", "8_forbidden_le_0.05", "9_human_good_plus_partial_ge_0.82", "10_human_bad_le_0.18", "2_false_platform_le_0.05"]
            met = sum(1 for k, v in verdict.items() if v)
            policy_ok = met >= 8 and all(verdict[k] for k in mandatory)
            report["heldout_v4"] = {"passed": ev["passed"], "total": ev["total"], "summary": summ, "human_review": human, "thresholds": verdict, "secondary": secondary,
                                    "primary_met": met, "primary_total": len(verdict), "mandatory_met": all(bool(verdict[k]) for k in mandatory), "stable_candidate_blind_policy": policy_ok}
        except (ValueError, KeyError, StopIteration) as e:
            report["heldout_v4"] = {"error": out[-500:] + f" ({e})"}
    if args.heldout_v5:
        code, out = run(["evals/run_evals.py", "--group", "heldout-v5", "--json"])
        try:
            ev = json.loads(out[out.index("{"):])
            summ = next(iter(ev.get("heldout_summary", {}).values()))
            non = max(1, summ["cases"] - summ["abstain_cases"]); claims = max(1, summ["platform_claims"])
            human = None
            if args.human_review and Path(args.human_review).exists():
                hv = json.loads(Path(args.human_review).read_text(encoding="utf-8"))
                vd = hv.get("verdicts", hv) if isinstance(hv, dict) else {}
                verdicts = [(v["verdict"] if isinstance(v, dict) else v).upper() for v in vd.values()]
                defects = [(v.get("defect") or "").lower() for v in vd.values() if isinstance(v, dict)]
                hn = len([v for v in verdicts if v in ("GOOD", "PARTIAL", "BAD")]) or 1
                human = {"n": len(verdicts), "good": verdicts.count("GOOD"), "partial": verdicts.count("PARTIAL"), "bad": verdicts.count("BAD"),
                         "correct_abstain": verdicts.count("CORRECT_ABSTAIN"), "wrong_abstain": verdicts.count("WRONG_ABSTAIN"),
                         "good_plus_partial_rate": round((verdicts.count("GOOD") + verdicts.count("PARTIAL")) / hn, 3), "bad_rate": round(verdicts.count("BAD") / hn, 3),
                         "defects": {d: defects.count(d) for d in sorted(set(defects)) if d},
                         "generic_rate": round(defects.count("generic") / hn, 3), "wrong_screen_rate": round(defects.count("wrong-screen") / hn, 3),
                         "wrong_product_rate": round(defects.count("wrong-product") / hn, 3), "missing_critical_rate": round(defects.count("missing-critical") / hn, 3)}
            verdict = {
                "1_scope_ge_0.93": summ["scope_correct"] / max(1, summ["cases"]) >= 0.93,
                "2_false_platform_le_0.05": summ["platform_resolved_wrong"] / claims <= 0.05,
                "3_platform_correct_ge_0.75": summ["platform_resolved_correct"] / claims >= 0.75,
                "4_mode_ge_0.85": summ["mode_correct"] / non >= 0.85,
                "5_critical_recall_ge_0.80": (summ["mean_critical_recall"] or 0) >= 0.80,
                "6_concept_recall_ge_0.62": (summ["mean_concept_recall"] or 0) >= 0.62,
                "7_forbidden_le_0.05": summ["forbidden_violation_cases"] / non <= 0.05,
                "8_human_good_plus_partial_ge_0.85": (human["good_plus_partial_rate"] >= 0.85) if human else None,
                "9_human_bad_le_0.15": (human["bad_rate"] <= 0.15) if human else None,
                "10_generic_defect_le_0.12": (human["generic_rate"] <= 0.12) if human else None,
                "11_wrong_screen_defect_le_0.08": (human["wrong_screen_rate"] <= 0.08) if human else None,
            }
            secondary = {"resolution_rate": summ["platform_resolution_rate"], "unresolved_rate": round(summ["platform_unresolved"] / claims, 3),
                         "fundamental_mode_miss_le_0.10": summ["mode_fundamental_miss"] / non <= 0.10, "empty_rate": round(summ["empty_results"] / non, 3),
                         "mean_bundle_size": summ["mean_bundle_size"], "mean_bundle_tokens": summ["mean_bundle_tokens"], "quality_totals": summ.get("quality_totals"), "by_stress": summ.get("by_stress")}
            mandatory = ["1_scope_ge_0.93", "2_false_platform_le_0.05", "5_critical_recall_ge_0.80", "7_forbidden_le_0.05", "8_human_good_plus_partial_ge_0.85", "9_human_bad_le_0.15"]
            met = sum(1 for k, v in verdict.items() if v)
            policy_ok = met >= 9 and all(verdict[k] for k in mandatory)
            report["heldout_v5"] = {"passed": ev["passed"], "total": ev["total"], "summary": summ, "human_review": human, "thresholds": verdict, "secondary": secondary,
                                    "primary_met": met, "primary_total": len(verdict), "mandatory_met": all(bool(verdict[k]) for k in mandatory), "stable_candidate_blind_policy": policy_ok}
        except (ValueError, KeyError, StopIteration) as e:
            report["heldout_v5"] = {"error": out[-500:] + f" ({e})"}
    if args.projects:
        root4 = SKILL.parent / "research" / "phase4-projects"
        arts4 = []
        for p in sorted(root4.glob("*/artifacts.json")):
            try:
                arts4.append(json.loads(p.read_text(encoding="utf-8")))
            except json.JSONDecodeError as e:
                arts4.append({"task": p.parent.name, "error": str(e)})
        good4 = [a for a in arts4 if "error" not in a]
        def dsum(key):
            tot = {}
            for a in good4:
                for k, v in (a.get(key) or {}).items():
                    tot[k] = tot.get(k, 0) + (v if isinstance(v, (int, float)) else 0)
            return tot
        def frac(field, key):
            vals = [a.get(field, {}).get(key) for a in good4 if isinstance(a.get(field), dict) and key in a.get(field, {})]
            yes = sum(1 for v in vals if v in (True, "yes"))
            return {"yes": yes, "partial": sum(1 for v in vals if v == "partial"), "no": sum(1 for v in vals if v in (False, "no")), "n": len(vals)}
        report["projects_phase4"] = {
            "tasks": len(arts4), "applications": len({a.get("project") for a in good4}), "existing_ui_tasks": sum(1 for a in good4 if a.get("existing_ui")),
            "first_render_defects": dsum("first_render_defects"), "final_defects": dsum("final_defects"),
            "iterations": sum(a.get("iterations", 0) for a in good4),
            "guidance": {"relevant": sum(a.get("guidance_relevant", 0) for a in good4), "partial": sum(a.get("guidance_partial", 0) for a in good4), "offtarget": sum(a.get("guidance_offtarget", 0) for a in good4)},
            "context_detection": {k: frac("context_detection", k) for k in ("navigation", "theme", "typography", "surfaces", "spacing")},
            "preservation": {k: frac("preservation", k) for k in ("navigation", "theme", "typography", "component_reuse")},
            "unjustified_structural_change": sum((a.get("preservation") or {}).get("unjustified_structural_change", 0) for a in good4),
            "misses_by_layer": {l: sum(1 for a in good4 for m in a.get("misses", []) if m.get("layer") == l) for l in ("scope", "mode", "requirements", "concerns", "expected-concepts", "candidate-retrieval", "bundle-selection", "direction", "project-adaptation")},
            "tags": {t: sum(1 for a in good4 if t in a.get("tags", [])) for t in sorted({t for a in good4 for t in a.get("tags", [])})},
            "per_task": [{k: a.get(k) for k in ("task", "project", "mode", "change_budget", "render_mode", "iterations")} for a in good4],
        }
        root5 = SKILL.parent / "research" / "phase5-projects"
        arts5 = []
        for p in sorted(root5.glob("p5-[0-9][0-9]/artifacts.json")):
            try:
                arts5.append(json.loads(p.read_text(encoding="utf-8")))
            except json.JSONDecodeError as e:
                arts5.append({"task": p.parent.name, "error": str(e)})
        good5 = [a for a in arts5 if "error" not in a]
        if arts5:
            def dsum5(key):
                tot = {}
                for a in good5:
                    for k, v in (a.get(key) or {}).items():
                        tot[k] = tot.get(k, 0) + (v if isinstance(v, (int, float)) else 0)
                return tot
            def frac5(field, key):
                vals = [a.get(field, {}).get(key) for a in good5 if isinstance(a.get(field), dict) and key in a.get(field, {})]
                return {"yes": sum(1 for v in vals if v in (True, "yes")), "partial": sum(1 for v in vals if v == "partial"), "no": sum(1 for v in vals if v in (False, "no")), "n": len(vals)}
            def tally(key):
                out = {}
                for a in good5:
                    out[str(a.get(key))] = out.get(str(a.get(key)), 0) + 1
                return out
            recalls = [a.get("concept_recall") for a in good5 if isinstance(a.get("concept_recall"), (int, float))]
            crit = [a.get("critical_recall") for a in good5 if isinstance(a.get("critical_recall"), (int, float))]
            hashes = {a.get("build_hash_start") for a in good5} | {a.get("build_hash_end") for a in good5}
            report["projects_phase5"] = {
                "tasks": len(arts5), "codebases": len({a.get("project") for a in good5}), "existing_ui_tasks": sum(1 for a in good5 if a.get("existing_ui")),
                "new_screen_tasks": sum(1 for a in good5 if a.get("new_screen")),
                "platform_correct": tally("platform_correct"), "artifact_state_correct": tally("artifact_state_correct"),
                "mode_correct": tally("mode_correct"), "scope_correct": tally("scope_correct"),
                "platforms": tally("platform_expected"),
                "mean_concept_recall": round(sum(recalls) / len(recalls), 3) if recalls else None,
                "mean_critical_recall": round(sum(crit) / len(crit), 3) if crit else None,
                "tasks_critical_recall_1": sum(1 for c in crit if c >= 0.999),
                "concept_misses_by_layer": {l: sum(1 for a in good5 for m in a.get("concept_misses", []) if m.get("layer") == l) for l in ("expected-concepts", "candidate-retrieval", "bundle-selection", "knowledge-gap")},
                "first_render_defects": dsum5("first_render_defects"), "final_defects": dsum5("final_defects"),
                "iterations": sum(a.get("iterations", 0) for a in good5),
                "guidance": {"relevant": sum(a.get("guidance_relevant", 0) for a in good5), "partial": sum(a.get("guidance_partial", 0) for a in good5), "offtarget": sum(a.get("guidance_offtarget", 0) for a in good5)},
                "bad_guidance_by_category": {c: sum(1 for a in good5 for b in a.get("bad_guidance", []) if b.get("category") == c) for c in ("off-platform", "wrong-mode", "generic", "contradicts-codebase", "missing-critical", "harmful")},
                "skill_effect": tally("skill_effect"),
                "context_detection": {k: frac5("context_detection", k) for k in ("navigation", "theme", "typography", "surfaces", "spacing")},
                "preservation": {k: frac5("preservation", k) for k in ("navigation", "theme", "typography", "component_reuse")},
                "unjustified_structural_change": sum((a.get("preservation") or {}).get("unjustified_structural_change", 0) for a in good5),
                "misses_by_layer": {l: sum(1 for a in good5 for m in a.get("misses", []) if m.get("layer") == l) for l in ("scope", "platform", "mode", "requirements", "concerns", "expected-concepts", "candidate-retrieval", "bundle-selection", "direction", "project-adaptation")},
                "tags": {t: sum(1 for a in good5 if t in a.get("tags", [])) for t in sorted({t for a in good5 for t in a.get("tags", [])})},
                "build_hashes": sorted(h for h in hashes if h), "single_build": len({h for h in hashes if h}) == 1,
                "per_task": [{k: a.get(k) for k in ("task", "project", "platform_expected", "platform_correct", "mode_correct", "scope_correct", "concept_recall", "critical_recall", "skill_effect", "iterations")} for a in good5],
            }
        root = SKILL.parent / "research" / "phase3-projects"
        arts = []
        for p in sorted(root.glob("*/artifacts.json")):
            try:
                arts.append(json.loads(p.read_text(encoding="utf-8")))
            except json.JSONDecodeError as e:
                arts.append({"case": p.parent.name, "error": str(e)})
        good = [a for a in arts if "error" not in a]
        report["projects"] = {
            "cases": len(arts), "rendered": sum(1 for a in good if a.get("rendered")),
            "first_render_defects": sum(a.get("first_render_defects", 0) for a in good),
            "final_defects": sum(a.get("final_defects", 0) for a in good),
            "iterations": sum(a.get("iterations", 0) for a in good),
            "guidance_relevant": sum(a.get("guidance_relevant", 0) for a in good),
            "guidance_partial": sum(a.get("guidance_partial", 0) for a in good),
            "guidance_offtarget": sum(a.get("guidance_offtarget", 0) for a in good),
            "knowledge_gaps": sorted({g for a in good for g in a.get("knowledge_gaps", [])})[:40],
            "ranking_misses": sorted({g for a in good for g in a.get("ranking_misses", [])})[:40],
            "tags": {t: sum(1 for a in good if t in a.get("tags", [])) for t in sorted({t for a in good for t in a.get("tags", [])})},
            "per_case": [{k: a.get(k) for k in ("case", "platform", "render_mode", "first_render_defects", "final_defects", "iterations")} for a in good],
        }
    if args.real_activation:
        code, out = run(["evals/activation_metrics.py", "--real", "--json"])
        if code == 6:
            report["real_activation"] = "SKIPPED — claude CLI not authenticated for non-interactive use"
        else:
            try:
                report["real_activation"] = json.loads(out[out.index("{"):]).get("real")
            except ValueError:
                report["real_activation"] = {"error": out[-300:]}
    else:
        report["real_activation"] = "NOT RUN (pass --real-activation)"
    report["ok"] = ok_all
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for g, v in report["gates"].items():
            print(f"{'PASS' if v.get('ok') else 'FAIL'}  {g}: " + json.dumps({k: x for k, x in v.items() if k != 'ok'}, ensure_ascii=False)[:400])
        if "heldout" in report:
            print("HELD-OUT v1 (historical, report only): " + json.dumps({k: v for k, v in report['heldout'].items() if k != 'summary'}))
        if "heldout_v2" in report:
            hv = report["heldout_v2"]
            print("HELD-OUT v2 (blind, report only): " + json.dumps({k: v for k, v in hv.items() if k not in ('summary',)}, ensure_ascii=False)[:900])
        if "heldout_v4" in report:
            hv = report["heldout_v4"]
            print("HELD-OUT v4 (blind, pre-registered thresholds): " + json.dumps({k: v for k, v in hv.items() if k not in ('summary',)}, ensure_ascii=False)[:1400])
        if "heldout_v3" in report:
            hv = report["heldout_v3"]
            print("HELD-OUT v3 (blind, pre-registered thresholds): " + json.dumps({k: v for k, v in hv.items() if k not in ('summary',)}, ensure_ascii=False)[:1200])
        if "projects_phase5" in report:
            print("PROJECTS phase 5: " + json.dumps({k: v for k, v in report['projects_phase5'].items() if k not in ('per_task',)}, ensure_ascii=False)[:1200])
        if "projects_phase4" in report:
            print("PROJECTS phase 4: " + json.dumps({k: v for k, v in report['projects_phase4'].items() if k not in ('per_task',)}, ensure_ascii=False)[:900])
        if "projects" in report:
            print("PROJECTS (phase 3 torture tests): " + json.dumps({k: v for k, v in report['projects'].items() if k not in ('per_case', 'knowledge_gaps', 'ranking_misses')}, ensure_ascii=False)[:600])
        print(f"REAL_ACTIVATION: {report['real_activation'] if isinstance(report['real_activation'], str) else json.dumps(report['real_activation'])[:300]}")
        print("RELEASE CHECK:", "PASS" if ok_all else "FAIL")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
