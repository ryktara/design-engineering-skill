# p3-erp-desktop-dotnet — results

## Task
"Purchase order lines grid for our WPF ERP client; clerks enter 200 lines a day with the keyboard"

Built: a dense purchase-order-lines editing screen (12 columns: item, description, qty, unit, unit price, discount %, tax %, line total, warehouse, requested date, status, notes) with keyboard-first editing, column priority for narrow windows, multi-selection with bulk actions (set status / warehouse, duplicate, delete with undo), per-cell validation, empty / loading / error states, menu bar + command bar + context menu sharing the same commands, and a status bar with counts, error/unsaved indicators, hidden-column notice and totals.

## Stack / platform
Desktop Windows, WPF on .NET 10 (`dotnet new wpf`, no NuGet packages). Project under `project/`: `Themes/Light.xaml` (semantic brushes), `Themes/Typography.xaml` (text roles), `Themes/Controls.xaml` (grid/cell/header/button styles), `Models/PurchaseOrderLine.cs` (INotifyDataErrorInfo validation), `Models/SampleData.cs` (24 lines, two deliberately invalid), `ViewModels/PurchaseOrderLinesViewModel.cs` (states, commands, totals, filter), `Views/PurchaseOrderLinesView.xaml(.cs)` (screen, keyboard handling, column priority), `Views/ColumnPriority.cs` (attached `HideBelow` property), `App.xaml.cs` (normal start plus a `--capture` harness). `dotnet build`: 0 warnings, 0 errors.

**Render mode: native.** The app was launched in `--capture` mode, which renders the window client area with `RenderTargetBitmap` at the real DPI (96) and, with `--scenario keys`, drives the grid with real OS keyboard input (`keybd_event`) while writing a JSON trace after every step. No HTML twin was needed. The title bar is not part of the captures (client area only).

## Inspection verdict
`01-inspect.json`: stack `wpf` KNOWN (from `UseWPF`), platform `desktop`, tokens → `App.xaml`, routing → `Views/`, `ViewModels/`, component dir → `Themes/`. Correct as far as it goes. Missed: the two theme dictionaries themselves (`Themes/Light.xaml`, `Themes/Typography.xaml`) were not listed as token/theme files (only `App.xaml`, which merely merges them); fonts (`Segoe UI Variable` defined as a resource) not detected; the DPI manifest (`PerMonitorV2`) not noted; no MVVM-framework detection (there is none, which is itself a useful KNOWN). "explicit focus handling in 0 files" was right for the baseline.

## Requirements verdict (`02-requirements.json`, exit 4 AMBIGUOUS)
| Field | Value | Verdict |
|---|---|---|
| platform | desktop (KNOWN, project) | right |
| input | keyboard KNOWN, pointer INFERRED | right |
| product | erp (KNOWN) | right |
| stack | wpf (KNOWN) | right |
| density | high (INFERRED from erp) | right |
| mode | create (default) | right |
| screen | [] | **missing** — "lines grid" / "purchase order lines" should map to a data-entry grid / table screen |
| components | [] | **missing** — "grid" was even counted as the only UI term, yet not recorded as a component |
| jobs | [] | **missing** — "clerks enter 200 lines a day" is a batch data-entry job; the vocabulary does not catch it |
| risk | low | **wrong** — financial data entry by keyboard, the matching record (`comp-data-entry-grid`) carries a11y/perf risk high |
| status | AMBIGUOUS | **wrong** — activation shows `ui_score 1.0, non_ui_score 0`; the request is unambiguously UI. It appears to flip to ambiguous when only one UI term is found. SKILL.md defines AMBIGUOUS as conflicting platforms or unclear scope; neither applies |
| missing | brand | right |
| accessibility flags | all true | right |

## Guidance verdict (`03-guidance.md/json`, 6 records: 3 core + 3 guardrails)
| Record | Role | Verdict |
|---|---|---|
| `comp-data-table` | core | relevant (sticky header, selection column + count, inline edit, keyboard nav, virtualised rows, empty state inside the body) |
| `dir-operational-workbench` | core | relevant (4 px grid, tabular figures, hairline borders with real contrast, one accent for selection/primary, mono for IDs) — followed closely |
| `chart-small-multiples` | core | **off-target** — no chart anywhere in the request; composition filled a "chart" slot with lexical score 0.076 |
| `desktop-keyboard-first` | guardrail | relevant (F2, Delete with undo, Ctrl+F, F6, arrow keys, Ctrl/Shift selection, access keys) |
| `search-filter-feedback` | guardrail | partial — the "result count" and "clear" parts were applied to the filter; chips, URL state and the TV clause are irrelevant. It was selected to cover the *states* concern, but it is not a states record; the empty/loading/error guidance actually used came from `comp-data-table` and `layout-table-first` |
| `a11y-keyboard-operable` | guardrail | relevant (Tab does not stop on every cell → `KeyboardNavigation.TabNavigation=Once`, arrows inside the grid, Escape restores) |

