# p4-10 — results

## Task
"users lose their place in the live-now rail after coming back from a match; fix focus restoration without changing the home layout"

## Project / stack / platform
`phase3-projects/p3-android-tv-compose/project` — Android TV, Compose for TV (`androidx.tv:tv-material 1.0.0`, Compose Foundation 1.8, Media3, Coil). Existing UI (Phase 3 live-sports home: immersive hero, Live now / Coming up / Catch up / sport rails, EPG tile, mini player, modal side drawer, details/player/guide routes).

**Render mode: html-twin + static review.** No Gradle/SDK; the Kotlin was reviewed statically and the existing HTML twin (`p3-android-tv-compose/render/twin.html`, 1 dp = 2 px, 1920×1080, Playwright 1.63.0) was extended. Arrow keys = DPAD, Enter = SELECT, Backspace/Escape = BACK.

## Design-context table (detected vs actual)
| field | detected | status | actual (from SportsTheme.kt / HomeScreen.kt / Cards.kt) | correct? |
|---|---|---|---|---|
| navigation | tv-rails | KNOWN | rails inside a `ModalNavigationDrawer` side nav (nav-tv-side + rails); evidence cites AppState.kt, Cards.kt, HomeRail.kt but not SportsApp.kt where the drawer lives | partial (rails yes; side drawer not named) |
| theme | dark-first | INFERRED | dark-only `darkColorScheme`, canvas #0B1220, one amber accent #FFC533, `design/tokens.json` dark theme only | yes (should be KNOWN: tokens.json + darkColorScheme are explicit) |
| surfaces | bordered-flat | INFERRED | flat tonal surfaces (canvas/surface/elevated steps) + focus **border + glow + scale**; a 1 dp border only on the EPG tile; cards are imagery-backed with scrims | partial (flat yes; "bordered" is the focus ring, not the surface language) |
| radius | medium (8) | INFERRED | 8 dp cards/mini player, 4 dp badges, pill (50%) buttons | yes |
| spacing | irregular [16,10,8,6] | UNKNOWN | `SportsDimens`: safeH 48 / safeV 27 / gutter 20 / railGap 28 / focusPadding 12 — a named, deliberate scale; the sampled 16/10/8/6 are inner paddings | no (the dimens object is not read) |
| typography | unknown | UNKNOWN | `SportsTypography`: full TV scale (display 74/56, headline 46/38, title 30/28, body 30/24, label 24/20 sp), condensed display face for titles/scores, system sans body; `FontFamily.SansSerif` is declared | no (`FontFamily.SansSerif` + a `Typography(...)` block are font declarations) |
| components | compose, compose-tv-material, media3, coil | KNOWN | same, plus project components EventCard / EpgEntryTile / MiniPlayer / HeroButton / RailRow (`component_dirs: []` despite `ui/home`, `ui/details`, `ui/theme`) | partial |
| tokens | [] | — | `design/tokens.json` in the skill's own `tokens.py init` shape | no (same miss as Phase 3) |
| platforms | tv | KNOWN | tv-only (leanback, touchscreen not required) | yes — the Phase 3 `mobile` false positive is fixed ("Compose dependencies imply mobile but the only launcher is leanback: TV-only app") |

## Requirements verdict (`02-requirements.json`, status CONFIDENT, exit 0)
- scope `UI_INTERACTION`, in_scope — right (a focus/DPAD problem is UI work; `activation.ui_terms = [layout, focus]`).
- mode `[audit, refactor]` with evidence "interaction problem on existing UI / fix follows the diagnosis" — right; `intent.existing = true`, `problem = true`, `facet = interaction`, `creation = false` — all right.
- `intent.preserve = ["layout"]` — right, taken from "without changing the home layout".
- `change_budget = moderate` — wrong for this task: a fix that must not change the layout is a *minimal* budget; nothing in the sentence justifies "moderate". (`intent.scope = moderate` is the default, not evidence.)
- platform tv / input remote / stack compose+compose-tv / screen home / subtype rails / product media — right (all KNOWN from the inspection or request).
- `problems = [interaction]`, `primary_jobs = ["audit home"]` — thin: the sentence names the exact object ("live-now rail"), the trigger ("coming back from a match" = return from the player) and the symptom ("lose their place" = focus + scroll position). None of "rail", "player/return", "focus restoration", "scroll position" reaches jobs/components; `components = [media]` only.
- `project_context` is passed through unchanged from the inspector (same partials as the table above).
- `accessibility.keyboard = true` is odd for a TV/remote request (harmless).

