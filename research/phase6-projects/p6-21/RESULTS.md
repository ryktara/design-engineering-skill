# p6-21 — FleetDesk (Avalonia desktop) — vehicles list width adaptation

**Task sentence (verbatim):** "The vehicle map and the list fight for space when the window is narrow."
**Project:** `research/phase5-projects/p5-avalonia-fleet/project` · Avalonia 11 / .NET / MVVM · desktop
**Existing UI:** yes. New screen: no.
**Build hash start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`** (matches the frozen c3 hash).
**`dotnet build` is available and was used** — it succeeds before and after the change (0 warnings, 0 errors).

## Headline: the sentence has a false premise

There is no map in this codebase. `grep -ri map` over the whole project returns exactly one hit, the word "maps" in a README sentence about view-model wiring. `VehiclesView.axaml` is a `DockPanel` with a header row, a `DataGrid` and a bottom selection summary. The "vehicle map and the list fight for space" complaint cannot be taken literally here.

The real narrow-window contention on the vehicles view is:
1. the header `Grid ColumnDefinitions="*,Auto"` — column 1 holds a checkbox + a **fixed** 280 px `TextBox` + a Clear button (~540 px) against a title block that needs ~340 px, so they collide near the window's own `MinWidth="960"`;
2. the `DataGrid` — six fixed columns total 750 px plus a star `Driver` column, so `Driver` is crushed to ~120 px at narrow widths.

I fixed that and did **not** invent a map. The skill cannot know the map is absent from the sentence alone; what it could have done is reconcile the `screen_subtype: map` it extracted from the wording against the inspected project, which it did not — see "Misses".

## Design context (step 1)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | menu bar + toolbar strip + status bar (MainWindow.axaml) | yes |
| theme | light-first | INFERRED | light-first, Theme.axaml header says so | yes |
| surfaces | bordered-flat | INFERRED | `Border.surface`: 1 px line, radius 4, "NO drop shadows" | yes |
| radius | small | INFERRED | `AppCornerRadius` = 4 | yes |
| spacing | 4 | INFERRED | declared scale is **8/16/24/32** (`Space1..4`); 4/6/2 are only inner control paddings | **partial** (the declared scale was ignored in favour of raw literal frequency) |
| typography | humanist-sans | KNOWN | Segoe UI → Inter, 600 weights, encoded scale, tabular numerals | yes |
| components | avalonia | KNOWN | Avalonia + DataGrid | yes |
| tokens | `[]` | — | `Styles/Theme.axaml` is a complete token dictionary (colours, brushes, type scale, spacing, shape) | **no** — a full design-token file was reported as no tokens |
| breakpoints | `[]` | — | correct, there were none | yes |

## Requirements verdict (step 2)

| Field | Value | Verdict |
|---|---|---|
| platform_evidence | desktop, WEAK_INFERENCE from "window"/"the window", confirmed by project inspection | correct |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | responsive | correct |
| intent.change_scope | screen | correct |
| mode + mode_evidence | `responsive`, `audit` ("responsive defect", "diagnose first") | correct — inside my acceptable set, and the sentence carries no mode word |
| scope.kind | in-scope | correct |
| change_budget | moderate | correct |
| intent.preserve | `[]`, but `constraints.preserve_existing_system: true` | acceptable |
| project_context | carried through from inspect | correct except spacing (above) |
| screen_subtype | `map` | correct *from the sentence*, wrong *for this project* — not reconciled against the inspection (see Misses) |

Status CONFIDENT, `missing: []`. No unwarranted abstain.

## Guidance verdict (step 3)

Bundle = 6 (core 2 + guardrails 4), 715 tokens, OPTIONAL layer empty. `status=PARTIAL` because required concern `accessibility` was uncovered.

| Layer | Record | Verdict | Category |
|---|---|---|---|
| core | `chart-geo` | off-target | `contradicts-codebase` — choropleth/symbol map guidance for a project with no map anywhere |
| core | `chart-relationship` | off-target | `wrong-screen` — scatter/bubble has no bearing on a map-vs-list width fight; its own `marginal` says `task evidence: ` (empty) |
| guardrail | `impl-reuse-before-new` | partial | `generic` — true, but SKILL.md §2 already says it; contributed nothing this task needed |
| guardrail | `desktop-window-resizing` | **relevant** | — this record carried the whole answer: breakpoint matrix, "panes collapse in a documented order", "star/auto grid sizing, not absolute", DPI |
| guardrail | `desktop-keyboard-first` | partial | `generic` — correct for the platform, nothing width-related |
| guardrail | `layout-states-empty-loading-error` | off-target | `generic` — no async/empty-state work in this task; selected to satisfy a `state.loading_empty_error` requirement the sentence never raised |

relevant 1 · partial 2 · off-target 3. `optional_useful` 0 / `optional_noise` 0 (layer omitted — correct here).

### Concept recall

Delivered (union over selected records): `adaptive.breakpoint_matrix`, `table.column_priority`, `process.reuse_first`, `interaction.keyboard_navigation`, `interaction.shortcuts`, `interaction.focus_visible`, `state.loading_empty_error`, `data.chart_by_question`, `data.accessible_chart_alternative`.

| Expected id | Critical | Delivered? | Layer if missing |
|---|---|---|---|
| `adaptive.breakpoint_matrix` | yes | yes (`desktop-window-resizing`, SPECIFIC) | — |
| `table.column_priority` | yes | yes (`desktop-window-resizing`) | — |
| `layout.spacing_scale` | no | no | `expected-concepts` (never demanded) |
| `desktop.spacing_grid` | no | no | `expected-concepts` |
| `process.safe_modification` | no | no | `expected-concepts` — `process.reuse_first` was demanded instead |
| `content.readable_measure` | no | no | `expected-concepts` |

**Concept recall 2/6 = 0.33. Critical recall 2/2 = 1.00.** Both pre-registered critical concepts landed, in one SPECIFIC record. No forbidden concept appeared (no touch/TV/kiosk records; the platform filter correctly dropped six mobile/TV/kiosk candidates).

The skill's own critical set was different from mine (`data.accessible_chart_alternative`, `process.reuse_first`) — the first is a direct consequence of the phantom `map` subtype.

Not-surfaced: `adaptive.navigation_transform` (carriers filtered as mobile/tablet) and `desktop.persist_workspace` (cap/utility). Neither was needed.

## Direction verdict (step 4)

12 of 13 slots `preserved` with the correct reason ("existing system with change budget 'moderate'"). **`unjustified_direction_slots: 1`** — the `cards` slot is `new` → "List rows (`card-list-row`)", reason "no repository evidence for this slot". The project has no cards and uses a DataGrid; nothing in the task justifies introducing a card/list-row geometry. I ignored it. Minor: the fingerprint reports `corner_language: "sharp"` while the same output detects radius 4 / `small` — internally inconsistent, though no slot acted on it. `validation: OK`. Preservation metrics correct.

## Implementation (step 5)

Files changed (originals in `before/`):
- `Views/VehiclesView.axaml` — header `Grid` gains a second row; the filter cluster becomes a named `Grid#FilterPanel` (`Auto,*,Auto`); two `UserControl.narrow` styles move it to the full-width second row and release the filter box from its fixed 280 px; `Driver` gets `MinWidth="140"`; grid named `VehicleGrid`; summary text wraps.
- `Views/VehiclesView.axaml.cs` — Avalonia has no container queries, so the view observes its own `Bounds` and applies two documented thresholds: **< 1120 epx narrow** (filter row stacks, `Odometer (km)` dropped), **< 1000 epx compact** (`Last service` dropped as well). Columns are dropped in a documented lowest-priority-first order. `x:Name` on a `DataGridColumn` does **not** generate a field (columns are not in the name scope) — caught by `dotnet build`, fixed by addressing columns by index off the named grid.
- `ViewModels/VehiclesViewModel.cs` — `SelectionSummary` now also carries last service and service label, so the dropped columns lose no information.
- `render/twin.html` — the vehicles screen only (scoped `#vehicles` CSS + a `body.fit` sizing hook). The dispatch screens were not touched, as required by the concurrency constraint.

