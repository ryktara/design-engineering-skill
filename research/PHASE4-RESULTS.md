# Phase 4 results — "turn design-engineering into a stable candidate" (2026-09-09)

Eval case counts on the frozen build (validated by `validate_skill.py`):

| group | count |
|---|---|
| development | 269 cases |
| regression | 40 cases |
| heldout (v1, historical, non-blind) | 145 cases |
| heldout-v2 (historical, non-blind since Phase 3 analysis) | 212 cases |
| heldout-v3 (blind, generator / expectation reviewer / bundle-quality reviewers separated) | 311 cases |
| activation (frozen) | 180 cases |

Machine-readable sources: `research/runs/phase4-final-release-check.json` (gates, v1, v2, v3 with thresholds, projects, activation), `research/runs/phase4-freeze.json` (hashes: de_core `4ecbca0ecca2e676…`, de_semantic `2bbee02f0959f68e…`, inspect_project `6e77763f547f2301…`, lexicon `55341c3c720e75fe…`; 237 records, 109 concepts, 16 concerns), `research/runs/heldout-v3-run1-blind.json`, `research/runs/heldout-v3-human-review.json`, `research/benchmark-results.json`, `research/runs/phase4-output-size.json`, `research/runs/phase4-projects-aggregate.json`. Baseline: `research/PHASE4-BASELINE.md`.

## Verdict

**personal-production-ready** — one pre-registered threshold short of stable-candidate. Six of nine primary blind thresholds were met (scope, required-concern coverage, forbidden-concept rate, empty rate, human GOOD+PARTIAL, human BAD); platform correctness, mode correctness and required-concept recall were missed. The label policy written before the run (`evals/heldout-v3/THRESHOLDS.md`) requires seven of nine for stable-candidate. No threshold was changed after the run.

## Deterministic gates

| gate | result |
|---|---|
| validator | OK (237 records, 109 concept ids, relations acyclic, no orphan concepts) |
| development + regression | 309 / 309 |
| activation proxy (frozen 180) | precision 0.987 · recall 1.000 · FPR 0.014 · FNR 0.000 (unchanged from Phase 3 baseline except recall 0.987 → 1.000) |
| performance | load 6 ms · search 228 ms cold index · direction 63 ms; benchmark cold median 414 ms vs upstream 200 ms, warm search 43 ms / guidance 54 ms |
| real activation | SKIPPED (CLI not authenticated for non-interactive use) |

## Blind held-out v3 (311 cases; 281 in scope, 30 out of scope) — run once

| pre-registered threshold | measured | met |
|---|---|---|
| platform correctness ≥ 0.92 | 223 / 281 = **0.79** | no |
| mode correctness ≥ 0.80 | 181 / 281 = **0.64** | no |
| scope / abstention ≥ 0.90 | 287 / 311 = **0.92** (25 / 30 abstains right; 19 in-scope prompts abstained) | yes |
| required-concern coverage ≥ 0.90 | **0.91** | yes |
| required concept recall ≥ 0.60 | **0.50** (182 / 281 at ≥ ½; 40 at zero) | no |
| forbidden-concept rate ≤ 0.08 | 8 / 281 = **0.03** | yes |
| empty bundle rate ≤ 0.02 | **0.00** | yes |
| human GOOD + PARTIAL ≥ 0.80 | (118 + 99) / 267 = **0.81** | yes |
| human BAD ≤ 0.20 | 50 / 267 = **0.19** | yes |
| acceptable (secondary) ≥ 0.50 | 125 / 311 = 0.40 | no |

Human review (three blind Claude Opus sessions, prompt + guidance text only, ids stripped): GOOD 118 · PARTIAL 99 · BAD 50 · ABSTAIN-CORRECT 25 · ABSTAIN-WRONG 19. Agreement with the machine score: of 125 machine-acceptable cases 96 were GOOD/PARTIAL and 4 BAD; of the machine-failed in-scope cases 121 were still GOOD/PARTIAL and 46 BAD — the machine criteria are stricter than the human judgement, mostly because of platform/mode misses that did not hurt the guidance.

