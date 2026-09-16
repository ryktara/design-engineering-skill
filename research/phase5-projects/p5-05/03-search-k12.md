## design-engineering search: Keyboard users can't get to the chart filters.
status=PARTIAL modes=['accessibility', 'audit'] platforms={} inputs={'keyboard': 'KNOWN'} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'anti-pattern', 'data-viz'] unmet=[] diversity=0.67
MISSING: platform: audit targets differ by platform; not stated

### Search and filters: visible state and instant feedback  `search-filter-feedback`  [rule/search; component] score 0.448 · heuristic
Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails.
- use when: Catalogues, tables, media libraries, admin lists.
- avoid when: Never hide applied filters; never reset filters on navigation without asking; never search on every keystroke against a slow backend without debounce.
- why: lexical 0.472, structural 0.42 (secondary mode)

### Chart container and interaction  `comp-chart-container`  [component/chart; component/platform] score 0.429 · heuristic
Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV.
- use when: Any chart in a product.
- avoid when: Decorative charts with no question; charts of fewer than ~4 points (use a stat).
- why: lexical 0.633, structural 0.18 (secondary mode)

### Everything operable by keyboard, no traps  `a11y-keyboard-operable`  [rule/accessibility; accessibility/platform] score 0.415 · accessibility-requirement
Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
- use when: Every interactive element, including custom widgets, drag/drop, sliders, menus, date pickers, and anything that appears on hover.
- avoid when: Never skip.
- why: lexical 0.263, structural 0.6 (input keyboard (stated), mode accessibility)

### Desktop: keyboard is a first-class input  `desktop-keyboard-first`  [rule/input; interaction/platform] score 0.406 · platform-standard
Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
- use when: Every desktop screen: shortcuts for frequent commands, access keys for menus, Tab/arrow semantics in lists, trees, grids, and toolbars, Enter/Escape in dialogs.
- avoid when: Never assign shortcuts that collide with platform or assistive-tech shortcuts; never make Tab stop on every cell of a grid.
- why: lexical 0.247, structural 0.6 (input keyboard (stated), mode accessibility)

### Filter bar / faceted filters  `comp-filters`  [component/search; component/platform] score 0.356 · heuristic
Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL.
- use when: Lists with several filterable attributes.
- avoid when: One or two filters (inline selects); TV (use rail categories or a simple filter row).
- why: lexical 0.5, structural 0.18 (secondary mode)

### Visible focus ring (web/desktop)  `focus-ring-standard`  [pattern/focus; interaction/platform] score 0.356 · accessibility-requirement
One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- use when: All pointer+keyboard UI: a 2–3 px ring with ≥3:1 contrast against adjacent colours, offset so it is not hidden by borders, shown for :focus-visible.
- avoid when: TV (needs scale/glow because the ring is too subtle at 3 m).
- incompatible with: focus-scale-glow, focus-none-touch-only
- why: lexical 0.125, structural 0.46 (input keyboard (stated), mode accessibility)

### Never colour alone  `a11y-color-not-only`  [rule/accessibility; accessibility] score 0.339 · accessibility-requirement
Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint.
- use when: Status, validation errors, chart series, selected/active states, required fields, links inside text.
- avoid when: Never skip.
- why: lexical 0.207, structural 0.5 (mode accessibility)

### Actions only on hover  `anti-hover-only-actions`  [antipattern/craft; anti-pattern/platform] score 0.339 · accessibility-requirement
Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.
- use when: Row actions, card menus, and edit buttons that appear only on mouse hover.
- avoid when: Never as the sole path.
- why: lexical 0.125, structural 0.6 (input keyboard (stated), mode accessibility)

### Chart colour: categorical ≤8, colour-blind safe, plus shape/label  `chart-accessible-colour`  [chart/chart; data-viz] score 0.324 · accessibility-requirement
One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette.
- use when: Any chart with more than one series or category.
- avoid when: Never red/green as the only distinction; never a rainbow for ordered data.
- why: lexical 0.295, structural 0.36 (mode accessibility)

### Grids with row actions are one Tab stop  `grid-single-tab-stop`  [rule/table; component/platform] score 0.309 · accessibility-requirement
Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell.
- use when: Data tables or grids where each row has buttons/links (edit, delete, approve, download) and there are more than a handful of rows.
- avoid when: Small static tables with no interactive cells.
- why: lexical 0.071, structural 0.6 (input keyboard (stated), mode accessibility)

### Mobile: keyboard and input types  `mobile-keyboard-ime`  [rule/forms; component/platform] score 0.298 · platform-standard
Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms.
- use when: Every text field.
- avoid when: Never leave the default keyboard for emails, numbers, phone, or URLs; never let the keyboard cover the focused field or the submit button.
- why: lexical 0.281, structural 0.32 (secondary mode)

### Focus visible and not obscured  `a11y-focus-visible`  [rule/focus; interaction/platform] score 0.292 · accessibility-requirement
Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
- use when: Every focusable element in every theme; sticky headers, footers, toasts, and cookie banners must never cover the focused element.
- avoid when: Never remove focus styles; use :focus-visible to hide them for mouse clicks only.
- why: lexical 0.039, structural 0.6 (input keyboard (stated), mode accessibility)