**Guidance used:** `desktop-window-resizing` — documented breakpoints, documented pane/column collapse order, star/auto over absolute sizing (the fixed 280 px filter box and the crushed `Driver` column were exactly the "absolute sizing" failure it names).
**Guidance ignored:** `chart-geo` and `chart-relationship` (no map, no chart in this project); `layout-states-empty-loading-error` (no state work in scope); `impl-reuse-before-new` (already covered by SKILL.md §2, and followed anyway); `desktop-keyboard-first` (unrelated to the request; existing keyboard behaviour preserved); direction's `cards` slot (would have replaced a DataGrid with list rows for no reason).

**Process guidance check:** SKILL.md §2 and §7 were sufficient. `impl-reuse-before-new` in the bundle added nothing, and `verify-render-and-inspect` was not in the bundle yet the render-and-inspect loop happened anyway. `process_records_needed: false`.

## Render (steps 6–7)

`render_mode: html-twin` — there is no `--capture` harness in `Program.cs`; `dotnet build` verifies compilation but cannot produce a screenshot headlessly here (`tooling-limit`). Playwright 1.63.0, Chromium, at 1280×800 (wide), 1100×700 (narrow) and 900×700 (compact). I looked at all three.

First-render defects: **visual 1** — the twin's `.grid-wrap { overflow: hidden }` cut the last table row in half at every width, which the real `DataGrid` (which scrolls) would not do. No other defect: the wide render at 1280×800 is byte-for-byte the baseline layout, the 900×700 render shows the stacked full-width filter row, both low-priority columns dropped, `Driver` readable, and the selection summary carrying `132,870 km - last service 2026-08-28 - OK`.

