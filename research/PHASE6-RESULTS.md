# Phase 6 — Final stability hardening: results

Recorded 2026-09-16. Candidate under judgement: **c4**, sha256 `32e67640c9b8ef1d519ef9695016fb396116b92412e63c324da090aecf1df385` (`research/runs/phase6-freeze.json`). Development cases 885 by the validator's count (884 run as cases; benchmark.json is excluded), regression cases 54, held-out v1 145 cases, held-out-v2 212 cases, held-out-v3 311 cases, held-out-v4 434 cases, held-out-v5 525 cases, activation 180 cases. Records 248, concepts 114, alias groups 75.

## A. Verdict

**PERSONAL-PRODUCTION-READY.** Not stable-candidate. The pre-registered policy (`evals/heldout-v5/THRESHOLDS.md`, sha256 `3d0452ab…00f3`, written before v5 generation and never edited) requires the implemented project round to pass and v5 to meet ≥ 9 of 11 thresholds including six mandatory ones. The project round failed 4 of 9 criteria on the implemented build (c3) and still 4 of 9 after the routed fixes (c4, guidance-only rescore). v5 met 5 of 11 thresholds; three mandatory thresholds failed (scope as scored, critical recall, human quality). Phase-chasing stops here as the mission directed; the remaining defects are listed in §Z, not explained away.

## B. Baseline (Phase 5 c2, recorded before any change)

`research/PHASE6-BASELINE.md`: v4 platform UNKNOWN 44.2 % · false 3.0 % · forbidden 9.7 % · critical recall 0.630 · human GOOD+PARTIAL 0.754 / BAD 0.246 · defects generic 98 · wrong-screen 88 · missing-critical 83. Development 575 / 575, regression 40 / 40, idle gates load 8 / search 224 / direction 158 ms, guidance markdown mean 1045 / p95 1370 tokens, bundle size mean 6.3.

## C. What changed (surgical scope)

No retrieval architecture, no new ontology, no new capability, one new record (`mobile-orientation-size-classes`). Changed layers only: expected-concept criticality, bundle selection (guidance-bundle/v3), contamination / compatibility, situational platform evidence, token traps, the inspector's TV-package and render-directory handling, and the direction's freedom rule. SKILL.md unchanged. `research/NEW-ARCHITECTURE.md` §15 and `docs/MAINTENANCE.md` describe the mechanics.

## D. Workstream A — bundle purity

`task_evidence` flags and `coverage_quality` (DIRECT / SPECIFIC / GENERIC / INCIDENTAL) on every candidate; core records need positive task evidence; GENERIC admission requires the record's primary concept (or a named concept, wording, a problem statement, high risk, a build task or a platform baseline); coverage is diagnostic (`not_surfaced`), no soft minimum, stop condition at marginal utility ≤ 0.5, `marginal` exposed under `--explain`. Effect: mean bundle size 6.3 → 3.7 on the development queries (2.8 on v5), off-target records in the project round 37 → 14 after re-review, wrong-screen 22 → 9 — and 78 empty bundles on v5 (§V).

## E. Workstream B — wrong-screen / wrong-product cores

Screen families, job affinity, product-mismatch waiver limited to focused explicit carriers, platform-only records penalised without platform evidence, `RECORD_WORD_GATES` for narrow-subject records (mini-player, drag-drop, plan comparison, skip link, keypad, geo chart, master-detail, pagination, entry grid, toast), token traps (Tab key, landscape, overlays, remote office, terminal, guide, poster print, payment card / freezing a card, completion screen, mouse negated, compare files, spacing grid). v5 wrong-screen primary-defect rate 0.072 (threshold ≤ 0.08, met; v4 0.203). The wrong-screen stress set still delivers a forbidden concept on 15 of 62 cases (§T).

## F. Workstream C — critical concepts first

`priority` 0–3 and `critical` on required concepts; critical → core → required → specialist → recommended; conditional criticality (platform generics on non-interactive tasks, narrow-task demotion, product / repository baselines at priority 2, accessibility review on touch-only platforms without keyboard demands); `concept_trace` carries `critical` and `carrier_quality`; markdown output in three layers. Critical recall: development concept diagnostics 144 / 144; project round 0.635 (c3) → 0.682 (c4); v5 0.448 (v4 historical 0.630 on c2, 0.569 on c4). The demand layer, not selection, is the bottleneck: 120 of 227 PARTIAL/BAD v5 verdicts name `missing-critical`.

