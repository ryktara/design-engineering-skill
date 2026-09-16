# Design direction: The waiting room board: nothing tells the front desk how long each patient has been sitting there.

**KNOWN:** platform: web (project inspection); product: healthcare (request: patient); product: ecommerce (project inspection (README)); stack: svelte (project inspection); stack: tailwind (project inspection); environment: shared-device (request: waiting room); project_navigation: left-rail (repository: left-rail: 1 matches in +layout.svelte (shell/layout file); also breadcrumb-tree: 1 matches); project_components: tailwind (repository: tailwind)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: audit (perceived-performance defect); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 13 near-white, 1 near-black); project_spacing: 4 (repository: most used spacing values [4, 8, 12, 16]; tailwind spacing classes (4)); project_typography: custom (repository: font family theme (1 refs))
**Project context:** navigation=left-rail (KNOWN); theme=light-first (INFERRED); spacing=4 (INFERRED); typography=custom (INFERRED); components=tailwind (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Preserve existing surface: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Guardrails (required concerns: ; uncovered: none)

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "color_strategy": "neutral-plus-accent",
  "focus_strategy": "ring"
}
```

## Validation: VIOLATIONS
- audit: no accessibility constraints attached

## Alternatives considered
- focus: Underline / weight focus for text-first UI (0.182)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
