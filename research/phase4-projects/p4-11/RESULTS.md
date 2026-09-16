# p4-11 — results

## Task
"add a match details screen with play, resume and add-to-watchlist, consistent with the existing dark rails home"

## Project / stack / platform
`phase3-projects/p3-android-tv-compose/project` (after p4-10) — Android TV, Compose for TV. Existing project, new/extended screen: the Phase 3 `EventDetailsScreen.kt` was a placeholder (backdrop, title, three unlabelled-state buttons, no resume, no watchlist state, no related content); it is rebuilt in place so the existing `Route.Details`, the home → details → player flow and the BACK contract stay as they were.

**Render mode: html-twin + static review** (same twin as p4-10, extended; Playwright 1.63.0 at 1920×1080; arrows = DPAD, Enter = SELECT, Backspace/Escape = BACK).

## Design-context table (detected vs actual)
Same `01-inspect.json` as p4-10 (identical project state at inspection time), so the same verdicts apply:
| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | tv-rails | KNOWN | modal side drawer + immersive hero + rails | partial |
| theme | dark-first | INFERRED | dark-only, canvas #0B1220, single amber accent, `design/tokens.json` | yes (should be KNOWN) |
| surfaces | bordered-flat | INFERRED | flat tonal steps + scrims; focus = ring + glow + scale | partial |
| radius | medium (8) | INFERRED | 8 dp cards, pill buttons, 4 dp badges | yes |
| spacing | irregular | UNKNOWN | `SportsDimens` named scale (48/27/20/28/12) | no |
| typography | unknown | UNKNOWN | `SportsTypography` TV scale, condensed display face | no |
| components | compose, tv-material, media3, coil | KNOWN | + EventCard / HeroButton / LiveBadge / Pill / RailRow (`component_dirs: []`) | partial |

What "consistent with the existing dark rails home" meant in practice (all taken from the code, none from the inspector): `SportsColors`/`SportsDimens`/`SportsTypography`, the `HeroButton` treatment (accent pill primary, elevated secondary, 3 dp white ring + 1.08 scale, scale dropped under reduced motion), `EventCard` + `RailPivotSpec` for the related rail, `LiveBadge`/`Pill` for status, `formatClock`, the dual-scrim backdrop, 48/27 dp safe margins.

## Requirements verdict (`02-requirements.json`, CONFIDENT)
- scope `UI_DESIGN`, mode `create` (evidence "add a") — right.
- platform tv / input remote / stack compose+compose-tv / product media — right.
- `screen = [detail, home]` and `primary_jobs` containing "create home" — wrong: "the existing dark rails home" is the reference system, not a screen to create. `intent.existing = true` was detected (from "existing") but did not stop `home` from becoming a creation target.
- `jobs = [details, resume, watchlist]` — right, and exactly the three actions of the task.
- `constraints.preserve_existing_system = true` — right; `intent.preserve = []` — should carry theme/components/navigation from "consistent with the existing".
- `change_budget = moderate` — acceptable for a new screen.
- `screen_subtype = rails` — right for the related rail, though it came from the word "rails" describing the home.
- `missing: brand` — right (no brand file; the token file is the brand).

## Guidance verdict (`03-guidance.md/json`; 8 records: 5 core + 3 guardrails; concepts 10/10, ≈1688 tokens, coverage/1k 5.92, purity 0.98)
| record | role | verdict | note |
|---|---|---|---|
| `media-resume-and-details` | core | relevant | effectively the spec: Play/Resume with remaining time + Start over as default focus, text metadata, ≤3-line synopsis, secondary actions after Play in one row, watchlist toggle with text state reflected on cards, BACK to the launching row, compose-tv note (focusRequester on Play, remember the launching card). Followed verbatim |
| `cta-focus-selects` | core | relevant | "≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails" — shaped the action row and the related rail |
| `layout-rails` | core | partial | applies to the related rail (pivot, focus memory, partial trailing card) |
| `comp-mini-player` | core | off-target | selected "for required coverage: loading, empty and error states, TV safe margins"; the details screen has no mini player |
| `comp-tv-rail` | core | partial | rail title ≥24 sp, one aspect ratio, stable keys — reused for the related rail |
| `tv-typography-distance` | guardrail | relevant | synopsis ≤3 lines, titles ≤2 lines, 20 sp caption floor for the metadata labels |
| `a11y-focus-visible` | guardrail | relevant | ring + scale on every action and card |
| `tv-dpad-axes` | guardrail | relevant | straight paths: LEFT/RIGHT in the row, DOWN into the rail, UP back |

