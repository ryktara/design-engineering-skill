# Design direction: The appointments grid re-renders the whole day when one chip is dragged, so dragging stutters.

**KNOWN:** platform: web (project inspection); product: healthcare (project inspection (README)); product: ecommerce (project inspection (README)); stack: svelte (project inspection); stack: tailwind (project inspection); project_navigation: left-rail (repository: left-rail: 1 matches in +layout.svelte (shell/layout file); also breadcrumb-tree: 1 matches); project_components: tailwind (repository: tailwind)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (interaction defect on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 13 near-white, 1 near-black); project_spacing: 4 (repository: most used spacing values [4, 8, 12, 16]; tailwind spacing classes (4)); project_typography: custom (repository: font family theme (1 refs))
**Project context:** navigation=left-rail (KNOWN); theme=light-first (INFERRED); spacing=4 (INFERRED); typography=custom (INFERRED); components=tailwind (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'typography', 'color'] · changed ['density']

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'moderate' |
| layout | Dashboard grid of modules (`layout-dashboard-grid`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | changed | existing 4 (INFERRED) → density-high: allowed by change budget 'moderate' |
| surface | Elevated cards as the primary container (`surface-elevated-cards`) | new | no repository evidence for this slot |
| cards | Portrait poster cards (2:3) (`card-poster-portrait`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Functional thumbnails (`imagery-thumbnails`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers.
- **cards** — Fixed 2:3 ratio, title below the art (not over it) unless the art contains the title reliably, placeholder with title text, scale on focus with reserved margin. On TV about 6 per row at 960 dp width with 20 dp gutters.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries.
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.

## Guardrails (required concerns: accessibility, interaction, component; uncovered: none)
**interaction**
- Grids with row actions are one Tab stop: Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
- Hover reveals need a non-hover path: Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_
**platform**
- Web: content-driven breakpoints and a test matrix: Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
**anti / patterns**
- Trend aesthetics at the cost of usability: Run every aesthetic choice through contrast, target size, focus visibility, platform input model, and reading distance before keeping it. Brand character must come from choices that pass, not from breaking them. _(covers: structure before style decision order, high contrast)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "dashboard-grid",
  "grid_behavior": "responsive-columns",
  "content_density": "high",
  "surface_strategy": "elevated",
  "card_geometry": "poster-portrait",
  "corner_language": "small",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "single-primary",
  "image_strategy": "thumbnails",
  "icon_strategy": "outline",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Catalog grid (0.479), EPG / program guide grid (0.394), Single column, one task (0.376)
- density: Medium density (0.367), Low density / spacious (0.344)
- surface: Imagery-backed surfaces (0.289), Bordered panes (0.23), Flat surfaces with tonal layers (0.224)
- cards: No card containers (dividers and spacing) (0.367), Flat tiles (0.346)
- motion: Spring-based physical motion (0.307), Expressive brand motion (0.279), Crossfade and shared-element continuity (0.252)
- focus: Underline / weight focus for text-first UI (0.182)
- cta: Sticky action bar (0.331), Toolbar / command bar with selection-driven commands (0.261), Contextual inline actions (0.185)
- imagery: Illustration system (0.358), Data graphics as the visual layer (0.352), Poster art as primary recognition (0.347)
- icon: Duotone icons as brand accent (0.261), Custom glyph set (0.243), Text-only, no icon system (0.225)
- metadata: Rich metadata (operational) (0.348), Minimal metadata (0.222), Moderate metadata with a hierarchy (0.214)

## Rejected for incompatibility
- surface: surface-imagery-backed — incompatible with density-high
- surface: surface-glass — incompatible with layout-dashboard-grid,density-high
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cards: card-bordered — incompatible with surface-elevated-cards
- motion: motion-cinematic — incompatible with density-high,layout-dashboard-grid
- motion: motion-spring — incompatible with density-high
- motion: motion-expressive — incompatible with density-high
- motion: motion-crossfade — incompatible with density-high
- imagery: imagery-illustration — incompatible with density-high
- imagery: imagery-hero — incompatible with layout-dashboard-grid,density-high
- icon: icon-duotone — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
