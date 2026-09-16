# WinUI 3 / Windows App SDK (and UWP/Uno where applicable)

Read `platforms/desktop.md` first.

## Conventions to detect and respect
- `App.xaml` resources (`ResourceDictionary` theme resources, overrides of `AccentFillColorDefaultBrush`, `ControlCornerRadius`), MVVM (CommunityToolkit.Mvvm `ObservableObject`/`RelayCommand`), navigation (`Frame` + `NavigationView`), `x:Bind`, Community Toolkit controls (`DataGrid`, `SettingsCard`, `Segmented`, `GridSplitter`), Win2D/charts libraries, packaging (MSIX), `Uno.` for cross-platform.

## Implementation rules
- Shell: `NavigationView` (`PaneDisplayMode=Auto`, `MenuItems` grouped with headers, `FooterMenuItems` for settings/account, `IsBackButtonVisible` bound to the frame); `TabView` for documents; `BreadcrumbBar` for hierarchy; `CommandBar` (`AppBarButton` with `KeyboardAccelerator`, `Label`, `AccessKey`), `MenuBar` for full command sets, `ContextFlyout` per object.
- Layout: `Grid` star/auto sizing, `SplitView`/`GridSplitter` with persisted widths, `AdaptiveTrigger` at 641/1008 epx, `x:Load` for deferred panes, spacing in multiples of 4 epx (`Spacing`, `Margin`), 32 epx control height, `Mica` via `SystemBackdrop`, `Acrylic` only on flyouts.
- Tokens: `ThemeResource` brushes (`TextFillColorPrimaryBrush`, `CardBackgroundFillColorDefaultBrush`, `LayerFillColorDefaultBrush`, `ControlStrokeColorDefaultBrush`, `SystemFillColorCritical/Success/Caution`) and text styles (`CaptionTextBlockStyle` … `DisplayTextBlockStyle`); brand accent via `ResourceDictionary.ThemeDictionaries` overrides for Light/Dark/HighContrast; never literal colours in pages.
- Data: `DataGrid` (Toolkit) with `AutoGenerateColumns=False`, sorting, selection, `IsReadOnly` per column, `ItemsSource` virtualised; `ListView`/`ItemsView` with `ItemTemplate`s and `x:Bind`; `AutoSuggestBox` for search/palette; `InfoBar`/`TeachingTip` for feedback; `ContentDialog` one at a time with `DefaultButton`; `Expander`, `SettingsCard` for settings.
- Keyboard: `KeyboardAccelerator`s on commands, `AccessKey` on menus/buttons, `TabFocusNavigation`/`XYFocusKeyboardNavigation` for grids, `IsTabStop` discipline, F6 pane cycling via handlers; default/close buttons on dialogs.
- Accessibility: `AutomationProperties.Name/HelpText/LiveSetting/HeadingLevel`, `AutomationPeer` for custom controls, `UseSystemFocusVisuals`, high-contrast verified; Narrator pass; Accessibility Insights.
- Motion: built-in transitions (`ContentThemeTransition`, connected animations) and Composition animations on transform/opacity; respect `UISettings.AnimationsEnabled`.
- Persistence: `ApplicationData.LocalSettings` for window size, pane widths, column layouts, last selection.

## Verification
Run at 800×600 and maximised, DPI 150/200%, Light/Dark/High Contrast, keyboard-only pass, Narrator; screenshots of each state; XAML binding failures in output window.
