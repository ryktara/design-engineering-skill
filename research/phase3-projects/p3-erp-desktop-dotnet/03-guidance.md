## guidance: Purchase order lines grid for our WPF ERP client; clerks enter 200 lines a day with the keyboard
status=AMBIGUOUS mode=['create'] platform=['desktop'] input=['keyboard', 'pointer'] product=['erp'] screen=[] stack=['wpf'] density=high env=[] risk=low negatives=[]
MISSING: brand: no brand assets, guideline, or character description available
concerns required=['structure', 'states', 'interaction', 'accessibility', 'data-display'] covered=1.0 uncovered=[] recommended=['navigation', 'anti-pattern', 'brand'] bundle=6 (core 3 + guardrails 3) diversity=1.0 redundancy=0.33

### Core (what to build)
- **Data table / grid** `comp-data-table` [component/data-display/structure] — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
  - wpf: DataGrid with virtualisation flags; DevExpress GridControl if present in the project.
  - selected for: highest-scoring component with lexical evidence; lexical 0.573, structural 0.88
- **Operational workbench** `dir-operational-workbench` [brand/structure] — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
  - selected for: highest-scoring direction with lexical evidence; lexical 0.212, structural 0.88
- **Many series or groups → small multiples** `chart-small-multiples` [data-display] — Identical axes across panels (state if not), consistent ordering, panel titles as data labels, shared legend/colour meaning, grid sized so each panel keeps a readable aspect; lazy-render offscreen panels.
  - selected for: highest-scoring chart with lexical evidence; lexical 0.076, structural 0.6

### Guardrails (must hold)
- **Desktop: keyboard is a first-class input** `desktop-keyboard-first` [interaction; platform-standard] — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
  - selected for: most relevant record for the request wording
- **Search and filters: visible state and instant feedback** `search-filter-feedback` [component/feedback/states; heuristic] — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails.
  - selected for: required concern states: every screen ships empty/loading/error states
- **Everything operable by keyboard, no traps** `a11y-keyboard-operable` [accessibility/interaction; accessibility-requirement] — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
  - selected for: required concern accessibility: platform accessibility baseline

Omitted (redundant): comp-data-entry-grid (same category as a core pick or incompatible with one); dir-windows-native-tool (same category as a core pick or incompatible with one)
Filtered out: anti-hero-template (platform ['web'] not in request ['desktop']); anti-desktop-scaled-to-tv (platform ['tv'] not in request ['desktop']); comp-media-card (platform ['mobile', 'tv', 'web'] not in request ['desktop']); comp-player-controls (platform ['mobile', 'tv', 'web'] not in request ['desktop']); comp-epg (platform ['tablet', 'tv', 'web'] not in request ['desktop']); comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['desktop'])