Counts: relevant 5 · partial 2 · off-target 1. `uncovered required concepts`: none reported.

Missing guidance:
1. `tv-safe-area` (in the base) not selected → the first render lifted the focused first action 16 px into the horizontal margin and 4 px below the vertical one; the record says persistent UI stays inside, but neither it nor `focus-scale-glow` says *a focused control at the safe edge must reserve its scale overflow on that edge* (the cards reserve it between neighbours). Phase 3 tvOS reported this exact gap; still absent → **knowledge gap** (expected-concepts) plus **ranking miss** for tv-safe-area (bundle-selection).
2. Vertical budget of a bottom-aligned details block: title lines × size + synopsis lines + metadata + actions must fit `frame − 2×safeV`; `media-resume-and-details` prescribes the parts but not that the sum must fit, and the display size to use. First render pushed the LIVE badge above the top margin at displayLarge → knowledge gap.
3. Status/toast placement: `a11y-live-status` (not selected here; it was selected for p4-10 where it was irrelevant) says nothing about *where* a toast may sit; the first placement covered the focused action row → knowledge gap (small).
4. `a11y-tv-focus-always` (initial focus on Play, restoration) and `tv-back-behavior` not selected; their content is partially duplicated inside `media-resume-and-details`, so the bundle still covered the behaviour → ranking miss, low impact.
5. `card-poster-landscape` (progress bar for continue-watching inside the art bottom edge) not selected although the resume fraction on cards is part of the task → ranking miss.

## Direction verdict (`04-direction.md/json`, validation OK; preserved [navigation, surface, color]; changed [])
| slot | choice | status | verdict |
|---|---|---|---|
| navigation | nav-tv-side (preserved) | preserved | right |
| layout | layout-rails | new | should be "preserved": the details layout is prescribed by the platform file (backdrop + text + action row + rails) and the home already has rails |
| density | density-medium | new | web-unit text, unusable on TV |
| surface | bordered-flat (preserved) | preserved | acceptable |
| cards | card-flat-tile | new | wrong: the project's card is 16:9 imagery-backed (`EventCard`); the related rail must reuse it, not introduce flat tiles (`card-poster-landscape` was runner-up 0.401) |
| typography | typography-system-native | new | wrong: `SportsTypography` exists; should be preserved |
| color | color-dark-accent (preserved) | preserved | right |
| motion / focus / cta / imagery / icon / metadata | as p4-10 | new | match the code; labelled "new — no repository evidence" |

Unjustified changed slots: cards, typography (layout is a detection miss rather than a proposal to change). I built against the code, not the table; the per-slot `cta` text (≤4 actions, Play first, DOWN to rails) was directly useful.

