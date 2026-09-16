## design-engineering search: polish the billing settings page so plan cards, seat table and invoice history feel consistent with the rest of the admin, without changing navigation or theme
status=CONFIDENT modes=['polish', 'refactor'] platforms={'web': 'KNOWN'} inputs={'pointer': 'INFERRED', 'keyboard': 'INFERRED', 'touch': 'INFERRED'} products={'saas': 'KNOWN', 'finance': 'KNOWN'} density=high stacks=['nextjs', 'react', 'tailwind', 'shadcn'] screens=['settings'] negatives=['navigation-change']
facets required=['anti-pattern', 'layout', 'visual', 'component'] unmet=[] diversity=0.92
MISSING: brand: no brand assets, guideline, or character description available

### Plan comparison and billing management  `comp-plan-comparison`  [component/settings; component/platform] score 0.745 · heuristic
Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- use when: Billing/plan pages: choosing or changing a plan, seat management, invoice history, payment method.
- avoid when: Public pricing marketing pages (hero + narrative) or checkout for a one-off purchase.
- nextjs: Server component for the invoice table; client radio group for plans; shadcn Dialog with returnFocus; Table with <th scope> and numeric cells using tabular-nums.
- react: role=radiogroup on the plan row; roving tabindex; download as <a download> with the file name in the link text.
- why: lexical 0.782, structural 0.7 (platform web, secondary mode, product saas, screen settings)

### Bordered cards  `card-bordered`  [pattern/cards; layout/platform] score 0.455 · heuristic
Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- use when: Settings pages, integration lists, plan pickers: discrete objects on a light canvas where a 1 px border (≥3:1) delineates without elevation.
- avoid when: Nested inside other cards or panels; on dark themes where borders vanish (use tonal steps).
- incompatible with: surface-elevated-cards, surface-imagery-backed, card-none
- why: lexical 0.199, structural 0.68 (platform web, input keyboard,pointer, secondary mode, product finance,saas)

### Persistent left rail / sidebar  `nav-left-rail`  [pattern/navigation; navigation/platform] score 0.44 · heuristic
Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- use when: Authenticated tools with 6+ peer sections, frequent switching, and wide viewports; power users who need stable wayfinding.
- avoid when: Marketing pages, single-task flows (checkout, onboarding), phone widths, or when the product has three destinations and the rail would be mostly empty.
- shadcn: Use the Sidebar primitives (SidebarProvider/SidebarMenu) which already handle collapse state and keyboard; do not hand-roll a second implementation.
- incompatible with: nav-top-bar, nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.033, structural 0.76 (platform web, input keyboard,pointer,touch, secondary mode, product finance,saas, density high)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.408 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.012, structural 0.76 (platform web, input keyboard,pointer, secondary mode, product finance,saas, density high)

### High density  `density-high`  [pattern/density; layout/platform] score 0.404 · heuristic
4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- use when: Expert users, repeated daily use, comparison and scanning tasks, large screens with a pointer.
- avoid when: Touch-only, first-time users, TV, or emotional/branding surfaces.
- incompatible with: density-low, layout-editorial, typography-serif-display
- why: lexical 0.003, structural 0.76 (platform web, input keyboard,pointer, secondary mode, product finance,saas, density high)

### Numeric tables: alignment, figures, units, precision  `data-tables-numeric`  [rule/table; component/platform] score 0.396 · heuristic
Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator.
- use when: Any table or KPI with numbers: money, quantities, percentages, dates.
- avoid when: Never centre numbers; never mix precisions in a column; never rely on colour alone for negative values.
- why: lexical 0.033, structural 0.84 (platform web, input keyboard,pointer, mode polish, product finance,saas, density high)

### Bordered panes  `surface-bordered-panes`  [pattern/surface; layout/platform] score 0.394 · heuristic
One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- use when: Dense workbenches where regions are separated by 1 px borders and the canvas is a single tone; the IDE/spreadsheet aesthetic.
- avoid when: Consumer or brand-led products, touch-first products with fat targets.
- incompatible with: surface-glass, surface-elevated-cards, layout-immersive-rails
- why: lexical 0.003, structural 0.76 (platform web, input keyboard,pointer, secondary mode, product finance,saas, density high)

### Sidebar / navigation rail  `comp-sidebar-nav`  [component/navigation; component/platform] score 0.377 · heuristic
Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header).
- use when: Justified by the left-rail navigation pattern (6+ sections, frequent switching).
- avoid when: Three destinations, marketing pages, phones (collapse to drawer), TV.
- shadcn: Sidebar component family; SidebarGroup for grouping; keep it at one instance per app.
- incompatible with: nav-top-bar, nav-bottom-tabs
- why: lexical 0.064, structural 0.76 (platform web, input keyboard,pointer,touch, secondary mode, product finance,saas, density high)

### Operational workbench  `dir-operational-workbench`  [direction/direction; direction/platform] score 0.371 · internal-preference
Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- use when: Daily-use record tools (ERP, ledgers, ticketing, admin) for trained users who value speed and scanning.
- avoid when: Consumer, marketing, TV, or first-time-user products.
- incompatible with: surface-glass, motion-cinematic, imagery-hero, typography-serif-display
- why: lexical 0.053, structural 0.76 (platform web, input keyboard,pointer, secondary mode, product finance,saas, density high)

### The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)  `anti-generic-sidebar-dashboard`  [antipattern/generic-ai; anti-pattern/platform] score 0.37 · heuristic
Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why.
- use when: Any 'dashboard' request answered with the same skeleton regardless of what the user monitors or does.
- avoid when: Each element can be right; the failure is choosing them before knowing the task.
- why: lexical 0.1, structural 0.7 (platform web, mode polish, product finance,saas)

### Data graphics as the visual layer  `imagery-data-graphics`  [pattern/imagery; platform/visual] score 0.349 · heuristic
One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- use when: Analytics, monitoring, and finance where charts, sparklines, and status marks are the imagery; identity comes from the chart style.
- avoid when: Content or commerce products.
- incompatible with: imagery-hero, imagery-immersive-backdrop
- why: lexical 0.005, structural 0.68 (platform web, input keyboard,pointer, product finance,saas, density high)

### Focus visible and not obscured  `a11y-focus-visible`  [rule/focus; interaction/platform] score 0.349 · accessibility-requirement
Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
- use when: Every focusable element in every theme; sticky headers, footers, toasts, and cookie banners must never cover the focused element.
- avoid when: Never remove focus styles; use :focus-visible to hide them for mouse clicks only.
- why: lexical 0.012, structural 0.76 (platform web, input keyboard, mode polish)

Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['web']); anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['web']); comp-tv-rail (platform ['tv'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); dir-cinematic-media-tv (platform ['tv'] not in request ['web']); dir-broadcast-guide-tv (platform ['tv'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web']); dir-social-feed-mobile (platform ['mobile'] not in request ['web'])
