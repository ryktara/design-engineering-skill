# Design direction: Add a subtitles and audio language chooser to the player.

**KNOWN:** platform: tv (project inspection); input: remote (project inspection: DPAD/remote handling in source); product: media (request: player); stack: compose (project inspection); stack: compose-tv (project inspection); screen: player (request: player); project_navigation: tv-rails (repository: tv-rails: 95 matches in AppState.kt, Cards.kt, EventDetailsScreen.kt (shell/layout file)); project_theme: dark-first (repository: dark theme configuration signals: 1; root/canvas backgrounds: 0 light, 1 dark); project_components: compose, compose-tv-material, media3, images:coil (repository: compose; compose-tv-material)
**INFERRED:** density: medium (implied by product media); mode: create (build/create request on an existing surface); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_surfaces: bordered-flat (repository: borders in 6 files, shadow/elevation in 1); project_radius: medium (repository: most common radius 8 (3×); others [50.0, 4.0]); project_spacing: 8 (repository: most used spacing values [16, 10, 8])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=tv-rails (KNOWN); theme=dark-first (KNOWN); surfaces=bordered-flat (INFERRED); radius=medium (INFERRED); spacing=8 (INFERRED); components=compose, compose-tv-material, media3, images:coil (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: tv-rails (KNOWN) (`nav-tv-side`) | preserved | repository evidence with change budget 'moderate' |
| layout | Player with overlay controls (`layout-split-player`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Platform system font (`typography-system-native`) | new | no repository evidence for this slot |
| color | Preserve existing color: dark-first (KNOWN) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | Focus is the action (TV) (`cta-focus-selects`) | new | no repository evidence for this slot |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | new | no repository evidence for this slot |
| icon | Custom glyph set (`icon-custom-glyphs`) | new | no repository evidence for this slot |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page. (Existing system: do not replace it for this task.)
- **layout** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Define the grid (24 px, 2 px stroke or filled), test at every token size, ship as SVG sprites/vector drawables with names that map to meaning, and keep a fallback mapping to a system set for missing glyphs.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences.
- **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout.
- **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, performance; uncovered: none)
**interaction**
- TV: transport control conventions: Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input (any key resets the timer; do not hide while a control is receiving input); subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour, live channel switching and mini guide, subtitle and audio track selection reachable from the player)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- TV: focus response and list performance: Focus moves must render within one frame (≤16 ms at 60 Hz) even while images load; key events are never dropped or coalesced into jumps; images sized to card, cached, and loaded with placeholders; rows virtualised vertically and horizontally; heavy backdrops debounced; test on the cheapest target device (e.g. 1–2 GB RAM set-top boxes), not the emulator. _(covers: focus latency, virtualization of long collections, image sizing and formats)_
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "canvas",
  "cta_strategy": "focus-selects",
  "content_density": "medium",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "system-native",
  "color_strategy": "dark-with-accent",
  "motion_character": "focus-scale",
  "focus_strategy": "border-plus-scale",
  "image_strategy": "immersive-backdrop",
  "icon_strategy": "custom-glyphs",
  "metadata_density": "focus-reveal"
}
```

## Validation: OK

## Alternatives considered
- layout: Horizontal rails (rows of content) (0.366), Immersive hero + rails (0.346), EPG / program guide grid (0.29)
- cards: Portrait poster cards (2:3) (0.391), Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Neutral workhorse sans (0.42), Condensed display for broadcast/media (0.371), Grotesk display + quiet body (0.345)
- motion: Cinematic reveals (brand moments only) (0.325), Crossfade and shared-element continuity (0.291), Functional minimal motion (0.278)
- cta: One primary action per screen (0.18)
- imagery: Poster art as primary recognition (0.401), Functional thumbnails (0.221), No decorative imagery (0.205)
- icon: Filled icons for distance and touch (0.375), Platform icon set (0.312)
- metadata: Minimal metadata (0.311), Moderate metadata with a hierarchy (0.304)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