## G. Workstream D — situational platform inference

Evidence families with compound WEAK→STRONG resolution, platform traps, ~160 new WEAK phrases; `evals/platform_confusion.py`. Development 237 / 237 cases: resolved-correct 186, unresolved 51, resolved-wrong 0, resolution rate 0.964. v5: claims 355, resolved-correct 274 (0.772), unresolved 72 (0.203), resolved-wrong 9 (0.025); 8 of 9 `expect_unknown` cases correctly unresolved. v4 historical on c4: correct 231 (c2: 208), UNKNOWN 151 (174), wrong 12 (12).

## H. Development cases written before the code

`platform-situational.json` 150 (76 → 150 passing), `purity.json` 159 (71 → 159), plus dated amendments to eleven existing cases (coverage is diagnostic; three situational cases corrected). All amendments carry dated notes; no case was edited to pass silently. Final: development 884 / 885 (the failing check is the validator's doc-count, §Y), regression 54 / 54, activation proxy precision 1.0 / recall 1.0, mode confusion 145 primary / 0 incorrect, concept diagnostics recall 1.0.

## I. Generic process records vs SKILL.md

`impl-reuse-before-new`, `impl-safe-modification`, `verify-render-and-inspect` enter 2 of 281 development bundles; in the project round `impl-reuse-before-new` was needed on 4 tasks and judged generic on 4. Kept; `process.reuse_first` stays a priority-1 demand on existing repositories (regression case `reg-polish-in-existing-reuses-primitives`).

## J. Three-layer output and bundle size

CORE / CRITICAL GUARDRAILS / OPTIONAL NOTES (empty layer omitted). Development + purity + v1 queries (273): guidance markdown mean 702 / median 628 / p95 1305 tokens (Phase 5: 1045 / 1055 / 1370); bundle size mean 3.7 / p95 8; bundle tokens mean 585 / p95 1273; 12 empty bundles of 273. Context cost targets (mean ≤ 1100, p95 ≤ 1500) met.

## K. Direction on existing systems

Only a greenfield build (artifact new **and** budget greenfield) picks layout / cards / cta / metadata / imagery freely. Unjustified direction slots in the round: 22 (c3) → 12 (c4); still above the ≤ 2 bar. The remaining cases are `cta` marked `new` when the sentence contains "button", `cards → card-none` on Compose screens whose card surface the inspector does not read, and TV `cards` portrait vs the codebase's landscape.

## L. Regression cases added

Nine guidance cases and five mode cases (`evals/regression/guidance.json`, `evals/regression/mode.json`) plus one context case (`c6-tizen-webos-tv-web-app`), each with a dated note naming the task and the earliest wrong layer.

## M. Candidate history and disclosure

c3 frozen (`phase6-freeze-c3.json`, `ea8eed72…d9947`) for the implemented round; c4 (`32e67640…f385`) after routed fixes; guidance-only rescore of c4 on the same tasks. **Disclosure:** during Phase 6 a patch script truncated `scripts/de_core.py` to zero bytes; it was rebuilt from the Phase 4 backup plus every recorded Phase 5 / 6 patch and re-validated on all suites, but the Phase 5 c2 hash `50966e8e…` is not reproducible byte-for-byte. Scripts are now backed up to the session scratchpad before every patch. Implementer agents ran on Claude Opus after the first batch hit a spend limit on the default model; their step 0–4 outputs were kept and pre-registered expectations were never changed.

## N. Implemented project round — protocol

`research/phase6-projects/PROTOCOL.md` (+ addendum), `TASKS.md`: 32 tasks, 16 codebases (12 existing + 4 new fixtures), web 10 · mobile 7 · desktop 6 · TV 5 · kiosk 4; 27 existing-UI changes; 24 sentences without a mode word; pre-registered critical / expected / forbidden concepts per task; implement → render → inspect → fix; per-record review categories; HELPED / NEUTRAL / HURT; unjustified direction slots; process-record check. Build hash equal at start and end on all 32 tasks.

## O. Implemented project round — results (c3)

Platform 30 yes / 2 wrong · scope 32 / 32 · mode 21 yes / 9 acceptable / 2 no · critical recall 0.635 · concept recall 0.434 · forbidden deliveries 0 · skill effect helped 22 / neutral 10 / hurt 0 · records reviewed 143: relevant 57 / partial 49 / off-target 37 (generic 59, wrong-screen 22, missing-critical 21 bundle-level, off-platform 2, contradicts-codebase 2, wrong-product 1) · unjustified direction slots 22 · first-render defects 68 → final 7 · guidance tokens mean 681 · process records needed on 4 tasks. Pass criteria met 5 / 9 → **round FAIL**. Full table: `research/PHASE6-PROJECTS.md`.

## P. c4 rescore of the same round (guidance-only)

Platform 31 / 1 (the one "wrong" is the mechanical scorer filtering `tablet`) · mode 32 / 32 acceptable-or-better · critical recall 0.682 · forbidden 1 task · records 124: relevant 59 / partial 51 / off-target 14 (generic 55, wrong-screen 9, contradicts-codebase 1) · unjustified direction slots 12 · independent re-review: better 17 / same 10 / worse 5 (bundles that shrank past the record the implementer had used). Criteria met 5 / 9 → **still FAIL** (critical recall, off-target rate, direction slots, platform by the scorer).

## Q. Routing of every project defect (earliest wrong layer)

expected-concepts 76 concept misses · bundle-selection 60 · project-context 32 · requirements 17 · direction 16 · candidate-compatibility 10 · criticality 8 · mode 3 · candidate-retrieval 2 · platform-evidence 2 · knowledge gap 2 · implementation 2 · concerns 1. c4 addressed criticality, compatibility, mode, platform-evidence, the inspector's TV / render handling and the direction freedom rule; it reached the expected-concepts layer only through aliases for demonstrated phrasings.

## R. Held-out v5 — construction and independence

525 cases (`evals/heldout-v5/cases.json`, sha256 in `MANIFEST.json`): create 70 · refactor-fix 100 · polish 60 · audit-review 50 · accessibility 45 · responsive 40 · tv-media 35 · desktop-native 30 · mobile-native 30 · kiosk-public 25 · adversarial 40; stress wrong-screen 62, generic-guardrail 66; scope in-scope 464 / partial 24 / abstain 37; platform claims 165 by the reviewer's `required` field (355 including `acceptable_inferred`); 488 cases with 1–3 critical concepts. Roles: generator Claude Sonnet (4 sessions, prompts only, `GENERATOR-BRIEF.md`); expectation reviewer Claude Opus (4 sessions, `REVIEWER-BRIEF.md` + `ONTOLOGY.md` only); bundle-quality reviewer Claude Sonnet (6 sessions, `QUALITY-REVIEW-BRIEF.md`, ids stripped). None saw records, lexicon, cases or code. All three roles are Anthropic Claude models: the shared-vendor limitation is stated. The set was run **once**, on frozen c4, after `phase6-freeze.json`; no code change between the freeze and this document.

## S. Pre-registered thresholds (unchanged)

Scope ≥ 0.93 · false platform ≤ 0.05 · platform correct ≥ 0.75 · mode ≥ 0.85 · critical recall ≥ 0.80 · required recall ≥ 0.62 · forbidden ≤ 0.05 · human GOOD+PARTIAL ≥ 0.85 · human BAD ≤ 0.15 · generic defect ≤ 0.12 · wrong-screen defect ≤ 0.08. Stable-candidate: ≥ 9 of 11 including scope, false platform, critical recall, forbidden, human GOOD+PARTIAL, human BAD; plus the project round.

## T. Held-out v5 — deterministic results (run once, `research/runs/heldout-v5-run1-c4.json`)

| # | metric | value | threshold | met |
|---|---|---|---|---|
| 1 | scope correctness | 440 / 525 = **0.838** | ≥ 0.93 | **no** |
| 2 | false platform (resolved-wrong / claims) | 9 / 355 = 0.025 | ≤ 0.05 | yes |
| 3 | platform correctness | 274 / 355 = 0.772 | ≥ 0.75 | yes |
| 4 | mode correctness | 447 / 488 = 0.916 | ≥ 0.85 | yes |
| 5 | critical recall (488 cases) | **0.448** | ≥ 0.80 | **no** |
| 6 | required concept recall | **0.346** | ≥ 0.62 | **no** |
| 7 | forbidden concept rate | 24 / 488 = 0.049 | ≤ 0.05 | yes |

Secondary: resolution rate 0.797 · unresolved 0.203 · fundamental mode misses 14 (0.029) · mean bundle size 2.77 · mean bundle tokens 424 · quality totals DIRECT 312 / SPECIFIC 816 / GENERIC 223 / INCIDENTAL 0 · abstain cases correct 30 / 37 · acceptable cases 73 / 525. Per-category acceptable: adversarial 30 / 40, create 16 / 70, polish 16 / 60, audit-review 10 / 50, refactor-fix 1 / 100, all others 0. Critical recall by category: tv-media 0.70, accessibility 0.62, mobile-native 0.60, refactor-fix 0.45, kiosk 0.44, responsive 0.41, create 0.39, desktop 0.35, polish 0.35, audit-review 0.33. Stress sets: wrong-screen 62 cases → forbidden delivered 15, empty 11; generic-guardrail 66 → forbidden 8, empty 11.

## U. Held-out v5 — human quality review (`research/runs/heldout-v5-human-review-full.json`)

| # | metric | value | threshold | met |
|---|---|---|---|---|
| 8 | GOOD + PARTIAL (of GOOD/PARTIAL/BAD) | (190 + 111) / 417 = **0.722** | ≥ 0.85 | **no** |
| 9 | BAD | 116 / 417 = **0.278** | ≤ 0.15 | **no** |
| 10 | generic primary defect | 57 / 417 = **0.137** | ≤ 0.12 | **no** |
| 11 | wrong-screen primary defect | 30 / 417 = 0.072 | ≤ 0.08 | yes |

Also: CORRECT_ABSTAIN 45, **WRONG_ABSTAIN 63**; defects missing-critical 120, should-not-abstain 35, overlong 7, should-abstain 6, wrong-product 4, contradicts-request 2, off-platform 1. By category (GOOD/PARTIAL/BAD/wrong-abstain): tv-media 20/9/5/1, mobile-native 14/6/4/3, accessibility 22/12/7/4, kiosk 10/10/2/2, responsive 16/14/7/3, desktop 12/8/4/6, audit-review 26/6/2/16, create 21/15/24/10, refactor-fix 32/17/30/11, polish 17/13/24/6, adversarial 0/1/7/1 (+31 correct abstain). Compared with v4 (c2): GOOD+PARTIAL 0.754 → 0.722, BAD 0.246 → 0.278, generic 0.226 → 0.137, wrong-screen 0.203 → 0.072, missing-critical 0.191 → 0.288.

**Thresholds met 5 / 11; mandatory met: no (scope, critical recall, human GOOD+PARTIAL, human BAD failed).**

## V. What v5 shows (defect analysis, aggregate)

1. **Empty bundles counted as abstention.** 78 in-scope prompts (15 %) returned no record; the guidance status becomes `ABSTAIN` when the bundle is empty, so the pre-registered scorer counts them as scope failures (hence 0.838) and the reviewers marked 63 of them WRONG_ABSTAIN. Read literally, scope classification was right on 518 / 525 (0.987) — but that is a diagnostic reading, not the pre-registered metric, and the threshold stands as failed. Empty bundles concentrate on plain build requests without a screen noun ("start with the list view", "a fresh screen to enter shipment manifests"), on audit / review sentences (16) and on refactor-fix (21): precision-first selection with no positive evidence yields nothing, and "no guidance" was the wrong answer for most of them.
2. **Missing critical concepts dominate quality.** 120 of 227 PARTIAL/BAD verdicts. The concepts the reviewers expected are in the ontology and mostly have carriers; they were never demanded (expected-concepts layer). Aliases scale linearly with phrasings and v5 phrasings were new by design.
3. **Generic filler fell but did not disappear** (0.226 → 0.137): platform baselines (TV typography / safe area / d-pad axes, web keyboard / hover) and states records on tasks that did not need them.
4. **Wrong-screen fell below threshold** (0.203 → 0.072) — the one Phase 6 target class that cleared its bar — but the stress set still delivers forbidden concepts on 15 / 62 (Tab key, card, overlay, guide senses that traps do not cover).
5. Platform: false assignment 0.025 and correctness 0.772 meet the bars; resolution rate 0.797; 9 wrong assignments (listed in the run file).

## W. Historical held-out reruns on c4 (non-blind, trend only)

| set | passed | key numbers (c2 → c4) |
|---|---|---|
| v1 (145) | 27 / 145 | platform 122 → 122 · mode 106 → 106 · recall 0.369 → 0.297 · empty 7 → 11 |
| v2 (212) | 23 / 212 | platform 196 → 202 · mode 137 → 137 · recall 0.232 → 0.192 · empty 17 → 26 |
| v3 (311) | 125 / 311 | scope 298 → 291 · platform 221 → 222 · mode 228 → 229 · recall 0.533 → 0.432 · forbidden 6 → 3 |
| v4 (434) | 94 / 434 | platform correct 208 → 231 · UNKNOWN 174 → 151 · wrong 12 → 12 · mode 366 → 371 · recall 0.535 → 0.440 · critical 0.630 → 0.569 · forbidden 40 → 14 · bundle size ≈ 6.3 → 3.25 |

Precision up (forbidden, wrong platform, UNKNOWN), recall down on every historical set. Historical sets were run once each and were never used for tuning.

## X. Benchmark (regression only, idle, 7 reps)

Idle rerun on c4, 7 repetitions, upstream re-cloned (`research/benchmark-results.json`, rendered `BENCHMARK-RESULTS.md`, 18 queries). Relevant-term coverage upstream 0.200 · ours 0.922 (Phase 5: 0.915 search / 0.927 bundle); off-target 0.189 · ours 0.148 (Phase 5: 0.106–0.111 — worse: smaller bundles lose fewer off-target terms than they lose relevant filler, and two off-target terms now come from the remaining platform baselines); empty results 3 · 0; cold median 139 ms upstream vs 377 ms ours (p95 244 / 473), warm median 144 ms; mean facet coverage 0.764 (Phase 5 concern coverage 0.992 — expected under coverage-as-diagnostic). Regression coverage only; the benchmark queries are author-written and were never used for tuning.

## Y. Output size, performance, validator

Output size §J. Performance idle: load 11 ms · search 303 ms · direction 314 ms (Phase 5 baseline 8 / 224 / 158; slower because every candidate now carries task-evidence and coverage-quality computation; still inside the sanity gate, and the CLI cold path in the benchmark stayed at 377 ms median). Validator: 2 errors — `check_doc_counts` is bound to `PHASE5-RESULTS.md` in a hashed script and compares its 575 / 40 figures with the 885 development and 54 regression cases now on disk; changing the validator would change the frozen hash after the v5 run, so the fix is deferred and the release check reports `validator: False` and `development+regression: 938 / 939` for this reason alone. Activation proxy precision 1.0 / recall 1.0; real activation **SKIPPED** (CLI unauthenticated).

## Z. Acceptance gates and what remains

Gates: deterministic development + regression green except the doc-count check (yes, with the disclosure above) · platform confusion resolved-wrong 0 on development (yes) · project round pass (**no**) · v5 ≥ 9 / 11 with mandatory (**no**, 5 / 11) · context cost mean ≤ 1100 / p95 ≤ 1500 (yes) · no goalposts moved, no threshold lowered, no case edited to pass without a dated note (yes).

Open failure classes, in routing order: **expected concepts** (the demand layer does not generalise to unseen phrasings; aliases are the wrong tool at this scale), **bundle selection** (precision-first leaves in-scope build requests without positive evidence empty — a floor of one relevant record for build tasks with a known screen or product would have answered most of the 78), **criticality** (platform baselines still surface as filler), **direction** (`cta` / `cards` on existing systems), **project context** (token and surface detection on Compose, SwiftUI and CSS custom-property projects). None of these is fixable within the "surgical" scope Phase 6 allowed; the honest state of the architecture is a precise but under-recalling retriever with a lexical demand layer.

## AA. Decision

PERSONAL-PRODUCTION-READY, unchanged from Phase 5. Phase-chasing stops. The skill helped on 22 of 32 implemented tasks and hurt none; it is safe and useful for its author, and it is not a stable candidate by its own pre-registered standard.
