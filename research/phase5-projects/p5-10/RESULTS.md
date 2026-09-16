# p5-10 — subtitles and audio language chooser in the player (Android TV, Compose for TV)

**Task (verbatim):** "Add a subtitles and audio language chooser to the player."
**Project:** `research/phase3-projects/p3-android-tv-compose/project` — Kotlin, Jetpack Compose 1.8 + androidx.tv tv-material 1.0, Media3, Coil. Platform: tv. Existing app; the player was a placeholder (`FullPlayerPlaceholder` in `SportsApp.kt`: "Media3 PlayerView + transport overlay live here in the real app"), so the task is a **new feature on an existing codebase**: a player screen with a transport overlay had to exist for the chooser to hang off. p5-09's rail hold pacing (`consumeFastDpadRepeat`, `rememberRailPivotSpec`) was not touched.
**Build hash:** start `bf034323…f0d8` = end `bf034323…f0d8` (skill untouched).
**Render mode:** html-twin (the Phase 3 twin at `p3-android-tv-compose/render/twin.html`, extended with the player + sheet, 1920×1080, Playwright 1.63 / Chromium) + static Kotlin review. No Android toolchain: the Kotlin was not compiled; tv-material `ListItem`/`ListItemDefaults` usage is from API knowledge and is the main compile risk.

## Design-context table (`01-inspect.json` vs code)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | tv-rails | KNOWN | collapsible left drawer (`ModalNavigationDrawer`) + immersive hero + horizontal rails; direction resolves it to `nav-tv-side` | yes |
| theme | dark-first | KNOWN | `darkColorScheme` only; dark tokens only | yes |
| surfaces | bordered-flat | INFERRED | flat tonal surfaces; "borders" are the 3 dp white focus ring and one 1 dp outline on the EPG tile | partial |
| radius | medium (8) | INFERRED | 8 dp cards, 4 dp pills, 50 % buttons | yes |
| spacing | 8 | INFERRED | 8-dp family | yes |
| typography | unknown | UNKNOWN | explicit `SportsTypography` 10-foot scale 20–74 sp on `FontFamily.SansSerif` with documented condensed-display intent; `type_scale: true` detected | partial |
| components | compose, compose-tv-material, media3, coil | KNOWN | same | yes |
| tokens | [] | — | `design/tokens.json` exists and is referenced by README + theme | no |

Same picture as p5-09 (same inspector, same repo).

## Requirements verdict (`02-requirements.json`)
- platform `tv` — correct (project inspection; `platform_evidence` empty but `known` lists the leanback launcher). input `remote` correct.
- artifact_state `existing` — correct. operations `create` — correct. problem_domain `[]` — acceptable (a feature request has no defect). change_scope `screen` — correct (a component on one screen).
- mode `create` ("build/create request on an existing surface") — **correct** (expected create; refactor acceptable).
- scope `in-scope`, domain `UI_DESIGN`, reason "UI design / interaction task"; `scope_evidence.ui` includes `concept:media.track_selection` — correct.
- change_budget `moderate` — right for a new screen + sheet. `constraints.preserve_existing_system: true` — good.
- `intent.preserve` `[]` — miss (same as p5-09): an existing repo with KNOWN navigation/theme should list them.
- accessibility flags all true — fine. risk `low` — arguable for a modal-ish sheet on TV, harmless.
- status CONFIDENT; missing: "brand" — noise for a feature on an existing themed app.

## Guidance verdict (`03-guidance.md/json`, 8 records, ≈1408 tokens)
| record | role | verdict | note |
|---|---|---|---|
| comp-player-controls | core | relevant | captions + audio track selectors, every control labelled, overlay auto-hides except while focused; the compose-tv note (Media3 + Compose overlay, focusRequester on play/pause) is exactly what was built |
| layout-split-player | core | relevant | "subtitles and audio selection in a side sheet that pauses the auto-hide", first focus on play/pause, seek with a text readout — followed literally |
| comp-mini-player | core | partial | selected only to cover states / focus_restore / back; the mini player already exists in the codebase. Its "BACK from the full player returns to the mini state with focus restored" matched the existing contract, nothing else applied (**generic**) |
| tv-player-controls | guardrail | relevant | media keys without the overlay, DPAD_CENTER shows controls, 3–5 s auto-hide, "subtitle/audio pickers are side sheets that keep playback visible" |
| tv-typography-distance | guardrail | partial | caption floor 20 sp applied to the track detail line; otherwise generic |
| a11y-focus-visible | guardrail | partial | ring ≥3:1 applied; generic |
| tv-dpad-axes | guardrail | relevant | "every focusable element reachable with straight presses" is what caught the disabled Go-to-live button (see defects); LEFT/RIGHT between the two columns, UP/DOWN inside |
| tv-focus-performance | guardrail | off-target | virtualisation, image sizing, "never coalesce key events" — nothing to do with a track chooser; carries `table.virtualization`, which is a forbidden concept for this task (**generic**) |

