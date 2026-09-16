## guidance: our React energy dashboard looks cramped and inconsistent, facility managers complain the numbers are hard to read and they don't know which button to press
status=CONFIDENT mode=['polish', 'audit'] platform=['web'] input=['keyboard', 'pointer', 'touch'] product=[] screen=['dashboard'] stack=['react'] density=None env=[] risk=low negatives=[]
MISSING: brand: no brand assets, guideline, or character description available
concerns required=['structure', 'anti-pattern', 'interaction', 'accessibility', 'data-display'] covered=1.0 uncovered=[] recommended=['content', 'component', 'adaptive', 'feedback'] bundle=7 (core 3 + guardrails 4) diversity=0.86 redundancy=0.4

### Core (what to build)
- **KPI / stat tile** `comp-kpi-tile` [data-display] — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default.
  - selected for: highest-scoring component with lexical evidence; lexical 0.181, structural 0.58
- **Analytical console** `dir-analytical-console` [brand/structure] — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
  - selected for: highest-scoring direction with lexical evidence; lexical 0.151, structural 0.4
- **Dashboard grid of modules** `layout-dashboard-grid` [structure] — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
  - selected for: highest-scoring pattern with lexical evidence; lexical 0.252, structural 0.48

### Guardrails (must hold)
- **Arbitrary spacing and misaligned edges** `anti-inconsistent-spacing` [anti-pattern; heuristic] — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change.
  - selected for: required concern anti-pattern: polish removes generic devices
- **Everything operable by keyboard, no traps** `a11y-keyboard-operable` [accessibility/interaction; accessibility-requirement] — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
  - selected for: required concern interaction: input model: keyboard,pointer,touch
- **One clear focal point per screen** `layout-hierarchy-one-thing` [structure; heuristic] — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title.
  - selected for: required concept layout.focal_hierarchy
- **Focus visible and not obscured** `a11y-focus-visible` [accessibility/interaction; accessibility-requirement] — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
  - selected for: required concept interaction.focus_visible

Omitted (redundant): comp-chart-container (same category as a core pick or incompatible with one)
Filtered out: comp-list-row-mobile (platform ['mobile', 'tablet'] not in request ['web']); comp-tv-sign-in (platform ['tv'] not in request ['web']); dir-broadcast-guide-tv (platform ['tv'] not in request ['web']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['web']); nav-bottom-tabs (platform ['mobile'] not in request ['web']); layout-rails (platform ['tv'] not in request ['web'])
