# Held-out v5 — pre-registered thresholds and stability policy (Phase 6)

Written 2026-09-10 **before** v5 generation, on the frozen candidate c3 (`research/runs/phase6-freeze-c3.json`), after the Phase 6 development work and before the implemented project round was scored. Hashed into `evals/heldout-v5/THRESHOLDS.sha256` and later into `research/runs/phase6-freeze.json` and `evals/heldout-v5/MANIFEST.json`. **Never lowered afterward.** Held-out v1–v4 are historical (non-blind) from Phase 6 on; v5 is the only blind judge of this phase.

## Why these numbers

v4 (Phase 5, blind, 434 cases) met 3 of 10 thresholds. The misses were dominated by three defect classes (generic guardrails, wrong-screen cores, missing critical concepts) and by platform UNKNOWN (44 %), not by wrong platforms (3 %). Phase 6 changed only the layers responsible. The bars below are therefore *tighter* than v4 on what Phase 6 fixed (mode, scope, critical recall, human quality, and two new defect-rate bars) and *looser only* on platform correctness, because the Phase 6 contract prefers UNKNOWN over a wrong platform and the v4 measurement counted every UNKNOWN as a miss. Platform is reported in three parts (resolved-correct / unresolved / resolved-wrong) plus the resolution rate so the trade-off is visible, never hidden.

## Case format

```json
{"id": "hv5-001", "prompt": "...", "category": "create | refactor-fix | polish | audit-review | accessibility | responsive | tv-media | desktop-native | mobile-native | kiosk-public | adversarial",
 "stress": "none | wrong-screen | generic-guardrail",
 "scope": "in-scope | partial | abstain",
 "artifact_state": "new | existing | unknown",
 "acceptable_modes": ["..."],
 "platform": {"required": ["..."], "acceptable_inferred": ["..."], "expect_unknown": false},
 "required_concepts": ["ids"], "critical_concepts": ["1-3 ids, subset of required"], "recommended_concepts": [], "forbidden_concepts": [],
 "preservation": ["navigation | typography | color | behaviour"],
 "acceptable_alternatives": {"id": ["ids"]}}
```

Prompts are natural developer-typed sentences (observations, questions, half-sentences, typos allowed), written by a generator that has no access to the records, lexicon, cases or code; expectations are set by a separate expectation reviewer from the public ontology (`evals/heldout-v5/ONTOLOGY.md`, ids + labels only). Suggested mix (≥ 500): create 70 · refactor/fix 100 · polish 60 · audit/review 50 · accessibility 45 · responsive 40 · TV/media 35 · desktop-native 30 · mobile-native 30 · kiosk/public 25 · adversarial 40; plus the wrong-screen and generic-guardrail stress sets (tagged `stress`) inside those counts.

## Per-case scoring (guidance path, `evals/run_evals.py --group heldout-v5`)

- scope correct: `abstain` ⇔ ABSTAIN / OUT_OF_SCOPE status; `partial` and `in-scope` ⇔ guidance produced.
- mode correct: any acceptable mode among the two highest detected modes; a `create` primary on an existing artifact with only change modes acceptable is a *fundamental* miss (reported separately).
- platform, on cases that make a claim (`required` non-empty or `expect_unknown`): **resolved-correct** when every required platform is resolved and nothing outside `required ∪ acceptable_inferred ∪ {tablet}` is; **resolved-wrong** when a resolved platform lies outside that set, or anything is resolved on an `expect_unknown` case; **unresolved** otherwise (a required platform missing, nothing wrong). Resolution rate = (resolved-correct + resolved-wrong) / claims.
- required concept recall = |required ∩ bundle concepts (with alternatives)| / |required|; critical recall likewise over `critical_concepts` (cases with ≥ 1 critical id).
- forbidden violation: any bundle record whose concepts intersect `forbidden_concepts`.
- preservation correct: each entry is a preserve constraint or intent target.
- bundle size and tokens reported per case; empty bundles on in-scope cases reported (not a failure by themselves — "no guidance" is allowed when nothing specific fits, but the human review decides whether it should have abstained).

## Human quality review (bundle-quality reviewer; record ids stripped; sees prompt + three-layer guidance text)