Counts: relevant 4 · partial 3 · off-target 1. The skill's own purity 0.84 / coverage 1.0 again measure coverage of its own demand, not task fit. Reporting bug: the explain output says "Omitted (redundant): comp-mini-player" while comp-mini-player is in core.

**Concept recall** (expected from `00-expectation.json`; delivered = union of `concepts` over the 8 selected records = tv.player_autohide, a11y.accessible_names, media.track_selection, interaction.focus_restore, interaction.back_semantics, state.loading_empty_error, tv.safe_margins, media.live_channel_switching, tv.ten_foot_typography, interaction.focus_visible, interaction.dpad_reachability, perf.focus_latency, table.virtualization, perf.image_sizing):
| expected | delivered? | layer if missing |
|---|---|---|
| media.track_selection (critical) | yes (tv-player-controls, comp-player-controls) | — |
| interaction.selection_visible (critical) | **no** | expected-concepts — never demanded for a chooser/radio list; the base carries it (color-states-complete, a11y-color-not-only, comp-data-table, grid-single-tab-stop) but no candidate was ever requested. The direction's focus-slot text ("selected ≠ focused") is the only place it surfaced |
| interaction.back_semantics (critical) | yes (tv-player-controls, comp-mini-player) | — |
| a11y.dialog_focus | **no** | expected-concepts — never demanded although the sentence asks for a chooser (a sheet). Note also a platform gap: `a11y-modal-dialog` (the rule that carries it) is platform `web/desktop/mobile`, so it can never be selected for tv; only `comp-dialog` (platform any, with "TV: side sheet… focusRequester" notes) could carry it |
| interaction.dpad_reachability | yes (tv-dpad-axes) | — |
| tv.player_autohide | yes (3 records) | — |
| interaction.focus_visible | yes (a11y-focus-visible) | — |

Recall 5/7 = 0.71 · critical 2/3 = 0.67 · forbidden delivered: `table.virtualization` (via tv-focus-performance). `state.loading_empty_error` was demanded ("asynchronous or remote data on this screen") and marked covered by comp-mini-player — a record about a different component; the one empty state that matters here (a stream with no subtitle tracks) came from nowhere in the bundle.

`search -k 12` (`03-search-k12.txt`): the top three are the same player records; nothing about radio/selection lists, side sheets as a component, or focus return on close. Without a project file the search reports platform MISSING and drifts to web font loading and bottom tabs — search alone is not usable for TV without `--project`.

## Direction verdict (`04-direction.md/json`)
13 slots: preserved 3 (navigation `nav-tv-side`, surface, color) · changed 0 · new 10. `validation.ok = true`. Preserved slots right. Of the "new — no repository evidence" slots: `layout-split-player` is the right layout for the task; `card-poster-landscape` matches the 16:9 cards this time (p5-09 got portrait) but is irrelevant to a player chooser; `typography-system-native` matches `FontFamily.SansSerif` but ignores the documented condensed-display intent (partial); motion / focus / cta / imagery describe what the code already does and are labelled "no repository evidence" (context-detection weakness, as in p5-09). Two slots contradict the codebase and were ignored: `icon-custom-glyphs` (the app uses material-icons-core), `metadata-focus-reveal` (cards show title + subtitle always). `density-medium` is a default. The focus slot's "selected ≠ focused (a selected tab still needs a focus treatment)" and "initial focus is deterministic on every screen" were used.

