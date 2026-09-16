# p5-09 — held RIGHT streams the rail too fast (Android TV, Compose for TV)

**Task (verbatim):** "When you hold right on the remote the rail flies past too fast to read the titles."
**Project:** `research/phase3-projects/p3-android-tv-compose/project` — Kotlin, Jetpack Compose 1.8 + androidx.tv tv-material, Media3, Coil. Platform: tv. Existing UI (home rails in `HomeScreen.kt`, cards in `Cards.kt`, related rail in `EventDetailsScreen.kt`). No new screen.
**Build hash:** start `bf034323…f0d8` = end `bf034323…f0d8` (skill untouched).
**Render mode:** html-twin (Phase 3 twin, 1920×1080, Playwright/Chromium) + static Kotlin review. No Android toolchain, so the Kotlin was not compiled.

## Root cause (from code, before any skill output)
`RailRow` is a `LazyRow` with `focusRestorer()` and a 25 % pivot `BringIntoViewSpec`. Android auto-repeats `KEYCODE_DPAD_RIGHT` every ~50 ms after the initial delay; each repeat moves focus one card, and the default spring scroll never finishes before the next move, so the track streams past at ~20 cards/s. Nothing in the app paced the repeat. The hero backdrop was already debounced (300 ms), so only the rail itself was the problem.

## Design-context table (`01-inspect.json` vs code)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | tv-rails | KNOWN | collapsible left drawer (`SportsApp.kt`) + immersive hero + horizontal rails; direction later resolved it to `nav-tv-side`, which matches | yes |
| theme | dark-first | KNOWN | `darkColorScheme` only, dark tokens only | yes |
| surfaces | bordered-flat | INFERRED | flat tonal cards on `elevated`; borders are the focus ring (3 dp white) and a 1 dp outline on the EPG tile; accent glow on focus | partial |
| radius | medium (8) | INFERRED | 8 dp cards, 4 dp pills, pill (50 %) buttons | yes |
| spacing | 8 | INFERRED | 8-dp family (8/12/16/20/28) | yes |
| typography | unknown | UNKNOWN | `SportsTypography` is an explicit 10-foot scale 20–74 sp on `FontFamily.SansSerif`, with a documented condensed-display intent; `type_scale: true` was even detected | partial |
| components | compose, compose-tv-material, media3, coil | KNOWN | same | yes |
| tokens | [] | — | `design/tokens.json` exists (semantic dark roles, referenced by README and theme) | no |

## Requirements verdict (`02-requirements.json`)
- platform `tv` — correct (project inspection; `platform_evidence` empty but `known` lists the leanback launcher). input `remote` correct.
- artifact_state `existing` — correct. operations `diagnose, modify` — correct. problem_domain `interaction, visual` — acceptable ("visual" comes from the word "read").
- change_scope `unknown` — acceptable; the sentence does not say.
- mode `audit + refactor` (evidence: "interaction defect on existing UI" / "fix follows the diagnosis") — **acceptable, not ideal**: the sentence is a fix request, `polish`/`refactor` was expected; `audit` pulled in audit-mode recommended concepts (accessible names, contrast) that have nothing to do with the defect.
- scope `in-scope`, domain `UI_INTERACTION`, reason "UI design / interaction task" — correct.
- change_budget `moderate` — high for a one-modifier fix; `small` would have been right. `constraints.preserve_existing_system: true` and `performance_sensitive: true` — good.
- `intent.preserve` `[]` — miss: an existing repo with KNOWN navigation/theme should list them (the direction step then preserved navigation/surface/color anyway).
- accessibility flags all true incl. `reduced_motion: true` — correct, but see concept recall: reduced motion was never demanded as a concept.
- status CONFIDENT, missing [] — correct.

## Guidance verdict (`03-guidance.md/json`, 7 records, ≈1197 tokens)
| record | role | verdict | note |
|---|---|---|---|
| comp-tv-rail | core | relevant | the right component (pivot, focus memory, lazy load) and it carries `perf.focus_latency`, but its text says nothing about key-repeat / hold pacing — the one thing this task needs (**missing-critical**) |
| dir-broadcast-guide-tv | core | off-target | whole-product direction (top tabs, EPG grid, "no glow") for a hold-repeat bug; declared incompatible with `layout-immersive-rails`, which is exactly this codebase (**contradicts-codebase**) |
| comp-mini-player | core | off-target | selected only to cover states/back/safe-margins; unrelated to rail scroll speed (**generic**) |
| tv-typography-distance | guardrail | partial | title size is not the problem; harmless |
| tv-dpad-axes | guardrail | partial | axes rule, nothing about repeat |
| a11y-tv-focus-always | guardrail | partial | "keep focus on screen" is the one line that applies during a hold |
| tv-safe-area | guardrail | off-target | nothing to do with the defect (**generic**) |

