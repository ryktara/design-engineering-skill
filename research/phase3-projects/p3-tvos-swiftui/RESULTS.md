# p3-tvos-swiftui — results

## Task
"tvOS documentary streaming app: sign-in with an activation code and a player with auto-hiding transport controls and a subtitle picker"

Scope built: (a) sign-in with on-screen activation code + QR + "sign in on this Apple TV" fallback (system keyboard), (b) full-screen player with custom transport controls (auto-hide 5 s), subtitle/audio side sheet, next-episode prompt with countdown. Focus engine (`focusScope`/`prefersDefaultFocus`/`@FocusState` restoration/`focusSection`), Siri Remote (`onMoveCommand`, `onPlayPauseCommand`, tap, long-press), Menu (`onExitCommand`) unwinding one layer at a time, 60 pt safe area.

## Stack / platform
Apple TV, tvOS 17, SwiftUI. Swift package-style tree at `project/` (`Package.swift`, `Sources/LumenTV/{App,Theme,Models,SignIn,Player,Components,Resources}`, `Tests/LumenTVTests`). 15 Swift files, ~900 lines. No Xcode on this machine: **render_mode = html-twin + static review**. The Swift was reviewed by hand against the guidance; two HTML twins (`render/signin.html`, `render/player.html`, shared `twin.css` mirroring `Theme/Tokens.swift`) were rendered with Playwright 1.63.0 / Chromium at 1920×1080 and driven with arrow keys (swipe/DPAD), Enter (select), Escape (Menu), Space (Play/Pause).

## Inspection verdict (`01-inspect.json`)
- Right: `Package.swift: Apple project` (KNOWN), `tvOS target` (KNOWN, from `.tvOS(.v17)`), stack `swiftui`, product hint `media`, "explicit focus handling in 5 files", "DPAD/remote/TV-focus handling in 4 files", "a11y attributes present in 4 files".
- Wrong: `platforms: ["mobile","tv"]` — the package targets tvOS only; `mobile` is added unconditionally for any Apple project. This single error cascades: requirements reports a platform CONFLICT and returns **AMBIGUOUS (exit 4)** for an unambiguous tvOS request.
- Missed: `tokens: []` (Theme/Tokens.swift with semantic `LumenColor`/`LumenFont`/`LumenSpace`), `icons: []` (SF Symbols via `systemName:` in 5 files), `component_dirs: []` (`Components/`), `tests: []` (`Tests/LumenTVTests`), `i18n: []` (`Localizable.xcstrings`), `package_manager: null` (SwiftPM manifest present), `fonts: []` (system font — acceptable).

## Requirements verdict (`02-requirements.json`, status AMBIGUOUS / exit 4)
| Field | Value | Verdict |
|---|---|---|
| mode | create | right (INFERRED default) |
| platform | tv (KNOWN "tvos") | right |
| input | remote (KNOWN via inspection) | right |
| product | media | right |
| screen | auth, player; subtype sign-in | right; "activation code" not captured as subtype detail |
| stack | swiftui | right |
| density | medium (INFERRED "implied by product media") | wrong for these two screens — a sign-in and a player are low-density; the inference keys on product, not screen |
| components | ["media"] | too coarse: "transport controls" and "subtitle picker" are both component records in the base (`comp-player-controls`, side sheet in `tv-player-controls`) but are not recognised as components from the request wording (vocabulary gap) |
| environment | large-display, shared-device | right |
| jobs | authentication | missing "watch/consume" for the player half |
| constraints | preserve_existing_system, performance_sensitive | right |
| accessibility | screen_reader, focus, reduced_motion, contrast | right |
| negative_constraints | [] | right |
| missing | brand | right |
| conflicts | platform tv vs project mobile | **false conflict** caused by the inspector; produces AMBIGUOUS on a clear request |
| not captured | "auto-hiding" (behavioural constraint), "activation code", "next episode" | requirements-miss |

