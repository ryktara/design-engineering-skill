# Design direction: Android TV live sports app home with rails, EPG entry and a mini player for the family TV, Compose

**KNOWN:** platform: tv (request: tv, android tv, epg, rails); input: remote (project inspection: DPAD/remote handling in source); product: media (request: player, epg); stack: compose (request: compose); stack: compose-tv (project inspection); screen: home (request: home); screen: list (request: epg); screen: player (request: player)
**INFERRED:** density: medium (implied by product media); mode: create (default when no mode word is present); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform)
**MISSING:** brand: no brand assets, guideline, or character description available
**CONFLICTS:** platform: request ['tv'] vs project mobile → request kept; repository platform recorded as context

| Slot | Choice | Why |
|---|---|---|
| navigation | TV side navigation (collapsible drawer) (`nav-tv-side`) | platform tv, input remote (stated), mode create, product media, density medium |
| layout | Horizontal rails (rows of content) (`layout-rails`) | platform tv, input remote (stated), mode create, product media, screen home,list, density medium |
| density | Medium density (`density-medium`) | density medium (INFERRED) |
| surface | Imagery-backed surfaces (`surface-imagery-backed`) | platform tv, mode create, product media |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | platform tv, mode create, product media, density medium |
| typography | Condensed display for broadcast/media (`typography-condensed-display`) | platform tv, mode create, product media, density medium |
| color | Neutral canvas + one accent (`color-neutral-accent`) | mode create, product mismatch |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | platform tv, input remote (stated), mode create, product media |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | platform tv, input remote (stated), mode create |
| cta | Focus is the action (TV) (`cta-focus-selects`) | platform tv, input remote (stated), mode create, product media, screen home,list,player |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | platform tv, input remote (stated), mode create, product media |
| icon | Filled icons for distance and touch (`icon-filled-system`) | platform tv, input remote (stated), mode create |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | platform tv, input remote (stated), mode create, product media, density medium |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page.
- **layout** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Every text-over-image placement gets a scrim tuned so the worst-case image still yields ≥4.5:1; image sizes are capped to the panel/viewport; focus/hover states cannot rely on colour changes hidden by imagery (use scale, border, glow). Provide a text-only fallback for missing artwork.
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Condensed only for titles and channel names (e.g. Barlow Condensed, Oswald, Roboto Condensed, Archivo Narrow) at heavy weights; body and metadata in a normal-width sans with tabular figures for times.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences.
- **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.
- **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional.

## Guardrails (required concerns: component, structure, navigation, states, interaction, accessibility, performance, data-display; uncovered: none)
**interaction**
- TV: exactly one visible focus at all times: Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state.
- TV: focus response and list performance: Focus moves must render within one frame (≤16 ms at 60 Hz) even while images load; key events are never dropped or coalesced into jumps; images sized to card, cached, and loaded with placeholders; rows virtualised vertically and horizontally; heavy backdrops debounced; test on the cheapest target device (e.g. 1–2 GB RAM set-top boxes), not the emulator.
- TV: overscan-safe margins: Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content.
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3.
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks.

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "rails",
  "grid_behavior": "horizontal-scroll",
  "content_density": "medium",
  "surface_strategy": "imagery-backed",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "condensed-display",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "focus-scale",
  "focus_strategy": "border-plus-scale",
  "cta_strategy": "focus-selects",
  "image_strategy": "immersive-backdrop",
  "icon_strategy": "filled",
  "metadata_density": "focus-reveal"
}
```

## Validation: OK

## Alternatives considered
- navigation: TV top tabs (0.454), Linear wizard / stepper (0.047)
- layout: Player with overlay controls (0.632), Immersive hero + rails (0.616), EPG / program guide grid (0.55)
- surface: Flat surfaces with tonal layers (0.278)
- cards: Portrait poster cards (2:3) (0.391), Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Grotesk display + quiet body (0.345), Platform system font (0.339), Humanist sans for approachable products (0.246)
- color: Dark canvas + accent (dark-first) (0.365), Dominant brand colour (0.345), Material tonal palette (Android) (0.345)
- motion: Cinematic reveals (brand moments only) (0.325), Crossfade and shared-element continuity (0.291), Functional minimal motion (0.278)
- cta: One primary action per screen (0.324)
- imagery: Poster art as primary recognition (0.401), Functional thumbnails (0.221), No decorative imagery (0.205)
- icon: Platform icon set (0.312), Custom glyph set (0.169)
- metadata: Minimal metadata (0.311), Moderate metadata with a hierarchy (0.304)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
