# Design direction: add a match details screen with play, resume and add-to-watchlist, consistent with the existing dark rails home

**KNOWN:** platform: tv (request: rails); input: remote (project inspection: DPAD/remote handling in source); product: media (request: watchlist); stack: compose (project inspection); stack: compose-tv (project inspection); screen: home (request: home); screen: detail (request: detail); job: resume (request: resume); job: watchlist (request: watchlist); job: details (request: details screen); project_navigation: tv-rails (repository: tv-rails: 56 matches in AppState.kt, Cards.kt, HomeRail.kt (shell/layout file)); project_components: compose, compose-tv-material, media3, images:coil (repository: compose; compose-tv-material)
**INFERRED:** density: medium (implied by product media); mode: create (default (no mode cue)); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_theme: dark-first (repository: dark theme configuration signals: 1; hex palette: 2 near-white, 4 near-black); project_surfaces: bordered-flat (repository: borders in 3 files, shadow/elevation in 1); project_radius: medium (repository: most common radius 8 (3×); others [50.0, 4.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=tv-rails (KNOWN); theme=dark-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=medium (INFERRED); components=compose, compose-tv-material, media3, images:coil (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: tv-rails (KNOWN) (`nav-tv-side`) | preserved | repository evidence with change budget 'moderate' |
| layout | Horizontal rails (rows of content) (`layout-rails`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Flat tiles (`card-flat-tile`) | new | no repository evidence for this slot |
| typography | Platform system font (`typography-system-native`) | new | no repository evidence for this slot |
| color | Preserve existing color: dark-first (INFERRED) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | Focus is the action (TV) (`cta-focus-selects`) | new | no repository evidence for this slot |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | new | no repository evidence for this slot |
| icon | Platform icon set (`icon-platform-native`) | new | no repository evidence for this slot |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page. (Existing system: do not replace it for this task.)
- **layout** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Use the platform set with its variable weight/fill axes rather than importing a web set; align icon weight to text weight; provide accessibility labels via the platform API.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **Media details screen, resume playback and watchlist** — Details: the primary action is Play (or Resume with the remaining time and a Start over alternative) and it takes default focus; metadata is a short scannable block (duration, year, rating, badges as text not colour), synopsis ≤3 lines with an expander, episodes as a rail or list with progress bars and the next unwatched episode preselected; secondary actions (watchlist, trailer, more like this) sit after Play in one row. Resume: a continue-watching row shows progress on each card, resumes at the saved position, and removes finished items; entering a title from the row returns focus to that card. Watchlist: one toggle with a clear on/off state and text label, works from cards and details, and is reflected immediately in the watchlist row. Everything is reachable with D-pad UP/DOWN/LEFT/RIGHT and BACK returns to the row that launched the details.
- **Focus is the action (TV)** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **Horizontal rails (rows of content)** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web.
- **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp).

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, performance; uncovered: none)
**interaction**
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "rails",
  "grid_behavior": "horizontal-scroll",
  "content_density": "medium",
  "card_geometry": "flat-tile",
  "corner_language": "small",
  "typography_character": "system-native",
  "color_strategy": "dark-with-accent",
  "motion_character": "focus-scale",
  "focus_strategy": "border-plus-scale",
  "cta_strategy": "focus-selects",
  "image_strategy": "immersive-backdrop",
  "icon_strategy": "system",
  "metadata_density": "focus-reveal"
}
```

## Validation: OK

## Alternatives considered
- layout: Immersive hero + rails (0.631), EPG / program guide grid (0.447), Player with overlay controls (0.328)
- cards: Landscape media cards (16:9) (0.401), Portrait poster cards (2:3) (0.391), No card containers (dividers and spacing) (0.268)
- typography: Condensed display for broadcast/media (0.371), Grotesk display + quiet body (0.345), Humanist sans for approachable products (0.221)
- motion: Crossfade and shared-element continuity (0.457), Cinematic reveals (brand moments only) (0.405), Functional minimal motion (0.278)
- cta: One primary action per screen (0.324)
- imagery: Poster art as primary recognition (0.401), Functional thumbnails (0.28), No decorative imagery (0.205)
- icon: Filled icons for distance and touch (0.375), Custom glyph set (0.169)
- metadata: Moderate metadata with a hierarchy (0.403), Minimal metadata (0.332)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
