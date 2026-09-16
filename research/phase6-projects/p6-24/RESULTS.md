# p6-24 — "Pressing back on the detail page throws you out of the app."

- **Task sentence (verbatim):** `Pressing back on the detail page throws you out of the app.` (no mode word)
- **Project:** `research/phase3-projects/p3-android-tv-compose/project` — Android TV, Kotlin + Jetpack Compose + `androidx.tv:tv-material` + Media3 + Coil, leanback-only launcher.
- **Platform:** tv · **Existing UI** (not a new screen).
- **Build hash start/end:** `ea8eed72…5d9947` / `ea8eed72…5d9947` — equal, matches the c3 freeze.

## 1. Design context (`01-inspect.json`) vs the code

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | `tv-rails` | KNOWN | Collapsed side drawer (`ModalNavigationDrawer`, `NavSection`) + a rail column of `LazyRow`s on Home | yes |
| theme | `dark-first` | KNOWN | `darkColorScheme`, canvas `#0B1220`, no light scheme at all | yes |
| surfaces | `bordered-flat` | INFERRED | Cards/buttons are 3 dp bordered flat fills; the only "elevation" is gradient scrims over artwork | yes |
| radius | `pill` | INFERRED | Pills for badges and action buttons; cards are 16 dp rounded rectangles — "pill" is the modal value, not the card value | partial |
| spacing | `8` | INFERRED | `SportsDimens` uses 8/12/16/20/24/28/48; base 8 is right | yes |
| typography | `custom` | KNOWN | Custom `Typography` with a documented 10-foot scale over `FontFamily.SansSerif` (`DisplayCondensed`/`BodySans` swap points) | yes |
| components | `compose, compose-tv-material, media3, images:coil` | KNOWN | Exactly that | yes |

No context-detection failure that mattered for this task. `radius` is the one modal-value-over-mixed-system case.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Resolved | Expected | Verdict |
|---|---|---|---|
| platform | `tv` (project inspection, `platform_evidence: []`) | tv | **correct** — resolved from the repository, not the sentence; the sentence alone has no platform word and `search` correctly emits `MISSING: platform` when run without `--project` |
| artifact_state | `existing` | existing | correct |
| operations | `diagnose`, `modify` | diagnose + fix | correct |
| problem_domain | `[]` | navigation/interaction | **weak** — the domain list is empty on a sentence that names a concrete interaction defect ("pressing back … throws you out") |
| change_scope | `screen` | screen (with an app-shell fix) | acceptable; the real fix lives in the shell, not the detail screen |
| mode | `audit`, `refactor` | refactor/polish/audit | correct; `mode_evidence` is honest ("problem statement on existing UI" / "fix follows the diagnosis") |
| scope.kind | `in-scope` | in-scope | correct — remote BACK layering is a TV interaction contract, not a pure engineering bug |
| change_budget | `moderate` | low–moderate | correct |
| intent.preserve | `[]` | navigation, theme, typography, focus memory | **miss** — nothing was demanded preserved, even though `constraints.preserve_existing_system: true` is set |
| project_context | full, correct | — | correct |

`activation.decision` is `ambiguous` (ui 1.0 / non-ui 1, "page" vs "throws") yet `scope.kind` still lands on `in-scope`. Right answer, thin evidence.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

`status=PARTIAL` (uncovered required concern `performance`), bundle = 6 records, **core 0 / guardrails 6 / optional 0**, ≈700 tokens, purity 0.94.

| Record | Layer | Verdict | Category | Note |
|---|---|---|---|---|
| `tv-back-behavior` | guardrail | **relevant** | — | The record for this request. Gives the full ladder (player controls → player → detail → home → nav → exit) and "deep-linked entries still unwind to the app home". |
| `a11y-tv-focus-always` | guardrail | **relevant** | — | "restore focus to the previously focused item when returning" is the other half of a correct BACK; drove the focus-restore check in the render. |
| `tv-dpad-axes` | guardrail | partial | `generic` | True for the app, says nothing a BACK fall-through needed. |
| `tv-safe-area` | guardrail | partial | `generic` | Only used to grade the twin, not the change. |
| `tv-typography-distance` | guardrail | **off-target** | `generic` | 10-foot type has no bearing on BACK. Pure TV-platform boilerplate: it entered on `platform=tv`, not on any task evidence. |
| `layout-states-empty-loading-error` | guardrail | **off-target** | `generic` | Loading/empty/error states are not what "back throws you out" is about; the codebase already enumerates them (`HomeUiState`). |
| *(bundle level)* | — | — | `missing-critical` | `navigation.orientation_and_back` — the pre-registered critical concept "back returns to the previous screen with its scroll and selection" is absent from the bundle. |

