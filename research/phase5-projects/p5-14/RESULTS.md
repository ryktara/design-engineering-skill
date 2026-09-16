# p5-14 — "Purchase-order lines: operators keep typing the quantity into the price column."

**Task** p5-14 · sentence run verbatim · **Project** `research/phase3-projects/p3-erp-desktop-dotnet/project` · **Stack** WPF on .NET 10 (`net10.0-windows`, no NuGet packages, MVVM without a framework) · **Platform** desktop · **Existing UI** (one screen: menu bar, title band, command bar, DataGrid of 24 PO lines, status bar; light theme via `Themes/Light.xaml` semantic brushes, `Typography.xaml` roles, `Controls.xaml` styles) · **New screen** no.

Build hash start `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` = end hash. Skill not modified.

`dotnet build -c Release`: 0 warnings, 0 errors before and after. bin/ and obj/ deleted afterwards.

## Root cause (from the code, written in `00-expectation.json` before any advise call)

`ColQty` (header "Qty", 76 px, `StringFormat=N2`) and `ColPrice` ("Unit price", 100 px, `N2`) share `Text.Numeric` / `Edit.Cell.Numeric` and the same two-decimal format, so `240.00` and `14.75` read as the same kind of number; only the 72 px Unit ComboBox (which folds below 1020 DIP) sits between them. The cell has a 2 px focus ring but the column header is never marked, type-to-edit starts on any digit, and Enter commits and moves **down** in the same column, so an operator who lands one column too far right keeps typing quantities into prices row after row with no cue. The baseline render (`render/before-*.png`) shows exactly this.

## Design-context table (`01-inspect.json` vs the code)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | Menu (File/Edit/View/Help) + command bar + status bar | yes |
| theme | light-first | KNOWN | single light theme, `Brush.*` semantic tokens, DynamicResource everywhere | yes |
| surfaces | bordered-flat | INFERRED | 1 px `Brush.Border.Strong` panes, no shadows | yes |
| radius | small (2) | INFERRED | CornerRadius 2 on buttons, square grid | yes |
| spacing | 4 | INFERRED | 4 px grid, 32 px rows/controls, 16 px page inset | yes |
| typography | **monospace** | INFERRED | `Font.UI` = Segoe UI Variable Text 14/12/20 (Typography.xaml); Cascadia Mono is only the item-code cell role; tabular numerals yes | **no** (confident wrong value from one mono reference; `features.monospace` is even `false` in the same object) |
| components | wpf | KNOWN | stock WPF DataGrid/Menu/StatusBar, restyled | yes |
| focus (not a slot) | — | — | `Brush.Focus.Ring` + 2 px ring triggers in 6 styles; inspect only says "explicit focus handling in 3 files" | not surfaced → direction later calls the focus slot "new: no repository evidence" |

## Requirements verdict (`02-requirements.json`)

- **platform** desktop from project inspection — correct (`platform_evidence` is empty; resolved from `01-inspect.json`).
- **artifact_state** existing — correct. `intent.operations` = diagnose, modify — correct. `intent.utterance` observation, `problem` true — correct.
- **intent.problem_domain** `[]`, `screen` `[]`, `screen_subtype` `[]`, `change_scope` unknown, `intent.preserve` `[]` — **miss**: the sentence names a grid column and a data-entry mistake; nothing was extracted (`scope_evidence.ui` = ["column"] only). `constraints.preserve_existing_system` true compensates partly.
- **mode** [audit, refactor] with evidence "problem statement on existing UI / fix follows the diagnosis" — acceptable (my expectation: refactor, polish). `primary_jobs` = [audit].
- **scope.kind** in-scope, reason "UI design / interaction task" — correct.
- **change_budget** low — reasonable for this task.
- **activation** `decision: skip, ui_score 0, non_ui_score 0` — worth flagging: if activation gates skill invocation, this sentence would not trigger the skill at all even though scope says in-scope.
- **project_context** carries the wrong typography value through.
- status CONFIDENT, `missing` [] — the UNKNOWN-with-confirm path was not needed.

## Guidance verdict (`03-guidance.md/json`; bundle 6 = core 2 + guardrails 4; 1268 tokens; concept coverage 3/3 required)

