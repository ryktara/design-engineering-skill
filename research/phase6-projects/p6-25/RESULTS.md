# p6-25 — Add a "continue watching" row to the home screen.

**Project:** `research/phase3-projects/p3-android-tv-compose/project` · Kotlin / Compose for TV (`androidx.tv.material3`, media3, coil) · platform **tv** (leanback launcher, no touchscreen)
**Existing UI:** yes — new element on an existing screen (hero + "Live now" + catalogue rails already exist)
**Build hash:** start `ea8eed72…d9947` = end `ea8eed72…d9947` ✔ (candidate c3, unchanged)
**Untouched by this task:** the `NavStack` / `navHasFocus` back-stack work from p6-24.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | what the code actually does | correct? |
|---|---|---|---|---|
| navigation | `tv-rails` | KNOWN | `ModalNavigationDrawer` side nav + `LazyColumn` of `LazyRow` rails | yes |
| theme | `dark-first` | KNOWN | `darkColorScheme`, canvas `#0B1220` | yes |
| surfaces | `bordered-flat` | INFERRED | flat `Card`/`Surface`, 1 dp borders, focus glow only | yes |
| radius | `pill` | INFERRED | cards/tiles are 8 dp; only the hero `Button` is `RoundedCornerShape(50)` | **partial** — the dominant card radius is 8 dp; "pill" is the button shape, and a new rail built to "pill" would be wrong |
| spacing | `8` | INFERRED | `SportsDimens` 8/12/16/20/28/48 — base 4, step 8 | yes |
| typography | `custom` | KNOWN | full 10-foot `Typography` in `SportsTheme.kt` | yes |
| components | compose, compose-tv-material, media3, coil | KNOWN | exactly that | yes |

One `partial` (radius). It did not hurt here because the direction preserved every visual slot and I reused the existing card.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| `platform_evidence` | `platform=[tv]` from project inspection (`platform_evidence` list itself empty) | correct |
| `intent.artifact_state` | `existing` | correct |
| `intent.operations` | `[create]` | correct |
| `intent.problem_domain` | `[]` | correct (no defect reported) |
| `intent.change_scope` | `screen` | correct |
| `mode` / `mode_evidence` | `[create]` · "build/create request on an existing surface" | correct |
| `scope.kind` / reason | `in-scope` · "UI design / interaction task" | correct |
| `change_budget` | `moderate` | acceptable (low would also be right; the direction still preserved everything) |
| `intent.preserve` | `[]` | thin — the sentence carries no preserve words, and `constraints.preserve_existing_system=true` carries the load instead |
| `project_context` | as inspected; `jobs=[resume]`, `product=[media]`, `screen=[home]` | correct, and `job=resume` from "continue watching" is the good inference here |

No platform, mode, scope or artifact-state miss.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Bundle = 8 records (core 4 + guardrails 4), ≈1352 tokens, no OPTIONAL layer.

| record | layer | verdict | category | note |
|---|---|---|---|---|
| `comp-media-card` | core | relevant | — | "one status overlay max" is what caught the REPLAY-pill-plus-progress-bar defect; accessible name = title + status. |
| `media-resume-and-details` | core | relevant | — | The one record that defined the feature: progress on each card, **resume at the saved position**, remove finished items, return focus to the launching card. |
| `dir-cinematic-media-tv` | core | partial | `generic` | Carries no concepts; restates the identity the app already has (backdrop, side nav, rails, focus glow). Nothing actionable for a new rail. |
| `comp-tv-rail` | core | relevant | — | Rail title ≥24 sp, per-rail focus memory, pivot scroll, stable item keys — all of which the new rail inherits from `RailRow`. |
| `impl-reuse-before-new` | guardrail | relevant | — | Reuse `RailRow`/`EventCard`, extend through the API. |
| `tv-typography-distance` | guardrail | partial | `generic` | True and platform-correct, but `SportsTypography` already encodes it; used only to grade, no change made. |
| `tv-dpad-axes` | guardrail | relevant | — | "vertical = sections" is the reason the row is a full rail in the column and why the rail index map had to shift. |
| `a11y-tv-focus-always` | guardrail | relevant | — | "move focus to a sensible neighbour when the focused item is removed" → the new rail had to be registered in `railIndexById` / `railItemKeys`, and items must leave the rail on completion. |