Totals: relevant 4 · partial 1 · off-target 1.

**Ranking misses** (present in the base, not selected; verified with `search -k 12`):
- `comp-data-entry-grid` scored 0.694 (second overall) and is the *most* specific record for this task (Enter/Tab movement, F2, Escape, type-to-edit, per-cell validation with a summary, totals row, Enter on the last row adds a row, undo). It was dropped as "redundant: same category as a core pick" (`comp-data-table`). For a data-entry request the more specific record should win, or both should be kept.
- `data-tables-numeric` (right-align, tabular lining figures, one precision per column, totals distinct) — exists, matches the "numeric rule" that `comp-data-table` itself points to, not selected.
- `nav-menu-bar-desktop` — exists (score 0.357 on a status-bar/validation query) but the direction chose `nav-command-palette` (see below).
- `dir-windows-native-tool` omitted as redundant with `dir-operational-workbench`; for a WPF client it is at least as applicable.

**Knowledge gaps** (needed, absent from the base):
- Column priority / progressive column hiding for narrow desktop windows (which columns disappear first, how to tell the user, how to restore). `platforms/desktop.md` covers *pane* collapse order only; `responsive.md` mentions "table columns" for the laptop band without a rule. I designed it ad hoc (Notes → Tax → Disc → Requested → Unit → Warehouse → Status; essentials never hide; status bar says "N columns hidden (View › Columns)").
- Desktop status bar pattern (message · counts · error/unsaved indicators · totals; what to drop first when narrow).
- Grid empty/loading/error state specifics for a data grid (keep the real header visible, put the state in the body, Retry as default button) — only generic sentences exist.
- WPF pitfalls that cost real time and that `stacks/wpf.md` does not mention: (1) `DataGrid` bound to an `ICollectionView` inherits `IsSynchronizedWithCurrentItem`, which re-syncs `SelectedItem` on every `CurrentCell` move and silently collapses multi-selection; (2) Tab out of an editing cell keeps edit mode on the next cell, so a `DataGridComboBoxColumn` then swallows arrow keys; (3) `Validation.HasError` lands on the column's element (TextBlock/TextBox), not the `DataGridCell`, so cell-level error triggers never fire — the error template belongs on the ElementStyle.
- Numeric editing caret behaviour (F2 on a formatted "800.00" appends; select-all or unformatted edit value for quantity fields).

## Direction verdict (`04-direction.md/json`, validation OK)
| Slot | Choice | Fit |
|---|---|---|
| navigation | command palette as primary navigation | **off** — for a WPF ERP screen the platform standard is menu bar + toolbar (`nav-menu-bar-desktop`, which the base has); the palette record itself says it "augments visible navigation, never replaces it". Implemented menu bar + command bar + context menu; no palette |
| layout | table-first working screen | right |
| density | high | right |
| surface | bordered panes | right (borders raised to ≥3:1 after the contrast check) |
| cards | list rows (48–72 dp, tappable, swipe actions) | **does not fit** — mobile wording on a desktop grid; the slot is always filled (direction-invariant) |
| typography | neutral workhorse sans | right; kept the system font per the rule ("if the codebase already uses a system font, keep it"); Cascadia Mono for IDs per the workbench direction |
| color | neutral canvas + one accent | right |
| motion | functional minimal | right (no storyboards) |
| focus | visible focus ring | right (2 px `Brush.Focus.Ring` on the cell, constant border so content does not shift) |
| cta | toolbar with selection-driven commands | right (disabled not hidden, count next to commands, overflow "More ▾" when narrow) |
| imagery | none | right |
| icon | outline set | unused (text glyphs only) |
| metadata | rich | right (View › Columns, mono IDs, status as text, truncation with full value on hover) |

The ledger (KNOWN/INFERRED/MISSING) was accurate. `validation.violations` empty.

## First-render defects (numbered)
1. **Edit-mode trap:** Tab out of an editing cell left the next cell (Unit `ComboBox`) in edit mode; the following Shift+Down / Ctrl+End were consumed by the editor (interaction trace: `editing=true, focusedElement=ComboBox`).
2. **Multi-selection collapsed** to a single row on every current-cell move; ~70 `SelectionChanged` events fired during load (`IsSynchronizedWithCurrentItem` default with an `ICollectionView`). Native Shift+arrow could never extend the selection.
3. Status bar overflow at 1100×700 and 820×600: the hidden-columns message pushed the totals off the right edge ("Total 8" clipped).
4. 820×600: the 260 px filter box overlapped the Save button; the command bar had no overflow behaviour.
5. Stray default "select all" triangle glyph in the row-header corner.
6. Validation rendered as WPF's default red box adorner; the designed tint + error bar never appeared and there was no message tooltip (trigger on the cell, error on the element).
7. Description (essential) truncated at 1440 while Notes (least important) had 1.4* width.
8. Loading state showed a blank grey header strip with no column captions (grid hidden while loading).
9. Redundant status text "Loaded 24 lines · 24 lines".
10. Contrast (computed with `tokens.py contrast`): pane/control border `#B9BFC8` 1.85:1 (< 3:1 non-text), filter placeholder `#9AA3AF` 2.55:1, warning caption `#9A6700` on the header strip 4.26:1 (< 4.5).

