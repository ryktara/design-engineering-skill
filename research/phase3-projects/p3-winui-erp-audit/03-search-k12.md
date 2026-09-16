## design-engineering search: Warehouse clerks say our WinUI stock adjustments page is confusing and they keep missing rows; the screen reader reads the status column as just text
status=CONFIDENT modes=['accessibility', 'audit'] platforms={'desktop': 'KNOWN', 'tv': 'KNOWN'} inputs={'remote': 'KNOWN', 'pointer': 'INFERRED', 'keyboard': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['winui'] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'platform', 'anti-pattern'] unmet=[] diversity=0.75

### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.49 · heuristic
Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- use when: Status, category, or count must be scannable in lists and headers (Open/Closed, New, 3 unread).
- avoid when: As decoration on everything; when more than two badges per item appear, the design has become noisy.
- incompatible with: metadata-minimal, layout-immersive-rails
- why: lexical 0.343, structural 0.58 (platform desktop, product erp, density medium)

### Actions only on hover  `anti-hover-only-actions`  [antipattern/craft; anti-pattern/platform] score 0.421 · accessibility-requirement
Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.
- use when: Row actions, card menus, and edit buttons that appear only on mouse hover.
- avoid when: Never as the sole path.
- why: lexical 0.176, structural 0.72 (platform desktop, input keyboard,pointer, mode accessibility)

### Rich metadata (operational)  `metadata-rich`  [pattern/metadata; layout/platform] score 0.401 · heuristic
Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- use when: Operations: many attributes per record visible at once (tables, ledgers, tickets), with sorting/filtering on any of them.
- avoid when: Consumer browsing, mobile, TV.
- incompatible with: metadata-minimal, layout-rails, layout-immersive-rails, density-low
- why: lexical 0.162, structural 0.56 (platform desktop, input keyboard,pointer, product erp)

### Data table / grid  `comp-data-table`  [component/table; component/platform] score 0.401 · heuristic
Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- use when: Homogeneous records with several comparable attributes; sorting, filtering, selection, bulk actions, inline editing.
- avoid when: Fewer than ~10 rows (use a list), heterogeneous items (use cards/list), phone widths (convert to rows).
- winui: CommunityToolkit DataGrid (keyboard + UIA built in) or ItemsView; avoid ListView with a fake header row.
- incompatible with: layout-rails, surface-elevated-cards
- why: lexical 0.205, structural 0.64 (platform desktop, input keyboard,pointer, secondary mode, product erp)

### Horizontal rails (rows of content)  `layout-rails`  [pattern/layout; layout/platform] score 0.383 · platform-standard
Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- use when: TV browsing of categorised content: vertical axis moves between categories, horizontal axis moves within a category. The default TV home structure.
- avoid when: Fewer than ~8 items total (use a grid or list), or content that must be compared side by side.
- incompatible with: layout-single-column, layout-table-first, layout-three-pane, layout-dashboard-grid, nav-top-bar, nav-left-rail
- why: lexical 0.227, structural 0.44 (platform tv, input remote (stated), product mismatch, density medium)

### List rows  `card-list-row`  [pattern/cards; layout/platform] score 0.382 · platform-standard
Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- use when: Homogeneous items on phones and in side panels: full-width rows with leading image/icon, title, secondary line, trailing meta, hairline dividers.
- avoid when: Items whose image is the recognition cue (use tiles/posters).
- incompatible with: card-poster-portrait, card-poster-landscape, surface-elevated-cards
- why: lexical 0.244, structural 0.44 (platform desktop, density medium)

### Hover reveals need a non-hover path  `a11y-hover-not-required`  [rule/input; interaction/platform] score 0.382 · accessibility-requirement
Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover.
- use when: Row actions that appear on hover, tooltips, hover cards, mega menus.
- avoid when: Never rely on hover alone; touch and keyboard users never hover.
- why: lexical 0.105, structural 0.72 (platform desktop, input keyboard,pointer, mode accessibility)

### TV: 10-foot typography  `tv-typography-distance`  [rule/typography; platform/visual] score 0.38 · platform-standard
Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3.
- use when: All text on TV.
- avoid when: Never scale a desktop type ramp up by a factor; rebuild the scale for distance and for reduced text volume.
- incompatible with: typography-serif-editorial
- why: lexical 0.101, structural 0.72 (platform tv, input remote (stated), secondary mode)

### Never colour alone  `a11y-color-not-only`  [rule/accessibility; accessibility] score 0.379 · accessibility-requirement
Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint.
- use when: Status, validation errors, chart series, selected/active states, required fields, links inside text.
- avoid when: Never skip.
- why: lexical 0.246, structural 0.54 (mode accessibility)

### Scale + glow/border focus (TV)  `focus-scale-glow`  [pattern/focus; interaction/platform] score 0.377 · platform-standard
Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- use when: All TV UI: focused item scales (1.05–1.1), gains a border or glow with ≥3:1 contrast, and its metadata may expand; unfocused items stay quiet.
- avoid when: Never elsewhere; and on TV never rely on colour tint alone.
- incompatible with: focus-ring-standard, focus-none-touch-only, focus-underline
- why: lexical 0.0, structural 0.66 (platform tv, input remote (stated), mode accessibility)

### Data-entry grid (spreadsheet-like)  `comp-data-entry-grid`  [component/table; component/platform] score 0.367 · heuristic
Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.
- use when: Batch entry of many similar rows (invoice lines, journal entries, stock counts).
- avoid when: Occasional single-record edits (use a form).
- winui: CommunityToolkit DataGrid editing + KeyboardAccelerator overrides.
- incompatible with: layout-single-column, nav-bottom-tabs
- why: lexical 0.144, structural 0.64 (platform desktop, input keyboard,pointer, secondary mode, product erp)

### TV: exactly one visible focus at all times  `a11y-tv-focus-always`  [rule/focus; interaction/platform] score 0.366 · platform-standard
Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state.
- use when: Every TV screen, after every navigation, after data loads, after dialogs close, after list updates.
- avoid when: Never leave focus on a hidden or off-screen element; never let focus disappear after a list refresh.
- why: lexical 0.012, structural 0.8 (platform tv, input remote (stated), mode accessibility)

Filtered out: anti-scroll-animation-everything (platform ['mobile', 'web'] not in request ['desktop', 'tv']); anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['desktop', 'tv']); comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['desktop', 'tv']); comp-hero-section (platform ['mobile', 'web'] not in request ['desktop', 'tv']); dir-service-app-mobile (platform ['mobile'] not in request ['desktop', 'tv']); dir-public-kiosk (platform ['kiosk'] not in request ['desktop', 'tv']); nav-top-bar (platform ['web'] not in request ['desktop', 'tv']); nav-bottom-tabs (platform ['mobile'] not in request ['desktop', 'tv'])
