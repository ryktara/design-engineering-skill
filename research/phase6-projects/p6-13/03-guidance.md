## guidance: The habit list has nothing to say the first time you open the app.
status=PARTIAL mode=['audit', 'refactor'] platform=['mobile'] input=['touch'] product=[] screen=[] stack=['swiftui'] density=None env=[] risk=low negatives=[]
budget=moderate mode evidence: audit: problem statement on existing UI | refactor: fix follows the diagnosis
project context: navigation={'value': 'bottom-tabs', 'status': 'KNOWN', 'evidence': ['bottom-tabs: 7 matches in README.md, RootTabView.swift, StreaksApp.swift (shell/layout file)']}, theme={'value': 'dual-theme', 'status': 'KNOWN', 'evidence': ['dark theme configuration signals: 2', 'root/canvas backgrounds: 2 light, 2 dark', 'hex palette: 7 near-white, 6 near-black'], 'default': 'light'}, surfaces={'value': 'elevated', 'status': 'INFERRED', 'evidence': ['shadow/elevation in 5 files, borders in 1']}, radius={'value': 'small', 'status': 'INFERRED', 'evidence': ['most common radius 5 (4×); others [3.0, 8.0]']}, spacing={'value': 'irregular', 'status': 'UNKNOWN', 'evidence': ['most used spacing values [6, 32, 2, 3, 4]']}, typography={'value': 'custom', 'status': 'KNOWN', 'evidence': ['font family System (7 refs)', 'weights 600, 500, 700, 800', 'encoded type scale in 4 files']}, components={'value': 'unknown', 'status': 'UNKNOWN', 'evidence': []}
concepts required=1.0 covered (2/2); tokens≈277 coverage/1k=7.22 purity=0.83
concerns required=['accessibility', 'interaction', 'component'] covered=0.67 uncovered=['accessibility'] recommended=['states', 'anti-pattern', 'feedback', 'adaptive'] bundle=2 (core 2 + guardrails 0) diversity=1.0 redundancy=0.0

### CORE (what to build)
- **Mobile list and swipe actions** `comp-list-row-mobile` [component/data-display/interaction] — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_
  - swiftui: List with .swipeActions and Sections; LazyVStack only when List styling is impossible.
  - selected for: task evidence: component, lexical_strong; lexical 0.354, structural 0.58
- **Empty / zero state** `comp-empty-state` [states] — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
  - selected for: task evidence: lexical_strong; lexical 0.413, structural 0.4

Omitted (redundant): comp-pagination (same category as a core pick (adds no new concept) or incompatible with one); chart-trend-line (contamination: product-specific with product unknown; low purity 0.00: most of its concepts are off-task; chart record outside a data-visualisation task)
Filtered out: anti-hero-template (platform ['web'] not in request ['mobile']); anti-generic-sidebar-dashboard (platform ['desktop', 'web'] not in request ['mobile']); anti-default-fonts (platform ['web'] not in request ['mobile']); chart-relationship (platform ['desktop', 'web'] not in request ['mobile']); chart-realtime (platform ['desktop', 'tv', 'web'] not in request ['mobile']); comp-data-table (platform ['desktop', 'web'] not in request ['mobile'])

Concept trace (explain): covered state.loading_empty_error, touch.minimum_target, touch.gestures_discoverable
  - UNCOVERED a11y.accessible_names: candidates existed but the bundle cap or a lower utility left them out (candidates a11y-native-semantics, comp-photo-capture-field, comp-player-controls)
  - UNCOVERED a11y.contrast: candidates existed but the bundle cap or a lower utility left them out (candidates anti-fashion-over-usability, a11y-contrast-text, a11y-nontext-contrast)
  - UNCOVERED process.reuse_first: candidates existed but the bundle cap or a lower utility left them out (candidates impl-reuse-before-new)
  - UNCOVERED touch.thumb_reach: candidates existed but the bundle cap or a lower utility left them out (candidates mobile-thumb-reach, anti-mobile-desktop-shrunk, cta-sticky-bar)
  - UNCOVERED touch.safe_areas: candidates existed but the bundle cap or a lower utility left them out (candidates mobile-orientation-size-classes, mobile-safe-areas, cta-sticky-bar)
  - UNCOVERED navigation.platform_grammar: candidates existed but the bundle cap or a lower utility left them out (candidates mobile-platform-navigation, nav-bottom-tabs)
