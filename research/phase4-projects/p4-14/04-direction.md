# Design direction: add a settings screen (sync frequency, units, high-contrast mode) to the field inspection app in its existing style

**KNOWN:** platform: mobile (project inspection); platform: tv (project inspection); input: remote (project inspection: DPAD/remote handling in source); product: erp (project inspection (README)); product: iot (project inspection (README)); stack: flutter (project inspection); screen: settings (request: settings); project_navigation: top-bar (repository: top-bar: 2 matches in checklist_screen.dart, defect_report_screen.dart (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 4; light theme configuration signals: 1); project_components: go_router, riverpod (repository: go_router; riverpod)
**INFERRED:** input: touch (implied by platform mobile); density: medium (implied by product erp (capped for touch/remote platform)); mode: create (default (no mode cue)); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_surfaces: elevated (repository: weak signal: shadow 1, border 0); project_spacing: 4 (repository: most used spacing values [12])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); surfaces=elevated (INFERRED); spacing=4 (INFERRED); components=go_router, riverpod (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Rounded friendly sans (`typography-rounded-friendly`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Platform icon set (`icon-platform-native`) | new | no repository evidence for this slot |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Rounded terminals (e.g. Nunito, Quicksand for display only, Varela Round, M PLUS Rounded) with generous size; keep weights ≥500 for legibility; pair corner radius and icon style consistently with the type.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Use the platform set with its variable weight/fill axes rather than importing a web set; align icon weight to text weight; provide accessibility labels via the platform API.
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Core guidance (components / layouts to build)
- **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, performance, feedback, data-display; uncovered: performance)
**interaction**
- TV: exactly one visible focus at all times: Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- Mobile: density is bounded by touch: Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- TV: overscan-safe margins: Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

## Fingerprint
```json
{
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "medium",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "large",
  "typography_character": "rounded-friendly",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "focus-scale",
  "focus_strategy": "border-plus-scale",
  "cta_strategy": "single-primary",
  "image_strategy": "none",
  "icon_strategy": "system",
  "metadata_density": "moderate"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Single column, one task (0.348), Immersive hero + rails (0.262), Horizontal rails (rows of content) (0.24)
- cards: Flat tiles (0.305), No card containers (dividers and spacing) (0.296)
- typography: Platform system font (0.388), Geometric sans for product/tech brands (0.327)
- motion: Cinematic reveals (brand moments only) (0.346), Crossfade and shared-element continuity (0.308), Spring-based physical motion (0.292)
- focus: Touch-only focus handling (mobile) (0.339)
- cta: Focus is the action (TV) (0.304), Contextual inline actions (0.197)
- imagery: Immersive backdrop (0.338), Poster art as primary recognition (0.275)
- icon: Filled icons for distance and touch (0.375), Duotone icons as brand accent (0.189), Custom glyph set (0.043)
- metadata: Focus-revealed metadata (TV) (0.421), Inline badges and status chips (0.391), Minimal metadata (0.185)

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards
- typography: typography-serif-display — product-specific (ecommerce,marketing,content) does not fit request product ['erp', 'iot']; alternative within 25%
- cta: cta-sticky-bar — product-specific (ecommerce,finance,saas,healthcare) does not fit request product ['erp', 'iot']; alternative within 25%
- imagery: imagery-illustration — product-specific (education,healthcare,government,social,saas) does not fit request product ['erp', 'iot']; alternative within 25%

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
