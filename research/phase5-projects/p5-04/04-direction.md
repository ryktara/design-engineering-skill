# Design direction: The product page never tells shoppers when it will arrive or that returns are free.

**KNOWN:** platform: web (project inspection); product: ecommerce (request: product page); stack: html-css (project inspection); screen: detail (request: product page); project_navigation: top-bar (repository: top-bar: 4 matches in checkout.html, index.html, product.html (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 6 near-white, 2 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: pill (repository: most common radius 999 (5×); others [5.0, 4.0]); project_typography: geometric-sans (repository: font family Inter (1 refs); weights 600, 500, 400)
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=elevated (INFERRED); radius=pill (INFERRED); typography=geometric-sans (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'typography', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Catalog grid (`layout-grid-catalog`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: geometric-sans (INFERRED) (`typography-geometric-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Crossfade and shared-element continuity (`motion-crossfade`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Functional thumbnails (`imagery-thumbnails`) | new | no repository evidence for this slot |
| icon | Text-only, no icon system (`icon-text-only`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Shared element for one anchor (the image) plus a crossfade for the rest; 250–350 ms; reduced-motion swaps to an instant crossfade. Use platform APIs (View Transitions API, SharedTransitionLayout, matchedGeometryEffect) not manual clones.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.
- **icon** — Words for everything except universally understood glyphs (search, close, menu on narrow widths); use weight and case for hierarchy; this is a deliberate stance and must be applied consistently.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Product detail page (PDP)** — Above the fold on every viewport: product name, price (with tabular figures and any discount stated in words), primary image, variant selectors and one add-to-cart action; variant choice is a radio group with visible labels and a disabled-but-visible state for out-of-stock options; the add-to-cart button is sticky on phones without covering focused controls; shipping, returns and stock are stated next to the price, not in a tab; the gallery has fixed aspect boxes (no layout shift), keyboard-operable thumbnails and alt text per image; reviews show the distribution and a count, and stars always have a text value; secondary actions (wishlist, share, size guide) never compete visually with add-to-cart; the size guide opens as a dialog that returns focus.
- **Functional thumbnails** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.

## Guardrails (required concerns: accessibility, interaction, component; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**platform**
- Web: content-driven breakpoints and a test matrix: Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "layout_topology": "grid-catalog",
  "grid_behavior": "responsive-columns",
  "content_density": "medium",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "geometric-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "crossfade",
  "focus_strategy": "ring",
  "cta_strategy": "single-primary",
  "image_strategy": "thumbnails",
  "icon_strategy": "text-only",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Single column, one task (0.312), Master–detail (list + detail pane) (0.276), Editorial columns (0.266)
- density: High density (0.24)
- cards: List rows (0.384), No card containers (dividers and spacing) (0.338), Flat tiles (0.212)
- motion: Spring-based physical motion (0.361), Expressive brand motion (0.335), Functional minimal motion (0.242)
- focus: Underline / weight focus for text-first UI (0.374)
- cta: Contextual inline actions (0.393), Sticky action bar (0.362)
- imagery: Hero imagery on landing/brand pages (0.44), Poster art as primary recognition (0.426), Data graphics as the visual layer (0.333)
- icon: Outline icon set, one weight (0.384), Duotone icons as brand accent (0.243), Custom glyph set (0.169)
- metadata: Rich metadata (operational) (0.24), Moderate metadata with a hierarchy (0.232), Minimal metadata (0.149)

## Rejected for incompatibility
- density: density-low — product-specific (marketing,content,media,education) does not fit request product ['ecommerce']; alternative within 25%
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cta: cta-toolbar-commands — product-specific (erp,devtools,finance,saas) does not fit request product ['ecommerce']; alternative within 25%

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
