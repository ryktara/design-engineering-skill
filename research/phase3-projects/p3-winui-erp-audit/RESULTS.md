# p3-winui-erp-audit — results

## Task

"Warehouse clerks say our WinUI stock adjustments page is confusing and they keep missing rows; the screen reader reads the status column as just text"

Audit + refactor of a deliberately flawed page written into a copy of the `winui-erp` fixture. Baseline kept at `baseline/StockAdjustmentsPage.before.xaml(.cs)`. Flaws planted: `ListView` used as a grid with a separate header `Grid`; row actions revealed on `PointerEntered` only, `IsTabStop=False`, glyph-only, unnamed; no `KeyboardAccelerator`/`AccessKey`; status = 8 px coloured `Ellipse` only; filter `TextBox`/`ComboBox` with `PlaceholderText` as the only label; no empty/loading state; 4 px spacing, 24 px rows, 12 px text; quantity columns aligned left / centre / right / left; literal `#FFFFFF`/`#F3F3F3` brushes; `UseSystemFocusVisuals=False`.

## Stack / platform

Desktop Windows, WinUI 3 (Windows App SDK 1.7, CommunityToolkit.Mvvm, Toolkit DataGrid), XAML + C#. Project: `project/` (App, MainWindow with NavigationView, Models, ViewModels, Views, Converters).

**Render mode: `html-twin` + static review.** `dotnet build` (SDK 10.0.300) failed twice for two different reasons:
1. As shipped, the fixture references `CommunityToolkit.WinUI.Controls.DataGrid 8.2.250402`, which does not exist on nuget.org (NU1101). The 8.x toolkit never published a DataGrid under that id; the real package is `CommunityToolkit.WinUI.UI.Controls.DataGrid` (7.x). **Fixture defect.** I corrected the id in my copy only.
2. With that removed (diagnostic copy in scratchpad), C# compiled but PRI generation needs `Microsoft.Build.Packaging.Pri.Tasks.dll` from the Visual Studio AppxPackage tooling (MSB4062) — the Windows App SDK build workload is not installed. **Tooling limit.** So the XAML was reviewed statically against the WinUI stack file and mirrored 1:1 in `render/before.html` / `render/after.html` at 1440×900 (320 px NavigationView + 1088 px content, the WinUI "large" class).

## Inspection verdict (`01-inspect.json`)

| Signal | Reported | Verdict |
|---|---|---|
| stack_groups `winui`, ui_libraries `winui3`, `community-toolkit` | KNOWN | right |
| tokens `App.xaml` | KNOWN | right (theme dictionaries + accent override) |
| product_hints `erp` | | right |
| routing `Views/`, `ViewModels/` | | right but shallow: `NavigationView` + `Frame` in MainWindow.xaml not reported as the navigation convention |
| platforms `desktop`, **`tv`** | KNOWN | **wrong**. `DPAD_RE` in `inspect_project.py:88` ends with `|isTV` and is compiled with `re.I`; `ListView` contains `istv`, so every WinUI/WPF/UWP/Avalonia file with a `ListView` is reported as "DPAD / remote key handling found in source". Verified: all 9 hits in this project are `ListView`/`ListViewItem`. This single false positive poisoned platform, input, density, environment, guidance and direction downstream (see below). |
| focus_handling "explicit focus handling in 2 files" | | right (UseSystemFocusVisuals, IsTabStop) |
| accessibility "a11y attributes present in 1 files" | | right (OrdersPage AutomationProperties) |
| fonts, icons | empty | missed: Segoe Fluent Icons glyphs (`&#xE710;` …) and `FontFamily="Segoe Fluent Icons"` are in the page |
| hover-only handlers (`PointerEntered/Exited`) | not reported | missed; an audit-relevant signal for desktop |
| tests, i18n, breakpoints | empty | right (none) |

Because of the TV false positive I also produced `01-inspect-corrected.json` (tv/remote removed by hand) and re-ran requirements/guidance/direction as a **control** (`02b-`, `03b-`, `04b-`). Verdicts below are for the protocol run first, control in brackets.

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)

| Field | Value | Verdict |
|---|---|---|
| mode | `accessibility`, `audit` | **right** — screen reader → accessibility; "confusing, keep missing" → audit. Not classified as create. |
| platform | `desktop`, `tv` | `desktop` right; `tv` **wrong** (inspection false positive) |
| input | `keyboard`, `pointer`, `remote` | `remote` **wrong**; keyboard/pointer right |
| product | `erp` | right (from "warehouse") |
| stack | `winui` | right |
| screen / screen_subtype | `[]` | **missing** — "page" + "rows" + "status column" should yield a table/list working screen |
| components | `[]` | **missing** — status column, rows → data table, status badge |
| density | `medium` | **wrong**: "capped for touch/remote platform". Control run: `high`, correct for desktop ERP |
| environment | `large-display`, `shared-device` | **wrong**, TV-derived ("a TV is normally a shared household device"). Control: `[]` |
| jobs | `[]` | missing but not derivable from the sentence; acceptable |
| problems | `accessibility`, `interaction` | right |
| primary_jobs | `accessibility` | right |
| constraints.preserve_existing_system | true | right (audit) |
| accessibility flags | keyboard, screen_reader, focus, reduced_motion, contrast all true | right |
| negative_constraints | `[]` | right |
| status | CONFIDENT | **wrong** — desktop + tv from the same project is a platform conflict; the contract documents exit 4 for conflicting platforms but did not trigger. |

