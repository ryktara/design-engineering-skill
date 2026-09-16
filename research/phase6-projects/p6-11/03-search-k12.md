## design-engineering search: Inspectors in gloves keep missing the small checkbox on each defect row.
status=CONFIDENT modes=['audit', 'responsive', 'refactor'] platforms={} inputs={'touch': 'KNOWN'} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'anti-pattern'] unmet=[] diversity=0.92
MISSING: platform: audit targets differ by platform; not stated

### Field use: sunlight readability and glanceable status  `mobile-field-use`  [rule/environment; accessibility/platform] score 0.624 · heuristic
Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding).
- use when: Couriers, inspectors, technicians, warehouse and construction workers, outdoor kiosks: bright light, gloves, movement, interruptions.
- avoid when: Desk-bound indoor use.
- why: lexical 0.577, structural 0.68 (input touch (stated), mode audit, environment gloves)

### Exceptions first: surface what needs attention in lists and tables  `data-exceptions-first`  [rule/feedback; component] score 0.456 · heuristic
Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service').
- use when: Any collection where some items need action (overdue, late, failed, expiring, over budget) and the user should see them without opening each one.
- avoid when: Never rely on colour alone for the status; never bury the exception state inside the detail view; never sort exceptions below normal rows by default.
- why: lexical 0.42, structural 0.5 (mode audit)

### Grids with row actions are one Tab stop  `grid-single-tab-stop`  [rule/table; component/platform] score 0.424 · accessibility-requirement
Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell.
- use when: Data tables or grids where each row has buttons/links (edit, delete, approve, download) and there are more than a handful of rows.
- avoid when: Small static tables with no interactive cells.
- why: lexical 0.444, structural 0.4 (mode audit)

### Actions only on hover  `anti-hover-only-actions`  [antipattern/craft; anti-pattern/platform] score 0.388 · accessibility-requirement
Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.
- use when: Row actions, card menus, and edit buttons that appear only on mouse hover.
- avoid when: Never as the sole path.
- why: lexical 0.214, structural 0.6 (input touch (stated), mode audit)

### Many series or groups → small multiples  `chart-small-multiples`  [chart/chart; data-viz/platform] score 0.377 · heuristic
Identical axes across panels (state if not), consistent ordering, panel titles as data labels, shared legend/colour meaning, grid sized so each panel keeps a readable aspect; lazy-render offscreen panels.
- use when: More than ~6 series, or comparing the same chart across regions/products/devices.
- avoid when: When one combined chart with ≤4 series is readable.
- why: lexical 0.522, structural 0.2 (mode audit)

### Hover reveals need a non-hover path  `a11y-hover-not-required`  [rule/input; interaction/platform] score 0.341 · accessibility-requirement
Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover.
- use when: Row actions that appear on hover, tooltips, hover cards, mega menus.
- avoid when: Never rely on hover alone; touch and keyboard users never hover.
- why: lexical 0.129, structural 0.6 (input touch (stated), mode audit)

### List rows  `card-list-row`  [pattern/cards; layout/platform] score 0.322 · platform-standard
Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- use when: Homogeneous items on phones and in side panels: full-width rows with leading image/icon, title, secondary line, trailing meta, hairline dividers.
- avoid when: Items whose image is the recognition cue (use tiles/posters).
- incompatible with: card-poster-portrait, card-poster-landscape, surface-elevated-cards
- why: lexical 0.298, structural 0.24 (secondary mode)

### Horizontal rails (rows of content)  `layout-rails`  [pattern/layout; layout/platform] score 0.32 · platform-standard
Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- use when: TV browsing of categorised content: vertical axis moves between categories, horizontal axis moves within a category. The default TV home structure.
- avoid when: Fewer than ~8 items total (use a grid or list), or content that must be compared side by side.
- incompatible with: layout-single-column, layout-table-first, layout-three-pane, layout-dashboard-grid, nav-top-bar, nav-left-rail
- why: lexical 0.375, structural 0.12 (secondary mode)

### Target size by platform  `a11y-target-size`  [rule/input; interaction] score 0.307 · accessibility-requirement
Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon.
- use when: Every tappable/clickable element; especially icon buttons, table row actions, chips, close buttons, and pagination.
- avoid when: Inline text links inside a sentence are exempt from the size rule but still need spacing.
- why: lexical 0.035, structural 0.64 (input touch (stated), mode audit)

### Mobile: orientation changes and size classes  `mobile-orientation-size-classes`  [rule/responsive; layout/platform] score 0.28 · platform-standard
Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open.
- use when: Any screen that can rotate, run on tablets, or be shown in split view / multi-window; primary actions and navigation that must stay reachable in landscape.
- avoid when: Never lock orientation to dodge the layout work (accessibility exemptions aside); never let the keyboard or the landscape height push the primary action off screen.
- why: lexical 0.018, structural 0.6 (input touch (stated), mode audit)

### Mobile: image sizing, overdraw, and effect cost  `mobile-perf-images-overdraw`  [rule/performance; performance/platform] score 0.278 · engineering-practice
Request images at the rendered size (Coil/Glide/SDWebImage/expo-image with sizing), remove redundant opaque backgrounds (overdraw), keep list item composables/cells cheap and keyed, prefer opacity/transform animations, measure with the platform profiler (Perfetto, Instruments, Flipper).
- use when: Image-heavy lists, blur/shadow effects, nested backgrounds, animations in lists.
- avoid when: Never load original-resolution images into thumbnails; never animate blur or shadow radius in scrolling lists.
- incompatible with: surface-glass
- why: lexical 0.015, structural 0.6 (input touch (stated), mode audit)

### Mobile: keyboard and input types  `mobile-keyboard-ime`  [rule/forms; component/platform] score 0.278 · platform-standard
Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms.
- use when: Every text field.
- avoid when: Never leave the default keyboard for emails, numbers, phone, or URLs; never let the keyboard cover the focused field or the submit button.
- why: lexical 0.015, structural 0.6 (input touch (stated), mode audit)
