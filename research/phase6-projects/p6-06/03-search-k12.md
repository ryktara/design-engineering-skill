## design-engineering search: The patient detail billing tab shows amounts that do not line up.
status=CONFIDENT modes=['polish', 'audit'] platforms={} inputs={} products={'healthcare': 'KNOWN'} density=None stacks=[] screens=['detail'] negatives=[]
facets required=['anti-pattern', 'layout', 'visual', 'component'] unmet=[] diversity=0.83
MISSING: brand: no brand assets, guideline, or character description available; platform: audit targets differ by platform; not stated

### Media details screen, resume playback and watchlist  `media-resume-and-details`  [component/detail; component/platform] score 0.461 · platform-standard
Details: the primary action is Play (or Resume with the remaining time and a Start over alternative) and it takes default focus; metadata is a short scannable block (duration, year, rating, badges as text not colour), synopsis ≤3 lines with an expander, episodes as a rail or list with progress bars and the next unwatched episode preselected; secondary actions (watchlist, trailer, more like this) sit after Play in one row. Resume: a continue-watching row shows progress on each card, resumes at the saved position, and removes finished items; entering a title from the row returns focus to that card. Watchlist: one toggle with a clear on/off state and text label, works from cards and details, and is reflected immediately in the watchlist row. Everything is reachable with D-pad UP/DOWN/LEFT/RIGHT and BACK returns to the row that launched the details.
- use when: Title/episode details, continue-watching rows, watchlist actions in a streaming or catch-up app.
- avoid when: Live-only channels without on-demand content (use the guide and player rules).
- why: lexical 0.707, structural 0.16 (secondary mode, product mismatch, screen detail)

### Master–detail (list + detail pane)  `layout-master-detail`  [pattern/layout; layout/platform] score 0.384 · platform-standard
List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- use when: Users scan a list of records and act on one at a time (tickets, orders, patients, mail); wide enough for two panes (≥ ~900 px / 641 epx).
- avoid when: Phone widths (collapse to list → push detail), records that need the full width (large tables, editors), or when the list has only a handful of items.
- incompatible with: layout-single-column, layout-immersive-rails, layout-rails
- why: lexical 0.294, structural 0.36 (product healthcare, screen detail)

### Tabs  `comp-tabs`  [component/tabs; component] score 0.329 · platform-standard
Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content.
- use when: Peer views of the same object (Details / Activity / Files) at the same level.
- avoid when: Sequential steps (wizard), primary navigation on web (use nav), more than ~6 tabs (use a select or side nav), tabs that hide required form fields.
- why: lexical 0.337, structural 0.32 (secondary mode)

### Product detail page (PDP)  `comp-product-detail-page`  [component/detail; component/platform] score 0.319 · heuristic
Above the fold on every viewport: product name, price (with tabular figures and any discount stated in words), primary image, variant selectors and one add-to-cart action; variant choice is a radio group with visible labels and a disabled-but-visible state for out-of-stock options; the add-to-cart button is sticky on phones without covering focused controls; shipping, returns and stock are stated next to the price, not in a tab; the gallery has fixed aspect boxes (no layout shift), keyboard-operable thumbnails and alt text per image; reviews show the distribution and a count, and stars always have a text value; secondary actions (wishlist, share, size guide) never compete visually with add-to-cart; the size guide opens as a dialog that returns focus.
- use when: Selling a physical or digital product: gallery, variants, price, availability, add-to-cart, trust and shipping information, reviews.
- avoid when: Catalog/listing pages (use list + filters) or marketing landing pages (hero + narrative).
- why: lexical 0.335, structural 0.3 (mode polish, product mismatch, screen detail)

