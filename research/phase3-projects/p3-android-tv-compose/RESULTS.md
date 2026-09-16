# p3-android-tv-compose — results

## Task
"Android TV live sports app home with rails, EPG entry and a mini player for the family TV, Compose"

Built from a copy of `evals/fixtures/compose-tv` (`project/`): live-sports home (immersive hero that follows the focused live tile, "Live now" rail with broadcast progress, "Coming up" rail led by an EPG entry tile, Catch up / Football / Motorsport rails, mini player docked in the hero band, collapsible side navigation), an event details screen, player/guide placeholders, app-level focus memory, BACK layering, safe margins, dark TV tokens. 1 290 lines of Kotlin across 9 files plus `design/tokens.json`.

## Stack / platform
Android TV, Jetpack Compose for TV (`androidx.tv:tv-material 1.0.0`, Compose UI/Foundation 1.8.0, Media3, Coil). Rails use `LazyRow` + `Modifier.focusRestorer()` + `LocalBringIntoViewSpec` per the skill's compose-tv guidance; the task sentence said `TvLazyRow`, the stack file says it is deprecated, so I followed the skill and noted it in `HomeRail.kt`.

**Render mode: html-twin + static review.** No gradle wrapper / Android SDK, so the Kotlin was reviewed statically against `platforms/tv.md` and `stacks/compose-tv.md`, and an HTML twin (`render/twin.html`, 1 dp = 2 px, 1920×1080) reproduces the layout, focus scale/ring/glow, safe margins, 10-foot type and the Compose focus semantics (row/column D-pad, focusRestorer memory, pivot scroll, BACK layering). Playwright 1.63.0 drove screenshots and the D-pad test. The Kotlin did not compile anywhere; tv-material API signatures were checked from knowledge, not by a compiler.

