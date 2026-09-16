# WPF (including DevExpress / MahApps / Material Design in XAML / WinForms interop)

Read `platforms/desktop.md` first.

## Conventions to detect and respect
- Theme source: `App.xaml` merged dictionaries, `Themes/Generic.xaml`, third-party theme packs (DevExpress themes, MahApps, MaterialDesignThemes), `DynamicResource` keys for brushes; MVVM framework (Prism, CommunityToolkit.Mvvm, Caliburn), `RoutedUICommand`/`ICommand` usage, `DataTemplate`s per view model, existing custom controls and `Style`s with `x:Key`.
- DevExpress presence (`DevExpress.Wpf.*`): `GridControl`/`TableView`, `RibbonControl`, `DockLayoutManager`, `NavigationFrame`, `ThemeManager`: use them, not parallel controls.

## Implementation rules
- Tokens: semantic brushes as `DynamicResource` (`Brush.Bg.Canvas`, `Brush.Text.Primary`, `Brush.Action.Primary` …) defined per theme dictionary (Light/Dark/HighContrast); text `Style`s per role (`Text.Body`, `Text.Title`); never literal colours in views; check `SystemParameters.HighContrast`.
- Shell: menu bar (`Menu` with `InputGestureText`, `_` access keys), `ToolBar` for frequent commands, `ContextMenu` per object bound to the same commands, left navigation as a styled `ListBox`/`TreeView` or DevExpress `NavBar/Accordion`, `Grid` + `GridSplitter` panes with persisted widths, docking via DevExpress/AvalonDock if present.
- Data: `DataGrid` with `EnableRowVirtualization`, `VirtualizingPanel.IsVirtualizingWhenGrouping`, column widths persisted, `ScrollViewer.CanContentScroll`; DevExpress `GridControl` with `TableView` (already keyboard-complete, editing, totals, band columns) when present; `TreeView` with `HierarchicalDataTemplate` and virtualisation; numeric columns right-aligned with `StringFormat`.
- `DataGrid` pitfalls (seen in a real build, 2026-09-09): `IsSynchronizedWithCurrentItem` with an `ICollectionView` collapses multi-selection to the current item, leave it unset for bulk actions; Tab out of an editing cell into a `DataGridComboBoxColumn` keeps edit mode, commit with `CommitEdit(DataGridEditingUnit.Row, true)` on `PreviewKeyDown`; `Validation.HasError` is raised on the editing element, not the cell, so style the `DataGridCell` via a trigger on `Validation.HasError` of its content or use `RowValidationErrorTemplate`; hide low-priority columns by an attached "hide below width" property driven by `SizeChanged` rather than by fixed `MinWidth`s.
- Forms: labels beside/above via a shared `Grid` column definition (`SharedSizeGroup`), `ValidatesOnNotifyDataErrors` with an `ErrorTemplate` that shows text, `IsDefault`/`IsCancel` buttons, tab order via `TabIndex`, `KeyboardNavigation.TabNavigation`.
- Keyboard: `InputBindings` (`KeyBinding`) for accelerators, `RoutedUICommand` gestures, `FocusVisualStyle` explicitly set on retemplated controls, `Keyboard.Focus` on dialog open.
- Accessibility: `AutomationProperties.Name/HelpText/LiveSetting`, `AutomationPeer` for custom controls, high-contrast theme dictionaries, DPI awareness (`PerMonitorV2`), text scaling tests.
- Motion: `Storyboard`s on opacity/transform only, `VisualStateManager` for control states, `SystemParameters.ClientAreaAnimation` respected.
- Persistence: user settings for window geometry, splitter positions, grid layouts (DevExpress `SaveLayoutToXml`).

## Verification
Run at minimum size and maximised, 150/200% DPI, themes including High Contrast, keyboard-only pass, Narrator/NVDA; check binding errors in the Output window; snapshot screenshots per state.
