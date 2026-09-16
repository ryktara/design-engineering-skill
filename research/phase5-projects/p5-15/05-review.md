# Accessibility review — Stock adjustments page (WinUI 3)

Task (verbatim): "Review the stock adjustments page against our accessibility checklist."

Scope: `project/Views/StockAdjustmentsPage.xaml`, `StockAdjustmentsPage.xaml.cs`, `ViewModels/StockAdjustmentsViewModel.cs`, `Converters/*.cs`, shell (`MainWindow.xaml`, `App.xaml`). Stack: Windows App SDK 1.7 / WinUI 3, CommunityToolkit.WinUI.UI.Controls.DataGrid 7.1.2, CommunityToolkit.Mvvm 8.4.

Method: static code review against WCAG 2.2 A/AA plus the Windows accessibility guidance (UI Automation, Narrator, text scaling, high contrast). Where a claim depends on control internals, it was checked against the Toolkit 7.1.2 source (`DataGrid.cs`, `DataGrid.xaml`, `Automation/DataGridColumnHeaderAutomationPeer.cs`, `Automation/DataGridCellAutomationPeer.cs`) and Microsoft Learn (Custom automation peers; Accessibility Insights UWP XAML samples; Text scaling; InfoBar). The project does not build on this machine (no Windows App SDK build workload, see Phase 3 notes), so nothing was verified with Narrator or Accessibility Insights; every finding says what would confirm it.

Severity scale: **Blocker** = a WCAG A/AA failure on the page's primary path with no equivalent; **Major** = A/AA failure with a workaround, or a promised accessibility behaviour that does not exist; **Moderate** = AA/best-practice gap; **Minor** = polish. Only Blockers were fixed (protocol rule); the fixes are listed at the end.

## Summary

| # | Finding | WCAG / Windows reference | Severity | Fixed |
|---|---|---|---|---|
| F1 | Four numeric column headers have no UI Automation name | 1.3.1 Info and Relationships (A); 4.1.2 Name, Role, Value (A) | Blocker | yes |
| F2 | The three live regions never announce; InfoBar announces only the first message and disappears for good once closed | 4.1.3 Status Messages (AA) | Blocker | yes |
| F3 | Row-action buttons are not reachable by keyboard inside the grid; the F1 dialog says they are | 2.1.1 Keyboard (A) — equivalent path exists; 3.3.2 / help accuracy | Major | no (documented) |
| F4 | Status cell: accessible name "Status: Pending approval" is set on a StackPanel and the cell itself gets no name | 1.3.1 (A) — text still conveyed | Major | no |
| F5 | Fixed `RowHeight="36"` / `ColumnHeaderHeight="36"` and fixed widths clip text at Windows text scaling 150–225 % | 1.4.4 Resize Text (AA); Windows text-scaling guidance | Major | no |
| F6 | Status filter: blank "any" item with no name; enum values shown/announced as `PendingApproval`, `CycleCount` | 2.4.6 Headings and Labels (AA); 3.1.5 readability (best practice) | Moderate | no |
| F7 | `RowActionButton` style hard-codes `Transparent` background/border in every theme, including High Contrast | 1.4.11 Non-text Contrast (AA); Windows High Contrast guidance | Moderate | no |
| F8 | Initial focus is programmatic (no focus visual) and is lost when the grid is collapsed (empty state) | 2.4.7 Focus Visible (AA); 2.4.3 Focus Order (A) | Moderate | no |
| F9 | Filter row is not a landmark/group; Narrator landmark navigation cannot reach it | 2.4.1 Bypass Blocks (A, partially met by F6 pane cycling) | Minor | no |
| F10 | Sort state is not exposed to UIA and not announced | 4.1.2 (A, best practice for grids) | Minor | no |
| F11 | Loading state never announced; `IsLoading` is never set | 4.1.3 (AA) — currently dead code | Minor | no |
| F12 | Access key `J` for Reject does not match a letter in the label | Windows access-key guidance | Minor | no |

Passing checks (evidence in "What passes" below): text contrast, colour-not-only for status and signed quantities, names on every icon-only control, visible labels on inputs, heading level, keyboard accelerators with documentation, dialog focus return, no custom motion, tabular figures, focus visuals on custom-styled buttons, theme resources instead of literal colours.

## Findings

### F1 — Numeric column headers have no accessible name (Blocker, fixed)

Evidence (before/ copy, `Views/StockAdjustmentsPage.xaml` lines 235–277): the Before, Change, After and Value (EUR) columns set the header as an element:

```xml
<controls:DataGridTemplateColumn Width="76" Tag="QuantityBefore" CanUserSort="True">
    <controls:DataGridTemplateColumn.Header>
        <TextBlock Text="Before" Style="{StaticResource NumericHeader}" />
    </controls:DataGridTemplateColumn.Header>
```

