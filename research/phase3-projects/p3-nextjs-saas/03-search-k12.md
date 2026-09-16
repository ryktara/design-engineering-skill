## design-engineering search: Add a team billing settings page with plan comparison, seat management table and invoice history to our Next.js SaaS admin
status=CONFIDENT modes=['create'] platforms={'web': 'KNOWN'} inputs={'pointer': 'INFERRED', 'keyboard': 'INFERRED', 'touch': 'INFERRED'} products={'saas': 'KNOWN', 'finance': 'KNOWN'} density=high stacks=['nextjs', 'react', 'tailwind', 'shadcn'] screens=['settings'] negatives=[]
facets required=['component', 'layout', 'platform', 'navigation', 'direction'] unmet=[] diversity=0.83
MISSING: brand: no brand assets, guideline, or character description available

### Bordered cards  `card-bordered`  [pattern/cards; layout/platform] score 0.567 · heuristic
Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- use when: Settings pages, integration lists, plan pickers: discrete objects on a light canvas where a 1 px border (≥3:1) delineates without elevation.
- avoid when: Nested inside other cards or panels; on dark themes where borders vanish (use tonal steps).
- incompatible with: surface-elevated-cards, surface-imagery-backed, card-none
- why: lexical 0.337, structural 0.76 (platform web, input keyboard,pointer, mode create, product finance,saas)

### The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)  `anti-generic-sidebar-dashboard`  [antipattern/generic-ai; anti-pattern/platform] score 0.556 · heuristic
Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why.
- use when: Any 'dashboard' request answered with the same skeleton regardless of what the user monitors or does.
- avoid when: Each element can be right; the failure is choosing them before knowing the task.
- why: lexical 0.438, structural 0.7 (platform web, mode create, product finance,saas)

### Persistent left rail / sidebar  `nav-left-rail`  [pattern/navigation; navigation/platform] score 0.527 · heuristic
Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- use when: Authenticated tools with 6+ peer sections, frequent switching, and wide viewports; power users who need stable wayfinding.
- avoid when: Marketing pages, single-task flows (checkout, onboarding), phone widths, or when the product has three destinations and the rail would be mostly empty.
- shadcn: Use the Sidebar primitives (SidebarProvider/SidebarMenu) which already handle collapse state and keyboard; do not hand-roll a second implementation.
- incompatible with: nav-top-bar, nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.125, structural 0.84 (platform web, input keyboard,pointer,touch, mode create, product finance,saas, density high)

### High density  `density-high`  [pattern/density; layout/platform] score 0.482 · heuristic
4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- use when: Expert users, repeated daily use, comparison and scanning tasks, large screens with a pointer.
- avoid when: Touch-only, first-time users, TV, or emotional/branding surfaces.
- incompatible with: density-low, layout-editorial, typography-serif-display
- why: lexical 0.08, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Numeric tables: alignment, figures, units, precision  `data-tables-numeric`  [rule/table; component/platform] score 0.46 · heuristic
Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator.
- use when: Any table or KPI with numbers: money, quantities, percentages, dates.
- avoid when: Never centre numbers; never mix precisions in a column; never rely on colour alone for negative values.
- why: lexical 0.15, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.449 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.021, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Operational workbench  `dir-operational-workbench`  [direction/direction; direction/platform] score 0.439 · internal-preference
Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- use when: Daily-use record tools (ERP, ledgers, ticketing, admin) for trained users who value speed and scanning.
- avoid when: Consumer, marketing, TV, or first-time-user products.
- incompatible with: surface-glass, motion-cinematic, imagery-hero, typography-serif-display
- why: lexical 0.11, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Data graphics as the visual layer  `imagery-data-graphics`  [pattern/imagery; platform/visual] score 0.43 · heuristic
One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- use when: Analytics, monitoring, and finance where charts, sparklines, and status marks are the imagery; identity comes from the chart style.
- avoid when: Content or commerce products.
- incompatible with: imagery-hero, imagery-immersive-backdrop
- why: lexical 0.021, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Bordered panes  `surface-bordered-panes`  [pattern/surface; layout/platform] score 0.428 · heuristic
One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- use when: Dense workbenches where regions are separated by 1 px borders and the canvas is a single tone; the IDE/spreadsheet aesthetic.
- avoid when: Consumer or brand-led products, touch-first products with fat targets.
- incompatible with: surface-glass, surface-elevated-cards, layout-immersive-rails
- why: lexical 0.0, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance,saas, density high)

### Data-entry grid (spreadsheet-like)  `comp-data-entry-grid`  [component/table; component/platform] score 0.424 · heuristic
Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.
- use when: Batch entry of many similar rows (invoice lines, journal entries, stock counts).
- avoid when: Occasional single-record edits (use a form).
- react: AG Grid or Glide Data Grid for real spreadsheet behaviour; do not hand-roll.
- incompatible with: layout-single-column, nav-bottom-tabs
- why: lexical 0.28, structural 0.6 (platform web, input keyboard,pointer, mode create, product finance, screen mismatch, density high)

### Tree + breadcrumb for deep hierarchies  `nav-breadcrumb-tree`  [pattern/navigation; navigation/platform] score 0.398 · platform-standard
Tree in the left pane with full keyboard semantics (arrow keys expand/collapse, type-ahead), breadcrumb above the content that mirrors the tree path and is clickable at every level. Persist expansion state per session. Virtualise beyond ~500 nodes.
- use when: Hierarchies of 3+ levels (accounts → cost centres → entries, folders, org charts) where users need to see where they are and jump laterally.
- avoid when: Flat structures, mobile widths, or when the tree would exceed a few hundred visible nodes without virtualisation.
- react: Use a tested tree (react-arborist, or a headless treeview following the APG pattern) rather than nested <ul> with click handlers.
- incompatible with: nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.0, structural 0.84 (platform web, input keyboard,pointer, mode create, product finance, density high)

### Semantic structure: headings, landmarks, lists, tables  `a11y-semantics-structure`  [rule/accessibility; accessibility/platform] score 0.397 · accessibility-requirement
Structure first, style second: choose the element for its meaning and restyle it. Data tables use <th scope>; layout tables are forbidden; visually hidden headings are fine for screen readers when the visual design omits them.
- use when: Every page: one h1, ordered heading levels, main/nav/aside landmarks, real <button>/<a>/<table>, lists for lists.
- avoid when: Never use divs with click handlers as buttons; never use heading levels for visual size.
- why: lexical 0.15, structural 0.7 (platform web, mode create)

Filtered out: anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['web']); nav-bottom-tabs (platform ['mobile'] not in request ['web']); nav-tv-side (platform ['tv'] not in request ['web']); typography-system-native (platform ['desktop', 'mobile', 'tv'] not in request ['web']); cta-focus-selects (platform ['tv'] not in request ['web']); cta-fab (platform ['mobile'] not in request ['web'])