### Measure, rhythm, and hierarchy by contrast of size and weight  `typo-measure-and-rhythm`  [rule/typography; visual] score 0.307 · heuristic
45–75 characters per line for prose; vertical spacing from the spacing scale tied to line height; hierarchy from clear jumps (≥1.25×) in size or weight, not from five near-identical sizes; headings closer to the content below than to the content above.
- use when: Reading content, forms, dashboards with mixed text.
- avoid when: Never make everything bold; never use more than two weights per role.
- why: lexical 0.117, structural 0.54 (mode polish)

### Trend over time → line / area  `chart-trend-line`  [chart/chart; data-viz] score 0.285 · heuristic
Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data.
- use when: Continuous measure over time; rate of change matters; 1–6 series.
- avoid when: Fewer than 4 points (use a stat + delta), more than ~6 series (small multiples), discrete categories (bars), cumulative composition (stacked area only if parts sum meaningfully).
- why: lexical 0.141, structural 0.46 (secondary mode, product healthcare)

### One type scale with named roles  `typo-scale-and-roles`  [rule/typography; visual] score 0.275 · heuristic
Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles.
- use when: Any screen with more than two text sizes; any design system.
- avoid when: Never pick sizes per screen; never use more than ~7 sizes.
- why: lexical 0.058, structural 0.54 (mode polish)

### Cards inside cards, everything in a rounded box  `anti-card-everything`  [antipattern/generic-ai; anti-pattern] score 0.269 · heuristic
Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid.
- use when: Reviewing any layout where sections, lists, forms, and even single lines are wrapped in bordered/elevated containers.
- avoid when: A card is fine when the item is a discrete tappable object or needs elevation (drag, overlay).
- why: lexical 0.047, structural 0.54 (mode polish)

### TV top tabs  `nav-tv-top-tabs`  [pattern/navigation; navigation/platform] score 0.267 · platform-standard
Tabs sit in the top safe area; Back from any rail jumps focus to the active tab and scrolls to top; focused tab shows the underline/pill with ≥3:1 contrast and the label stays visible. Switching tabs does not move focus into content until the user presses DOWN.
- use when: Two to five sections, when the left edge must stay free for immersive artwork or when the brand wants a browsing feel closer to a broadcast guide.
- avoid when: More than five sections, or when rows below are long (UP from deep rows must scroll back to tabs predictably; that gets slow).
- incompatible with: nav-tv-side, nav-top-bar, nav-left-rail, nav-bottom-tabs
- why: lexical 0.297, structural 0.14 (generic)

### UI changes must not break routes, state, contracts, or tests  `impl-safe-modification`  [rule/implementation; process] score 0.266 · engineering-practice
Keep routes, state management, API calls, data-testid/automation ids, accessibility semantics, keyboard/remote handling, playback/auth flows unchanged unless the task is about them; run the existing tests; verify each supported input mode still works after the change.
- use when: Any modification to an existing screen.
- avoid when: Never rename props/ids/routes/test hooks as part of a visual change; never mix backend changes into a UI commit.
- why: lexical 0.041, structural 0.54 (mode polish)

### Functional minimal motion  `motion-functional-minimal`  [pattern/motion; visual] score 0.264 · heuristic
Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- use when: Default for application UI: motion only for state change, continuity (open/close, expand), and feedback; 120–250 ms, ease-out for entering, ease-in for leaving.
- avoid when: Brand moments (launch, onboarding) that deliberately need more; then use 'expressive' for those moments only.
- incompatible with: motion-cinematic, motion-expressive
- why: lexical 0.007, structural 0.4 (mode polish)

### Focus-revealed metadata (TV)  `metadata-focus-reveal`  [pattern/metadata; layout/platform] score 0.263 · platform-standard
Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.
- use when: TV rails: unfocused cards show title only (or nothing over art); the focused card or a fixed detail strip shows synopsis, year, duration, rating.
- avoid when: Never for touch/pointer; and on TV avoid when the reveal reflows the rail (use a fixed strip instead).
- incompatible with: metadata-rich, layout-table-first
- why: lexical 0.237, structural 0.14 (generic)

Filtered out: mobile-field-use (environment ['gloves', 'outdoor'] not in request)
