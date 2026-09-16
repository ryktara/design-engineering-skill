# Design direction: Front desk on a tablet: the appointment chips are too small to tap.

**KNOWN:** platform: tablet (request: tablet); input: touch (request: tap); product: healthcare (project inspection (README)); stack: svelte (project inspection); stack: tailwind (project inspection); project_navigation: left-rail (repository: left-rail: 1 matches in +layout.svelte (shell/layout file); also breadcrumb-tree: 1 matches); project_components: tailwind (repository: tailwind)
**INFERRED:** mode: responsive (responsive defect); mode: audit (diagnose first); project_theme: light-first (repository: hex palette: 13 near-white, 1 near-black); project_surfaces: bordered-flat (repository: borders in 12 files, shadow/elevation in 2); project_spacing: 4 (repository: most used spacing values [16, 8, 12, 4, 24]; tailwind spacing classes (123)); project_typography: custom (repository: font family theme (1 refs); tabular numerals)
**CONFLICTS:** platform: request ['tablet'] vs project web → request kept; repository platform recorded as context
**Project context:** navigation=left-rail (KNOWN); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); spacing=4 (INFERRED); typography=custom (INFERRED); components=tailwind (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | new | no repository evidence for this slot |

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
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Guardrails (required concerns: adaptive, structure, interaction, accessibility, privacy; uncovered: none)
**interaction**
- Target size by platform: Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
- One clear focal point per screen: Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- Spacing from one scale, grouping by proximity: A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
**platform**
- Mobile: orientation changes and size classes: Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
**privacy / environment**
- Privacy on shared and public screens: Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_

## Fingerprint
```json
{
  "color_strategy": "neutral-plus-accent",
  "metadata_density": "moderate"
}
```

## Validation: OK

## Alternatives considered
- metadata: Minimal metadata (0.095)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
