# p4-07 — results

## Task
"polish this existing light-theme WPF purchase-order screen: inconsistent spacing in the toolbar and status bar, and validation errors are hard to read"

## Project / stack / platform
`phase3-projects/p3-erp-desktop-dotnet/project` — native WPF, .NET 10 (`net10.0-windows`, no NuGet), desktop, keyboard-first. **Existing UI** (the Phase 3 purchase-order-lines grid: menu bar + title band + command bar + DataGrid + status bar, single Light theme dictionary).

**Render mode: native.** `ErpClient.exe --capture <dir> --size WxH --state ready --scenario keys` (RenderTargetBitmap of the client area at 96 DPI, real OS keyboard input via `keybd_event`, JSON trace per step). Sizes 1440×900 (required), 1100×700, 820×600; states ready / error / empty. Title bar not captured (client area only).

## Design-context table (`01-inspect.json` → `design_context`)
| field | detected | status | actual (read from `Themes/*.xaml`, the view) | correct? |
|---|---|---|---|---|
| navigation | menu-bar | INFERRED | `Menu` (File/Edit/View/Help with access keys + InputGestureText) + command bar + per-object ContextMenu | yes |
| theme | light-first | INFERRED | one `Themes/Light.xaml` of semantic brushes (`Brush.Bg.*`, `Brush.Text.*`, `Brush.Feedback.*`, `Brush.Focus.Ring`), all views `DynamicResource`; no dark/HC dictionary | yes |
| surfaces | bordered-flat | INFERRED ("weak signal") | 1 px borders (`Brush.Border.Strong` 3.59:1), no shadows, header strips; CornerRadius 2 on buttons | yes |
| radius | small (2) | INFERRED | 2 px on buttons, 1 px inner ring, 10 px only for the error badge circle | yes |
| spacing | 4 (values 16, 4, 12, 10, 6) | INFERRED | 4 px grid tokens (`Size.Row` 32, `Size.Control` 32, `Space.Cell` 8,0, `Space.Pane` 16,8); off-grid literals 10 (button padding, placeholder margin), 6 (glyph margins), 33 (overlay), and space-character separators in the status bar | partial — the base was right; the 10/6 the inspector listed are exactly the task's "inconsistent spacing" but nothing flags them |
| typography | unknown ("no font family declaration found") | UNKNOWN | `Typography.xaml`: `<FontFamily x:Key="Font.UI">Segoe UI Variable Text, Segoe UI</FontFamily>`, `Font.Mono` Cascadia Mono for IDs, 3-step scale Caption 12 / Body 14 / Subtitle 20, SemiBold headings, tabular numerals | **no** — WPF `<FontFamily x:Key>` resources are not recognised; `monospace:false` and `type_scale:false` are also wrong |
| components | wpf | KNOWN | WPF with a project style set (`Btn.Tool`, `Btn.Primary`, `Input.Filter`, `Grid.*`, `Bar.Status`, `Menu.Main`, `Text.*` roles) | yes (stack only; the style vocabulary is not surfaced) |

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| field | value | verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope | right |
| mode / mode_evidence | polish + audit ("explicit: polish", "visual problem on existing UI", "diagnose first") | right |
| change_budget | low | right |
| intent | existing=true, problem=true, facet=visual, preserve=[] | right (nothing to preserve was stated; `preserve_existing_system` constraint true) |
| platform / input / stack / product / density | desktop, keyboard+pointer, wpf, erp, high | right |
| screen | [] | miss — "purchase-order screen" is a data-entry grid screen |
| components | form, navigation | **partial/wrong** — "toolbar", "status bar", "validation errors" are the named components; "form" is not what the screen is (it is a grid) |
| jobs | [] | miss (polish/readability) |
| accessibility flags | all true | right ("hard to read" is a contrast/readability problem) |
| project_context | as in the table above | typography wrong, rest right |

## Guidance verdict (`03-guidance.md`, PARTIAL: 4 core + 4 guardrails; concepts 7/7, coverage/1k 5.21, purity 0.75, uncovered required concern **accessibility**)
| record | role | verdict |
|---|---|---|
| `comp-form` | core | partial — only the WPF line ("ErrorTemplate that shows text, not only a red border") applied; labels-above / one-column / autosave are for forms, not a grid |
| `cta-toolbar-commands` | core | relevant (existing bar already follows it; confirmed count-near-commands, disabled-not-hidden) |
| `nav-menu-bar-desktop` | core | relevant (preserve; shortcuts shown in menus → F8 added to the Edit menu) |
| `layout-table-first` | core | partial — describes what already exists; nothing on toolbar/status-bar spacing |
| `desktop-keyboard-first` | guardrail | relevant (shortcuts in menus and tooltips; used for the F8 / Shift+F8 error navigation) |
| `anti-inconsistent-spacing` | guardrail | relevant — the central record: one inset per container, align left edges, equalise gaps; drove the whole spacing pass |
| `typo-measure-and-rhythm` | guardrail | partial — vertical spacing from the scale applied; line length / hierarchy jumps not at issue |
| `layout-states-empty-loading-error` | guardrail | off-target — states were not part of the request and were already built |