Counts: **relevant 2 · partial 2 · off-target 2.** Four of six guardrails are platform boilerplate for a single-concept request; a 2-record bundle would have been strictly better here, and the cap (soft 6) appears to have been *filled* rather than *reached*.

### Concept recall

Expected 6 · delivered-from-expected 4 → **recall 0.67**. Critical 2 · delivered 1 → **critical recall 0.50**.

| Expected concept | Delivered? | Carrier | Layer if missing |
|---|---|---|---|
| `interaction.back_semantics` (critical) | yes | `tv-back-behavior` (SPECIFIC) | — |
| `navigation.orientation_and_back` (critical) | **no** | — | `expected-concepts` |
| `interaction.focus_restore` | yes | `a11y-tv-focus-always` (SPECIFIC) | — |
| `media.details_play_first` | yes | `a11y-tv-focus-always` | — |
| `interaction.dpad_reachability` | yes | `tv-dpad-axes` (SPECIFIC) | — |
| `navigation.platform_grammar` | **no** | — | `knowledge-gap` |

Routing of the two misses:

- `navigation.orientation_and_back` → **`expected-concepts`**, not `bundle-selection`. It never appears in the concept trace at all — neither `covered` nor `UNCOVERED` — so it was never demanded. The carrier exists and is healthy: `nav-orientation-and-back` ranks **5th** in `search -k 12` (score 0.398) on this exact sentence. The planner did not ask for it; ranking then had no reason to keep it.
- `navigation.platform_grammar` → **`knowledge-gap`**. The only records carrying it are `nav-bottom-tabs` and `mobile-platform-navigation`, both mobile. Nothing in the base carries "platform navigation grammar" for TV, so even if it had been demanded nothing could have delivered it.

Concepts delivered but not expected: `interaction.focus_visible`, `tv.ten_foot_typography`, `tv.safe_margins`, `state.loading_empty_error`. Only the first is on-task.

None of the forbidden concepts were delivered — the platform filter correctly dropped `comp-product-detail-page`, `comp-kpi-tile`, `media-photo-viewer` etc., and `comp-tv-sign-in` / EPG / search records never entered. **No off-platform and no wrong-product defects.** `media-resume-and-details` was omitted for low purity (0.33) despite being the single most task-adjacent media record; that omission was right for token economy but it is also the record that would have carried "BACK returns to the row that launched the details".

### Process guidance check

**Not needed.** SKILL.md §2 (inspect and reuse before adding) and §7 (render and inspect) were sufficient: I copied every touched file to `before/` first, reused `Route`/`HomeFocusMemory` conventions rather than introducing a navigation library, and rendered before claiming the fix. `process.reuse_first` is listed in `not_surfaced` and its absence cost nothing. → `process_records_needed: false`.

## 4. Direction verdict (`04-direction.md`)

12 of 13 slots `preserved` with correct repository reasons; `validation: OK`; preservation metrics list every slot as preserved.

**`unjustified_direction_slots: 1`** — `cards` is marked **`new`** ("No card containers (dividers and spacing)", reason "no repository evidence for this slot") on an existing UI with a `moderate` budget and a task that has nothing to do with card geometry. The repository *does* have evidence: `Cards.kt`, `surfaces=bordered-flat`, `SportsDimens.cardW/cardH`. Following it would have deleted the rail cards. Ignored.

The per-slot navigation guidance was accurate and useful as a statement of the existing contract ("Back from content returns to the drawer, Back from the drawer exits or goes Home") and it matches the code.

## 5. Implementation

Root cause, from static review of the shell (the detail screen itself is fine — `EventDetailsScreen.kt:94` already has `BackHandler { onBack() }`):

