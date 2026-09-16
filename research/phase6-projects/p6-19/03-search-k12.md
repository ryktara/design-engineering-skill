## design-engineering search: Add a status bar with the last sync time and any failed postings.
status=CONFIDENT modes=['create'] platforms={} inputs={} products={'erp': 'KNOWN'} density=high stacks=[] screens=[] negatives=[]
facets required=['layout', 'navigation', 'direction'] unmet=['direction'] diversity=0.75
MISSING: platform: not stated and not detectable from a repository; brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence

### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.574 · engineering-practice
Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- use when: Field, travel, and public-venue apps; anything used with poor connectivity; any screen that writes data.
- avoid when: Read-only always-online desktop tools where connectivity loss is exceptional (still show an error, not a blank).
- why: lexical 0.667, structural 0.46 (mode create)

### Progress for background work: what, how far, what went wrong  `feedback-progress-async`  [rule/feedback; component] score 0.458 · heuristic
State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes.
- use when: Sync, upload, export, import, batch send, long saves: anything that takes more than a second and can partially fail.
- avoid when: Never show an indeterminate spinner with no words for more than a moment; never hide failures behind a generic 'something went wrong'; never announce every tick to screen readers.
- why: lexical 0.423, structural 0.5 (mode create)

### Desktop status bar as the persistent feedback surface, with next-error navigation  `desktop-status-bar-and-error-navigation`  [rule/feedback; component/platform] score 0.421 · platform-standard
One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width.
- use when: Data-entry and workbench windows where validation, selection and sync state must be visible without dialogs or toasts.
- avoid when: Consumer apps without a persistent window chrome; mobile.
- why: lexical 0.438, structural 0.4 (mode create, product erp)

### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.35 · heuristic
Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- use when: Status, category, or count must be scannable in lists and headers (Open/Closed, New, 3 unread).
- avoid when: As decoration on everything; when more than two badges per item appear, the design has become noisy.
- incompatible with: metadata-minimal, layout-immersive-rails
- why: lexical 0.188, structural 0.46 (mode create, product erp)

### Toolbar / command bar with selection-driven commands  `cta-toolbar-commands`  [pattern/cta; layout/platform] score 0.343 · platform-standard
Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- use when: Workbenches and tables: commands apply to the current selection, live in a persistent bar, and are mirrored by context menus and shortcuts.
- avoid when: Consumer or single-task screens; touch-first products.
- incompatible with: cta-single-primary, cta-focus-selects, cta-sticky-bar
- why: lexical 0.121, structural 0.48 (mode create, product erp, density high)

### No decorative imagery  `imagery-none`  [pattern/imagery; visual] score 0.331 · heuristic
Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- use when: Operational products: imagery only where it is data (avatars, product thumbnails, charts).
- avoid when: Brand or content products where imagery is the content.
- incompatible with: imagery-hero, imagery-immersive-backdrop, surface-imagery-backed
- why: lexical 0.0, structural 0.58 (mode create, product erp, density high)

### Neutral workhorse sans  `typography-neutral-sans`  [pattern/typography; visual] score 0.321 · heuristic
One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- use when: Dense, functional UI where the type must disappear: tables, forms, consoles. Prioritise x-height, tabular figures, and broad language coverage.
- avoid when: Brand-led or editorial products where the type is part of the identity (this choice will read as default).
- incompatible with: typography-serif-display, typography-condensed-display
- why: lexical 0.0, structural 0.58 (mode create, product erp, density high)

### Desktop menu bar + toolbar commands  `nav-menu-bar-desktop`  [pattern/navigation; navigation/platform] score 0.321 · platform-standard
Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live.
- use when: Document-centric or record-centric desktop apps with many commands, where discoverability through menus and accelerators matters (Alt+F, Ctrl+S).
- avoid when: Consumer apps with a handful of actions (use a command bar), touch-first devices, or web apps pretending to be native.
- incompatible with: nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.117, structural 0.48 (mode create, product erp, density high)

### Persistent left rail / sidebar  `nav-left-rail`  [pattern/navigation; navigation/platform] score 0.306 · heuristic
Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- use when: Authenticated tools with 6+ peer sections, frequent switching, and wide viewports; power users who need stable wayfinding.
- avoid when: Marketing pages, single-task flows (checkout, onboarding), phone widths, or when the product has three destinations and the rail would be mostly empty.
- incompatible with: nav-top-bar, nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.018, structural 0.48 (mode create, product erp, density high)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.301 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.045, structural 0.48 (mode create, product erp, density high)

### Master–detail (list + detail pane)  `layout-master-detail`  [pattern/layout; layout/platform] score 0.29 · platform-standard
List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- use when: Users scan a list of records and act on one at a time (tickets, orders, patients, mail); wide enough for two panes (≥ ~900 px / 641 epx).
- avoid when: Phone widths (collapse to list → push detail), records that need the full width (large tables, editors), or when the list has only a handful of items.
- incompatible with: layout-single-column, layout-immersive-rails, layout-rails
- why: lexical 0.026, structural 0.48 (mode create, product erp, density high)

### Part-to-whole → stacked bar, waffle, or (rarely) donut  `chart-composition`  [chart/chart; data-viz] score 0.273 · heuristic
Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices.
- use when: Shares of a total with ≤5 parts; one moment in time.
- avoid when: More than 5 slices, comparing parts across many totals (use 100% stacked bars), when precise comparison matters (angles are hard to read).
- why: lexical 0.202, structural 0.36 (mode create)

Filtered out: mobile-field-use (environment ['gloves', 'outdoor'] not in request)
