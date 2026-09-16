# p6-20 — WinUI 3 ERP, stock adjustments grid

**Task sentence (verbatim):** "The stock adjustments grid shows 3,000 rows and scrolling is janky."

**Project:** `research/phase3-projects/p3-winui-erp-audit/project` · WinUI 3 (WindowsAppSDK 1.7) + CommunityToolkit DataGrid 7.1.2 + CommunityToolkit.Mvvm · desktop · existing UI (the page was already refactored by an earlier design-engineering audit) · no new screen.

**Build hash:** start `ea8eed72…d9947` = end `ea8eed72…d9947` = the frozen c3 hash. OK.

**Render mode:** `html-twin` (`project/render/twin.html`, new) at 1280×800. `dotnet build` fails in this environment with `XamlCompiler.exe exited with code 1` — I verified on an untouched copy of the project that the **pristine** tree fails identically, so this is a pre-existing tooling limit, not a defect I introduced. The XAML was XML-parsed; no compile verification was possible.

---

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | `NavigationView PaneDisplayMode="Auto"` in MainWindow.xaml | yes |
| theme | dual-theme | INFERRED | `ThemeDictionaries` Light + Dark in App.xaml | yes |
| surfaces | bordered-flat | INFERRED | table pane = 1 px `CardStrokeColorDefaultBrush` border, no shadow | yes |
| radius | unknown | UNKNOWN | `OverlayCornerRadius` / `ControlCornerRadius` theme resources are used explicitly | partial — the values are system resources, but the code does state a corner language |
| spacing | 4 | INFERRED | 16/12/8/4/2 throughout; 36 epx rows | yes |
| typography | unknown | UNKNOWN | no font family is declared (WinUI type ramp styles only) — `TitleTextBlockStyle`, `BodyTextBlockStyle`, `CaptionTextBlockStyle`, `Typography.NumeralAlignment=Tabular` | partial — "no font family" is literally true, but the page does have a type system and tabular figures, and `features.tabular_numerals` was reported `false` when `Typography.NumeralAlignment="Tabular"` is set in the page |
| components | winui3, community-toolkit | KNOWN | exactly right | yes |

Two `partial`s, both in the same direction: the detector reads only font-family declarations and hex literals, so a page that gets its type and radius entirely from platform theme resources reads as UNKNOWN. On WinUI that is the *correct* way to write the page.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Value | Verdict |
|---|---|---|
| platform | `desktop`, from project inspection, `platform_evidence: []` | correct (project-derived; the sentence itself has no platform word) |
| artifact_state | `existing` | correct |
| operations | `diagnose`, `modify` | correct |
| problem_domain | `interaction` | acceptable — the honest label is *performance*; there is no perf domain and `interaction` is the nearest |
| change_scope | `screen` | correct |
| mode | `audit` + `refactor` (sentence has no mode word) | correct |
| scope.kind | `in-scope` | correct |
| change_budget | `moderate` | correct |
| intent.preserve | `[]` | miss — an existing, already-audited screen should carry navigation/theme/typography into `preserve`; the direction step preserves them anyway, so no harm |
| density / screen_subtype | `high` / `data-grid` | correct and useful |
| project_context | carried through verbatim | correct |

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Bundle: 5 records (core 2 + guardrails 3), no OPTIONAL layer, ≈1141 tokens.

| Record | Layer | Verdict | Category | Why |
|---|---|---|---|---|
| `comp-data-table` | core | relevant | — | contains the one clause that matters ("virtualised rows"), plus fixed row height by density token and persisted column state |
| `comp-data-entry-grid` | core | off-target | wrong-screen | spreadsheet batch-entry guidance (F2/F4 editors, paste, totals row, row-add-on-Enter) for a grid declared `IsReadOnly="True"`; following it would add per-cell editors, i.e. more per-row cost, on a screen whose complaint is scroll cost |
| `grid-single-tab-stop` | guardrail | relevant | — | "a table with N rows must never produce N Tab stops per action column" is exactly the defect at 3,000 rows; it drove the real change I shipped |
| `data-exceptions-first` | guardrail | partial | generic | already fully implemented on this page (status column = glyph + word + theme brush, pending count in the header summary); adds nothing for jank |
| `table-column-disambiguation` | guardrail | off-target | wrong-screen | "Editable grids…"; the grid is read-only, and the numeric formatting it asks for is already in place |
| *(bundle-level)* | — | — | missing-critical | `perf.layout_shift` (stable row geometry while scrolling) was pre-registered critical and is absent from the bundle |

