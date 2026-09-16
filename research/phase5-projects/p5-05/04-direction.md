# Design direction: Keyboard users can't get to the chart filters.

**KNOWN:** platform: web (project inspection); input: keyboard (request: keyboard); stack: react (project inspection); project_navigation: top-bar (repository: top-bar: 5 matches in App.jsx, styles.css (shell/layout file))
**INFERRED:** input: pointer (implied by platform web); input: touch (implied by platform web); mode: accessibility (accessibility defect on existing UI); mode: audit (diagnose the reported defect); project_theme: light-first (repository: hex palette: 12 near-white, 1 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 4 (1×); others [6.0, 999.0])
**Project context:** navigation=top-bar (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED)
**Change budget:** low · preserved ['navigation', 'layout', 'surface', 'cards', 'typography', 'color', 'motion', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | High density (`density-high`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: as implemented | preserved | change budget 'low': the task does not concern this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV.
- **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Non-text contrast 3:1 for controls and focus: Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- Never colour alone: Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
**accessibility**
- Search and filters: visible state and instant feedback: Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- Semantic structure: headings, landmarks, lists, tables: Structure first, style second: choose the element for its meaning and restyle it. Data tables use <th scope>; layout tables are forbidden; visually hidden headings are fine for screen readers when the visual design omits them. _(covers: semantic structure and roles)_
- Accessible names for every control and image: Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "color_strategy": "neutral-plus-accent",
  "focus_strategy": "ring"
}
```

## Validation: OK

## Alternatives considered
- density: Low density / spacious (0.195), Medium density (0.178)
- focus: Underline / weight focus for text-first UI (0.399)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
