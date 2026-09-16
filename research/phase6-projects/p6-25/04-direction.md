# Design direction: Add a "continue watching" row to the home screen.

**KNOWN:** platform: tv (project inspection); input: remote (project inspection: DPAD/remote handling in source); product: media (request: continue watching); stack: compose (project inspection); stack: compose-tv (project inspection); screen: home (request: home screen, home); job: resume (request: continue watching); project_navigation: tv-rails (repository: tv-rails: 100 matches in AppState.kt, Cards.kt, EventDetailsScreen.kt (shell/layout file)); project_theme: dark-first (repository: dark theme configuration signals: 1; root/canvas backgrounds: 0 light, 1 dark); project_typography: custom (repository: font family System (5 refs); weights bold, semibold, normal, medium); project_components: compose, compose-tv-material, media3, images:coil (repository: compose; compose-tv-material)
**INFERRED:** density: medium (implied by product media); mode: create (build/create request on an existing surface); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_surfaces: bordered-flat (repository: borders in 8 files, shadow/elevation in 1); project_radius: pill (repository: most common radius 50 (6×); others [8.0, 4.0]); project_spacing: 8 (repository: most used spacing values [16, 10, 8])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=tv-rails (KNOWN); theme=dark-first (KNOWN); surfaces=bordered-flat (INFERRED); radius=pill (INFERRED); spacing=8 (INFERRED); typography=custom (KNOWN); components=compose, compose-tv-material, media3, images:coil (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'layout', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: tv-rails (KNOWN) (`nav-tv-side`) | preserved | repository evidence with change budget 'moderate' |
| layout | Preserve existing layout: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| density | Preserve existing density: spacing base 8 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (KNOWN) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: dark-first (KNOWN) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV.
- **Media details screen, resume playback and watchlist** — Details: the primary action is Play (or Resume with the remaining time and a Start over alternative) and it takes default focus; metadata is a short scannable block (duration, year, rating, badges as text not colour), synopsis ≤3 lines with an expander, episodes as a rail or list with progress bars and the next unwatched episode preselected; secondary actions (watchlist, trailer, more like this) sit after Play in one row. Resume: a continue-watching row shows progress on each card, resumes at the saved position, and removes finished items; entering a title from the row returns focus to that card. Watchlist: one toggle with a clear on/off state and text label, works from cards and details, and is reflected immediately in the watchlist row. Everything is reachable with D-pad UP/DOWN/LEFT/RIGHT and BACK returns to the row that launched the details.
- **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp).

## Guardrails (required concerns: structure, navigation, states, interaction, accessibility, performance; uncovered: none)
**interaction**
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- TV: exactly one visible focus at all times: Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "color_strategy": "dark-with-accent"
}
```

## Validation: OK

## Alternatives considered
- cards: Portrait poster cards (2:3) (0.395), Flat tiles (0.284), No card containers (dividers and spacing) (0.272)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
