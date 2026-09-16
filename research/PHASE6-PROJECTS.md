# Phase 6 implemented real-project round (32 tasks, 16 codebases)

Protocol: `research/phase6-projects/PROTOCOL.md` (Phase 5 steps + Phase 6 addendum). Tasks: `research/phase6-projects/TASKS.md`. Every task was implemented, rendered, reviewed and fixed on the **frozen candidate c3** (`research/runs/phase6-freeze-c3.json`, sha256 `ea8eed72…d9947`; start and end hash equal on all 32 tasks). Fixes routed from the round produced **candidate c4**, which was re-scored on the same tasks guidance-only (`evals/rescore_projects.py --phase 6 --label c4`, per-record re-review by an independent reviewer with the c3 verdicts as the yardstick). Implementation outcomes belong to c3 and were not re-run.

Codebases: 12 from Phases 3 and 5 plus 4 new fixtures written before the round (`p6-compose-banking` Kotlin/Compose banking app, `p6-kiosk-transit` HTML transit ticket kiosk, `p6-tv-iptv-web` Tizen/webOS TV web app, `p6-vue-inventory` Vue 3 warehouse app). Mix: web 10 · mobile 7 · desktop 6 · TV 5 · kiosk 4; existing-UI changes 27; sentences without a mode word 24 of 32. Implementers ran on Claude Opus after the first batch was cut off by a spend limit on the default model (their step 0–4 outputs were kept; expectations were never rewritten).

## Aggregate against the pre-registered pass criteria (`evals/heldout-v5/THRESHOLDS.md`, "Implemented project round")

| criterion | threshold | c3 (implemented) | c4 (guidance-only rescore) | pass |
|---|---|---|---|---|
| platform resolved-wrong with project context | 0 | 2 (p6-12 "site" read as web over a Flutter repo; p6-28 Tizen/webOS package inspected as web) | 1 (mechanical scorer only: p6-07 resolves `tablet`, which the scorer filters; the c3 reviewer judged it correct in spirit) | c3 no · c4 no (by the scorer) |
| scope correct on every task | 32/32 | 32/32 | 32/32 | yes |
| mode yes or acceptable | ≥ 0.85 | 30/32 = 0.938 (no: p6-03 "narrow down" → responsive, p6-16 create on a defect) | 32/32 | yes |
| critical recall (pre-registered) | ≥ 0.80 | **0.635** | **0.682** (12 of 32 tasks at 1.0) | **no** |
| forbidden-concept deliveries | ≤ 2 tasks | 0 | 1 (p6-27 `media.details_play_first` via the broadcast-guide direction) | yes |
| skill_effect HURT ≤ 3, HELPED ≥ 0.5 | | hurt 0 · helped 22 · neutral 10 | n/a (implementation not re-run) | yes |
| generic + wrong-screen + wrong-product records / reviewed | ≤ 0.20 | 82 / 143 = **0.573** (generic 59 · wrong-screen 22 · wrong-product 1) | 64 / 124 = **0.516** (generic 55 · wrong-screen 9 · contradicts-codebase 1) | **no** |
| unjustified direction slots (round) | ≤ 2 | **22** | **12** | **no** |
| severe systemic defect | none | none harmful (no task hurt); the recurring classes are omission and filler, not harm | | yes |

**Round verdict: FAIL** on c3 (5 of 9 criteria) and still FAIL on c4 (5 of 9). The skill helped on 22 of 32 implemented tasks and hurt none; final defects across 32 tasks were 7 (from 68 at first render), all fixed by the implementers' own render-and-inspect loop. The failing criteria are the three the mission targeted: critical concepts still go undemanded, generic baseline records still fill bundles, and the direction still marks slots `new` on existing systems.

## What c4 changed on the same 32 tasks (guidance-only)

- **Better 17 · same 10 · worse 5** by the independent re-review. Off-target records 37 → 14; wrong-screen 22 → 9; bundle tokens mean 681 → 581; platform fixed on p6-12 and p6-28; mode fixed on p6-03 and p6-16 (critical recall 0 → 0.5 there); i18n, sync-status, virtualization and orientation records now enter where they were never candidates (p6-32, p6-19 partially, p6-20, p6-27).
- **Worse (5):** p6-04, p6-10, p6-18, p6-26, p6-29 — the bundle shrank past the record the c3 implementer had actually used (`layout-states-empty-loading-error`, `layout-dashboard-grid` + `a11y-color-not-only`, `a11y-keyboard-operable`, `comp-mini-player`, `nav-wizard`). Precision-first selection removes filler and occasionally the useful neighbour with it.
- **Unchanged classes:** 20 of 32 c4 bundles still miss a pre-registered critical concept (`layout.focal_hierarchy`, `a11y.color_not_only`, `a11y.live_status`, `navigation.orientation_and_back`, `data.refresh_timestamp` recur) — an expected-concepts problem that aliases only partly reach; `generic` partials remain 55 (TV platform baselines `tv-typography-distance` / `tv-safe-area` / `tv-dpad-axes`, states, hierarchy).

## Recurring findings by earliest wrong layer (c3 implementers' routing)

| layer | count | typical |
|---|---|---|
| expected-concepts | 76 concept misses (28 task-level) | concept named in the sentence but no alias / rule demanded it |
| bundle-selection | 33 + 27 | demanded concept dropped at the cap or by utility; generic carrier admitted |
| project-context | 32 | inspector token / spacing / radius misreads (Compose `Spacing.kt`, CSS `:root` tokens, SwiftUI theme), twin HTML scraped from `render/` (fixed in c4: `render/` ignored), Tizen/webOS package read as web (fixed in c4) |
| requirements / mode | 17 / 3 | "narrow … down", "small", "cut off" as viewport cues; "mouse" negated by "without"; present-tense "happens" |
| direction | 16 | `cta` / `cards` / `imagery` marked `new` on existing systems |
| candidate-compatibility | 10 | drag-drop rule as a keyboard carrier; plan comparison from SaaS product evidence; mini-player from media component; editable grid on a read-only grid |
| criticality | 8 | product / repository baselines (tabular figures, privacy, outdoor) marked critical; keyboard critical on touch-only a11y review |
| candidate-retrieval | 2 | top search hit never a candidate (virtualization, numeric alignment) |
| knowledge gap | 2 | "derive instead of re-asking"; focus restore on a non-modal web control |

Process records: `impl-reuse-before-new` was needed on 4 tasks and judged generic on 4 others; SKILL.md §2 / §7 were sufficient on 28. Records were not removed (see PHASE6-RESULTS.md §L).

Raw data: `research/runs/phase6-projects-c3.json` (implemented round aggregate), `research/runs/phase6-c4-projects-rescore.json` (mechanical rescore), `research/runs/phase6-projects-c4-review.json` (re-review aggregate), per task `research/phase6-projects/p6-NN/{RESULTS.md, artifacts.json, c4/review.json}`.
