# p4-08 — results

## Task
"add a column-defaults settings dialog to the purchase order lines window so clerks can choose default warehouse and hidden columns"

## Project / stack / platform
`phase3-projects/p3-erp-desktop-dotnet/project` (state after p4-07) — native WPF, .NET 10, desktop, keyboard-first. **Existing project, new dialog.**

**Render mode: native.** `ErpClient.exe --capture <dir> --size 1440x900 --state ready --scenario dialog` — the harness opens the modal dialog through the view's own `OpenColumnDefaults()`, drives it with real OS keys (`keybd_event`) from inside the nested message loop, writes a JSON trace per run, and composites the dialog's client area onto the main window capture (OS title bars are not rendered; the focus-visual adorner layer is outside the rendered visual, so keyboard focus rings inside the dialog are traced, not pictured).

## Design-context table (`01-inspect.json`, same inspection as p4-07)
| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | menu-bar | INFERRED | menu bar + command bar + context menus; settings belong under View | yes |
| theme | light-first | INFERRED | single `Light.xaml` semantic brush set, `DynamicResource` everywhere | yes |
| surfaces | bordered-flat | INFERRED | 1 px `Border.Strong` borders, no shadows, radius 2 | yes |
| radius | small | INFERRED | 2 px | yes |
| spacing | 4 | INFERRED | 4 px grid, 32 px controls, 16 px page inset (plus the p4-07 band tokens) | yes |
| typography | unknown | UNKNOWN | Segoe UI Variable 12/14/20, Cascadia Mono for IDs | **no** (WPF FontFamily resource not recognised) |
| components | wpf | KNOWN | WPF + project styles (`Btn.Tool`, `Btn.Primary`, `Input.Filter`, `Text.*`) | yes |

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| field | value | verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope (activation flagged "add a column" as a non-UI term but still activated) | right |
| mode | create ("default (no mode cue)") | right — "add a … dialog" is a create; the evidence string is weak ("no mode cue" although "add a" was matched under `create`) |
| change_budget | moderate | right |
| intent | existing=true, creation=false, preserve=[] | partial — `creation:false` contradicts mode create; harmless |
| platform / input / stack / product / density | desktop (KNOWN from "window"), keyboard+pointer, wpf, erp, high | right |
| screen / components | settings; dialog, settings, table | right |
| jobs | [] | miss ("choose default warehouse and hidden columns" = configure defaults) |
| accessibility flags | all true | right |

## Guidance verdict (`03-guidance.md`, CONFIDENT: 3 core + 4 guardrails; concepts 7/7, coverage/1k 5.15, purity 0.86, contaminated none)
| record | role | verdict |
|---|---|---|
| `comp-settings-screen` | core | relevant — grouped rows, current values visible, picker for the enum, explicit Save (OK) |
| `comp-dialog` | core | relevant — title as heading, one primary action, sized to content, Escape + Cancel, WPF note "Owned Window with ShowDialog; set initial focus" |
| `comp-form` | core | partial — labels above / help below applied; validation, autosave, autofill do not apply |
| `grid-single-tab-stop` | guardrail | off-target — about row-action grids; the grid was untouched (selected only to cover *data-display*) |
| `a11y-modal-dialog` | guardrail | relevant — focus first control on open, return to invoker on close, Escape; this is the interaction test |
| `data-tables-numeric` | guardrail | off-target — no numbers in the dialog |
| `layout-states-empty-loading-error` | guardrail | off-target — a settings dialog has no async states |

Totals: relevant 3 · partial 1 · off-target 3.

