# Candidate c4 bundle re-review (guidance-only rescoring of the Phase 6 round)

The 32 tasks were implemented on frozen candidate c3. Fixes routed from that round produced candidate c4. Per protocol, a fix means a new candidate hash and a **guidance-only** rescore: `evals/rescore_projects.py --phase 6 --label c4` wrote `<task>/c4/03-guidance.md` (and `.json`, `02-requirements.json`, `04-direction.json`) for every task. Implementation and render outcomes are NOT re-run; they belong to c3.

Your job (reviewer): for each assigned task, read `<task>/00-expectation.json` (pre-registered critical / expected / forbidden concepts), the task sentence in `TASKS.md`, the c3 review in `<task>/RESULTS.md` (per-record verdicts) and the new `<task>/c4/03-guidance.md`. Then classify **every record in the c4 bundle** as `relevant`, `partial` or `off-target` using the same standard the c3 reviewer applied to the same task (consistency with RESULTS.md matters more than your own taste: a record judged off-target in c3 stays off-target in c4 unless the bundle context genuinely changed its role), and name one Phase 6 category for each partial / off-target record: `generic`, `wrong-screen`, `wrong-product`, `off-platform`, `contradicts-request`, `contradicts-codebase`, `overlong`. Also record whether a pre-registered critical concept is still absent (`missing-critical`, bundle level) and count `unjustified_direction_slots` from `<task>/c4/04-direction.json` (slots with status `changed` or `new` that the task does not justify; the c3 RESULTS.md explains which slots were unjustified before).

Do not modify anything under `design-engineering/` or any existing task file. Write ONE file per task: `<task>/c4/review.json`:

```json
{"task": "p6-NN", "records": [{"id": "...", "verdict": "relevant|partial|off-target", "category": "<or empty>", "why": "<one short sentence>"}],
 "missing_critical": ["concept ids still absent"], "unjustified_direction_slots": 0, "layer_review": {"core": [], "critical": [], "optional": []},
 "change_vs_c3": "<one sentence: better / same / worse and why>"}
```

Be factual and terse. A c4 bundle that is smaller and drops off-target records without losing the record the c3 implementer actually used is "better"; one that drops that record is "worse" even if smaller.
