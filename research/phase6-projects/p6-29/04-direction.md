# Design direction: The confirmation screen prints the receipt but never says the pick-up is complete.

**KNOWN:** platform: kiosk (project inspection); product: healthcare (project inspection (README)); product: iot (project inspection (README)); stack: html-css (project inspection); screen: form (request: confirmation screen); environment: public (project inspection (README)); project_navigation: hub-spoke (repository: hub-spoke: 29 matches in README.md, app.js, i18n.js (shell/layout file)); project_typography: humanist-sans (repository: font family Nunito (2 refs); weights 700, 800, 600, 500)
**INFERRED:** input: touch (implied by platform kiosk); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: medium (repository: most common radius 12 (1×); others [20.0, 32.0])
**Project context:** navigation=hub-spoke (KNOWN); surfaces=elevated (INFERRED); radius=medium (INFERRED); typography=humanist-sans (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: hub-spoke (KNOWN) (`nav-hub-spoke`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: as implemented Kiosk floor: targets ≥ 64 px, body ≥ 20 px. | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: humanist-sans (KNOWN) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
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
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Keep the current color; inspect and reuse it. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **On-screen keypad / keyboard for kiosks** — Keys ≥ 64 px with ≥ 16 px gaps, one key = one accessible name ('Hyphen', 'Delete', 'Space'), the keypad is a role=group labelled by the field it edits; the value box is focusable and read back through a polite live region as it changes; a persistent format hint (not a placeholder) is tied to the field with aria-describedby and errors set aria-invalid with a specific message ('Day must be 1–31'); focus never falls to the page body after a tap (re-focus the equivalent key after a re-render); a physical keypad or scanner wedge writes into the same field (human-speed keys fill, Enter continues, bursts are treated as scans); masked entry for PINs with a visible dot per character; in accessible mode the keypad and value sit in the reach zone (lower part of the screen).
- **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action.
- **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action.

## Guardrails (required concerns: accessibility, interaction, component, environment, privacy, feedback; uncovered: none)
**states**
- Progress for background work: what, how far, what went wrong: State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_
**privacy / environment**
- Kiosk: public, hurried, standing users: Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

## Fingerprint
```json
{
  "navigation_model": "hub-and-spoke",
  "typography_character": "humanist-sans",
  "cta_strategy": "single-primary"
}
```

## Validation: OK

## Alternatives considered

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