Question: *would a competent engineer, following this guidance, materially improve the interface for this request without being distracted or misled?* Verdicts: GOOD (materially helps, nothing misleading), PARTIAL (helps but a real gap or a distracting record), BAD (misleads, contradicts, generic filler dominates, or the one thing that mattered is missing), CORRECT_ABSTAIN, WRONG_ABSTAIN. Every PARTIAL / BAD names one primary defect: `generic`, `wrong-screen`, `wrong-product`, `missing-critical`, `off-platform`, `contradicts-request`, `contradicts-codebase`, `overlong`, `should-abstain`, `should-not-abstain`.

## Set-level thresholds (11 primary)

| # | metric | threshold | v4 (historical, for scale) |
|---|---|---|---|
| 1 | scope correctness (all cases) | ≥ 0.93 | 0.935 |
| 2 | false platform assignment rate (resolved-wrong / claims) | ≤ 0.05 | 0.030 |
| 3 | platform correctness (resolved-correct / claims) | ≥ 0.75 | 0.528 |
| 4 | mode correctness (multi-mode credit) | ≥ 0.85 | 0.884 |
| 5 | critical concept recall (mean, cases with critical ids) | ≥ 0.80 | 0.630 |
| 6 | required concept recall (mean) | ≥ 0.62 | 0.535 |
| 7 | forbidden concept rate | ≤ 0.05 | 0.097 |
| 8 | human GOOD + PARTIAL (non-abstain cases) | ≥ 0.85 | 0.754 |
| 9 | human BAD | ≤ 0.15 | 0.246 |
| 10 | generic primary-defect rate (cases) | ≤ 0.12 | 0.226 |
| 11 | wrong-screen primary-defect rate (cases) | ≤ 0.08 | 0.203 |

Secondary (reported, not counted): resolution rate, unresolved rate, fundamental mode misses ≤ 0.10, empty bundle rate, mean bundle size, guidance markdown tokens mean ≤ 1100 / p95 ≤ 1500, wrong-product and missing-critical defect rates, stress-set breakdowns.

## Implemented project round (mandatory for stable-candidate; `research/phase6-projects`, frozen c3)

≥ 30 tasks over ≥ 15 codebases (web ≥ 8, mobile ≥ 6, desktop ≥ 5, TV ≥ 4, kiosk ≥ 3; ≥ 20 existing-UI changes; ≥ half without a mode word), each fully implemented, rendered, reviewed and fixed. Pass ⇔ all of: platform resolved-wrong = 0 with project context; scope correct on every task; mode correct or acceptable on ≥ 0.85; critical recall (pre-registered) ≥ 0.80 mean; forbidden-concept deliveries ≤ 2 tasks; `skill_effect` HURT ≤ 3 tasks and HELPED ≥ 0.5 of tasks; `generic` + `wrong-screen` + `wrong-product` off-target records ≤ 0.20 of reviewed records; unjustified direction slots ≤ 2 across the round; no severe systemic defect (a defect class repeated on ≥ 3 tasks that a reviewer would call harmful).

## Stability policy (decided now; exactly one verdict in PHASE6-RESULTS.md)

- **experimental** — a deterministic gate fails, or a severe systemic real-project defect.
- **personal-production-ready** — deterministic gates pass and the project round shows the skill helps, but the stable-candidate conditions are not all met.
- **stable-candidate** — all of: every deterministic gate passes (development + regression + validator + activation proxy); the implemented project round passes as defined above; v5 meets ≥ 9 of the 11 primary thresholds **including all of the mandatory ones**: #1 scope, #2 false platform, #5 critical recall, #7 forbidden, #8 human GOOD+PARTIAL, #9 human BAD.
- **stable** — not reachable in Phase 6 (needs real Claude activation validation, a second independent blind qualification and continued real-project use).

If v5 or the project round fails, the verdict stays personal-production-ready and phase-chasing stops; the failures are listed, not explained away. Real-model activation is SKIPPED if the CLI is unauthenticated and stated as a limitation.

## Independence

Three roles in separate sessions: generator (prompts only), expectation reviewer (expectations from the ontology), bundle-quality reviewer (prompt + guidance text, ids stripped). None sees records, lexicon, development cases, or code. Model families are recorded in `MANIFEST.json`; when different families are not available the shared-family limitation is stated. The set is run **once** on the frozen build recorded in `research/runs/phase6-freeze.json`; no code change between the freeze and the run.
