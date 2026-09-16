# Design direction: Stock adjustment form: Save and Discard look identical and people click the wrong one.

**KNOWN:** platform: web (project inspection); stack: vue (project inspection); screen: form (request: form); project_navigation: top-bar (repository: top-bar: 8 matches in App.vue, TopBar.vue, tokens.css (shell/layout file)); project_typography: humanist-sans (repository: font family IBM Plex Sans (2 refs); weights 600, 500)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: polish (visual defect on existing UI); mode: audit (diagnose first); project_surfaces: bordered-flat (repository: borders in 11 files, shadow/elevation in 2); project_radius: small (repository: most common radius 5 (1×); others [6.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=top-bar (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); typography=humanist-sans (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'low': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: as implemented | preserved | change budget 'low': the task does not concern this slot |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Keep the current color; inspect and reuse it. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action.
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility, feedback; uncovered: none)
**accessibility**
- One clear focal point per screen: Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
**anti / patterns**
- Brands that differ only by logo, primary colour, and font: Run fingerprint.py compare on the candidate brand systems; a COSMETIC-ONLY verdict fails differentiation. Vary at least two structural axes (navigation model, layout topology, density, surface strategy, image strategy, metadata density, CTA strategy) per brand, then cosmetics. _(covers: structural, not cosmetic, brand differentiation)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "typography_character": "humanist-sans"
}
```

## Validation: OK

## Alternatives considered
- cards: Bordered cards (0.381), Flat tiles (0.342), No card containers (dividers and spacing) (0.268)

## Rejected for incompatibility
- cards: card-poster-landscape — media-specific pattern (education,media) with no media signal in the request or repository
- cards: card-poster-portrait — media-specific pattern (education,media) with no media signal in the request or repository

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