Totals: relevant 4 · partial 3 · off-target 1.

Misses (with earliest wrong layer):
- **ranking-miss** — `a11y-forms-errors` (search rank 8, 0.382: "error message next to the field, programmatically associated, what is wrong and how to fix") is the record for "validation errors are hard to read"; it was not selected although the *accessibility* concern was reported uncovered. Layer: bundle-selection.
- **ranking-miss** — `a11y-color-not-only` (rank 6, 0.396) not selected; same concern. Layer: bundle-selection.
- **ranking-miss** — `layout-spacing-scale` (rank 3, 0.426, "every 'spacing feels off' complaint") not selected; `anti-inconsistent-spacing` covered the concept, so tolerable. Layer: bundle-selection.
- **requirements-miss** — components = form/navigation: "toolbar", "status bar", "grid" never became components, so `comp-data-table` was pruned as "no table evidence in the request". Layer: requirements.
- **knowledge-gap** — no record for a desktop status bar (segments, separator, priority order when narrow, where a validation message lives). Layer: expected-concepts.
- **knowledge-gap** — no record for validation display in an editable grid (cell tint + row marker + message location + next/previous-error navigation, F8 idiom). `comp-data-entry-grid` says "per-cell validation with a summary" only. Layer: expected-concepts.
- **knowledge-gap** — `stacks/wpf.md` does not mention that a `Validation.ErrorTemplate` adorner draws *over* the element, so a tinted adorner washes out the value text (the actual "hard to read" cause here). Layer: project-adaptation.

## Direction verdict (`04-direction.md`, validation OK, budget low)
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | menu-bar (`nav-menu-bar-desktop`) | preserved | yes |
| density | spacing base 4 | preserved | yes |
| surface | bordered-flat (`surface-bordered-panes`) | preserved | yes |
| color | light-first (`color-neutral-accent`) | preserved | yes |
| layout | dashboard grid of modules | new | **no** — the screen is table-first (the alternative list had it at 0.47); no repository evidence because the inspector does not see a `DataGrid` as a layout signal |
| cards | none | new | fits (already true) |
| typography | platform system font | new | fits the actual (Segoe UI) but is marked "no repository evidence" — detection miss |
| motion | functional minimal | new | fits (no storyboards) |
| focus | visible focus ring | new | fits (already true) |
| cta | toolbar with selection-driven commands | new | fits (already true) |
| imagery | data graphics | new | **no** — no chart on the screen |
| icon | outline set | new | n/a (text glyphs only) |
| metadata | inline badges and status chips | new | **no** — the grid shows status as plain text; badges would be a new visual device |

`preservation`: preserved 4 slots, changed 0. Unjustified changes: none applied; the three wrong "new" slots were ignored. For a low-budget polish task the direction step added nothing beyond the preserved slots; the useful material came from the guardrails.

## Implementation (files changed; before-copies in `before/`)
- `Themes/Controls.xaml` — spacing tokens `Space.Band.Title` (16,12,16,8), `Space.Band.Commands` (16,0,16,12), `Space.Band.Content` (16,0,16,12), `Space.Gap.Control` (0,0,8,0), `Space.Gap.Group` (16,0,0,0), `Space.Inset.Bar` (16,0); `Btn.Tool` padding 10→12 and margin from the token; `Menu.Main` padding so "File" sits on the 16 px inset; `Bar.Status` inset 16 with `Bar.Status.Item` (padding 0), `Bar.Status.Sep` (one "·" with 8/8 margins instead of space characters), `Bar.Status.Text`, `Btn.Status.Link`; validation: `CellErrorTemplate` no longer paints a 55 %-opacity tint *over* the text (adorner = bottom bar only), the cell tints itself through a DataTrigger on `Content.(Validation.HasError)`, the editor tints itself through `Validation.HasError`; `AutomationProperties.HelpText` carries the message; row-header glyph 12→14.
- `Views/PurchaseOrderLinesView.xaml` — band margins from the tokens; selection-summary/filter gaps on the scale; status bar rebuilt as a DockPanel with the separator style, the error count as a link (next error), a trimmed "Line N: message" segment for the focused row; F8 / Shift+F8 key bindings and Edit-menu items; key hints mention F8.
- `Views/PurchaseOrderLinesView.xaml.cs` — `UpdateFocusedError()` on `CurrentCellChanged`/`ErrorCount` (cell's own error first, else the row's first message), `GoToError(backwards)` wrapping through rows/visible columns, `UpdateKeyHints()` (hints fold below 1180 DIP or while a message is shown), shortcut help text.
- `ViewModels/PurchaseOrderLinesViewModel.cs` — `FocusedError`, `NavigateToError`, `NextErrorCommand`, `PreviousErrorCommand`.
- `App.xaml.cs` (harness only) — layout probe (left edges / band tops), F8 steps, error-cell colour readout.