## Implementation
Files changed (before-copies under `before/`; `PlayerScreen.kt` is new):
- `app/src/main/java/com/example/tv/data/SportsCatalog.kt` — `TrackKind`, `MediaTrack(id, kind, language, label, detail)`, `TrackList`, `TrackSelection`; `SampleCatalog.tracksFor(event)` (football: 5 subtitle + 4 audio incl. audio description and stadium-only; motorsport: team radio; one replay with no subtitles so the "Off only" state is reachable).
- `app/src/main/java/com/example/tv/ui/AppState.kt` — `PlaybackPrefs`: remembered by language + label/detail flavour (ids are per stream), `selectionFor(tracks)` resolves against what a stream carries, falls back to the first audio track.
- `app/src/main/java/com/example/tv/ui/theme/SportsTheme.kt` — `SportsDimens.playerAutoHideMs = 4000`, `playerSeekStepSec = 10`, `trackSheetW = 600.dp`, `trackRowH = 56.dp`.
- `app/src/main/java/com/example/tv/ui/player/PlayerScreen.kt` (new) — `PlayerScreen`: picture (Media3 PlayerView slot, poster stands in), `TransportOverlay` (LIVE badge + meta + title + score top-left; focusable `SeekBar` with text readout and LEFT/RIGHT ±10 s; control row Pause/Play · −10 s · Go to live | +10 s · **Subtitles & audio** · current-choice summary text), `TrackSheet` (600 dp right sheet, two `focusRestorer` columns of tv-material `ListItem` rows: selected = `selectionBg` fill + accent check + `Role.RadioButton`/`selected`/"Selected" semantics; focused = 3 dp white ring, no scale in the list; default focus on the current subtitle row; "Off" row; "This broadcast has no subtitles." when empty; SELECT applies immediately and keeps the sheet open). Auto-hide 4 s, never while paused or the sheet is open; any key reveals the overlay and is consumed; MEDIA_PLAY_PAUSE toggles without the overlay (pausing shows it). BACK: sheet → close and focus returns to the opener; otherwise leave the player (existing contract).
- `app/src/main/java/com/example/tv/ui/SportsApp.kt` — `PlayerScreen` wired in place of `FullPlayerPlaceholder`; `PlaybackPrefs` remembered at app level; BACK-layering doc updated.
- `render/twin.html` (case-level, edited via `p5-10/render/twin.html` and written back) — player screen, overlay, sheet, `PlaybackPrefs`, `tracksFor`, key handling mirroring the Kotlin; `__twin.PLAYER_AUTOHIDE.ms` exposed for the render script.
- `p5-10/render/render-player.js` (new) — 31-check D-pad walk-through with screenshots; `render.js` and `interaction.js` copied from the Phase 3 / p5-09 suites for regression.

Guidance used: comp-player-controls (labelled track selectors, overlay auto-hide, compose-tv note), layout-split-player (side sheet pauses auto-hide, first focus play/pause, text readout), tv-player-controls (media keys, DPAD_CENTER shows controls, 3–5 s, side sheet keeps playback visible), tv-dpad-axes (drove the Go-to-live reachability fix), direction focus slot (selected ≠ focused, deterministic first focus), tv-typography-distance (20 sp caption floor for the detail line). Ignored: comp-mini-player (already in the codebase), tv-focus-performance (irrelevant), icon-custom-glyphs and metadata-focus-reveal (contradict the codebase). Not in the bundle and supplied from own knowledge: selected-state treatment distinct from focus, focus return to the invoker on close, remembering the preference per language/flavour across streams, the no-subtitles empty state, the always-visible "Subtitles off · English 5.1 surround" summary next to the control, keeping "Go to live" focusable at the live edge.

Decision against a plausible alternative: BACK with the overlay showing hides the overlay first on YouTube/Leanback, but the app documents "player → home" and the Phase 3 interaction suite asserts one BACK from the player; the existing contract was kept (sheet → player → home) and the overlay is only dismissed by the timer.

## Render (1920×1080)
`render-player.js`: first pass 29/31, final 31/31 (`player-checks-first.json`, `player-checks-final.json`). Phase 3 screenshot pass re-run (`final-home-*`, `final-details`), Phase 3 D-pad suite **23/23** on the final twin (`05-interaction-p5-10-final.json`) — home, details, mini player, BACK layering, restore, safe margins, reduced motion unchanged.