Final defects: **0**. Iterations: 2 (1 build-error fix + 1 render fix).

No defect the guidance warned about was shipped.

## Preservation

Menu bar / toolbar / status bar untouched. Theme, typography, radius, spacing tokens untouched — every new value is a `StaticResource` from `Theme.axaml`. No new colour, no new component. Sorting, filtering, the `OverdueOnly` checkbox, `SelectedItem` binding, the `Service` badge (words + colour, never colour alone) and all `Classes` semantics are intact. DispatchView, SettingsView and MainWindow were not opened for edit. `unjustified_structural_change: 0`.

## Misses by earliest wrong layer (step 8)

1. `candidate-compatibility` — `screen_subtype: map` was extracted from the wording and never reconciled against the inspected project, which has no map. Two of the two CORE records (50% of the bundle's core, 33% of its records) are map/chart guidance for a project that has neither. The platform filter works; there is no equivalent project-compatibility filter for screen subtypes that the repository contradicts.
2. `expected-concepts` — `layout.spacing_scale`, `desktop.spacing_grid`, `process.safe_modification`, `content.readable_measure` were never demanded for a "things fight for space at narrow widths" request. The two that mattered most were demanded, so this is a recall, not a criticality, failure.
3. `project-context` — `inspect_project.py` reports `tokens: []` for a project whose `Styles/Theme.axaml` is a full token dictionary, and reports `spacing: 4` when the file declares an 8-px scale in a commented header. Literal-frequency counting beats declared scales.
4. `direction` — `cards: new / card-list-row` on an existing UI with a moderate budget and no card anywhere in the repository.

## Regressions to propose

- query: `"The vehicle map and the list fight for space when the window is narrow."` with an Avalonia/WPF project inspection that contains **no** map/chart evidence → expect: no `chart-*` record in CORE; expect `desktop-window-resizing` in the bundle.
- query: any narrow-width table/grid request on desktop → expect `table.column_priority` **and** a record that names where dropped column values go (detail pane / summary row); today only the first exists.
- inspect fixture: an Avalonia `Styles/*.axaml` with `<Color>`/`<SolidColorBrush>`/`<x:Double>` resource keys → expect `tokens` non-empty and the declared 8-px spacing scale preferred over literal frequency.

## Tags

`skill-helped`, `concept-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `preservation-ok`, `tooling-limit`
