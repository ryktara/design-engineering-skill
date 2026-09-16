# Held-out v4 — pre-registered thresholds and stability policy

Written 2026-09-09 **before** any Phase 5 development case, implementation change, or v4 generation. Hashed into `research/runs/phase5-freeze.json` and `evals/heldout-v4/MANIFEST.json`. Not edited afterward.

## Why these numbers (review of the Phase 4 rationale)

Phase 4 set platform ≥ 0.92 and mode ≥ 0.80 from synthetic/historical performance; the blind v3 run showed that diverse natural-language prompts (device idioms instead of platform names, observations instead of verbs) are harder than those sets, and that most platform misses were *unknown* rather than *wrong*. Phase 5 therefore measures platform in two parts (correctness, and false assignment) and mode with multi-mode credit, and lowers the aspirational bars to values that still require real semantic generalisation. Concept recall stays close to Phase 4 (0.58 vs 0.60) because the ontology is now stable and the remaining gap is derivation/retrieval, not vocabulary; a critical-concept recall is added because missing the one principle that matters (focus navigation on TV, validation on a form) is worse than missing a nicety. Human usefulness bars rise slightly (0.82 / 0.18) because the Phase 4 result (0.81 / 0.19) must not regress.

## Case format

```json
{"id": "hv4-001", "prompt": "...", "category": "...",
 "scope": "in-scope | partial | abstain",
 "artifact_state": "new | existing | unknown",
 "acceptable_modes": ["..."],
 "platform": {"required": ["..."], "acceptable_inferred": ["..."]},
 "required_concerns": ["..."],
 "required_concepts": ["ids"], "critical_concepts": ["subset of required"], "recommended_concepts": [], "forbidden_concepts": [],
 "preservation": ["navigation | typography | color | behaviour"],
 "acceptable_alternatives": {"id": ["ids"]}}
```

## Per-case scoring (guidance path)

- scope correct: `abstain` ⇔ ABSTAIN status; `partial` and `in-scope` ⇔ guidance produced.
- mode correct: any acceptable mode among the two highest detected modes (multi-mode credit); a `create` primary against an existing artifact with only diagnose/modify modes acceptable is a *fundamental* miss and counted separately.
- platform: correct when every `required` platform is detected and no detected platform lies outside `required ∪ acceptable_inferred ∪ {tablet}`; **false assignment** when a detected platform lies outside that set; **unknown** when a required platform is missing but nothing wrong was assigned. Cases with empty `required` and empty `acceptable_inferred` make no platform claim.
- required concept recall = |required ∩ bundle concepts (with alternatives and canonical aliases)| / |required|; critical recall likewise over `critical_concepts`.
- forbidden violation: any bundle record whose concepts intersect `forbidden_concepts`.
- preservation correct: each `preservation` entry is a preserve constraint or intent target.
- acceptable (non-abstain): scope ∧ mode ∧ platform ∧ recall ≥ 0.5 ∧ no forbidden ∧ preservation ∧ non-empty.

## Set-level thresholds (10 primary)

| # | metric | threshold |
|---|---|---|
| 1 | platform correctness (cases with a platform claim) | ≥ 0.88 |
| 2 | false platform assignment rate (cases with a claim) | ≤ 0.05 |
| 3 | mode correctness (multi-mode credit) | ≥ 0.75 |
| 4 | scope correctness (all cases) | ≥ 0.92 |
| 5 | required concern coverage (mean) | ≥ 0.90 |
| 6 | required concept recall (mean) | ≥ 0.58 |
| 7 | critical concept recall (mean over cases with critical ids) | ≥ 0.80 |
| 8 | forbidden concept rate (cases with a violation) | ≤ 0.05 |
| 9 | human GOOD + PARTIAL | ≥ 0.82 |
| 10 | human BAD | ≤ 0.18 |

Secondary (reported, not counted): empty bundle rate ≤ 0.01, acceptable cases ≥ 0.50, fundamental mode misses ≤ 0.10, guidance mean tokens ≤ 1200 / p95 ≤ 1600.

## Stability policy (decided now)

- **experimental** — any deterministic gate fails, or a severe systemic real-project defect.
- **personal-production-ready** — deterministic gates pass and real projects show the skill helps, but the stable-candidate conditions below are not all met.
- **stable-candidate** — all of: every deterministic gate passes; no severe systemic real-project defect (no class of unjustified structural change, no platform-invalid guidance cluster, no recurring harmful record, no scope/mode failure class repeated across projects); ≥ 8 of the 10 primary thresholds met; **mandatory** regardless of count: #4 scope, #8 forbidden rate, #9 human GOOD+PARTIAL, #10 human BAD, #2 false platform assignment.
- **stable** — not reachable in Phase 5: needs stable-candidate, real Claude activation validation, a second independent blind qualification, continued real-project use, and no severe regression cluster.

Real-model activation is not required for stable-candidate; its absence is stated as a limitation.

## Independence

Generator, expectation reviewer and quality reviewer are separate sessions that see only this file's format section, the public ontology (`evals/heldout-v4/ONTOLOGY.md`, ids + labels), the taxonomy labels, and — for the quality reviewer — the prompt plus guidance text with record ids stripped. Model assignment is recorded in the manifest; if different model families are not available, the same-family limitation is stated, never hidden.