## Guidance verdict (`03-guidance.md/json`; 8 records: 3 core + 5 guardrails; metrics: concepts 8/8 covered, ≈1279 tokens, coverage/1k 6.25, purity 0.96, contaminated: none reported)
| record | role | verdict | note |
|---|---|---|---|
| `comp-tv-rail` | core | relevant | "focus memory per rail", pivot, stable keys — the rail contract the fix has to keep |
| `comp-mini-player` | core | partial | "BACK from the full player returns … with focus restored to the element that was focused before" is exactly the flow; the rest (corner placement, two actions) is not this task |
| `cta-single-primary` | core | off-target | selected "for required coverage: one primary action per view" — nothing in a focus-restoration fix concerns the primary CTA |
| `a11y-tv-focus-always` | guardrail | relevant | the decisive rule: "restore focus to the previously focused item … move focus to a sensible neighbour when the focused item is removed" — drove the id → index → hero resolver |
| `tv-back-behavior` | guardrail | relevant | the "BACK semantics unchanged" constraint; the layering player → home (not details) was kept because of it |
| `tv-dpad-axes` | guardrail | partial | straight-path reachability is a regression check, not part of the fix |
| `tv-typography-distance` | guardrail | off-target | no text changes |
| `a11y-live-status` | guardrail | off-target | selected "for required coverage: feedback"; a focus fix has no status announcements |

Counts: relevant 3 · partial 2 · off-target 3. `uncovered required concepts`: none reported.

Missing guidance and where it is missing:
1. **Hoist every piece of "place" state above the screen** (scroll states, hero/backdrop state, focused id) because a route switch drops the screen's `remember`/`rememberSaveable`. Absent from the base (`search "hoist rail scroll state …"` returns `layout-rails`, which only says "rails remember their last focused index when returning") → **knowledge gap** (layer: expected-concepts; no record to rank).
2. **Do not re-scroll on return** — restore by *not moving* the lists when the target is already laid out; `scrollToItem` top-aligns a rail and snaps a card to the leading edge, which is a different picture from the one the viewer left. Absent → knowledge gap.
3. **Lazy-list restoration timing on Compose**: wait until the item is in `layoutInfo` before `requestFocus()` (throws on a detached requester), bounded by frames. Phase 3 listed this as gap 6; still absent (`search "lazy list requestFocus after scrollToItem …"` returns `a11y-tv-focus-always`, `nav-tv-side`) → knowledge gap.
4. **Time-based rails**: match the remembered tile by stable id first, index second, because the rail re-sorts while the viewer is away. `a11y-tv-focus-always` covers the removed case in one clause; nothing says "id first, index as fallback" → knowledge gap (small).
5. `layout-immersive-rails` (search rank 3, 0.631) is the project's actual layout and is not in the bundle; `layout-rails` was preferred by direction. Not needed for this fix, but it is the record that says the hero "follows the focused item", which is state that must survive the return → ranking miss (bundle-selection), minor.

## Direction verdict (`04-direction.md/json`, validation OK; change budget moderate; preserved [navigation, surface, color], changed [])
| slot | choice | status | verdict |
|---|---|---|---|
| navigation | nav-tv-side (preserved from tv-rails KNOWN) | preserved | right (the project is a modal side drawer + rails) |
| layout | layout-rails | new | should be *preserved*: the repository has the layout (immersive hero + rails); "no repository evidence for this slot" is a detection miss, and `layout-immersive-rails` is the correct value |
| density | density-medium | new | slot text is web units ("8 px base, 40–48 px interactive heights, 16 px body on web/mobile") — unusable on TV, same as Phase 3 |
| surface | bordered-flat (preserved) | preserved | acceptable |
| cards | card-poster-portrait | new | wrong: Cards.kt is 16:9 landscape (`cardH = 151 dp` for `cardW = 268 dp`); `card-poster-landscape` was runner-up 0.442; a preserve-layout task must not propose changing the card geometry |
| typography | typography-system-native | new | wrong: the project defines `SportsTypography` with a condensed display face; should be preserved (`typography-condensed-display` runner-up 0.393) |
| color | color-dark-accent (preserved) | preserved | right |
| motion / focus / cta / imagery / icon / metadata | focus-scale, scale-glow, focus-selects, immersive-backdrop, platform-native, focus-reveal | new | all match what the project already does, but every one is labelled "new — no repository evidence" on a task whose sentence forbids layout change; `icon-platform-native` vs the project's filled material icons is a nit |