Counts: relevant 2 · partial 1 · off-target 2.

**Real concept recall**

Delivered (union over selected records): `table.selection_bulk`, `table.inline_edit`, `table.virtualization`, `table.tabular_figures`, `data.pagination_strategy`, `interaction.selection_visible`, `interaction.keyboard_navigation`, `interaction.focus_visible`, `data.exception_first`, `a11y.color_not_only`, `env.glanceable_status`, `feedback.validation_errors`.

| Expected id | Delivered? | Earliest wrong layer |
|---|---|---|
| `table.virtualization` (critical) | yes | — (but only as one sub-clause inside `comp-data-table`; see below) |
| `perf.layout_shift` (critical) | no | expected-concepts — never demanded; absent from `concept_trace` and from `not_surfaced` |
| `perf.focus_latency` | no | expected-concepts — never demanded |
| `data.pagination_strategy` | yes | — |
| `desktop.persist_workspace` | no | bundle-selection — `not_surfaced` names `desktop-state-persistence` as an existing candidate |
| `state.loading_empty_error` | no | expected-concepts — never demanded |

recall **2/6 = 0.33** · critical recall **1/2 = 0.50**.

**The headline miss.** The knowledge base *does* contain the record written for this exact sentence — `web-virtualize-long-lists` ("Virtualise long lists and tables"; platform `["web","desktop","mobile","tv"]`, so it is not platform-filtered; `use_when: lists/tables beyond a few hundred rows`). `advise.py search "virtualize long list scroll performance jank recycle rows"` ranks it first at 0.593. For the actual task sentence it never appears: not in `core`, not in `guardrails`, not in `rejected` (which lists only platform filtering), not in `omitted`. The sentence says "3,000 rows" and "janky" and never says "virtualise" or "long list", and `table.virtualization` was already nominally satisfied by `comp-data-table`, so nothing demanded it. Earliest wrong layer: **candidate-retrieval**. This is the single most valuable finding in this task: the bundle for a scroll-performance complaint contains inline editing, exceptions-first and column-unit disambiguation, and omits the one performance record in the base.

`status` was CONFIDENT, not PARTIAL_SCOPE, so no design/engineering split note to judge.

## 4. Direction verdict (`04-direction.md`)

12 of 14 slots `preserved` with correct reasons. Two slots `new`:

- **layout → `layout-table-first`** — `new` only because the detector found no layout evidence; the page already *is* table-first, and the slot text carries the useful line "Virtualise beyond a few hundred rows". Unjustified by the task, harmless in effect.
- **cards → `card-list-row`** — unjustified and wrong here: "row height from the density token (48–72 dp), whole row tappable, swipe actions". Applying it to a 36 epx desktop DataGrid would nearly double row height and cut visible rows by a third on the very screen the task says is too heavy. Ignored.

`unjustified_direction_slots: 2`. `preservation` metrics and `validation: OK` are right. The fingerprint (`grid_behavior: virtualized`, `content_density: high`, `corner_language: sharp`) matches the screen.

## 5. Implementation

Files changed (originals in `before/`):
- `ViewModels/StockAdjustmentsViewModel.cs`
- `Views/StockAdjustmentsPage.xaml`
- `Views/StockAdjustmentsPage.xaml.cs`
- `ViewModels/BulkObservableCollection.cs` *(new)*
- `render/twin.html` *(new, review instrument)*

What changed, and why each is a jank cause:

