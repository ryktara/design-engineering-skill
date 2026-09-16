## design-engineering search: accessibility review and fix of the seat management table: keyboard users can't reach row actions and the status column is colour only
status=CONFIDENT modes=['accessibility', 'audit'] platforms={'web': 'KNOWN'} inputs={'keyboard': 'KNOWN', 'pointer': 'INFERRED', 'touch': 'INFERRED'} products={'finance': 'KNOWN', 'saas': 'KNOWN'} density=high stacks=['nextjs', 'react', 'tailwind', 'shadcn'] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'platform', 'anti-pattern'] unmet=[] diversity=0.83

### Actions only on hover  `anti-hover-only-actions`  [antipattern/craft; anti-pattern/platform] score 0.654 · accessibility-requirement
Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.
- use when: Row actions, card menus, and edit buttons that appear only on mouse hover.
- avoid when: Never as the sole path.
- why: lexical 0.535, structural 0.8 (platform web, input keyboard (stated), mode accessibility)

### Plan comparison and billing management  `comp-plan-comparison`  [component/settings; component/platform] score 0.637 · heuristic
Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- use when: Billing/plan pages: choosing or changing a plan, seat management, invoice history, payment method.
- avoid when: Public pricing marketing pages (hero + narrative) or checkout for a one-off purchase.
- nextjs: Server component for the invoice table; client radio group for plans; shadcn Dialog with returnFocus; Table with <th scope> and numeric cells using tabular-nums.
- react: role=radiogroup on the plan row; roving tabindex; download as <a download> with the file name in the link text.
- why: lexical 0.684, structural 0.58 (platform web, secondary mode, product saas)

### Data table / grid  `comp-data-table`  [component/table; component/platform] score 0.605 · heuristic
Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- use when: Homogeneous records with several comparable attributes; sorting, filtering, selection, bulk actions, inline editing.
- avoid when: Fewer than ~10 rows (use a list), heterogeneous items (use cards/list), phone widths (convert to rows).
- react: TanStack Table (headless) + TanStack Virtual; render semantic <table> when static, role=grid when interactive; sticky via position: sticky on th.
- shadcn: DataTable recipe (TanStack) is the convention; keep the Table primitives, add virtualisation for >200 rows.
- incompatible with: layout-rails, surface-elevated-cards
- why: lexical 0.445, structural 0.8 (platform web, input keyboard (stated), secondary mode, product finance,saas, density high)

### Grids with row actions are one Tab stop  `grid-single-tab-stop`  [rule/table; component/platform] score 0.6 · accessibility-requirement
Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell.
- use when: Data tables or grids where each row has buttons/links (edit, delete, approve, download) and there are more than a handful of rows.
- avoid when: Small static tables with no interactive cells.
- react: role=grid with a roving tabindex hook; tabIndex=-1 on non-active cells; key handlers on the grid container.
- why: lexical 0.436, structural 0.8 (platform web, input keyboard (stated), mode accessibility)

### Table-first working screen  `layout-table-first`  [pattern/layout; layout/platform] score 0.543 · heuristic
Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- use when: The record set is the product (orders, transactions, tickets, inventory): users filter, sort, select, and bulk-act. Screen = toolbar + filters + table + optional side panel.
- avoid when: Phone widths (switch to list rows), fewer than ~20 rows, or when each record needs rich media.
- react: TanStack Table for logic + TanStack Virtual for rows; render <table> semantics or role=grid with aria-rowcount.
- incompatible with: layout-single-column, layout-immersive-rails, layout-feed, layout-editorial
- why: lexical 0.29, structural 0.72 (platform web, input keyboard (stated), product finance,saas, density high)

### Never colour alone  `a11y-color-not-only`  [rule/accessibility; accessibility] score 0.484 · accessibility-requirement
Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint.
- use when: Status, validation errors, chart series, selected/active states, required fields, links inside text.
- avoid when: Never skip.
- why: lexical 0.439, structural 0.54 (mode accessibility)

### Hover reveals need a non-hover path  `a11y-hover-not-required`  [rule/input; interaction/platform] score 0.462 · accessibility-requirement
Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover.
- use when: Row actions that appear on hover, tooltips, hover cards, mega menus.
- avoid when: Never rely on hover alone; touch and keyboard users never hover.
- why: lexical 0.185, structural 0.8 (platform web, input keyboard (stated), mode accessibility)

### Visible focus ring (web/desktop)  `focus-ring-standard`  [pattern/focus; interaction/platform] score 0.458 · accessibility-requirement
One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- use when: All pointer+keyboard UI: a 2–3 px ring with ≥3:1 contrast against adjacent colours, offset so it is not hidden by borders, shown for :focus-visible.
- avoid when: TV (needs scale/glow because the ring is too subtle at 3 m).
- tailwind: focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[--color-focus-ring]; drop ring-0 overrides.
- incompatible with: focus-scale-glow, focus-none-touch-only
- why: lexical 0.148, structural 0.66 (platform web, input keyboard (stated), mode accessibility)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.449 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.118, structural 0.72 (platform web, input keyboard (stated), product finance,saas, density high)

### Everything operable by keyboard, no traps  `a11y-keyboard-operable`  [rule/accessibility; accessibility/platform] score 0.437 · accessibility-requirement
Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
- use when: Every interactive element, including custom widgets, drag/drop, sliders, menus, date pickers, and anything that appears on hover.
- avoid when: Never skip.
- why: lexical 0.14, structural 0.8 (platform web, input keyboard (stated), mode accessibility)

### Toolbar / command bar with selection-driven commands  `cta-toolbar-commands`  [pattern/cta; layout/platform] score 0.432 · platform-standard
Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- use when: Workbenches and tables: commands apply to the current selection, live in a persistent bar, and are mirrored by context menus and shortcuts.
- avoid when: Consumer or single-task screens; touch-first products.
- react: Toolbar following the APG toolbar pattern (roving tabindex); disable via aria-disabled with reason in tooltip.
- incompatible with: cta-single-primary, cta-focus-selects, cta-sticky-bar
- why: lexical 0.087, structural 0.72 (platform web, input keyboard (stated), product finance,saas, density high)

### Persistent left rail / sidebar  `nav-left-rail`  [pattern/navigation; navigation/platform] score 0.404 · heuristic
Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- use when: Authenticated tools with 6+ peer sections, frequent switching, and wide viewports; power users who need stable wayfinding.
- avoid when: Marketing pages, single-task flows (checkout, onboarding), phone widths, or when the product has three destinations and the rail would be mostly empty.
- shadcn: Use the Sidebar primitives (SidebarProvider/SidebarMenu) which already handle collapse state and keyboard; do not hand-roll a second implementation.
- incompatible with: nav-top-bar, nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.0, structural 0.72 (platform web, input keyboard (stated), product finance,saas, density high)

Filtered out: anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['web']); comp-tv-rail (platform ['tv'] not in request ['web']); comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); dir-cinematic-media-tv (platform ['tv'] not in request ['web']); dir-broadcast-guide-tv (platform ['tv'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web']); dir-social-feed-mobile (platform ['mobile'] not in request ['web'])
