## design-engineering search: Review the stock adjustments page against our accessibility checklist.
status=PARTIAL modes=['accessibility', 'audit', 'review'] platforms={} inputs={} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'anti-pattern'] unmet=[] diversity=0.75
MISSING: platform: audit targets differ by platform; not stated

### Product detail page (PDP)  `comp-product-detail-page`  [component/detail; component/platform] score 0.38 · heuristic
Above the fold on every viewport: product name, price (with tabular figures and any discount stated in words), primary image, variant selectors and one add-to-cart action; variant choice is a radio group with visible labels and a disabled-but-visible state for out-of-stock options; the add-to-cart button is sticky on phones without covering focused controls; shipping, returns and stock are stated next to the price, not in a tab; the gallery has fixed aspect boxes (no layout shift), keyboard-operable thumbnails and alt text per image; reviews show the distribution and a count, and stars always have a text value; secondary actions (wishlist, share, size guide) never compete visually with add-to-cart; the size guide opens as a dialog that returns focus.
- use when: Selling a physical or digital product: gallery, variants, price, availability, add-to-cart, trust and shipping information, reviews.
- avoid when: Catalog/listing pages (use list + filters) or marketing landing pages (hero + narrative).
- why: lexical 0.544, structural 0.18 (secondary mode)

### Setup / progress checklist  `comp-setup-checklist`  [component/wizard; component/platform] score 0.333 · heuristic
A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position.
- use when: Multi-session onboarding where tasks can be done in any order over days (connect data, invite team, verify identity, complete profile).
- avoid when: Strictly ordered dependent steps (use a wizard) or a single setup action.
- why: lexical 0.408, structural 0.24 (secondary mode)

### Native accessibility semantics (mobile/desktop)  `a11y-native-semantics`  [rule/accessibility; accessibility/platform] score 0.311 · accessibility-requirement
Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code.
- use when: Custom composables/views/controls, merged semantics for cards, live regions for status, headings in long screens.
- avoid when: Never build a tappable Box/View/Border without a role and name.
- why: lexical 0.189, structural 0.46 (mode accessibility)

### Non-text contrast 3:1 for controls and focus  `a11y-nontext-contrast`  [rule/accessibility; accessibility] score 0.294 · accessibility-requirement
Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails.
- use when: Input borders, checkbox/radio outlines, focus indicators, icons that carry meaning, chart marks, toggle states.
- avoid when: Purely decorative borders and dividers are exempt, but then they must not be the only boundary of a control.
- why: lexical 0.126, structural 0.5 (mode accessibility)

### No decorative imagery  `imagery-none`  [pattern/imagery; visual] score 0.246 · heuristic
Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- use when: Operational products: imagery only where it is data (avatars, product thumbnails, charts).
- avoid when: Brand or content products where imagery is the content.
- incompatible with: imagery-hero, imagery-immersive-backdrop, surface-imagery-backed
- why: lexical 0.206, structural 0.14 (generic)

### Visible focus ring (web/desktop)  `focus-ring-standard`  [pattern/focus; interaction/platform] score 0.232 · accessibility-requirement
One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- use when: All pointer+keyboard UI: a 2–3 px ring with ≥3:1 contrast against adjacent colours, offset so it is not hidden by borders, shown for :focus-visible.
- avoid when: TV (needs scale/glow because the ring is too subtle at 3 m).
- incompatible with: focus-scale-glow, focus-none-touch-only
- why: lexical 0.064, structural 0.26 (mode accessibility)

### UI changes must not break routes, state, contracts, or tests  `impl-safe-modification`  [rule/implementation; process] score 0.213 · engineering-practice
Keep routes, state management, API calls, data-testid/automation ids, accessibility semantics, keyboard/remote handling, playback/auth flows unchanged unless the task is about them; run the existing tests; verify each supported input mode still works after the change.
- use when: Any modification to an existing screen.
- avoid when: Never rename props/ids/routes/test hooks as part of a visual change; never mix backend changes into a UI commit.
- why: lexical 0.045, structural 0.42 (secondary mode)

### Scale + glow/border focus (TV)  `focus-scale-glow`  [pattern/focus; interaction/platform] score 0.213 · platform-standard
Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- use when: All TV UI: focused item scales (1.05–1.1), gains a border or glow with ≥3:1 contrast, and its metadata may expand; unfocused items stay quiet.
- avoid when: Never elsewhere; and on TV never rely on colour tint alone.
- incompatible with: focus-ring-standard, focus-none-touch-only, focus-underline
- why: lexical 0.03, structural 0.26 (mode accessibility)

### Glassmorphism without a reason  `anti-glass-everywhere`  [antipattern/generic-ai; anti-pattern] score 0.208 · heuristic
Replace with solid tonal surfaces unless the layer must reveal content beneath it; if kept, use the platform material, verify contrast against worst-case backgrounds, and measure GPU cost on low-end devices and TV.
- use when: Frosted panels, blurred cards, translucent nav bars in application UI.
- avoid when: Platform materials for transient layers (sheets, menus) are legitimate.
- incompatible with: surface-glass
- why: lexical 0.035, structural 0.42 (secondary mode)

### Wizard / stepper  `comp-wizard-stepper`  [component/wizard; component] score 0.208 · heuristic
Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action.
- use when: Ordered multi-step flows (checkout, applications, setup).
- avoid when: Independent sections (tabs); flows that fit one screen.
- why: lexical 0.198, structural 0.22 (secondary mode)

### Platform icon set  `icon-platform-native`  [pattern/icon; platform/visual] score 0.192 · platform-standard
Use the platform set with its variable weight/fill axes rather than importing a web set; align icon weight to text weight; provide accessibility labels via the platform API.
- use when: Native apps: SF Symbols on Apple, Material Symbols on Android/TV, Fluent/Segoe Fluent Icons on Windows, so weight, scale, and accessibility metadata match the platform.
- avoid when: Multi-brand products needing custom glyph identity.
- incompatible with: icon-duotone, icon-custom-glyphs
- why: lexical 0.109, structural 0.16 (generic)

### One-page checkout  `comp-checkout-one-page`  [component/form; component/platform] score 0.18 · heuristic
Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries.
- use when: Purchase flows with contact, shipping, payment and review on one scrolling page.
- avoid when: Multi-session or regulated flows that need a stepper with server-side validation per step.
- incompatible with: nav-wizard
- why: lexical 0.18, structural 0.18 (secondary mode)
