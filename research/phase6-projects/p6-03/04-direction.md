# Design direction: On the product listing, shoppers cannot narrow 120 products down to what fits them.

**KNOWN:** platform: web (project inspection); product: ecommerce (request: product listing); stack: html-css (project inspection); screen: list (request: listing); project_navigation: top-bar (repository: top-bar: 4 matches in checkout.html, index.html, product.html (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: responsive (responsive defect); mode: audit (diagnose first); project_theme: light-first (repository: hex palette: 6 near-white, 2 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: pill (repository: most common radius 999 (5×); others [5.0, 4.0]); project_typography: geometric-sans (repository: font family Inter (1 refs); weights 600, 500, 400)
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=elevated (INFERRED); radius=pill (INFERRED); typography=geometric-sans (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | *(no compatible option; decide from references)* | unfilled | |
| typography | Preserve existing typography: geometric-sans (INFERRED) (`typography-geometric-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **typography** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Catalog grid** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift.

## Guardrails (required concerns: adaptive, structure, interaction, accessibility, data-display; uncovered: adaptive, interaction, accessibility, data-display)

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "surface_strategy": "elevated",
  "card_geometry": "elevated",
  "corner_language": "medium",
  "typography_character": "geometric-sans",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cards: card-poster-landscape — media-specific pattern (education,media) with no media signal in the request or repository
- cards: card-poster-portrait — media-specific pattern (education,media) with no media signal in the request or repository

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
