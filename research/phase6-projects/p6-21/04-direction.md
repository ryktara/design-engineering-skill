# Design direction: The vehicle map and the list fight for space when the window is narrow.

**KNOWN:** platform: desktop (project inspection); stack: avalonia (project inspection); project_navigation: menu-bar (repository: menu-bar: 1 matches in MainWindow.axaml (shell/layout file); also left-rail: 1 matches); project_typography: humanist-sans (repository: font family Segoe UI, avares://Avalonia.Fonts.Inter/Assets#Inter (2 refs); weights 600, semibold); project_components: avalonia (repository: avalonia)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); mode: responsive (responsive defect); mode: audit (diagnose first); project_theme: light-first (repository: root/canvas backgrounds: 1 light, 0 dark; hex palette: 18 near-white, 0 near-black); project_surfaces: bordered-flat (repository: borders in 3 files, shadow/elevation in 1); project_radius: small (repository: most common radius 4 (3×); others []); project_spacing: 4 (repository: most used spacing values [6, 4, 8, 2, 16])
**Project context:** navigation=menu-bar (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); typography=humanist-sans (KNOWN); components=avalonia (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (KNOWN) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Geographic values → choropleth or symbol map** — Choropleth for rates with a sequential palette and ≤7 classes; symbol map for counts with area-scaled circles; equal-area projection; hover/focus tooltip with region name and value; always provide a ranked table alternative; load map data lazily.
- **Relationship → scatter / bubble** — Both axes labelled with units, aspect ratio near 1:1 for correlation reading, bubble area (not radius) encodes size with a size legend, opacity for overplotting, trend line only with the method stated, keyboard-accessible point list or table alternative.

## Guardrails (required concerns: adaptive, structure, interaction, accessibility; uncovered: accessibility)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
**platform**
- Desktop: layouts survive window resizing and DPI: Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

## Alternatives considered
- cards: Bordered cards (0.234), No card containers (dividers and spacing) (0.192), Flat tiles (0.158)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
