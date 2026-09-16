# Phase 2 results (release candidate, 2026-09-08)

All numbers below come from files in this workspace: `evals/run_evals.py` output, `research/runs/*.json`, `research/benchmark-results.json` (method v2). Baseline: `research/PHASE2-BASELINE.md`.

## Evaluation groups

| Group | Files | Count |
|---|---|---|
| development (tuning allowed) | `evals/development/*.json` | 142 cases |
| regression (real defects, never removed) | `evals/regression/*.json` | 15 cases |
| heldout (frozen, independent, not tuned against) | `evals/heldout/cases.json` | 145 cases |
| activation (frozen, independent) | `evals/activation/cases.json` | 180 cases |

## Gate results

| Gate | Baseline | Release |
|---|---|---|
| validate_skill | 0 errors | 0 errors, 0 warnings (now also checks manifests, hashes, requirements schema, facet mapping, benchmark drift, doc counts) |
| development + regression evals | 108/109 (one suite set) | 157/157 |
| `winui-erp-grid` (original known failure) | fail (rank 7) | pass; `desktop-keyboard-first` enters via the unmet `interaction` facet, replacing a redundant second layout record |
| activation proxy on the 180-case set, blind run 1 | not measured | precision 0.849, recall 0.961, FPR 0.176, FNR 0.039 |
| activation proxy after lexicon fixes derived from run 1 (not blind) | — | precision 0.987, recall 0.987, FPR 0.014, FNR 0.013 (TP 75 FP 1 TN 73 FN 1) |
| real-model activation | SKIPPED | SKIPPED — `claude -p` is not authenticated for non-interactive use in this environment; the probe aborts instead of scoring |
| benchmark vs upstream (18 queries, method v2) | method v1, mixed timing | relevant 0.200 vs 0.879; off-target 0.189 vs 0.134; empty 3 vs 0; cold median 238 ms vs 332 ms; ours warm median 28 ms |
| performance sanity | — | load 53 ms, search ≈30 ms warm, direction ≈65 ms, cold CLI ≈330 ms |

## Held-out results (frozen set, two runs, both archived)

Run 1 used literal substring matching for concept phrases and is archived as `runs/heldout-run1-literal-matching.json`: acceptable 6/145, mean concept recall 0.066. Literal matching scored near zero even for obviously right answers ("focus restoration" vs "focus is restored"), so the metric definition was changed once to token-level matching (all content tokens of the phrase present in the returned text) and frozen. One defect found in run 1 ("site" not recognised as web) was fixed through a regression case. Run 2 is the release measurement (`runs/heldout-run2-release-token-matching.json`):

| Held-out metric (n = 145) | Result |
|---|---|
| acceptable (classification correct ∧ ≥⅓ concepts ∧ ≤⅓ off-target ∧ non-empty) | 10 / 145 |
| platform recall (all expected platforms detected) | 123 / 145 |
| platform precision (no unexpected platform) | 137 / 145 |
| mode correct (an expected mode within top-2) | 98 / 145 |
| input inference correct | 130 / 145 |
| negative constraints correct | 138 / 145 |
| MISSING flagged as expected | 112 / 145 |
| mean concept recall (token match) | 0.184 |
| cases with concept recall ≥ ½ | 15 / 145 |
| mean off-target rate / cases within ⅓ | 0.178 / 131 |
| required-facet coverage complete | 72 / 145 |
| empty results | 1 |
| status distribution | CONFIDENT 96 · PARTIAL 33 · AMBIGUOUS 15 · ABSTAIN 1 |
| abstain cases handled (skip/abstain/ambiguous) | 6 / 6 |

Reading: the requirements layer generalises (platforms, inputs, negatives, abstention); the *guidance* layer does not yet: retrieved records rarely contain the independent reviewer's expected concepts. Decomposition (`research/KNOWLEDGE-GAPS.md`): 478 misses are records that exist but were not in the top 5 (ranking), 192 are concepts absent from the base (knowledge), 148 hits. The largest ranking cause is that universal interaction/accessibility rules are not required facets for create-mode requests on touch/web platforms. This is the first Phase 3 item; it was deliberately not tuned during Phase 2 because the held-out set was the measurement.

Confidence calibration on held-out: mean concept recall by label was high 0.227 (n 25), medium 0.171 (n 113), low 0.500 (n 1); by status CONFIDENT 0.176, PARTIAL 0.237, AMBIGUOUS 0.137. The labels reflect lexical/structural fit, not verified relevance, and must not be read as calibrated probabilities. They are kept for automation but documented as uncalibrated; recalibration needs a second independent set.

## Regressions found in Phase 2 (all have cases in `evals/regression/`)

1. Facet swap traded a strong component match (`comp-tv-rail`) for a zero-lexical navigation record; fixed with a swap ratio guard (incoming ≥ 0.75 × outgoing).
2. Required facets could exceed the slot budget (6 facets, k=5), forcing PARTIAL on terse TV queries; capped to k−1.
3. Stack words were platform evidence: "Compose" made mobile a KNOWN platform for an explicit TV request → AMBIGUOUS status. Stack words now only imply a platform when none is stated, and Compose on TV resolves to compose-tv as INFERRED.
4. "React" made web KNOWN; now INFERRED (React Native / TV exist).
5. "refresh the visual style" classified as create (polish vocabulary).
6. EPG not recognised as a list screen.
7. "site" not recognised as web (from held-out run 1).
8. Activation proxy false positives on framework-runtime prompts (7 regression prompts); platform inferred from a stack word no longer counts as UI evidence.

## What changed architecturally

- `DesignRequirements` (schema `design-requirements/v1`) built once by `build_requirements(query, project)`; `search` and `direction` consume it; `advise.py requirements` exposes it (compact by default, `--explain` shows reasons, `--full` dumps evidence maps). Evidence priority: explicit request > repository evidence > platform inference > default; conflicts recorded, request wins.
- Facet-aware result composition (`select_with_coverage`): required facets derived from requirements, relevance floor, swap ratio, per-category cap; metrics `facet_coverage`, `category_diversity`, `duplicate_pressure`, `swaps` in every search result.
- Negative and preservation constraints: rails, navigation-change, typography-change, dependencies, hover, remote/keyboard/touch-only; direction preserves navigation/typography slots on request and validates invariants (`validation.violations`).
- Statuses CONFIDENT / PARTIAL / AMBIGUOUS / ABSTAIN with CLI exit codes 0/3/4/5 (2 invalid input, 1 tool failure).
- Benchmark: canonical `research/benchmark-results.json` (method v2, cold/warm separated, median/p95, 5 reps), Markdown rendered from it, drift validated.
- `evals/release_check.py` runs validator, development+regression, activation proxy, performance sanity; `--heldout` and `--real-activation` optional.

## Recommendation

personal-production-ready, not stable. Standard used: every claim above is reproducible from committed files; the requirements layer passes an independent held-out set on classification; the guidance layer's held-out acceptability (10/145) is low and documented with a decomposed cause list; real-model activation remains unmeasured in this environment.