| record | role | verdict | BAD category | note |
|---|---|---|---|---|
| `comp-data-table` | core | partial | — | generic table checklist; its only pointer to the fix is "Financial tables: see numeric rule" — and that rule (`data-tables-numeric`) was omitted from the bundle. Carries `data.pagination_strategy` + `table.virtualization` for a 24-row grid (noise). |
| `metadata-rich` | core | relevant (thin) | — | "consistent formatting per type (dates, currency, IDs in monospace)" is the one line in the bundle that touches the fix. Record has `concepts: []`, so it counts for nothing in recall. |
| `grid-single-tab-stop` | guardrail | partial | — | already fully implemented in the project (Tab once, arrows, F2/Esc); "announce the current row/column" is the relevant sentence, framed around row-action buttons that this grid does not have. |
| `desktop-status-bar-and-error-navigation` | guardrail | off-target | generic | describes, almost verbatim, what this project already has (F8 next error, "Line 50: Quantity must be greater than 0"); no bearing on column confusion. |
| `anti-no-states` | guardrail | off-target | generic | loading/empty/error states exist and are untouched by the task. |
| `a11y-native-semantics` | guardrail | partial | — | AutomationProperties reminder; used it to word the editor HelpText. |

Relevant 1 · partial 3 · off-target 2. No `harmful` or `off-platform` record. Omitted: `comp-data-entry-grid` ("same category as a core pick"), the most task-specific component record in the base. PARTIAL_SCOPE: not raised (correct).

### Concept recall

| expected id | delivered? | via | layer if missing |
|---|---|---|---|
| table.inline_edit (critical) | yes | comp-data-table | — |
| table.tabular_figures (critical) | yes | comp-data-table | — (but the record carrying the operative text, `data-tables-numeric`, was dropped) |
| interaction.focus_visible (critical) | yes | grid-single-tab-stop | — |
| interaction.keyboard_navigation | yes | grid-single-tab-stop | — |
| a11y.accessible_names | yes | a11y-native-semantics | — |
| feedback.validation_errors | yes | desktop-status-bar-and-error-navigation | — |
| process.reuse_first | **no** | — | **bundle-selection** (trace: candidate `impl-reuse-before-new` 0.28 existed, "bundle cap or lower utility left it out") |