Bundle-level defect: **`missing-critical`** — `state.loading_empty_error`.

### Concept recall

expected 7 · delivered 6 · **recall 0.857** · critical 3 · delivered 2 · **critical recall 0.667**

| expected id | delivered? | layer if missing |
|---|---|---|
| `media.resume_playback` (critical) | yes (`media-resume-and-details`) | — |
| `layout.media_card` | yes (`comp-media-card`, `comp-tv-rail`) | — |
| `interaction.dpad_reachability` (critical) | yes (`tv-dpad-axes`) | — |
| `interaction.focus_restore` | yes (3 records) | — |
| `state.loading_empty_error` (critical) | **no** | `bundle-selection` |
| `process.reuse_first` | yes (`impl-reuse-before-new`) | — |
| `tv.ten_foot_typography` | yes (`tv-typography-distance`) | — |

The skill itself demanded `state.loading_empty_error` (it is in `metrics.required_concepts`) and reports it uncovered; `concept_trace` names the candidates it dropped — `layout-states-empty-loading-error`, `anti-no-states`, `comp-mini-player`. So this is not retrieval or a knowledge gap: the records exist and were candidates, and the cap-8 bundle left them out. `search -k 12` confirms the empty-state records never even enter the top 12 for this sentence, which is why they lost on utility. This matters concretely here: a "Continue watching" rail is empty on a fresh install, and an empty rail on TV is a dead row the viewer still has to press DOWN through. I implemented the omit-when-empty behaviour from my own pre-registration, not from the bundle.

`status` is CONFIDENT, not PARTIAL_SCOPE, which is right.

## 4. Direction verdict (`04-direction.md`)

12 of 13 slots `preserved`; `cards` is `new` (`card-poster-landscape`) with reason "no repository evidence for this slot". The choice it proposes — fixed 16:9, progress bar inside the art bottom edge with a scrim, text badge, title below — is *exactly* what `EventCard` already is, so the `new` status is a context-detection artefact (the inspector reports no `cards` slot for a Compose project), not a proposed change. Nothing in the direction pushed a restyle. **`unjustified_direction_slots` = 0.** `validation: OK`; preservation list covers navigation, layout, density, surface, typography, color, motion, focus, cta, imagery, icon, metadata.

## 5. Implementation

Files changed (copies in `before/`):

- `ui/AppState.kt` — `LibraryState` gains a private `recent` id list maintained by `savePosition`, and `continueWatching(catalogue, max)`: events with a meaningful `resumePoint`, most-recently-watched first, live excluded. Returns empty when there is no history.
- `ui/home/HomeScreen.kt` — `CONTINUE_RAIL_ID`; `HomeReady` derives `resumable` from `LibraryState` each composition and builds `continueRail` only when it is non-empty; the rail is emitted as a `LazyColumn` item directly under "Live now"; `railIndexById` and `railItemKeys` are index-shift-aware so focus restoration from Details/Player still resolves; SELECT calls the new `onResume(event, savedMinute)` instead of opening Details.
- `ui/home/Cards.kt` — `remainingMin` derived from the existing `resumeFraction` param; part-watched cards print "27 min left" instead of "Full time", the content description says "…, 27 minutes left" (same number, spoken and printed), and the REPLAY pill is suppressed when the progress bar is showing (one status overlay).
- `ui/SportsApp.kt` — seeds three part-watched replays into `LibraryState` (a real app loads the household history) and wires `onResume` to `leaveHome(Route.Player(event, startAt))`, which is the existing resume route.

No new component, no new token, no theme/nav/typography change. The rail is derived state, not a catalogue rail, so it self-empties when a title is finished.

