# Held-out v3 — pre-registered thresholds and stability labels

Written 2026-09-09, **before** v3 generation and before the implementation freeze hash existed. Not changed after the run. The manifest records the sha256 of this file at generation time.

## Case format (structured, no record ids, no required wording)

```json
{"id": "hv3-001", "prompt": "...", "category": "...",
 "expected_scope": "in-scope | abstain",
 "expected_modes": ["..."], "expected_platform": ["..."],
 "required_concepts": ["concept ids from the public ontology"], "recommended_concepts": [], "forbidden_concepts": [],
 "required_preservation": ["navigation | typography | color | behaviour"], "acceptable_alternatives": {"concept id": ["alternative ids"]}}
```

The generator and the expectation reviewer see the ontology (ids + one-line labels), the requirement taxonomy labels and this format. They never see records, lexicon, scripts, or existing cases. The bundle-quality reviewer sees only prompt + bundle guidance text (record ids stripped).

## Per-case scoring (scored on `advise.py guidance`)

- scope correct: `expected_scope == "abstain"` ⇔ bundle status ABSTAIN / requirements out of scope.
- mode correct: at least one expected mode among the two highest detected modes.
- platform correct: expected ⊆ detected and no extra platform beyond `tablet` (empty expected = no claim).
- required concept recall: |required ∩ bundle concepts (with acceptable alternatives)| / |required|.
- forbidden violation: any bundle record whose concepts intersect `forbidden_concepts`.
- preservation correct: every `required_preservation` entry appears in the requirements' preservation constraints (`preserve_*`) or intent preserve list.
- **acceptable** (non-abstain): scope ∧ mode ∧ platform ∧ recall ≥ 0.5 ∧ no forbidden violation ∧ preservation ∧ non-empty.

## Set-level thresholds

| Metric | Threshold | Rationale |
|---|---|---|
| platform correctness | ≥ 0.92 | already 0.95 on v2; must not regress |
| mode correctness | ≥ 0.80 | v2 was 0.61; the intent model targets this |
| scope / abstention correctness | ≥ 0.90 | v2 abstain 0.70; scope model targets this |
| required concern coverage (derived required concerns covered by the bundle) | ≥ 0.90 | v2 0.81 |
| required concept recall (mean) | ≥ 0.60 | v2 phrase recall 0.21; ids are stricter but structural |
| forbidden concept rate (cases with a violation) | ≤ 0.08 | contamination control |
| empty bundle rate | ≤ 0.02 | |
| human bundle review GOOD + PARTIAL | ≥ 0.80 | product goal |
| human bundle review BAD | ≤ 0.20 | |
| acceptable cases | ≥ 0.50 | secondary, reported |

## Stability labels (decided before the run)

- **experimental** — a deterministic gate fails (validator, dev/regression, activation precision < 0.9) or a serious systemic defect in the real-project round.
- **personal-production-ready** — all deterministic gates pass, real projects show the skill helps, but the blind v3 thresholds are materially missed (fewer than 6 of the 9 primary thresholds met, or the human GOOD+PARTIAL threshold missed).
- **stable-candidate** — all deterministic gates pass, at least 7 of the 9 primary thresholds met including human GOOD+PARTIAL ≥ 0.80 and scope ≥ 0.90, and the real-project round shows no serious systemic defect (no class of unjustified structural change, no scope/mode failure class repeated across projects).
- **stable** — not reachable in Phase 4: needs stable-candidate first, real Claude activation validation, more use over time, and a second independent blind run.

Primary thresholds (9): platform, mode, scope, concern coverage, concept recall, forbidden rate, empty rate, human GOOD+PARTIAL, human BAD.
