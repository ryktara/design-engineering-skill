# Design direction: In dark mode the transaction dates are barely visible.

**KNOWN:** platform: mobile (project inspection); product: finance (project inspection (README)); stack: compose (project inspection); project_navigation: top-bar (repository: top-bar: 30 matches in AccountDetailScreen.kt, AccountsScreen.kt, CardsScreen.kt (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 3; light theme configuration signals: 2); project_typography: custom (repository: font family System (8 refs); weights medium, normal, bold); project_components: compose, material3 (repository: compose; material3)
**INFERRED:** input: touch (implied by platform mobile); density: medium (implied by product finance (capped for touch/remote platform)); mode: accessibility (accessibility defect on existing UI); mode: audit (diagnose the reported defect); project_surfaces: bordered-flat (repository: borders in 2 files, shadow/elevation in 0); project_radius: small (repository: most common radius 4 (2×); others [12.0, 8.0])
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); typography=custom (KNOWN); components=compose, material3 (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'low': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: component, data-display)
**interaction**
- Non-text contrast 3:1 for controls and focus: Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_

## Fingerprint
```json
{
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
