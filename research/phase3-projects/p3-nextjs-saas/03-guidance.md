## guidance: Add a team billing settings page with plan comparison, seat management table and invoice history to our Next.js SaaS admin
status=CONFIDENT mode=['create'] platform=['web'] input=['keyboard', 'pointer', 'touch'] product=['finance', 'saas'] screen=['settings'] stack=['nextjs', 'react', 'shadcn', 'tailwind'] density=high env=[] risk=medium negatives=[]
MISSING: brand: no brand assets, guideline, or character description available
concerns required=['component', 'structure', 'states', 'interaction', 'accessibility', 'data-display'] covered=1.0 uncovered=[] recommended=['navigation', 'anti-pattern', 'brand', 'adaptive', 'feedback'] bundle=7 (core 3 + guardrails 4) diversity=0.86 redundancy=0.31

### Core (what to build)
- **Operational workbench** `dir-operational-workbench` [brand/structure] — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
  - selected for: highest-scoring direction with lexical evidence; lexical 0.11, structural 0.84
- **Data-entry grid (spreadsheet-like)** `comp-data-entry-grid` [component/data-display/structure] — Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.
  - react: AG Grid or Glide Data Grid for real spreadsheet behaviour; do not hand-roll.
  - selected for: highest-scoring component with lexical evidence; lexical 0.28, structural 0.6
- **Settings screen** `comp-settings-screen` [component/structure] — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).
  - selected for: highest-scoring component with lexical evidence; lexical 0.277, structural 0.52

### Guardrails (must hold)
- **Design empty, loading, error, and partial states** `layout-states-empty-loading-error` [states; heuristic] — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state.
  - selected for: required concern states: every screen ships empty/loading/error states
- **Focus visible and not obscured** `a11y-focus-visible` [accessibility/interaction; accessibility-requirement] — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
  - selected for: required concern interaction: input model: keyboard,pointer,touch
- **Actions only on hover** `anti-hover-only-actions` [anti-pattern; accessibility-requirement] — Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.
  - selected for: required concept interaction.hover_independence
- **Numeric tables: alignment, figures, units, precision** `data-tables-numeric` [content/data-display; heuristic] — Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator.
  - selected for: required concept table.tabular_figures

Omitted (redundant): comp-data-table (same category as a core pick or incompatible with one)
Filtered out: anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['web']); dir-service-app-mobile (platform ['mobile'] not in request ['web']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['web']); nav-bottom-tabs (platform ['mobile'] not in request ['web']); nav-tv-side (platform ['tv'] not in request ['web']); typography-system-native (platform ['desktop', 'mobile', 'tv'] not in request ['web'])
