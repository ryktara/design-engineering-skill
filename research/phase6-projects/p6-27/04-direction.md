# Design direction: In the channel guide the time header jumps every half hour and you lose where you were.

**KNOWN:** platform: web (project inspection); product: media (request: channel); stack: html-css (project inspection); screen: list (request: channel guide); project_navigation: top-bar (repository: top-bar: 6 matches in app.js, index.html, tv.css (shell/layout file))
**INFERRED:** platform: tv (wording suggests tv: channel guide); input: remote (implied by platform tv); input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: medium (implied by product media); mode: audit (perceived-performance defect); mode: refactor (fix follows the diagnosis); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_theme: dark-first (repository: root/canvas backgrounds: 0 light, 1 dark; hex palette: 1 near-white, 14 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 4 (2×); others [999.0, 5.0]); project_spacing: 4 (repository: most used spacing values [16, 12, 8, 20, 24])
**MISSING:** platform: only inferred from wording (tv); confirm before committing
**Project context:** navigation=top-bar (KNOWN); theme=dark-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: top-bar (KNOWN) (`nav-top-bar`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Preserve existing cards: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| typography | Preserve existing typography: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| color | Preserve existing color: dark-first (INFERRED) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **EPG / program guide grid** — Two-dimensional virtualisation (channels vertical, time horizontal), sticky channel column and time header, programme cells sized by duration with a minimum width so short programmes stay focusable, current time line always visible, LEFT/RIGHT move within a channel's programmes (not by pixel), UP/DOWN keep the same time slot, long press or a shortcut jumps to now, focused cell shows full title + time in a detail strip rather than truncating inside the cell.
- **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional.

## Guardrails (required concerns: accessibility, interaction, component, performance, data-display; uncovered: performance)
**interaction**
- TV: exactly one visible focus at all times: Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- TV: no touch, no hover, no scrollbars: Every interaction maps to DPAD + SELECT + BACK (+ optional MENU/PLAY keys); text entry is minimal and uses the system keyboard or voice; no hover-only affordances; no visible scrollbars; no small inline links; a desktop layout enlarged is not a TV layout. _(covers: no touch or hover assumptions on TV, no hover dependence)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "top-bar",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "color_strategy": "dark-with-accent"
}
```

## Validation: VIOLATIONS
- tv/remote: navigation 'top-bar' is a pointer/touch model

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