Counts: relevant 1 · partial 3 · off-target 3. Purity 0.95 / coverage 1.0 reported by the skill are coverage-of-its-own-demand, not task fit.

**Concept recall** (expected from `00-expectation.json`; delivered = union of `concepts` over the 7 selected records = interaction.focus_restore, perf.focus_latency, layout.media_card, interaction.back_semantics, state.loading_empty_error, tv.safe_margins, tv.ten_foot_typography, interaction.dpad_reachability, interaction.focus_visible, media.details_play_first):
| expected | delivered? | layer if missing |
|---|---|---|
| perf.focus_latency (critical) | yes (comp-tv-rail) | — |
| interaction.dpad_reachability (critical) | yes (tv-dpad-axes) | — |
| interaction.focus_visible | yes (a11y-tv-focus-always) | — |
| a11y.reduced_motion | no | expected-concepts (never in `required_concepts` although `accessibility.reduced_motion=true`) |
| tv.ten_foot_typography | yes | — |

Recall 4/5 = 0.80 · critical 2/2 = 1.00 · forbidden delivered: none.

**Knowledge gap (the real miss, invisible to recall):** no record in the base carries the fix — pacing D-pad auto-repeat / long-press on a rail. `search -k 12` confirms: the nearest records push the *opposite* way for this defect — `tv-focus-performance` ("key events are never dropped or coalesced into jumps") and `motion-focus-scale` ("input must never be dropped while animating (queue focus moves)"). Queuing every 50 ms repeat is precisely what makes the rail fly past. Neither was selected (comp-tv-rail beat tv-focus-performance for `perf.focus_latency`), so the bundle was not harmful, but the skill had nothing to say about the task. Recall counts `perf.focus_latency` as delivered via a record that does not address it.

## Direction verdict (`04-direction.md/json`)
13 slots: preserved 3 (navigation `nav-tv-side`, surface, color) · changed 0 · new 10. `validation.ok = true`. Preserved slots are right. Of the 10 "new — no repository evidence" slots, six describe what the code already does (layout-rails, motion-focus-scale with rail scroll ≤250 ms, focus-scale-glow, cta-focus-selects, imagery-immersive-backdrop, typography-condensed-display) — labelling them "no repository evidence" is a context-detection weakness, not a wrong choice. Two are wrong for this codebase and were ignored:
- **cards → `card-poster-portrait` (2:3)**: the app has 16:9 landscape cards (`cardW 268 × cardH 151`); the 16:9 alternative scored 0.38 and lost. Unjustified.
- **metadata → `metadata-focus-reveal`** (title only on the focused card, 150 ms delayed reveal): the code shows title + subtitle under every card, and for a complaint about *reading titles while holding RIGHT*, hiding titles on unfocused cards would be harmful. Unjustified.
`density-medium` and `icon-filled-system` are defaults, harmless. The motion slot's "rail scroll ≤250 ms" and "focus is the action" matched the codebase and were kept.

## Implementation
Files changed (before-copies under `before/`):
- `app/src/main/java/com/example/tv/ui/theme/SportsTheme.kt` — `SportsDimens.railScrollMs = 220`, `railHoldStepMs = 280L`.
- `app/src/main/java/com/example/tv/ui/home/HomeScreen.kt` — `RailPivotSpec` object → `rememberRailPivotSpec()` (same 25 % pivot; `scrollAnimationSpec` is a fixed 220 ms tween, `snap()` under `LocalReducedMotion`); new `consumeFastDpadRepeat(ev, clock, stepMs)`; `RailRow`'s `LazyRow` gets `.onPreviewKeyEvent { consumeFastDpadRepeat(it, holdClock) }` with a per-rail clock.
- `app/src/main/java/com/example/tv/ui/details/EventDetailsScreen.kt` — the related rail uses the same spec + governor (one system).
- `render/twin.html` (copied from the Phase 3 twin, updated in `p5-09/render/` and written back to `p3-android-tv-compose/render/`) — `consumeFastRepeat()` mirrors the Kotlin, applied to home rails and the details rail; `__twin.HOLD_STEP_MS` exposed.

Behaviour: the first press of a hold always moves; while held, LEFT/RIGHT repeats are admitted at most every 280 ms on the event clock (`nativeKeyEvent.repeatCount > 0`, `eventTime`) and the ones in between are consumed in the preview phase before the focused card sees them. Single presses, UP/DOWN/SELECT/BACK and key-up are untouched. The scroll tween (220 ms) is shorter than the step, so the focused card is always sitting at the pivot when the next step lands. Reduced motion keeps the same pace with an instant scroll. Routes, focus memory, restore logic, ids, semantics, theme and typography are unchanged.

