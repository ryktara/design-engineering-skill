# Design direction: Photos attached to a defect report are tiny thumbnails you can't check in the field.

**KNOWN:** product: erp (project inspection (README)); product: iot (project inspection (README)); stack: flutter (project inspection); environment: outdoor (request: in the field); project_navigation: top-bar (repository: top-bar: 3 matches in checklist_screen.dart, defect_report_screen.dart, settings_screen.dart (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 4; light theme configuration signals: 2); project_components: go_router, riverpod (repository: go_router; riverpod)
**INFERRED:** platform: mobile (wording suggests mobile: in the field); input: touch (implied by platform mobile); density: medium (implied by product erp (capped for touch/remote platform)); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_radius: small (repository: most common radius 4 (1×); others [])
**MISSING:** platform: only inferred from wording (mobile); confirm before committing
**Project context:** navigation=top-bar (KNOWN); theme=dual-theme (KNOWN); radius=small (INFERRED); components=go_router, riverpod (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Low density / spacious (`density-low`) | new | outdoor/gloves: low density unless stated |
| surface | Preserve existing surface: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: as implemented | preserved | change budget 'low': the task does not concern this slot |
| color | Preserve existing color: light-first (dual theme) (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Keep the current navigation; inspect and reuse it. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Whitespace must come from a scale (e.g. 24/40/64/96), not arbitrary padding; keep line length in measure; big type is only justified for the one thing that should be read first. Spacious does not mean everything is huge. Field use: targets ≥ 48 dp with ≥ 12 dp spacing, large glanceable status.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'.
- **No decorative imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.

## Guardrails (required concerns: accessibility, interaction, component, feedback, data-display, environment; uncovered: none)
**accessibility**
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
**platform**
- Mobile: safe areas and system insets: Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view. _(covers: safe areas and notches)_
**privacy / environment**
- Field use: sunlight readability and glanceable status: Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_

## Fingerprint
```json
{
  "content_density": "low",
  "color_strategy": "neutral-plus-accent",
  "image_strategy": "none"
}
```

## Validation: VIOLATIONS
- dense product: low/spacious density selected

## Alternatives considered
- imagery: Functional thumbnails (0.345), Poster art as primary recognition (0.283), Hero imagery on landing/brand pages (0.129)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
