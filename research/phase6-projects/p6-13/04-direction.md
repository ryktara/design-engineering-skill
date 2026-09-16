# Design direction: The habit list has nothing to say the first time you open the app.

**KNOWN:** platform: mobile (project inspection); stack: swiftui (project inspection); project_navigation: bottom-tabs (repository: bottom-tabs: 7 matches in README.md, RootTabView.swift, StreaksApp.swift (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 2; root/canvas backgrounds: 2 light, 2 dark); project_typography: custom (repository: font family System (7 refs); weights 600, 500, 700, 800)
**INFERRED:** input: touch (implied by platform mobile); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_surfaces: elevated (repository: shadow/elevation in 5 files, borders in 1); project_radius: small (repository: most common radius 5 (4×); others [3.0, 8.0])
**Project context:** navigation=bottom-tabs (KNOWN); theme=dual-theme (KNOWN); surfaces=elevated (INFERRED); radius=small (INFERRED); typography=custom (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: bottom-tabs (KNOWN) (`nav-bottom-tabs`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar.
- **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost.

## Guardrails (required concerns: accessibility, interaction, component; uncovered: accessibility)

## Fingerprint
```json
{
  "navigation_model": "bottom-tabs",
  "surface_strategy": "elevated",
  "card_geometry": "elevated",
  "corner_language": "medium",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