Recall 6/7 = **0.86**, critical 3/3 = **1.0**. Delivered union (16): a11y.accessible_names, a11y.contrast, a11y.live_status, a11y.semantics, data.pagination_strategy, desktop.persist_workspace, feedback.validation_errors, interaction.focus_visible, interaction.keyboard_navigation, interaction.selection_visible, interaction.shortcuts, state.loading_empty_error, table.inline_edit, table.selection_bulk, table.tabular_figures, table.virtualization. One forbidden id delivered: `data.pagination_strategy` (via comp-data-table's concept list, not its text). The trace also demanded `desktop.fluent_materials` ("Windows stack") — wrong for a WPF app with its own token theme; uncovered, so harmless.

**Knowledge gap (confirmed with `search -k 12`, `03-search.txt`):** nothing in the base says "mark the current column's header", "label the value in the editor with its unit/currency", or "adjacent numeric columns of different roles must not share a format". The top-12 for the verbatim sentence include `layout-epg-grid` and `layout-single-column`; the closest hit is `data-tables-numeric` at rank 8 (0.291) with "unit in the header not each cell, one precision per column". The ontology has no id for column disambiguation / mis-entry prevention; the recall above is therefore nominal — the three critical ids were "covered" by records whose text does not contain the fix.

## Direction verdict (`04-direction.md/json`)

Change budget low; 12 slots preserved, 0 changed, 1 **new**: `focus` → `focus-ring-standard` "no repository evidence for this slot". That is wrong: `Brush.Focus.Ring` (#1F5FBF) and 2 px `IsKeyboardFocused/IsKeyboardFocusWithin` triggers exist on cells, headers, buttons, inputs and checkboxes. Not harmful (the guidance text matches what exists) but a context-detection → direction miss. `typography` preserved as `typography-monospace-technical` with the per-slot text "Monospace for code, IDs, timestamps, and metrics" — **contradicts the codebase** (UI is Segoe UI Variable; only item codes are mono). Following it literally would have put the numeric columns in Cascadia Mono; ignored. `validation.ok = true`, no violations. Preservation of navigation/layout/density/surface/color: justified and followed.

## Implementation (files changed; all copied to `before/` first)

- `Views/PurchaseOrderLinesView.xaml` — Qty column: header **"Quantity"**, `StringFormat='#,##0.##'` (counts read `240`, `2.5`; money keeps `N2`), width 80; `ColPrice` `v:ColumnGroup.Edge="Start"` width 116, `ColTotal` `Edge="End"` width 116; `EditingElementStyle` → `Edit.Cell.Quantity` / `Edit.Cell.Money`; Disc/Tax/Requested trimmed by 4 px each so the star-sized Description keeps its width.
- `Views/PurchaseOrderLinesView.xaml.cs` — `ApplyCurrencyHeaders()` sets "Unit price (AED)" / "Line total (AED)" from `Vm.Currency` (DataContextChanged + Loaded, before the Columns menu is built); `OnCurrentCellChanged` calls `ActiveColumn.Apply`.
- `Views/ColumnPriority.cs` — three attached-property helpers next to the existing one: `ActiveColumn.IsCurrent` (DataGridColumn), `ColumnGroup.Edge` (DataGridColumn), `Affix.Prefix/Suffix` (editor TextBox).
- `Themes/Controls.xaml` — `xmlns:v`; header template: `ActiveBar` (2 px `Brush.Focus.Ring`, bottom) + primary foreground when `Column.(v:ActiveColumn.IsCurrent)`, `GroupStart/GroupEnd` 1 px `Brush.Border.Strong`; cell template: same group lines under the ring; new `Edit.Cell.Affix` template (prefix/suffix TextBlocks at caption size/secondary colour around `PART_ContentHost`), `Edit.Cell.Quantity` (suffix = row `Unit`), `Edit.Cell.Money` (prefix = grid `DataContext.Currency`), both with a column-specific `AutomationProperties.HelpText`.
- `Views/ColumnDefaultsDialog.xaml` — help text "Qty" → "Quantity".
- `App.xaml.cs` (capture harness only) — `--scenario price`: focuses a Unit price cell, F2, writes `{prefix}-editing-price.png` and a `priceEdit` JSON block (editor text/prefix, current column).

Kept: routes/commands, key bindings (Enter down, Tab right, F2, Esc, F8, Ins, Del, Ctrl+Z), column-priority folding, selection, validation, status bar, all tokens; no new colours, fonts or spacing values.

**Guidance used:** "consistent formatting per type … currency" (metadata-rich); "unit in the header not each cell, one precision per column" (data-tables-numeric — read from the search output, not from the bundle); "announce the current row/column … visible focus indicator" (grid-single-tab-stop); AutomationProperties HelpText (a11y-native-semantics); direction's preserve-everything table. **Ignored:** typography slot "monospace for metrics" (contradicts codebase); focus slot "new" (already exists); status-bar and states guardrails (already implemented, nothing to do); `comp-data-table`'s selection-checkbox / skeleton-rows / pagination items (not this task). **Deliberate deviation from a delivered rule:** `#,##0.##` is not "one precision per column" in the strict sense; `N0` would round `2.5 KG` to `3`, so variable precision was chosen and noted here.

## Render

**Render mode: native** (`ErpClient.exe --capture`, RenderTargetBitmap at the machine DPI; PNGs are 1782×1078 for a 1440×900 client area). `render/before-*` = untouched baseline, `render/first-*` = first render of the implementation, `render/final-*` = after the fix, plus `final-ready-1100x700`, `final-ready-820x600`, `final-price-editing-price.png`. The key-scenario JSON traces (`*-ready-1440x900.json`) record row/column/editing/focus-ring after every key.

**First-render defects (implementation):** visual 1 — the +36 px added to Quantity/Unit price/Line total came out of the star-sized Description column, which truncated "Rebar 12 mm deformed, 12 m" (fit before). No interaction, accessibility, platform, existing-system-mismatch or implementation-bug defects: trace identical to baseline (all 21 steps keep the focus ring, Enter/Tab/Shift+Tab/F2/Esc/F8/Shift+F8/Ctrl+End/Ctrl+Home behave the same, F6 cycle TextBox→Button→DataGridCell, Ctrl+F lands in FilterBox, numeric alignment Right/tabular on all five numeric columns).

**Fix (iteration 1):** rebalance widths (Quantity 80, Unit price 116, Line total 116, Disc 68, Tax 60, Requested 100). **Final defects: 0.** Iterations: 1. Layout probe unchanged vs baseline (menu x 16.8, title x 16, grid 16/118.4/1393.6×704, status bar h 28). Side observation, not a defect: the harness step "End 1 2" on quantity 800 now commits 80012 (before: 800.0012, displayed as 800.00) — the new format shows what was typed instead of hiding it in the hundredths.

Final evidence: `final-editing.png` (Quantity editor `800 | EA`, "Quantity" header with bar), `final-price-editing-price.png` (`AED | 13.20`, "Unit price (AED)" header marked; JSON `priceEdit.editorPrefix = "AED"`, `currentColumns = ["Unit price (AED)"]`), `final-ready-820x600.png` (Unit folded; Quantity still reads as counts and the strong divider separates it from the money block; 7 columns hidden reported as before).

## Preservation verdict

navigation ✓ theme ✓ typography ✓ (no new families/sizes; affix uses the existing caption size and secondary colour) component_reuse ✓ (all styles `BasedOn` existing ones; brushes are the existing tokens) · unjustified structural changes 0 · column-priority, dialog, key bindings, harness scenarios intact. **preservation-ok.**

## Skill effect

**neutral.** The bundle did not contradict the fix and two lines in it (currency formatting per type; announce the current column) point the right way, but the operative ideas — current-column header mark, unit/currency affix in the editor, quantity vs money precision — came from reading the code, not from the skill; the one record that states the precision/unit rule was dropped as redundant. Nothing harmful was applied; the wrong typography/focus slots were easy to ignore because the codebase is explicit.

## Misses by earliest wrong layer

1. **requirements** — `intent.problem_domain`, `screen`, `change_scope`, `intent.preserve` all empty for a sentence that names a grid column and a data-entry error; `activation.decision = skip` (ui_score 0).
2. **requirements (context detection)** — `project_context.typography = monospace` (confident wrong) propagated from inspect; focus tokens not surfaced as a slot.
3. **expected-concepts** — `desktop.fluent_materials` demanded for a token-themed WPF app; no concept for column disambiguation exists in the ontology (see knowledge gap).
4. **bundle-selection** — `data-tables-numeric` (the operative rule), `comp-data-entry-grid` (the task-specific component) and `impl-reuse-before-new` (process.reuse_first) all dropped by the category/redundancy cap in favour of two generic guardrails that restate the existing status bar and states.
5. **direction** — focus slot "new / no repository evidence"; typography slot text "monospace for metrics" contradicts the codebase.
6. **knowledge-gap** — no record for active-column marking, editor affixes, or role-distinct numeric formatting between adjacent columns.

## Regressions to propose

- Query: the sentence verbatim with this project → expect `intent.problem_domain` ⊇ {data-entry, table}, `screen` ⊇ {grid}, activation ≠ skip; bundle includes `data-tables-numeric` and `comp-data-entry-grid`; `comp-data-entry-grid` must not be dropped as "same category" when its `use_when` (invoice lines, batch entry) matches the product and sentence.
- Query: `inspect_project.py` on this project → typography = system-sans (Segoe UI Variable) with a mono role for codes, not `monospace`; a focus slot KNOWN from `Brush.Focus.Ring` / `IsKeyboardFocused` triggers.
- Query: direction for any task on this project → focus slot must be `preserved`, typography slot must not emit "monospace for metrics".
- Ontology: add an id for column disambiguation / mis-entry prevention (header marks the current column; unit or currency affix in the editor; distinct precision per numeric role) and one record carrying it for desktop/web data-entry grids.
- Data: `metadata-rich` has `concepts: []`; give it `table.tabular_figures`-adjacent ids or it can never count toward recall.

## Tags

`requirements-miss`, `context-detection-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`
