# Design direction: Add a Spanish language switch to the pick-up flow.

**KNOWN:** platform: web (project inspection); product: healthcare (project inspection (README)); product: government (project inspection (README)); stack: html-css (project inspection); project_navigation: hub-spoke (repository: hub-spoke: 27 matches in README.md, app.js, i18n.js (shell/layout file)); project_typography: humanist-sans (repository: font family Nunito (2 refs); weights 700, 800, 600, 500)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: create (build/create request on an existing surface); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: medium (repository: most common radius 12 (1×); others [20.0, 32.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=hub-spoke (KNOWN); surfaces=elevated (INFERRED); radius=medium (INFERRED); typography=humanist-sans (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'typography'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: hub-spoke (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Master–detail (list + detail pane) (`layout-master-detail`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Neutral canvas + one accent (`color-neutral-accent`) | new | no repository evidence for this slot |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.

## Guardrails (required concerns: structure, states, interaction, accessibility; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**platform**
- Web: content-driven breakpoints and a test matrix: Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
**states**
- Saving, saved, autosave, session expiry, and permission-denied states: Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry on a personal device (restore the draft after re-authentication; on shared or public screens clear it instead); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default. _(covers: saving, saved and conflict states, session expiry and idle reset, confirmation of destructive or high-risk actions)_
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "layout_topology": "master-detail",
  "grid_behavior": "fixed",
  "content_density": "high",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Dashboard grid of modules (0.374), Single column, one task (0.294), Catalog grid (0.258)
- density: Medium density (0.25), Low density / spacious (0.231)
- cards: No card containers (dividers and spacing) (0.25), Bordered cards (0.238), Flat tiles (0.23)
- color: Multicolour by category (0.263), Dark canvas + accent (dark-first) (0.221)
- motion: Spring-based physical motion (0.238), Expressive brand motion (0.208), Cinematic reveals (brand moments only) (0.181)
- focus: Underline / weight focus for text-first UI (0.218)
- cta: One primary action per screen (0.27), Toolbar / command bar with selection-driven commands (0.258), Contextual inline actions (0.211)
- imagery: No decorative imagery (0.313), Immersive backdrop (0.228)
- icon: Custom glyph set (0.233), Duotone icons as brand accent (0.171), Text-only, no icon system (0.171)
- metadata: Moderate metadata with a hierarchy (0.25), Inline badges and status chips (0.211), Minimal metadata (0.167)

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- color: color-dominant-brand — incompatible with density-high
- color: color-duotone — product-specific (media,marketing,education,social) does not fit request product ['government', 'healthcare']; alternative within 25%
- motion: motion-spring — incompatible with density-high
- motion: motion-expressive — incompatible with density-high
- motion: motion-cinematic — incompatible with density-high
- motion: motion-crossfade — incompatible with density-high
- imagery: imagery-illustration — incompatible with density-high
- imagery: imagery-immersive-backdrop — incompatible with density-high
- imagery: imagery-hero — incompatible with density-high
- icon: icon-duotone — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
