# Design direction: add a search screen to the tvOS documentary app that fits the existing sign-in and player styling

**KNOWN:** platform: tv (request: tvos); input: remote (project inspection: DPAD/remote handling in source); product: media (request: player); stack: swiftui (project inspection); screen: player (request: player); screen: search (request: search screen, search); screen: auth (request: sign in); job: authentication (request: sign in, sign-in); job: search (request: search screen)
**INFERRED:** density: medium (implied by product media); mode: create (default (no mode cue)); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_theme: dark-first (repository: dark theme configuration signals: 2; hex palette: 1 near-white, 2 near-black); project_surfaces: elevated (repository: weak signal: shadow 1, border 0); project_radius: medium (repository: most common radius 8 (1×); others [24.0])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** theme=dark-first (INFERRED); surfaces=elevated (INFERRED); radius=medium (INFERRED)
**Change budget:** moderate · preserved ['surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | TV side navigation (collapsible drawer) (`nav-tv-side`) | new | no repository evidence for this slot |
| layout | Player with overlay controls (`layout-split-player`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Condensed display for broadcast/media (`typography-condensed-display`) | new | no repository evidence for this slot |
| color | Preserve existing color: dark-first (INFERRED) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | Focus is the action (TV) (`cta-focus-selects`) | new | no repository evidence for this slot |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page.
- **layout** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Condensed only for titles and channel names (e.g. Barlow Condensed, Oswald, Roboto Condensed, Archivo Narrow) at heavy weights; body and metadata in a normal-width sans with tabular figures for times.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **TV sign-in: code on screen and companion device** — Primary path: a short activation code (6–8 chars, no ambiguous glyphs, large 10-foot type) plus a short URL or QR code, polled until the companion device completes sign-in; the TV screen shows what to do in one sentence, the code, a 'waiting' state that is obviously alive, expiry with a regenerate action, and a secondary 'type here' fallback using the system keyboard. On success land on the profile picker; on shared TVs offer a PIN for adult profiles. Focus starts on the primary fallback button so BACK/SELECT behave predictably.
- **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences.
- **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK.
- **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, performance, feedback; uncovered: performance)
**interaction**
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- Form labels, errors, and recovery: Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "canvas",
  "cta_strategy": "focus-selects",
  "content_density": "medium",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "condensed-display",
  "color_strategy": "dark-with-accent",
  "motion_character": "focus-scale",
  "focus_strategy": "border-plus-scale",
  "image_strategy": "immersive-backdrop",
  "icon_strategy": "filled",
  "metadata_density": "focus-reveal"
}
```

## Validation: OK

## Alternatives considered
- navigation: TV top tabs (0.454), Linear wizard / stepper (0.047)
- layout: Horizontal rails (rows of content) (0.51), Immersive hero + rails (0.346), Form stack with sections (0.33)
- cards: Portrait poster cards (2:3) (0.391), Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Platform system font (0.414), Grotesk display + quiet body (0.345), Humanist sans for approachable products (0.221)
- motion: Cinematic reveals (brand moments only) (0.325), Crossfade and shared-element continuity (0.291), Functional minimal motion (0.278)
- cta: One primary action per screen (0.324)
- imagery: Functional thumbnails (0.404), Poster art as primary recognition (0.401), No decorative imagery (0.205)
- icon: Platform icon set (0.312), Custom glyph set (0.169)
- metadata: Minimal metadata (0.311), Moderate metadata with a hierarchy (0.304)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
