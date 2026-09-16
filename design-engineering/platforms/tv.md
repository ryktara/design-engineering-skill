# TV / 10-foot UI (Android TV, Google TV, Fire TV, tvOS, set-top boxes, web-on-TV)

A TV screen is a focus-driven interface operated with a 5-way remote from ~3 m. It is not a scaled desktop layout. Load this file for anything involving TV, IPTV/OTT, set-top boxes, EPG, media rails, remote/DPAD navigation, or living-room displays.

## Contents
- Input model
- Focus system
- Navigation structure
- Layout and safe area
- Typography and colour
- Content patterns
- Playback
- Text entry, search, settings
- Performance
- Accessibility on TV
- Stack pointers
- Checklist

## Input model

DPAD (up/down/left/right), SELECT/CENTER, BACK, HOME, optional MENU, PLAY/PAUSE, FF/RW, channel up/down, number keys, voice. No touch, no hover, no pointer, no scroll wheel, no drag, no pinch, no on-screen scrollbars. Every interaction must map to DPAD + SELECT + BACK; other keys are accelerators. Design for the cheapest remote the product ships with.

## Focus system

- Exactly one focused element at all times, always on screen; initial focus is deterministic per screen (first content item, or Play on a detail screen); focus is restored to the previously focused item on return; when the focused item disappears (list refresh, removal), focus moves to a sensible neighbour, never to nothing.
- Focus indication must survive any artwork: scale 1.05–1.1 (Android defaults 1.025/1.05/1.1) plus a border (2–4 dp) or glow (2–32 dp elevation), ≥3:1 against surroundings; never colour tint alone. Reserve padding for the scale overflow so neighbours are not clipped.
- Focus ≠ selected ≠ pressed: a selected tab still needs a focus treatment; pressed is a brief SELECT feedback.
- Focus feedback is instant (≤150 ms); rail scrolling ≤250 ms; input is never dropped while animating.
- Screen readers (TalkBack/VoiceOver) read the focused item: give cards a merged description (title + status), mark rail titles as headings.

## Navigation structure

- Vertical axis moves between sections/rails; horizontal axis moves between items within a section. Straight-path reachability for every control; no diagonal reasoning; no controls that require passing through unrelated rows.
- Side navigation (4–8 sections): collapsed icon strip that expands on focus; LEFT from the first item of a rail enters it; RIGHT returns to the last focused content item. Top tabs (2–5 sections): BACK from content returns focus to the active tab and scrolls to top.
- BACK unwinds one layer: player controls → player → detail → home content → navigation → exit. Never an on-screen Back button; never an exit-confirmation loop; deep links unwind to the app home; splash screens are not in the back stack.
- Search and Settings live at a predictable edge (top of the side nav / last tab).
- Grids: LEFT at column 0 may enter navigation; RIGHT at the last column stays; UP from the first row goes to the section header/tabs.

## Layout and safe area

- Design frame 960×540 dp (1080p at 2×); assets at 1080p; 16:9.
- Safe margins ≥5%: 48 dp horizontal, 27 dp vertical (Android suggests up to 58/28 dp); tvOS uses 60 pt on all sides at 1920×1080. Persistent UI (nav, titles, buttons, subtitles) stays inside; artwork and rails may bleed, and partially visible cards signal continuation.
- 12-column grid, 52 dp columns, 20 dp gutters at the design frame. Card widths for full-width rows: 1×844, 2×412, 3×268, 4×196, 5×124 dp; typical rails show ~4 landscape (16:9) or ~6 portrait (2:3) cards.
- One or two panes maximum; no dense multi-panel layouts; content first, chrome minimal.
- Titles left-aligned in the safe area; rail titles ≥24 sp.

## Typography and colour

- Type scale rebuilt for distance: body ≥24 sp (Android) / ≥29 pt (tvOS), captions ≥20 sp, titles 32–48, display 57–72 at the 1080p frame; sans with large x-height; weights ≥400 (avoid thin/light); short strings (titles ≤2 lines, synopsis ≤3 lines with expand); line height ≥1.3. `tokens.py scale --platform tv`.
- Dark-first: tinted dark canvas (not pure white backgrounds; pure black only for deliberate OLED), text 87–92% white, accent for focus and primary only, semantic colours ≥4.5:1 on dark, avoid large saturated red/orange areas (bloom/banding), dither or avoid gradients (8-bit panel banding), sRGB for UI, test in "Standard" picture mode on a real panel. `tokens.py validate --platform tv` applies stricter targets.
- Scrims under any text over imagery, tuned for the brightest artwork in the catalogue.