**Guidance used:** `media-resume-and-details` (resume at the saved position rather than opening Details; remove finished items; focus returns to the launching card), `comp-media-card` (one status overlay → REPLAY pill suppressed), `comp-tv-rail` + `impl-reuse-before-new` (reuse `RailRow`/`EventCard` wholesale), `tv-dpad-axes` (a section is a row in the vertical axis), `a11y-tv-focus-always` (register the rail in the focus-restore maps).
**Guidance ignored:** `dir-cinematic-media-tv` (describes the identity the app already has; its "heavy display face, filled icons ≥32 dp" is not this task) and `tv-typography-distance` (already satisfied by `SportsTypography`; no change made).

**Process guidance check.** `impl-reuse-before-new` was in the bundle and was correct, but SKILL.md §2/§7 already forces the inspect-reuse-render loop; `verify-render-and-inspect` was *not* in the bundle and I rendered and inspected anyway. So: **`process_records_needed: false`** — spending one of eight slots on the generic reuse record bought nothing that §2 did not already give, and that slot is exactly what `state.loading_empty_error` needed.

## 6. Render

**Mode: `html-twin`** at 1920×1080 (Playwright 1.63.0 / Chromium, `render/twin.html` + `render/shoot.js`). No capture harness exists for this Compose project; the twin is adapted from the one authored for p6-24 and rebuilt around the home rail column, at dp×2 against `SportsTheme.kt` tokens. `?v=before` renders the pre-change column, `?history=none` renders an empty `LibraryState`. Every screenshot listed was opened and looked at (`first-01/02/03/05`, `final-01/02/03/04/05`).

Screens: `01-home-top`, `02-continue-focused`, `03-resume-select`, `04-back-to-card`, `05-empty-history`, plus `evidence-before-no-continue.png`.

### First-render defects (2, iterations 2)

| type | defect |
|---|---|
| implementation-bug | Twin only: focusing the Continue watching rail scrolled its title off the top of the screen and clipped the focused card above the safe area — the scroll target was measured with `getBoundingClientRect()` while the column transform was still animating. Fixed with `offsetTop` + a max-scroll clamp. |
| existing-system-mismatch | Real change: a part-watched card carried both the REPLAY pill and the resume progress bar — two status markers, against `comp-media-card`'s "one status overlay max". This is a defect the guidance explicitly warned about and I shipped on the first pass: it counts against me, not the skill. Fixed by suppressing the pill when `remainingMin != null`. |

### Final defects: none

Verified in the final renders: rail title visible and inside the safe area, focus ring + scale on the focused card, "27 / 89 / 36 min left" with matching progress fractions, SELECT → `startAtMin = 88 of 115 (resumed, not restarted)`, BACK → focus back on the launching card, and with an empty history the rail is absent and "Coming up" follows "Live now" directly.

**Known limitation (not a defect, out of budget):** a part-watched replay appears both in "Continue watching" and in the catalogue "Catch up" rail, because `content.rails` is server-side content this task does not own.

## 7. Preservation

Navigation (drawer + rail column), theme, typography, surfaces, card geometry, focus treatment and motion are untouched; the change reuses `RailRow` and `EventCard` and adds one derived rail plus one callback. p6-24's back-stack handling untouched. `unjustified_structural_change: 0`.

## 8. Miss routing

One miss, earliest layer **`bundle-selection`**: `state.loading_empty_error` was demanded as a required concept, candidate records carrying it existed (`layout-states-empty-loading-error`, `anti-no-states`), and the cap-8 bundle dropped them in favour of `dir-cinematic-media-tv` (zero concepts) and the two generic guardrails.

## 9. Regressions to propose

1. `Add a "continue watching" row to the home screen.` (TV/Compose project) → the bundle must carry `state.loading_empty_error`: a derived row with no items is omitted, never rendered as an empty rail.
2. `Show the last thing the viewer was watching on the TV home screen.` → expect `media.resume_playback` + `layout.media_card` + `interaction.focus_restore`, and no `touch.*` / `tv.sign_in_code` records.
3. A record that contributes zero concepts and only restates the project's existing identity (`dir-cinematic-media-tv` here) should lose its slot to a record carrying an uncovered required concept when the bundle is at cap.

## 10. Tags

`concept-miss`, `ranking-miss`, `context-detection-miss` (radius=pill), `render-defect-fixed`, `skill-helped`, `preservation-ok`
