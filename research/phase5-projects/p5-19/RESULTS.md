# p5-19 — results

## Task
"Sync status is a spinner that never says what is happening." (run verbatim)

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8`. Nothing under `design-engineering/` was touched.

## Project / stack / platform
`research/phase3-projects/p3-mobile-flutter-field/project` — Flutter 3.22+ / Material 3, Riverpod, go_router, connectivity_plus. Utility field-inspection app (outdoor sunlight, gloves, offline-first). Hand-tuned light + dark `ColorScheme`, `StatusColors` ThemeExtension, `FieldSizes` tokens (56 dp controls, 12 dp gaps, radius 8), in-app high-contrast switch. Platform: mobile. p5-18's photo-tile change in `defect_report_screen.dart` was kept and not touched.

## Existing UI or new screen
Existing UI. What the code did before: `SyncState = {pending, lastSyncedAt, syncing: bool}`; `drain()` flipped `syncing`, waited 800 ms and emptied the queue. No per-item status, no count, no current item, no failure state, no reason. The banner said "Syncing 3…", the queue sheet listed every row as "Pending" and its button said "Syncing…"; the Settings row repeated the pending count. (The only literal `CircularProgressIndicator` in the app is the defect form's Save button — a local write, not the sync — so the sentence describes the "Syncing…" text/button state, which is a spinner in all but shape: it names no item, no progress and no outcome.)

Render mode: **html-twin + static review**. `flutter`/`dart` are not on PATH. The p5-18 twin (Phase 3 twin + p5-18 photo viewer) was copied to `p5-19/render/twin.html` and extended with the five banner states, the queue sheet with per-item status chips and the Settings row; shot at 390×844 @2x with Playwright 1.63.0. The Phase 3 and p5-18 twins are unchanged.

## Design-context table (`01-inspect.json`, identical output to p5-18 — same project)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `AppBar` on every screen, go_router stack, modal bottom sheets | yes (`routing: []` although `GoRouter(routes:…)` is in `main.dart`) |
| theme | dual-theme, default light | KNOWN | `theme` + `darkTheme` + `highContrastTheme`, `ThemeMode.system` | yes |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations") | flat, elevation 0, 1–3 dp `BorderSide` outlines everywhere | partial |
| radius | small (4) | INFERRED | `FieldSizes.radius = 8` on every control; 4 only on the index chip | no |
| spacing | irregular ([2, 12]) | UNKNOWN | explicit scale `FieldSizes.space1..space8` = 4/8/12/16/24/32 | partial |
| typography | unknown; tabular_numerals false | UNKNOWN | system font (correct); explicit `TextTheme`; `FontFeature.tabularFigures()` on the count | partial |
| components | "go_router, riverpod" | KNOWN | those are libraries; components live in `lib/widgets/` (`OfflineBanner`, `SyncQueueSheet`, `StatusBadge`, …) | partial |
| product_hints | erp, iot | — | field service / utility inspection; README says "outdoor", "gloves", "offline-first" | no |
| tests | [] | — | `test/checklist_test.dart` exists | no |

## Requirements verdict (`02-requirements.json`, status CONFIDENT)
| field | value | verdict |
|---|---|---|
| platform_evidence | `[]`; `known` has "platform=mobile (project inspection)" | correct (KNOWN from pubspec, no MISSING confirm this time) |
| intent.artifact_state | existing ("present-tense observation") | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | `["performance-ux"]` from "spinner" | partial — the complaint is about status communication (what is happening, what failed), not perceived speed |
| intent.change_scope | unknown; scope moderate | acceptable |
| mode + evidence | audit ("perceived-performance defect"), refactor | acceptable (in my list; polish/refactor would fit better) |
| scope.kind / reason | in-scope, "UI design / interaction task" (ui: spinner, concept:state.loading_empty_error) | correct |
| **activation** | `decision: skip`, ui_score 0, non_ui_score 0, no ui_terms | **wrong** — the activation gate says skip on a sentence the scope layer calls in-scope; "spinner", "sync status", "what is happening" are not in the activation lexicon. If activation gates the skill, this task never reaches it. |
| change_budget | low | correct |
| intent.preserve | [] | acceptable |
| product | erp, iot | wrong (README misread; persists from Phase 3) |
| environment | `[]` | wrong — README says outdoor / gloves; this is what filtered `mobile-field-use` out of every bundle ("environment ['gloves','outdoor'] not in request") |
| density | medium ("implied by product erp") | wrong for a gloves app (56 dp controls) |
| risk | low | arguable (safety-critical defect reports whose upload fails silently) |
| concerns.required | accessibility, interaction, component, **data-display ("numbers, tables or charts are the content")** | data-display wrong; **feedback is only "recommended"** although the whole task is feedback |
| required_concepts | state.loading_empty_error, touch.minimum_target, **table.tabular_figures ("numeric data")** | loading/error partly right (the failed state); tabular figures wrong; `feedback.progress_indicator` and `a11y.live_status` never demanded |

## Guidance verdict (`03-guidance.md/json`; status CONFIDENT; bundle 6 = core 2 + guardrails 4; 768 tokens; no `concept_trace` in the explain output)
| record | role | verdict | BAD category | note |
|---|---|---|---|---|
| `metadata-inline-badges` | core | partial | — | "Pill for status/count, text inside, never colour only" — usable for the per-item status chip in the queue sheet; says nothing about progress, the current item, or failure. Selected as "highest-scoring pattern with lexical evidence" (the word *status*). |
| `comp-list-row-mobile` | core | off-target | **generic** | Swipe actions, pull-to-refresh, sticky headers, selection mode via long press — none of it applies; selected only to cover the "component / data-display / interaction" concerns. Ignored. |
| `states-offline-and-sync` | guardrail | relevant | — | The one record about the task: per-item 'pending sync' marker, 'last synced' timestamp, manual retry, never lose data. All of it was already in the Phase 3 code. It has no line about *progress* (n of m, current item) or a *failure reason*, which is what the sentence asks for; and it landed as a guardrail, not core. |
| `layout-states-empty-loading-error` | guardrail | partial | — | "Error: what failed, what to do, retry that works" shaped the failed state. The loading half (skeleton at final size) is about page loads, not a background upload. |
| `typo-scale-and-roles` | guardrail | off-target | **generic** | Selected for "tabular figures / numeric data" because data-display was (wrongly) required. "2 of 3" is not a table. Ignored. |
| `a11y-color-not-only` | guardrail | relevant | — | Banner states and chips are word + icon + colour; matches the codebase's `StatusBadge` idiom. Confirmed rather than informed. |

Relevant 2 · partial 2 · off-target 2. Search k=12 (`03-search-k12.md`) ranked `a11y-live-status` 5th (0.339) and `desktop-status-bar-and-error-navigation` 2nd (0.427, "avoid when: mobile") — neither made the bundle; the mobile list row (lexical 0.0) did.

### Real concept recall
Delivered concepts (union over the 6 selected records): a11y.color_not_only, brand.type_roles, data.pagination_strategy, interaction.selection_visible, state.loading_empty_error, state.offline_sync, state.saving_conflict, table.tabular_figures, touch.gestures_discoverable, touch.minimum_target (10).

| expected id | critical | delivered? | layer if missing |
|---|---|---|---|
| feedback.progress_indicator | yes | no | **expected-concepts** — never demanded. Also a knowledge gap: the only carriers are `comp-wizard-stepper`, `comp-setup-checklist`, `nav-wizard`; no record in the base describes a determinate progress indicator for async work (upload/sync: n of m, current item, failure reason), and the word "spinner" appears in no record. |
| state.offline_sync | yes | yes (`states-offline-and-sync`) | — |
| a11y.live_status | yes | no | **expected-concepts** — never demanded; carrier `a11y-live-status` was a candidate (0.339) but nothing asked for it. |
| env.glanceable_status | yes | no | **expected-concepts** — never demanded; its only carrier `mobile-field-use` was filtered on environment (root cause upstream: `environment=[]` in requirements). |
| a11y.color_not_only | no | yes (`a11y-color-not-only`) | — |
| data.refresh_timestamp | no | no | **expected-concepts** — never demanded; only carrier is a chart record (`charts.jsonl`). `states-offline-and-sync` says "'last synced' timestamp" in prose but does not carry the id (labelling gap). |
| process.reuse_first | no | no | **candidate-retrieval** — recommended, but `impl-reuse-before-new` is not among the top-12 candidates (12th scored 0.234). |

Recall 2/7 = **0.29**; critical recall 1/4 = **0.25**.

## Direction verdict (`04-direction.md/json`)
Change budget low. Preserved: navigation, layout, surface, cards, typography, color (light-first dual theme), motion, focus, cta, imagery, icon — all correct. `validation.ok = true`. The JSON has no `preservation` metrics block (null).
| slot | choice | justified? |
|---|---|---|
| density | `density-medium` (new) — "8 px base, 40–48 px interactive heights… safe default when the audience is unknown" | **no** — derived from `product=erp`; the codebase is explicitly low density (56 dp controls, 12 dp gaps) and the direction's own preserved-slots rule ("existing system wins") makes it moot. Ignored. |
| metadata | `metadata-inline-badges` (new) — "no repository evidence for this slot" | yes for the queue rows (status chip, word inside, ≤2 per item); the repository does have evidence (`StatusBadge`) that inspect did not surface. |

Fingerprint `content_density: medium` is wrong for the app; `metadata_density: inline-badges` is fine.

## Implementation
Files changed (originals in `before/`):
- `project/lib/models/inspection.dart`: `enum SyncItemStatus { queued, sending, sent, failed }` with a word per value; `PendingSync` gains `status`, `error` (plain-language reason), `attempts`, `copyWith`.
- `project/lib/state/providers.dart`: `SyncState` gains `runTotal`, `runSent`, `completedAt` and derived `sending`, `failed`, `queued`, `hasFailures`, `progress`. `drain()` now sends items one at a time, marks each queued → sending → (removed) or failed-with-reason, keeps `lastSyncedAt` only when something went, sets `completedAt` when the queue is empty and clears it after 4 s. New `retry(id)` and `retryFailed()`. Simulated transport fails ids containing `fail` on the first attempt so the state can be exercised. Public API (`enqueue`, `drain`, `syncQueueProvider`, `isOnlineProvider`) unchanged; `checklist_test.dart` still finds `Offline`.
- `project/lib/widgets/offline_banner.dart`: five explicit states, each with icon + headline + detail + colours + the screen-reader phrase: Offline (unchanged) · "3 waiting to send / Last synced X" · **"Sending 2 of 3 / High defect on item C2"** with a 6 dp determinate bar riding the strip's bottom edge · **"1 failed to send / Photo IMG_2091.jpg · Server rejected the file (too large)"** in `errorContainer` with a 56 dp **Retry** button (`retryFailed`) · **"All sent / Synced just now"** in `StatusColors.pass` for 4 s. The live-region label is "Sending 3 items." for the whole run (announced once, not per item), then the failure or completion phrase. Row min-height 56 dp so the strip is the same height with or without a button. New shared `SyncProgressBar` (visual only, `ExcludeSemantics`) and `SyncItemChip` (word + icon + colour, `StatusBadge` idiom).
- `project/lib/widgets/sync_queue_sheet.dart`: subtitle says "Sending 2 of 3 · <item>" / "1 failed to send · last synced X" / "Last synced X"; progress bar while sending; each row shows its own chip (QUEUED / SENDING / FAILED) and, when failed, the reason in error colour as the second line; merged semantics read "<label>. failed. <reason>."; button is "Sending 2 of 3…" (disabled, truthful) / "Retry 1 failed" / "Retry sync now".
- `project/lib/screens/settings_screen.dart`: the Sync queue row's value and icon follow the same three phrases.
- `render/twin.html`, `render/shoot.js` (p5-19 copies): banner states, chips, sheet phases, Settings row, `sent=N`.

Guidance used: `states-offline-and-sync` (per-item marker, last-synced, manual retry — kept), `layout-states-empty-loading-error` (failed state: what failed, why, Retry that works), `a11y-color-not-only` (chips and banner states), `metadata-inline-badges` (chip rules: text inside, ≤2 per row). Guidance ignored: `comp-list-row-mobile` (nothing applies), `typo-scale-and-roles` (no numeric content), the direction's `density-medium`. What actually answers the sentence — a determinate "n of m + current item", a failed state with the server's reason and a Retry, an "All sent" confirmation, a live announcement that fires once per run — came from the codebase and my expectation; no record in the bundle or the k=12 search says any of it.

Static review (no compiler): `LinearProgressIndicator(borderRadius:)` exists since Flutter 3.10; `ListTile.minTileHeight` was already used in the project; `Color.withOpacity` is deprecated from 3.27 (warning only, project pins ≥3.22); `cast<PendingSync?>().firstWhere(orElse: () => null)` is the null-safe idiom; Dart 3 switch expressions match the existing style; all new colours come from `ColorScheme` / `StatusColors` (light: `#FFE08A/#241A00`, `#FFDAD6/#410002`, `#085A26/#FFFFFF`; dark: `#523F00/#FFE08A`, `#93000A/#FFDAD6`, `#7BE495/#00210B` — every pair ≥ 7:1).