## Final defects (remaining)
1. F2 on a formatted numeric cell places the caret after "800.00"; appending digits yields 800.0012. Excel-like but confusing with fixed two decimals; a select-all-on-F2 or unformatted edit value would be better.
2. The empty and loading states show the column header without the 48 px row-header column (no rows → no row headers), so the Item column sits 48 px further left than in the ready state.
3. Stock WPF scrollbar, not on the theme.
4. Only a Light theme dictionary; Dark / High-contrast dictionaries (required by `stacks/wpf.md`) not created and not verified.
5. ComboBox columns (Unit, Warehouse, Status) have no validation adorner (values are list-constrained, but the model can still flag them).
6. Column widths/order/visibility are not persisted per user (guidance asked for it); "Reset column layout" exists but nothing is saved.
Not verified: Narrator/NVDA, 150/200 % DPI, high contrast, mouse and context-menu paths.

## Iterations
1. **Fix pass 1** (defects 1, 3–10 except 2): Tab-while-editing handler that commits and moves without re-entering edit mode; status bar left segment made flexible with totals detail collapsing below 1000 px; filter shrinks to 180 px and Set status / Warehouse fold into a "More ▾" overflow below 980 px; select-all corner restyled ("#"); validation moved to a `Validation.ErrorTemplate` on the cell element (tint + 2 px bar + tooltip); Description 3*, Notes 1*; loading/empty overlays cover only the body so the real header stays; status message "Ready".
2. **Fix pass 2:** `ShowGrid` corrected so the header really shows while loading; diagnostic scenario for selection → found the `IsSynchronizedWithCurrentItem` collapse → set it to false (also removes the load-time selection churn).
3. **Fix pass 3:** Shift+Down still failed → traced to the harness: `keybd_event` without `KEYEVENTF_EXTENDEDKEY` sends numpad arrows and Windows injects a Shift release around Shift+numpad. Fixed the harness, removed the now-redundant explicit range-selection handler (native DataGrid behaviour works once the sync is off), applied the three contrast fixes (`Border.Strong` → `#7F8894` 3.59:1, `Feedback.Warning` → `#805400` 5.77:1, placeholder → secondary text 5.98:1).
4. **Micro pass:** hover tooltip with the full value on trimmed cells; re-captured 1440×900.

## Interaction test summary (`05-interaction.json`, native, real OS keyboard input)
18/18 checks pass on the final build: arrow navigation in both axes; F2 edits; Enter commits and moves down (previous row dirty, totals updated); Tab right / Shift+Tab left without entering edit mode; type-to-edit; Escape cancels; qty 0 + Enter marks the row (`Quantity must be greater than 0.`) and the status-bar error count goes 2→3; Shift+Down ×2 selects 3 rows; Ctrl+End scrolls (offset 3) with the header at the same y (115.2); Enter on the last row adds line 250 and focuses it; focus ring present in every snapshot; Qty / Unit price / Disc % / Tax % / Line total right-aligned with tabular numerals, all text columns left; F6 cycles filter → command bar → grid; Ctrl+F focuses the filter; column priority 0 / 4 / 7 hidden at 1440 / 1100 / 820 with the five essentials always visible. First render: 2 of the same checks failed (edit-mode trap, selection extension).

## Time spent (rough)
About 2.5 h: 15 min skill steps and reading references, 60 min implementation, 45 min render/interaction harness and debugging (the selection issue took the longest), 20 min fixes and re-renders, 10 min write-up.

## Failure taxonomy tags
`requirements-miss`, `vocabulary-gap`, `ranking-miss`, `knowledge-gap`, `direction-invariant`, `render-defect-fixed`, `render-defect-remaining`, `skill-helped`

Where the skill helped: `layout-table-first` + `comp-data-table` + `dir-operational-workbench` + `desktop-keyboard-first` gave the structure (toolbar with selection count, filter row, table filling the height, quiet header strip, tabular figures, one accent, disabled-not-hidden commands, F2/Del-with-undo/Ctrl+F/F6) before any visual decision; `stacks/wpf.md` set the token/`DynamicResource`, text-role and virtualisation conventions the project follows; `tokens.py contrast` caught three failing pairs I would otherwise have shipped. Where it did not: the most task-specific record was pruned, the direction proposed a command palette and mobile list-row cards for a WPF grid, and column priority, status bar and the three WPF DataGrid pitfalls had to be worked out without it.