## Inspection verdict (`01-inspect.json`, re-run after implementation in `01b-inspect-after-impl.json`)
- Right (KNOWN): compose, tv-material, media3, coil from `build.gradle.kts`; leanback launcher from the manifest. INFERRED "touchscreen not required" right. After implementation: "a11y attributes present in 4 files", "explicit focus handling in 5 files" right.
- Wrong: INFERRED "both mobile and TV Android targets; check product flavors" → `platforms: [mobile, tv]`. The manifest has `leanback required=true`, `touchscreen required=false`, and there are no flavors; this is a TV-only project. This single false positive made `requirements`, `guidance` and `direction` all exit 4 AMBIGUOUS.
- Wrong: `routing: ["app/ (next-app-router or nuxt app dir)"]` — the Android `app/` module was read as a Next.js/Nuxt app directory.
- Missed: `design/tokens.json` (semantic-role tokens in the skill's own `tokens.py init` shape) is not detected as a token file even after it exists; `component_dirs` empty although `ui/home`, `ui/details`, `ui/theme` exist; "DPAD/remote/TV-focus handling in 3 files" on a fixture with one Kotlin file (the count includes README/manifest matches).

## Requirements verdict (`02-requirements.json`, exit 4)
| field | value | verdict |
|---|---|---|
| mode | create (INFERRED) | right |
| platform | tv (KNOWN) | right; but `conflicts: platform request tv vs project mobile` is wrong (inspector false positive) and is the only reason for status AMBIGUOUS |
| input | remote (KNOWN, from project) | right |
| product | media | right but thin: "live sports" not captured; no sport/live sub-signal anywhere |
| screen | home, list, player | home right; `list` for "EPG" is a stretch (EPG is a guide/grid; `screen_subtype: epg` is the useful part); `player` right for the mini player but the mini-player concept itself is not represented (vocabulary gap) |
| screen_subtype | epg, rails | right |
| stack | compose, compose-tv | right |
| density | medium (INFERRED "implied by product media") | acceptable default |
| components | [media] | missing: rails, hero, epg tile, mini player, side nav |
| environment | large-display, shared-device | right (family TV → shared device) |
| jobs / problems | [] | missing: "browse live", "resume watching while browsing" would be derivable from "live" + "mini player" |
| accessibility | screen_reader, focus, reduced_motion, contrast all true | right |
| constraints | preserve_existing_system, performance_sensitive | right |
| missing | brand | right |

Requirements errors recorded: platform conflict from inspector; mini player/PiP not a known concept; sports/live not captured; components list too thin; `list` for EPG.

## Guidance verdict (`03-guidance.md/json`, 8 records: 3 core + 5 guardrails)
| record | verdict | note |
|---|---|---|
| comp-player-controls (core) | partial | full transport overlay guidance; the task needs a mini player state on the home. Only the Media3/focusRequester note helped for the expand-to-player route |
| dir-broadcast-guide-tv (core) | partial | its identity (flat tonal guide surfaces, condensed titles, tabular times, live badges, mini player while browsing, border+scale focus) shaped the EPG tile and card treatment; but it prescribes top tabs and is declared incompatible with `layout-immersive-rails` and `surface-imagery-backed`, which the task asks for (immersive hero) and which the direction command itself selected. Core guidance and direction slots contradict each other |
| comp-epg (core) | partial | full-grid guidance; now/next, channel number, current-programme highlight transferred to the entry tile; the rest is for the Guide screen |
| anti-no-states (guardrail) | relevant | drove `HomeUiState` Loading/Error/Empty/Ready and `MiniPlayerState` Hidden/Playing/Paused/Buffering |
| a11y-tv-focus-always (guardrail) | relevant | drove deterministic first focus, `HomeFocusMemory`, restoration after Details/Player, focusable action in every status pane |
| tv-focus-performance (guardrail) | relevant | debounced backdrop, stable keys, hoisted focus state, one LazyListState per rail |
| tv-typography-distance (guardrail) | relevant | type scale built with `tokens.py scale --platform tv` (caption raised to the 20 sp floor) |
| tv-safe-area (guardrail) | relevant | exposed first-render defect 2 (nav strip inside the overscan margin) and fixed it |

Counts: relevant 5, partial 3, off-target 0.

Knowledge gaps (needed, absent from the base):
1. Mini player / PiP-while-browsing as a home component: where it sits in the focus graph, its states, how BACK from the full player returns to it.
2. Live-sports card content: score + match clock + broadcast progress layout on a 16:9 card (`card-poster-landscape` covers the progress bar only); long score strings (tennis sets) squeezing the channel label.
3. Fixed-height hero band so rails never jump when the hero follows focus (`layout-immersive-rails` and `metadata-focus-reveal` imply it, neither states it).
4. Side navigation vs overscan margin: `nav-tv-side` never says the collapsed icon strip must itself carry the 48 dp margin; `tv-safe-area` says persistent UI stays inside. Reconciling them cost an iteration.
5. `NavigationDrawer` (pushes content, reflows the hero) vs `ModalNavigationDrawer` (overlay) — the compose-tv stack file lists both without a recommendation for a rails home.
6. Cross-screen focus restoration on lazy lists: `FocusRequester.requestFocus()` throws when the tile is not composed; you must `scrollToItem` the column and the rail first, wait a frame, then request. The stack file only says "focusRestorer on every LazyRow".
7. Nested `BackHandler` ordering (the innermost enabled handler wins), needed for drawer-exit vs rails-to-hero.

Ranking misses (present in the base, not selected; `03-search-k12.txt`):
- `tv-back-behavior` is in the base (search rank 10) yet guidance reported "uncovered required concepts: interaction.back_semantics".
- `layout-immersive-rails` (search rank 5) not in guidance core although the request is an immersive-hero home; `layout-rails` was chosen by direction instead.
- `card-poster-landscape` (rank 9, progress bar for live/continue-watching) not in guidance.
- `nav-tv-side` (rank 6) selected by direction but absent from guidance.
- `tv-no-touch-hover` (rank 12) would have been a cheap guardrail for a home with a mini player.

## Direction verdict (`04-direction.md/json`)
Validation: `ok: true, violations: []`. Slots:
- navigation `nav-tv-side` — fits; implemented as a modal (overlay) drawer.
- layout `layout-rails` — the request says immersive hero; `layout-immersive-rails` was the runner-up (0.616) and is what was built. Wrong pick for this request.
- density `density-medium` — slot text is web/mobile ("8 px base, 40–48 px interactive heights, 16 px body"), unusable on TV as written (direction-invariant: same text regardless of platform).
- surface `surface-imagery-backed` — fits the hero; contradicts the guidance core `dir-broadcast-guide-tv` (declared incompatible).
- cards `card-poster-landscape` — fits.
- typography `typography-condensed-display` — fits; not visually verified (twin has no condensed webfont).
- color `color-neutral-accent` with reason "product mismatch" — on TV the platform file says dark-first; `color-dark-accent` (0.365) should have won. Built dark-first anyway.
- motion `motion-focus-scale`, focus `focus-scale-glow`, cta `cta-focus-selects`, imagery `imagery-immersive-backdrop`, icon `icon-filled-system`, metadata `metadata-focus-reveal` — all fit.
Fingerprint plausible. Slot guidance for focus/motion/imagery was directly actionable (padding for scale overflow, debounce 300 ms, dual scrim).

## First-render defects (numbered)
1. Hero band overflowed upward: meta line and title clipped above the safe area (content taller than the 240 dp band; `first-home-initial.png`). Twin and Kotlin.
2. Side-nav icon strip inside the 5% overscan margin (icons 12 dp from the edge; `first-home-safe-overlay.png`, test failure). Twin and Kotlin.
3. Expanding the drawer pushed and reflowed the hero and rails (title rewrapped and clipped; `first-home-nav-open.png`). Twin and Kotlin (`NavigationDrawer` → `ModalNavigationDrawer`).
4. Card bottom row: channel name collapsed to "Sp…", "C…" when score + clock were long (tennis; `first-home-live-rail.png`). Twin and Kotlin.
5. Details screen rendered over a still-visible home; its text hid behind the drawer (`first-details.png`; CSS specificity bug). Twin only.
6. Fast D-pad input made the browser natively scroll the `overflow:hidden` content container, throwing a whole rail off-screen (`first-home-deep-rail.png` is nearly empty; 4 "focused element off screen" failures). Twin only (`focus({preventScroll:true})`); Compose unaffected.
7. Static review, Kotlin only: the home `BackHandler(enabled = true)` would shadow the drawer's exit handler (innermost enabled handler wins), so BACK on the drawer would never exit.
8. Static review, Kotlin only: focus restoration called `requestFocus()` on requesters of lazily composed tiles without scrolling them into composition first (throws / silently fails when the tile is off-screen).
9. Static review, Kotlin only: no reduced-motion path (`ANIMATOR_DURATION_SCALE`) for the backdrop crossfade and the focus scale.
10. Test harness: the safe-margin check measured block boxes for headings (false positives on `h2` spanning the row).

## Final defects (remaining)
1. A rail keeps its horizontal scroll memory after BACK-to-hero, so the Live rail's first card can sit partly under the content edge while the hero is focused (`final-home-after-back.png`). Compose `LazyRow` behaves the same; visible but arguably correct.
2. EPG entry tile: now/next columns truncate heavily at 412 dp × 20 sp ("Arsenal v Live…", "11:30 Real M…"; `final-home-epg-tile.png`). Needs a wider tile or a single now-only column.
3. Mini player title truncates at 240 dp ("Singapore Grand …").
4. Twin fidelity: gradient placeholder art, no condensed webfont, no real video; the condensed-display typography and the scrim-over-real-artwork contrast are unverified.
5. Kotlin never compiled; tv-material 1.0.0 signatures (`ModalNavigationDrawer`, `ClickableSurfaceDefaults`, `CardDefaults.glow`, `BringIntoViewSpec`) are believed correct but unverified.

## Iterations
- Iteration 1 (first render + D-pad test): 21/23 checks; defects 1–6 and 10 found.
- Iteration 2 (fix and re-render): hero band 288 dp with 1-line title, drawer carries the 48 dp margin and overlays content, card row reorganised (clock left, score right, channel to subtitle), twin visibility/scroll bugs, test timing and measurement fixes; 23/23 checks, screenshots `final-*.png`.
- Iteration 3 (static review of the Kotlin, no re-render needed): BackHandler gating (`backEnabled = !navHasFocus`), lazy-aware restoration (scroll column + rail, `awaitFrame`, guarded `requestFocus`, hero fallback), `LocalReducedMotion` from `ANIMATOR_DURATION_SCALE`, mini-player content description.

## Interaction test summary (`05-interaction.json` = final run; `05-interaction-first.json` kept)
23 checks on the twin at 1920×1080 with arrow keys / Enter / Backspace+Escape: deterministic initial focus; every home focusable reachable by straight D-pad paths (25 targets, 0 unreached); focus always visible (3 px white ring + accent glow + scale) and on screen; LEFT from a rail's first item enters the drawer, RIGHT from the drawer restores the last content focus; SELECT on a tile opens details with first focus on Watch; BACK from details restores focus to the opening tile; per-rail focus memory on UP/DOWN; BACK from a rail returns to the hero and scrolls to top; BACK from the hero goes to the drawer; BACK from the drawer exits; mini player reachable (RIGHT from Details), expands, BACK returns to it, DOWN lands in the Live rail; EPG tile opens the guide and BACK restores it; zero `:hover` rules; smallest visible text 40 px (20 sp caption floor), all ≥ 24 px; persistent UI inside the 96/54 px safe frame; reduced motion removes the scale animation and transitions while the ring stays; focus scale stays within the reserved padding. First run 21/23, final 23/23.

## Tokens
`design/tokens.json` (dark theme only, TV): `tokens.py validate --platform tv` first FAIL (strong border 2.74:1), fixed to #66799A (4.25:1) → OK, 1 warning (default border 1.48:1, advisory) — `06-tokens-validate.txt`. Note: the protocol says `tokens.py check`; the tool only has `validate`.

## Time spent (rough)
About 2 hours: 25 min skill/protocol reading and CLI runs, 45 min Kotlin, 35 min twin + Playwright scripts, 25 min two render/test iterations and static review, 10 min write-up.

## Failure taxonomy tags
`requirements-miss` (platform conflict from inspector; mini player, live sports, components not captured) · `vocabulary-gap` (mini player / PiP; "immersive" not steering the layout slot) · `ranking-miss` (tv-back-behavior reported uncovered; layout-immersive-rails, card-poster-landscape, nav-tv-side not in guidance) · `knowledge-gap` (7 items above) · `direction-invariant` (density slot text in web units on TV; colour slot ignores the dark-first TV rule) · `render-defect-fixed` (10) · `render-defect-remaining` (5) · `tooling-limit` (no Android build; `tokens.py check` does not exist; inspector misreads Android `app/` as Next.js) · `skill-helped` (TV platform + compose-tv files gave the focus/safe-area/typography/BACK rules that shaped the code; the safe-area guardrail and `tokens.py` caught two real defects; the deprecation note steered away from `TvLazyRow`).