Guidance used: comp-tv-rail's pivot (kept), a11y-tv-focus-always "keep focus on screen" (pivot + bounded tween), direction motion slot "rail scroll ≤250 ms" and requirements' `reduced_motion` flag. Ignored: dir-broadcast-guide-tv, comp-mini-player, tv-safe-area (irrelevant); card-poster-portrait and metadata-focus-reveal (contradict the codebase); the search-visible "never coalesce key events / queue focus moves" advice (wrong for a hold). The pacing itself came from platform knowledge, not from the skill.

## Render (1920×1080)
`render/hold.js` simulates Android's repeat (first press, then a `repeat=true` keydown every 50 ms for 1.5 s) on the "Coming up" rail (EPG tile + 6 cards) and logs focus moves.
- **baseline** (before twin): 6 moves in 254 ms, min gap 49 ms → **19.7 cards/s**; `baseline-hold-mid.png` (400 ms in) already sits on the last card.
- **first/final** (updated twin): gaps 299–303 ms → **3.3 cards/s**; `first-hold-mid.png` is on card 2 with the focused card pinned at the pivot and its title fully legible; `first-hold-end.png` reaches the last card at 1.5 s.
- Full Phase 3 screenshot pass (`render.js`) re-run as `first-*` and `final-*` (10 each): unchanged from Phase 3, single presses still move one card (deep-rail shot lands on the 5th Football card after 4 presses).
- Phase 3 D-pad interaction suite re-run on the updated twin: **23/23 pass** (`05-interaction-p5-09-final.json`) — reachability, focus visibility, restore, BACK semantics, safe margins, reduced motion, type floors intact.

First-render defects: visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0. Final: same. Iterations: 1.
Pre-existing twin limitation, not counted and not changed: the twin's `translateX` pivot does not clamp at the end of the track (a real `LazyRow` cannot scroll past its content), so the last card sits at the pivot with empty space to its right (`*-hold-end.png`, Phase 3's `deep-rail` shot shows the same).

## Preservation
navigation ✓ · theme ✓ · typography ✓ · component reuse ✓ (same `EventCard`, same pivot, same focus memory) · unjustified structural change 0. `preservation-ok`.

## Misses by earliest wrong layer
1. **knowledge-gap** — no record for D-pad auto-repeat / long-press pacing on rails (or grids/EPG); the two nearest records advise the opposite ("never coalesce", "queue focus moves").
2. **expected-concepts** — `a11y.reduced_motion` never demanded although `accessibility.reduced_motion = true` and the task is about motion.
3. **bundle-selection** — `dir-broadcast-guide-tv` and `comp-mini-player` in core for coverage; a product direction and an unrelated component in a 7-record bundle for a one-modifier defect.
4. **requirements** — `intent.preserve` empty on an existing repo with KNOWN navigation/theme; `change_budget` moderate for a small fix.
5. **mode** (minor) — `audit` inferred from "defect on existing UI"; a reported defect is a fix request, and audit mode dragged in unrelated recommended concepts.
6. **context-detection** — `design/tokens.json` not detected; typography UNKNOWN despite an explicit Compose `Typography(...)` scale; surfaces "bordered" when borders are focus rings; direction then labels six slots "no repository evidence" that the code clearly has.
7. **direction** — cards `card-poster-portrait` (code is 16:9) and metadata `metadata-focus-reveal` (would hide the very titles the user wants to read).

## Regressions to propose
- Query: the task sentence verbatim. Expect: a core record about pacing held D-pad LEFT/RIGHT on rails (admit ~3–5 cards/s while held, first press immediate, scroll finishes per step, same pace under reduced motion; optional page-jump/fast-scroll mode for long rails); `a11y.reduced_motion` and `perf.focus_latency` demanded; no product direction record; mode polish/refactor, change_budget small.
- Query: "Holding down on the remote in the guide grid skips whole hours before you can stop." Expect the same pacing concept for EPG grids plus `tv.time_navigation`.
- Query: "Long-press right on the remote should fast-scroll the rail without losing the focused card." Expect pacing + `interaction.focus_visible`, not "queue every key event".
- Inspect regression: a repo with `design/tokens.json` → `tokens` non-empty; a Compose `Typography(...)` with explicit `fontSize` values → typography KNOWN (scale present, system sans).
- Direction regression: repo with `cardW > cardH` / 16:9 `Box(height = cardH)` evidence → cards slot preserved as landscape, never `card-poster-portrait`.

## Tags
`knowledge-gap`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `requirements-miss`, `skill-neutral`, `preservation-ok`, `tooling-limit`
