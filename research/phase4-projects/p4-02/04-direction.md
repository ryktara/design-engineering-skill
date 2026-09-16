# Design direction: accessibility review and fix of the seat management table: keyboard users can't reach row actions and the status column is colour only

**KNOWN:** platform: web (project inspection); input: keyboard (request: keyboard); product: finance (project inspection (README)); product: saas (project inspection (README)); stack: nextjs (project inspection); stack: react (project inspection); stack: tailwind (project inspection); stack: shadcn (project inspection); mode: accessibility (explicit: accessibility; problem statement about assistive tech / accessibility); project_navigation: left-rail (repository: left-rail: 1 matches in app-shell.tsx (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 1; root/canvas backgrounds: 1 light, 0 dark); project_components: tailwind, radix, shadcn-style cva, table:tanstack, shadcn (repository: tailwind; radix)
**INFERRED:** input: pointer (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: audit (diagnose the reported defect); project_radius: small (repository: most common radius 0.5 (1×); others []); project_spacing: 8 (repository: most used spacing values [16, 8, 4, 12, 24]; tailwind spacing classes (93)); project_typography: custom (repository: font family globals (1 refs); monospace usage)
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (KNOWN); radius=small (INFERRED); spacing=8 (INFERRED); typography=custom (INFERRED); components=tailwind, radix, shadcn-style cva, table:tanstack, shadcn (KNOWN)
**Change budget:** low · preserved ['navigation', 'density', 'typography', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'low' |
| layout | Table-first working screen (`layout-table-first`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 8 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Bordered panes (`surface-bordered-panes`) | new | no repository evidence for this slot |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Grids with row actions are one Tab stop: Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions)_
**accessibility**
- Semantic structure: headings, landmarks, lists, tables: Structure first, style second: choose the element for its meaning and restyle it. Data tables use <th scope>; layout tables are forbidden; visually hidden headings are fine for screen readers when the visual design omits them. _(covers: semantic structure and roles)_
- Text contrast 4.5:1 (3:1 large): Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- Accessible names for every control and image: Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
**anti / patterns**
- Actions only on hover: Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV. _(covers: no hover dependence)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "table-first",
  "grid_behavior": "virtualized",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
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
- layout: Master–detail (list + detail pane) (0.391), Dashboard grid of modules (0.377), Three-pane workbench (0.362)
- surface: Imagery-backed surfaces (0.311), Flat surfaces with tonal layers (0.188), Translucent (glass) layers, justified (0.171)
- cards: Bordered cards (0.375), No card containers (dividers and spacing) (0.194), Landscape media cards (16:9) (0.166)
- motion: Cinematic reveals (brand moments only) (0.22), Spring-based physical motion (0.166), Expressive brand motion (0.136)
- focus: Underline / weight focus for text-first UI (0.218)
- cta: Contextual inline actions (0.4), One primary action per screen (0.356), Sticky action bar (0.31)
- imagery: No decorative imagery (0.452), Functional thumbnails (0.221), Illustration system (0.209)
- icon: Text-only, no icon system (0.271), Duotone icons as brand accent (0.063), Custom glyph set (0.025)
- metadata: Inline badges and status chips (0.52), Moderate metadata with a hierarchy (0.2), Minimal metadata (0.101)

## Rejected for incompatibility
- layout: layout-editorial — incompatible with nav-left-rail
- surface: surface-imagery-backed — incompatible with layout-table-first
- surface: surface-glass — incompatible with layout-table-first
- surface: surface-elevated-cards — incompatible with layout-table-first
- cards: card-poster-landscape — incompatible with layout-table-first
- cards: card-poster-portrait — incompatible with layout-table-first
- motion: motion-cinematic — incompatible with layout-table-first
- motion: motion-expressive — incompatible with surface-bordered-panes
- motion: motion-crossfade — incompatible with layout-table-first
- focus: focus-underline — incompatible with layout-table-first
- imagery: imagery-illustration — incompatible with layout-table-first
- imagery: imagery-poster — incompatible with layout-table-first,surface-bordered-panes
- imagery: imagery-immersive-backdrop — incompatible with surface-bordered-panes,layout-table-first
- metadata: metadata-minimal — incompatible with layout-table-first

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
