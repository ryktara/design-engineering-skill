# Design direction: From the sofa nobody can tell which row is selected on the living-room screen.

**KNOWN:** input: remote (project inspection: DPAD/remote handling in source); product: media (project inspection (README)); stack: swiftui (project inspection); project_navigation: tv-rails (repository: tv-rails: 9 matches in SearchView.swift, TVButtonStyle.swift (shell/layout file))
**INFERRED:** platform: tv (wording suggests tv: living-room, from the sofa, sofa); density: medium (implied by product media); mode: audit (interaction defect on existing UI); mode: refactor (fix follows the diagnosis); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform); project_theme: dark-first (repository: dark theme configuration signals: 2; hex palette: 1 near-white, 2 near-black); project_surfaces: elevated (repository: shadow/elevation in 2 files, borders in 0); project_radius: medium (repository: most common radius 8 (1×); others [24.0])
**MISSING:** platform: only inferred from wording (tv); confirm before committing
**Project context:** navigation=tv-rails (KNOWN); theme=dark-first (INFERRED); surfaces=elevated (INFERRED); radius=medium (INFERRED)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: tv-rails (KNOWN) (`nav-tv-side`) | preserved | repository evidence with change budget 'moderate' |
| layout | Horizontal rails (rows of content) (`layout-rails`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | new | density medium (INFERRED) |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'moderate' |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | new | no repository evidence for this slot |
| typography | Grotesk display + quiet body (`typography-grotesk-display`) | new | no repository evidence for this slot |
| color | Preserve existing color: dark-first (INFERRED) (`color-dark-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Crossfade and shared-element continuity (`motion-crossfade`) | new | no repository evidence for this slot |
| focus | Scale + glow/border focus (TV) (`focus-scale-glow`) | new | no repository evidence for this slot |
| cta | Focus is the action (TV) (`cta-focus-selects`) | new | no repository evidence for this slot |
| imagery | Immersive backdrop (`imagery-immersive-backdrop`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Focus-revealed metadata (TV) (`metadata-focus-reveal`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page. (Existing system: do not replace it for this task.)
- **layout** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — Display face with real character (e.g. Bricolage Grotesque, Instrument Sans, Familjen Grotesk, Schibsted Grotesk, Unbounded for very bold) used at ≥28 px only; body from a proven text face. Subset and preload the display font; on TV keep the display weight heavy enough to survive overscan and compression.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels). (Existing system: do not replace it for this task.)
- **motion** — Shared element for one anchor (the image) plus a crossfade for the rest; 250–350 ms; reduced-motion swaps to an instant crossfade. Use platform APIs (View Transitions API, SharedTransitionLayout, matchedGeometryEffect) not manual clones.
- **focus** — Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.

## Core guidance (components / layouts to build)
- **Media details screen, resume playback and watchlist** — Details: the primary action is Play (or Resume with the remaining time and a Start over alternative) and it takes default focus; metadata is a short scannable block (duration, year, rating, badges as text not colour), synopsis ≤3 lines with an expander, episodes as a rail or list with progress bars and the next unwatched episode preselected; secondary actions (watchlist, trailer, more like this) sit after Play in one row. Resume: a continue-watching row shows progress on each card, resumes at the saved position, and removes finished items; entering a title from the row returns focus to that card. Watchlist: one toggle with a clear on/off state and text label, works from cards and details, and is reflected immediately in the watchlist row. Everything is reachable with D-pad UP/DOWN/LEFT/RIGHT and BACK returns to the row that launched the details.
- **Horizontal rails (rows of content)** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).

## Guardrails (required concerns: accessibility, interaction, component, performance; uncovered: none)
**interaction**
- Every interactive colour has hover/pressed/focus/disabled/selected: Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them. _(covers: visible focus, selected state visible and distinct from focus and hover)_
- TV: vertical = sections, horizontal = items: Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- TV: overscan-safe margins: Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
**accessibility**
- TV: 10-foot typography: Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
**platform**
- Virtualise long lists and tables: Windowed rendering with stable row heights or measured heights, keyboard focus preserved when rows unmount (roving focus by key), aria-rowcount/aria-setsize so assistive tech knows the real size, scroll restoration on back navigation. Native: LazyColumn/List/FlatList/VirtualizingStackPanel already virtualise; keep keys stable. _(covers: virtualization of long collections)_

## Fingerprint
```json
{
  "navigation_model": "tv-side-nav",
  "layout_topology": "rails",
  "grid_behavior": "horizontal-scroll",
  "content_density": "medium",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "grotesk-display",
  "color_strategy": "dark-with-accent",
  "motion_character": "crossfade",
  "focus_strategy": "border-plus-scale",
  "cta_strategy": "focus-selects",
  "image_strategy": "immersive-backdrop",
  "icon_strategy": "filled",
  "metadata_density": "focus-reveal"
}
```

## Validation: OK

## Alternatives considered
- layout: Immersive hero + rails (0.4), EPG / program guide grid (0.344), Player with overlay controls (0.334)
- cards: Portrait poster cards (2:3) (0.34), Flat tiles (0.243), No card containers (dividers and spacing) (0.217)
- typography: Condensed display for broadcast/media (0.281), Platform system font (0.248), Neutral workhorse sans (0.141)
- motion: Focus-driven motion (TV) (0.404), Functional minimal motion (0.328), Cinematic reveals (brand moments only) (0.235)
- cta: One primary action per screen (0.27)
- imagery: Poster art as primary recognition (0.347), No decorative imagery (0.323), Functional thumbnails (0.167)
- icon: Platform icon set (0.258), Custom glyph set (0.151)
- metadata: Minimal metadata (0.257), Moderate metadata with a hierarchy (0.25)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
