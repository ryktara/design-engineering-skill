# p6-19 — "Add a status bar with the last sync time and any failed postings."

- **Project:** `research/phase3-projects/p3-erp-desktop-dotnet/project` — WPF (.NET 10), MVVM, single window (`MainWindow` → `PurchaseOrderLinesView`), light-first semantic brush dictionary.
- **Platform:** desktop · **Existing UI**, new element (not a new screen).
- **Build hash start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`** (matches the frozen c3 candidate).
- **Key fact the task hinges on:** the project **already has a status bar** (`Views/PurchaseOrderLinesView.xaml` lines 175–229, styled by `Bar.Status` / `Bar.Status.Item` / `Bar.Status.Sep` / `Bar.Status.Text` / `Btn.Status.Link` in `Themes/Controls.xaml`). The correct implementation is to extend it with two segments, not to build one.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | `<Menu>` docked top + command bar below | yes |
| theme | light-first | KNOWN | `Themes/Light.xaml`, no dark dictionary | yes |
| surfaces | bordered-flat | INFERRED | 1 px borders, zero shadows/elevation | yes |
| radius | small | INFERRED | 2 px on controls (10 only on the error dot) | yes |
| spacing | 4 | INFERRED | `Space.*` tokens on a 4 base (6/8/12/16) | yes |
| typography | humanist-sans | INFERRED | Segoe UI Variable Text + Cascadia Mono for IDs, tabular numerals | yes |
| components | wpf | KNOWN | WPF `StatusBar`, `DataGrid`, custom styles | yes |

All seven fields correct. What inspect does **not** surface is the screen's existing composition (status bar, command bar, single data table) — see the direction miss in §4: the direction step reads "no repository evidence for this slot" for layout/cta/cards/metadata and invents them.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| `platform` / `platform_evidence` | `desktop`, evidence `[]`, known via project inspection | correct |
| `intent.artifact_state` | **`new`** | **wrong** — existing codebase, existing screen, existing status bar. Partly rescued by `constraints.preserve_existing_system: true`. |
| `intent.operations` | `["create"]` | correct |
| `intent.problem_domain` | `[]` | acceptable (no problem stated) |
| `intent.change_scope` | `unknown` | weak |
| `intent.preserve` | `[]` | wrong — should carry navigation/theme/typography for an existing UI |
| `mode` / `mode_evidence` | `["create"]`, "build/create request" | acceptable (within my `create/refactor/polish`) |
| `scope.kind` | `in-scope` | correct |
| `change_budget` | `moderate` | correct |
| `product` | `erp` from the word "posting" | correct and useful |
| `project_context` | full, matches inspect | correct |

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Bundle = 7 records (core 2 + critical guardrails 5). **OPTIONAL layer absent** (`optional_useful` 0, `optional_noise` 0). ≈1063 guidance tokens.

| record | layer | verdict | category |
|---|---|---|---|
| `metadata-rich` | core | partial | `wrong-screen` — it is guidance for the grid's columns, not the bar; only its "status as text+colour" line applied |
| `dir-operational-workbench` | core | relevant | — |
| `impl-reuse-before-new` | guardrail | relevant | — |
| `desktop-status-bar-and-error-navigation` | guardrail | relevant | — the best record in the run; it names "sync/save state with timestamp", "real separators, not spaces", LiveSetting/UIA announcements, and "the bar keeps its height at every window width" |
| `desktop-keyboard-first` | guardrail | partial | `generic` — true, but the task adds no keyboard surface |
| `data-exceptions-first` | guardrail | relevant | — word + icon + colour, count in the status bar, state the rule |
| `typo-scale-and-roles` | guardrail | partial | `generic` — the project already has `Text.Body/Caption/Subtitle`; generating a scale would violate preservation |

relevant 4 · partial 3 · off-target 0. Bundle-level defect: `missing-critical` (below).

### Concept recall

delivered = union over selected records (14 concepts). recall **4/7 = 0.57**, critical **1/3 = 0.33**.

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `process.reuse_first` (critical) | yes (`impl-reuse-before-new`) | — |
| `a11y.color_not_only` | yes (`data-exceptions-first`) | — |
| `a11y.live_status` | yes (`desktop-status-bar-…`) | — |
| `data.exception_first` | yes (`data-exceptions-first`) | — |
| `data.refresh_timestamp` (critical) | **no** | `expected-concepts` |
| `state.offline_sync` (critical) | **no** | `expected-concepts` |
| `desktop.spacing_grid` | no | `expected-concepts` |

The two critical misses are the same failure and it is the headline result of this task: **"last sync time" is half the sentence and neither `data.refresh_timestamp` nor `state.offline_sync` was ever demanded.** They do not appear anywhere in `concept_trace` — so they were never candidates, never ranked, never dropped. This is **not** a knowledge gap: `advise.py search "<sentence>" -k 12` (`03-search-k12.md`) returns `states-offline-and-sync` as the **#1 hit at 0.574** ("a 'last synced' timestamp", "queue writes locally with a visible 'pending sync' marker", "stale data is labelled with its age") and `feedback-progress-async` at #2 ("on failure name the item and the reason with a Retry action"). Both records exist, both rank top-2 for the literal sentence, and neither reached the bundle because no concept demanded them. The guidance survived only because `desktop-status-bar-and-error-navigation` happens to mention a timestamp in prose while carrying none of the sync concepts.

`status` was CONFIDENT, not PARTIAL_SCOPE, so no design/engineering split note to judge.

### Process guidance check

`impl-reuse-before-new` **was** in the bundle and was the right guardrail for this task (an existing status bar is exactly the reuse-vs-new trap), though I had already read the XAML and found the bar. `verify-render-and-inspect` was **not** in the bundle and SKILL.md §7 was enough — I rendered anyway and it caught three defects. `process_records_needed: true`, for the reuse record specifically.

## 4. Direction verdict (`04-direction.md`)

Preserved: navigation, density, surface, typography, color, motion, focus, icon — all correct, all "do not replace it for this task".

**5 slots marked `new`, all with the reason "no repository evidence for this slot", none justified by the sentence** (`unjustified_direction_slots: 5`; expected 0 on an existing UI with a moderate budget):

- `layout: master-detail` — **contradicts the codebase**: one full-width data grid, no detail pane, and the slot guidance tells me to build a list+detail pane with Back on narrow widths.
- `cards: card-bordered` (6–8 px radius) — contradicts both the codebase (2 px, no cards) and the direction's own surface slot ("no rounded card containers inside panes").
- `cta: cta-toolbar-commands` — harmless; describes the command bar the project already has.
- `imagery: imagery-none` — harmless; already true.
- `metadata: metadata-inline-badges` — harmless; already true.

Root cause is one layer earlier than `direction`: `01-inspect.json` reports no layout/cta/metadata/card evidence at all, so every slot the project does have but inspect cannot see gets invented. Validation reported OK, which it should not have for `layout: master-detail` against a single-table window.

## 5. Implementation

Files changed (originals in `before/`):

- `Models/FailedPosting.cs` **(new)** — `record FailedPosting(Reference, Reason, AttemptedAt)`.
- `Models/SampleData.cs` — `LastSync()` and `FailedPostings()` (two deterministic failures with real ERP reasons).
- `ViewModels/PurchaseOrderLinesViewModel.cs` — `LastSyncAt`, `LastSyncFailed`, `SyncCompact`, `LastSyncText`, `LastSyncTooltip`, `FailedPostings`, `FailedPostingCount`, `FailedPostingSummary`, `FailedPostingDetail`, `RetryPostingsCommand`, `Ago()`, a 30 s `DispatcherTimer` so the relative age never goes stale; `LoadAsync` sets synced state on success and `Sync failed` on the error path.
- `Views/PurchaseOrderLinesView.xaml` — two new segments **inside the existing `StatusBar`**, inserted after the existing error segment so no existing segment is reordered: failed postings (`!` glyph + `Btn.Status.Link` "2 postings failed — Retry", tooltip naming every reference and reason, `LiveSetting=Polite`) and last sync (`Synced 23:32 (4 min ago)`, tabular numerals, full timestamp in the tooltip).
- `Views/PurchaseOrderLinesView.xaml.cs` — extended the project's existing chrome-priority ladder (see defects).

No new styles, no new brushes, no new fonts: every element uses `Bar.Status.Sep`, `Bar.Status.Text`, `Btn.Status.Link`, `Brush.Feedback.Error` (5.76:1 on the `#EEF0F3` bar) exactly as the existing error segment does.

