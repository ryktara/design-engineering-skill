# Design direction: Add a usage page showing this month's API calls against the plan quota.

**KNOWN:** platform: web (project inspection); product: finance (project inspection (README)); product: saas (project inspection (README)); stack: nextjs (project inspection); stack: react (project inspection); stack: tailwind (project inspection); stack: shadcn (project inspection); project_navigation: left-rail (repository: left-rail: 1 matches in app-shell.tsx (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 1; root/canvas backgrounds: 1 light, 0 dark); project_typography: custom (repository: font family Var (2 refs); monospace usage); project_components: tailwind, radix, shadcn-style cva, table:tanstack, shadcn (repository: tailwind; radix)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: create (build/create request on an existing surface); project_surfaces: bordered-flat (repository: borders in 13 files, shadow/elevation in 1); project_radius: small (repository: most common radius 0.5 (1×); others []); project_spacing: 8 (repository: most used spacing values [8, 16, 12, 4, 24]; tailwind spacing classes (124))
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=8 (INFERRED); typography=custom (KNOWN); components=tailwind, radix, shadcn-style cva, table:tanstack, shadcn (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 8 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

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
- **Progress to target → bullet / progress bar, not gauge** — Bullet graph: measure bar, target tick, qualitative bands in greys; label the value and target numerically; multiple bullets align for comparison; progress bars must show the numeric value and the whole.
- **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length.

## Guardrails (required concerns: structure, states, interaction, accessibility, data-display; uncovered: states, interaction, accessibility)
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
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