## Implementation summary (before-copies in `before/`)
- `ui/AppState.kt` — `Route.Player(event, startAtMin)`; new `LibraryState` (watchlist ids, saved positions, `resumePoint`, `toggleWatchlist`, `savePosition`) shared by Home and Details.
- `ui/details/EventDetailsScreen.kt` — rebuilt: backdrop + dual scrim (unchanged), meta line with LIVE/REPLAY badge, title (displayMedium, ≤2 lines, heading semantics), score/clock, synopsis ≤3 lines, `MetadataBlock` (Channel / Kick-off / Length / Status as label+value text), `ActionRow` by state (LIVE: Watch live · Watch from start · toggle; REPLAY+position: Resume · N min left · Start over · toggle; REPLAY: Play · toggle; UPCOMING: Set reminder · toggle) with `focusRequester` on the primary, `focusRestorer`, `stateDescription` on the toggle, icon + text state; `RelatedRail` (same `EventCard`, `RailPivotSpec`, `focusRestorer`, heading) inside a `LazyColumn` with `beyondBoundsItemCount = 1` so DOWN from the actions finds the rail and scrolls it into view; SELECT on a related card re-targets the route (BACK still returns Home); scale overflow reserved at the safe edges.
- `ui/SportsApp.kt` — `LibraryState` created at app level; Details receives `library`, `related`, `onPlay(startAt)`, `onOpenRelated`; the player placeholder receives `startAtMin`, reports the watched position on BACK (saved for non-live events), and keeps the p4-10 return path.
- `ui/home/Cards.kt` — `EventCard(saved, resumeFraction)`: text "SAVED" pill at the top-right, watched fraction on the existing progress bar, merged content description extended.
- `ui/home/HomeScreen.kt` — `RailPivotSpec` made `internal` for reuse; `library` threaded to `RailRow`/`EventCard`. Home layout unchanged.
- `data/SportsCatalog.kt` — `allEvents`, `related(event)` (same competition first, then same sport, capped at 8).
- Twin: details section rebuilt (column with hero block + related rail, metadata block, dynamic action row, watchlist toggle with `aria-pressed` + text, `role=status` toast, library sync into home cards in place, `savePlayerPosition` on BACK from the player); `render/interaction.js` (Phase 3 suite) updated for the renamed details keys and scoped to `#home` rails. Scripts: `render/render-p4-11.js`, `render/interaction-p4-11.js`.