## Renders
`render/first-*.png` and `render/final-*.png` (18 each): checklist with pending / syncing / failed / synced / offline banners in light, dark and high-contrast; queue sheet offline / syncing / failed (light + dark); Settings row syncing / failed; defect form while sending.

First-render defects: 1 × **visual** — the banner grew from 72 to 86 dp when the progress bar appeared, so the content below jumped at the start and end of every run (measured with `getBoundingClientRect`). Fixed by drawing the bar over the strip's bottom edge (`Stack` + `Positioned(bottom: 0)`, the app-bar-progress idiom); final height is 72 dp in every online state (84 offline / failed, where the detail wraps to two lines, as before). Interaction 0, accessibility 0, platform 0, existing-system-mismatch 0, implementation-bug 0.
Final defects: 0. Iterations: 1.

Observed and accepted: in the failed state the banner's single button is Retry, so from the checklist the full queue is reachable only through Settings until the retry succeeds or fails again (the banner itself names the item and the reason). A two-line item label ("High defect on item C2") wraps in the sheet next to a 96 dp-min chip; `ListTile` does the same.

## Preservation
Navigation preserved (no route changes; sheet idiom unchanged). Theme preserved (only `ColorScheme` roles and `StatusColors`; no new colours; dark and high-contrast follow automatically). Typography preserved (theme text styles only). Component reuse: `OfflineBanner`, `SyncQueueSheet`, `TextButton` strip button, `ListTile`, `FilledButton.icon`, `FieldSizes`, `StatusBadge` idiom for the chip. Unjustified structural changes: 0. Provider API shape, routes, tests intact.

