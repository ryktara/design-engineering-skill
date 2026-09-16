## design-engineering search: Add an offline banner and retry to the report list for when the site has no signal.
status=CONFIDENT modes=['create'] platforms={'web': 'KNOWN'} inputs={'pointer': 'INFERRED', 'keyboard': 'INFERRED', 'touch': 'INFERRED'} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['component', 'layout', 'platform', 'navigation', 'direction'] unmet=['direction'] diversity=0.83
MISSING: product: product family / primary user task not stated; brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence

### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.543 · engineering-practice
Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- use when: Field, travel, and public-venue apps; anything used with poor connectivity; any screen that writes data.
- avoid when: Read-only always-online desktop tools where connectivity loss is exceptional (still show an error, not a blank).
- why: lexical 0.447, structural 0.66 (platform web, mode create)

### List rows  `card-list-row`  [pattern/cards; layout/platform] score 0.441 · platform-standard
Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- use when: Homogeneous items on phones and in side panels: full-width rows with leading image/icon, title, secondary line, trailing meta, hairline dividers.
- avoid when: Items whose image is the recognition cue (use tiles/posters).
- incompatible with: card-poster-portrait, card-poster-landscape, surface-elevated-cards
- why: lexical 0.286, structural 0.52 (platform web, mode create)

### Master–detail (list + detail pane)  `layout-master-detail`  [pattern/layout; layout/platform] score 0.38 · platform-standard
List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- use when: Users scan a list of records and act on one at a time (tickets, orders, patients, mail); wide enough for two panes (≥ ~900 px / 641 epx).
- avoid when: Phone widths (collapse to list → push detail), records that need the full width (large tables, editors), or when the list has only a handful of items.
- incompatible with: layout-single-column, layout-immersive-rails, layout-rails
- why: lexical 0.157, structural 0.52 (platform web, input keyboard,pointer,touch, mode create)

### Semantic structure: headings, landmarks, lists, tables  `a11y-semantics-structure`  [rule/accessibility; accessibility/platform] score 0.38 · accessibility-requirement
Structure first, style second: choose the element for its meaning and restyle it. Data tables use <th scope>; layout tables are forbidden; visually hidden headings are fine for screen readers when the visual design omits them.
- use when: Every page: one h1, ordered heading levels, main/nav/aside landmarks, real <button>/<a>/<table>, lists for lists.
- avoid when: Never use divs with click handlers as buttons; never use heading levels for visual size.
- why: lexical 0.15, structural 0.66 (platform web, mode create)

### No card containers (dividers and spacing)  `card-none`  [pattern/cards; layout] score 0.376 · heuristic
Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts.
- use when: Most screens: sections separated by headings, spacing, and hairline dividers; cards reserved for genuinely tappable objects.
- avoid when: When the item boundary is itself the target and items are visually heterogeneous (then a card is right).
- incompatible with: surface-elevated-cards
- why: lexical 0.228, structural 0.4 (mode create)

### Grids with row actions are one Tab stop  `grid-single-tab-stop`  [rule/table; component/platform] score 0.365 · accessibility-requirement
Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell.
- use when: Data tables or grids where each row has buttons/links (edit, delete, approve, download) and there are more than a handful of rows.
- avoid when: Small static tables with no interactive cells.
- why: lexical 0.075, structural 0.72 (platform web, input keyboard,pointer, mode create)

### Everything operable by keyboard, no traps  `a11y-keyboard-operable`  [rule/accessibility; accessibility/platform] score 0.361 · accessibility-requirement
Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
- use when: Every interactive element, including custom widgets, drag/drop, sliders, menus, date pickers, and anything that appears on hover.
- avoid when: Never skip.
- why: lexical 0.067, structural 0.72 (platform web, input keyboard, mode create)

### Design empty, loading, error, and partial states  `layout-states-empty-loading-error`  [rule/feedback; component] score 0.352 · heuristic
Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state.
- use when: Every list, table, chart, form, and detail screen.
- avoid when: Never ship a blank area for empty data; never show a spinner for more than ~1 s without a skeleton or progress; never show an error without a next step.
- why: lexical 0.199, structural 0.54 (mode create)

### Drag and drop: affordance, feedback, keyboard alternative, no layout thrash  `interaction-drag-drop`  [rule/input; interaction/platform] score 0.351 · heuristic
Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion.
- use when: Reordering, rescheduling, moving cards between columns, dragging chips in a grid.
- avoid when: Never make drag the only way (WCAG 2.5.7); never re-render the whole collection on every pointer move; never drop without a visible target and a result announcement.
- why: lexical 0.05, structural 0.72 (platform web, input keyboard,pointer,touch, mode create)

### Visible focus ring (web/desktop)  `focus-ring-standard`  [pattern/focus; interaction/platform] score 0.35 · accessibility-requirement
One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- use when: All pointer+keyboard UI: a 2–3 px ring with ≥3:1 contrast against adjacent colours, offset so it is not hidden by borders, shown for :focus-visible.
- avoid when: TV (needs scale/glow because the ring is too subtle at 3 m).
- incompatible with: focus-scale-glow, focus-none-touch-only
- why: lexical 0.016, structural 0.58 (platform web, input keyboard,pointer, mode create)

### Virtualise long lists and tables  `web-virtualize-long-lists`  [rule/performance; performance/platform] score 0.345 · engineering-practice
Windowed rendering with stable row heights or measured heights, keyboard focus preserved when rows unmount (roving focus by key), aria-rowcount/aria-setsize so assistive tech knows the real size, scroll restoration on back navigation. Native: LazyColumn/List/FlatList/VirtualizingStackPanel already virtualise; keep keys stable.
- use when: Lists/tables beyond a few hundred rows, grids of images, infinite feeds, EPGs.
- avoid when: Small lists (<100) where virtualisation adds focus and find-in-page problems.
- why: lexical 0.251, structural 0.46 (platform web, mode create)

### Persistent left rail / sidebar  `nav-left-rail`  [pattern/navigation; navigation/platform] score 0.326 · heuristic
Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- use when: Authenticated tools with 6+ peer sections, frequent switching, and wide viewports; power users who need stable wayfinding.
- avoid when: Marketing pages, single-task flows (checkout, onboarding), phone widths, or when the product has three destinations and the rail would be mostly empty.
- incompatible with: nav-top-bar, nav-bottom-tabs, nav-tv-side, nav-hub-spoke
- why: lexical 0.022, structural 0.52 (platform web, input keyboard,pointer,touch, mode create)

Filtered out: anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['web']); comp-tv-rail (platform ['tv'] not in request ['web']); comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); comp-photo-capture-field (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-side-sheet (platform ['tv'] not in request ['web']); dir-broadcast-guide-tv (platform ['tv'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web'])