Measured after the change (1440×900, DIP): menu "File" text x 16.8 · title x 16 · Add line x 16 · grid x 16 · status text x 16 · totals right edge = grid right edge (1409.6); vertical: menu 28 → title +12 → command bar +8 → grid +12 → status bar +12. Contrast (tokens.py): error link `#B42318` on the bar `#EEF0F3` 5.76:1; error cell text `#1B1F24` on `#FDECEA` 14.48:1 (was drawn under a 55 % tint before); warning caption 5.77:1.

## First-render defects (`render/first-*`)
| # | type | defect |
|---|---|---|
| 1 | implementation-bug | the focused-row error message in the status bar was clipped ("Line 40: Quantity must be gre") — horizontal StackPanel gives infinite width so `TextTrimming` never applied |
| 2 | visual | fallback message used the property name ("Line 250: ItemCode: Item is required.") |

Everything else rendered as intended on the first build: solid error tint behind readable text, aligned insets, uniform separators, F8 navigation.

## Final defects (`render/final-*`)
| # | type | defect |
|---|---|---|
| 1 | visual (minor) | menu text lands at x = 16.8, not 16 (default `MenuItem` header padding is not on the 4 px grid; 0.8 DIP) |
| 2 | visual (minor) | the focused-row message sits at the end of the left status segment (after "unsaved") because it is the DockPanel fill child; reading order would prefer it next to the error count |
| 3 | existing-system (untouched) | empty/loading overlays keep the literal `Margin="1,33,1,1"` header offset; Dark / High-contrast dictionaries still absent |
Not verified: Narrator/NVDA reading of `HelpText`, 150/200 % DPI, high contrast.

## Iterations
2 renders (first → fix → final). Fix: left status segment became a DockPanel with the message as the trimmed fill child (tooltip carries the full text); key hints hide while a message is shown; message text uses `ErrorSummary` (messages only).

## Interaction test summary (`render/final-ready-1440x900.json`, native, real OS keys)
21 steps, all as expected, none regressed from Phase 3: arrows, F2, Enter commits/moves, Tab/Shift+Tab without edit-mode trap, type-to-edit, Escape, qty 0 → row error (`Line 50: Quantity must be greater than 0.` in the status bar; cell background `#FDECEA`, foreground `#1B1F24`), Up shows `Line 40: …`, **F8 → line 50 Qty, F8 → line 160 Requested ("Requested date is in the past."), Shift+F8 → line 50**, Shift+Down ×2 selects 3, Ctrl+End keeps the header at y 119.2, Enter on the last row adds line 250 (message "Line 250: Item is required."), F6 cycle filter → command bar → grid, Ctrl+F. Numeric columns right/tabular, text columns left. Columns hidden 0 / 4 / 7 at 1440 / 1100 / 820; status bar never overflows at 820 (`Total 89,307.97 AED` flush with the grid edge).

## Preservation verdict
Navigation, theme (no new brushes — `Feedback.Error`, `Feedback.Error.Bg`, `Focus.Ring`, `Bg.Header` reused), typography, and the component language (Btn.*, Text.* roles, Grid.* styles) kept; the one new style (`Btn.Status.Link`) is a caption-sized text button in the same tokens. No structural change: the same bands, the same status segments in the same order plus one. `preservation-ok`.

## Regressions to propose
- "polish inconsistent spacing in the toolbar and status bar of a WPF screen" → bundle contains `anti-inconsistent-spacing` and `layout-spacing-scale`; no states record; components include toolbar / status bar.
- "validation errors are hard to read in an editable data grid" → bundle covers the accessibility concern with `a11y-forms-errors` and `a11y-color-not-only`; `comp-data-entry-grid` (per-cell validation with a summary) retained.
- "polish this existing screen …" (budget low) → direction fills no `imagery`/`metadata` slot with a new visual device (data graphics, badges) unless the request or repository supports it.
- inspect_project on a WPF project with `<FontFamily x:Key="Font.UI">` → typography KNOWN (family, mono, scale).

## Tags
`context-detection-miss` (typography), `requirements-miss` (components/screen), `ranking-miss` (a11y-forms-errors, a11y-color-not-only), `knowledge-gap` (status bar, grid validation display, WPF adorner z-order), `direction-mismatch` (dashboard-grid / data-graphics / badges on a polish task), `render-defect-fixed`, `render-defect-remaining`, `skill-helped` (anti-inconsistent-spacing + desktop-keyboard-first + comp-form's WPF line + tokens.py contrast), `preservation-ok`.
