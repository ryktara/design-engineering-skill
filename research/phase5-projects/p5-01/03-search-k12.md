## design-engineering search: The invoices table on the billing page is hard to scan once there are more than twenty rows.
status=CONFIDENT modes=['audit', 'refactor'] platforms={} inputs={} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'anti-pattern'] unmet=['interaction'] diversity=0.92
MISSING: platform: audit targets differ by platform; not stated

### Grids with row actions are one Tab stop  `grid-single-tab-stop`  [rule/table; component/platform] score 0.574 · accessibility-requirement
Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell.
- use when: Data tables or grids where each row has buttons/links (edit, delete, approve, download) and there are more than a handful of rows.
- avoid when: Small static tables with no interactive cells.
- why: lexical 0.716, structural 0.4 (mode audit)

### Plan comparison and billing management  `comp-plan-comparison`  [component/settings; component/platform] score 0.472 · heuristic
Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- use when: Billing/plan pages: choosing or changing a plan, seat management, invoice history, payment method.
- avoid when: Public pricing marketing pages (hero + narrative) or checkout for a one-off purchase.
- why: lexical 0.645, structural 0.26 (mode audit)

### Pagination vs infinite scroll vs load more  `comp-pagination`  [component/list; component] score 0.325 · heuristic
Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page.
- use when: Any list longer than one screen.
- avoid when: Never use infinite scroll where the footer must be reachable or where users return to specific items (use pagination or load-more).
- why: lexical 0.296, structural 0.36 (mode audit)

### Semantic structure: headings, landmarks, lists, tables  `a11y-semantics-structure`  [rule/accessibility; accessibility/platform] score 0.306 · accessibility-requirement
Structure first, style second: choose the element for its meaning and restyle it. Data tables use <th scope>; layout tables are forbidden; visually hidden headings are fine for screen readers when the visual design omits them.
- use when: Every page: one h1, ordered heading levels, main/nav/aside landmarks, real <button>/<a>/<table>, lists for lists.
- avoid when: Never use divs with click handlers as buttons; never use heading levels for visual size.
- why: lexical 0.18, structural 0.46 (mode audit)

### Users always know where they are and how to go back  `nav-orientation-and-back`  [rule/navigation; navigation] score 0.269 · heuristic
Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there.
- use when: Every navigation model; deep links; multi-step flows; tabs that hold stacks.
- avoid when: Never break the browser/system back; never use a single URL for many states on the web.
- why: lexical 0.081, structural 0.5 (mode audit)

### Data table / grid  `comp-data-table`  [component/table; component/platform] score 0.264 · heuristic
Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- use when: Homogeneous records with several comparable attributes; sorting, filtering, selection, bulk actions, inline editing.
- avoid when: Fewer than ~10 rows (use a list), heterogeneous items (use cards/list), phone widths (convert to rows).
- incompatible with: layout-rails, surface-elevated-cards
- why: lexical 0.317, structural 0.2 (mode audit)

### One primary action per screen  `cta-single-primary`  [pattern/cta; layout] score 0.261 · heuristic
Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- use when: Task screens (forms, checkout, onboarding, settings) where one action completes the job; the primary is filled, secondaries are quiet.
- avoid when: Workbenches with many equal commands (toolbar pattern) or browse screens where selection is the action (focus-selects).
- incompatible with: cta-toolbar-commands, cta-focus-selects
- why: lexical 0.016, structural 0.36 (mode audit)

### One type scale with named roles  `typo-scale-and-roles`  [rule/typography; visual] score 0.259 · heuristic
Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles.
- use when: Any screen with more than two text sizes; any design system.
- avoid when: Never pick sizes per screen; never use more than ~7 sizes.
- why: lexical 0.061, structural 0.5 (mode audit)

### Every interactive colour has hover/pressed/focus/disabled/selected  `color-states-complete`  [rule/color; visual] score 0.253 · heuristic
Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them.
- use when: Buttons, links, list rows, tabs, chips, inputs, cards that are tappable, focus on TV.
- avoid when: Never leave a state to the framework default on one platform and custom on another.
- why: lexical 0.051, structural 0.5 (mode audit)

### Internationalisation: expansion, RTL, formats  `i18n-text-expansion-rtl`  [rule/content; visual] score 0.251 · engineering-practice
Allow 30–50% text expansion (German, Finnish), test with pseudo-localisation, use logical CSS properties / start-end alignment, mirror navigation and progress in RTL, format dates/numbers/currency by locale, verify font coverage per script, keep tabular figures across locales.
- use when: Any product with more than one locale; fixed-width buttons, tab labels, truncated titles, mirrored layouts.
- avoid when: Never hard-code widths around English strings; never concatenate translated fragments; never flip icons that indicate physical direction (play) in RTL.
- why: lexical 0.047, structural 0.5 (mode audit)

### Arbitrary spacing and misaligned edges  `anti-inconsistent-spacing`  [antipattern/craft; anti-pattern] score 0.242 · heuristic
Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change.
- use when: Paddings like 13/18/22 px, cards with different inner padding, text not aligned to the grid, icons off-baseline, unequal gaps between equal items.
- avoid when: Never.
- why: lexical 0.03, structural 0.5 (mode audit)

### One clear focal point per screen  `layout-hierarchy-one-thing`  [rule/layout; layout] score 0.24 · heuristic
Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title.
- use when: Designing any screen; reviewing 'it looks busy'.
- avoid when: Never give three elements the same maximum emphasis; never make the primary content compete with chrome.
- why: lexical 0.027, structural 0.5 (mode audit)

Filtered out: mobile-field-use (environment ['gloves', 'outdoor'] not in request)