Class-level reading (aggregates only; individual cases were not opened):
- Platform misses (58): in 43 the tool detected **no** platform where the author expected one (a recall gap in platform vocabulary), not over-inference; 19 cases failed on platform alone.
- Mode misses (100): 74 were `create` where the author expected refactor/polish/audit — existing-UI wording the intent cues do not yet cover; the model rarely mis-assigns problem statements (10 polish/audit swaps).
- Recall: mean 0.50; 34 cases at 1.0, 40 at 0. Weakest categories by acceptability: adversarial 4/32, polish 1/12, web 2/12, design-system 4/21; strongest: tv 14/22, saas 15/27, healthcare 4/5.
- Statuses: CONFIDENT 90 · PARTIAL 162 · AMBIGUOUS 10 · ABSTAIN 44 — the tool itself marks most bundles PARTIAL, which matches the recall result.
- Generation: Opus (blind, ontology only); expectation review: Sonnet (blind; 312 → 311, 4 platform edits, 1 preservation edit, 1 near-duplicate removed; noted a mild desktop over-inference bias in the draft); bundle-quality review: Opus ×3. Same model family throughout; documented as a limitation.

## Historical sets (non-blind; run once after the freeze)

| metric | v1 Phase 3 final | v1 Phase 4 | v2 Phase 3 (blind then) | v2 Phase 4 |
|---|---|---|---|---|
| acceptable | 37 / 145 | 38 / 145 | 18 / 212 | 30 / 212 |
| mean concept recall (phrase) | 0.336 | 0.359 | 0.206 | 0.234 |
| mode correct | 113 | 119 | 129 (61 %) | 139 (66 %) |
| platform correct | 132 | 132 | 201 | 201 |
| abstain correct | 6 / 6 | 5 / 6 | 14 / 20 | 17 / 20 |
| concern coverage | 0.961 | 0.917 | 0.808 | 0.808 |
| forbidden violations | — | — | 7 | 4 |
| false abstentions (new) | 0 | 3 | 0 | 3 |

## Benchmark v2 (18 author-written queries; regression coverage only)

relevant: upstream 0.200 · search k=5 0.909 · guidance bundle 0.928; off-target: 0.189 · 0.148 · 0.106; empty 3 · 0 · 0; cold 200 ms vs 414 ms (7 reps, idle machine; an earlier run under agent load measured 1128 vs 1462 ms); warm 43 / 54 ms; bundle 6.56 records, concern coverage 0.966, 4.5 kB.

## Output size (204 queries, tokens ≈ chars / 4)

guidance markdown mean 1031 (median 1016, p95 1302) · guidance JSON mean 2797 · direction markdown mean 2236 (p95 2593) · bundle median 6 records, mean 957 tokens, coverage 5.4 required concepts per 1k tokens, mean purity 0.85. Within the 800–1300 target; direction unchanged despite the added context table.

## Real projects (15 tasks, 9 applications; `research/PHASE4-PROJECTS.md`)

Preservation held on 15 / 15 tasks (navigation, theme, typography, component reuse; 0 unjustified structural changes). Defects first → final: visual 11 → 6, interaction 3 → 0, accessibility 2 → 0, platform 4 → 2, existing-system mismatch 3 → 2, implementation bug 7 → 0. Design-context detection judged correct: navigation 7 yes / 8 partial, theme 13 / 1 / 1, typography 1 / 5 / 9, surfaces 5 / 2 / 8, spacing 6 / 3 / 6 (parsers fixed after the round). Nine class fixes with regressions; three records added with sources.

## What changed (summary; `NEW-ARCHITECTURE.md` §13, `MAINTENANCE.md`)

Scope model with out-of-scope reasons; task-intent model (existing / problem / facet / diagnose / redesign / preserve) with mode evidence and change budget; reference-clause stripping; concept ontology 57 → 109 ids with relations and `derive_expected_concepts`; guidance-bundle/v2 (concept-aware utility, token cost, purity, category contamination, specialist rules); inspector `design_context`; direction preservation with compatibility table and low-budget slot policy; 5 records added (12 → 237 total), ~90 records relabelled; development suites scope/mode/context (+ real-project fixtures); 8 + 9 regressions; held-out v3 infrastructure with pre-registered thresholds; release check flags.

## Honest limits

- Platform recall on blind wording is the largest gap (0.79); the lexicon-based detector misses device idioms the author considered obvious. Mode: modifications of existing UI without a problem or change cue still read as `create`.
- Concept recall 0.50: half of what an independent author expects is surfaced; 40 bundles surfaced none of it.
- Scope false negatives: 19 in-scope prompts abstained (6.8 %); 5 out-of-scope prompts received (BAD) guidance.
- Same model family for generation, expectation review and bundle-quality review.
- Real activation still unverified (CLI not authenticated). Native TV/mobile code reviewed statically. Cold latency is ~2× upstream.
- Typography/surface/spacing context detection is still weak on native stacks.