## Guidance verdict (`03-guidance.md/json`, 3 core + 5 guardrails)
| Record | Verdict | Note |
|---|---|---|
| `comp-tv-sign-in` (core) | relevant | Prescribed exactly the built screen: 6–8 char code with no ambiguous glyphs, URL + QR, polled, alive waiting state, expiry + regenerate, system-keyboard fallback, first focus on the fallback button. Profile picker / PIN out of scope. |
| `comp-player-controls` (core) | relevant | Skip ±10, captions/audio selectors, labelled controls, captions follow system prefs. Its swiftui note ("use AVPlayerViewController, customise only if brand requires") is a sensible hedge but the brief demanded custom controls; the record has no guidance on how to do custom controls well on tvOS. |
| `dir-cinematic-media-tv` (core) | partial | Dark tinted canvas, transient controls, focus glow apply; backdrop home, side nav, rails, focus-revealed metadata do not exist in this task. |
| `tv-player-controls` (guardrail) | relevant | Media keys without overlay, select shows controls, LEFT/RIGHT seek in fixed steps, 3–5 s auto-hide, side sheets keep video visible. Wording issue: "never hide while a control is focused" — on tvOS something is *always* focused while the overlay is up, so read literally it forbids auto-hide; interpreted as "while adjusting / sheet open". |
| `anti-no-states` (guardrail) | relevant | Drove waiting/expired/error/approved states, buffering indicator, disabled "Get a new code" while requesting. |
| `a11y-tv-focus-always` (guardrail) | relevant | Deterministic initial focus, restoration on return, never colour-only. Caught the restore-on-reappear contract (see defect 6). |
| `tv-focus-performance` (guardrail) | partial | One-frame focus response applies; virtualised rails / backdrop debounce do not. |
| `tv-dpad-axes` (guardrail) | relevant | "Forms: one field per row, DOWN advances" shaped the device sign-in fallback; straight-path reachability checked in the interaction test. |

Relevant 6 · partial 2 · off-target 0. Filtered-out list (web/desktop/mobile records) was correct.

**Ranking misses** (present in the base, not selected; verified with `advise.py search`): `tv-back-behavior` (BACK unwinds one layer — the core Menu semantics of this task; scores 0.711 for a Menu query), `tv-safe-area` (0.874 for a safe-area query), `tv-typography-distance` (0.773), `a11y-reduced-motion` (0.719), `a11y-focus-visible`. Guidance itself printed "uncovered required concepts: tv.ten_foot_typography, tv.safe_margins" while records tagged for those concepts exist — a concept-tag/coverage mismatch. `layout-split-player` (top search hit, 0.737, and the richest player rule set) reached the direction's layout slot but not the guidance bundle.

**Knowledge gaps** (no record, needed for this task): next-episode / autoplay prompt (placement, countdown, cancel, Menu behaviour — search returned cards/side-nav/upsell anti-pattern); Siri Remote gesture model (click vs swipe vs long-press, Menu vs Back on the 2nd-gen remote — query routed to `mobile-gestures-discoverable` and returned AMBIGUOUS mobile+tv: vocabulary gap on "swipe"); activation-code specifics (which glyphs to exclude, chunking "H7K-M4Q", TTL, polling cadence); QR sizing/quiet zone/contrast at 3 m; layer exclusivity (transport row must not remain under a sheet or prompt — defect 1 below); focus-lift overflow at the *screen edge* (the base says reserve padding so neighbours are not clipped, not that a 490 pt button at the 60 pt guide lifts outside the overscan limit — defect 4); tvOS API footguns (`controlSize` unavailable on tvOS — defect 5); `tokens.py scale --platform tv --base 29` emits a caption of 18 (below its own 20 floor, and below the 23 pt tvOS caption) and a body of 28 (< 29 pt tvOS body) and warns about it — the TV scale generator does not know the tvOS floors.