Misses:
- **ranking-miss** — `desktop-keyboard-first` ("every dialog has a default and cancel button", access keys) was rank ≤12 in p4-07's search and in the bundle there, but not here; the interaction requirement it states (default/cancel) is the task's acceptance test. Layer: bundle-selection.
- **ranking-miss** — `a11y-keyboard-operable` (search rank 9, 0.402) and `focus-ring-standard` (rank 8, 0.408) not selected; the stock `CheckBox` needed an explicit `FocusVisualStyle` to match the project's ring. Layer: bundle-selection.
- **knowledge-gap** — column chooser pattern (which columns may be hidden, essentials locked and labelled, relation to the width rule, "restore defaults"); `metadata-rich` only says "user-controlled visibility". Layer: expected-concepts.
- **knowledge-gap** — `stacks/wpf.md` covers `IsDefault`/`IsCancel` and `Keyboard.Focus` on open but not focus *return* (re-resolve the grid cell after the modal closes) nor `FocusVisualStyle` for stock controls used inside a retemplated app. Layer: project-adaptation.
- Concern coverage bought three off-target guardrails (`grid-single-tab-stop`, `data-tables-numeric`, `layout-states`) because *data-display* and *states* were marked required for a settings dialog. Layer: concerns.

## Direction verdict (`04-direction.md`, validation OK, budget moderate)
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | menu-bar | preserved | yes — entry added under View |
| surface | bordered-flat | preserved | yes |
| color | light-first neutral+accent | preserved | yes |
| layout | form stack with sections | new | yes — label above, help below, sections, primary action last |
| density | high (4 px grid, 32 px controls, 28 px rows) | new | yes — matches the window |
| cards | bordered cards | new | **no** — contradicts the preserved bordered-panes surface ("no rounded card containers inside panes"); not used |
| typography | system native | new | yes (already true) |
| motion | functional minimal | new | yes |
| focus | visible ring | new | yes — ring on ComboBox/buttons, `Focus.Ring.Visual` for CheckBox |
| cta | one primary action | new | yes — OK is the only filled button |
| imagery | none | new | yes |
| icon | platform set | new | n/a |
| metadata | rich (user-controlled column visibility) | new | yes — this is the feature |

`preservation`: 3 preserved, 0 changed. Unjustified changes: none applied (cards ignored).

## Implementation (files; before-copies in `before/`)
- `Models/ColumnDefaults.cs` (new) — `DefaultWarehouse`, `HiddenColumns`, JSON persistence under `%LOCALAPPDATA%\ErpClient\column-defaults.json`; `StorePath = null` disables it (capture mode).
- `Views/ColumnDefaultsDialog.xaml(.cs)` (new) — owned modal `Window` (`ShowDialog`, `CenterOwner`, `SizeToContent=Height`, width 520, no resize, no taskbar entry), 20 px inset, section "Default warehouse" (label above, `Input.Combo`, help caption), section "Columns shown" (2-column list of `Check.Std`; the five essential columns are ticked, disabled, and labelled "(always shown)"), button row: Restore defaults (left) · OK (`IsDefault`, primary) · Cancel (`IsCancel`); focus on open → warehouse picker; works on a clone, returns `Result` on OK.
- `Themes/Controls.xaml` — `Space.Dialog.Inset` (20), `Input.Combo` (same metrics/border/focus as `Input.Filter`), `Check.Std` (28 px rows, secondary text when locked), `Focus.Ring.Visual` (2 px ring for stock controls).
- `Views/PurchaseOrderLinesView.xaml(.cs)` — View › "Column defaults…"; `ApplyColumnDefaults()` pins hidden columns as user overrides and releases the others to the width rule (also on load and on "Reset column layout"); `OpenColumnDefaults()` opens the dialog, applies + saves on OK, sets a status message, and re-focuses the grid cell the clerk came from.
- `ViewModels/PurchaseOrderLinesViewModel.cs` — `Defaults` (saving on set), `DefaultWarehouse`; `AddLine` starts new lines in the default warehouse.
- `App.xaml.cs` (harness) — `--scenario dialog`, composite capture, no settings persistence in capture mode.