Requirements errors: `platform=tv`, `input=remote`, `density=medium`, `environment=*`, `screen=[]`, `components=[]`, `status=CONFIDENT despite platform conflict`.

## Guidance verdict (`03-guidance.md` / `.json`, bundle 8 = core 2 + guardrails 6)

| Record | Role | Verdict | Why |
|---|---|---|---|
| `comp-data-table` | core | **relevant** | Names the exact defect in its winui note: "avoid ListView with a fake header row"; row actions visible on focus as well as hover; empty state inside the table body; keyboard grid navigation; points to the numeric rule. This one record drove most of the refactor. |
| `comp-tv-rail` | core | **off-target** | TV rails for a desktop ERP grid; consequence of the `ListView`→TV false positive |
| `a11y-nontext-contrast` | guardrail | relevant | Status glyphs, focus ring, card border all measured ≥3:1 |
| `tv-safe-area` | guardrail | **off-target** | overscan margins |
| `a11y-live-status` | guardrail | relevant | Drove `InfoBar` + result summary with `AutomationProperties.LiveSetting=Polite` |
| `web-virtualize-long-lists` | guardrail | partial | Correct for a grid (DataGrid virtualises), but selected "for focus latency and catalog virtualization on TV" |
| `a11y-labels-names` | guardrail | relevant | "Visible label for inputs (not placeholder-only) … AutomationProperties.Name for icon-only controls" — two planted defects |
| `desktop-keyboard-first` | guardrail | relevant | Accelerators in tooltips, F2, Ctrl+F, F5, access keys |

Count: relevant 5, partial 1, off-target 2. "uncovered required concepts: interaction.dpad_reachability, tv.ten_foot_typography" — both artefacts of the false positive.

[Control bundle (6): `comp-data-table` relevant; `comp-form` partial (filter bar is a form of sorts and its winui note "TextBox Header + PlaceholderText" is the exact fix for placeholder-only labels); `a11y-nontext-contrast`, `desktop-keyboard-first`, `a11y-labels-names` relevant; `states-persistence-and-session` off-target (saving/session-expiry states chosen for the "states" concern when the page needed the empty/loading rule).]

### Ranking misses (present in the base, not in either bundle)

Checked with `advise.py search "<task>" -k 12 --explain` (`03-search-k12.md`) and targeted queries:

- `anti-hover-only-actions` — rank 2 in the k=12 search for the task sentence (score 0.42), yet not in the guidance bundle. The single most relevant record for "they keep missing rows" with hover-only actions.
- `a11y-color-not-only` — rank 9 at k=12; not in the bundle. The request describes exactly a colour-only status.
- `data-tables-numeric` — not in the k=12 list at all; found only with a targeted query ("numeric columns right aligned tabular figures", score 0.83). `comp-data-table` says "see numeric rule" but the bundle did not pull it.
- `anti-placeholder-labels` — not in k=12; found by targeted query (0.75).
- `layout-states-empty-loading-error` / `comp-empty-state` / `anti-no-states` — not in k=12; the "states" concern was only *recommended*, and the control run satisfied it with the wrong states record.
- `metadata-inline-badges` / `metadata-rich` ("status as text+colour") — rank 1 and 3 in search, absent from guidance (they did appear as direction slots).

### Knowledge gaps (absent from the base)

- Single Tab stop for a grid with per-row buttons (roving tabindex; arrows reach the buttons). `comp-data-table` covers arrow navigation but nothing says row-action buttons must leave the Tab sequence; my first render put 24 buttons in the Tab order and no record would have caught it.
- Column-width budget: fitting the default column set into the minimum/target window without horizontal scroll that hides the actions column; which columns to hide by default and expose via a persisted column chooser. Records mention "column visibility persisted" but not the budget decision.
- WinUI recipes for the specific fixes: `Typography.NumeralAlignment="Tabular"` for tabular figures, an icon+text status cell with one `AutomationProperties.Name` and the glyph set to `AccessibilityView=Raw`, `DataGridColumn.Visibility` for the default set. The stack file lists `AutomationProperties.Name` generally.
- Short visible label vs. full accessible name ("Pending" / "Status: Pending approval") when a column is narrow.