1. **The data set is now 3,000 rows.** `Load()` seeded 8 rows; the task describes the screen at its real size. The 8 hand-written rows are kept and a deterministic 2,992-row history is generated, so every change below is reviewed at the size the complaint is about.
2. **One `Reset` instead of 1 + n notifications.** `FilteredItems` was an `ObservableCollection` refilled with `Clear()` + 3,000 × `Add()`. Each `Add` makes the DataGrid re-measure and re-realise; this ran on every keystroke. New `BulkObservableCollection<T>.Reset(items)` raises a single `NotifyCollectionChangedAction.Reset`.
3. **Debounced text filters.** `SearchText` / `LocationFilter` bind with `UpdateSourceTrigger=PropertyChanged`; each keystroke re-filtered and re-sorted 3,000 rows synchronously on the UI thread. Coalesced to one pass 180 ms after the last keystroke via `DispatcherQueueTimer` (falls back to synchronous when there is no dispatcher).
4. **Typed sort comparisons.** `ApplySort` used `Func<StockAdjustment, object>`, boxing a `decimal` or enum on every comparison — ~35k boxes per sort at 3,000 rows. Replaced with `Comparison<T>` and an in-place `List.Sort`.
5. **Numeric template columns → text columns.** `Before`, `After`, `Value (EUR)` were `DataGridTemplateColumn`s: a ContentPresenter plus an inflated DataTemplate per cell, per realised row. They are now `DataGridTextColumn`s with the same converter and `ElementStyle="{StaticResource NumericCellText}"` — identical output (right-aligned, tabular figures, U+2212 minus), one TextBlock per cell. `Change` stays a template column because it needs the sign-driven brush and weight; `Status` stays a template column because it needs glyph + text + UIA name.
6. **Three row-action buttons → one row-actions button.** This is the change `grid-single-tab-stop` asks for, and it is also a realisation-cost change: 3,000 rows × 3 buttons was ~9,000 focusable controls and three visual subtrees per realised row, plus three Tab stops per row. The button now selects its row and opens the **existing** `DataGrid.ContextFlyout` MenuFlyout (named `RowActionsFlyout`) — reuse, not a new flyout per row. Edit/Approve/Reject remain on the command bar, on Shift+F10, and on their accelerators; the F1 shortcut list is unchanged and still correct. The Actions column narrows 108 → 72 epx, which gives the Description column back the width the before-render shows it losing.
7. **Virtualisation contract written down in the XAML.** The DataGrid sits in a `Height="*"` row with a fixed `RowHeight="36"`; a comment states that it must never be wrapped in a ScrollViewer or an `Auto` row, which is the standard way this regresses to realising all rows.

Kept intact: navigation, theme resources, type ramp, spacing grid, all accelerators and access keys, the F6 region cycling, the live regions and `RaiseAutomationEvent(LiveRegionChanged)`, the persisted "Created by" column, the empty/loading states, the InfoBar re-announce trick, sort-in-viewmodel.

**Guidance used:** `grid-single-tab-stop` (drove change 6), `comp-data-table` (virtualised rows, fixed row height by density token — changes 5/7), the layout-slot line "Virtualise beyond a few hundred rows".
**Guidance ignored:** `comp-data-entry-grid` and `table-column-disambiguation` (the grid is `IsReadOnly="True"`; both describe editable grids, and adding per-cell editors would make the reported problem worse); `data-exceptions-first` (already implemented); direction slot `cards → card-list-row` (48–72 dp rows contradict a 36 epx desktop grid and the task).

**Not done, deliberately:** no pagination / load-more. `data.pagination_strategy` was delivered, but this is an approval queue with sort and filter; with real virtualisation the 3,000 rows scroll, and paging would remove the ability to sort across the whole set. Stated here rather than silently dropped.

**Process guidance check.** No. SKILL.md §2 / §7 were enough — reuse-before-new produced change 6 (reuse the existing ContextFlyout instead of a per-row flyout) and render-verify produced the two twin iterations, without `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` being in the bundle. `process_records_needed: false`.

