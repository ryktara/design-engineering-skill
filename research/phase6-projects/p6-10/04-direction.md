# Design direction: Make the dashboard tell the manager which items need reordering today.

**KNOWN:** platform: web (project inspection); stack: vue (project inspection); screen: dashboard (request: dashboard); project_navigation: top-bar (repository: top-bar: 8 matches in App.vue, TopBar.vue, tokens.css (shell/layout file)); project_typography: humanist-sans (repository: font family IBM Plex Sans (2 refs); weights 600, 500)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: refactor (modification of existing UI: make); project_surfaces: bordered-flat (repository: borders in 11 files, shadow/elevation in 2); project_radius: small (repository: most common radius 5 (1×); others [6.0])
**Project context:** navigation=top-bar (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); typography=humanist-sans (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Keep the current color; inspect and reuse it. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV.
- **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **Relationship → scatter / bubble** — Both axes labelled with units, aspect ratio near 1:1 for correlation reading, bubble area (not radius) encodes size with a size legend, opacity for overplotting, trend line only with the method stated, keyboard-accessible point list or table alternative.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, data-display; uncovered: navigation)
**interaction**
- Drag and drop: affordance, feedback, keyboard alternative, no layout thrash: Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- Never colour alone: Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
- Exceptions first: surface what needs attention in lists and tables: Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "typography_character": "humanist-sans"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
