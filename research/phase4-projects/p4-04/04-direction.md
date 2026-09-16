# Design direction: add a compare-to-last-week view to the energy dashboard KPIs and the hourly chart, keeping the existing top bar and light theme

**KNOWN:** platform: web (project inspection); product: finance (request: kpi); product: iot (request: energy); stack: react (project inspection); screen: dashboard (request: dashboard); job: compare (request: compare); project_navigation: top-bar (repository: top-bar: 5 matches in App.jsx, styles.css (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: create (default (no mode cue)); project_theme: light-first (repository: hex palette: 12 near-white, 1 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 6 (1×); others [999.0]); project_spacing: 4 (repository: most used spacing values [4, 8, 12, 16, 20]; tailwind spacing classes (5))
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Dashboard grid of modules (`layout-dashboard-grid`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | new | density high (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV.
- **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**anti / patterns**
- The default SaaS dashboard (sidebar + 4 KPI cards + chart + table): Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "layout_topology": "dashboard-grid",
  "grid_behavior": "responsive-columns",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "typography_character": "neutral-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- layout: Table-first working screen (0.495), Master–detail (list + detail pane) (0.35), Three-pane workbench (0.3)
- cards: Landscape media cards (16:9) (0.372), List rows (0.302), No card containers (dividers and spacing) (0.268)
- typography: Rounded friendly sans (0.352), Serif editorial text (0.299), Geometric sans for product/tech brands (0.291)
- motion: Crossfade and shared-element continuity (0.262), Spring-based physical motion (0.256), Expressive brand motion (0.226)
- focus: Underline / weight focus for text-first UI (0.2)
- cta: Sticky action bar (0.485), Contextual inline actions (0.265), One primary action per screen (0.189)
- imagery: No decorative imagery (0.393), Poster art as primary recognition (0.239), Immersive backdrop (0.231)
- icon: Duotone icons as brand accent (0.153), Text-only, no icon system (0.153), Custom glyph set (0.043)
- metadata: Inline badges and status chips (0.355), Moderate metadata with a hierarchy (0.268), Minimal metadata (0.149)

## Rejected for incompatibility
- typography: typography-rounded-friendly — incompatible with density-high,surface-bordered-panes
- typography: typography-serif-editorial — incompatible with density-high
- typography: typography-geometric-sans — incompatible with density-high
- motion: motion-crossfade — incompatible with density-high
- motion: motion-spring — incompatible with density-high
- motion: motion-expressive — incompatible with density-high,surface-bordered-panes
- motion: motion-cinematic — incompatible with density-high,layout-dashboard-grid
- imagery: imagery-poster — incompatible with surface-bordered-panes
- imagery: imagery-immersive-backdrop — incompatible with surface-bordered-panes,density-high
- imagery: imagery-hero — incompatible with layout-dashboard-grid,density-high
- icon: icon-duotone — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
