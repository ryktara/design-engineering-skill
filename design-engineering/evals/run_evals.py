#!/usr/bin/env python3
"""Evaluation runner for the design-engineering skill.

  python evals/run_evals.py [--group development|regression|heldout|all] [--suite NAME ...] [--verbose] [--json] [--out report.json]

Groups (directories under evals/):
  development/  cases written alongside the implementation; allowed for tuning
  regression/   real defects found in use; never removed while valid
  heldout/      frozen, independently generated; NOT for tuning (see heldout/MANIFEST.json)

Suite type is the file's `suite` field (defaults to the file name). Types: activation, retrieval,
platform, brand, project, greenfield, tools, requirements, conflicts, heldout. Cases are never
edited to make the implementation pass; a wrong case is fixed with a dated `note`.
Exit 1 if any case in the selected groups fails (held-out failures are reported, and also fail).
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import de_core as core  # noqa: E402
import fingerprint as fpmod  # noqa: E402
import inspect_project  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

EVALS = SKILL / "evals"


def _fixture_project(rel: str | None) -> dict | None:
    if not rel:
        return None
    root = (SKILL.parent / rel).resolve() if rel.startswith("research/") else (EVALS / rel).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    return inspect_project.inspect(root, 2000)


def _ledger_strings(req: dict, status: str) -> set[str]:
    return {f"{e['field']}={e['value']}" for e in (req["known"] if status == "KNOWN" else req["inferred"])}


# ---------------------------------------------------------------- suites
def run_activation(records, cases):
    out = []
    for c in cases:
        got = core.build_requirements(c["prompt"])["activation"]["decision"]
        # 'skip' means "must not activate": a deferral (ambiguous) satisfies it, matching the metric definition
        # in activation_metrics.py where only 'activate' counts as a false positive.
        ok = (got != "activate") if c["expect"] == "skip" else (got == "activate" if c["expect"] == "activate" else True)
        out.append({"id": c["id"], "ok": ok, "detail": f"expected {c['expect']} got {got}"})
    return out


def _retrieval_case(records, c):
    proj = _fixture_project(c.get("fixture"))
    req = core.build_requirements(c["query"], project=proj, hints=c.get("hints"))
    res = core.search(c["query"], records, k=c.get("k", 5), requirements=req,
                      kinds=set(c["kinds"]) if c.get("kinds") else None, explain=True)
    got = [r["id"] for r in res["results"]]
    problems = []
    for i in c.get("expect_ids", []):
        if i not in got:
            problems.append(f"missing {i}")
    if c.get("expect_any_ids") and not any(i in got for i in c["expect_any_ids"]):
        problems.append(f"none of {c['expect_any_ids']}")
    for i in c.get("forbid_ids", []):
        if i in got:
            problems.append(f"forbidden {i} present")
    cats = [r["category"] for r in res["results"]]
    for cat in c.get("expect_categories", []):
        if cat not in cats:
            problems.append(f"category {cat} absent")
    for p in c.get("expect_platforms", []):
        if p not in req["platform"]:
            problems.append(f"platform {p} not detected")
    for m in c.get("expect_modes", []):
        if m not in req["mode"][:2]:
            problems.append(f"mode {m} not in top-2 modes {req['mode']}")
    if c.get("expect_confidence") and res["confidence"] != c["expect_confidence"]:
        problems.append(f"confidence {res['confidence']} != {c['expect_confidence']}")
    if c.get("expect_status") and res["status"] != c["expect_status"]:
        problems.append(f"status {res['status']} != {c['expect_status']}")
    if c.get("expect_missing") and not req["missing"]:
        problems.append("expected a MISSING ledger entry")
    if c.get("min_facet_coverage") is not None and res["coverage"]["facet_coverage"] < c["min_facet_coverage"]:
        problems.append(f"facet coverage {res['coverage']['facet_coverage']} < {c['min_facet_coverage']}")
    if c.get("max_duplicate_pressure") is not None and res["coverage"]["duplicate_pressure"] > c["max_duplicate_pressure"]:
        problems.append(f"duplicate pressure {res['coverage']['duplicate_pressure']} > {c['max_duplicate_pressure']}")
    for f in c.get("expect_facets", []):
        if f not in res["coverage"]["required_facets_satisfied"]:
            problems.append(f"facet {f} not covered")
    return {"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or "top=" + ",".join(got[:4])}


def run_retrieval(records, cases):
    return [_retrieval_case(records, c) for c in cases]


def run_platform(records, cases):
    out = []
    for c in cases:
        tops, problems = {}, []
        for plat in c["platforms"]:
            q = c["query_template"].replace("{platform}", plat)
            tops[plat] = [r["id"] for r in core.search(q, records, k=c.get("k", 5))["results"]]
            for must in c.get("must_include", {}).get(plat, []):
                if must not in tops[plat]:
                    problems.append(f"{plat}: missing {must}")
            for must_not in c.get("must_exclude", {}).get(plat, []):
                if must_not in tops[plat]:
                    problems.append(f"{plat}: forbidden {must_not}")
        top1 = {p: (t[0] if t else None) for p, t in tops.items()}
        if len(set(top1.values())) < c.get("min_distinct_top", len(c["platforms"])):
            problems.append(f"only {len(set(top1.values()))} distinct top results: {top1}")
        plats = c["platforms"]
        allowed = {tuple(sorted(p)) for p in c.get("allow_overlap_pairs", [])}
        for i in range(len(plats)):
            for j in range(i + 1, len(plats)):
                if tuple(sorted((plats[i], plats[j]))) in allowed:
                    continue
                a, b = set(tops[plats[i]]), set(tops[plats[j]])
                overlap = len(a & b) / max(1, min(len(a), len(b)))
                if overlap > c.get("max_overlap", 0.6):
                    problems.append(f"{plats[i]}/{plats[j]} overlap {overlap:.2f}")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or json.dumps(top1)})
    return out


def run_brand(records, cases):
    out = []
    for c in cases:
        docs, bad = [], []
        for i, fp in enumerate(c["fingerprints"]):
            bad += fpmod.validate(fp)
            docs.append({"name": f"brand{i+1}", "fingerprint": fp})
        if bad:
            out.append({"id": c["id"], "ok": False, "detail": "; ".join(bad)})
            continue
        rep = fpmod.compare(docs, c.get("threshold", 0.7))
        got = "PASS" if rep["pass"] else "FAIL"
        verdicts = [p["verdict"] for p in rep["pairs"]]
        ok = got == c["expect"] and (not c.get("expect_verdicts") or verdicts == c["expect_verdicts"])
        out.append({"id": c["id"], "ok": ok, "detail": f"{got} {verdicts}"})
    return out


def run_project(records, cases):
    out = []
    for c in cases:
        try:
            res = _fixture_project(c["fixture"])
        except FileNotFoundError as e:
            out.append({"id": c["id"], "ok": False, "detail": f"fixture missing: {e}"})
            continue
        problems = []
        for key, vals in c.get("expect", {}).items():
            got = res.get(key, [])
            for v in vals:
                if not any(v in str(g) for g in got):
                    problems.append(f"{key} lacks '{v}' (got {got})")
        for key, vals in c.get("expect_absent", {}).items():
            for v in vals:
                if any(v in str(g) for g in res.get(key, [])):
                    problems.append(f"{key} unexpectedly has '{v}'")
        if c.get("then_query"):
            req = core.build_requirements(c["then_query"], project=res)
            sres = core.search(c["then_query"], records, k=5, requirements=req)
            got_ids = [r["id"] for r in sres["results"]]
            for i in c.get("then_expect_ids", []):
                if i not in got_ids:
                    problems.append(f"after inspection, query lacks {i} (got {got_ids})")
            for p in c.get("then_expect_platforms", []):
                if p not in req["platform"]:
                    problems.append(f"after inspection, platform {p} not present")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"stacks={res['stack_groups']} platforms={res['platforms']}"})
    return out


def run_greenfield(records, cases):
    out = []
    by_id = {r["id"]: r for r in records}
    for c in cases:
        d = core.direction(c["query"], hints=c.get("hints"), records=records, explain=True)
        problems = []
        missing = " ".join(d["ledger"]["MISSING"]).lower()
        for s in c.get("expect_missing_substrings", []):
            if s.lower() not in missing:
                problems.append(f"MISSING ledger lacks '{s}'")
        for s in c.get("forbid_missing_substrings", []):
            if s.lower() in missing:
                problems.append(f"MISSING ledger wrongly contains '{s}'")
        filled = sum(1 for v in d["direction"].values() if v)
        if filled < c.get("expect_slots_filled_min", 10):
            problems.append(f"only {filled} slots filled")
        chosen = {v["id"] for v in d["direction"].values() if v and v.get("id")}
        for i in c.get("expect_ids", []):
            if i not in chosen:
                problems.append(f"direction lacks {i}")
        for i in c.get("forbid_ids", []):
            if i in chosen:
                problems.append(f"direction contains forbidden {i}")
        for ax, val in c.get("expect_fingerprint", {}).items():
            if d["fingerprint"].get(ax) != val:
                problems.append(f"fingerprint {ax}={d['fingerprint'].get(ax)} != {val}")
        for a in chosen:
            for b in by_id[a].get("incompatible", []):
                if b in chosen:
                    problems.append(f"incompatible pair chosen: {a} / {b}")
        if not d["validation"]["ok"]:
            problems.append("validation: " + "; ".join(d["validation"]["violations"]))
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"{filled} slots; nav={d['fingerprint'].get('navigation_model')} layout={d['fingerprint'].get('layout_topology')}"})
    return out


def run_tools(records, cases):
    out = []
    for c in cases:
        script = SKILL / ("evals" if c["tool"] in ("run_evals", "activation_metrics", "release_check", "benchmark_upstream") else "scripts") / f"{c['tool']}.py"
        args = [a.replace("${EVALS}", str(EVALS)) for a in c["args"]]
        proc = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8")
        problems = []
        if proc.returncode != c.get("expect_exit", 0):
            problems.append(f"exit {proc.returncode} != {c.get('expect_exit', 0)}: {proc.stderr.strip()[:200]}")
        for s in c.get("expect_stdout_contains", []):
            if s not in proc.stdout:
                problems.append(f"stdout lacks '{s}'")
        first = proc.stdout.strip().splitlines()[0][:100] if proc.stdout.strip() else "no output"
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or first})
    return out


def run_requirements(records, cases):
    out = []
    for c in cases:
        proj = _fixture_project(c.get("fixture"))
        req = core.build_requirements(c["query"], project=proj)
        problems = list(core.validate_requirements(req))
        known, inferred = _ledger_strings(req, "KNOWN"), _ledger_strings(req, "INFERRED")
        missing = {m["field"] for m in req["missing"]}
        for s in c.get("expect_known", []):
            if s not in known:
                problems.append(f"not KNOWN: {s}")
        for s in c.get("expect_inferred", []):
            if s not in inferred:
                problems.append(f"not INFERRED: {s}")
        for s in c.get("forbid_known", []):
            if s in known:
                problems.append(f"wrongly KNOWN: {s}")
        for s in c.get("forbid_inferred", []):
            if s in inferred:
                problems.append(f"wrongly INFERRED: {s}")
        for f in c.get("expect_missing", []):
            if f not in missing:
                problems.append(f"not MISSING: {f}")
        for n in c.get("expect_negatives", []):
            if n not in req["negative_constraints"]:
                problems.append(f"negative {n} not detected")
        for n in c.get("forbid_negatives", []):
            if n in req["negative_constraints"]:
                problems.append(f"negative {n} wrongly detected")
        for k, v in c.get("expect_constraint", {}).items():
            if req["constraints"].get(k) != v:
                problems.append(f"constraint {k}={req['constraints'].get(k)} != {v}")
        for k in c.get("forbid_constraint", []):
            if req["constraints"].get(k):
                problems.append(f"constraint {k} wrongly set")
        for f in c.get("expect_conflict_fields", []):
            if f not in {x["field"] for x in req["conflicts"]}:
                problems.append(f"no conflict recorded for {f}")
        if c.get("expect_status") and core.requirements_status(req) != c["expect_status"]:
            problems.append(f"status {core.requirements_status(req)} != {c['expect_status']}")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"known={sorted(known)[:5]} missing={sorted(missing)}"})
    return out


def run_conflicts(records, cases):
    out = []
    for c in cases:
        proj = _fixture_project(c.get("fixture"))
        req = core.build_requirements(c["query"], project=proj)
        d = core.direction(c["query"], records=records, requirements=req)
        problems = []
        base = run_requirements(records, [dict(c, fixture=None)]) if not c.get("fixture") else None
        # reuse the requirements assertions
        known, inferred = _ledger_strings(req, "KNOWN"), _ledger_strings(req, "INFERRED")
        for s in c.get("expect_known", []):
            if s not in known:
                problems.append(f"not KNOWN: {s}")
        for s in c.get("forbid_known", []):
            if s in known:
                problems.append(f"wrongly KNOWN: {s}")
        for n in c.get("expect_negatives", []):
            if n not in req["negative_constraints"]:
                problems.append(f"negative {n} not detected")
        for k, v in c.get("expect_constraint", {}).items():
            if req["constraints"].get(k) != v:
                problems.append(f"constraint {k}={req['constraints'].get(k)} != {v}")
        for k in c.get("forbid_constraint", []):
            if req["constraints"].get(k):
                problems.append(f"constraint {k} wrongly set")
        for f in c.get("expect_conflict_fields", []):
            if f not in {x["field"] for x in req["conflicts"]}:
                problems.append(f"no conflict recorded for {f}")
        for f in c.get("expect_missing", []):
            if f not in {m["field"] for m in req["missing"]}:
                problems.append(f"not MISSING: {f}")
        chosen = {slot: (v or {}).get("id") for slot, v in d["direction"].items()}
        for slot in c.get("expect_direction_slot_preserved", []):
            if not d["direction"].get(slot) or not d["direction"][slot].get("preserved"):
                problems.append(f"slot {slot} not preserved (got {chosen.get(slot)})")
        for slot in c.get("expect_direction_slots", []):
            if not chosen.get(slot):
                problems.append(f"slot {slot} empty")
        for i in c.get("forbid_direction_ids", []):
            if i in chosen.values():
                problems.append(f"direction contains forbidden {i}")
        for ax, val in c.get("expect_fingerprint", {}).items():
            if d["fingerprint"].get(ax) != val:
                problems.append(f"fingerprint {ax}={d['fingerprint'].get(ax)} != {val}")
        for ax, vals in c.get("forbid_fingerprint", {}).items():
            if d["fingerprint"].get(ax) in vals:
                problems.append(f"fingerprint {ax}={d['fingerprint'].get(ax)} forbidden")
        if c.get("expect_fingerprint_complete") and len(d["fingerprint"]) < len(core.FINGERPRINT_AXES):
            problems.append(f"fingerprint incomplete {len(d['fingerprint'])}/{len(core.FINGERPRINT_AXES)}")
        if "expect_validation_ok" in c and d["validation"]["ok"] != c["expect_validation_ok"]:
            problems.append(f"validation ok={d['validation']['ok']}: {d['validation']['violations']}")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"conflicts={[x['field'] for x in req['conflicts']]} nav={chosen.get('navigation')}"})
    return out


def _text_of(results):
    """Text the model actually receives for a result: title, guidance, use/avoid, stack notes and the
    surfaced concept labels ('covers: ...')."""
    return " ".join(f"{r['title']} {r['guidance']} {r['use_when']} {r['avoid_when']} {' '.join(r.get('implementation', {}).values())} {' '.join(r.get('covers', []))}" for r in results).lower()


def _concept_hit(phrase: str, text: str, text_tokens: set[str]) -> bool:
    if phrase.lower() in text:
        return True
    toks = core._tokens(phrase)
    return bool(toks) and all(t in text_tokens for t in toks)


def run_heldout(records, cases):
    """Independent cases: expectations are platform/mode/input/screen/negative labels and concept
    phrases matched against returned text (never record ids). A case passes when every hard
    assertion holds; per-metric detail is aggregated by the caller."""
    out = []
    for c in cases:
        e = c["expect"]
        req = core.build_requirements(c["query"])
        res = core.search(c["query"], records, k=5, requirements=req)          # Phase 2 path (reference)
        g = core.guidance(c["query"], records, requirements=req)               # Phase 3 path (scored)
        bundle = g["core"] + g["guardrails"]
        text = _text_of(bundle)
        text_search = _text_of(res["results"])
        m = {}
        exp_p = set(e.get("platforms", []))
        got_p = set(req["platform"])
        m["platform_ok"] = (exp_p <= got_p) if exp_p else True
        m["platform_precision_ok"] = not (got_p - exp_p - {"tablet"}) if exp_p else True
        m["mode_ok"] = (set(e.get("modes", [])) & set(req["mode"][:2])) != set() if e.get("modes") else True
        m["input_ok"] = set(e.get("inputs", [])) <= set(req["input"])
        m["screen_ok"] = set(e.get("screens", [])) <= set(req["screen"]) if e.get("screens") else True
        m["negatives_ok"] = set(e.get("negatives", [])) <= set(req["negative_constraints"])
        concepts = e.get("concepts", [])
        text_tokens = set(core._tokens(text))
        # token-level match: a concept phrase counts when all of its content tokens appear in the
        # returned text (stemmed, stop words removed). Literal substring matching scored 0.066 mean
        # recall on run 1 because free-form phrases rarely appear verbatim; see research/PHASE2-RESULTS.md.
        hit = [k for k in concepts if _concept_hit(k, text, text_tokens)]
        m["concept_recall"] = round(len(hit) / len(concepts), 2) if concepts else None
        st_search = set(core._tokens(text_search))
        m["concept_recall_search_k5"] = round(len([k for k in concepts if _concept_hit(k, text_search, st_search)]) / len(concepts), 2) if concepts else None
        off = [k for k in e.get("offtarget", []) if _concept_hit(k, text, text_tokens)]
        m["offtarget_rate"] = round(len(off) / len(e["offtarget"]), 2) if e.get("offtarget") else 0.0
        m["facet_coverage"] = g["metrics"]["facet_coverage"]
        m["concern_coverage"] = g["metrics"]["coverage_ratio"]
        m["bundle_size"] = g["metrics"]["bundle_size"]
        m["bundle_bytes"] = len(json.dumps(bundle))
        m["empty"] = not bundle
        m["status"] = g["status"]
        m["missing_ok"] = set(e.get("missing", [])) <= {x["field"] for x in req["missing"]}
        if c.get("expect_abstain"):
            ok = g["status"] in ("ABSTAIN", "AMBIGUOUS") or req["activation"]["decision"] == "skip"
            m["abstain_ok"] = ok
        else:
            # acceptable = classification correct AND at least a third of the expected concepts present
            # AND at most a third of off-target concepts present AND a non-empty result
            ok = (m["platform_ok"] and m["mode_ok"] and m["input_ok"] and m["negatives_ok"]
                  and (m["concept_recall"] is None or m["concept_recall"] >= 0.34) and m["offtarget_rate"] <= 0.34 and not m["empty"])
            m["recall_at_least_half"] = bool(m["concept_recall"] is not None and m["concept_recall"] >= 0.5)
        out.append({"id": c["id"], "ok": ok, "category": c.get("category"), "metrics": m,
                    "detail": f"plat {sorted(got_p)} modes {req['mode'][:2]} recall {m['concept_recall']} (search {m['concept_recall_search_k5']}) off {m['offtarget_rate']} hit={hit} off={off} status={g['status']}"})
    return out


def run_heldout_v2(records, cases):
    """Blind held-out v2: structured expectations (see evals/heldout-v2/THRESHOLDS.md). Scores the guidance
    bundle. Acceptability rule and thresholds were fixed before the cases were generated."""
    out = []
    for c in cases:
        e = c["expect"]
        req = core.build_requirements(c["query"])
        g = core.guidance(c["query"], records, requirements=req)
        bundle = g["core"] + g["guardrails"]
        text = _text_of(bundle)
        text_tokens = set(core._tokens(text))
        covered = set().union(*(set(it["concerns"]) for it in bundle)) if bundle else set()
        m = {}
        exp_p = set(e.get("platforms", [])); got_p = set(req["platform"])
        m["platform_ok"] = (exp_p <= got_p) if exp_p else True
        m["platform_precision_ok"] = not (got_p - exp_p - {"tablet"}) if exp_p else True
        m["mode_ok"] = (set(e.get("modes", [])) & set(req["mode"][:2])) != set() if e.get("modes") else True
        m["input_ok"] = set(e.get("inputs", [])) <= set(req["input"])
        m["screen_ok"] = set(e.get("screens", [])) <= set(req["screen"]) if e.get("screens") else True
        m["negatives_ok"] = set(e.get("negatives", [])) <= set(req["negative_constraints"])
        m["missing_ok"] = set(e.get("missing", [])) <= {x["field"] for x in req["missing"]}
        req_c = e.get("required_concerns", [])
        m["required_concern_coverage"] = round(len([x for x in req_c if x in covered]) / len(req_c), 2) if req_c else 1.0
        m["required_concerns_ok"] = all(x in covered for x in req_c)
        derived_req = {x["concern"] for x in g["concerns"]["required"]}
        m["derived_required_agreement"] = round(len([x for x in req_c if x in derived_req]) / len(req_c), 2) if req_c else None
        rec_c = e.get("recommended_concerns", [])
        m["recommended_concern_coverage"] = round(len([x for x in rec_c if x in covered]) / len(rec_c), 2) if rec_c else None
        forb = set(e.get("forbidden_concerns", []))
        m["forbidden_violations"] = [it["id"] for it in bundle if set(it["concerns"]) and set(it["concerns"]) <= forb]
        concepts = e.get("concepts", [])
        hit = [k for k in concepts if _concept_hit(k, text, text_tokens)]
        m["concept_recall"] = round(len(hit) / len(concepts), 2) if concepts else None
        off = [k for k in e.get("offtarget", []) if _concept_hit(k, text, text_tokens)]
        m["offtarget_rate"] = round(len(off) / len(e["offtarget"]), 2) if e.get("offtarget") else 0.0
        m["bundle_size"] = g["metrics"]["bundle_size"]; m["bundle_bytes"] = len(json.dumps(bundle))
        m["empty"] = not bundle
        m["status"] = g["status"]
        m["facet_coverage"] = g["metrics"]["facet_coverage"]
        if c.get("expect_abstain"):
            ok = g["status"] in ("ABSTAIN", "AMBIGUOUS") or req["activation"]["decision"] == "skip"
            m["abstain_ok"] = ok
        else:
            ok = (m["platform_ok"] and m["platform_precision_ok"] and m["mode_ok"] and m["input_ok"] and m["negatives_ok"]
                  and m["required_concerns_ok"] and not m["forbidden_violations"]
                  and (m["concept_recall"] is None or m["concept_recall"] >= 0.5) and m["offtarget_rate"] <= 0.34 and not m["empty"])
            m["recall_at_least_half"] = bool(m["concept_recall"] is not None and m["concept_recall"] >= 0.5)
        out.append({"id": c["id"], "ok": ok, "category": c.get("category"), "metrics": m,
                    "detail": f"plat {sorted(got_p)} modes {req['mode'][:2]} concerns {m['required_concern_coverage']} recall {m['concept_recall']} off {m['offtarget_rate']} hit={hit} off={off} forbidden={m['forbidden_violations']} status={g['status']}"})
    return out


def run_heldout_v3(records, cases):
    """Blind held-out v3: structured expectations scored on the guidance bundle (evals/heldout-v3/THRESHOLDS.md)."""
    out = []
    for c in cases:
        req = core.build_requirements(c["prompt"])
        g = core.guidance(c["prompt"], records, requirements=req)
        bundle = g["core"] + g["guardrails"]
        concepts = set().union(*(set(it.get("concepts", [])) for it in bundle)) if bundle else set()
        m = {}
        abstained = g["status"] == "ABSTAIN" or not req["scope"]["in_scope"]
        m["scope_ok"] = abstained if c.get("expected_scope") == "abstain" else not abstained
        exp_p = set(c.get("expected_platform", [])); got_p = set(req["platform"])
        m["platform_ok"] = (exp_p <= got_p) and not (got_p - exp_p - {"tablet"}) if exp_p else True
        m["mode_ok"] = (set(c.get("expected_modes", [])) & set(req["mode"][:2])) != set() if c.get("expected_modes") else True
        alts = c.get("acceptable_alternatives", {}) or {}
        reqc = c.get("required_concepts", [])
        hit = [x for x in reqc if x in concepts or any(a in concepts for a in alts.get(x, []))]
        m["concept_recall"] = round(len(hit) / len(reqc), 2) if reqc else None
        recc = c.get("recommended_concepts", [])
        m["recommended_recall"] = round(len([x for x in recc if x in concepts]) / len(recc), 2) if recc else None
        m["forbidden_violations"] = sorted(concepts & set(c.get("forbidden_concepts", [])))
        pres_ok = True
        for t in c.get("required_preservation", []):
            key = {"navigation": "preserve_navigation", "typography": "preserve_typography", "color": "preserve_color", "behaviour": "preserve_behaviour", "behavior": "preserve_behaviour"}.get(t)
            if not ((key and req["constraints"].get(key)) or t in req["intent"].get("preserve", [])):
                pres_ok = False
        m["preservation_ok"] = pres_ok
        m["required_concern_coverage"] = g["metrics"].get("coverage_ratio", 0.0)
        m["concept_coverage_ratio"] = g["metrics"].get("concept_coverage_ratio", 0.0)
        m["bundle_size"] = g["metrics"].get("bundle_size", 0); m["bundle_tokens"] = g["metrics"].get("bundle_tokens", 0)
        m["empty"] = not bundle and not abstained
        m["status"] = g["status"]; m["domain"] = req["scope"]["domain"]; m["change_budget"] = req["change_budget"]
        if c.get("expected_scope") == "abstain":
            ok = m["scope_ok"]; m["abstain_ok"] = ok
        else:
            ok = (m["scope_ok"] and m["mode_ok"] and m["platform_ok"] and (m["concept_recall"] is None or m["concept_recall"] >= 0.5)
                  and not m["forbidden_violations"] and pres_ok and not m["empty"])
            m["recall_at_least_half"] = bool(m["concept_recall"] is not None and m["concept_recall"] >= 0.5)
        out.append({"id": c["id"], "ok": ok, "category": c.get("category"), "metrics": m,
                    "detail": f"scope={m['scope_ok']} mode={req['mode'][:2]}/{m['mode_ok']} plat={sorted(got_p)}/{m['platform_ok']} recall={m['concept_recall']} forb={m['forbidden_violations']} pres={pres_ok} status={g['status']}"})
    return out


def _concept_present(cid, concepts, alts):
    return cid in concepts or any(a in concepts for a in (alts or {}).get(cid, []))


def run_heldout_v4(records, cases):
    """Blind held-out v4 (evals/heldout-v4/THRESHOLDS.md): scope kinds, artifact state, multi-mode credit,
    platform correctness with false assignment tracked separately, required/critical/recommended concept recall
    with alias credit, forbidden concepts, preservation."""
    import de_semantic as sem
    out = []
    for c in cases:
        req = core.build_requirements(c["prompt"])
        g = core.guidance(c["prompt"], records, requirements=req)
        bundle = g["core"] + g["guardrails"]
        concepts = set().union(*(set(it.get("concepts", [])) for it in bundle)) if bundle else set()
        m = {}
        abstained = g["status"] == "ABSTAIN" or not req["scope"]["in_scope"]
        exp_scope = c.get("scope", "in-scope")
        m["scope_ok"] = abstained if exp_scope == "abstain" else not abstained
        m["scope_kind"] = req["scope"].get("kind")
        acc_modes = set(c.get("acceptable_modes", []))
        top2 = req["mode"][:2]
        m["mode_ok"] = bool(acc_modes & set(top2)) if acc_modes else True
        m["mode_fundamental_miss"] = bool(acc_modes) and not m["mode_ok"] and req["mode"][0] == "create" and not (acc_modes & {"create", "reconstruct"})
        m["artifact_ok"] = (req["intent"].get("artifact_state") == c.get("artifact_state")) if c.get("artifact_state") in ("new", "existing") else None
        pl = c.get("platform", {}) or {}
        required_p = set(pl.get("required", [])); acc_p = set(pl.get("acceptable_inferred", [])); got_p = set(req["platform"])
        claim = bool(required_p or acc_p)
        m["platform_claim"] = claim
        if claim:
            wrong = got_p - required_p - acc_p - {"tablet"}
            m["platform_false"] = bool(wrong)
            m["platform_unknown"] = bool(required_p - got_p) and not wrong
            m["platform_ok"] = (required_p <= got_p) and not wrong
        else:
            m["platform_false"] = False; m["platform_unknown"] = False; m["platform_ok"] = True
        alts = c.get("acceptable_alternatives", {}) or {}
        reqc = c.get("required_concepts", []); crit = c.get("critical_concepts", []); recc = c.get("recommended_concepts", [])
        m["concept_recall"] = round(sum(1 for x in reqc if _concept_present(x, concepts, alts)) / len(reqc), 2) if reqc else None
        m["critical_recall"] = round(sum(1 for x in crit if _concept_present(x, concepts, alts)) / len(crit), 2) if crit else None
        m["recommended_recall"] = round(sum(1 for x in recc if _concept_present(x, concepts, alts)) / len(recc), 2) if recc else None
        m["forbidden_violations"] = sorted(concepts & set(c.get("forbidden_concepts", [])))
        reqcn = c.get("required_concerns", [])
        covered_c = set().union(*(set(it["concerns"]) for it in bundle)) if bundle else set()
        m["required_concern_coverage"] = round(sum(1 for x in reqcn if x in covered_c) / len(reqcn), 2) if reqcn else g["metrics"].get("coverage_ratio", 0.0)
        pres_ok = True
        for t in c.get("preservation", []):
            key = {"navigation": "preserve_navigation", "typography": "preserve_typography", "color": "preserve_color", "behaviour": "preserve_behaviour", "behavior": "preserve_behaviour"}.get(t)
            if not ((key and req["constraints"].get(key)) or t in req["intent"].get("preserve", [])):
                pres_ok = False
        m["preservation_ok"] = pres_ok
        m["bundle_size"] = g["metrics"].get("bundle_size", 0); m["bundle_tokens"] = g["metrics"].get("bundle_tokens", 0)
        m["empty"] = not bundle and not abstained
        m["status"] = g["status"]; m["domain"] = req["scope"]["domain"]; m["change_budget"] = req["change_budget"]; m["modes"] = top2
        if exp_scope == "abstain":
            ok = m["scope_ok"]; m["abstain_ok"] = ok
        else:
            ok = (m["scope_ok"] and m["mode_ok"] and m["platform_ok"] and (m["concept_recall"] is None or m["concept_recall"] >= 0.5)
                  and not m["forbidden_violations"] and pres_ok and not m["empty"])
        out.append({"id": c["id"], "ok": ok, "category": c.get("category"), "metrics": m,
                    "detail": f"scope={m['scope_ok']}/{m['scope_kind']} mode={top2}/{m['mode_ok']} plat={sorted(got_p)}/{m['platform_ok']}{'!' if m['platform_false'] else ''} recall={m['concept_recall']} crit={m['critical_recall']} forb={m['forbidden_violations']} pres={pres_ok} status={g['status']}"})
    return out


def heldout_v4_summary(results):
    ms = [r["metrics"] for r in results if "metrics" in r]
    non = [m for m in ms if "abstain_ok" not in m]; abst = [m for m in ms if "abstain_ok" in m]
    claims = [m for m in non if m["platform_claim"]]
    def mean(vals): return round(sum(vals) / len(vals), 3) if vals else None
    return {
        "cases": len(ms), "abstain_cases": len(abst), "acceptable": sum(1 for r in results if r["ok"]),
        "scope_correct": sum(1 for m in ms if m["scope_ok"]), "abstain_correct": sum(1 for m in abst if m["abstain_ok"]),
        "scope_kinds": {k: sum(1 for m in ms if m["scope_kind"] == k) for k in ("in-scope", "partial", "abstain")},
        "platform_claims": len(claims), "platform_correct": sum(1 for m in claims if m["platform_ok"]),
        "platform_false_assignment": sum(1 for m in claims if m["platform_false"]), "platform_unknown": sum(1 for m in claims if m["platform_unknown"]),
        "mode_correct": sum(1 for m in non if m["mode_ok"]), "mode_fundamental_miss": sum(1 for m in non if m["mode_fundamental_miss"]),
        "artifact_state_correct": sum(1 for m in non if m["artifact_ok"]), "artifact_state_claims": sum(1 for m in non if m["artifact_ok"] is not None),
        "mean_concept_recall": mean([m["concept_recall"] for m in non if m["concept_recall"] is not None]),
        "concept_recall_ge_half": sum(1 for m in non if m["concept_recall"] is not None and m["concept_recall"] >= 0.5),
        "mean_critical_recall": mean([m["critical_recall"] for m in non if m["critical_recall"] is not None]),
        "critical_cases": sum(1 for m in non if m["critical_recall"] is not None),
        "mean_recommended_recall": mean([m["recommended_recall"] for m in non if m["recommended_recall"] is not None]),
        "forbidden_violation_cases": sum(1 for m in non if m["forbidden_violations"]),
        "preservation_correct": sum(1 for m in non if m["preservation_ok"]),
        "mean_required_concern_coverage": mean([m["required_concern_coverage"] for m in non]),
        "mean_bundle_size": mean([m["bundle_size"] for m in non]), "mean_bundle_tokens": mean([m["bundle_tokens"] for m in non]),
        "empty_results": sum(1 for m in non if m["empty"]),
        "status_counts": {s_: sum(1 for m in ms if m["status"] == s_) for s_ in ("CONFIDENT", "PARTIAL", "AMBIGUOUS", "ABSTAIN")},
        "by_category": {cat: {"n": sum(1 for r in results if r.get("category") == cat), "ok": sum(1 for r in results if r.get("category") == cat and r["ok"])} for cat in sorted({r.get("category") for r in results})},
    }


def run_heldout_v5(records, cases):
    """Blind held-out v5 (evals/heldout-v5/THRESHOLDS.md): v4 scoring plus the three-way platform outcome
    (resolved-correct / unresolved / resolved-wrong, expect_unknown cases), stress tags and per-case bundle
    quality counts. Empty bundles on in-scope cases are reported, not failed."""
    out = run_heldout_v4(records, cases)
    by_id = {c["id"]: c for c in cases}
    for r in out:
        c = by_id[r["id"]]; m = r["metrics"]
        pl = c.get("platform", {}) or {}
        req = core.build_requirements(c["prompt"])
        got_p = set(req["platform"])
        required_p = set(pl.get("required", [])); acc_p = set(pl.get("acceptable_inferred", []))
        m["platform_expect_unknown"] = bool(pl.get("expect_unknown"))
        if pl.get("expect_unknown"):
            m["platform_claim"] = True
            m["platform_false"] = bool(got_p); m["platform_unknown"] = not got_p; m["platform_ok"] = not got_p
        if m["platform_claim"]:
            m["platform_outcome"] = "resolved-wrong" if m["platform_false"] else ("unresolved" if m["platform_unknown"] else "resolved-correct")
        else:
            m["platform_outcome"] = "no-claim"
        m["stress"] = c.get("stress", "none")
        g = core.guidance(c["prompt"], records, requirements=req, explain=True)
        qs = [v.get("quality") for v in (g.get("marginal") or {}).values()]
        m["quality_counts"] = {q: qs.count(q) for q in ("DIRECT", "SPECIFIC", "GENERIC", "INCIDENTAL") if qs.count(q)}
        m["critical_uncovered"] = (g["metrics"].get("critical_trace") or {}).get("uncovered", [])
        if c.get("scope", "in-scope") != "abstain":
            r["ok"] = (m["scope_ok"] and m["mode_ok"] and m["platform_ok"] and (m["concept_recall"] is None or m["concept_recall"] >= 0.5)
                       and not m["forbidden_violations"] and m["preservation_ok"])
        r["detail"] += f" platform={m['platform_outcome']} quality={m['quality_counts']}"
    return out


def heldout_v5_summary(results):
    s = heldout_v4_summary(results)
    ms = [r["metrics"] for r in results if "metrics" in r]
    non = [m for m in ms if "abstain_ok" not in m]
    claims = [m for m in non if m.get("platform_claim")]
    s["platform_claims"] = len(claims)
    s["platform_resolved_correct"] = sum(1 for m in claims if m.get("platform_outcome") == "resolved-correct")
    s["platform_unresolved"] = sum(1 for m in claims if m.get("platform_outcome") == "unresolved")
    s["platform_resolved_wrong"] = sum(1 for m in claims if m.get("platform_outcome") == "resolved-wrong")
    s["platform_correct"] = s["platform_resolved_correct"]; s["platform_false_assignment"] = s["platform_resolved_wrong"]; s["platform_unknown"] = s["platform_unresolved"]
    s["platform_resolution_rate"] = round((s["platform_resolved_correct"] + s["platform_resolved_wrong"]) / max(1, len(claims)), 3)
    s["expect_unknown_cases"] = sum(1 for m in claims if m.get("platform_expect_unknown"))
    s["expect_unknown_correct"] = sum(1 for m in claims if m.get("platform_expect_unknown") and m.get("platform_outcome") == "unresolved")
    s["critical_uncovered_cases"] = sum(1 for m in non if m.get("critical_uncovered"))
    s["quality_totals"] = {q: sum(m.get("quality_counts", {}).get(q, 0) for m in non) for q in ("DIRECT", "SPECIFIC", "GENERIC", "INCIDENTAL")}
    s["by_stress"] = {st: {"n": sum(1 for r in results if r["metrics"].get("stress") == st), "ok": sum(1 for r in results if r["metrics"].get("stress") == st and r["ok"])} for st in sorted({r["metrics"].get("stress", "none") for r in results})}
    return s


def heldout_v3_summary(results):
    ms = [r["metrics"] for r in results if "metrics" in r]
    non = [m for m in ms if "abstain_ok" not in m]; abst = [m for m in ms if "abstain_ok" in m]
    n = len(ms) or 1
    def mean(vals): return round(sum(vals) / len(vals), 3) if vals else None
    return {
        "cases": len(ms), "abstain_cases": len(abst), "acceptable": sum(1 for r in results if r["ok"]),
        "scope_correct": sum(1 for m in ms if m["scope_ok"]), "abstain_correct": sum(1 for m in abst if m["abstain_ok"]),
        "platform_correct": sum(1 for m in non if m["platform_ok"]), "mode_correct": sum(1 for m in non if m["mode_ok"]),
        "mean_concept_recall": mean([m["concept_recall"] for m in non if m["concept_recall"] is not None]),
        "concept_recall_ge_half": sum(1 for m in non if m.get("recall_at_least_half")),
        "mean_recommended_recall": mean([m["recommended_recall"] for m in non if m["recommended_recall"] is not None]),
        "forbidden_violation_cases": sum(1 for m in non if m["forbidden_violations"]),
        "preservation_correct": sum(1 for m in non if m["preservation_ok"]),
        "mean_required_concern_coverage": mean([m["required_concern_coverage"] for m in non]),
        "mean_bundle_size": mean([m["bundle_size"] for m in non]), "mean_bundle_tokens": mean([m["bundle_tokens"] for m in non]),
        "empty_results": sum(1 for m in non if m["empty"]),
        "status_counts": {s: sum(1 for m in ms if m["status"] == s) for s in ("CONFIDENT", "PARTIAL", "AMBIGUOUS", "ABSTAIN")},
        "by_category": {cat: {"n": sum(1 for r in results if r.get("category") == cat), "ok": sum(1 for r in results if r.get("category") == cat and r["ok"])} for cat in sorted({r.get("category") for r in results})},
    }


def run_guidance(records, cases):
    out = []
    for c in cases:
        proj = _fixture_project(c.get("fixture"))
        req = core.build_requirements(c["query"], project=proj, hints=c.get("hints"))
        g = core.guidance(c["query"], records, requirements=req)
        problems = []
        ids = [it["id"] for it in g["core"] + g["guardrails"]]
        concepts = set().union(*(set(it.get("concepts", [])) for it in g["core"] + g["guardrails"])) if ids else set()
        text = " ".join(f"{it['title']} {it['guidance']}" for it in g["core"] + g["guardrails"]).lower()
        required = [e["concern"] for e in g["concerns"]["required"]]
        m = g["metrics"]
        for cn in c.get("expect_required_concerns", []):
            if cn not in required:
                problems.append(f"concern {cn} not required (got {required})")
            elif cn not in m["covered_required_concerns"]:
                problems.append(f"required concern {cn} not covered")
        for cid in c.get("expect_concepts", []):
            if cid not in concepts:
                problems.append(f"concept {cid} not in bundle")
        for i in c.get("expect_ids", []):
            if i not in ids:
                problems.append(f"missing {i}")
        if c.get("expect_ids_any") and not any(i in ids for i in c["expect_ids_any"]):
            problems.append(f"none of {c['expect_ids_any']}")
        for i in c.get("forbid_ids", []):
            if i in ids:
                problems.append(f"forbidden {i} present")
        for cid in c.get("forbid_concepts", []):
            if cid in concepts:
                problems.append(f"forbidden concept {cid} present")
        kinds_sel = [it.get("kind") for it in g["core"] + g["guardrails"]]
        for kd in c.get("forbid_kinds", []):
            if kd in kinds_sel:
                problems.append(f"forbidden kind {kd} in bundle ({[it['id'] for it in g['core'] + g['guardrails'] if it.get('kind') == kd]})")
        if c.get("expect_kinds_any") and not (set(c["expect_kinds_any"]) & set(kinds_sel)):
            problems.append(f"none of kinds {c['expect_kinds_any']} in bundle")
        if c.get("expect_coverage_min") is not None and m["coverage_ratio"] < c["expect_coverage_min"]:
            problems.append(f"coverage {m['coverage_ratio']} < {c['expect_coverage_min']} (uncovered {m['uncovered_required_concerns']})")
        if c.get("max_bundle") and m["bundle_size"] > c["max_bundle"]:
            problems.append(f"bundle {m['bundle_size']} > {c['max_bundle']}")
        if c.get("min_bundle") and m["bundle_size"] < c["min_bundle"]:
            problems.append(f"bundle {m['bundle_size']} < {c['min_bundle']}")
        if c.get("max_guardrails") and m["guardrail_size"] > c["max_guardrails"]:
            problems.append(f"guardrails {m['guardrail_size']} > {c['max_guardrails']}")
        if c.get("expect_status") and g["status"] != c["expect_status"]:
            problems.append(f"status {g['status']} != {c['expect_status']}")
        if c.get("expect_scope_kind") and g.get("scope", {}).get("kind") != c["expect_scope_kind"]:
            problems.append(f"scope kind {g.get('scope', {}).get('kind')} != {c['expect_scope_kind']}")
        if c.get("max_required_concepts") and len(g["concerns"]["required_concepts"]) > c["max_required_concepts"]:
            problems.append(f"required concepts {len(g['concerns']['required_concepts'])} > {c['max_required_concepts']}")
        if c.get("expect_risk") and req["risk"] != c["expect_risk"]:
            problems.append(f"risk {req['risk']} != {c['expect_risk']}")
        for st in c.get("expect_subtypes", []):
            if st not in req["screen_subtype"]:
                problems.append(f"subtype {st} not detected")
        if c.get("expect_modes_any") and not set(c["expect_modes_any"]) & set(req["mode"][:2]):
            problems.append(f"modes {req['mode'][:2]} lack any of {c['expect_modes_any']}")
        if c.get("expect_primary_mode") and req["mode"][0] != c["expect_primary_mode"]:
            problems.append(f"primary mode {req['mode'][0]} != {c['expect_primary_mode']}")
        if c.get("forbid_primary_mode") and req["mode"][0] == c["forbid_primary_mode"]:
            problems.append(f"primary mode is {req['mode'][0]}")
        for pl in c.get("expect_platforms", []):
            if pl not in req["platform"]:
                problems.append(f"platform {pl} not detected ({req['platform']})")
        for pl in c.get("forbid_platforms", []):
            if pl in req["platform"]:
                problems.append(f"platform {pl} wrongly detected")
        for en in c.get("forbid_environment", []):
            if en in req["environment"]:
                problems.append(f"environment {en} wrongly detected")
        for pr in c.get("forbid_products", []):
            if pr in req["product"]:
                problems.append(f"product {pr} wrongly detected")
        for x in c.get("forbid_components", []):
            if x in req["components"]:
                problems.append(f"component {x} wrongly detected")
        for x in c.get("forbid_screens", []):
            if x in req["screen"]:
                problems.append(f"screen {x} wrongly detected")
        for t in c.get("expect_preserve", []):
            if t not in req["intent"]["preserve"] and not req["constraints"].get({"navigation": "preserve_navigation", "typography": "preserve_typography", "color": "preserve_color", "behaviour": "preserve_behaviour"}.get(t, "")):
                problems.append(f"preserve lacks {t} ({req['intent']['preserve']})")
        if c.get("expect_requirements_status") and core.requirements_status(req) != c["expect_requirements_status"]:
            problems.append(f"requirements status {core.requirements_status(req)} != {c['expect_requirements_status']}")
        if c.get("direction_ok") is not None:
            d = core.direction(c["query"], records=records, requirements=req)
            if d["validation"]["ok"] != c["direction_ok"]:
                problems.append(f"direction validation ok={d['validation']['ok']}: {d['validation']['violations']}")
            for slot, forbidden in c.get("forbid_direction_slots", {}).items():
                if (d["direction"].get(slot) or {}).get("id") in forbidden:
                    problems.append(f"direction slot {slot} = {d['direction'][slot]['id']} (forbidden)")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"bundle={ids} cov={m['coverage_ratio']}"})
    return out


def run_scope(records, cases):
    out = []
    for c in cases:
        req = core.build_requirements(c["query"])
        sc = req["scope"]; problems = []
        if c.get("expect_domain_any") and sc["domain"] not in c["expect_domain_any"]:
            problems.append(f"domain {sc['domain']} not in {c['expect_domain_any']}")
        if c.get("expect_in_scope") is not None and sc["in_scope"] != c["expect_in_scope"]:
            problems.append(f"in_scope {sc['in_scope']} != {c['expect_in_scope']} ({sc['reason']})")
        if c.get("expect_reason_contains") and c["expect_reason_contains"].lower() not in (sc.get("reason") or "").lower():
            problems.append(f"reason lacks '{c['expect_reason_contains']}': {sc.get('reason')}")
        if c.get("expect_concepts") and sc["in_scope"]:
            g = core.guidance(c["query"], records, requirements=req)
            concepts = set().union(*(set(it.get("concepts", [])) for it in g["core"] + g["guardrails"])) if (g["core"] or g["guardrails"]) else set()
            for cid in c["expect_concepts"]:
                if cid not in concepts:
                    problems.append(f"concept {cid} not in bundle")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"{sc['domain']} in_scope={sc['in_scope']}"})
    return out


def run_platform_evidence(records, cases):
    out = []
    for c in cases:
        req = core.build_requirements(c["query"]); problems = []
        got = set(req["platform"]); exp = set(c.get("expect_platforms", [])); acc = set(c.get("acceptable", [])) | {"tablet"} if exp else set(c.get("acceptable", []))
        for pl in exp:
            if pl not in got:
                problems.append(f"platform {pl} missing (got {sorted(got)})")
        for pl in got - exp - acc:
            problems.append(f"platform {pl} wrongly assigned (got {sorted(got)})")
        for pl in c.get("forbid_platforms", []):
            if pl in got:
                problems.append(f"platform {pl} forbidden")
        if c.get("expect_unknown") and got:
            problems.append(f"expected UNKNOWN but got {sorted(got)}")
        if c.get("expect_unknown") and not any(m["field"] == "platform" for m in req["missing"]):
            problems.append("expected a MISSING platform entry")
        for pl, st in c.get("expect_strength", {}).items():
            cand = next((x for x in req["platform_evidence"]["candidates"] if x["platform"] == pl), None)
            if not cand:
                problems.append(f"no candidate for {pl}")
            elif cand["strength"] != st:
                problems.append(f"{pl} strength {cand['strength']} != {st}")
        for i in c.get("expect_inputs", []):
            if i not in req["input"]:
                problems.append(f"input {i} missing ({req['input']})")
        m = {"wrong": bool(got - exp - acc), "unknown": bool(exp - got) and not (got - exp - acc)}
        out.append({"id": c["id"], "ok": not problems, "metrics": m, "detail": "; ".join(problems) or f"platforms={sorted(got)} cands={[(x['platform'], x['strength']) for x in req['platform_evidence']['candidates']]}"})
    return out


def run_mode(records, cases):
    out = []
    for c in cases:
        req = core.build_requirements(c["query"]); problems = []
        modes = req["mode"]; primary = modes[0]; secondary = modes[1:3]
        if c.get("expect_primary") and primary != c["expect_primary"]:
            problems.append(f"primary {primary} != {c['expect_primary']}")
        if c.get("expect_primary_any") and primary not in c["expect_primary_any"]:
            problems.append(f"primary {primary} not in {c['expect_primary_any']}")
        if c.get("forbid_primary") and primary == c["forbid_primary"]:
            problems.append(f"primary is {primary}")
        if c.get("expect_secondary_any") and not set(c["expect_secondary_any"]) & set(modes[1:]):
            problems.append(f"secondary {modes[1:]} lacks {c['expect_secondary_any']}")
        for m in c.get("forbid_secondary", []):
            if m in modes:
                problems.append(f"mode {m} present but forbidden")
        for k, v in c.get("expect_intent", {}).items():
            if k.endswith("_any"):
                base = k[:-4]
                got_v = req["intent"].get(base)
                got_set = set(got_v) if isinstance(got_v, list) else {got_v}
                if not got_set & set(v):
                    problems.append(f"intent.{base}={got_v} lacks any of {v}")
            elif req["intent"].get(k) != v:
                problems.append(f"intent.{k}={req['intent'].get(k)} != {v}")
        if c.get("expect_budget") and req["change_budget"] != c["expect_budget"]:
            problems.append(f"budget {req['change_budget']} != {c['expect_budget']}")
        if c.get("expect_budget_any") and req["change_budget"] not in c["expect_budget_any"]:
            problems.append(f"budget {req['change_budget']} not in {c['expect_budget_any']}")
        if c.get("expect_conflict") and not req["conflicts"]:
            problems.append("no conflict recorded")
        if c.get("expect_status_any") and core.requirements_status(req) not in c["expect_status_any"]:
            problems.append(f"status {core.requirements_status(req)} not in {c['expect_status_any']}")
        for t in c.get("expect_preserve", []):
            if t not in req["intent"]["preserve"]:
                problems.append(f"preserve lacks {t}")
        for pl in c.get("expect_platforms", []):
            if pl not in req["platform"]:
                problems.append(f"platform {pl} missing")
        if c.get("expect_concepts"):
            con = core.derive_concerns(req)
            ids = {x["concept"] for x in con["required_concepts"]} | {x["concept"] for x in con["recommended_concepts"]}
            for cid in c["expect_concepts"]:
                if cid not in ids:
                    problems.append(f"expected concept {cid} not derived")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"modes={modes[:3]} budget={req['change_budget']} evidence={req['mode_evidence'][:2]}"})
    return out


def run_context(records, cases):
    out = []
    for c in cases:
        proj = _fixture_project(c.get("fixture"))
        req = core.build_requirements(c["query"], project=proj); problems = []
        ctx = req["project_context"]
        for k, v in c.get("expect_context", {}).items():
            got = ctx.get(k, {}).get("value")
            if k == "theme" and got == "dual-theme" and v in ("light-first", "dark-first"):
                got = v if (proj or {}).get("design_context", {}).get("theme", {}).get("default") == v.split("-")[0] else got
            if str(got) != str(v):
                problems.append(f"context.{k}={got} != {v}")
        for k, allowed in c.get("expect_context_any_of", {}).items():
            if ctx.get(k, {}).get("value") not in allowed:
                problems.append(f"context.{k}={ctx.get(k, {}).get('value')} not in {allowed}")
        for pl in c.get("expect_platforms_ctx", []):
            if pl not in req["platform"]:
                problems.append(f"platform {pl} not detected from the project ({req['platform']})")
        for pl in c.get("forbid_platforms_ctx", []):
            if pl in req["platform"]:
                problems.append(f"platform {pl} wrongly detected from the project")
        for k, allowed in c.get("expect_context_status", {}).items():
            if ctx.get(k, {}).get("status") not in allowed:
                problems.append(f"context.{k}.status={ctx.get(k, {}).get('status')} not in {allowed}")
        if c.get("expect_budget") and req["change_budget"] != c["expect_budget"]:
            problems.append(f"budget {req['change_budget']} != {c['expect_budget']}")
        if c.get("expect_budget_any") and req["change_budget"] not in c["expect_budget_any"]:
            problems.append(f"budget {req['change_budget']} not in {c['expect_budget_any']}")
        # Phase 5 round-1 keys
        if c.get("expect_scope_kind") and req["scope"].get("kind") != c["expect_scope_kind"]:
            problems.append(f"scope.kind {req['scope'].get('kind')} != {c['expect_scope_kind']} ({req['scope'].get('reason')})")
        for pr in c.get("forbid_products_ctx", []):
            if pr in req["product"]:
                problems.append(f"product {pr} wrongly detected from the project")
        for pr in c.get("expect_products_ctx", []):
            if pr not in req["product"]:
                problems.append(f"product {pr} not detected from the project ({req['product']})")
        for en in c.get("expect_environment_ctx", []):
            if en not in req["environment"]:
                problems.append(f"environment {en} not detected from the project ({req['environment']})")
        if c.get("expect_no_missing_platform") and any(m.get("field") == "platform" for m in req.get("missing", [])):
            problems.append("MISSING platform entry present although the repository states the platform: " + "; ".join(m["reason"] for m in req["missing"] if m.get("field") == "platform"))
        if c.get("expect_modes_any_ctx") and not (set(c["expect_modes_any_ctx"]) & set(req["mode"][:2])):
            problems.append(f"modes {req['mode'][:2]} share nothing with {c['expect_modes_any_ctx']}")
        d = core.direction(c["query"], records=records, requirements=req)
        comp = d["compatibility"]
        for slot in c.get("expect_preserved", []):
            if comp.get(slot, {}).get("status") != "preserved":
                problems.append(f"slot {slot} not preserved ({comp.get(slot)})")
        for slot in c.get("expect_changed_allowed", []):
            if comp.get(slot, {}).get("status") == "preserved" and slot in d["preservation"]["unjustified_structural_change"]:
                problems.append(f"slot {slot} change flagged unjustified")
        for slot, forbidden in c.get("forbid_direction_slots", {}).items():
            got = (d["direction"].get(slot) or {}).get("id")
            if got in forbidden:
                problems.append(f"direction {slot}={got} forbidden")
        if c.get("direction_ok") is not None and d["validation"]["ok"] != c["direction_ok"]:
            problems.append(f"direction validation ok={d['validation']['ok']}: {d['validation']['violations'][:2]}")
        out.append({"id": c["id"], "ok": not problems, "detail": "; ".join(problems) or f"ctx={{{', '.join(f'{k}={v['value']}' for k, v in ctx.items() if v['status'] != 'UNKNOWN')}}} budget={req['change_budget']} preserved={d['preservation']['preserved']}"})
    return out


SUITES = {"activation": run_activation, "guidance": run_guidance, "scope": run_scope, "mode": run_mode, "context": run_context, "platform_evidence": run_platform_evidence, "retrieval": run_retrieval, "platform": run_platform, "brand": run_brand,
          "accessibility": run_retrieval, "anti-generic": run_retrieval, "project": run_project, "greenfield": run_greenfield,
          "tools": run_tools, "requirements": run_requirements, "conflicts": run_conflicts, "heldout": run_heldout,
          "regression": None}


def load_group(group: str):
    files = sorted((EVALS / group).glob("*.json"))
    for p in files:
        if p.name in ("MANIFEST.json", "benchmark.json", "archive.json"):
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        suite = doc.get("suite", p.stem)
        yield p.stem, suite, doc.get("cases", [])


def _mean(vals):
    return round(sum(vals) / len(vals), 3) if vals else None


def heldout_summary(results):
    ms = [r["metrics"] for r in results if "metrics" in r]
    n = len(ms) or 1
    recall_vals = [m["concept_recall"] for m in ms if m["concept_recall"] is not None]
    by_cat = {}
    for r in results:
        d = by_cat.setdefault(r.get("category", "?"), {"n": 0, "ok": 0})
        d["n"] += 1; d["ok"] += int(r["ok"])
    return {
        "cases": len(ms),
        "acceptable": sum(1 for r in results if r["ok"]),
        "platform_correct": sum(1 for m in ms if m["platform_ok"]),
        "platform_precise": sum(1 for m in ms if m["platform_precision_ok"]),
        "mode_correct": sum(1 for m in ms if m["mode_ok"]),
        "input_correct": sum(1 for m in ms if m["input_ok"]),
        "negatives_correct": sum(1 for m in ms if m["negatives_ok"]),
        "missing_correct": sum(1 for m in ms if m["missing_ok"]),
        "mean_concept_recall": round(sum(recall_vals) / len(recall_vals), 3) if recall_vals else None,
        "mean_offtarget_rate": round(sum(m["offtarget_rate"] for m in ms) / n, 3),
        "concept_recall_ge_half": sum(1 for m in ms if m.get("recall_at_least_half")),
        "concept_recall_ge_third": sum(1 for m in ms if m["concept_recall"] is not None and m["concept_recall"] >= 0.34),
        "offtarget_within_third": sum(1 for m in ms if m["offtarget_rate"] <= 0.34),
        "facet_coverage_full": sum(1 for m in ms if m["facet_coverage"] >= 1.0),
        "mean_concern_coverage": round(sum(m.get("concern_coverage", m.get("required_concern_coverage", 0)) for m in ms) / n, 3),
        "mean_bundle_size": round(sum(m.get("bundle_size", 0) for m in ms) / n, 2),
        "mean_bundle_bytes": round(sum(m.get("bundle_bytes", 0) for m in ms) / n),
        "mean_concept_recall_search_k5": _mean([m["concept_recall_search_k5"] for m in ms if m.get("concept_recall_search_k5") is not None]),
        "required_concerns_all_covered": sum(1 for m in ms if m.get("required_concerns_ok")),
        "forbidden_violations": sum(1 for m in ms if m.get("forbidden_violations")),
        "mean_derived_required_agreement": _mean([m["derived_required_agreement"] for m in ms if m.get("derived_required_agreement") is not None]),
        "empty_results": sum(1 for m in ms if m["empty"]),
        "status_counts": {s: sum(1 for m in ms if m["status"] == s) for s in ("CONFIDENT", "PARTIAL", "AMBIGUOUS", "ABSTAIN")},
        "abstain_correct": sum(1 for m in ms if m.get("abstain_ok")),
        "abstain_cases": sum(1 for m in ms if "abstain_ok" in m),
        "by_category": by_cat,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--group", action="append", choices=["development", "regression", "heldout", "heldout-v2", "heldout-v3", "heldout-v4", "heldout-v5", "all"])
    ap.add_argument("--suite", action="append")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    groups = args.group or ["development", "regression"]
    if "all" in groups:
        groups = ["development", "regression", "heldout", "heldout-v2", "heldout-v3", "heldout-v4", "heldout-v5"]
    records = core.load_records()
    report, total_ok, total = {}, 0, 0
    for group in groups:
        for name, suite, cases in load_group(group):
            if args.suite and name not in args.suite and suite not in args.suite:
                continue
            fn = run_heldout if group == "heldout" else run_heldout_v2 if group == "heldout-v2" else run_heldout_v3 if group == "heldout-v3" else run_heldout_v4 if group == "heldout-v4" else run_heldout_v5 if group == "heldout-v5" else SUITES.get(suite)
            if fn is None:
                fn = run_retrieval if group == "regression" and suite == "regression" else SUITES.get(suite, run_retrieval)
            try:
                res = fn(records, cases)
            except Exception as e:  # tool failure must be visible, not silent
                res = [{"id": f"{name}:*", "ok": False, "detail": f"suite crashed: {type(e).__name__}: {e}"}]
            key = f"{group}/{name}"
            report[key] = res
            ok = sum(1 for r in res if r["ok"])
            total_ok += ok
            total += len(res)
            if not args.json:
                print(f"{key:<32} {ok:>3}/{len(res):<3} {'OK' if ok == len(res) else 'FAIL'}")
                for r in res:
                    if not r["ok"] or args.verbose:
                        print(f"   {'✓' if r['ok'] else '✗'} {r['id']}: {r.get('detail', '')}")
            if group in ("heldout", "heldout-v2", "heldout-v3", "heldout-v4", "heldout-v5") and not args.json:
                s = heldout_v5_summary(res) if group == "heldout-v5" else heldout_v4_summary(res) if group == "heldout-v4" else heldout_v3_summary(res) if group == "heldout-v3" else heldout_summary(res)
                print("   held-out summary: " + json.dumps({k: v for k, v in s.items() if k != "by_category"}))
    summary = {"groups": groups, "suites": report, "passed": total_ok, "total": total}
    for key, res in report.items():
        if key.startswith("heldout/") or key.startswith("heldout-v2/"):
            summary.setdefault("heldout_summary", {})[key] = heldout_summary(res)
        if key.startswith("heldout-v3/"):
            summary.setdefault("heldout_summary", {})[key] = heldout_v3_summary(res)
        if key.startswith("heldout-v4/"):
            summary.setdefault("heldout_summary", {})[key] = heldout_v4_summary(res)
        if key.startswith("heldout-v5/"):
            summary.setdefault("heldout_summary", {})[key] = heldout_v5_summary(res)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"TOTAL {total_ok}/{total}")
    sys.exit(0 if total_ok == total else 1)


if __name__ == "__main__":
    main()
