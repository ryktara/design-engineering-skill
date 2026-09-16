# Design direction: People walk away mid-purchase and the next person finds the previous ticket half bought.

**KNOWN:** platform: kiosk (project inspection); stack: html-css (project inspection); environment: public (project inspection (README)); project_navigation: hub-spoke (repository: hub-spoke: 24 matches in README.md, app.js, i18n.js (shell/layout file))
**INFERRED:** input: touch (implied by platform kiosk); mode: audit (navigation defect on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 8 near-white, 1 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: small (repository: most common radius 5 (3×); others [8.0, 12.0]); project_spacing: 4 (repository: most used spacing values [6, 12, 8])
**Project context:** navigation=hub-spoke (KNOWN); theme=light-first (INFERRED); surfaces=elevated (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: hub-spoke (KNOWN) (`nav-hub-spoke`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 4 (INFERRED) Kiosk floor: targets ≥ 64 px, body ≥ 20 px. | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — One home screen of large, labelled entry points; each spoke is a linear flow with an obvious way back to the hub. Group entry points by user goal, not by internal system module. On kiosks, the hub also serves as the idle/attract screen and every spoke must time out back to it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Guardrails (required concerns: accessibility, interaction, component, environment, privacy; uncovered: accessibility, component)
**privacy / environment**
- Kiosk: public, hurried, standing users: Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

## Fingerprint
```json
{
  "navigation_model": "hub-and-spoke",
  "color_strategy": "neutral-plus-accent",
  "cta_strategy": "single-primary"
}
```

## Validation: OK

## Alternatives considered

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
