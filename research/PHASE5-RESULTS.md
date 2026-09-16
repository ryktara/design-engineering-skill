# Phase 5 results — stable-candidate qualification (2026-09-09)

Build under test: candidate **c2**, sha256 `50966e8e6184f317…` (`research/runs/phase5-freeze.json`; candidate c1 `bf034323a2b68202…` in `phase5-freeze-c1.json`). Pre-registered thresholds and stability policy: `design-engineering/evals/heldout-v4/THRESHOLDS.md` (sha256 `e880c59e4c4b70ef…`, hashed before any Phase 5 change; not edited). Machine-readable sources: `research/runs/phase5-final-release-check.json`, `heldout-v4-run1-blind.json`, `heldout-v4-human-review.json`, `heldout-v4-quality-review-part1..4.json`, `phase5-c1-projects-release-check.json`, `phase5-c2-projects-rescore.json`, `phase5-c2-projects-review.json`, `heldout-v1/v2/v3-phase5-historical.json`, `phase5-output-size.json`, `research/benchmark-results.json`. Baseline: `research/PHASE5-BASELINE.md`.

## A. Verdict

**personal-production-ready** — not stable-candidate. Under the pre-registered policy the deterministic gates pass, the real-project round shows the skill helps more than it hurts on the frozen build, but the blind held-out v4 run met **3 of 10** primary thresholds and failed three of the five mandatory ones (forbidden-concept rate, human GOOD+PARTIAL, human BAD). No threshold was changed after the run; no v4 case was edited; the set was run once.

## B. Deterministic gates (frozen c2)

| gate | result |
|---|---|
| validator (`scripts/validate_skill.py`) | OK — 247 records, 114 concepts, 16 concerns, 60 alias groups; ontology/alias/intent/platform-evidence/manifest checks |
| development + regression suites | 615 / 615 (575 development, 40 regression) |
| activation proxy (frozen 180-case set) | precision 1.000 · recall 1.000 · FPR 0.000 · FNR 0.000 |
| real Claude activation | SKIPPED (CLI not authenticated for non-interactive use; stated as a limitation, as the policy allows) |
| mode confusion (`evals/mode_confusion.py`) | 145 mode cases: primary correct 145, incorrect 0, fundamental create-misses 0 |
| concept diagnostics (`evals/concept_diagnostics.py`) | development guidance cases: expected 144, hit 144; misses by layer none |
| performance sanity | idle rerun of the gates alone (`research/runs/phase5-final-gates-idle.json`): load 11 ms · search 307 ms (cold index) · direction 155 ms — OK (Phase 4: 7 / 246 / 65). The combined final run (`phase5-final-release-check.json`, all held-out sets + projects + activation probe in one process) recorded 21 / 762 / 459 ms and marked this gate not ok; that measurement was taken inside a long run and is superseded by the idle rerun, not by any change to the build |

## C. Freeze and build discipline

- c1 frozen before the real-project round (22 task folders record the same start and end hash `bf034323…`; `single_build: true` in the aggregate).
- Fixes routed from the round were preceded by 63 new development cases (`evals/development/p5r-scope|mode|guidance|context.json`, 16 of 63 passing on c1) and produced c2; c2 was re-scored on all 22 tasks (`evals/rescore_projects.py`). The concept ontology is unchanged between c1 and c2 (`ontology_unchanged_since_c1: true`), so the v4 set generated after the c1 freeze remains valid for c2.
- Held-out v4 was placed in `evals/heldout-v4/` after the c2 freeze (MANIFEST records the case-file hash `60f3f063…`, the build hash, the roles and models) and run exactly once; the build hash is unchanged after the run.

## D. Workstream A — platform semantic resolution