`preservation`: preserved 3 of 13 slots; 10 "new". For an audit/refactor task with `intent.preserve = [layout]` the direction should preserve (or at least not propose) every slot and report the layout slot as KNOWN. Unjustified changed slots: layout, cards, typography (three). I ignored the direction table entirely; only the per-slot focus/motion text was consistent with the code.

## Implementation summary
Kotlin (before-copies in `before/app/...`):
- `ui/AppState.kt` — `HomeFocusMemory` now also holds the app-level `columnState: LazyListState`, `heroEvent`, `lastFocusedEventId`; `rememberTile(...)` takes the event id; new pure `resolveRestoreTarget(railItems)` → `RestoreTarget(key, railId, index, exact)` implementing id → clamped index in the same rail → hero.
- `ui/home/HomeScreen.kt` — hero/backdrop state seeded from `focusMemory.heroEvent` and written back; the column uses `focusMemory.columnState` (the old `rememberSaveable` was dropped on every route switch); the restore `LaunchedEffect` resolves the target against the current content, scrolls the column/rail **only if the target is not laid out**, waits (bounded, `awaitFrame`) until the rail and the item are in `layoutInfo`, requests focus with the guard, falls back to the hero, and re-records the neighbour as the new memory when the tile was gone. `RailRow` passes `event.id`. Unused `rememberSaveable` import removed.
- No change to `SportsApp.kt`, routes, `BackHandler`s, `Cards.kt`, dimens, tokens: the home layout is untouched.
Twin (before-copy in `before/render/twin.html`): records rail/index/event id on focus, mirrors `resolveRestoreTarget`, `__twin.finishEvent(id, score)` moves a live match to Catch up and re-renders the rails, `__twin.legacyRestore` reproduces the pre-fix Kotlin path (baseline render only).
Scripts: `render/render-p4-10.js`, `render/interaction-p4-10.js` (run with `NODE_PATH` = the Phase 3 render `node_modules`).

Static review findings in the *original* Kotlin that the twin had not reproduced (twin fidelity gap from Phase 3): (a) `focusedLive`/`heroEvent` were `remember`ed inside `HomeReady`, so the return showed the first live event and crossfaded to the remembered tile 300 ms later; (b) `listState` was `rememberSaveable` inside `HomeReady` → reset to top, then `scrollToItem(rail)` top-aligned the rail, hiding the hero; (c) `railState.scrollToItem(index)` snapped the card to the leading edge although the rail state was already hoisted and correct; (d) a tile that left the rail fell back to the hero, not to a neighbour; (e) a single `awaitFrame()` after two lazy scrolls is not enough for the item to compose, so the guarded `requestFocus` silently fell back to the hero. All five are fixed.