## First-render defects (`render/first-*`)
| # | type | defect |
|---|---|---|
| 1 | interaction | Tab from the warehouse picker landed on the `ItemsControl` itself (a Control is focusable by default), so Space toggled nothing; fixed with `Focusable="False"` + `TabNavigation=Continue` |
| 2 | visual / accessibility | locked columns were plain disabled boxes with a 2.55:1 label and the reason only in a tooltip; fixed with a "(always shown)" label and secondary-text foreground (5.44:1 on the canvas) |
| — | tooling | the composite drew the dialog transparent and offset by its margin (`RenderTargetBitmap.Render` bakes the content's layout offset); harness only |

## Final defects (`render/final-*`)
| # | type | defect |
|---|---|---|
| 1 | existing-system-mismatch (minor) | stock Aero2 `ComboBox` chrome (hover gradient, drop glyph) and `CheckBox` glyphs are not themed, like the stock scrollbar elsewhere |
| 2 | platform (unverified) | keyboard focus ring on `CheckBox` (`Focus.Ring.Visual`) not visible in captures — the adorner layer is not part of the rendered visual; focus movement itself is traced |
| 3 | visual (minor) | no accelerator for the dialog (menu access keys only: Alt, V, D) |
Not verified: Narrator reading of `LabeledBy`/`HelpText`, 150/200 % DPI, high contrast, persistence round-trip outside capture mode.

## Iterations
3 builds: first render → fix (tab stop, locked-column labels, composite background) → composite offset fix → final. Product changes only in iteration 1.

## Interaction test summary (`render/final-ready-1440x900.json` → `dialog.runs`)
4 runs, all pass:
1. **escape** — dialog open, owned and modal; focus on open = `ComboBox#WarehouseBox` (inside the dialog); OK `IsDefault` / Cancel `IsCancel`; Escape → `DialogResult=false`, dialog closed, focus back on `DataGridCell[Item]` row 0 (the invoker), defaults unchanged.
2. **enter-applies** — Down selects "DXB-02 Cold"; Tab → `CheckBox:Unit` (first hideable); Space unticks it; Enter (default button) → result true, `DefaultWarehouse = DXB-02 Cold`, `HiddenColumns = [Unit]`, Unit column collapsed (11 visible), status "Column defaults saved — new lines start in DXB-02 Cold", a new line's warehouse = DXB-02 Cold; focus returned to the same cell.
3. **cancel-button** — change warehouse, focus Cancel, Enter → result false, nothing changed, focus returned.
4. **restore** — Restore defaults resets the picker to DXB-01 Main and ticks all boxes (focus back on the picker); OK → hidden columns [], hidden count 0, focus returned.
Dialog metrics: client 505.6×432.8 DIP centred on the owner (460, 215); OK bottom = content bottom (no clipping).

## Preservation verdict
Navigation (View menu), theme (no new brushes), typography, and component language preserved; the dialog reuses `Btn.Tool`/`Btn.Primary`/`Text.*` and the new `Input.Combo` mirrors `Input.Filter`. Grid behaviour unchanged except the intended column pinning. `preservation-ok`, unjustified structural change 0.

## Regressions to propose
- "add a settings dialog to a WPF window" → bundle includes `desktop-keyboard-first` (default + cancel button) and `a11y-modal-dialog`; no numeric-table or empty/loading-state guardrails.
- "choose which columns are hidden" → a column-chooser/visibility record (essentials locked, relation to responsive column priority, restore defaults).
- direction for a dialog inside a bordered-panes system → `cards` slot = none, not bordered cards.

## Tags
`context-detection-miss` (typography), `ranking-miss` (desktop-keyboard-first, a11y-keyboard-operable, focus-ring-standard), `knowledge-gap` (column chooser, WPF focus return / FocusVisualStyle), `direction-mismatch` (cards), `render-defect-fixed`, `render-defect-remaining`, `tooling-limit` (adorner layer, title bars), `skill-helped` (comp-dialog + a11y-modal-dialog + comp-settings-screen + comp-form label/help layout), `preservation-ok`.
