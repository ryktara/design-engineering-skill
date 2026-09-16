## design-engineering search: From the sofa nobody can tell which row is selected on the living-room screen.
status=CONFIDENT modes=['audit', 'refactor'] platforms={'tv': 'INFERRED'} inputs={'remote': 'INFERRED'} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'platform', 'anti-pattern'] unmet=[] diversity=0.83
MISSING: platform: only inferred from wording (tv); confirm before committing

### Every interactive colour has hover/pressed/focus/disabled/selected  `color-states-complete`  [rule/color; visual] score 0.458 · heuristic
Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them.
- use when: Buttons, links, list rows, tabs, chips, inputs, cards that are tappable, focus on TV.
- avoid when: Never leave a state to the framework default on one platform and custom on another.
- why: lexical 0.391, structural 0.54 (mode audit)

### Horizontal rails (rows of content)  `layout-rails`  [pattern/layout; layout/platform] score 0.414 · platform-standard
Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- use when: TV browsing of categorised content: vertical axis moves between categories, horizontal axis moves within a category. The default TV home structure.
- avoid when: Fewer than ~8 items total (use a grid or list), or content that must be compared side by side.
- incompatible with: layout-single-column, layout-table-first, layout-three-pane, layout-dashboard-grid, nav-top-bar, nav-left-rail
- why: lexical 0.283, structural 0.44 (platform tv, input remote, secondary mode)

### Privacy on shared and public screens  `shared-device-privacy`  [rule/privacy; accessibility/platform] score 0.389 · heuristic
Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value.
- use when: TVs in a household, waiting-room tablets, kiosks, wall displays, any screen other people can see; personal data, balances, health details, viewing history, messages.
- avoid when: Single-user personal devices with a lock screen already protecting the data.
- why: lexical 0.167, structural 0.66 (platform tv, mode audit)

### TV rail (horizontal row of cards)  `comp-tv-rail`  [component/tv-rail; component/platform] score 0.381 · platform-standard
Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp).
- use when: Categorised browsing on TV home, section, and search screens.
- avoid when: Fewer than ~4 items (use a grid row), comparison tasks.
- incompatible with: layout-table-first
- why: lexical 0.268, structural 0.52 (platform tv, input remote, mode audit)

### TV: 10-foot typography  `tv-typography-distance`  [rule/typography; platform/visual] score 0.367 · platform-standard
Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3.
- use when: All text on TV.
- avoid when: Never scale a desktop type ramp up by a factor; rebuild the scale for distance and for reduced text volume.
- incompatible with: typography-serif-editorial
- why: lexical 0.078, structural 0.72 (platform tv, input remote, mode audit)

### TV: vertical = sections, horizontal = items  `tv-dpad-axes`  [rule/navigation; navigation/platform] score 0.333 · platform-standard
Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances.
- use when: Any TV layout: rails, grids, menus, settings, forms.
- avoid when: Avoid nested horizontal groups inside horizontal groups; avoid controls placed where no straight DPAD path reaches them.
- why: lexical 0.016, structural 0.72 (platform tv, input remote, mode audit)

### TV: focus response and list performance  `tv-focus-performance`  [rule/performance; performance/platform] score 0.332 · engineering-practice
Focus moves must render within one frame (≤16 ms at 60 Hz) even while images load; key events are never dropped or coalesced into jumps; images sized to card, cached, and loaded with placeholders; rows virtualised vertically and horizontally; heavy backdrops debounced; test on the cheapest target device (e.g. 1–2 GB RAM set-top boxes), not the emulator.
- use when: Rails, grids, EPG, any list on TV; especially with images.
- avoid when: Never decode full-size artwork for thumbnails; never render all rails at once.
- why: lexical 0.015, structural 0.72 (platform tv, input remote, mode audit)

### TV: predictable BACK  `tv-back-behavior`  [rule/navigation; navigation/platform] score 0.332 · platform-standard
BACK closes the topmost layer (player controls → player → detail → home → nav → exit); in a rail-based home, BACK from content first moves focus to the navigation (side nav or top tabs) and scrolls to top, then exits. Deep-linked entries still unwind to the app home. Splash screens are never in the back stack.
- use when: Every screen and overlay.
- avoid when: Never show an on-screen Back button (the remote has one); never trap the user in an exit-confirmation loop.
- why: lexical 0.014, structural 0.72 (platform tv, input remote, mode audit)

### TV: overscan-safe margins  `tv-safe-area`  [rule/layout; layout/platform] score 0.331 · platform-standard
Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content.
- use when: All persistent UI (nav, titles, buttons, subtitles); backgrounds and artwork may bleed.
- avoid when: Do not inset full-bleed imagery; do not rely on the panel reporting overscan.
- why: lexical 0.013, structural 0.72 (platform tv, input remote, mode audit)

### Focus is the action (TV)  `cta-focus-selects`  [pattern/cta; layout/platform] score 0.329 · platform-standard
No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- use when: TV browse/detail screens: the focused card is the call to action, SELECT opens, and detail screens expose a small row of focusable buttons (Play, Resume, Add to list) with a deterministic first focus.
- avoid when: Never on touch/pointer platforms.
- incompatible with: cta-single-primary, cta-toolbar-commands, cta-sticky-bar
- why: lexical 0.043, structural 0.5 (platform tv, input remote, secondary mode)

### Focus visible and not obscured  `a11y-focus-visible`  [rule/focus; interaction/platform] score 0.324 · accessibility-requirement
Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
- use when: Every focusable element in every theme; sticky headers, footers, toasts, and cookie banners must never cover the focused element.
- avoid when: Never remove focus styles; use :focus-visible to hide them for mouse clicks only.
- why: lexical 0.0, structural 0.72 (platform tv, input remote, mode audit)

### A desktop or mobile layout enlarged for TV  `anti-desktop-scaled-to-tv`  [antipattern/platform; anti-pattern/platform] score 0.324 · platform-standard
Rebuild around focus: rails and grids, side/top navigation, one visible focus, 10-foot type scale, safe margins, minimal text entry, transport controls, BACK semantics. Reuse data and business logic, not the layout.
- use when: TV screens with hover menus, small links, scrollbars, sidebars with 12 items, forms with many fields, hamburger menus, touch gestures, mouse-oriented layouts.
- avoid when: Never.
- why: lexical 0.0, structural 0.72 (platform tv, input remote, mode audit)

Filtered out: anti-hero-template (platform ['web'] not in request ['tv']); anti-generic-sidebar-dashboard (platform ['desktop', 'web'] not in request ['tv']); anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['tv']); anti-default-fonts (platform ['web'] not in request ['tv']); anti-hover-only-actions (platform ['desktop', 'web'] not in request ['tv']); chart-heatmap-matrix (platform ['desktop', 'web'] not in request ['tv']); comp-data-table (platform ['desktop', 'web'] not in request ['tv']); comp-filters (platform ['desktop', 'mobile', 'web'] not in request ['tv'])