**Guidance used:** `impl-reuse-before-new` (extend the existing bar, reuse its styles), `desktop-status-bar-and-error-navigation` (real separators; sync state *with* a timestamp; UIA `LiveSetting`; constant bar height), `data-exceptions-first` (word + `!` + colour, never colour alone; count in the bar; the failure reason stated), `dir-operational-workbench` (4 px grid, tabular figures, status colour language), `metadata-rich` (status as text+colour).
**Guidance ignored:** `typo-scale-and-roles` — the project has named text roles already and a new scale would break preservation; `desktop-keyboard-first` — no new keyboard surface, the existing accelerator set is untouched (verified by the harness scenario).

## 6. Render

`render_mode: native` — the project's own `--capture` harness (`RenderTargetBitmap`, real client area). Desktop viewport 1440×900, plus 1024×700 and the error state.

**First render (`render/first-ready-1440x900.png`) — 1 defect:**

1. `visual` — the left status region overflowed: the bar ended at "… ! 2 postings failed —", the "Retry" word was cut and the whole last-sync segment and the "2 unsaved" segment were clipped off-screen. The project's chrome-priority ladder folds the key-hints string only below 1180 DIP, which no longer leaves room once two segments are added.

**Fixes (3 iterations), then `render/final-*.png`:**

1. Raised the key-hints fold floor to `1180 + 300` while failed postings occupy the left region — following the project's own stated priority ("key hints are the lowest-priority status segment"). A learning aid must not displace an exception.
2. `visual` — the sync text `Synced 23:28 · 4 min ago` used the middle dot, which is the bar's **segment** separator, so the one segment read as two. Changed to `Synced 23:28 (4 min ago)`.
3. `visual` — at 1024×700 the sync value truncated mid-value ("Synced 23:"). Added `SyncCompact` (drops the clock, keeps the age, full timestamp still in the tooltip) below 1180, and folded the Subtotal/Tax detail earlier (1220 instead of 1000) while postings are failing. At 1024 the only thing that now trims is the pre-existing lowest-priority "columns hidden" text.

