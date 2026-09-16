#!/usr/bin/env python3
"""Validate the design-engineering skill package. Exit 1 on any error.

  python validate_skill.py [--skill-dir PATH] [--json]

Checks (each a small function): SKILL.md frontmatter and size, referenced paths (one level deep),
knowledge records (schema, enums, cross references, duplicates, facet mapping), lexicon/schema
alignment (incl. negative labels, constraint labels, screens), requirements schema on examples,
eval case files (ids, categories, group layout), held-out and activation manifests (hashes, counts),
benchmark JSON schema and Markdown/JSON consistency, documented eval counts in research docs.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import de_core as core  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LINK_RE = re.compile(r"\]\(([^)#]+)\)")
PATH_RE = re.compile(r"`((?:references|platforms|stacks|scripts|data|evals|docs)/[A-Za-z0-9_./-]+)`")
FIRST_PERSON = re.compile(r"\b(I can|I will|I'll|you can use this|use me)\b", re.I)
REQUIREMENT_EXAMPLES = ["Build an Android TV EPG in Compose.", "Audit our checkout form.", "iOS banking app home screen",
                        "WinUI desktop ERP data grid with keyboard shortcuts", "fix the SQL deadlock in the orders service"]


def check_skill_md(skill_dir, errors, warnings):
    p = skill_dir / "SKILL.md"
    if not p.exists():
        errors.append("SKILL.md missing"); return {}
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter"); return {}
    end = text.find("\n---", 4)
    fm, body = text[4:end], text[end + 4:]
    meta = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    name, desc = meta.get("name", ""), meta.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"frontmatter name '{name}' must be lowercase kebab-case ≤64 chars")
    if any(w in name for w in ("anthropic", "claude")):
        errors.append("frontmatter name must not contain reserved words")
    if name and name != skill_dir.name:
        warnings.append(f"frontmatter name '{name}' differs from directory '{skill_dir.name}'")
    if not desc:
        errors.append("frontmatter description missing")
    if len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars; spec maximum is 1024")
    if len(desc) + len(meta.get("when_to_use", "")) > 1536:
        errors.append("description + when_to_use exceeds Claude Code's 1536-char listing cap")
    if "<" in desc and ">" in desc:
        errors.append("description must not contain XML tags")
    if FIRST_PERSON.search(desc):
        warnings.append("description should be written in third person")
    lines = body.count("\n") + 1
    if lines > 500:
        errors.append(f"SKILL.md body is {lines} lines; keep under 500")
    elif lines > 350:
        warnings.append(f"SKILL.md body is {lines} lines; consider trimming")
    for ref in sorted(set(LINK_RE.findall(text)) | set(PATH_RE.findall(text))):
        if ref.startswith(("http://", "https://", "${")):
            continue
        if not (skill_dir / ref).exists():
            errors.append(f"SKILL.md references missing path: {ref}")
    for md in [*(skill_dir / "references").glob("*.md"), *(skill_dir / "platforms").glob("*.md"), *(skill_dir / "stacks").glob("*.md")]:
        t = md.read_text(encoding="utf-8")
        for ref in set(LINK_RE.findall(t)) | set(PATH_RE.findall(t)):
            if ref.startswith(("http://", "https://")):
                continue
            target = (skill_dir / ref) if ref.split("/")[0] in ("references", "platforms", "stacks", "scripts", "data", "evals", "docs") else (md.parent / ref)
            if not target.exists():
                errors.append(f"{md.relative_to(skill_dir)} references missing path: {ref}")
        if t.count("\n") > 100 and "## Contents" not in t and "## Sections" not in t:
            warnings.append(f"{md.relative_to(skill_dir)} is >100 lines without a Contents section")
    return meta


def check_records(skill_dir, errors, warnings):
    try:
        recs = core.load_records(skill_dir / "data")
    except ValueError as e:
        errors.append(str(e)); return []
    ids = Counter(r.get("id") for r in recs)
    errors.extend(f"duplicate record id '{i}' ({n}×)" for i, n in ids.items() if n > 1)
    titles = Counter(r.get("title", "").strip().lower() for r in recs)
    warnings.extend(f"duplicate record title '{t}' ({n}×)" for t, n in titles.items() if n > 1)
    known = set(ids)
    for r in recs:
        errors.extend(core.validate_record(r, known))
    stack_files = {p.stem for p in (skill_dir / "stacks").glob("*.md")}
    used = {k for r in recs for k in r.get("implementation", {}) if k != "any"}
    errors.extend(f"implementation notes reference stack '{s}' but stacks/{s}.md does not exist" for s in sorted(used - stack_files))
    try:
        from fingerprint import ALLOWED
        for r in recs:
            for ax, val in r.get("fingerprint", {}).items():
                if val not in ALLOWED.get(ax, []):
                    errors.append(f"{r['id']}: fingerprint {ax}='{val}' not in allowed values")
    except ImportError:
        warnings.append("fingerprint.py not importable; skipped fingerprint value check")
    # facet mapping: every rule/pattern category must map explicitly (not fall back)
    for r in recs:
        if r["kind"] == "rule" and r["category"] not in core._RULE_FACET:
            warnings.append(f"{r['id']}: rule category '{r['category']}' has no explicit facet mapping (falls back to process)")
        if r["kind"] == "pattern" and r["category"] not in core._PATTERN_FACET:
            warnings.append(f"{r['id']}: pattern category '{r['category']}' has no explicit facet mapping (falls back to layout)")
    seen = {}
    for r in recs:
        key = r.get("guidance", "")[:60].lower()
        if key in seen:
            warnings.append(f"records {seen[key]} and {r['id']} start with the same guidance text")
        seen[key] = r["id"]
    return recs


def check_lexicon(skill_dir, errors, warnings):
    try:
        lex = json.loads((skill_dir / "data" / "lexicon.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"lexicon.json: {e}"); return
    for group, allowed in (("modes", core.MODES), ("platforms", core.PLATFORMS - {"any"}), ("inputs", core.INPUTS - {"any"}),
                           ("products", core.PRODUCTS - {"any"}), ("stacks", core.STACK_GROUPS - {"any"}), ("density", core.DENSITY - {"any"}),
                           ("screens", core.SCREENS - {"any"}), ("negatives", core.NEGATIVE_LABELS)):
        bad = set(lex.get(group, {})) - allowed
        if bad:
            errors.append(f"lexicon.{group} has labels not in schema: {sorted(bad)}")
        missing = allowed - set(lex.get(group, {}))
        if missing and group in ("modes", "platforms", "stacks", "screens"):
            warnings.append(f"lexicon.{group} has no phrases for {sorted(missing)}")
    for p in lex.get("stack_platforms", {}):
        if p not in core.STACK_GROUPS:
            errors.append(f"lexicon.stack_platforms has unknown stack '{p}'")
    allowed_constraints = {"remote-only", "keyboard-only", "touch-only", "preserve-system", "performance"}
    bad = set(lex.get("constraints", {})) - allowed_constraints
    if bad:
        errors.append(f"lexicon.constraints has unknown labels {sorted(bad)}")
    # stack words must not double as platform evidence (Phase 2 regression)
    stack_phrases = {ph for phs in lex.get("stacks", {}).values() for ph in phs}
    for plat, phrases in lex.get("platforms", {}).items():
        dup = stack_phrases & set(phrases)
        if dup:
            errors.append(f"lexicon.platforms.{plat} contains stack phrases {sorted(dup)}; stacks imply platforms, they are not platform evidence")
    dupes = Counter(ph for phrases in lex["modes"].values() for ph in phrases)
    warnings.extend(f"lexicon phrase '{ph}' appears in {n} mode labels (ambiguous)" for ph, n in dupes.items() if n > 1)


def check_ontology(recs, errors, warnings):
    import de_semantic as sem
    for cid, (label, concern) in sem.CONCEPT_META.items():
        if concern not in core.CONCERNS:
            errors.append(f"concept {cid}: primary concern '{concern}' not in taxonomy")
        ns = cid.split(".")[0]
        if ns not in ("a11y", "interaction", "navigation", "layout", "state", "form", "table", "data", "adaptive", "touch", "tv", "desktop", "privacy", "env", "perf", "content", "brand", "motion", "onboarding", "media", "anti", "process", "feedback"):
            errors.append(f"concept {cid}: unknown namespace {ns}")
    for cid, rel in sem.RELATIONS.items():
        if cid not in sem.CONCEPTS:
            errors.append(f"relation source {cid} is not a concept")
        for kind, targets in rel.items():
            if kind not in ("requires", "implies", "related", "conflicts"):
                errors.append(f"relation {cid}: unknown relation kind {kind}")
            for t in targets:
                if t not in sem.CONCEPTS:
                    errors.append(f"relation {cid}.{kind} -> unknown concept {t}")
    if sem.relation_cycles():
        errors.append(f"requires cycles: {sem.relation_cycles()}")
    used = {c for r in recs for c in r.get("concepts", [])}
    for cid in sorted(sem.CONCEPTS - used):
        warnings.append(f"orphan concept '{cid}': no record carries it")
    for r in recs:
        for c in r.get("concepts", []):
            if sem.CONCEPT_CONCERN.get(c) and sem.CONCEPT_CONCERN[c] not in core.record_concerns(r) and r["kind"] in ("rule", "component") and len(r.get("concepts", [])) <= 2:
                warnings.append(f"{r['id']}: concept {c} belongs to concern '{sem.CONCEPT_CONCERN[c]}' which the record does not declare")
    for cid, als in sem.ALIASES.items():
        if cid not in sem.CONCEPTS:
            errors.append(f"alias group for unknown concept {cid}")
        if not als:
            warnings.append(f"alias group for {cid} is empty")
    seen_alias = {}
    for cid, als in sem.ALIASES.items():
        for a in als:
            n = sem.normalize_phrase(a)
            if n in seen_alias and seen_alias[n] != cid:
                errors.append(f"alias '{a}' maps to both {seen_alias[n]} and {cid}")
            seen_alias[n] = cid
    for q in REQUIREMENT_EXAMPLES:
        req = core.build_requirements(q)
        pe = req.get("platform_evidence", {})
        for c in pe.get("candidates", []):
            if c["platform"] not in core.PLATFORMS or c["strength"] not in sem.STRENGTH_ORDER:
                errors.append(f"platform evidence malformed for {q!r}: {c}")
        it = req.get("intent", {})
        if it.get("artifact_state") not in sem.ARTIFACT_STATES or any(o not in sem.OPERATIONS for o in it.get("operations", [])) or it.get("change_scope") not in sem.CHANGE_SCOPES:
            errors.append(f"intent schema malformed for {q!r}: {it}")
        if req["change_budget"] not in core.CHANGE_BUDGETS:
            errors.append(f"change_budget {req['change_budget']} invalid for {q!r}")
        for k in ("navigation", "theme", "surfaces", "radius", "spacing", "typography", "components"):
            v = req["project_context"].get(k)
            if not isinstance(v, dict) or v.get("status") not in ("KNOWN", "INFERRED", "UNKNOWN"):
                errors.append(f"project_context.{k} malformed for {q!r}")


def check_concerns(skill_dir, recs, errors, warnings):
    """Concern/concept taxonomy: every derived concern in range, concept ids valid, guidance bundle contract."""
    for r in recs:
        if not core.record_concerns(r) <= core.CONCERNS:
            errors.append(f"{r['id']}: concerns {core.record_concerns(r)} outside taxonomy")
    used = {c for r in recs for c in r.get("concepts", [])}
    for cid in sorted(core.CONCEPTS - used):
        warnings.append(f"concept id '{cid}' declared in CONCEPTS but no record carries it")
    for q in REQUIREMENT_EXAMPLES:
        req = core.build_requirements(q)
        con = core.derive_concerns(req)
        for e in con["required"] + con["recommended"] + con["optional"]:
            if e["concern"] not in core.CONCERNS:
                errors.append(f"derive_concerns emitted unknown concern {e['concern']} for {q!r}")
        for e in con["required_concepts"] + con["recommended_concepts"]:
            if e["concept"] not in core.CONCEPTS:
                errors.append(f"derive_concerns emitted unknown concept {e['concept']} for {q!r}")
        g = core.guidance(q, recs, requirements=req)
        for key in ("schema", "status", "requirements", "concerns", "core", "guardrails", "metrics"):
            if key not in g:
                errors.append(f"guidance bundle missing '{key}' for {q!r}")
        if g.get("schema") != core.BUNDLE_SCHEMA:
            errors.append("guidance bundle schema mismatch")
        if g["metrics"]["bundle_size"] > 8:
            errors.append(f"guidance bundle for {q!r} exceeds 8 records")


def check_requirements_schema(errors):
    for q in REQUIREMENT_EXAMPLES:
        req = core.build_requirements(q)
        for e in core.validate_requirements(req):
            errors.append(f"requirements schema failed for {q!r}: {e}")
        compact = core.compact_requirements(req)
        if len(json.dumps(compact)) > 4000:
            errors.append(f"compact requirements for {q!r} exceed 4000 chars; keep the contract context-sized")


def _load_cases(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    return doc, doc.get("cases", [])


def check_evals(skill_dir, recs, errors, warnings):
    ids = {r["id"] for r in recs}
    cats = {r["category"] for r in recs}
    evals = skill_dir / "evals"
    for group in ("development", "regression", "heldout"):
        if not (evals / group).is_dir():
            errors.append(f"evals/{group} missing"); continue
        seen_ids = Counter()
        for p in sorted((evals / group).glob("*.json")):
            if p.name in ("MANIFEST.json", "archive.json", "benchmark.json"):
                continue
            try:
                doc, cases = _load_cases(p)
            except (OSError, json.JSONDecodeError) as e:
                errors.append(f"{p}: {e}"); continue
            for c in cases:
                seen_ids[c.get("id")] += 1
                for key in ("expect_ids", "forbid_ids", "expect_any_ids", "forbid_direction_ids"):
                    for i in c.get(key, []):
                        if i not in ids:
                            errors.append(f"{group}/{p.name} case '{c.get('id')}' references unknown record id '{i}'")
                for cat in c.get("expect_categories", []):
                    if cat not in cats:
                        errors.append(f"{group}/{p.name} case '{c.get('id')}' references unknown category '{cat}'")
                for f in c.get("expect_facets", []):
                    if f not in core.FACETS:
                        errors.append(f"{group}/{p.name} case '{c.get('id')}' references unknown facet '{f}'")
                if group == "regression" and not c.get("note"):
                    errors.append(f"regression case '{c.get('id')}' must carry a note describing the defect")
                if group == "heldout" and any(k in c for k in ("expect_ids", "forbid_ids", "expect_any_ids")):
                    errors.append(f"held-out case '{c.get('id')}' must not reference record ids")
        errors.extend(f"duplicate case id '{i}' in evals/{group}" for i, n in seen_ids.items() if n > 1)
    # frozen manifests
    for sub in ("heldout", "activation", "heldout-v2", "heldout-v3", "heldout-v4"):
        man = evals / sub / "MANIFEST.json"
        if not man.exists():
            (warnings if sub in ("heldout-v2", "heldout-v3", "heldout-v4") else errors).append(f"evals/{sub}/MANIFEST.json missing"); continue
        m = json.loads(man.read_text(encoding="utf-8"))
        files = m.get("files") or {m.get("file"): {"sha256": m.get("sha256"), "count": m.get("count")}}
        for fname, info in files.items():
            fp = evals / sub / fname
            if not fp.exists():
                errors.append(f"evals/{sub}/{fname} listed in manifest but missing"); continue
            digest = hashlib.sha256(fp.read_bytes()).hexdigest()
            if digest != info.get("sha256"):
                errors.append(f"evals/{sub}/{fname} hash {digest[:12]} != manifest {str(info.get('sha256'))[:12]} (frozen file was modified)")
            n = len(json.loads(fp.read_text(encoding="utf-8")).get("cases", []))
            if n != info.get("count"):
                errors.append(f"evals/{sub}/{fname} has {n} cases, manifest says {info.get('count')}")


def check_benchmark(skill_dir, errors, warnings):
    research = skill_dir.parent / "research"
    jp, mp = research / "benchmark-results.json", research / "BENCHMARK-RESULTS.md"
    if not jp.exists():
        warnings.append("research/benchmark-results.json missing (run evals/benchmark_upstream.py)"); return
    try:
        data = json.loads(jp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"benchmark-results.json invalid: {e}"); return
    for key in ("schema", "benchmark_method", "date", "versions", "queries", "aggregate", "timing_method"):
        if key not in data:
            errors.append(f"benchmark-results.json missing '{key}'")
    if data.get("schema") != "benchmark-results/v1":
        errors.append("benchmark-results.json schema must be benchmark-results/v1")
    if not mp.exists():
        errors.append("BENCHMARK-RESULTS.md missing"); return
    md = mp.read_text(encoding="utf-8")
    a = data.get("aggregate", {})
    for label, val in (("mean relevant-term coverage", f"{a.get('upstream', {}).get('mean_relevant', -1):.3f} | {a.get('ours', {}).get('mean_relevant', -1):.3f}"),
                       ("mean off-target-term coverage", f"{a.get('upstream', {}).get('mean_offtarget', -1):.3f} | {a.get('ours', {}).get('mean_offtarget', -1):.3f}"),
                       ("empty results", f"{a.get('upstream', {}).get('empty_results')} | {a.get('ours', {}).get('empty_results')}")):
        if f"| {label} | {val} |" not in md:
            errors.append(f"BENCHMARK-RESULTS.md row '{label}' does not match benchmark-results.json (regenerate with --render)")
    if f"method {data.get('benchmark_method')}" not in md:
        errors.append("BENCHMARK-RESULTS.md methodology version does not match JSON")
    # prose documents may only quote canonical numbers
    for doc in ("UPSTREAM-VS-NEW.md", "PHASE2-RESULTS.md"):
        p = research / doc
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r"relevant-term coverage[^|\n]*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)", t):
            up, ours = float(m.group(1)), float(m.group(2))
            if abs(up - a["upstream"]["mean_relevant"]) > 0.006 or abs(ours - a["ours"]["mean_relevant"]) > 0.006:
                errors.append(f"{doc} quotes relevant-term coverage {up}/{ours}; canonical JSON says {a['upstream']['mean_relevant']}/{a['ours']['mean_relevant']}")


def check_doc_counts(skill_dir, errors, warnings):
    """Eval counts quoted in research docs must match the case files."""
    evals = skill_dir / "evals"
    counts = {}
    for group in ("development", "regression", "heldout", "heldout-v2", "heldout-v3", "heldout-v4"):
        counts[group] = sum(len(_load_cases(p)[1]) for p in (evals / group).glob("*.json") if p.name not in ("MANIFEST.json", "archive.json", "benchmark.json"))
    counts["activation"] = len(_load_cases(evals / "activation" / "cases.json")[1]) if (evals / "activation" / "cases.json").exists() else 0
    p = skill_dir.parent / "research" / "PHASE5-RESULTS.md"
    if not p.exists():
        p = skill_dir.parent / "research" / "PHASE4-RESULTS.md"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        for group, n in counts.items():
            m = re.search(rf"{group}[^\n]*?(\d+)\s*cases", t, re.I)
            if m and int(m.group(1)) != n:
                errors.append(f"{p.name} says {group} has {m.group(1)} cases; files contain {n}")
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill-dir", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    skill_dir = Path(args.skill_dir).resolve()
    errors, warnings = [], []
    for required in ("SKILL.md", "scripts/advise.py", "scripts/de_core.py", "scripts/tokens.py", "scripts/fingerprint.py",
                     "scripts/inspect_project.py", "data/lexicon.json", "references", "platforms", "stacks", "evals/run_evals.py"):
        if not (skill_dir / required).exists():
            errors.append(f"missing {required}")
    meta = check_skill_md(skill_dir, errors, warnings)
    recs = check_records(skill_dir, errors, warnings)
    check_lexicon(skill_dir, errors, warnings)
    check_requirements_schema(errors)
    check_concerns(skill_dir, recs, errors, warnings)
    check_ontology(recs, errors, warnings)
    check_evals(skill_dir, recs, errors, warnings)
    check_benchmark(skill_dir, errors, warnings)
    counts = check_doc_counts(skill_dir, errors, warnings)
    summary = {"skill": meta.get("name"), "records": len(recs), "eval_counts": counts, "errors": errors, "warnings": warnings, "ok": not errors}
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"validate_skill: {'OK' if not errors else 'FAIL'} — {len(recs)} records, {len(errors)} errors, {len(warnings)} warnings; cases {counts}")
        for e in errors:
            print("ERROR " + e)
        for w in warnings:
            print("warn  " + w)
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