## 6. Render and defects

`render/first-*.png` and `render/final-*.png`, 1280×800: `grid-top` (scrollTop 0), `grid-scrolled` (scrollTop 54,000 = row 1,500), `before-variant` (the pre-change screen, all rows realised, 3 buttons per row). Playwright reports 24 and 30 `.row` elements in the DOM for the two virtualised shots against 3,000 for the before variant.

First-render defects — **all five are twin-fidelity defects; none are in the shipped XAML or C#**:

| # | Type | Defect |
|---|---|---|
| 1 | implementation-bug | the twin's LCG lost its low bits to `% n`; 3,000 rows produced 6 Pending and no Rejected rows, so the status colours could not be reviewed |
| 2 | implementation-bug | the twin generated ids from ADJ-10421 downwards, colliding with the eight hand-written rows `Load()` keeps |
| 3 | existing-system-mismatch | status text rendered "Pending approval"; `StatusToPresentationConverter` returns the short "Pending" (the long form is the UIA name only), and the long form truncated in the 108 epx column |
| 4 | existing-system-mismatch | hyphen-minus in Change / Value; the converter emits U+2212 |
| 5 | visual | the instrumentation badge covered the last grid row |

Totals — first: visual 1, interaction 0, accessibility 0, platform 0, existing-system-mismatch 2, implementation-bug 2 (**5**). Final: **0**. **Iterations: 2.**

No defect the guidance had warned about was shipped.

## 7. Preservation

Navigation, theme, typography, spacing, focus handling, accessibility semantics: preserved. Component reuse: yes (existing converters, existing MenuFlyout, existing styles; one new 20-line collection type). One structural change — the row-actions column — justified by the task (per-row realisation cost) and required by a critical guardrail. `unjustified_structural_change: 0`. **preservation-ok.**

## 8. Skill-miss routing (one layer per miss, earliest)

| Miss | Layer |
|---|---|
| `web-virtualize-long-lists` not surfaced for a sentence about scroll jank, though it is platform-compatible and top-ranked for a virtualisation-worded query | candidate-retrieval |
| `perf.layout_shift`, `perf.focus_latency`, `state.loading_empty_error` never demanded for a performance complaint | expected-concepts |
| `desktop.persist_workspace` demanded, candidate `desktop-state-persistence` existed, dropped | bundle-selection |
| `comp-data-entry-grid` / `table-column-disambiguation` selected for a `IsReadOnly="True"` grid | candidate-compatibility |
| direction slot `cards → card-list-row` (48–72 dp rows) on a 36 epx desktop grid | direction |
| `intent.preserve` empty on an existing, already-audited screen | requirements |

## 9. Regressions to propose

1. `"The stock adjustments grid shows 3,000 rows and scrolling is janky."` → expect `web-virtualize-long-lists` in the bundle (core or guardrail), not only the virtualisation sub-clause of `comp-data-table`.
2. `"the invoice list stutters when I scroll through 8,000 lines"` → expect at least one record whose subject is list/table performance; expect `perf.layout_shift` among the demanded concepts when the complaint is about scrolling.
3. `"the read-only approvals grid is slow"` with a project whose grid is `IsReadOnly` → expect `comp-data-entry-grid` and `table-column-disambiguation` **not** selected (both are editable-grid records).
4. `inspect_project.py` on a WinUI page that sets `Typography.NumeralAlignment="Tabular"` → expect `typography.features.tabular_numerals: true`.

## 10. Tags

`concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `requirements-miss`, `render-defect-fixed`, `tooling-limit`, `skill-helped`, `preservation-ok`.

**Skill effect: helped.** `grid-single-tab-stop` is a critical guardrail that named the row-actions defect precisely and produced the change that is simultaneously the accessibility fix and the largest per-row cost reduction; I would plausibly have left three buttons per row and fixed only the collection and sort paths. That verdict is narrow: for the literal request — scroll jank on 3,000 rows — the bundle was mostly about something else, and the one record in the base written for this problem never surfaced.
