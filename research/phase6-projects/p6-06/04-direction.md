# Design direction: The patient detail billing tab shows amounts that do not line up.

**KNOWN:** platform: web (project inspection); product: healthcare (request: patient); stack: svelte (project inspection); stack: tailwind (project inspection); screen: detail (request: detail); project_navigation: left-rail (repository: left-rail: 1 matches in +layout.svelte (shell/layout file); also breadcrumb-tree: 1 matches); project_components: tailwind (repository: tailwind)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: polish (visual defect on existing UI); mode: audit (diagnose first); project_theme: light-first (repository: hex palette: 13 near-white, 1 near-black); project_surfaces: bordered-flat (repository: borders in 12 files, shadow/elevation in 2); project_spacing: 4 (repository: most used spacing values [16, 8, 12, 4, 24]; tailwind spacing classes (119)); project_typography: custom (repository: font family theme (1 refs); tabular numerals)
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=left-rail (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); spacing=4 (INFERRED); typography=custom (INFERRED); components=tailwind (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'low': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
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
- **Master–detail (list + detail pane)** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content.
- **Clinical workstation** — Patient banner always visible (identity, allergies, alerts) as the focal element, master-detail for patient lists and records, strict status colour language with text and icons (never colour alone), large legible numerics with units, quiet neutral surfaces, confirmation for critical actions with the safe default, interruption-safe autosave. Identity via the banner treatment and status language; restraint is the brand.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility; uncovered: anti-pattern, accessibility)
**accessibility**
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
