# p4-12 — results

## Task
"add a search screen to the tvOS documentary app that fits the existing sign-in and player styling"

## Project / stack / platform
`phase3-projects/p3-tvos-swiftui/project` — Apple TV, tvOS 17, SwiftUI (`Package.swift`, `Sources/LumenTV/{App,Theme,Components,Models,SignIn,Player,Resources}`). Existing UI (sign-in with activation code, custom player); new screen (Search) plus the minimal shell it needs (signed-in root had no navigation at all: `RootView` jumped straight into the player).

**Render mode: html-twin + static review.** No Xcode; the Swift was reviewed against `platforms/tv.md` and `stacks/swiftui.md`; a new twin `render/search.html` sharing the Phase 3 `twin.css` (extended with rail/card styles) was rendered with Playwright 1.63.0 at 1920×1080 and driven with arrows (swipe/DPAD), Enter (select), Escape (Menu). The twin's one-row scrolling keyboard stands in for the tvOS system keyboard that `.searchable` provides (with Siri dictation); the Swift does not draw a keyboard.

## Design-context table (detected vs actual)
| field | detected | status | actual (Theme/Tokens.swift, Components/TVButtonStyle.swift, SignInView, PlayerView) | correct? |
|---|---|---|---|---|
| navigation | unknown | UNKNOWN | none before this task (`RootView` switch signedOut/signedIn → player directly); Menu unwinds layers inside screens. "Unknown" is correct as a value but the inspector cannot tell "no navigation" from "not found" | partial |
| theme | dark-first | INFERRED | `.preferredColorScheme(.dark)` + `LumenColor` (canvas #0F1218, surface #1A1F29, raised #242B38, 92% white text, amber accent for focus/primary only) — explicit | yes (should be KNOWN) |
| surfaces | elevated ("weak signal: shadow 1") | INFERRED | flat tonal surfaces (surface / surfaceRaised steps); the only shadow is the focus glow under a lifted control | no |
| radius | medium (8) | INFERRED | `LumenFocus.cornerRadius = 16` continuous on every control, 24 on the next-episode card, 8 only on the scrubber | no |
| spacing | irregular [6] | UNKNOWN | `LumenSpace` named scale xs 8 / s 16 / m 24 / l 40 / xl 64, `safeArea 60` | no |
| typography | unknown | UNKNOWN | `LumenFont` system sizes display 76 / title 48 / headline 34 / body 29 / caption 23, monospaced 132 for the code; weights ≥ regular | no (`Font.system(size:weight:)` declarations are not read) |
| components | unknown | UNKNOWN | `TVButtonStyle` (primary / secondary / icon prominences: ring 4 pt + lift 1.08/1.04, glow), `QRCodeView`, `TransportControls`, `TrackPickerSheet`, `NextEpisodePrompt` | no |
| platforms | tv | KNOWN | tvOS only | yes (the Phase 3 `mobile` false positive is gone) |

What "fits the existing sign-in and player styling" resolved to from the code: LumenColor/LumenFont/LumenSpace, `TVButtonStyle` for every control (extended with a `.card` prominence so cards get the same ring + lift), 60 pt safe area, eyebrow caption with 2 pt tracking (as in the player header), surface tiles for text items (as in the track picker), Menu unwinding one layer (as in the player).

## Requirements verdict (`02-requirements.json`, CONFIDENT)
- scope UI_DESIGN, mode create, platform tv (from "tvos"), input remote, stack swiftui, product media — right.
- `screen = [auth, player, search]`, `jobs = [authentication, search]`, `primary_jobs` including "create auth" and "create player" — wrong: sign-in and player are the *existing* screens named as the styling reference; only `search` is to be created. Same failure shape as p4-11 ("existing … home" → create home).
- `screen_subtype = sign-in` — wrong for the same reason.
- `risk = medium` — unexplained; a search screen is low risk.
- `components = [media, search]` — right; `intent.existing = true`, `preserve_existing_system = true` — right; `intent.preserve = []` — should carry theme/components from "fits the existing".
- `change_budget = moderate` — acceptable (new screen + a shell).

## Guidance verdict (`03-guidance.md/json`; status PARTIAL; 8 records: 4 core + 4 guardrails; concepts 12/12, ≈1502 tokens, coverage/1k 7.99, purity 0.90; uncovered required concern: performance)
| record | role | verdict | note |
|---|---|---|---|
| `comp-tv-sign-in` | core | off-target | the sign-in exists; selected first (lexical 0.471) because the sentence names it as the reference. Its "secondary 'type here' fallback using the system keyboard" line is the one transferable sentence |
| `comp-player-controls` | core | off-target | the player exists and is not touched |
| `comp-search` | core | relevant | the spec for the task: "TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK", debounce, recent searches, empty-result guidance, result count announced; swiftui note (`.searchable` renders the system search screen) followed |
| `comp-mini-player` | core | off-target | selected "for required coverage: states, BACK, focus restoration, safe margins" — no mini player in the task |
| `tv-typography-distance` | guardrail | relevant | 29/23 pt floors kept on the new screen |
| `tv-dpad-axes` | guardrail | relevant | "Search lives at a predictable edge" → Search as the last top tab; straight paths keyboard → rails → tabs |
| `a11y-focus-visible` | guardrail | relevant | ring on every key, tile, card, tab; selected tab ≠ focused tab |
| `a11y-forms-errors` | guardrail | partial | a search field has no validation; "keep entered data" applied (query persists when the keyboard closes) |

Counts: relevant 4 · partial 1 · off-target 3. Uncovered required concern "performance" (nothing in the bundle on virtualised rails / debounced lookup; I used `LazyHStack` + 250 ms debounce from `comp-search` and the tv platform file).

Missing guidance and where it is missing:
1. **Ranking**: `search "<task sentence>" -k 12` does not contain `comp-search` at all (top: comp-tv-sign-in 0.673, comp-player-controls 0.554, comp-mini-player 0.515 …); the reference-styling words outrank the object to build. A focused query ("tvOS search screen system keyboard results rails focus returns to the field on Menu") ranks `comp-search` first at 0.748 → **ranking miss (candidate-retrieval)**; the requirements layer feeding auth/player as screens is the root (layer: requirements).
2. `tv-back-behavior` (Menu unwinds: results → keyboard → field → leave) not selected; needed for the Menu contract on the search screen → ranking miss (bundle-selection).
3. `tv-safe-area` not selected; a 1120 pt field lifting 1.04 leaves the 48 pt limit — the Phase 3 tvOS "wide control lift at the edge" gap, still absent from the base → knowledge gap.
4. No record for the **tvOS system keyboard geometry** (one scrolling row, letters + space/delete/done, DOWN leaves it into content, Menu closes it, dictation via the Siri button) — the twin had to be modelled from platform knowledge; `comp-search` says only "system keyboard or voice" → knowledge gap.
5. No record for **top tabs vs side nav by section count on tvOS** as an actionable rule for *adding* a first navigation to an app that had none; `platforms/tv.md` has it ("2–5 sections: top tabs"), the direction chose `nav-tv-side` → direction mismatch.
6. `layout-rails` / `comp-tv-rail` (ranks 4 and 9) not in the bundle although results-as-rails is the requested output → ranking miss.

## Direction verdict (`04-direction.md/json`, validation OK; preserved [surface, color]; changed [])
| slot | choice | status | verdict |
|---|---|---|---|
| navigation | nav-tv-side | new | wrong: two sections (Watch, Search) → tvOS `TabView` top tabs per the platform file; built top tabs |
| layout | layout-split-player | new | wrong: the task is a search screen (rails under a field); the player already exists |
| density | density-medium | new | web-unit text again |
| surface | elevated (preserved) | preserved | the detected value is wrong (flat tonal), so "preserve elevated" would have been wrong; kept the real surface language |
| cards | card-poster-landscape | new | fits (16:9 documentary stills, title below) |
| typography | typography-condensed-display | new | wrong: `LumenFont` is the system font and `stacks/swiftui.md` says tvOS system styles are right; runner-up "Platform system font" 0.414 was the correct pick |
| color | color-dark-accent (preserved) | preserved | right |
| motion / focus / cta | focus-scale, scale-glow, focus-selects | new | fit (and match `TVButtonStyle`) |
| imagery | immersive-backdrop | new | not for a search screen; sign-in's subtle backdrop is the only backdrop in the app |
| icon | icon-filled-system | new | fits (SF Symbols) |
| metadata | metadata-focus-reveal | new | not used; card titles are static below the art |

Unjustified changed slots: navigation, layout, typography, imagery (four). Direction was ignored except for cards/focus/motion.

## Implementation summary (before-copies in `before/`)
- `Models.swift` — `Series` gains `synopsis`/`topicIds`; new `Topic`, `SearchResults`; `SampleCatalogue` gains `topics`, `allSeries`, `allEpisodes` (12 episodes across 6 series) and `search(_:)` (case/diacritic-insensitive over titles, synopses, topics; ≥2 chars).
- `Search/SearchModel.swift` (new) — `@Observable`: `query` with a 250 ms debounced lookup, `phase` = idle / searching / results / empty, `recent` (max 6, `commit()` on submit or open), `announcement` for VoiceOver.
- `Search/SearchView.swift` (new) — `NavigationStack` + `.searchable(prompt: "Titles, topics, places")` (system keyboard + dictation), `.onSubmit(of: .search)` commits; `SearchResultsView` renders idle (Recent searches + Browse topics tile rails), results ("N results for …" caption, Series and Episodes `CardRail`s of 400×225 art with eyebrow + title + subtitle, Topics tile rail), empty (guidance + Browse topics, never a dead end); `AccessibilityNotification.Announcement` for the count; rails are `ScrollView(.horizontal)` + `LazyHStack` + `.scrollTargetLayout()/.viewAligned` + `.scrollClipDisabled()` + `.focusSection()`; SELECT on a series/episode presents `PlayerView` full screen.
- `Components/TVButtonStyle.swift` — `.card` prominence (`.tvCard`): ring around the artwork only, no padding/background, lift 1.04 (wide) so an edge card stays inside the 48 pt limit.
- `App/LumenApp.swift` — signed-in root is `CatalogueShell` (`TabView`: Watch, Search); `ContinueWatchingView` keeps the previous "straight to the player" behaviour as one primary card.
- `README.md` — Search flow documented.
- Twin: `render/twin.css` (+ `.rail`, `.card`, placeholder art, reduced-motion additions), `render/search.html` (new; tab bar, field with hint, scrolling keyboard stand-in, rails, states, live region, focus engine); scripts `render/shoot-p4-12.js`, `render/interaction-p4-12.js`.

## First-render defects by type (`first-*.png`, `05-interaction-first.json` 29/31)
1. **visual** — the hint caption under the field touched the content below it (results headings, "No results", the keyboard row) with no gap (`first-search-idle-recent.png`, `first-search-keyboard-typing.png`).
2. **platform** — the one-row keyboard overflowed the right edge: DELETE clipped, DONE off-screen and unreachable visually (`first-search-keyboard-typing.png`); the system keyboard scrolls.
3. **interaction** — UP from the field entered the tab bar on Watch (first item) instead of the selected Search tab.
4. **platform** — the focused 1120 px field lifted 1.04 to x≈37, outside the 48 px overscan limit (seen in `first-search-results-field.png`, not caught by the first test).
5. **implementation-bug** (harness) — safe-area check measured rail headings as full-width blocks.
Totals: visual 1 · interaction 1 · accessibility 0 · platform 2 · existing-system-mismatch 0 · implementation-bug 1.

## Final defects by type (`final-*.png`, `05-interaction-final.json` 33/33; Phase 3 tvOS suite 51/51)
visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
Remaining, not counted: twin keyboard geometry is an approximation of the system keyboard; the Swift `.searchable` result area cannot be visually verified here (system chrome); `TVButtonStyle.card` ring frame (225 pt) is coupled to the card art height; Swift never compiled (`.scrollClipDisabled`, `AccessibilityNotification.Announcement`, `.onSubmit(of: .search)` on tvOS 17 believed available). Phase 3 tvOS suite shows a pre-existing timing flake on "signin: initial focus visible (ring)" (mid-transition 3.99 px value; 1 of 4 runs).

## Iterations
3 (first render; fixes 1–3 + harness; field lift fix after the visual pass).

## Interaction test summary (`05-interaction-final.json`, 33 checks)
Field: initial focus with a visible ring, lifted field inside the 48 px limit, hint names both entry paths (select to type / Siri to dictate). **System keyboard fallback reachable**: SELECT opens it with the first key focused; LEFT/RIGHT walk the row; the row scrolls so every key including DONE is on screen and inside the overscan limit; typing "deep" updates the field and, after the debounce, the results; count announced in a polite live region. **Results as rails**: Series / Episodes / Topics; cards are 16:9 with the title below. **Arrows reach every result**: DOWN from the keyboard enters the first rail; RIGHT across each rail and DOWN between rails reach all 17 focusables; **focus visible** (ring) on every one and always fully on screen; lifted item inside the 48 px limit; UP returns to the keyboard. Menu unwinds one layer: results → keyboard → (closes keyboard) field → leave; with the keyboard closed, DOWN from the field enters results and Menu returns to the field. Tab bar: UP from the field lands on the selected Search tab (aria-selected distinct from focus), LEFT reaches Watch. SELECT on an episode plays it and stores the recent query. Empty state has guidance and a focusable Browse topics rail; SELECT on a topic runs that search; idle shows Recent searches + Browse topics. Smallest text 23 px; persistent UI inside the 60 px safe area; first card at the safe margin; reduced motion drops lifts and keeps rings; no `:hover`.

## Preservation verdict
Tokens, type scale, `TVButtonStyle` focus language, 60 pt safe area, Menu semantics and the sign-in and player screens are untouched (sign-in/player twins unchanged; Phase 3 suite 51/51). Structural change: the signed-in root gained a two-tab shell so Search has an entry point and "Watch" keeps the old path — justified (the task cannot exist without an entry point; two sections → top tabs per the platform file). Unjustified structural changes: 0. `preservation-ok`.

## Regressions to propose
- query: "add a search screen to the tvOS documentary app that fits the existing sign-in and player styling" → expect `screen = [search]`, jobs = [search], `intent.preserve` ⊇ [theme, components]; `comp-search` first in search and in the bundle core; `comp-tv-sign-in`/`comp-player-controls`/`comp-mini-player` absent; `tv-back-behavior`, `layout-rails` present; direction navigation = top tabs (2 sections), typography = system font, layout ≠ split-player.
- query: "which navigation for a tvOS app with two sections" → expect top tabs (TabView), not nav-tv-side.
- query: "tvOS search: what happens to focus when Menu is pressed in the results" → expect results → keyboard/field → leave.
- inspect: SwiftUI project with `Font.system(size:)` enums, a `LumenSpace`-style enum and `cornerRadius: 16` everywhere → expect typography KNOWN, spacing KNOWN, radius "large/16", surfaces "flat".

## Tags
`preservation-ok`, `skill-helped` (comp-search was the spec; tv-dpad-axes placed Search at the edge; tv platform file's "2–5 sections → top tabs", 60 pt, 29/23 pt floors, `.searchable`/`focusSection`/`scrollClipDisabled` vocabulary from the stack file), `requirements-miss` (auth/player as creation targets; preserve list empty; risk medium), `context-detection-miss` (surfaces, radius, spacing, typography, components all wrong or unknown), `direction-mismatch` (nav-tv-side, split-player, condensed type, immersive backdrop), `ranking-miss` (comp-search absent from top-12 for the sentence; tv-back-behavior, layout-rails, tv-safe-area not selected; three off-target cores), `knowledge-gap` (tvOS system keyboard model; wide-control lift at the edge), `render-defect-fixed` (5), `tooling-limit` (no Xcode; system search chrome not renderable in a twin).


## Addendum — knowledge-base drift during the run
The skill's data files (`data/rules.jsonl`, `patterns.jsonl`, `components.jsonl`, `lexicon.json`, eval fixtures) were modified between 12:23 and 12:57 by another process, not by this run (no write of this run touched `design-engineering/`). All `01`–`04` files above were produced at 12:20–12:21 against the earlier base; `02-requirements-rerun-1303.json` and `03-guidance-rerun-1303.json` were produced at 13:03 against the modified base. Diff: No change: guidance ids identical (three off-target cores remain), requirements identical (auth/player still parsed as creation targets).
