## design-engineering search: add keyboard shortcuts and a command bar to the existing stock adjustments page without changing its navigation or theme
status=CONFIDENT modes=['create'] platforms={'desktop': 'KNOWN'} inputs={'keyboard': 'KNOWN', 'pointer': 'INFERRED'} products={'erp': 'KNOWN'} density=high stacks=['winui'] screens=[] negatives=[]
facets required=['component', 'layout', 'platform', 'interaction', 'navigation', 'direction'] unmet=[] diversity=0.83
MISSING: brand: no brand assets, guideline, or character description available

### Desktop menu bar + toolbar commands  `nav-menu-bar-desktop`  [pattern/navigation; navigation/platform] score 0.704 · platform-standard
Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live.
- use when: Document-centric or record-centric desktop apps with many commands, where discoverability through menus and accelerators matters (Alt+F, Ctrl+S).
- avoid when: Consumer apps with a handful of actions (use a command bar), touch-first devices, or web apps pretending to be native.
- winui: MenuBar + CommandBar; assign KeyboardAccelerator and AccessKey on every MenuFlyoutItem.
- incompatible with: nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.488, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Toolbar / command bar with selection-driven commands  `cta-toolbar-commands`  [pattern/cta; layout/platform] score 0.691 · platform-standard
Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- use when: Workbenches and tables: commands apply to the current selection, live in a persistent bar, and are mirrored by context menus and shortcuts.
- avoid when: Consumer or single-task screens; touch-first products.
- winui: CommandBar with AppBarButton + KeyboardAccelerator; IsEnabled bound to selection.
- incompatible with: cta-single-primary, cta-focus-selects, cta-sticky-bar
- why: lexical 0.426, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Command palette as primary navigation accelerator  `nav-command-palette`  [pattern/navigation; navigation/platform] score 0.6 · heuristic
Global shortcut (Ctrl/Cmd+K), fuzzy search over commands and records, recent items first, arrow-key navigation with aria-activedescendant, Escape closes and restores focus. Every command in the palette must also exist somewhere visible.
- use when: Power-user tools with many commands/records; users who live on the keyboard; anywhere a menu tree would be three levels deep.
- avoid when: Touch-first products, casual users, or as the only way to reach a feature (it augments visible navigation, never replaces it).
- winui: Implement as a ContentDialog-free Flyout with an AutoSuggestBox; register KeyboardAccelerator on the root.
- why: lexical 0.334, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Command palette  `comp-command-palette`  [component/command-palette; component/platform] score 0.583 · heuristic
Global shortcut, combobox semantics (aria-activedescendant), grouped results (commands, records, navigation), recent items, fuzzy match with highlighted matches, keyboard hints, Escape restores focus, executes in ≤1 keystroke after selection, debounced async search with loading state.
- use when: Power-user tools with many commands and records; augments visible navigation.
- avoid when: As the only way to reach features; touch-first apps.
- winui: AutoSuggestBox in a Flyout with grouped ItemsSource; KeyboardAccelerator Ctrl+K.
- why: lexical 0.339, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Master–detail (list + detail pane)  `layout-master-detail`  [pattern/layout; layout/platform] score 0.474 · platform-standard
List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- use when: Users scan a list of records and act on one at a time (tickets, orders, patients, mail); wide enough for two panes (≥ ~900 px / 641 epx).
- avoid when: Phone widths (collapse to list → push detail), records that need the full width (large tables, editors), or when the list has only a handful of items.
- winui: Two-column Grid with a splitter, or the WinUI Gallery master/detail sample; ListView.SelectionMode=Single with SelectedItem bound TwoWay.
- incompatible with: layout-single-column, layout-immersive-rails, layout-rails
- why: lexical 0.033, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Data-entry grid (spreadsheet-like)  `comp-data-entry-grid`  [component/table; component/platform] score 0.457 · heuristic
Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.
- use when: Batch entry of many similar rows (invoice lines, journal entries, stock counts).
- avoid when: Occasional single-record edits (use a form).
- winui: CommunityToolkit DataGrid editing + KeyboardAccelerator overrides.
- incompatible with: layout-single-column, nav-bottom-tabs
- why: lexical 0.112, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### High density  `density-high`  [pattern/density; layout/platform] score 0.456 · heuristic
4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- use when: Expert users, repeated daily use, comparison and scanning tasks, large screens with a pointer.
- avoid when: Touch-only, first-time users, TV, or emotional/branding surfaces.
- incompatible with: density-low, layout-editorial, typography-serif-display
- why: lexical 0.0, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Table-first working screen  `layout-table-first`  [pattern/layout; layout/platform] score 0.456 · heuristic
Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- use when: The record set is the product (orders, transactions, tickets, inventory): users filter, sort, select, and bulk-act. Screen = toolbar + filters + table + optional side panel.
- avoid when: Phone widths (switch to list rows), fewer than ~20 rows, or when each record needs rich media.
- winui: DataGrid from CommunityToolkit or a virtualised ListView with a header; enable IsItemClickEnabled and keyboard sorting.
- incompatible with: layout-single-column, layout-immersive-rails, layout-feed, layout-editorial
- why: lexical 0.0, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.456 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.0, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### No decorative imagery  `imagery-none`  [pattern/imagery; visual] score 0.404 · heuristic
Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- use when: Operational products: imagery only where it is data (avatars, product thumbnails, charts).
- avoid when: Brand or content products where imagery is the content.
- incompatible with: imagery-hero, imagery-immersive-backdrop, surface-imagery-backed
- why: lexical 0.1, structural 0.62 (mode create, product erp, density high)

### Operational workbench  `dir-operational-workbench`  [direction/direction; direction/platform] score 0.404 · internal-preference
Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- use when: Daily-use record tools (ERP, ledgers, ticketing, admin) for trained users who value speed and scanning.
- avoid when: Consumer, marketing, TV, or first-time-user products.
- incompatible with: surface-glass, motion-cinematic, imagery-hero, typography-serif-display
- why: lexical 0.014, structural 0.88 (platform desktop, input keyboard (stated), mode create, product erp, density high)

### Desktop: keyboard is a first-class input  `desktop-keyboard-first`  [rule/input; interaction/platform] score 0.402 · platform-standard
Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
- use when: Every desktop screen: shortcuts for frequent commands, access keys for menus, Tab/arrow semantics in lists, trees, grids, and toolbars, Enter/Escape in dialogs.
- avoid when: Never assign shortcuts that collide with platform or assistive-tech shortcuts; never make Tab stop on every cell of a grid.
- why: lexical 0.077, structural 0.8 (platform desktop, input keyboard (stated), mode create)

Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['desktop']); anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['desktop']); comp-media-card (platform ['mobile', 'tv', 'web'] not in request ['desktop']); comp-player-controls (platform ['mobile', 'tv', 'web'] not in request ['desktop']); comp-tv-rail (platform ['tv'] not in request ['desktop']); comp-hero-section (platform ['mobile', 'web'] not in request ['desktop']); comp-product-detail-page (platform ['mobile', 'web'] not in request ['desktop']); comp-mini-player (platform ['mobile', 'tv', 'web'] not in request ['desktop'])
