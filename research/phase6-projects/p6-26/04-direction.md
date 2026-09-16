# Design direction: Titles on the poster rows are cut off and there is no way to read the full name.

**KNOWN:** platform: tv (project inspection); input: remote (project inspection: DPAD/remote handling in source); product: media (request: poster); stack: swiftui (project inspection); project_navigation: tv-rails (repository: tv-rails: 29 matches in SearchView.swift, TVButtonStyle.swift, Tokens.swift (shell/layout file)); project_typography: custom (repository: font family System (2 refs); monospace usage)
**INFERRED:** density: medium (implied by product media); mode: polish (visual defect on existing UI); mode: responsive (size/viewport cues with a defect); mode: audit (diagnose first); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_theme: dark-first (repository: dark theme configuration signals: 2; hex palette: 2 near-white, 4 near-black); project_surfaces: elevated (repository: shadow/elevation in 2 files, borders in 0); project_radius: medium (repository: most common radius 8 (1×); others [24.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=tv-rails (KNOWN); theme=dark-first (INFERRED); surfaces=elevated (INFERRED); radius=medium (INFERRED); typography=custom (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: tv-rails (KNOWN) (`nav-tv-side`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: as implemented | preserved | existing system with change budget 'low': density is not the task |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'low' |
| cards | Portrait poster cards (2:3) (`card-poster-portrait`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: dark-first (INFERRED) (`color-dark-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Poster art as primary recognition (`imagery-poster`) | new | no repository evidence for this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Fixed 2:3 ratio, title below the art (not over it) unless the art contains the title reliably, placeholder with title text, scale on focus with reserved margin. On TV about 6 per row at 960 dp width with 20 dp gutters.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — One aspect ratio per rail (2:3 portrait or 16:9 landscape), title text below or revealed on focus (never over the art without a scrim), placeholders with the title text for missing art, images sized to the rendered card (no 4K posters in 200 px cards), progressive loading with a low-res or colour placeholder.
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV.
- **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility, performance; uncovered: anti-pattern, performance)
**interaction**
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- Every interactive colour has hover/pressed/focus/disabled/selected: Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them. _(covers: visible focus, selected state visible and distinct from focus and hover)_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- Spacing from one scale, grouping by proximity: A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- One clear focal point per screen: Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "color_strategy": "dark-with-accent",
  "image_strategy": "poster-art"
}
```

## Validation: OK

## Alternatives considered
- cards: No card containers (dividers and spacing) (0.352), Landscape media cards (16:9) (0.34), Flat tiles (0.208)
- imagery: Immersive backdrop (0.338), No decorative imagery (0.261), Functional thumbnails (0.131)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
