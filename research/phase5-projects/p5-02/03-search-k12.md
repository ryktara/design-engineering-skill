## design-engineering search: Add a team members page with an invite flow, consistent with the rest of the settings area.
status=PARTIAL modes=['create'] platforms={} inputs={} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['layout', 'navigation', 'direction'] unmet=['direction'] diversity=0.58
MISSING: platform: not stated and not detectable from a repository; product: product family / primary user task not stated; brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence

### Settings screen  `comp-settings-screen`  [component/settings; component] score 0.345 · platform-standard
Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).
- use when: Preferences, account, notifications, appearance.
- avoid when: Never bury frequently changed settings three levels deep; never use toggles for actions.
- why: lexical 0.333, structural 0.36 (mode create)

### Flows between states → Sankey / alluvial  `chart-flow-sankey`  [chart/chart; data-viz/platform] score 0.295 · heuristic
≤~12 nodes, link width proportional to flow, node labels with totals, hover/focus isolates a path, consistent node ordering to reduce crossings, table alternative mandatory.
- use when: Quantities moving between categories (budget allocation, user paths, energy).
- avoid when: Few nodes (a table is clearer), audiences unfamiliar with the form, mobile widths.
- why: lexical 0.374, structural 0.2 (mode create)

### Trend over time → line / area  `chart-trend-line`  [chart/chart; data-viz] score 0.289 · heuristic
Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data.
- use when: Continuous measure over time; rate of change matters; 1–6 series.
- avoid when: Fewer than 4 points (use a stat + delta), more than ~6 series (small multiples), discrete categories (bars), cumulative composition (stacked area only if parts sum meaningfully).
- why: lexical 0.281, structural 0.3 (mode create)

### Form stack with sections  `layout-form-stack`  [pattern/layout; layout] score 0.284 · heuristic
Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- use when: Data entry and settings: labelled fields in one column, grouped into titled sections, with the save/submit action fixed in a predictable place.
- avoid when: Spreadsheet-style batch entry (use a data-entry grid), or tiny forms of 1–2 fields (inline them).
- incompatible with: layout-immersive-rails, layout-rails
- why: lexical 0.113, structural 0.36 (mode create)

### Mobile: safe areas and system insets  `mobile-safe-areas`  [rule/layout; layout/platform] score 0.283 · platform-standard
Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view.
- use when: Bottom bars, sticky CTAs, full-bleed backgrounds, top app bars, landscape.
- avoid when: Never hard-code status/nav bar heights.
- why: lexical 0.187, structural 0.4 (mode create)

### One primary action per screen  `cta-single-primary`  [pattern/cta; layout] score 0.269 · heuristic
Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- use when: Task screens (forms, checkout, onboarding, settings) where one action completes the job; the primary is filled, secondaries are quiet.
- avoid when: Workbenches with many equal commands (toolbar pattern) or browse screens where selection is the action (focus-selects).
- incompatible with: cta-toolbar-commands, cta-focus-selects
- why: lexical 0.03, structural 0.36 (mode create)

### Plan comparison and billing management  `comp-plan-comparison`  [component/settings; component/platform] score 0.253 · heuristic
Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- use when: Billing/plan pages: choosing or changing a plan, seat management, invoice history, payment method.
- avoid when: Public pricing marketing pages (hero + narrative) or checkout for a one-off purchase.
- why: lexical 0.248, structural 0.26 (mode create)

### Users always know where they are and how to go back  `nav-orientation-and-back`  [rule/navigation; navigation] score 0.246 · heuristic
Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there.
- use when: Every navigation model; deep links; multi-step flows; tabs that hold stacks.
- avoid when: Never break the browser/system back; never use a single URL for many states on the web.
- why: lexical 0.037, structural 0.5 (mode create)

### UI changes must not break routes, state, contracts, or tests  `impl-safe-modification`  [rule/implementation; process] score 0.238 · engineering-practice
Keep routes, state management, API calls, data-testid/automation ids, accessibility semantics, keyboard/remote handling, playback/auth flows unchanged unless the task is about them; run the existing tests; verify each supported input mode still works after the change.
- use when: Any modification to an existing screen.
- avoid when: Never rename props/ids/routes/test hooks as part of a visual change; never mix backend changes into a UI commit.
- why: lexical 0.024, structural 0.5 (mode create)

### Target size by platform  `a11y-target-size`  [rule/input; interaction] score 0.236 · accessibility-requirement
Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon.
- use when: Every tappable/clickable element; especially icon buttons, table row actions, chips, close buttons, and pagination.
- avoid when: Inline text links inside a sentence are exempt from the size rule but still need spacing.
- why: lexical 0.07, structural 0.44 (mode create)

### Bottom tab bar  `nav-bottom-tabs`  [pattern/navigation; navigation/platform] score 0.227 · platform-standard
3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination.
- use when: Phone apps with 3–5 top-level destinations of similar importance that users switch between often.
- avoid when: More than five destinations, tablet/desktop widths (use a rail), single-flow apps, or when one destination dominates usage.
- incompatible with: nav-left-rail, nav-top-bar, nav-tv-side, nav-tv-top-tabs
- why: lexical 0.055, structural 0.26 (mode create)

### Sticky action bar  `cta-sticky-bar`  [pattern/cta; layout/platform] score 0.225 · heuristic
Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- use when: Long forms or detail pages where the primary action must stay reachable (Add to cart, Save, Continue).
- avoid when: Short screens, TV, or when the bar would cover content without a scroll padding compensation.
- incompatible with: cta-focus-selects, layout-rails
- why: lexical 0.21, structural 0.2 (mode create)
