## guidance: Stock adjustment form: Save and Discard look identical and people click the wrong one.
status=CONFIDENT mode=['polish', 'audit'] platform=['web'] input=['keyboard', 'pointer', 'touch'] product=[] screen=['form'] stack=['vue'] density=None env=[] risk=low negatives=[]
MISSING: brand: no brand assets, guideline, or character description available
budget=low mode evidence: polish: visual defect on existing UI | audit: diagnose first
project context: navigation={'value': 'top-bar', 'status': 'KNOWN', 'evidence': ['top-bar: 8 matches in App.vue, TopBar.vue, tokens.css (shell/layout file)']}, theme={'value': 'unknown', 'status': 'UNKNOWN', 'evidence': ['hex palette: 11 near-white, 6 near-black']}, surfaces={'value': 'bordered-flat', 'status': 'INFERRED', 'evidence': ['borders in 11 files, shadow/elevation in 2']}, radius={'value': 'small', 'status': 'INFERRED', 'evidence': ['most common radius 5 (1×); others [6.0]']}, spacing={'value': 'irregular', 'status': 'UNKNOWN', 'evidence': ['most used spacing values [6, 4, 2]']}, typography={'value': 'humanist-sans', 'status': 'KNOWN', 'evidence': ['font family IBM Plex Sans (2 refs)', 'weights 600, 500', 'encoded type scale in 1 files']}, components={'value': 'unknown', 'status': 'UNKNOWN', 'evidence': []}
concepts required=1.0 covered (3/3); tokens≈1059 coverage/1k=2.83 purity=0.76
concerns required=['structure', 'anti-pattern', 'interaction', 'accessibility', 'feedback'] covered=1.0 uncovered=[] recommended=['content', 'component', 'adaptive'] bundle=6 (core 3 + guardrails 3) diversity=0.83 redundancy=0.38

### CORE (what to build)
- **Dialog / modal** `comp-dialog` [accessibility/component/feedback/interaction] — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
  - selected for: critical concept (GENERIC): confirmation of destructive or high-risk actions; lexical 0.05, structural 0.36
- **Form** `comp-form` [component/feedback/states/structure] — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
  - selected for: task evidence: screen, component, lexical_strong; lexical 0.426, structural 0.44
- **Form stack with sections** `layout-form-stack` [structure] — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
  - selected for: task evidence: screen, lexical_strong; lexical 0.463, structural 0.36

### CRITICAL GUARDRAILS (must hold)
- **Brands that differ only by logo, primary colour, and font** `anti-brand-cosmetic-only` [anti-pattern; heuristic; GENERIC] — Run fingerprint.py compare on the candidate brand systems; a COSMETIC-ONLY verdict fails differentiation. Vary at least two structural axes (navigation model, layout topology, density, surface strategy, image strategy, metadata density, CTA strategy) per brand, then cosmetics. _(covers: structural, not cosmetic, brand differentiation)_
  - selected for: critical concept (GENERIC): structural, not cosmetic, brand differentiation
- **Design empty, loading, error, and partial states** `layout-states-empty-loading-error` [states; heuristic; GENERIC] — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
  - selected for: required coverage (GENERIC): loading, empty and error states

### OPTIONAL NOTES (apply only when they fit)
- **One clear focal point per screen** `layout-hierarchy-one-thing` [data-display/structure; heuristic; SPECIFIC] — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
  - selected for: recommended coverage (SPECIFIC): visual hierarchy with one focal point

Omitted (redundant): comp-checkout-one-page (contamination: product-specific with product unknown; screen-specific (checkout) vs ['form'])
Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['web']); comp-tv-rail (platform ['tv'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); comp-kiosk-keypad (platform ['kiosk', 'tablet'] not in request ['web']); comp-photo-capture-field (platform ['mobile', 'tablet'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web'])

Concept trace (explain): covered feedback.confirmation_destructive [CRITICAL GENERIC], brand.structural_differentiation [CRITICAL GENERIC], state.loading_empty_error, state.unsaved_changes_guard, feedback.validation_errors, form.autofill_attributes, layout.focal_hierarchy
  - UNCOVERED layout.no_nested_cards: candidates existed but the bundle cap or a lower utility left them out (candidates anti-card-everything, card-none)
  - UNCOVERED process.safe_modification: candidates existed but the bundle cap or a lower utility left them out (candidates impl-safe-modification)
  - UNCOVERED state.saving_conflict: candidates existed but the bundle cap or a lower utility left them out (candidates states-persistence-and-session, comp-checkout-one-page, states-offline-and-sync)
  - UNCOVERED touch.minimum_target: candidates existed but the bundle cap or a lower utility left them out (candidates media-photo-viewer, a11y-target-size, comp-product-detail-page)
  - UNCOVERED adaptive.breakpoint_matrix: candidates existed but the bundle cap or a lower utility left them out (candidates web-responsive-breakpoints)
  - UNCOVERED layout.spacing_scale: candidates existed but the bundle cap or a lower utility left them out (candidates anti-inconsistent-spacing, layout-spacing-scale)
  - UNCOVERED process.reuse_first: candidates existed but the bundle cap or a lower utility left them out (candidates impl-reuse-before-new)
  - UNCOVERED interaction.keyboard_navigation: candidates existed but the bundle cap or a lower utility left them out (candidates interaction-drag-drop, grid-single-tab-stop, a11y-skip-link)