## First-render defects by type (`first-*.png`, `05-interaction-first.json` 26/28)
1. **visual** — LIVE details: 2-line title at displayLarge + 3-line synopsis + metadata + actions overflowed the frame; the LIVE badge and meta line sat above the 54 px top margin (`first-details-live.png`). Twin + Kotlin.
2. **visual** — the status toast (bottom-right at the safe margin) covered "Watch from start" / the focused watchlist toggle and the related rail captions (`first-details-watchlist-on.png`, `first-details-related-rail.png`). Twin (Kotlin has no toast; TalkBack gets the toggle's `stateDescription`).
3. **platform** — focused first action lifted 16 px into the horizontal safe margin and 4 px below the vertical one (interaction check). Twin + Kotlin.
4. **implementation-bug** — twin only: home cards were not re-synced after the player saved a position (no watched-fraction bar).
5. **implementation-bug** (harness) — Phase 3 suite's safe-margin loop measured the hidden details rail (`first-card:d-related`, left 0); the p4-10 script still expected the old `details:watch` key.
Totals: visual 2 · interaction 0 · accessibility 0 · platform 1 · existing-system-mismatch 0 · implementation-bug 2.

## Final defects by type (`final-*.png`, `05-interaction-final.json` 28/28; Phase 3 suite 23/23; p4-10 suite 18/18)
visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
Remaining, not counted as defects: the action row is indented 12 dp from the title/metadata column (the reserved lift; visible in `final-details-live.png`); "Set reminder" has no reminder service behind it (toast only); the twin title is not condensed (no webfont); Kotlin unverified by a compiler (`LazyColumn(beyondBoundsItemCount)` availability in Foundation 1.8 and `Icons.Filled.Add/Check` from icons-core are believed correct).

## Iterations
3 (first render → fix 1–4 and harness → second run found the wide-primary lift still 4 px over at 6 dp reservation and the vertical dip → final).

## Interaction test summary (`05-interaction-final.json`, 28 checks)
LIVE: SELECT on a live card opens details; **Play (Watch live) takes default focus**; actions = Watch live · Watch from start · +Add to watchlist, one primary; RIGHT walks to the toggle and stays at the end; **toggle text Add to watchlist → In watchlist with aria-pressed, focus stays**, announced by the status region, home card shows SAVED immediately, toggle off restores the text. DOWN enters the related rail (scrolled into view, ring visible), every related card reachable by RIGHT with visible on-screen focus, rail has a "More Premier League" heading, UP returns to the remembered action, SELECT on a related card re-targets details with focus on Play, **BACK returns home with focus on the launching card**. REPLAY: Play + toggle only; Play → player from 0; BACK → launching card; re-opened details offers Resume · 118 min left (primary, default focus) + Start over + toggle; metadata is text with minutes left; Resume starts at the saved position; home card shows the watched fraction; Start over plays from 0. UPCOMING: Set reminder + toggle. All details text ≥ 40 px; persistent UI inside the 96/54 px frame (lifted state included); no `:hover`; reduced motion keeps the ring and drops the scale.

## Preservation verdict
Navigation (drawer + rails), theme tokens, typography scale, button and card language, routes, BACK layering and the p4-10 restoration all preserved; new elements (metadata block, toggle, related rail, SAVED pill, resume bar) are built from existing primitives. Structural change: the details column became a `LazyColumn` so a rail can sit below the fold — justified by the platform pattern ("DOWN into related rails"). Unjustified structural changes: 0. `preservation-ok`.

## Regressions to propose
- query: "add a match details screen with play, resume and add-to-watchlist, consistent with the existing dark rails home" → expect `screen = [detail]` only (no "create home"), `intent.preserve` ⊇ [theme, components], `tv-safe-area` in guardrails, no `comp-mini-player`, direction cards/typography preserved from the repo.
- query: "details screen action row at the safe-area edge with focus scale" (tv) → expect guidance to reserve the scale overflow on the edge side (or reduce the lift for wide buttons).
- query: "details text block overflows the top of the screen on TV" → expect a rule on the vertical budget (title lines/size + synopsis lines + metadata + actions ≤ frame − margins).
- query: "watchlist toggle on TV" → expect text-state + state semantics + reflected on cards (media-resume-and-details) and `card-poster-landscape` for the continue-watching bar.

## Tags
`preservation-ok`, `skill-helped` (media-resume-and-details + cta-focus-selects were the spec; tv-typography-distance set the line limits), `requirements-miss` ("home" as a creation target; preserve list empty), `context-detection-miss` (same as p4-10), `direction-mismatch` (cards flat-tile, typography system-native, density web text), `ranking-miss` (tv-safe-area, card-poster-landscape, a11y-tv-focus-always not selected; comp-mini-player selected), `knowledge-gap` (edge lift reservation, vertical budget, toast placement), `render-defect-fixed` (5), `tooling-limit` (no Android build).


## Addendum — knowledge-base drift during the run
The skill's data files (`data/rules.jsonl`, `patterns.jsonl`, `components.jsonl`, `lexicon.json`, eval fixtures) were modified between 12:23 and 12:57 by another process, not by this run (no write of this run touched `design-engineering/`). All `01`–`04` files above were produced at 12:20–12:21 against the earlier base; `02-requirements-rerun-1303.json` and `03-guidance-rerun-1303.json` were produced at 13:03 against the modified base. Diff: Requirements improved: `screen` [detail, home] → [detail] and "create home" dropped from `primary_jobs` (the miss reported above is fixed in the newer base). Guidance changed: + `tv-safe-area` (would have covered first-render defect 3, the edge lift) and + `layout-states-empty-loading-error`; − `comp-mini-player` (the off-target core) and − `comp-tv-rail`; status CONFIDENT → PARTIAL (reported uncovered concern not re-examined). The implementation was already done against the 12:21 bundle; verdict counts in this file refer to that bundle.