Toolkit 7.1.2 `DataGridColumnHeaderAutomationPeer.GetNameCore()` (lines 83–92) returns the header only when `OwningHeader.Content is string`; otherwise it falls back to `base.GetNameCore()`, which is empty because nothing sets `AutomationProperties.Name` on the header element. Consequence: the UIA Table pattern reports four header items without a name; Narrator in table navigation announces "column 7" and the value with no header, so a screen-reader user cannot tell Before from After or Change from Value. Four of eleven visible columns, including the ones an approver needs most.

Fix applied: `Header="Before"` (string) plus a `HeaderStyle` (`TargetType="primitives:DataGridColumnHeader"`, `HorizontalContentAlignment="Right"`); the Toolkit header template binds `HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"` (`DataGrid.xaml` line 572), so the right alignment is kept. Verify at build: the style has no `BasedOn`; the default style comes from the Toolkit's generic dictionary via `DefaultStyleKey`, so the template should still apply — confirm with Inspect that the four headers now have names and the text is right-aligned.

### F2 — Live regions never announce; InfoBar announces once (Blocker, fixed)

Evidence: three elements carry `AutomationProperties.LiveSetting="Polite"` (result summary line 71, selection label line 84, InfoBar line 165) and neither the code-behind nor the view model ever calls `RaiseAutomationEvent(AutomationEvents.LiveRegionChanged)` (grep: no `AutomationPeer`/`RaiseAutomationEvent` in the project). Microsoft's Accessibility Insights sample for UWP/WinUI XAML states: "In order for a screen reader to be made aware of the change to the LiveRegion, a LiveRegionChanged event must be raised in code-behind. Always raise the event after the updated text has been set on the TextBlock." So the "12 of 8 adjustments match the current filters" summary and the "Selected: ADJ-10421" label are silent when filters or selection change — the exact status messages the page was designed around.

InfoBar: WinUI raises the notification on the closed-to-open transition only (docs: "Once the control is open, any changes … will not raise a notification event … close and re-open the control to trigger the event"). `IsOpen` is bound one-way to `HasMessage`; the view model set `Message` directly, so a second Approve while the bar was open changed the text silently, and after the user closed the bar (`IsOpen` becomes false locally) `HasMessage` stayed true and no later message ever reopened it — no feedback at all, for anyone.

Fix applied: `x:Name` on the two TextBlocks; the page subscribes to `ViewModel.PropertyChanged` in `Loaded` (after the x:Bind listener, so the text is already updated) and raises `LiveRegionChanged` for `ResultSummary` / `SelectionLabel`; the view model routes approve/reject feedback through `Notify()` which sets `Message = null` before the new text so `HasMessage` toggles and the InfoBar closes/reopens (announced, and visible again after a manual close). Verify with Narrator: change a filter, arrow through rows, approve twice, close the bar and approve again.

Note on chatter: the selection label announces on every arrow key in addition to Narrator's own row announcement. If that proves noisy in testing, drop the live event for `SelectionLabel` and keep it for `ResultSummary`.

### F3 — Row-action buttons are keyboard-unreachable inside the grid; help text says otherwise (Major)

Evidence: `StockAdjustmentsViewModel.Shortcuts` line 46 lists "↑ ↓ Home End — Move between rows; → ← reach the row actions". Nothing in the code-behind moves focus into a cell's content. Toolkit `DataGrid.cs` line 407 sets `TabNavigation = KeyboardNavigationMode.Once`; `ProcessTabKey` (lines 7671–7692) in a read-only grid moves focus to the column header and then out of the grid; Left/Right only change the current cell. So the 24 `Button`s in the Actions column are visible but a keyboard user cannot Tab or arrow to them; only Narrator scan mode or a mouse reaches them.

Not a 2.1.1 failure: every row action has a keyboard equivalent on the selected row (Ctrl+Shift+A / R, F2, and the `ContextFlyout` on Shift+F10), and the buttons' names ("Approve ADJ-10421") are correct for pointer/AT users. It is a Major because the page's own keyboard reference promises a path that does not exist, and the Phase 3 interaction test "passed" this only in the HTML twin.