## Regressions to propose
1. Query: the task sentence on this project. Expect: `feedback.progress_indicator` and `a11y.live_status` in `required_concepts`; concern `feedback` required, `data-display` absent; a record about determinate progress for async work (n of m, current item, failure reason, retry) in core; `states-offline-and-sync` in core; `comp-list-row-mobile` and `typo-scale-and-roles` absent; `activation.decision` ≠ skip.
2. Query: "the upload spinner never says what is happening" on any mobile/web project. Expect: `feedback.progress_indicator` demanded and a carrier that is not a wizard/stepper; "spinner" recognised as a feedback term by activation and scope.
3. Requirements on a project whose README says outdoor / gloves / sunlight. Expect: `environment` = [outdoor, gloves] KNOWN from the project so `mobile-field-use` is never platform-filtered; density low from environment, not medium from a product guess.
4. Direction: `density-medium` must not be chosen as "new" when the repository's control size (56 dp) is available; expect density derived from tokens or preserved.
5. Inspect on this project: product hint field-service, not erp/iot; tests detected; radius 8; spacing scale 4/8/12/16/24/32; tabular numerals true.
6. `states-offline-and-sync` should carry `data.refresh_timestamp` (its prose already says "'last synced' timestamp").

## Tags
`context-detection-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `tooling-limit`, `skill-neutral`, `preservation-ok`
