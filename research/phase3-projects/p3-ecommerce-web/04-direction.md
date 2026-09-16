# Design direction: Design the product detail page and checkout for our outdoor gear web store; must convert well on phones

**KNOWN:** platform: web (request: web); platform: mobile (request: phone); product: ecommerce (request: store, checkout); screen: detail (request: detail page, detail); screen: checkout (request: checkout); mode: create (request: design the); environment: outdoor (request: outdoor)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web)
**MISSING:** brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence

| Slot | Choice | Why |
|---|---|---|
| navigation | Linear wizard / stepper (`nav-wizard`) | mode create, product ecommerce, screen checkout |
| layout | Master–detail (list + detail pane) (`layout-master-detail`) | platform web, input keyboard,pointer,touch, mode create, product mismatch, screen detail |
| density | Low density / spacious (`density-low`) | platform mobile,web, mode create, product mismatch |
| surface | Elevated cards as the primary container (`surface-elevated-cards`) | platform mobile,web, input pointer,touch, mode create, product ecommerce |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | platform mobile,web, mode create, product mismatch |
| typography | Humanist sans for approachable products (`typography-humanist-sans`) | mode create, product ecommerce |
| color | Monochrome with typographic hierarchy (`color-monochrome-light`) | platform mobile,web, mode create, product ecommerce |
| motion | Crossfade and shared-element continuity (`motion-crossfade`) | mode create, product ecommerce |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | platform web, input keyboard,pointer, mode create |
| cta | Sticky action bar (`cta-sticky-bar`) | platform mobile,web, input pointer,touch, mode create, product ecommerce, screen checkout,detail |
| imagery | Hero imagery on landing/brand pages (`imagery-hero`) | platform mobile,web, mode create, product ecommerce |
| icon | Filled icons for distance and touch (`icon-filled-system`) | platform mobile, input touch, mode create |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | platform mobile,web, mode create, product ecommerce |

## Guidance per slot
- **navigation** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action.
- **layout** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- **density** — Whitespace must come from a scale (e.g. 24/40/64/96), not arbitrary padding; keep line length in measure; big type is only justified for the one thing that should be read first. Spacious does not mean everything is huge.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers.
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it.
- **color** — Neutral scale only, with one reserved chromatic colour for errors and links if needed; interactive states via weight, underline, and tone; imagery provides the colour. Focus indication must be a visible ring or underline since colour is unavailable.
- **motion** — Shared element for one anchor (the image) plus a crossfade for the rest; 250–350 ms; reduced-motion swaps to an instant crossfade. Use platform APIs (View Transitions API, SharedTransitionLayout, matchedGeometryEffect) not manual clones.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — The hero is a thesis about the product: show the actual thing (product, interface, outcome). Reserve aspect box to avoid CLS, serve responsive sources, LCP image preloaded, text contrast guaranteed by placement or scrim, and no autoplay video without a static poster and reduced-motion respect.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action.
- **Product marketing site** — Structure derived from the buyer's questions (what is it, does it work for me, proof, price), a hero that shows the real product, one display face with character, one accent, one orchestrated motion moment, everything else quiet; no icon-feature grids, no gradient blobs, no testimonial carousel by default. Identity via the hero concept and type; run the anti-template check.
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, feedback, environment; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state.
**privacy / environment**
- Field use: sunlight readability and glanceable status: Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding).

## Fingerprint
```json
{
  "navigation_model": "wizard",
  "layout_topology": "master-detail",
  "grid_behavior": "fixed",
  "content_density": "low",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "monochrome",
  "motion_character": "crossfade",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "hero-imagery",
  "icon_strategy": "filled",
  "metadata_density": "inline-badges"
}
```

## Validation: OK

## Alternatives considered
- navigation: Top bar navigation (0.44), Bottom tab bar (0.359), Persistent left rail / sidebar (0.296)
- layout: Catalog grid (0.398), Single column, one task (0.348), Three-pane workbench (0.306)
- density: High density (0.319), Medium density (0.268)
- surface: Imagery-backed surfaces (0.355), Translucent (glass) layers, justified (0.322), Flat surfaces with tonal layers (0.278)
- cards: No card containers (dividers and spacing) (0.268), Bordered cards (0.256), Flat tiles (0.248)
- typography: Condensed display for broadcast/media (0.425), Monospace as identity for technical products (0.409), Grotesk display + quiet body (0.345)
- color: Neutral canvas + one accent (0.388), Dominant brand colour (0.345), Dark canvas + accent (dark-first) (0.33)
- motion: Spring-based physical motion (0.382), Expressive brand motion (0.352), Functional minimal motion (0.278)
- focus: Touch-only focus handling (mobile) (0.339), Underline / weight focus for text-first UI (0.236)
- cta: One primary action per screen (0.38), Toolbar / command bar with selection-driven commands (0.312), Contextual inline actions (0.265)
- imagery: Functional thumbnails (0.448), Poster art as primary recognition (0.395), Immersive backdrop (0.323)
- icon: Text-only, no icon system (0.403), Duotone icons as brand accent (0.4), Outline icon set, one weight (0.322)
- metadata: Moderate metadata with a hierarchy (0.377), Rich metadata (operational) (0.298), Minimal metadata (0.208)

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
