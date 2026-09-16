# Design direction: Make the Add Habit sheet work when the keyboard is up.

**KNOWN:** platform: mobile (project inspection); input: keyboard (request: keyboard); product: ecommerce (project inspection (README)); stack: swiftui (project inspection); mode: create (build/create request); project_navigation: bottom-tabs (repository: bottom-tabs: 7 matches in README.md, RootTabView.swift, StreaksApp.swift (shell/layout file))
**INFERRED:** input: touch (implied by platform mobile); project_theme: dual-theme (repository: dark theme configuration signals: 2; hex palette: 0 near-white, 0 near-black); project_surfaces: elevated (repository: shadow/elevation in 4 files, borders in 0); project_radius: medium (repository: most common radius 8 (1×); others []); project_spacing: 4 (repository: most used spacing values [2, 4, 12, 16]); project_typography: humanist-sans (repository: font family Nunito (1 refs); encoded type scale in 3 files)
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=bottom-tabs (KNOWN); theme=dual-theme (INFERRED); surfaces=elevated (INFERRED); radius=medium (INFERRED); spacing=4 (INFERRED); typography=humanist-sans (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'typography', 'color'] · changed ['density']

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: bottom-tabs (KNOWN) (`nav-bottom-tabs`) | preserved | repository evidence with change budget 'moderate' |
| layout | Catalog grid (`layout-grid-catalog`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | changed | existing 4 (INFERRED) → density-medium: allowed by change budget 'moderate' |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (INFERRED) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (dual theme) (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Spring-based physical motion (`motion-spring`) | new | no repository evidence for this slot |
| focus | Touch-only focus handling (mobile) (`focus-none-touch-only`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | Functional thumbnails (`imagery-thumbnails`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination. (Existing system: do not replace it for this task.)
- **layout** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Use the platform spring APIs (SwiftUI .spring, Compose spring(), Motion/Framer spring on web) with one or two named presets (snappy, gentle); interruptible and gesture-tracking; never chain springs on page load.
- **focus** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Product detail page (PDP)** — Above the fold on every viewport: product name, price (with tabular figures and any discount stated in words), primary image, variant selectors and one add-to-cart action; variant choice is a radio group with visible labels and a disabled-but-visible state for out-of-stock options; the add-to-cart button is sticky on phones without covering focused controls; shipping, returns and stock are stated next to the price, not in a tab; the gallery has fixed aspect boxes (no layout shift), keyboard-operable thumbnails and alt text per image; reviews show the distribution and a count, and stars always have a text value; secondary actions (wishlist, share, size guide) never compete visually with add-to-cart; the size guide opens as a dialog that returns focus.
- **Drawer / side panel** — Inline (pushes content) on wide screens, overlay on narrow; width from tokens (320–480 px); heading + close; focus moves in on open and returns on close; content scrolls independently; TV: side sheet that keeps the player/content visible and traps DPAD inside until BACK.
- **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action.

## Guardrails (required concerns: component, structure, interaction, accessibility; uncovered: none)
**interaction**
- Dialog focus management: On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. _(covers: dialog focus management, focus restoration)_
- Non-text contrast 3:1 for controls and focus: Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
**platform**
- Mobile: follow the platform navigation grammar: iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

## Fingerprint
```json
{
  "navigation_model": "bottom-tabs",
  "layout_topology": "grid-catalog",
  "grid_behavior": "responsive-columns",
  "content_density": "medium",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "spring",
  "focus_strategy": "none-touch-only",
  "cta_strategy": "sticky-bar",
  "image_strategy": "thumbnails",
  "icon_strategy": "filled",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Single column, one task (0.294), Vertical feed (0.248)
- density: Low density / spacious (0.231)
- cards: No card containers (dividers and spacing) (0.437), Flat tiles (0.23)
- motion: Expressive brand motion (0.334), Crossfade and shared-element continuity (0.273), Functional minimal motion (0.26)
- cta: One primary action per screen (0.27), Floating action button (Material) (0.25), Contextual inline actions (0.211)
- imagery: Poster art as primary recognition (0.347), Hero imagery on landing/brand pages (0.327), Illustration system (0.191)
- icon: Duotone icons as brand accent (0.297), Platform icon set (0.294), Custom glyph set (0.151)
- metadata: Moderate metadata with a hierarchy (0.25), Minimal metadata (0.167)

## Rejected for incompatibility
- layout: layout-split-player — product-specific (media) does not fit request product ['ecommerce']; alternative within 25%
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