1. **No back stack.** `SportsApp` held a single `var route: Route`. BACK correctness depended entirely on each screen happening to own an *enabled* `BackHandler`. Any route that does not — a new screen, a screen whose handler is conditionally disabled — falls through to the Activity default, which is `finish()`. That is exactly the reported symptom, one missing handler away at all times.
2. **Stale `navHasFocus`.** `onFocusChanged { navHasFocus = it.hasFocus }` on the drawer never fires on dispose. Leave Home from the drawer (SELECT "Guide" → `leaveHome(Route.Guide)`) and the flag stays `true`; on return, `BackHandler(enabled = navHasFocus) { onExit() }` is armed while focus sits on a rail tile, and `HomeScreen`'s `backEnabled = !navHasFocus` is simultaneously disabled — so the *next* BACK exits the app instead of stepping rails → hero → nav. Reproduced in the twin (`render/evidence-before-stale-exit.png`).
3. **Exit was not a root decision.** Nothing asserted "only the Home root may finish the Activity".

Change (2 files, both copied to `before/` first):

- `ui/AppState.kt` — added `class NavStack`: `mutableStateListOf(Route.Home)`, `current`, `atRoot`, `push`, `replaceTop`, `pop` (returns false at the root), `popToRoot`. Home is the root and is never popped.
- `ui/SportsApp.kt` —
  - `var route` → `val nav = remember { NavStack() }`; `leaveHome` pushes, `returnHome` pops, `onOpenRelated` uses `replaceTop` (preserves the codebase's documented "related re-targets, does not deepen" contract), player `onBack` uses `popToRoot` (preserves the documented "player → Home with the stream in the mini player" contract).
  - App-level fallback `BackHandler(enabled = !nav.atRoot) { nav.pop() }` composed **first** inside `SportsTheme`, so it is the lowest-priority callback: every screen's own handler still wins, and a screen without one loses a layer instead of finishing the Activity.
  - Exit gated on `navHasFocus && nav.atRoot`.
  - `navHasFocus` cleared in `leaveHome(...)` and by a `DisposableEffect(Unit) { onDispose { navHasFocus = false } }` inside the drawer column.

Routes, ids, focus memory, theme, typography, `HomeScreen`/`EventDetailsScreen`/`PlayerScreen` signatures and all accessibility semantics are untouched.

**Guidance used:** `tv-back-behavior` (the layering ladder and "exit is the last layer"), `a11y-tv-focus-always` (verified focus restoration survives the change), `tv-safe-area` (grading the twin).
**Guidance ignored:** `tv-typography-distance` and `layout-states-empty-loading-error` (nothing to do with the task); `tv-dpad-axes` (already satisfied, no change needed); and one clause *inside* `tv-back-behavior` — its ladder puts `player → detail`, while this codebase deliberately does `player → home` so the stream lands in the mini player. The existing documented contract wins under a `moderate` budget. The `cards: new` direction slot was ignored as unjustified.

## 6. Render

**Mode: `html-twin`** at 1920×1080 (Playwright 1.63.0 / Chromium, `render/twin.html` + `render/shoot.js`). No capture harness exists for this Compose project and no `project/render/twin.html` was present, so the twin was authored for this task at dp×2 against `SportsTheme.kt` tokens. It models Home / Details / Player / Guide, the drawer, focus keys, `HomeFocusMemory`, the `NavStack`, and an explicit "APP EXITED" state; `?v=before` runs the pre-change logic so the defect is visible rather than asserted. Every screenshot below was opened and inspected.

Scenarios captured (both passes): details opened · BACK on details · BACK on player · BACK on a screen with **no** handler of its own · the stale-`navHasFocus` sequence · BACK at the root with drawer focus (must still exit). Evidence of the old behaviour: `evidence-before-details-exit.png`, `evidence-before-stale-exit.png` — both land on "APP EXITED".

### First-render defects (5)

| Type | Defect |
|---|---|
| platform | The collapsed side-nav strip was drawn on the Details route; in `SportsApp.kt` the drawer is composed only under `Route.Home` and Details is full-screen. |
| interaction | The twin did not restore focus to the launching tile on BACK from Details — the very guarantee under test was left unverified (`first-02`). |
| accessibility | The focus ring on the accent primary action read as a dark edge over the yellow fill, not a visible ring (`.btn.primary` border vs the glow). |
| visual | Details backdrop was flattened to near-invisible by a full-width scrim. |
| visual | Home rail bottom edge sat ~30 px from the frame bottom, inside the 54 px (27 dp) vertical overscan margin. |

Counts — visual 2 · interaction 1 · accessibility 1 · platform 1 · existing-system-mismatch 0 · implementation-bug 0.

None of these were in the Kotlin change; all five were twin-fidelity defects, and two of them (safe area, focus visibility) were caught *by* guardrails that were in the bundle — `tv-safe-area` and `a11y-tv-focus-always`. The safe-area one is a defect the guidance explicitly warned about and I shipped anyway on the first pass: that counts against me, not the skill.

### Iterations: 2. Final defects (1)

| Type | Defect |
|---|---|
| visual | The focused rail card's 1.08 scale outline slightly overlaps the "Live now" rail title. The app reserves `SportsDimens.focusPadding = 12.dp` for exactly this; the twin does not reserve it above the rail title. Twin-only, not a defect in the app. |

Counts — visual 1 · everything else 0.

Behaviour verified in the final pass: BACK on Details → Home with focus restored to the Celtics @ Knicks tile (`final-02`); BACK on a handler-less screen → Home, not exit (`final-04`); the stale-flag sequence → focus moves to the nav instead of exiting (`final-05`); BACK at the root with drawer focus → still exits (`final-06`).

## 7. Preservation

navigation preserved · theme preserved · typography preserved · component reuse yes (no new UI components; `NavStack` sits beside the existing `Route`/`HomeFocusMemory` state classes) · **unjustified structural changes: 0** · `preservation-ok`.

## 8. Skill misses, routed to the earliest wrong layer

| Layer | Miss |
|---|---|
| `requirements` | `intent.problem_domain` empty and `intent.preserve` empty on a sentence that states a concrete navigation defect on an existing system with `preserve_existing_system: true`. |
| `expected-concepts` | `navigation.orientation_and_back` (pre-registered **critical**) was never demanded, although its carrier `nav-orientation-and-back` ranks 5th in `search -k 12` on this sentence. |
| `candidate-retrieval` | *(no miss)* — for `navigation.platform_grammar`, see below; retrieval behaved. |
| `bundle-selection` | Four of six guardrails (`tv-typography-distance`, `layout-states-empty-loading-error`, `tv-safe-area`, `tv-dpad-axes`) are platform/heuristic boilerplate admitted on `platform=tv` alone against a single-concept request; the soft cap of 6 was filled, not reached. |
| `direction` | `cards` slot returned `new` ("no repository evidence") on an existing UI with a moderate budget and visible card evidence in the repository (`Cards.kt`, `surfaces=bordered-flat`). |

Knowledge gap: no record in the base carries `navigation.platform_grammar` for TV (only mobile `nav-bottom-tabs` / `mobile-platform-navigation`).

## 9. Skill effect

**`neutral`.** `tv-back-behavior` states the correct layering ladder — but `SportsApp.kt`'s own KDoc already cites `tv-back-behavior` and reproduces the same ladder verbatim, and `HomeFocusMemory` already implements focus restoration. Nothing in the bundle told me something I would plausibly have missed or under-specified; the actual fix came from reading the shell code (stale `navHasFocus`, no root guard), not from the guidance. Nothing in the bundle led to a change I reverted either — the one harmful suggestion (`cards: new`) came from the **direction**, not the guidance, and was never applied. Hence neither `helped` nor `hurt`.

## 10. Regressions to propose

1. **Query:** `Pressing back on the detail page throws you out of the app.` (with a TV project context) — **expect:** the bundle delivers `navigation.orientation_and_back` (via `nav-orientation-and-back`, which already ranks 5th in search), and does **not** contain `tv-typography-distance` or `layout-states-empty-loading-error`. A BACK defect must not pull 10-foot typography.
2. **Query:** `back button on the TV details screen closes the app` — **expect:** a bundle of ≤4 records, all from interaction/navigation/accessibility; no typography, no safe-area, no empty-state filler. Single-concept requests should produce small bundles; an empty layer is a valid result under Phase 6.
3. **Query:** any TV navigation request — **expect:** at least one record carrying `navigation.platform_grammar` that applies to `platform=tv`; today only mobile records carry it.
4. **Direction:** existing UI, `change_budget=moderate`, repository `surfaces=bordered-flat` with a components directory containing cards — **expect:** the `cards` slot resolves `preserved`, not `new`.

## 11. Tags

`concept-miss` · `ranking-miss` · `knowledge-gap` · `requirements-miss` · `direction-mismatch` · `render-defect-fixed` · `render-defect-remaining` · `skill-neutral` · `preservation-ok`
