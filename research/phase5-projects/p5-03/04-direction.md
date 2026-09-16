# Design direction: Checkout on phones: the order summary pushes the pay button below the fold.

**KNOWN:** platform: mobile (request: phones); product: ecommerce (request: checkout); stack: html-css (project inspection); screen: checkout (request: checkout); mode: responsive (explicit: on phones); project_navigation: top-bar (repository: top-bar: 4 matches in checkout.html, index.html, product.html (shell/layout file))
**INFERRED:** input: touch (implied by platform mobile); mode: audit (layout/structure defect on existing UI); mode: refactor (structural fix follows); project_theme: light-first (repository: hex palette: 6 near-white, 2 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: pill (repository: most common radius 999 (5×); others [5.0, 4.0]); project_typography: geometric-sans (repository: font family Inter (1 refs); weights 600, 500, 400)
**CONFLICTS:** platform: request ['mobile'] vs project web → request kept; repository platform recorded as context
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=elevated (INFERRED); radius=pill (INFERRED); typography=geometric-sans (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'typography', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Single column, one task (`layout-single-column`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: geometric-sans (INFERRED) (`typography-geometric-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Spring-based physical motion (`motion-spring`) | new | no repository evidence for this slot |
| focus | Touch-only focus handling (mobile) (`focus-none-touch-only`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Functional thumbnails (`imagery-thumbnails`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Content width capped for reading (~60–75 characters per line), vertical rhythm from the spacing scale, primary action reachable without scrolling on the shortest supported viewport, or sticky at the bottom.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Use the platform spring APIs (SwiftUI .spring, Compose spring(), Motion/Framer spring on web) with one or two named presets (snappy, gentle); interruptible and gesture-tracking; never chain springs on page load.
- **focus** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries.
- **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.

## Guardrails (required concerns: adaptive, structure, interaction, accessibility, feedback; uncovered: none)
**interaction**
- Target size by platform: Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
**platform**
- Mobile: safe areas and system insets: Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view. _(covers: safe areas and notches)_
- Mobile: follow the platform navigation grammar: iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "layout_topology": "single-column",
  "grid_behavior": "fluid",
  "content_density": "medium",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "geometric-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "spring",
  "focus_strategy": "none-touch-only",
  "cta_strategy": "single-primary",
  "image_strategy": "thumbnails",
  "icon_strategy": "filled",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Form stack with sections (0.258), Catalog grid (0.258), Vertical feed (0.122)
- density: Low density / spacious (0.213)
- cards: Portrait poster cards (2:3) (0.37), List rows (0.266)
- motion: Expressive brand motion (0.28), Crossfade and shared-element continuity (0.255), Functional minimal motion (0.242)
- cta: Sticky action bar (0.362), Floating action button (Material) (0.244), Contextual inline actions (0.085)
- imagery: Poster art as primary recognition (0.396), Hero imagery on landing/brand pages (0.273), No decorative imagery (0.169)
- icon: Platform icon set (0.276), Duotone icons as brand accent (0.243), Custom glyph set (0.169)
- metadata: Moderate metadata with a hierarchy (0.232), Minimal metadata (0.149)

## Rejected for incompatibility
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