**First-render defects (4):**
- visual — sheet rows rendered label and detail inline, overlapping the check and running past the sheet's right edge (twin CSS: `.txt` not a column; Compose `ListItem` stacks headline/supporting so the Kotlin was fine).
- visual — overlay pills wrapped to two lines ("−10 / s", "Go to / live") because the summary text did not yield width (twin CSS; the Kotlin `Row` had the same latent overflow: the summary `Text` lacked `weight(1f)`, fixed in both).
- interaction — "Go to live" was `enabled = false` at the live edge: the twin's `.focus()` on a disabled button silently failed so RIGHT never got past it; in Compose a disabled Button is skipped, leaving a visible control that cannot be reached. Now always focusable, SELECT is a no-op at the edge (tv-dpad-axes).
- implementation-bug — preference remembered by language only: after choosing "English (CC)" the next stream came back with "English" (first `en` track). Fixed by remembering label/detail flavour first (Kotlin `PlaybackPrefs.subtitleLabel`, twin the same). Caught by the render check, not visible in a screenshot.
Two check failures were script errors, not defects (expected the play button after DOWN from the seek bar; the remembered control is correct focusRestorer behaviour; script timing on the shortened auto-hide).

**Final defects:** visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0. Two polish passes after the fix pass: sheet widened 560 → 600 dp so "Audio description" fits without ellipsis, CC detail shortened to "Sound cues". **Iterations: 3** (fix pass + 2 polish passes after the first render).
Screenshots: `render/first-player-*.png` (15), `render/final-player-*.png` (15), `render/final-home-*.png` + `final-details.png` (10, regression).

## Preservation
navigation ✓ (drawer/rails untouched) · theme ✓ (SportsColors only; no new hex) · typography ✓ (SportsTypography roles only) · component reuse ✓ (`LiveBadge`, the details/hero pill button treatment, `focusRestorer` pattern, `BackHandler` layering, `SportsDimens` safe margins and focus padding, tv-material `ListItem`) · structural change: the placeholder player replaced by a real player screen — justified by the task; BACK contract unchanged. `preservation-ok`.

## Misses by earliest wrong layer
1. **expected-concepts** — `interaction.selection_visible` never demanded for a chooser (a radio-style list where selected must read apart from focus is the core of the task); `a11y.dialog_focus` never demanded for a sheet.
2. **knowledge-gap** — the dialog-focus rule (`a11y-modal-dialog`: return focus to the invoker, first focus on the meaningful control) excludes platform tv, and there is no TV side-sheet record; `comp-dialog` has TV notes but was neither demanded nor retrieved.
3. **bundle-selection** — `tv-focus-performance` selected for the "performance" concern, bringing `table.virtualization`/`perf.image_sizing` into a track chooser; `comp-mini-player` into core for coverage of states/back that the codebase already has. `state.loading_empty_error` marked covered by a record about another component.
4. **requirements** — `intent.preserve` empty on an existing repo with KNOWN navigation/theme (repeat of p5-09).
5. **context-detection** — `design/tokens.json` not detected; typography UNKNOWN; surfaces "bordered"; direction labels five slots the code clearly has as "no repository evidence" (repeat).
6. **direction** — `icon-custom-glyphs` (app uses material-icons-core) and `metadata-focus-reveal` (cards always show title + subtitle) contradict the codebase; harmless for this task.
7. **reporting** — "Omitted (redundant): comp-mini-player" printed while the record is in core.

## Regressions to propose
- Query: the task sentence verbatim (with the project). Expect: `interaction.selection_visible` and `a11y.dialog_focus` demanded (chooser/sheet); a candidate that says selected ≠ focused for radio-style lists and "on close return focus to the control that opened the sheet"; no `table.virtualization`; `intent.preserve` = [navigation, theme].
- Query: "Let viewers switch the commentary language while the match is playing." Expect `media.track_selection` + `interaction.selection_visible`, tv-player-controls / layout-split-player, mode create.
- Query: "The captions menu disappears when the player controls auto-hide." Expect `tv.player_autohide` + `a11y.dialog_focus`, layout-split-player ("never while a menu is open").
- Rule platform regression: a tv request mentioning a sheet, dialog or chooser must be able to retrieve a dialog-focus rule (today `a11y-modal-dialog` is web/desktop/mobile only).
- Inspect/direction regressions: as p5-09 (tokens.json → tokens non-empty; explicit Compose `Typography` → KNOWN; 16:9 cards; material-icons-core → `icon-system-set`, never `icon-custom-glyphs`).

## Tags
`concept-miss`, `knowledge-gap`, `ranking-miss`, `requirements-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `tooling-limit`, `skill-helped`, `preservation-ok`