**Final defects: 0.** Verified at 1440×900 ready, 1024×700 ready, and 1440×900 error (`Could not load lines · 0 lines · Sync failed 23:29 (4 min ago)` — degrades in words, no colour-only signal, no failed-postings segment since nothing loaded).

Defect 1 is partly on me: `desktop-status-bar-and-error-navigation` says "the bar keeps its height at every window width" but says nothing about its *width* budget, and I shipped the overflow to the first render anyway.

## 7. Preservation & regression check

Navigation, theme, typography, spacing, focus and component conventions all untouched; zero unjustified structural changes; no new primitive except the `FailedPosting` record, which has no existing equivalent. The direction's `master-detail` and `card-bordered` slots were ignored — implementing them would have been the structural violation.

The previous task's purchase-order grid keyboard handling was **not touched**. Confirmed by running the harness `--scenario mouseless`: Ctrl+F → filter → Enter back to grid, Esc Esc, F4 dropdown, Ctrl+Shift+S sort toggle, Del + arrow, Ctrl+Z + arrow, add-line focus, empty-state focus — all steps behave as before. The two new status-bar controls sit inside `KeyboardNavigation.TabNavigation="None"`, so they take no tab stop, exactly like the existing error link.

## 8. Misses by earliest layer

| layer | what |
|---|---|
| `expected-concepts` | `data.refresh_timestamp` and `state.offline_sync` (both pre-registered critical) were never demanded for a sentence whose subject is "the last sync time"; `states-offline-and-sync` is the #1 search hit for the same sentence, so the records exist and rank — the demand side is the gap. `desktop.spacing_grid` likewise never demanded. |
| `requirements` | `intent.artifact_state = "new"` on an existing codebase with an existing status bar; `intent.preserve` empty; `change_scope` unknown. |
| `project-context` | inspect reports no layout / cta / cards / metadata evidence although the window plainly contains one data table, a command bar, a status bar and inline status text. |
| `direction` | 5 slots invented as `new`, two of them (`layout: master-detail`, `cards: card-bordered`) contradicting the codebase and the direction's own surface slot, with `Validation: OK`. |

## 9. Regressions to propose

1. **query** `Add a status bar with the last sync time and any failed postings.` — **expect** `data.refresh_timestamp` and `state.offline_sync` in required (ideally critical) concepts, and `states-offline-and-sync` in the bundle. Any wording pairing "sync"/"synced"/"last updated" with a time noun should demand the refresh-timestamp concept.
2. **query** the same sentence with `--project` pointing at a repo whose inspect reports an existing UI — **expect** `intent.artifact_state == "existing"` and a non-empty `intent.preserve`; "add X" names a new element, not a new artifact.
3. **query** `direction` for the same sentence + project at a moderate budget — **expect** 0 slots marked `new`, and specifically no `layout: master-detail` and no `card-bordered` against a single-table WPF window; "no repository evidence for this slot" should preserve/abstain, not invent.
4. **query** `Add a status bar …` with a project that already contains a `StatusBar` — **expect** guidance that says extend the existing bar (currently only the generic `impl-reuse-before-new` carries this).

## Tags

`concept-miss`, `requirements-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `preservation-ok`, `skill-helped`
