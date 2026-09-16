# Design direction: facility managers don't notice new alerts; make exceptions the first thing they see on the dashboard without redesigning it

**KNOWN:** platform: web (project inspection); product: iot (request: facility managers); stack: react (project inspection); screen: dashboard (request: dashboard); job: monitor (request: alert, alerts, exceptions); project_navigation: top-bar (repository: top-bar: 5 matches in App.jsx, styles.css (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 12 near-white, 1 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 6 (1×); others [999.0]); project_spacing: 4 (repository: most used spacing values [4, 8, 12, 16, 20]; tailwind spacing classes (5))
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED)
**Change budget:** low · preserved ['navigation', 'density', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'low' |
| layout | Dashboard grid of modules (`layout-dashboard-grid`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | Flat tiles (`card-flat-tile`) | new | no repository evidence for this slot |
| typography | Geometric sans for product/tech brands (`typography-geometric-sans`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Contextual inline actions (`cta-contextual-inline`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- **typography** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Actions are visible (not hover-only), consistently placed per item type, and grouped: at most one emphasised per item. Hover-reveal is allowed only as an addition to a visible affordance and never on touch/TV.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Core guidance (components / layouts to build)
- **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default.
- **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV.
- **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "layout_topology": "dashboard-grid",
  "grid_behavior": "responsive-columns",
  "surface_strategy": "bordered",
  "card_geometry": "flat-tile",
  "corner_language": "small",
  "typography_character": "geometric-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "contextual-inline",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "moderate"
}
```

## Validation: OK

## Alternatives considered
- layout: Table-first working screen (0.339), Single column, one task (0.254), Three-pane workbench (0.144)
- cards: Bordered cards (0.356), List rows (0.266), No card containers (dividers and spacing) (0.232)
- typography: Neutral workhorse sans (0.159), Monospace as identity for technical products (0.154)
- motion: Spring-based physical motion (0.184), Expressive brand motion (0.154), Crossfade and shared-element continuity (0.129)
- focus: Underline / weight focus for text-first UI (0.353)
- cta: Toolbar / command bar with selection-driven commands (0.276), One primary action per screen (0.18), Sticky action bar (0.092)
- imagery: Poster art as primary recognition (0.262), Immersive backdrop (0.174)
- icon: Duotone icons as brand accent (0.117), Text-only, no icon system (0.117), Custom glyph set (0.043)
- metadata: Inline badges and status chips (0.193), Minimal metadata (0.149)

## Rejected for incompatibility
- typography: typography-rounded-friendly — incompatible with surface-bordered-panes
- motion: motion-expressive — incompatible with surface-bordered-panes
- motion: motion-cinematic — incompatible with layout-dashboard-grid
- imagery: imagery-hero — incompatible with layout-dashboard-grid
- imagery: imagery-poster — incompatible with surface-bordered-panes
- imagery: imagery-immersive-backdrop — incompatible with surface-bordered-panes
- metadata: metadata-rich — product-specific (erp,finance,devtools,saas,healthcare) does not fit request product ['iot']; alternative within 25%

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
