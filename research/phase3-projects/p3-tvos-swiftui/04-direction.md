# Design direction: tvOS documentary streaming app: sign-in with an activation code and a player with auto-hiding transport controls and a subtitle picker

**KNOWN:** platform: tv (request: tvos); input: remote (project inspection: DPAD/remote handling in source); product: media (request: streaming, player); stack: swiftui (project inspection); screen: player (request: player); screen: auth (request: sign in); job: authentication (request: sign in, sign-in)
**INFERRED:** density: medium (implied by product media); mode: create (default when no mode word is present); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform)
**MISSING:** brand: no brand assets, guideline, or character description available
**CONFLICTS:** platform: request ['tv'] vs project mobile → request kept; repository platform recorded as context

| Slot | Choice | Why |
|---|---|---|
| navigation | TV side navigation (collapsible drawer) (`nav-tv-side`) | platform tv, input remote (stated), mode create, product media, density medium |
| layout | Player with overlay controls (`layout-split-player`) | platform tv, input remote (stated), mode create, product media, screen player |
| density | Medium density (`density-medium`) | density medium (INFERRED) |
| surface | Imagery-backed surfaces (`surface-imagery-backed`) | platform tv, mode create, product media |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | platform tv, mode create, product media, density medium |
| typography | Condensed display for broadcast/media (`typography-condensed-display`) | platform tv, mode create, product media, density medium |
| color | Dark canvas + accent (dark-first) (`color-dark-accent`) | platform tv, mode create, product media |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | platform tv, input remote (stated), mode create, product media |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | platform tv, input remote (stated), mode create |
| cta | Focus is the action (TV) (`cta-focus-selects`) | platform tv, input remote (stated), mode create, product media, screen player |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | platform tv, input remote (stated), mode create, product media |
| icon | Filled icons for distance and touch (`icon-filled-system`) | platform tv, input remote (stated), mode create |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | platform tv, input remote (stated), mode create, product media, density medium |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page.
- **layout** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Every text-over-image placement gets a scrim tuned so the worst-case image still yields ≥4.5:1; image sizes are capped to the panel/viewport; focus/hover states cannot rely on colour changes hidden by imagery (use scale, border, glow). Provide a text-only fallback for missing artwork.
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Condensed only for titles and channel names (e.g. Barlow Condensed, Oswald, Roboto Condensed, Archivo Narrow) at heavy weights; body and metadata in a normal-width sans with tabular figures for times.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels).
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **TV sign-in: code on screen and companion device** — Primary path: a short activation code (6–8 chars, no ambiguous glyphs, large 10-foot type) plus a short URL or QR code, polled until the companion device completes sign-in; the TV screen shows what to do in one sentence, the code, a 'waiting' state that is obviously alive, expiry with a regenerate action, and a secondary 'type here' fallback using the system keyboard. On success land on the profile picker; on shared TVs offer a PIN for adult profiles. Focus starts on the primary fallback button so BACK/SELECT behave predictably.
- **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences.
- **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, performance, feedback; uncovered: none)
**interaction**
- TV: transport control conventions: Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input; subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour)_
- TV: exactly one visible focus at all times: Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus)_
- TV: focus response and list performance: Focus moves must render within one frame (≤16 ms at 60 Hz) even while images load; key events are never dropped or coalesced into jumps; images sized to card, cached, and loaded with placeholders; rows virtualised vertically and horizontally; heavy backdrops debounced; test on the cheapest target device (e.g. 1–2 GB RAM set-top boxes), not the emulator. _(covers: focus latency, virtualization of long collections, image sizing and formats)_
**platform**
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "canvas",
  "cta_strategy": "focus-selects",
  "content_density": "medium",
  "surface_strategy": "imagery-backed",
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
- layout: Horizontal rails (rows of content) (0.366), Immersive hero + rails (0.346), Form stack with sections (0.33)
- surface: Flat surfaces with tonal layers (0.278)
- cards: Portrait poster cards (2:3) (0.391), Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Grotesk display + quiet body (0.345), Platform system font (0.302), Humanist sans for approachable products (0.221)
- color: Dominant brand colour (0.345), Material tonal palette (Android) (0.345), Duotone identity (0.325)
- motion: Cinematic reveals (brand moments only) (0.325), Crossfade and shared-element continuity (0.291), Functional minimal motion (0.278)
- cta: One primary action per screen (0.324)
- imagery: Poster art as primary recognition (0.401), Functional thumbnails (0.221), No decorative imagery (0.205)
- icon: Platform icon set (0.312), Custom glyph set (0.169)
- metadata: Minimal metadata (0.311), Moderate metadata with a hierarchy (0.304)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
