# Design direction: Purchase order screen: operators want to do the whole entry without touching the mouse.

**KNOWN:** platform: desktop (project inspection); input: pointer (request: mouse); product: erp (request: purchase order); stack: wpf (project inspection); project_navigation: menu-bar (repository: menu-bar: 2 matches in App.xaml.cs, PurchaseOrderLinesView.xaml (shell/layout file)); project_theme: light-first (repository: root/canvas backgrounds: 4 light, 0 dark; hex palette: 11 near-white, 1 near-black); project_components: wpf (repository: wpf)
**INFERRED:** input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_surfaces: bordered-flat (repository: borders in 5 files, shadow/elevation in 0); project_radius: small (repository: most common radius 2 (4×); others [1.0, 10.0]); project_spacing: 4 (repository: most used spacing values [16, 8, 6, 2, 12]); project_typography: humanist-sans (repository: font family Segoe UI Variable Text, Segoe UI (1 refs); monospace face Cascadia Mono, Consolas used for a code/number role)
**Project context:** navigation=menu-bar (KNOWN); theme=light-first (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); typography=humanist-sans (INFERRED); components=wpf (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (KNOWN) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: humanist-sans (INFERRED) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
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
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: component)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
**accessibility**
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
