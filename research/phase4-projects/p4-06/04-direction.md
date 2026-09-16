# Design direction: add a product listing page with filters to our outdoor gear web store, matching the existing product and checkout pages

**KNOWN:** platform: web (request: web); product: ecommerce (request: product listing, checkout, web store); stack: html-css (project inspection); screen: list (request: listing); screen: checkout (request: checkout); project_navigation: top-bar (repository: top-bar: 3 matches in checkout.html, index.html, product.html (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: create (default (no mode cue)); project_theme: light-first (repository: hex palette: 6 near-white, 2 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: pill (repository: most common radius 50 (3×); others [999.0, 4.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=elevated (INFERRED); radius=pill (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Catalog grid (`layout-grid-catalog`) | new | no repository evidence for this slot |
| density | Low density / spacious (`density-low`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Humanist sans for approachable products (`typography-humanist-sans`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Crossfade and shared-element continuity (`motion-crossfade`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | Hero imagery on landing/brand pages (`imagery-hero`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift.
- **density** — Whitespace must come from a scale (e.g. 24/40/64/96), not arbitrary padding; keep line length in measure; big type is only justified for the one thing that should be read first. Spacious does not mean everything is huge.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Shared element for one anchor (the image) plus a crossfade for the rest; 250–350 ms; reduced-motion swaps to an instant crossfade. Use platform APIs (View Transitions API, SharedTransitionLayout, matchedGeometryEffect) not manual clones.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — The hero is a thesis about the product: show the actual thing (product, interface, outcome). Reserve aspect box to avoid CLS, serve responsive sources, LCP image preloaded, text contrast guaranteed by placement or scrim, and no autoplay video without a static poster and reduced-motion respect.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL.
- **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries.
- **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, feedback, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**accessibility**
- Search and filters: visible state and instant feedback: Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "layout_topology": "grid-catalog",
  "grid_behavior": "responsive-columns",
  "content_density": "low",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "crossfade",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "hero-imagery",
  "icon_strategy": "outline",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Table-first working screen (0.471), Single column, one task (0.348), Master–detail (list + detail pane) (0.312)
- density: High density (0.276), Medium density (0.268)
- cards: List rows (0.302), No card containers (dividers and spacing) (0.268), Flat tiles (0.248)
- typography: Monospace as identity for technical products (0.392), Grotesk display + quiet body (0.345), Condensed display for broadcast/media (0.335)
- motion: Spring-based physical motion (0.382), Cinematic reveals (brand moments only) (0.365), Expressive brand motion (0.352)
- focus: Underline / weight focus for text-first UI (0.236)
- cta: One primary action per screen (0.372), Toolbar / command bar with selection-driven commands (0.312), Contextual inline actions (0.265)
- imagery: Poster art as primary recognition (0.378), Functional thumbnails (0.37), Data graphics as the visual layer (0.273)
- icon: Duotone icons as brand accent (0.315), Text-only, no icon system (0.315), Custom glyph set (0.169)
- metadata: Rich metadata (operational) (0.276), Moderate metadata with a hierarchy (0.268), Minimal metadata (0.185)

## Rejected for incompatibility
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- typography: typography-monospace-technical — incompatible with density-low
- typography: typography-condensed-display — incompatible with density-low
- metadata: metadata-rich — incompatible with density-low,density-low

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
