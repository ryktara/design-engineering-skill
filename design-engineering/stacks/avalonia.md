# Avalonia UI (Windows, macOS, Linux; mobile/browser where targeted)

Read `platforms/desktop.md` first.

## Conventions to detect and respect
- Theme: Fluent (`FluentTheme`) or Simple theme, `ThemeVariant` (Light/Dark), resource dictionaries with `DynamicResource` brushes, `Styles`/`ControlTheme`s with selectors; MVVM (CommunityToolkit.Mvvm/ReactiveUI), `.axaml` views, `TreeDataGrid`/`DataGrid` packages, `Avalonia.Controls.Notifications`, icon packs.

## Implementation rules
- Tokens: semantic brushes per `ThemeVariant` in `ResourceDictionary.ThemeDictionaries`; text `ControlTheme`s per role; never literal colours in views; validate light/dark with `tokens.py`.
- Shell: `NativeMenu` (macOS) / `Menu` with hot keys (`HotKey`), `SplitView` for a collapsible navigation pane, `TabControl` for documents, `ContextMenu`/`ContextFlyout` per object, `Grid` + `GridSplitter` panes with persisted sizes, `WindowState`/size persisted.
- Data: `TreeDataGrid` for large flat or hierarchical data (virtualised, sortable, keyboard), `DataGrid` for simpler tables, `ItemsControl`/`ListBox` with `VirtualizingStackPanel`, `AutoCompleteBox` for search/palette; numeric alignment via `TextAlignment="Right"` and formatting.
- Keyboard: `KeyBindings`/`HotKey`, `TabIndex` and `KeyboardNavigation` attached properties, `IsDefault`/`IsCancel` on dialog buttons, `FocusAdorner` kept visible for keyboard focus; access keys via `_` in headers.
- Accessibility: `AutomationProperties.Name/HelpText`, `AutomationPeer` for custom controls; platform screen readers (Narrator/VoiceOver/Orca) pass.
- Motion: `Transitions` on opacity/transform, `Animation` keyframes sparingly; respect OS reduce-motion where available.
- Responsive: `OnFormFactor`/`OnPlatform` markup, adaptive `Grid` definitions; minimum window size set.

## Verification
Run on the primary desktop OS at min/max sizes and DPI scaling, Light/Dark, keyboard-only pass, screen reader check; screenshots per state; cross-platform check on the other targeted OS if available.