## Direction verdict (`04-direction.md/json`, exit 3)

Protocol run: `layout-rails`, `color-dominant-brand`, `motion-focus-scale`, `cta-focus-selects` are TV-driven and wrong for a desktop ERP; `density-medium` wrong; `nav-breadcrumb-tree` partial (repo uses `NavigationView` left rail — `nav-left-rail` was the 2nd alternative; the inspector does not surface NavigationView so the slot cannot reconcile); `surface-bordered-panes`, `card-list-row`, `typography-system-native`, `focus-ring-standard`, `imagery-none`, `icon-outline-system`, `metadata-inline-badges` fit. **Validation: VIOLATIONS** ("tv/remote: focus strategy 'ring' is not a 10-foot focus treatment") — the validator correctly refused the mixed direction, which is the right behaviour given bad inputs.

[Control run, exit 0, **Validation OK**: `layout-table-first`, `density-high` ("4 px base grid, 32 px row height in tables, 13–14 px body … Numeric columns right-aligned with tabular figures"), `surface-bordered-panes`, `typography-neutral-sans` ("If the codebase already uses a system font, keep it"), `color-neutral-accent`, `motion-functional-minimal`, `focus-ring-standard`, `cta-toolbar-commands` (winui: "CommandBar with AppBarButton + KeyboardAccelerator; IsEnabled bound to selection"), `imagery-none`, `icon-outline-system`, `metadata-rich` ("status as text+colour"). All slots fit the platform; this is the direction I implemented. Only `nav-breadcrumb-tree` remained a mismatch with the repo's NavigationView in both runs — the navigation slot is invariant to the repository's actual shell.]

## Implementation (static review of `project/Views/StockAdjustmentsPage.xaml`)

- `CommandBar` with `AppBarButton` (Label, `AccessKey`, `KeyboardAccelerator` Ctrl+N / Ctrl+Shift+A / Ctrl+Shift+R / F5, tooltips show the shortcut), Approve/Reject `IsEnabled` bound to selection (disabled, not hidden).
- Filter row: `TextBox Header="Search"`, `Header="Location"`, `ComboBox Header="Status"`; placeholders demoted to format hints; Ctrl+F focuses search; "Clear filters".
- Toolkit `DataGrid` (`AutoGenerateColumns=False`, `RowHeight=36`, `ColumnHeaderHeight=36`, sortable/resizable/reorderable, `ContextFlyout` mirroring the commands, F2 edits) replaces the ListView + fake header.
- Status column template: `FontIcon` + `TextBlock`, brushes from `SystemFillColorSuccess/Caution/Critical` theme resources, one `AutomationProperties.Name="Status: Pending approval"` on the cell, glyph `AccessibilityView=Raw`.
- Numeric columns: `NumericCellText` style (right-aligned, `Typography.NumeralAlignment=Tabular`, one precision per column, true minus sign, explicit `+` on Change and Value, unit in the header "Value (EUR)").
- Row actions: always visible 28 epx buttons, `AutomationProperties.Name="Approve ADJ-10421"`, tooltips with shortcuts, disabled for Posted/Rejected rows; mirrored in the context menu and command bar.
- Empty state (heading, one sentence, one action; copy differs for "no data" vs "no match"), `ProgressRing` loading, `InfoBar` feedback with `LiveSetting=Polite`; result summary line also polite.
- Spacing 16/12/8 on the 4 epx grid; `ThemeResource` brushes only; system focus visuals kept; selection preserved by key on refresh (view model).
- Not verified (toolchain): XAML compile, Narrator pass, Dark/High Contrast rendering, DPI 150/200 %, 800×600 window, `DataGrid` sort indicator behaviour with template columns.

## First-render defects (after-twin, `render/first-after*.png`, `05-interaction.json` first pass)

1. Column budget: fixed widths summed to ~1460 px vs 1086 px available → horizontal scroll; the **Actions column was off-screen at rest** and the focus screenshot showed Status clipped on the left. (Same widths in the XAML.)
2. "Pending approval" truncated with an ellipsis in the 150 px status column.
3. Empty state collapsed to ~40 px: the hidden `InfoBar` (`display:none`) let the table card fall into the `auto` grid row instead of the `1fr` row.
4. Column-header sort buttons had **no visible focus** (`all:unset` removed the outline) — 11 tab stops without a ring.
5. All 24 row-action buttons were Tab stops (Tab order 39 stops before leaving the page) instead of one grid stop with arrow-key access.
6. "By" column truncated ("j.lindqvi") as a consequence of 1.
7. (Test harness) traversal stopped early on the before-twin because unnamed inputs collided in the de-duplication key.