Recommended fix (pick one): correct the F1 text to "→ ← move between columns; use the commands or Shift+F10 for row actions", or handle `PreviewKeyDown` on the DataGrid so Right/Enter on the Actions cell focuses the first enabled button and Escape returns to the cell (`grid-single-tab-stop` record's WinUI note describes the same shape).

### F4 — Status cell name is set on a Panel (Major)

Evidence: line 215–216, `AutomationProperties.Name="{x:Bind Status, Converter=…, ConverterParameter=Name}"` on a `StackPanel`. Microsoft Learn (Custom automation peers): "Border and Panel-based layout types such as Grid and Canvas do not [expose automation peers] … its meaningful child elements are surfaced through the nearest ancestor that has a peer." `DataGridCellAutomationPeer.GetNameCore()` (lines 121–160) names a cell only from a direct `TextBlock`/`TextBox` content, a bound column, or `ClipboardContentBinding`; a template column with a StackPanel has none of these, so the cell's name is empty and Narrator reads the child TextBlock "Pending". Status is still conveyed as text (colour-not-only holds), which is why this is not a Blocker, but the intended "Status: Pending approval" name is lost and the icon's `AccessibilityView="Raw"` is doing the only work.

Recommended fix: on the Status column set `ClipboardContentBinding="{Binding Status, Converter={StaticResource StatusPresentation}, ConverterParameter=Name}"` — deterministic per the peer source, and it also gives a sensible copy/paste value. Confirm with Inspect whether XAML created a peer for the named StackPanel (undocumented); either way the cell name is what table navigation reads.

### F5 — Fixed heights and widths versus text scaling (Major)

Evidence: `RowHeight="36"`, `ColumnHeaderHeight="36"` (lines 181, 183); numeric columns 76/88 epx; filter `TextBox Width="280"/"140"`, `ComboBox Width="180"` in a non-wrapping horizontal `StackPanel` (lines 142–159). Windows text scaling runs 100–225 % and applies to WinUI text automatically ("hard-coded control heights … you likely have to make some updates"). At 200 % the 14 epx body becomes 28 epx with a ~37 epx line box inside a 36 epx row: descenders clip; at 225 % all rows clip and "12,650" no longer fits 76 epx. The Toolkit row template already has `MinHeight="32"` on the cells presenter, so auto-sizing is safe.

Recommended fix: remove `RowHeight`/`ColumnHeaderHeight` (auto rows; verify density at 100 % stays ~36 with the 8 epx cell padding) or scale them from `UISettings.TextScaleFactor`; give numeric columns `MinWidth` instead of `Width` and let Description absorb the rest; let the filter row wrap (`ItemsWrapGrid`/a `Grid` with `Auto` columns and a second row below ~900 epx). Test at 150 %, 200 %, 225 % and at an 800×600 window.

### F6 — Status filter and Reason column show enum identifiers (Moderate)

Evidence: `StatusOptions` is `AdjustmentStatus?[] { null, Draft, PendingApproval, … }` (VM line 16–17) bound to a `ComboBox` with no `ItemTemplate`/converter; the `null` item renders as an empty row and has no accessible name, and `PendingApproval` is displayed and announced as one word. `DataGridTextColumn Binding="{Binding Reason}"` (line 232) shows `CycleCount`. Screen-reader users hear a non-word; sighted users see developer identifiers.

Recommended fix: a small `DisplayName` converter or `ItemTemplate` ("Any status", "Pending approval", "Cycle count"), reused by the Reason column.

### F7 — Hard-coded transparent chrome in High Contrast (Moderate)

Evidence: `RowActionButton` style (lines 37–44) sets `Background="Transparent"` and `BorderBrush="Transparent"` as plain values. Local style setters apply in every theme, so under a High Contrast theme the three icon-only buttons per row lose the button boundary the default `ButtonBackground`/`ButtonBorderBrush` theme resources would provide; the disabled Approve/Reject buttons on Posted/Rejected rows become indistinguishable from enabled ones. Non-text contrast fails in that theme only.

Recommended fix: move the two setters into a `ResourceDictionary.ThemeDictionaries` with Light/Dark = Transparent and no High Contrast override, or use `{ThemeResource SubtleFillColorTransparentBrush}`-style resources that carry a HighContrast entry.

### F8 — Initial focus (Moderate)

Evidence: `Grid.Focus(FocusState.Programmatic)` in `Loaded` (code-behind). WinUI draws focus visuals only for keyboard focus state, so after navigation the grid has focus with no visible indicator until the first key press; and when the list is empty the DataGrid is `Collapsed` (line 189), `Focus` fails, and focus stays on the Frame — a keyboard user's first Tab lands somewhere unpredictable.

Recommended fix: focus the grid with `FocusState.Keyboard` when it is visible, else the empty-state action button; keep the heading `Level1` for Narrator heading navigation.

### F9 — Filters region has no landmark (Minor)

Evidence: `CommandBar` is named ("Stock adjustment commands"), the grid is named; the `Filters` StackPanel is not. F6/Shift+F6 cycling exists (code-behind `FocusRegion`) so keyboard users can reach it; Narrator landmark navigation cannot. Recommended: `AutomationProperties.LandmarkType="Custom"` + `LocalizedLandmarkType="Filters"` on the panel (the Accessibility Insights sample does exactly this on a StackPanel).

### F10 — Sort state not exposed (Minor)

`Grid_Sorting` sets `SortDirection` (visual arrow) and re-sorts in the view model; the Toolkit header peer exposes no sort pattern, so nothing tells AT which column is sorted or that the order changed. Recommended: append the sort to the result summary ("… sorted by Status, descending") so the live region (now working) carries it.

### F11 — Loading never announced (Minor)

`ProgressRing` has a name but no live region and `IsLoading` is never set true (`Refresh` → `Load` is synchronous). Harmless today; when a real data source arrives, announce completion through the result summary.

### F12 — Access key `J` for Reject (Minor)

`AppBarButton Label="Reject" AccessKey="J"` (line 103): Windows shows the key tip, so it is operable, but users expect a letter from the label (`R` is taken by Refresh; `E` or `T` are free).

## What passes

- **Contrast (1.4.3 / 1.4.11)**: all brushes are theme resources; Phase 3 measurements of the same values: body 17.2:1, secondary 6.19:1, caution 5.25:1, success 5.44:1, critical 5.66:1, accent 5.38:1 on the card background — AA for text and 3:1 for the status glyphs and signed quantities in Light; Dark uses the WinUI dark counterparts of the same resources.
- **Colour not only (1.4.1)**: status = glyph + text + colour (`StatusToPresentationConverter`); quantity change = explicit sign (`SignedNumberConverter` "+N0", true minus U+2212) + colour; InfoBar severity carries icon + text.
- **Names (4.1.2)**: every icon-only row button has `AutomationProperties.Name="Approve ADJ-10421"` via `RowActionNameConverter`; `AppBarButton`s have labels; the grid, command bar and progress ring are named; the status glyph is `AccessibilityView="Raw"`.
- **Labels (3.3.2)**: `TextBox`/`ComboBox` use `Header` (WinUI forwards it as the UIA name); placeholders are format hints only.
- **Headings (1.3.1)**: page title `HeadingLevel="Level1"`.
- **Keyboard (2.1.1, 2.4.3)**: CommandBar accelerators with tooltips and access keys; Ctrl+F, Esc scoped to the search box, F2, F5, F6/Shift+F6 pane cycling, Shift+F10 context flyout; all listed in the F1 dialog (except the F3 inaccuracy). No keyboard trap: `ContentDialog` has `DefaultButton="Close"` and returns focus to the invoker.
- **Focus visible (2.4.7)**: `UseSystemFocusVisuals="True"` on the custom button style; DataGrid keeps its own cell focus visual; no `UseSystemFocusVisuals=False` anywhere in the page (the Phase 3 defect is gone).
- **Motion (2.3.3)**: no custom animations; WinUI honours the system animation setting.
- **Tabular figures**: `Typography.NumeralAlignment="Tabular"`, right-aligned numeric cells, one precision per column.
- **Target size (2.5.8)**: row buttons 28 epx ≥ 24 epx minimum (below the WinUI 32 epx control height, accepted for density).
- **Persistence**: "Created by" column visibility persisted in `LocalSettings`; selection preserved across refresh by key.

## Fixes applied (Blockers only)

Files changed (copies of the originals in `before/`):

- `Views/StockAdjustmentsPage.xaml` — F1: four numeric columns use string `Header` + `HeaderStyle="{StaticResource NumericHeader}"` (`primitives:DataGridColumnHeader`, right-aligned content); new `xmlns:primitives`. F2: `x:Name="ResultSummaryText"` / `"SelectionLabelText"`.
- `Views/StockAdjustmentsPage.xaml.cs` — F2: `ViewModel_PropertyChanged` raises `AutomationEvents.LiveRegionChanged` on the two TextBlocks; subscribed in `Loaded` (after x:Bind), idempotent.
- `ViewModels/StockAdjustmentsViewModel.cs` — F2: `Notify(severity, text)` toggles `Message` null → text so `HasMessage` transitions and the InfoBar re-opens and announces.

Visible output is unchanged (header text and alignment identical; the HTML twin in `render/` renders the same before and after). Not verified: XAML compile and Narrator behaviour (no Windows App SDK build workload on this machine) — run Accessibility Insights for Windows on the built page to confirm F1/F2 and to settle F4.

## Suggested checklist order for the next pass

F3 (fix or reword, 15 min) → F4 (one attribute) → F5 (text scaling, needs a visual pass at 100/150/200 %) → F6 → F7 → F8 → F9–F12.
