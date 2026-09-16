# Design direction: Patient search that finds nothing just shows a blank area.

**KNOWN:** platform: web (project inspection); product: healthcare (request: patient); product: ecommerce (project inspection (README)); stack: svelte (project inspection); stack: tailwind (project inspection); screen: search (request: search); project_navigation: left-rail (repository: left-rail: 1 matches in +layout.svelte (shell/layout file); also breadcrumb-tree: 1 matches); project_components: tailwind (repository: tailwind)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (navigation defect on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 13 near-white, 1 near-black); project_spacing: 4 (repository: most used spacing values [4, 8, 12, 16]; tailwind spacing classes (4)); project_typography: custom (repository: font family theme (1 refs))
**Project context:** navigation=left-rail (KNOWN); theme=light-first (INFERRED); spacing=4 (INFERRED); typography=custom (INFERRED); components=tailwind (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'typography', 'color'] · changed ['density']

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'moderate' |
| layout | Master–detail (list + detail pane) (`layout-master-detail`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | changed | existing 4 (INFERRED) → density-high: allowed by change budget 'moderate' |
| surface | Elevated cards as the primary container (`surface-elevated-cards`) | new | no repository evidence for this slot |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | Poster art as primary recognition (`imagery-poster`) | new | no repository evidence for this slot |
| icon | Text-only, no icon system (`icon-text-only`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers.
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — One aspect ratio per rail (2:3 portrait or 16:9 landscape), title text below or revealed on focus (never over the art without a scrim), placeholders with the title text for missing art, images sized to the rendered card (no 4K posters in 200 px cards), progressive loading with a low-res or colour placeholder.
- **icon** — Words for everything except universally understood glyphs (search, close, menu on narrow widths); use weight and case for hierarchy; this is a deliberate stance and must be applied consistently.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK.
- **Clinical workstation** — Patient banner always visible (identity, allergies, alerts) as the focal element, master-detail for patient lists and records, strict status colour language with text and icons (never colour alone), large legible numerics with units, quiet neutral surfaces, confirmation for critical actions with the safe default, interruption-safe autosave. Identity via the banner treatment and status language; restraint is the brand.

## Guardrails (required concerns: accessibility, interaction, component; uncovered: none)
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
  "navigation_model": "left-rail",
  "layout_topology": "master-detail",
  "grid_behavior": "fixed",
  "content_density": "high",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "poster-art",
  "icon_strategy": "text-only",
  "metadata_density": "rich"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Catalog grid (0.402), Dashboard grid of modules (0.248), Player with overlay controls (0.181)
- density: Medium density (0.232), Low density / spacious (0.213)
- surface: Translucent (glass) layers, justified (0.291), Imagery-backed surfaces (0.283), Flat surfaces with tonal layers (0.242)
- cards: No card containers (dividers and spacing) (0.232), Bordered cards (0.22), Flat tiles (0.212)
- motion: Expressive brand motion (0.28), Crossfade and shared-element continuity (0.255)
- cta: One primary action per screen (0.18), Toolbar / command bar with selection-driven commands (0.132), Contextual inline actions (0.085)
- imagery: Hero imagery on landing/brand pages (0.381), Data graphics as the visual layer (0.31), No decorative imagery (0.295)
- icon: Outline icon set, one weight (0.286), Duotone icons as brand accent (0.243), Custom glyph set (0.169)
- metadata: Inline badges and status chips (0.319), Moderate metadata with a hierarchy (0.232), Minimal metadata (0.149)

## Rejected for incompatibility
- surface: surface-glass — incompatible with density-high
- surface: surface-imagery-backed — incompatible with density-high
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- cards: card-bordered — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- motion: motion-spring — incompatible with density-high
- motion: motion-expressive — incompatible with density-high
- motion: motion-crossfade — incompatible with density-high
- motion: motion-cinematic — incompatible with density-high
- focus: focus-underline — product-specific (content,marketing) does not fit request product ['ecommerce', 'healthcare']; alternative within 25%
- imagery: imagery-hero — incompatible with density-high
- imagery: imagery-illustration — incompatible with density-high
- icon: icon-duotone — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