Before-twin (baseline, all intentional, confirmed by the test): 0/24 row actions visible without hover, 0 named; status 0/8 with text or icon; numerics 1/4 right-aligned, 0 tabular; 0/3 filter inputs labelled; 0/2 toolbar buttons named; no empty state; row focus visual removed; placeholder #8A8A8A on #FBFBFB = 3.34:1; orange status dot on white = 1.97:1 (non-text 3:1 fails).

## Final defects (after fix, `render/final-after*.png`)

- "Created by" is hidden by default (`Visibility=Collapsed`) to fit the budget; there is no column chooser yet, so users cannot show it. Documented trade-off.
- Row-action buttons are 28 epx (≥24 epx desktop floor, below the 32 epx WinUI control height) to fit three per row in 108 px.
- Light theme only in the twin; Dark/High Contrast, DPI scaling and Narrator remain unverified.
- Twin shows 8 rows in a tall card (sample data); real data relies on DataGrid virtualisation.

## Iterations

1. First render + interaction test → defects 1–7 above.
2. Fix: 8 px cell padding, narrower columns (108/96/112/*/80/96/76/76/76/88/108), "Created by" out of the default set, "Pending" short label with full UIA name, header focus ring restored, roving tabindex (one grid Tab stop; Right/Left to buttons, Up from row 1 to headers), infobar+card wrapped so the card owns the `1fr` row, test de-dup by element identity, new checks (header reachable, horizontal overflow, status truncation). Same width/padding/naming changes applied to the XAML, plus `RowActionNameConverter` replacing an overloaded converter. Re-render → all checks pass.

Count: 2 renders, 1 fix pass.

## Interaction test summary (`05-interaction.json`, final)

| Check | before | after |
|---|---|---|
| Row actions visible without hover / named / min target | 0/24, 0, 20 px | 24/24, 24, 28 px |
| Row action reached by keyboard (row → ArrowRight) | no (focus stays on UL) | yes → `BUTTON: Edit ADJ-10420` |
| Column header reached by keyboard with visible ring | no | yes (`Status`) |
| Tab stops to cross the page | 10 (list is one stop, rows unreachable individually) | 12 (grid is one stop) |
| Focus visible on every Tab stop | 10/10 (but rows have none) | 12/12 |
| Status text + icon + accessible name | 0/8 | 8/8 (`Status: Pending approval`) |
| Numeric cells right-aligned / tabular-nums | 1/4, 0/4 | 4/4, 4/4 |
| Filter inputs with visible label | 0/3 | 3/3 |
| Toolbar buttons named | 0/2 | 4/4 |
| Empty state present with heading + action | no | yes |
| Horizontal overflow at 1440×900 | none (content just clipped) | none (1086/1086) |
| Status truncation | n/a | 0/8 |
| Reduced motion respected | n/a (no motion) | transitions 0 s under `reduce` |
| Contrast (measured) | placeholder 3.34:1 fail; orange dot 1.97:1 fail | text 17.2, secondary 6.19, caution 5.25, success 5.44, critical 5.66, accent 5.38 (all AA) |

Tokens: no separate tokens.json was defined (values are WinUI theme resources), so `tokens.py check` was not run; ratios were computed with `tokens.py contrast`.

## Reproducibility note

All `advise.py`/`inspect_project.py` runs in this case were made at 00:30–00:32 (09-09). During the case, `data/lexicon.json`, `data/rules.jsonl`, `scripts/de_core.py`, `evals/run_evals.py` and `docs/USAGE.md` under `design-engineering/` changed on disk (00:33–00:37) from outside this session; nothing under `design-engineering/` was modified by this case. Re-running the skill commands now may give different bundles/rankings than those recorded in `02-`…`04b-`.

## Time spent (rough)

~1 h 45 min: project + flawed page 20 min, skill runs and control run 15 min, build attempts 10 min (background), refactor XAML/VM/converters 25 min, twins + Playwright 20 min, fix pass 10 min, write-up 15 min.

## Failure taxonomy tags

`requirements-miss` (tv/remote/density/environment/screen/components, CONFIDENT on a platform conflict — root cause is the `ListView`→`isTV` inspector regex), `ranking-miss` (anti-hover-only-actions, a11y-color-not-only, data-tables-numeric, anti-placeholder-labels, empty-state rule), `knowledge-gap` (grid roving tabindex for row buttons, column budget / default column set, WinUI status-cell and tabular-figure recipes), `direction-invariant` (navigation slot ignores the repo's NavigationView in both runs), `render-defect-fixed`, `render-defect-remaining`, `tooling-limit` (no Windows App SDK build workload; fixture package id invalid), `skill-helped` (mode classification audit+accessibility was correct; `comp-data-table`'s winui note, `desktop-keyboard-first`, `a11y-labels-names`, `a11y-live-status` and, once the TV signal was removed, the table-first/high-density/toolbar-commands direction were directly actionable and shaped the refactor).