## Content patterns

- Home: rails (categories vertical, items horizontal) with optional immersive backdrop of the focused item (debounced 300 ms crossfade, dual scrim); focus pivot ~20–30% from the left; focus memory per rail; lazy rails and images; "see all" as the last card when a rail is capped.
- Cards: one aspect per rail (16:9 landscape for episodes/live/continue-watching with a progress bar; 2:3 portrait for films/series); title below the art unless the art reliably contains it; placeholder with title text; whole card focusable and selectable; no inner buttons; metadata revealed on focus into reserved space (or a fixed detail strip) so rows never jump.
- Detail screen: backdrop, title, one line of metadata, short synopsis, ≤4 actions in one row with first focus on Play/Resume, LEFT/RIGHT between them, DOWN into episode/related rails.
- Live TV / EPG: 2-D virtualised grid, sticky channel column (logo + number) and time header, now-line updating per minute, cells sized by duration with a minimum width, focus moves by programme (UP/DOWN keep the time slot), jump-to-now, mini player or channel preview, day picker; long-press/menu opens programme actions (record, remind).
- Grids (search results, categories): consistent card size, page-by-page lazy loading, UP from first row to the filters/tabs.

## Playback

- Media keys work without showing the overlay; DPAD_CENTER on video toggles play/pause or shows controls (one convention, consistently); LEFT/RIGHT on the progress bar seek in fixed steps with a preview thumbnail and time; overlay auto-hides after 3–5 s but never while a control is focused or a sheet is open; first focus on play/pause; subtitle/audio pickers as side sheets that keep video visible; live: go-to-live, channel up/down, mini guide; captions follow system caption preferences.

## Text entry, search, settings

- Minimise text entry; use the system keyboard or voice; never a custom on-screen keyboard as the primary path.
- Search screen: field at the top, results as rails/grid, BACK returns focus to the field.
- Settings: vertical list, label left / value right, DOWN advances, SELECT opens a simple picker; no toggles that require precise targeting.
- Sign-in: code-on-screen + companion device flow rather than typing passwords.

## Performance

Focus moves render within one frame even while images load; rows virtualised in both axes; images sized to the card and cached; backdrops capped at panel resolution and debounced; no composition/re-render storms on focus change; test on the weakest device (1–2 GB set-top boxes), not the emulator.

## Accessibility on TV

One visible focus; ≥3:1 focus contrast; ≥24 sp text with 7:1 body contrast target; merged card semantics; headings on rail titles; captions preferences; no time-limited interactions without extension; reduced-motion honoured (static backdrop, no scale animation but still a visible focus state).

## Stack pointers

`stacks/compose-tv.md` (Compose for TV: `androidx.tv.material3`, focusRestorer, LazyRow/LazyColumn with BringIntoViewSpec, Media3), `stacks/swiftui.md` (tvOS section: focusable, focusSection, TabView sidebar, AVPlayerViewController), `stacks/react-native.md` (react-native-tvos: TVFocusGuideView, hasTVPreferredFocus, TVEventHandler), `stacks/react.md` (web-on-TV: spatial navigation libraries, focus keys, CSS focus states, no hover).

## Checklist

- [ ] Every control reachable with straight DPAD paths; no hover/touch/drag assumptions
- [ ] One visible focus at all times; initial focus, restoration, and removal handled
- [ ] Focus = scale + border/glow ≥3:1; selected ≠ focused
- [ ] BACK unwinds predictably; no on-screen back; no exit loops
- [ ] Safe margins 48/27 dp at 960×540; type ≥24 sp body, ≥20 sp captions
- [ ] Dark-first tokens validated for TV; scrims over imagery
- [ ] Rails: pivot, focus memory, one aspect per rail, lazy loading, "see all"
- [ ] Detail: Play first focus, ≤4 actions in a row
- [ ] Player: media keys, auto-hide rules, seek with preview, captions
- [ ] EPG: 2-D virtualisation, now-line, programme-based focus
- [ ] Verified on emulator/device with DPAD key events and screenshots; focus latency checked on low-end hardware
