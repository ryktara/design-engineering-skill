# Design direction: Sync status is a spinner that never says what is happening.

**KNOWN:** platform: mobile (project inspection); product: erp (project inspection (README)); product: iot (project inspection (README)); stack: flutter (project inspection); project_navigation: top-bar (repository: top-bar: 6 matches in checklist_screen.dart, defect_report_screen.dart, settings_screen.dart (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 5; light theme configuration signals: 2); project_components: go_router, riverpod (repository: go_router; riverpod)
**INFERRED:** input: touch (implied by platform mobile); density: medium (implied by product erp (capped for touch/remote platform)); mode: audit (perceived-performance defect); mode: refactor (fix follows the diagnosis); project_radius: small (repository: most common radius 4 (1×); others [])
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); radius=small (INFERRED); components=go_router, riverpod (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: as implemented | preserved | change budget 'low': the task does not concern this slot |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Inline badges and status chips** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Never colour alone: Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
**accessibility**
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
**privacy / environment**
- Offline, sync, and connectivity states: Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states)_

## Fingerprint
```json
{
  "content_density": "medium",
  "color_strategy": "neutral-plus-accent",
  "metadata_density": "inline-badges"
}
```

## Validation: OK

## Alternatives considered
- metadata: Moderate metadata with a hierarchy (0.29), Minimal metadata (0.131)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
