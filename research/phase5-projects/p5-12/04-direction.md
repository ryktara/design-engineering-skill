# Design direction: Older customers time out on the identify step before they finish typing.

**KNOWN:** platform: web (project inspection); product: healthcare (project inspection (README)); product: government (project inspection (README)); stack: html-css (project inspection); project_navigation: hub-spoke (repository: hub-spoke: 27 matches in README.md, app.js, i18n.js (shell/layout file)); project_typography: humanist-sans (repository: font family Nunito (2 refs); weights 700, 800, 600, 500)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: medium (repository: most common radius 12 (1×); others [20.0, 32.0])
**Project context:** navigation=hub-spoke (KNOWN); surfaces=elevated (INFERRED); radius=medium (INFERRED); typography=humanist-sans (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'surface', 'cards', 'typography', 'color', 'motion', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: hub-spoke (KNOWN) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | High density (`density-high`) | new | no repository evidence for this slot |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: as implemented | preserved | change budget 'low': the task does not concern this slot |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Keep the current color; inspect and reuse it. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action.
- **Flat surfaces with tonal layers** — Define three tonal steps per theme with measured contrast (each step ≥1.1:1 apart and borders ≥3:1 where they mark boundaries). Shadows reserved for transient layers (menus, dialogs, drag). Reads professional at any density and avoids the 'everything is a floating card' look.

## Guardrails (required concerns: accessibility, interaction, component; uncovered: component)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**platform**
- Web: content-driven breakpoints and a test matrix: Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
**states**
- Saving, saved, autosave, session expiry, and permission-denied states: Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry on a personal device (restore the draft after re-authentication; on shared or public screens clear it instead); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default. _(covers: saving, saved and conflict states, session expiry and idle reset, confirmation of destructive or high-risk actions)_

## Fingerprint
```json
{
  "content_density": "high",
  "surface_strategy": "elevated",
  "card_geometry": "elevated",
  "corner_language": "medium",
  "typography_character": "humanist-sans",
  "focus_strategy": "ring"
}
```

## Validation: OK

## Alternatives considered
- density: Medium density (0.214), Low density / spacious (0.195)
- focus: Underline / weight focus for text-first UI (0.182)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
