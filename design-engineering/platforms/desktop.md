# Desktop (Windows: WinUI 3, WPF, Avalonia, Uno; macOS; Electron/Tauri)

Pointer and keyboard, resizable windows, long sessions, expert users, dense information. Load for native desktop apps and desktop-first web tools.

## Contents
- Input model
- Window and layout
- Navigation and commands
- Density and spacing
- Data-heavy components
- Windows (Fluent) specifics
- macOS specifics
- State and persistence
- Performance
- Accessibility
- Checklist

## Input model

- Keyboard is first-class: accelerators for frequent commands (Ctrl+S, Ctrl+F, Delete with undo, F2 edit, F5 refresh), access keys for menus (Alt), Tab between groups and arrow keys within lists/grids/trees/toolbars, F6 between panes, Enter/Escape as default/cancel in dialogs; shortcuts shown in menus and tooltips; never collide with system or assistive-tech shortcuts.
- Pointer: hover states and tooltips are expected but never the only path; right-click context menus on every object mirroring the toolbar; double-click to open; drag with keyboard alternatives; precise targets ≥24 epx with 4–8 spacing.
- Touch on hybrids: keep targets usable (≥32 epx) but do not import phone sizing everywhere.

## Window and layout

- Minimum window size defined (e.g. 800×600 epx); breakpoints by window width (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order (inspector first, navigation to icons, then list); star/auto grid sizing, no absolute widths for content; DPI 100–300% tested; multi-monitor and window position/size restored per user.
- Topologies: master-detail, three-pane workbench, table-first, dashboard grid; content fills the window with internal scrolling per pane; splitters remembered.
- Title bar: system title bar unless a custom one keeps drag regions, caption buttons, and accessibility; Mica on Windows 11.

## Navigation and commands

- Section navigation: NavigationView-style left rail (collapsible to icons) for 6+ sections; top navigation for few sections; breadcrumb + tree for deep hierarchies.
- Commands: menu bar for document-centric apps (complete command set with accelerators), command bar/toolbar for the frequent subset, context menus per object, command palette (Ctrl+K) as an accelerator for power users. Commands are disabled by state, not hidden.
- Tabs for documents (closable, reorderable) vs. selector bars for section views.

## Density and spacing

4 epx grid; 8 between related controls, 12 between groups, 16 to edges; control height 32 epx (WinUI) / 22–28 pt (macOS); body 14 epx / 13 pt; table rows 32–36; high density is expected but text stays ≥12 epx and everything stays aligned. Offer compact/comfortable density where audiences differ.

## Data-heavy components

- Tables/grids: sticky headers, column resize/reorder/visibility persisted, sort indicators, multi-select with Ctrl/Shift, keyboard grid navigation, inline editing (F2/Enter/Escape), virtualisation, bulk actions in the command bar with a selection count, numeric alignment with tabular figures.
- Data-entry grids: predictable Enter/Tab movement, type-to-edit, lookup pickers (F4), per-cell validation with a summary, totals, paste from spreadsheets, undo.
- Trees: full keyboard semantics, lazy children, virtualisation beyond ~500 nodes, breadcrumb mirror.
- Forms: labels beside or above with consistent alignment, tab order = visual order, default button, validation summary, unsaved-changes guard.
- Charts: canvas rendering for large sets; keyboard-reachable values; data table alongside.

## Windows (Fluent) specifics

Use theme resources (text, control fill, accent, layer/card brushes) so light/dark/high-contrast work; Mica backdrop for the window, Acrylic only for transient surfaces; corner radius 8 epx top-level / 4 nested (`ControlCornerRadius`); Segoe UI Variable type ramp (Caption 12, Body 14, BodyStrong 14, Subtitle 20, Title 28, TitleLarge 40, Display 68); Segoe Fluent Icons; NavigationView, CommandBar, MenuBar, TabView, InfoBar, TeachingTip, ContentDialog (one at a time), Flyouts; `KeyboardAccelerator` and `AccessKey`; `AutomationProperties` on everything custom; respect the system accent unless brand-locked.

## macOS specifics

Menu bar with the standard menus, toolbar with customisation, sidebar with source-list styling, inspector panels, sheets attached to windows, SF Symbols, system font, Full Keyboard Access, NSAccessibility; respect the window/traffic-light conventions; native controls over custom.

## State and persistence

Restore window geometry, pane widths, column layouts, sorts, filters, last selection, open documents per user; "reset layout"; undo per document; never lose selection on refresh (re-select by key).

## Performance

UI virtualisation for lists/grids/trees; deferred loading of hidden panes; compiled bindings; minimal visual trees per row; no per-item blur/shadow; throttle live updates; startup with lazy pages.

## Accessibility

UI Automation names/roles/help text; AutomationPeers for custom controls; system focus visuals preserved when retemplating; high-contrast themes rendering every state; text scaling 100–225%; keyboard operability for every action; Narrator/NVDA pass; colour never alone; tooltips with shortcuts.

## Checklist

- [ ] Accelerators, access keys, arrow-key semantics, F6, default/cancel buttons
- [ ] Context menus mirror toolbar commands; commands disabled not hidden
- [ ] Minimum window size, breakpoints, pane collapse order, DPI 150/200% verified
- [ ] 4 epx grid, 32 epx controls, 14 epx body, aligned columns
- [ ] Grids virtualised with persisted column state; numeric alignment
- [ ] Theme resources for light/dark/high-contrast; Mica/Acrylic used sparingly
- [ ] Workspace state restored; undo; selection preserved on refresh
- [ ] Narrator/NVDA/VoiceOver pass; AutomationProperties on custom controls