## Direction verdict (`04-direction.md/json`)
Validation: `{"ok": true, "violations": []}`.
Slots that fit: layout `layout-split-player` (exactly this task), colour `color-dark-accent` (used: #0F1218 canvas, 92 % white text, amber accent for focus/primary only), motion `motion-focus-scale`, focus `focus-scale-glow` (ring + scale, selected ≠ focused implemented in the picker), icon `icon-filled-system` (SF Symbols filled, ≥34 pt), cta `cta-focus-selects` (≤5 actions in one row, first focus on Play/Pause).
Slots that do not fit the task (direction-invariant — chosen from platform+product regardless of the two screens requested): navigation `nav-tv-side` (there is no navigation in a sign-in + player flow), cards `card-poster-landscape`, metadata `metadata-focus-reveal`, imagery `imagery-immersive-backdrop` (used only as a subtle sign-in backdrop), typography `typography-condensed-display` (conflicts with `stacks/swiftui.md`, which says tvOS system styles are already correct; I used the system font — the direction's own alternative "Platform system font" scored 0.302). Density guidance text is web-flavoured ("8 px base, 40–48 px interactive heights, 16 px body on web/mobile") and wrong for TV. Ledger (KNOWN/INFERRED/MISSING) was accurate apart from the inherited `mobile` conflict.

## Static review of the Swift (no compiler available)
Reviewed every file against `platforms/tv.md` and `stacks/swiftui.md`. Confirmed present: `.focusScope` + `.prefersDefaultFocus` on every layer (sign-in fallback button, Play/Pause, current subtitle row, "Play next", email field); `@FocusState` restoration (`lastControlFocus`, route change back to `.fallback`); `.focusSection()` on action rows and picker columns; `.onExitCommand` per layer with `PlayerModel.handleMenu()` unwinding picker → prompt → controls → leave; `.onPlayPauseCommand` without showing the overlay; `.onMoveCommand` on the surface and scrubber (±10 s); `.onTapGesture`/`.onLongPressGesture` for Siri Remote click / long-press; 60 pt padding on all persistent UI, scrims bleed via `ignoresSafeArea`; type ≥ 29 pt body / 23 pt caption, weights ≥ regular; `accessibilityReduceMotion` drops scale and transitions but keeps the ring; VoiceOver labels/values/adjustable action on the scrubber, merged card semantics, `.isModal` on the sheet; captions map to `AVMediaSelection` (system caption styling preserved); unit test asserts the code alphabet excludes 0/O/1/I/L/2/Z/5/S/8/B.
Found and fixed: `.controlSize(.large)` (unavailable on tvOS) → `scaleEffect`; controls-reappear focus reset contradicting the documented restore contract; transport row rendered beneath the picker/prompt; audio column width; contrast ratios quoted in a comment before being computed (replaced with `tokens.py contrast` values: text 15.7:1, secondary 10.2:1, ring 18.8:1, accent 9.6:1, on-accent 9.6:1). Unverified without Xcode: focus-engine edge cases inside `focusSection` (e.g. LEFT from the sheet back to the dimmed player), `.isFocused` environment inside `ButtonStyle` on tvOS 17, actual AVPlayer media-selection behaviour, `while let self` loop compile on the target toolchain.

## First-render defects (numbered)
1. Transport row and time readout remained visible under the track-picker sheet ("Next episode" button half-covered by the sheet edge, "-27:52" showing through) and under the next-episode card (ghosting through the 96 % surface). Layer exclusivity missing in Swift (`overlay != .none`) and twin.
2. "English · Audio description" wrapped to two lines in the 420 px audio column, so the two picker columns' rows stopped aligning.
3. Sign-in instruction wrapped with an orphaned "this code." (max-width 820).
4. Focused primary button at the sign-in left edge lifted ~20 px past the 60 px guide (l ≈ 40–52) at scale 1.08; spinner rotation also measured outside the guide.
5. Static review: `ProgressView().controlSize(.large)` — API unavailable on tvOS.
6. Controls reappearing after a hide always reset focus to Play/Pause; the doc comment and `a11y-tv-focus-always` require restoring the last control (Swift + twin).
7. Tracks button summary read "English · English" once English subtitles were chosen (roles indistinguishable).
8. Interaction-test instrumentation bugs (not UI): transparent mid-transition `box-shadow` counted as a focus ring; scaled/rotated transforms counted as safe-area violations. Fixed by settling 160 ms and measuring resting geometry.
9. Regression during fix 4: the new `.btn.icon:focus` lift out-ranked the reduced-motion reset by specificity — caught by the reduced-motion check on the second run and fixed.

## Final defects (remaining)
1. Twin only: "Play next in  10" shows a visibly wide gap before the tabular-nums span (Swift builds one string; not present there).
2. Expired/error status line uses the same muted colour and 23 px glyph as the waiting state; differentiation relies on the icon and copy only (contrast is fine, semantics weak).
3. Twin QR is a deterministic stand-in pattern, not a scannable code (Swift uses `CIQRCodeGenerator`).
4. Not verifiable here: native focus-engine behaviour, focus latency, real panel contrast/bloom, VoiceOver — html-twin cannot stand in for the tvOS focus engine.

## Iterations
3.
1. First render + first interaction run: 35/45 pass. Visual pass found defects 1–4; run found 6 (real) and the cascade from it plus the two instrumentation bugs (8). Static review found 5.
2. Fixed 1, 2, 3, 5, 6, 8 in Swift and twins; added layer-exclusivity and column-alignment checks. 49/49 pass; noticed 7 in the output and re-measured the edge lift (4 still ~20 px over).
3. Fixed 4 (wide text buttons lift 1.04, icon buttons 1.08 — `LumenFocus.scaleWide`) and 7; added edge hard-limit checks (48 px) for sign-in and the picker's right column. Run 3a: 50/51 — the reduced-motion regression (9); fixed the media-query selector. Run 3b: 51/51.

## Interaction test summary (`05-interaction.json`, 51 checks, 51 pass)
Sign-in: initial focus on the primary action with a visible 4 px white ring; code "76CCMT" drawn from the unambiguous alphabet at 132 px; RIGHT/LEFT between the two actions, no focus loss at the ends or on DOWN; smallest text 23 px; resting layout inside the 60 px safe area; lifted focus inside the 48 px overscan limit; targets ≥ 88 px; reduced motion removes scale/transition and keeps the ring.
Player: starts with controls hidden and the invisible surface focused; any key shows controls with first focus on Play/Pause; straight-path RIGHT walk across the row (stays at the end), UP to scrubber, ±10 s seek, DOWN restores the last control; Menu with controls visible hides them (does not leave); select on the surface shows controls; still visible at 4 s, hidden at 5.5 s; input inside 5 s resets the timer; reappearing controls restore the last control; select on "Subtitles and audio" opens the side sheet with focus on the current subtitle; UP/DOWN within a column, LEFT/RIGHT between columns; select picks a track and the summary updates ("English subtitles · English audio"); auto-hide paused while the sheet is open; Menu closes the sheet and returns focus to the tracks button; transport row hidden beneath the sheet and the prompt; picker rows single-line and aligned; Menu with nothing on screen leaves the player; next-episode prompt focuses "Play next", Menu dismisses it and cancels the countdown; all layers inside the safe area; reduced motion honoured.

## Time spent (rough)
About 2 h: 35 min Swift project, 10 min skill scripts + reading their output, 35 min twins + Playwright scripts, 40 min render/inspect/fix loops and static review, 15 min write-up.

## Failure taxonomy tags
`requirements-miss`, `vocabulary-gap`, `ranking-miss`, `knowledge-gap`, `direction-invariant`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-helped`

Where the skill helped: `comp-tv-sign-in` and `tv-player-controls` are essentially the spec for the two screens (unambiguous glyphs, fallback default focus, expiry/regenerate, media keys without overlay, fixed-step seek, side sheet keeping video visible, 3–5 s auto-hide); `a11y-tv-focus-always` exposed the focus-restore contradiction; `anti-no-states` produced the waiting/expired/error/approved/buffering states; `tokens.py contrast` replaced guessed ratios; `platforms/tv.md` and `stacks/swiftui.md` supplied the 60 pt safe area, 29/23 pt floors, `focusScope`/`prefersDefaultFocus`/`onExitCommand` vocabulary. Where it did not: the inspector's `mobile` false positive turned a clear request AMBIGUOUS; the guidance bundle skipped the BACK, safe-area, typography and reduced-motion rules it has; the direction filled slots (side nav, cards, metadata reveal, condensed type) that have no place in a sign-in + player task; nothing covers the next-episode prompt or the Siri Remote gesture model.
