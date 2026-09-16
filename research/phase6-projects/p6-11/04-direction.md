# Design direction: Inspectors in gloves keep missing the small checkbox on each defect row.

**KNOWN:** platform: mobile (project inspection); input: touch (request: gloves); product: iot (project inspection (README)); stack: flutter (project inspection); environment: outdoor (project inspection (README)); environment: gloves (request: gloves); environment: low-bandwidth (project inspection (README)); project_navigation: top-bar (repository: top-bar: 6 matches in checklist_screen.dart, defect_report_screen.dart, settings_screen.dart (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 5; light theme configuration signals: 2); project_typography: custom (repository: font family System (7 refs); weights w600, w700, w400); project_components: go_router, riverpod (repository: go_router; riverpod)
**INFERRED:** mode: audit (interaction defect on existing UI); mode: responsive (size/viewport cues with a defect); mode: refactor (fix follows the diagnosis); project_radius: small (repository: most common radius 4 (1×); others [])
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); radius=small (INFERRED); typography=custom (KNOWN); components=go_router, riverpod (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: as implemented Field-use floor: targets ≥ 48 dp with ≥ 12 dp spacing. | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning.

## Guardrails (required concerns: accessibility, interaction, component, feedback, environment, states; uncovered: none)
**accessibility**
- One clear focal point per screen: Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
**privacy / environment**
- Field use: sunlight readability and glanceable status: Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_
- Offline, sync, and connectivity states: Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_

## Fingerprint
```json
{
  "card_geometry": "list-row",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

## Alternatives considered
- cards: Flat tiles (0.228), No card containers (dividers and spacing) (0.217), Landscape media cards (16:9) (0.209)

## Rejected for incompatibility
- cards: card-poster-landscape — media-specific pattern (education,media) with no media signal in the request or repository
- cards: card-poster-portrait — media-specific pattern (education,media) with no media signal in the request or repository

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