## First-render defects by type
Baseline (legacy mode, reproduces the shipped Kotlin): `baseline-home-after-back-immediate.png` shows all of (a)–(c): hero text clipped/off-screen, Live now top-aligned, Celtics card snapped to the left edge, backdrop = Arsenal (green) while focus is on Celtics; `baseline-home-after-match-ended.png` shows (d): focus on "Watch live", rail lost. Baseline interaction run: 6/18.
First render of the fix (`first-*.png`, `05-interaction-first.json`): 16/18.
- visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
- Two failures were test-harness predicates, not UI: (1) my "hero visible" check demanded `hero.top ≥ 0`, but the twin (and Compose's bring-into-view) legitimately scrolls the hero partly above the fold while the first rail is focused — the substantive assertion (position unchanged) passed; (2) the BACK-semantics section ran after scenario B3 had emptied the Live now rail, so DOWN from the hero could not enter a rail. Both fixed in the script (reload before the BACK section; compare visibility to the pre-leave state).
- Phase 3 regression (`interaction.js`, 23 checks): first run 22/23 ("focused element always on screen", rail:replays:r1 at y=806) while another Playwright instance was running; 3/3 subsequent runs 23/23, and the unmodified before-twin behaves identically → timing flake, not a regression.

## Final defects by type
visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
Remaining (not defects of this task): the mini player keeps showing the finished match as "Playing 96 – 90" after `finishEvent` (twin data, no state transition for a stream that ended — out of scope); Kotlin never compiled (`LazyListLayoutInfo.viewportEndOffset`, `awaitFrame` usage believed correct); `resolveRestoreTarget` is pure but has no unit test because the module has no test source set or JUnit dependency and `HomeFocusMemory` references `FocusRequester` (compose-ui AAR).

## Iterations
2 (first render + interaction run; script predicate fixes + final run). No UI change was needed between first and final: `final-*.png` = `first-*.png`.

## Interaction test summary (`05-interaction-final.json`, 18/18; `05-interaction-baseline.json`, 6/18 with legacy restore)
Live now card 3 → details (focus Watch live) → Watch live → player → BACK: returns home (not details); focus on the launching card; hero and backdrop unchanged immediately and after the debounce; column transform unchanged and hero as visible as before; live rail transform and card rect unchanged; ring visible and on screen. Match ended while in the player: focus lands on the neighbour at the same index (`rail:live:e4`), resolver reports `exact=false`, memory updated. Rail re-ordered while away (Catch up gains a new first item): the same event is found by id. Rail emptied: hero primary. BACK semantics unchanged: hero → nav, nav → exit, rail → hero + column at top, details → launching hero control. Phase 3 suite still 23/23.

## Preservation verdict
Navigation, theme, typography, component language, routes, BACK layering, ids and semantics all unchanged; the home layout is byte-identical in `Cards.kt`/`SportsApp.kt`. Structural changes: 0. `preservation-ok`.

## Regressions to propose
- query: "users lose their place in the live-now rail after coming back from a match; fix focus restoration without changing the home layout" → expect `change_budget = minimal`, direction `layout` slot preserved (KNOWN from HomeScreen.kt/`layout-immersive-rails`), no `cards`/`typography` "new" proposals, no `cta-single-primary`/`a11y-live-status` in the bundle.
- query: "focus lands on the hero instead of the tile the user left after the list refreshed" (tv, compose) → expect `a11y-tv-focus-always` first and a record about id-first/index-fallback restoration on time-based rails.
- query: "keep the rail scroll position when returning from the player" (compose-tv) → expect guidance that scroll/hero state must be hoisted above the screen and that restore must not re-scroll a laid-out target.
- inspect: Compose project with `Typography(...)` + `FontFamily.SansSerif` and a `SportsDimens`/`Dimens` object → expect typography KNOWN and spacing KNOWN (not "irregular").

## Tags
`preservation-ok`, `skill-helped` (a11y-tv-focus-always "sensible neighbour", tv-back-behavior, comp-tv-rail focus memory), `requirements-miss` (change budget moderate; rail/player/scroll not captured), `context-detection-miss` (spacing, typography, tokens, layout slot "no evidence", cards geometry), `direction-mismatch` (layout/cards/typography proposed as new on a preserve task; density text web-only), `ranking-miss` (cta-single-primary and a11y-live-status selected for coverage; layout-immersive-rails not selected), `knowledge-gap` (hoisting place-state; do-not-rescroll; lazy compose timing; id-first restoration), `render-defect-fixed` (baseline defects a–e fixed), `tooling-limit` (no Android build; twin fidelity had hidden a–c in Phase 3).


## Addendum — knowledge-base drift during the run
The skill's data files (`data/rules.jsonl`, `patterns.jsonl`, `components.jsonl`, `lexicon.json`, eval fixtures) were modified between 12:23 and 12:57 by another process, not by this run (no write of this run touched `design-engineering/`). All `01`–`04` files above were produced at 12:20–12:21 against the earlier base; `02-requirements-rerun-1303.json` and `03-guidance-rerun-1303.json` were produced at 13:03 against the modified base. Diff: Guidance bundle identical (8/8 same ids, CONFIDENT). Requirements regressed: `screen` [home] → [] and `primary_jobs` [audit home] → [audit media] — the sentence's "home layout" no longer yields the home screen.