Typed, graded evidence (`PLATFORM_EVIDENCE`, `resolve_platform`): explicit / stack / form-factor / modality / OS / environment / repository / product × DIRECT / STRONG_INFERENCE / WEAK_INFERENCE; device-class precedence; negations; "media browser" is not a browser; "desktop web app" is web; React Native is not React web; WEAK alone gives UNKNOWN plus a MISSING confirm entry. Repository platforms confirm wording; "on phones" on a web project is a viewport. 87 development cases written before implementation (`platform-evidence.json`; five strength expectations corrected with dated notes before implementation review, three cases corrected to expect UNKNOWN because they had demanded a platform from WEAK evidence, contradicting the model's own rule). Blind v4 outcome: false assignment 12 / 394 claims (**3.0 %**, threshold ≤ 5 % met); correctness 208 / 394 (**52.8 %**, threshold ≥ 88 % missed) because 174 claims stayed UNKNOWN where the reviewers required a platform from situational cues (only 1 of those 174 prompts names the platform canonically).

## E. Workstream B — task/mode semantics

`task_intent` v2 (artifact_state, operations, problem_domain, change_scope, utterance, preserve), `derive_modes` by lead domain, change budget v2; explicit verbs highest priority; observations about a screen are existing UI; spec-shaped noun phrases are new; screen names such as "Add Habit sheet" are not verbs. 122 development cases (96 without explicit verbs) plus 10 round-derived cases. Blind v4: mode correctness (multi-mode credit) 366 / 414 (**88.4 %**, ≥ 75 % met); fundamental create-misses 15 (3.6 %, secondary ≤ 10 % met); artifact state 353 / 414 (85.3 %). Remaining misses cluster in the `create` category: 15 prompts describing a new screen with a present-tense observation resolved as audit + refactor, and 15 with existing artifacts resolved as create.

## F. Workstream C — expected-concept generalisation

Alias layer (60 alias groups, one concept per phrase, validated), normalisation, job / screen / environment / risk mappings, derivation rules, saturation cap 8 by priority phase, `concept_trace` in `--explain` (JSON and Markdown). Five concept ids added (media.track_selection, tv.time_navigation, interaction.selection_visible, data.comparison_structure, feedback.trust_signals); 114 total. Bundles stay at mean 895 tokens (v4) / 950 (development + v1). Blind v4: required concept recall **0.535** (≥ 0.58 missed; v3 historical 0.533 on the same build, 0.498 at baseline), critical recall **0.630** (≥ 0.80 missed), required concern coverage **0.794** (≥ 0.90 missed), forbidden-concept cases 40 / 414 (**9.7 %**, ≤ 5 % missed).

## G. Workstream D — native design-context extraction

Typography / surfaces / radius / spacing on SwiftUI, Compose, WinUI, WPF, Avalonia, Flutter and Svelte / Vue templates; monospace faces never define the UI family; README kiosk declarations; README environment hints; word-bounded product hints; precision fixtures with misleading identifiers (`ListView`, `NavigationView`, `isTVEnabled`, `darkText`, `MobileSettings`). Real projects (c1): navigation 21 yes / 1 partial, theme 17 / 5, typography 4 / 17 / 1 no, surfaces 8 / 9 / 5, spacing 12 / 6 / 4; c2 corrected WPF typography (system, not monospace), Avalonia typography (humanist) and radius, Tailwind-template surfaces (bordered-flat) and tabular numerals; radius and spacing on token-based themes remain partial.

## H. Development and regression cases

575 development cases (269 at baseline; +87 platform evidence, +122 task intent, +27 guidance, +5 context, +2 scope, +63 round-derived) and 40 regression cases, all passing on c2. Cases were written before the implementation they test. Amended cases carry dated notes: three platform-evidence cases (WEAK evidence must not demand a platform), two strength notes, seven round-derived cases (validation_errors must not be *required*, virtualization is a legitimate concept of the data-table record, the harmful outcome is a hardware-keyboard record not a concept id, the invite dialog is not stated, TV rail performance legitimately mentions lazy composition, an Avalonia theme with 4/6/12 insets can read as a 4-base, a scope guard sentence that accidentally contained a UI word).

## I. Real-project qualification round c1 (implemented; `research/PHASE5-PROJECTS.md`)

22 tasks over 12 codebases (web 8, TV/kiosk 5, desktop-native 4, mobile 5; native 13; existing-UI 18; new screen on an existing codebase 4; one intended PARTIAL scope; one audit), three codebases new in Phase 5 (SvelteKit clinic, Avalonia fleet desk, SwiftUI habits). Pre-registered expectations, real concept recall, BAD categories, earliest-wrong-layer routing, build hash per task.

| metric | c1 |
|---|---|
| platform correct | 19 / 22 (wrong 3: kiosk project read as web ×2, "on phones" overriding a web project) |
| scope kind correct | 19 / 22 (abstain on plain sentences ×2, missing partial split ×1) |
| mode correct (yes / acceptable / no) | 9 / 12 / 1 |
| mean concept recall / critical recall | 0.387 / 0.470 (full critical recall 5 / 22) |
| guidance records relevant / partial / off-target | 32 / 50 / 47; BAD: generic 36, missing-critical 16, contradicts-codebase 14, off-platform 6, wrong-mode 1, harmful 0 |
| skill effect (implementer) | helped 3 · neutral 16 · hurt 3 |
| preservation | navigation / theme / typography / component reuse 22 / 22 each; unjustified structural change 0 |
| render defects first → final | visual 18 → 3, interaction 2 → 0, accessibility 4 → 1, platform 1 → 0, existing-system-mismatch 1 → 1, implementation-bug 5 → 0; 30 iterations |
| misses by earliest layer | scope 3 · platform 3 · mode 4 · requirements 28 · concerns 3 · expected-concepts 21 · candidate-retrieval 5 · bundle-selection 21 · direction 20 · project-adaptation 12 |
| concept misses by layer | expected-concepts 61 · bundle-selection 23 · candidate-retrieval 4 · knowledge-gap 2 (plus 13 tasks tagged knowledge-gap for records that did not exist) |

Severe systemic defects found on c1: scope abstain on UI sentences without lexicon nouns (3 tasks), kiosk project resolved as web (2 tasks), direction "new" slots contradicting the codebase (20 tasks), README product leaks driving checkout / product-detail records onto a habit tracker and a clinic.

## J. Fixes routed to layers (c1 → c2)

scope (repository context; UX symptom and UI vocabulary; decisive technical phrases per domain; `re-render*` + `stutter` gives PARTIAL) · platform (README kiosk, repository confirms wording, phones-on-web viewport) · mode (proper-noun screen names, accessibility / content / interaction cues, layout defects to audit + refactor) · requirements (environment hints from README, soft-keyboard wording not read as a hardware keyboard, reference clauses such as "against our accessibility checklist" stripped before retrieval) · expected concepts (aliases and rules listed in `NEW-ARCHITECTURE.md` §14) · candidate retrieval / selection (contamination for media-only patterns, CTA patterns without action wording, visual patterns without wording evidence on an existing UI) · direction (unmentioned slots preserved under moderate budgets, repository focus preserved, density preserved, no false "no accessibility constraints" violation) · project adaptation (inspector detectors above) · knowledge (9 records added, 6 corrected). Everything else stayed frozen.

## K. Real-project re-scoring on c2

Same 22 tasks, same pre-registered expectations, skill steps re-run on c2 (implementation not re-run): platform correct **22 / 22**, scope **22 / 22**, mode yes 14 / acceptable 8 / no 0, artifact state 21 / 22, mean concept recall **0.678** (from 0.387), critical recall **0.841** (from 0.470), full critical recall 14 / 22 (from 5), forbidden-concept tasks 5 (from 9), empty bundles 0 (from 2). Independent reviewers (claude opus) judged the c2 bundles record by record: relevant / partial / off-target 56 / 39 / 46 (c1: 32 / 50 / 47), BAD generic 39 · contradicts-codebase 8 · missing-critical 6 · off-platform 2 · wrong-mode 1 · harmful 0; verdict versus c1 better 21 / same 1; "would have helped" the recorded implementation: helped 18 · neutral 4 · hurt 0; unjustified direction slots 10 over 22 tasks (c1: direction-mismatch on 20 tasks). This is reviewer-estimated evidence, not an implemented round.

## L. Held-out v4 — generation and independence

434 cases (target ≥ 400): create 72 · refactor 72 · polish 52 · responsive 30 · audit-review 42 · accessibility 40 · tv-media 26 · desktop-native 26 · mobile-native 26 · kiosk 22 · adversarial 26 (20 abstain, 6 partial); artifact new 66 / existing 348 / unknown 20; 86.4 % of prompts without an explicit mode verb; 88.6 % of platform-specific prompts without a canonical platform name. Six generator agents (claude sonnet) saw only `BRIEF.md` and the public `ONTOLOGY.md`; three expectation reviewers (claude opus, a different family) corrected 336 of 434 cases (thin required sets, over-demanding platforms, narrow mode lists, per-bucket templating, near-duplicates rewritten); four bundle-quality reviewers (claude opus) saw prompt + guidance text only. Limitation: expectation reviewers and quality reviewers share a model family; generators do not. Generated after the c1 freeze, placed and run after the c2 freeze (ontology unchanged).

## M. Held-out v4 — machine results against the pre-registered thresholds (run once)

| # | metric | threshold | result | met |
|---|---|---|---|---|
| 1 | platform correctness (394 claims) | ≥ 0.88 | 208 / 394 = 0.528 (174 UNKNOWN, 12 wrong) | no |
| 2 | false platform assignment | ≤ 0.05 | 12 / 394 = 0.030 | yes |
| 3 | mode correctness (multi-mode credit, 414 non-abstain) | ≥ 0.75 | 366 / 414 = 0.884 | yes |
| 4 | scope correctness (434) | ≥ 0.92 | 406 / 434 = 0.935 | yes |
| 5 | required concern coverage (mean) | ≥ 0.90 | 0.794 | no |
| 6 | required concept recall (mean) | ≥ 0.58 | 0.535 (236 / 414 cases ≥ 0.5) | no |
| 7 | critical concept recall (mean) | ≥ 0.80 | 0.630 | no |
| 8 | forbidden concept rate | ≤ 0.05 | 40 / 414 = 0.097 | no |
| 9 | human GOOD + PARTIAL | ≥ 0.82 | 309 / 410 = 0.754 | no |
| 10 | human BAD | ≤ 0.18 | 101 / 410 = 0.246 | no |

Secondary: empty bundles 0 (≤ 0.01 met); acceptable cases 100 / 434 = 0.230 (≥ 0.50 missed); fundamental mode misses 15 / 414 = 0.036 (≤ 0.10 met); mean guidance tokens 895 (≤ 1200 met). Abstain cases: 8 / 20 abstained by the machine scorer; 12 engineering prompts with UI nouns received bundles. Partial cases: 2 / 7 returned PARTIAL. By category (acceptable / n): accessibility 10 / 40, adversarial 10 / 26, audit-review 12 / 42, create 11 / 72, desktop-native 0 / 26, kiosk 7 / 22, mobile-native 3 / 26, polish 15 / 52, refactor 21 / 72, responsive 6 / 30, tv-media 5 / 26. Primary thresholds met: 3 / 10; mandatory (#2, #4, #8, #9, #10): 2 of 5.

## N. Held-out v4 — blind bundle-quality review

GOOD 99 · PARTIAL 210 · BAD 101 · WRONG_ABSTAIN 15 · CORRECT_ABSTAIN 9 (434). Defect categories over BAD / WRONG_ABSTAIN / weak PARTIAL: generic 98, wrong-screen 88, missing-critical 83, off-platform 25, should-not-abstain 15, should-abstain 12, contradicts-request 5. Reviewer observations, consistent across all four parts: dilution by concern-filling guardrails ("Design empty, loading, error and partial states", "Desktop status bar", "Accessible names", "Trend aesthetics") on prompts they do not concern; whole-product direction records reaching core with no lexical match; literal token traps ("compare" → bar chart, "tab" → tabs, "landscape" → 16:9 media cards, "overlay" → player); one-directional platform leakage (TV guardrails on web/desktop prompts, mobile guardrails on TV prompts); the right record often present only as a guardrail behind off-task cores; CONFIDENT status not protective (13 of 101 BAD were CONFIDENT); the strongest groups are tightly scoped TV, desktop and kiosk prompts and unambiguous accessibility prompts.

## O. Failure analysis by earliest wrong layer (v4, aggregate classes only)

- **scope** (28 wrong): 12 engineering prompts that mention UI nouns were answered (should-abstain) and 15 UI prompts were abstained (should-not-abstain: help-centre content, whiteboard presence, window persistence, paywall differentiation, empty inbox, kitchen display privacy, captions, notch overlap); 5 of 7 partial prompts were treated as fully in scope.
- **platform** (174 UNKNOWN, 12 wrong): the UNKNOWN-over-wrong rule holds (3 % false), but the reviewers require a platform from situational cues (remote, sofa, tray icon, gloves, checkout lane) that the evidence table grades WEAK or does not know; UNKNOWN spans all platforms (desktop 46, web 40, mobile 38, tv 32, kiosk 18).
- **mode** (48): create ↔ existing confusion on spec-shaped versus observation-shaped prompts; 15 fundamental.
- **expected concepts / retrieval / selection** (recall 0.535, critical 0.630, coverage 0.794): most-missed critical ids adaptive.breakpoint_matrix, layout.focal_hierarchy, state.saving_conflict, touch.minimum_target, state.loading_empty_error, data.refresh_timestamp, layout.one_primary_action, table.column_priority; forbidden deliveries dominated by platform-generic concepts (touch.gestures_discoverable 8, interaction.shortcuts 7, touch.minimum_target 5, desktop.persist_workspace 3, touch.ime_keyboard 3, touch.thumb_reach 3) delivered by platform-matrix guardrails the reviewers consider wrong for the prompt.
- **direction / project adaptation**: not scored by v4 (guidance path); covered by the real-project round.

## P. Historical sets (non-blind, run once on c2)

| set | Phase 4 final | Phase 5 c2 |
|---|---|---|
| v1 (145) | acceptable 38, recall 0.359, mode 119, platform 132, empty 7 | acceptable 34, recall 0.369, mode 106, platform 122, empty 7 |
| v2 (212) | acceptable 30, recall 0.234, mode 139, platform 201, abstain 17 / 20 | acceptable 29, recall 0.232, mode 137, platform 196, abstain 17 / 20 |
| v3 (311) | acceptable 125, scope 287, platform 223, mode 181, recall 0.498, forbidden 8, abstain 25 / 30 | acceptable 152, scope 298, platform 221, mode 228, recall 0.533, forbidden 6, abstain 24 / 30 |

v1 and v2 use Phase 2/3 scoring (literal platform and single-mode credit) and move within noise; v3 improves on scope, mode and recall with the new layers. These sets were not used for tuning (aggregate classes only).

## Q. Benchmark v2 (18 author-written queries; regression coverage only)

Idle rerun, 7 repetitions, upstream revision unchanged. Relevant-term coverage upstream 0.200 · search k=5 0.915 · guidance bundle 0.927 (Phase 4: 0.200 / 0.909 / 0.928); off-target 0.189 / 0.111 / 0.106 (Phase 4: 0.189 / 0.148 / 0.106); empty results 3 / 0 / 0; cold median 359 ms upstream vs 815 ms ours (p95 746 / 1572; Phase 4: 200 vs 414), warm median search 193 ms · guidance 297 ms (Phase 4: 43 / 54); mean concern coverage 0.992, bundle size 6.67, bytes 4777; categories where upstream is higher: none. Regression coverage only; the benchmark queries are author-written and were never used for tuning.

## R. Output size and performance

Guidance Markdown mean 1045 / median 1055 / p95 1370 tokens (Phase 4: 1031 / 1016 / 1302); guidance JSON mean 2858 / p95 3543; direction Markdown mean 2282 / p95 2575; bundle size mean 6.3 / p95 8; bundle tokens mean 950 / p95 1335 (239 queries, chars / 4). v4 mean bundle tokens 895. The 800–1300 bundle budget holds.

## S. Activation

Proxy on the frozen 180-case set: precision 1.000, recall 1.000, FPR 0.000 (baseline 0.987 / 1.000 / 0.014); two transient false positives introduced by the widened UI vocabulary ("shard the tenants table", "DataGrid binding throws") were fixed by letting activation defer to a decisive technical-scope abstention and by keeping "row / column" out of the activation vocabulary; the frozen set was not edited. Real-model activation: SKIPPED (not authenticated).

## T. Knowledge changes

247 records (237 at baseline): added a11y-skip-link, tv-dpad-hold-pacing, feedback-progress-async, interaction-drag-drop, data-exceptions-first, table-column-disambiguation, ecommerce-delivery-promise, comp-tv-side-sheet, media-photo-viewer, tv-search-input; corrected cta-sticky-bar and metadata-rich (empty concept lists), a11y-modal-dialog (TV / kiosk), states-offline-and-sync (+ data.refresh_timestamp), comp-search (TV search concept moved), i18n-text-expansion-rtl (language-switch guidance and keywords), a11y-focus-visible (measurable focused-vs-unfocused contrast, TV ring size), comp-photo-capture-field (+ perf.image_sizing), a11y-time-and-auto (product fit any), comp-kpi-tile (product fit any), a11y-color-not-only (declares interaction). Concepts 109 → 114; no ontology explosion; lexicon: modes de-duplicated, stack→platform inference removed for Compose and SwiftUI, activation vocabulary widened.

## U. Documentation

`NEW-ARCHITECTURE.md` §14 (Phase 5), `docs/MAINTENANCE.md` (platform layer, intent v2, aliases, concept trace, scope with repository, real-project protocol and re-scoring), `docs/USAGE.md` (platform evidence, task semantics, partial scope, concept trace, README declarations), `README.md` (Phase 5 row, release-check command with v4), `research/PHASE5-PROJECTS.md`, `research/phase5-projects/PROTOCOL.md` and `TASKS.md`, `evals/heldout-v4/{THRESHOLDS,ONTOLOGY,MANIFEST}`, `research/heldout-v4-generation/` (briefs, generator and reviewer output). `SKILL.md` was not changed (it is part of the frozen build hash; the new behaviour is additive and reachable through the existing commands).

## V. Honest limits

- The blind v4 verdict is the verdict: 3 / 10 primary thresholds, five of the seven failures on concept-level metrics and human quality. The skill's bundles are diluted by concern-filling guardrails and occasionally led by a wrong-product core; those are the two classes to fix next, at the expected-concepts and selection layers, with the v4 aggregate classes as the only guide.
- Platform correctness is bounded by the pre-registered UNKNOWN-over-wrong rule: the false-assignment rate (3 %) is inside the mandatory bar, but 44 % of claims stay UNKNOWN on situational wording. Raising correctness without raising false assignment means grading more situational cues STRONG with device-class precedence, backed by new development cases, not by loosening the rule.
- The real-project evidence for c2 is re-scoring plus reviewer estimates; only c1 was implemented and rendered. A further implemented round on c2 is the next step before any stronger label.
- Real Claude activation remains unmeasured (SKIPPED). Expectation and quality reviewers share a model family; generators do not.
- Held-out v1 and v2 are historical only; their scoring predates multi-mode credit and platform evidence.
- Radius and spacing detection on token-based themes is still partial; the inspector never claims visual understanding.

## W. Deviations and incidents

- Session rate limits interrupted 14 background agents once; the five interrupted project tasks (p5-01, 05, 06, 12, 16) were completed by fresh agents from the files on disk; one generator (g2) was regenerated. No skill file changed during the round (hashes identical in every task).
- One task agent killed stray Node processes while restarting a dev server; no other task reported damage.
- The first benchmark rerun was taken under agent load and discarded; the reported numbers are from an idle rerun (7 repetitions).
- Held-out v4 was generated after the c1 freeze and run on c2; because the ontology and the case set are independent of the c1→c2 code changes, the run stays blind. The expectation reviewers changed 336 of 434 generator cases; all changes are logged in `research/heldout-v4-generation/reviewed-chunk-*.json`.
- Three platform-evidence cases and seven round-derived cases were amended with dated notes before the corresponding fix was run (Section H); no held-out case was touched.

## X. Verdict, restated, and what would change it

**personal-production-ready.** Not stable-candidate: v4 met 3 of 10 primary thresholds and failed mandatory #8 (forbidden 9.7 %), #9 (GOOD+PARTIAL 75.4 %) and #10 (BAD 24.6 %). The skill classifies scope, platform (without false assignment) and mode well on unseen wording, keeps existing systems intact on real codebases, and after c2 helps rather than hurts on the 22 real tasks; its bundles are still too diluted and too often led by a wrong-product core to be called stable. The next phase should target, in this order: bundle purity (concern-filling guardrails, whole-product cores without lexical evidence), expected-concept recall for critical ids (breakpoint matrix, focal hierarchy, saving conflict, minimum target, states), and platform inference from situational cues — each with cases written first, a frozen build, an implemented real-project round, and a new blind set.

Case counts for the validator: development 885 cases · regression 54 cases · heldout 145 cases · heldout-v2 212 cases · heldout-v3 311 cases · heldout-v4 434 cases · activation 180 cases.

This line indexes the case FILES AS THEY STAND, and is the only line the validator reads. It diverges from the Phase 5 narrative above on purpose: the tables and prose report the suites as they were when Phase 5 ran (575 development, 40 regression), and are a record of that run rather than a running total. Development has since grown by 310 cases and regression by 14, added after Phase 5 closed and NOT covered by any metric quoted above. Amended 2026-09-16 because `validate_skill.py` was failing on the stale counts; the Phase 5 figures were left standing rather than overwritten.
