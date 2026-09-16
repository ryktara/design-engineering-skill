# p6-23 — "Review the supplier invoice matching page for keyboard operability."

**Project** `research/phase3-projects/p3-winui-erp-audit/project` · **Stack** WinUI 3 (WindowsAppSDK 1.7, CommunityToolkit.Mvvm 8.4, CommunityToolkit.WinUI DataGrid 7.1.2, .NET 9) · **Platform** desktop
**Existing UI** yes (App shell + StockAdjustmentsPage are a finished, audited design system) · **New screen** yes — see below.
**Build hash** start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` ✅

## The page the sentence names does not exist

`MainWindow.xaml` declares a `NavigationViewItem Content="Invoices" Tag="Invoices"`, but `Nav_SelectionChanged`
has no `"Invoices"` arm: the tag falls through `_ => typeof(StockAdjustmentsPage)`, so selecting **Invoices**
marks Invoices as the current location in the pane while the frame shows Stock adjustments. `Views/` contains
only `OrdersPage` (a one-line stub) and `StockAdjustmentsPage`. There is no supplier invoice matching page to
review. Since a review task must end in implemented fixes, the screen was built to the conventions the audited
`StockAdjustmentsPage` already establishes, with keyboard operability as the design driver, and the routing bug
was fixed. `StockAdjustmentsPage` / its view model / its converters were **not touched** (another task owns them).

## 1. Design context (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | `menu-bar` | INFERRED | `NavigationView` left rail (`PaneDisplayMode="Auto"`, 4 MenuItems + header) in MainWindow; the CommandBar is a page-level toolbar, not the shell navigation | **no** — candidates show `left-rail: 3` but the 13 CommandBar/MenuFlyout hits on one page won |
| theme | `dual-theme` | INFERRED | App.xaml ThemeDictionaries Light/Dark + ThemeResource brushes throughout | yes |
| surfaces | `bordered-flat` | INFERRED | 1 px `CardStrokeColorDefaultBrush` border + `CardBackgroundFillColorDefault`, no shadows; Mica on the window | yes |
| radius | `unknown` | UNKNOWN | `{StaticResource OverlayCornerRadius}` and `ControlCornerRadius` are used explicitly | partial |
| spacing | `4` | INFERRED | 4 epx grid (2/6/8/12/16), 36 epx rows | yes |
| typography | `unknown`, `tabular_numerals: false` | UNKNOWN | no font family (correct — WinUI theme styles), but `Typography.NumeralAlignment="Tabular"` is set on the numeric style and Title/Subtitle/Body/Caption styles are used as a scale | partial — the "no tabular numerals" half is wrong |
| components | `winui3, community-toolkit` | KNOWN | exact | yes |

## 2. Requirements (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform / `platform_evidence` | `desktop`, evidence `[]` (from project inspection) | correct |
| `intent.artifact_state` | `existing` | correct for the sentence; the code says otherwise, which no input the skill has could reveal |
| `intent.operations` | `["review"]` | correct |
| `intent.problem_domain` | `["interaction"]` | correct |
| `intent.change_scope` | `screen` | correct |
| mode / `mode_evidence` | `["audit","review"]`, "explicit: review the" | correct (expected review/audit/accessibility) |
| `scope.kind` | `in-scope`, "UI design / interaction task" | correct |
| `change_budget` | `low` | correct |
| `intent.preserve` | `[]` (but `constraints.preserve_existing_system: true`) | acceptable |
| `project_context` | carries the wrong `navigation` value forward | see above |
| other | `screen: []` — "invoice matching page" was not resolved to a table/master-detail screen, which is why every table/component record was later dropped for "no positive task evidence" | miss |

## 3. Guidance (`03-guidance.md` / `.json`) — status PARTIAL, bundle 2 (core 0 + guardrails 2), 245 tokens

| record | layer | verdict | category |
|---|---|---|---|
| `desktop-keyboard-first` | CRITICAL GUARDRAIL | **relevant** — SPECIFIC; F6 pane cycling, Ctrl+F, grid arrow/Ctrl+Shift selection, dialog default+cancel, access keys on Alt | — |
| `typo-scale-and-roles` | CRITICAL GUARDRAIL | **partial** — true, but it is type-scale advice on a keyboard-operability review with `change_budget: low` and typography a preserved slot | `generic` |

OPTIONAL NOTES layer absent (valid). `layer_review`: core `[]`, critical `[typo-scale-and-roles, desktop-keyboard-first]`, optional `[]` (0 useful / 0 noise).

**Concept recall** — delivered = union of the two records' concepts = `table.tabular_figures`, `brand.type_roles`, `interaction.keyboard_navigation`, `interaction.shortcuts`, `interaction.focus_visible`.

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| interaction.keyboard_navigation | yes | — |
| interaction.focus_visible | yes | — |
| interaction.shortcuts | yes | — |
| a11y.accessible_names | no | `bundle-selection` — `a11y-labels-names` (0.243) and `a11y-native-semantics` (0.297) were candidates and were dropped |
| interaction.selection_visible | no | `expected-concepts` — never demanded |
| interaction.menu_semantics | no | `expected-concepts` — never demanded |
| a11y.dialog_focus | no | `expected-concepts` — never demanded |

Recall **3/7 = 0.43**; critical recall **3/3 = 1.00**. No forbidden concept appeared (no touch/TV/D-pad contamination; the six off-platform records were correctly filtered).

Two structural observations:
- `a11y-keyboard-operable` is the single best-matching record in the base for this sentence (`search` ranks it **first**, 0.45, above `desktop-keyboard-first` at 0.438) and it never reaches the bundle. Not a knowledge gap — a selection result.
- The skill marks `table.tabular_figures` **critical** for a keyboard-operability review. That one decision is what pulled a GENERIC typography record into a 2-record bundle instead of an accessibility record, and it is why `covered_required_concerns` is `[interaction, data-display]` while the two *uncovered* required concerns are `accessibility` and `component`.

PARTIAL_SCOPE note: status is `PARTIAL` because of concern coverage (0.5), not a design/engineering split — nothing to judge there.

## 4. Direction (`04-direction.md/json`)

13 slots, **all `preserved`, 0 `changed`, 0 `new`** → `unjustified_direction_slots: 0` (expected 0 on an existing UI with a low budget). Validation `OK`. `preservation` metrics: budget `low`, preserved list covers navigation/layout/density/surface/cards/typography/color/motion/focus/cta/imagery/icon/metadata.
The focus slot says the right thing ("keep and verify the existing indicator: ≥ 3:1, visible in every theme and state") — that is the most useful line the direction produced.
The navigation slot is wrong through the context miss: it recommends `nav-menu-bar-desktop` ("menu bar for the complete command set") for a shell that is a `NavigationView` rail. I preserved the rail, which is what "preserve the existing system" actually means here, so the wrong label cost nothing.

## 5. Implementation

Created (new files, no `before/` copy applies):
- `Models/SupplierInvoice.cs` — `SupplierInvoice`, `InvoiceMatchLine`, `MatchStatus`.
- `ViewModels/InvoiceMatchingViewModel.cs` — master/detail, filters, `Match` / `Hold` / `AcceptVariance` / `Refresh` / `ClearFilters`, `Shortcuts` list, live-region summary strings; reuses `BulkObservableCollection<T>` and `ShortcutInfo`.
- `Converters/MatchStatusToPresentationConverter.cs` — same Text/Glyph/Brush/Name contract as the existing `StatusToPresentationConverter`.
- `Views/InvoiceMatchingPage.xaml` + `.xaml.cs`.

Changed (copied to `before/`):
- `MainWindow.xaml.cs` — added the `"Invoices" => typeof(InvoiceMatchingPage)` arm.

Keyboard operability as shipped: every command on the command bar **and** the row context menu **and** an accelerator (Ctrl+M match, Ctrl+Shift+A accept variance, Ctrl+H hold, F5 refresh, Ctrl+Shift+L clear filters, Ctrl+F search, Escape scoped to the search box, F1 shortcut reference); access keys on Alt for all of them; F6 / Shift+F6 cycles the four regions (commands → filters → invoices → match lines); each DataGrid is one tab stop with arrow-key row movement; initial focus lands on the master grid, not on chrome; `AutomationProperties.Name` on both grids, both status cells (glyph marked `AccessibilityView="Raw"`), and the command bar; three polite live regions raised from code-behind (`LiveRegionChanged`, because XAML `LiveSetting` alone is not announced); the F1 `ContentDialog` has a default button and restores focus to its invoker.

**Guidance used**: `desktop-keyboard-first` (F6 pane cycling, Ctrl+F, grid arrow/Ctrl+Shift selection, dialog default+cancel, access keys on Alt, "document shortcuts in menus and tooltips").
**Guidance ignored**: `typo-scale-and-roles` — typography is a preserved slot at `change_budget: low`; the project inherits the WinUI type ramp and the numeric style already sets tabular figures. Following it would have meant generating a new scale for a screen whose task is keyboard operability.

**Process guidance check**: no. SKILL.md §2 (reuse → extend → compose → new) and §7 (render and inspect) were enough, and the sibling `StockAdjustmentsPage` is a stronger reuse signal than any record would have been. `process.reuse_first` was in fact *not surfaced* ("no sufficiently specific guidance"), and reuse was the single decision that shaped the whole implementation — so the bundle got no credit for it, but it also did not need to carry it. → `process_records_needed: false`.

## 6. Render — `render_mode: html-twin` (WinUI 3, no capture harness), Chromium 1280×800

`render/twin.html` mirrors the XAML structure, WinUI light theme resources and the App.xaml accent.
Screenshots: `first-desktop.png`, `first-shortcuts.png`, `final-desktop.png`, `final-shortcuts.png`. All four were looked at.

**First-render defects (4)**
| # | type | defect |
|---|---|---|
| 1 | visual | Master table overflowed its pane: at 1280 with the rail expanded the two-table split gives the master ~460 epx, and its six fixed columns need ~650 — the **Supplier** column disappeared and **Variance (EUR)** was cut in half. |
| 2 | visual | Detail table clipped the same way: `Variance (EUR)` ran off the right edge of the pane. |
| 3 | implementation-bug | `MatchLines` was a plain `ObservableCollection`, refilled with `Clear()` + n × `Add()`, while the page binds pane visibility and the empty state to `.Count` — the detail grid flickers through its empty state on every arrow-key move down the master list. The repo already has `BulkObservableCollection<T>` for exactly this. |
| 4 | implementation-bug | The pane divider was commented as a "keyboard-resizable splitter"; it is a 1 px decorative `Border` with no focus. A false accessibility claim in the source of a keyboard-operability screen. |

**Fixes (2 iterations)**
1. Master pane became a fixed 340 epx summary list — Status (96), Invoice/Supplier stacked in one 2-line cell with one accessible name (`*`, min 120), Variance (EUR) (116); the invoice total moved into the detail pane title. Detail pane takes the remaining width with trimmed columns. `MatchLines` → `BulkObservableCollection` + `Reset`. Divider comment corrected to say what it is.
2. Header text was still truncating ("Variance (E…", "Invoiced …", "Received …"): widened the master variance column, narrowed Status/Line/SKU, and shortened two detail headers to "Invoiced" / "Received" (the unit is in the pane title).

**Final defects (1)**
| type | defect |
|---|---|
| visual | Description cells in the detail grid still ellipsise at 1280 ("Hex bolt M8…"). Mitigated, not solved: the column is resizable and has `MinWidth="100"`. A wider window resolves it. |

No defect the guidance warned about was shipped.

## 7. Preservation

Navigation (NavigationView rail), Mica backdrop, dual theme via ThemeResource, WinUI type styles, 4 epx grid, 36 epx rows / 36 epx headers, bordered-flat surfaces with `OverlayCornerRadius`, status-as-glyph+text+colour, signed tabular numerics, command-bar + context-menu + accelerator triad — all inherited from the existing system. Converters, `BulkObservableCollection`, `ShortcutInfo` reused rather than re-created. No literal hex anywhere in the new XAML. `StockAdjustmentsPage` and its dependencies untouched. `unjustified_structural_change: 0`.

## 8. Skill misses, routed to the earliest layer

| layer | miss |
|---|---|
| `criticality` | `table.tabular_figures` is marked **critical** for a keyboard-operability review. It is not a keyboard concept; it is the reason a GENERIC typography record occupies half of a 2-record bundle. |
| `bundle-selection` | `a11y.accessible_names` uncovered although `a11y-native-semantics` / `a11y-labels-names` were candidates; `a11y-keyboard-operable`, the top-ranked record for this exact sentence in `search`, never entered the bundle. Accessible names on grid cells and icon-only buttons are half of what "keyboard operability" means on a WinUI DataGrid. |
| `expected-concepts` | `interaction.selection_visible`, `interaction.menu_semantics` and `a11y.dialog_focus` were never demanded — selection-vs-focus distinctness, Shift+F10 menu focus return, and dialog focus management are exactly what a keyboard review of a desktop table screen produces. |
| `project-context` | shell navigation detected as `menu-bar`; the app is a `NavigationView` left rail. Propagated into requirements, direction (`nav-menu-bar-desktop`) and the fingerprint. |
| `requirements` | `screen: []` — "invoice matching page" yielded no screen classification, so every table / master-detail / data-entry-grid record was omitted for "no positive task evidence", on a screen that is two tables. |

**Skill effect: neutral.** `desktop-keyboard-first` is a good, on-target record, but everything it says is already demonstrated one file away in `StockAdjustmentsPage`, which I was reusing anyway; nothing in the bundle changed a decision I would not otherwise have made. Nothing in the bundle was harmful either — `typo-scale-and-roles` was ignored without cost.

## 9. Regressions to propose

| query | expectation in words |
|---|---|
| "Review the supplier invoice matching page for keyboard operability." | Bundle contains `a11y-keyboard-operable` or `a11y-labels-names`; `a11y.accessible_names` is covered; `table.tabular_figures` is **not** critical for a keyboard/interaction review and `typo-scale-and-roles` does not enter the bundle. |
| Any keyboard/screen-reader review sentence naming a desktop table or grid screen | `interaction.selection_visible`, `interaction.menu_semantics` and `a11y.dialog_focus` are demanded as expected concepts. |
| `inspect_project` on a WinUI/WPF project whose shell is a `NavigationView`/`NavigationViewItem` set | `design_context.navigation` = `left-rail`, not `menu-bar`; page-level `CommandBar`/`MenuFlyout` hits must not outweigh shell navigation evidence. |
| `inspect_project` on a project setting `Typography.NumeralAlignment="Tabular"` | `typography.features.tabular_numerals` = true. |

**Tags**: `concept-miss`, `ranking-miss`, `context-detection-miss`, `requirements-miss`, `render-defect-fixed`, `render-defect-remaining`, `preservation-ok`, `partial-scope-ok`, `skill-neutral`, `direction-mismatch`
