## guidance: The patient detail billing tab shows amounts that do not line up.
status=PARTIAL mode=['polish', 'audit'] platform=['web'] input=['keyboard', 'pointer', 'touch'] product=['healthcare'] screen=['detail'] stack=['svelte', 'tailwind'] density=None env=[] risk=medium negatives=[]
MISSING: brand: no brand assets, guideline, or character description available
budget=low mode evidence: polish: visual defect on existing UI | audit: diagnose first
project context: navigation={'value': 'left-rail', 'status': 'KNOWN', 'evidence': ['left-rail: 1 matches in +layout.svelte (shell/layout file)', 'also breadcrumb-tree: 1 matches']}, theme={'value': 'light-first', 'status': 'INFERRED', 'evidence': ['hex palette: 13 near-white, 1 near-black']}, surfaces={'value': 'bordered-flat', 'status': 'INFERRED', 'evidence': ['borders in 12 files, shadow/elevation in 2']}, radius={'value': 'unknown', 'status': 'UNKNOWN', 'evidence': []}, spacing={'value': 4, 'status': 'INFERRED', 'evidence': ['most used spacing values [16, 8, 12, 4, 24]', 'tailwind spacing classes (123)']}, typography={'value': 'custom', 'status': 'INFERRED', 'evidence': ['font family theme (1 refs)', 'tabular numerals']}, components={'value': 'tailwind', 'status': 'KNOWN', 'evidence': ['tailwind']}
concepts required=1.0 covered (1/1); tokens≈475 coverage/1k=2.11 purity=0.5
concerns required=['structure', 'anti-pattern', 'interaction', 'accessibility'] covered=0.5 uncovered=['anti-pattern', 'accessibility'] recommended=['content', 'component', 'adaptive', 'feedback'] bundle=3 (core 2 + guardrails 1) diversity=1.0 redundancy=0.0

### CORE (what to build)
- **Tabs** `comp-tabs` [component/interaction/navigation] — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
  - selected for: task evidence: component, lexical_strong; lexical 0.337, structural 0.36
- **Clinical workstation** `dir-clinical-workstation` [brand/structure] — Patient banner always visible (identity, allergies, alerts) as the focal element, master-detail for patient lists and records, strict status colour language with text and icons (never colour alone), large legible numerics with units, quiet neutral surfaces, confirmation for critical actions with the safe default, interruption-safe autosave. Identity via the banner treatment and status language; restraint is the brand.
  - selected for: task evidence: product; lexical 0.195, structural 0.6

### CRITICAL GUARDRAILS (must hold)
- **One type scale with named roles** `typo-scale-and-roles` [content/data-display; heuristic; SPECIFIC] — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
  - selected for: critical concept (SPECIFIC): tabular figures and numeric alignment

Omitted (redundant): layout-master-detail (no positive task evidence (screen / subtype / component / job / product / wording) for a core record); layout-editorial (no positive task evidence (screen / subtype / component / job / product / wording) for a core record); comp-product-detail-page (contamination: product-specific (ecommerce) vs ['healthcare']; low purity 0.20: most of its concepts are off-task); media-resume-and-details (contamination: product-specific (media) vs ['healthcare']; low purity 0.00: most of its concepts are off-task); comp-chart-container (no positive task evidence (screen / subtype / component / job / product / wording) for a core record); cta-sticky-bar (no positive task evidence (screen / subtype / component / job / product / wording) for a core record)
Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['web']); comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); comp-kiosk-keypad (platform ['kiosk', 'tablet'] not in request ['web']); comp-photo-capture-field (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-side-sheet (platform ['tv'] not in request ['web'])

Concept trace (explain): covered table.tabular_figures [CRITICAL SPECIFIC]
  - UNCOVERED layout.no_nested_cards: candidates existed but the bundle cap or a lower utility left them out (candidates anti-card-everything, card-none)
  - UNCOVERED process.safe_modification: candidates existed but the bundle cap or a lower utility left them out (candidates impl-safe-modification)
  - UNCOVERED touch.minimum_target: candidates existed but the bundle cap or a lower utility left them out (candidates comp-product-detail-page, media-photo-viewer, a11y-target-size)
  - UNCOVERED adaptive.breakpoint_matrix: candidates existed but the bundle cap or a lower utility left them out (candidates web-responsive-breakpoints)
  - UNCOVERED feedback.confirmation_destructive: candidates existed but the bundle cap or a lower utility left them out (candidates states-persistence-and-session, comp-plan-comparison, comp-dialog)
  - UNCOVERED layout.spacing_scale: candidates existed but the bundle cap or a lower utility left them out (candidates anti-inconsistent-spacing, layout-spacing-scale)
  - UNCOVERED layout.focal_hierarchy: candidates existed but the bundle cap or a lower utility left them out (candidates metadata-rich, typo-measure-and-rhythm, anti-oversized-hero-text)
  - UNCOVERED process.reuse_first: candidates existed but the bundle cap or a lower utility left them out (candidates impl-reuse-before-new)
