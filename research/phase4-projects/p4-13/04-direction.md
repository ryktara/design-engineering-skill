# Design direction: refactor the defect report form so it stays usable with the keyboard open and photos can be retaken, keeping the app's existing theme and navigation

**KNOWN:** platform: mobile (project inspection); platform: tv (project inspection); input: keyboard (request: keyboard); input: remote (project inspection: DPAD/remote handling in source); product: erp (project inspection (README)); product: iot (project inspection (README)); stack: flutter (project inspection); screen: form (request: form); mode: refactor (explicit: refactor; change request with structural words: refactor, navigation); project_navigation: top-bar (repository: top-bar: 2 matches in checklist_screen.dart, defect_report_screen.dart (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 4; light theme configuration signals: 1); project_components: go_router, riverpod (repository: go_router; riverpod)
**INFERRED:** input: touch (implied by platform mobile); density: medium (implied by product erp (capped for touch/remote platform)); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_surfaces: elevated (repository: weak signal: shadow 1, border 0); project_spacing: 4 (repository: most used spacing values [12])
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); surfaces=elevated (INFERRED); spacing=4 (INFERRED); components=go_router, riverpod (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **TV top tabs** — Tabs sit in the top safe area; Back from any rail jumps focus to the active tab and scrolls to top; focused tab shows the underline/pill with ≥3:1 contrast and the label stays visible. Switching tabs does not move focus into content until the user presses DOWN.
- **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, performance, feedback, data-display; uncovered: performance)
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
  "corner_language": "small",
  "typography_character": "neutral-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "border-plus-scale",
  "cta_strategy": "sticky-bar",
  "image_strategy": "none",
  "icon_strategy": "filled",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- non-media product: poster (media) card geometry selected

## Alternatives considered
- layout: Single column, one task (0.424), Catalog grid (0.317), Immersive hero + rails (0.243)
- cards: Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Platform system font (0.357), Humanist sans for approachable products (0.35), Rounded friendly sans (0.316)
- motion: Focus-driven motion (TV) (0.395), Crossfade and shared-element continuity (0.307), Expressive brand motion (0.29)
- focus: Touch-only focus handling (mobile) (0.415)
- cta: Focus is the action (TV) (0.379), One primary action per screen (0.367), Floating action button (Material) (0.252)
- imagery: Poster art as primary recognition (0.275), Immersive backdrop (0.243), Functional thumbnails (0.221)
- icon: Platform icon set (0.35), Duotone icons as brand accent (0.258), Custom glyph set (0.043)
- metadata: Focus-revealed metadata (TV) (0.524), Moderate metadata with a hierarchy (0.304), Minimal metadata (0.185)

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards
- cards: card-none — incompatible with surface-elevated-cards

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
