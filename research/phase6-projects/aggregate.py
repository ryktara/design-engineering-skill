"""Aggregate the Phase 6 implemented project round (research/phase6-projects/p6-*/artifacts.json)
against the pre-registered pass criteria in evals/heldout-v5/THRESHOLDS.md (section "Implemented project round").
Usage: python aggregate.py [--json out.json]"""
import json, glob, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
FREEZE = "ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947"


def num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "p6-*", "artifacts.json"))):
        try:
            a = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("BAD JSON", f, e); continue
        a["_task"] = os.path.basename(os.path.dirname(f)); rows.append(a)
    n = len(rows)
    c = collections.Counter
    plat = c(str(a.get("platform_correct", "?")).lower() for a in rows)
    mode = c(str(a.get("mode_correct", "?")).lower() for a in rows)
    scope = sum(1 for a in rows if a.get("scope_correct") is True)
    crit = [num(a.get("critical_recall"), None) for a in rows if a.get("critical_recall") is not None]
    rec = [num(a.get("concept_recall"), None) for a in rows if a.get("concept_recall") is not None]
    effect = c(str(a.get("skill_effect", "?")).lower() for a in rows)
    hashes_ok = sum(1 for a in rows if str(a.get("build_hash_start", "")).startswith(FREEZE[:8]) and str(a.get("build_hash_end", "")).startswith(FREEZE[:8]))
    rel = sum(int(num(a.get("guidance_relevant"))) for a in rows); par = sum(int(num(a.get("guidance_partial"))) for a in rows); off = sum(int(num(a.get("guidance_offtarget"))) for a in rows)
    reviewed = rel + par + off
    bad = c(); bad_records = c()
    for a in rows:
        for b in a.get("bad_guidance", []) or []:
            bad[str(b.get("category", "?"))] += 1
            if b.get("record") and b["record"] not in ("bundle", "(bundle)", None):
                bad_records[b["record"]] += 1
    forbidden_tasks = sum(1 for a in rows if any(m.get("layer") == "forbidden" for m in a.get("misses", []) or []) or a.get("forbidden_delivered"))
    unjust = sum(int(num((a.get("preservation") or {}).get("unjustified_structural_change"))) for a in rows)
    unjust_dir = sum(int(num(a.get("unjustified_direction_slots"))) for a in rows)
    proc = sum(1 for a in rows if a.get("process_records_needed") is True)
    first = c(); final = c()
    for a in rows:
        for k, v in (a.get("first_render_defects") or {}).items(): first[k] += int(num(v))
        for k, v in (a.get("final_defects") or {}).items(): final[k] += int(num(v))
    layers = c()
    for a in rows:
        for m in a.get("misses", []) or []: layers[m.get("layer", "?")] += 1
        for m in a.get("concept_misses", []) or []: layers["concept:" + str(m.get("layer", "?"))] += 1
    tokens = [num(a.get("guidance_tokens"), None) for a in rows if a.get("guidance_tokens")]
    off_wrong = sum(bad[k] for k in ("generic", "wrong-screen", "wrong-product"))
    mean = lambda v: round(sum(v) / len(v), 3) if v else None
    crit_mean = mean(crit); mode_ok = (mode.get("yes", 0) + mode.get("acceptable", 0)) / max(1, n)
    criteria = {
        "platform_resolved_wrong_eq_0": plat.get("wrong", 0) == 0,
        "scope_correct_all": scope == n,
        "mode_yes_or_acceptable_ge_0.85": mode_ok >= 0.85,
        "critical_recall_mean_ge_0.80": (crit_mean or 0) >= 0.80,
        "forbidden_delivery_tasks_le_2": forbidden_tasks <= 2,
        "hurt_le_3": effect.get("hurt", 0) <= 3,
        "helped_ge_0.5": effect.get("helped", 0) / max(1, n) >= 0.5,
        "generic+wrong-screen+wrong-product_records_le_0.20": (off_wrong / max(1, reviewed)) <= 0.20,
        "unjustified_direction_slots_le_2": unjust_dir <= 2,
    }
    out = {"tasks": n, "frozen_hash_both_ends": hashes_ok, "platform": dict(plat), "mode": dict(mode), "mode_yes_or_acceptable_rate": round(mode_ok, 3), "scope_correct": scope,
           "critical_recall_mean": crit_mean, "critical_recall_by_task": {a["_task"]: a.get("critical_recall") for a in rows}, "concept_recall_mean": mean(rec),
           "skill_effect": dict(effect), "records_reviewed": reviewed, "relevant": rel, "partial": par, "offtarget": off, "bad_guidance_categories": dict(bad),
           "offtarget_rate_generic_wrongscreen_wrongproduct": round(off_wrong / max(1, reviewed), 3), "recurring_bad_records": dict(bad_records.most_common(12)),
           "forbidden_delivery_tasks": forbidden_tasks, "unjustified_structural_changes": unjust, "unjustified_direction_slots": unjust_dir, "process_records_needed_tasks": proc,
           "first_render_defects": dict(first), "final_defects": dict(final), "miss_layers": dict(layers), "guidance_tokens_mean": mean(tokens),
           "criteria": criteria, "criteria_met": sum(1 for v in criteria.values() if v), "criteria_total": len(criteria), "round_pass": all(criteria.values())}
    print(json.dumps(out, indent=1))
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
