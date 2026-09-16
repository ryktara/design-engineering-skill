# p6-15 — NorthBank transfer screen: IME type + Send button under the keyboard

**Task sentence (verbatim):** "Typing an amount on the transfer screen brings up the letters keyboard and the Send button disappears under it."

**Project:** `research/phase6-projects/p6-compose-banking/project` · Kotlin / Jetpack Compose / Material 3 (BOM 2025.01.00) · platform **mobile** · existing UI, no new screen · no gradle build available (static review + HTML twin at 390×844).

**Build hash:** start `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`, end identical. Nothing under `design-engineering/` was touched.

**Concurrency:** two other tasks were editing the cards screen and the theme. I touched only `ui/screens/transfer/TransferScreen.kt`. `project/render/twin.html` was overwritten by the account-detail task mid-run, so my twin lives at `project/render/twin-transfer.html` (copy in `render/twin-transfer.html`). Left theirs alone.

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | Both: app shell is a `NavigationBar` bottom-tab Scaffold (`BottomBar.kt`, 4 tabs); each screen additionally has a `TopAppBar`. Candidates show bottom-tabs:5 but top-bar:30 won on raw count | partial |
| theme | dual-theme, default light | KNOWN | `Theme.kt` LightColors + DarkColors, `isSystemInDarkTheme()`, light default | yes |
| surfaces | bordered-flat | INFERRED | `NbCard` = `OutlinedCard`, 1.dp outlineVariant border, no elevation | yes |
| radius | small | INFERRED | `NorthBankShapes` 4/8/12/16/24; `CardCornerRadius = 12.dp`, NbButton uses `shapes.medium` = 12.dp. "small" understates the actual 12.dp surface radius | partial |
| spacing | unknown | UNKNOWN | `Spacing.kt` is an explicit 4-pt grid object (xs 4 … xxl 32, `screen = 16`) with a doc comment telling screens to use it. Clear in code, reported UNKNOWN | **no** |
| typography | custom, tabular numerals | KNOWN | `Type.kt` full Material 3 `Typography` with 13 roles, `FontFamily.Default` | yes |
| components | compose, material3 | KNOWN | correct; the project-local `Nb*` wrapper family was not named | partial |

`spacing = UNKNOWN` is the one confident miss: a dedicated `Spacing.kt` token object is about as legible as a spacing system gets in Compose. Tag: `context-detection-miss`.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Resolved | Verdict |
|---|---|---|
| platform | `mobile`, from project inspection; `platform_evidence: []` | correct (matches expectation) |
| artifact_state | `existing` | correct |
| operations | `diagnose`, `modify` | correct |
| problem_domain | `interaction` | correct |
| change_scope | `local` | correct |
| mode | `audit`, `refactor` — "audit: interaction defect on existing UI / refactor: fix follows the diagnosis" | correct, in `acceptable_modes` |
| scope.kind | `in-scope` (UI_INTERACTION) | correct |
| change_budget | `moderate` | acceptable; `low` would fit a two-line defect fix better |
| intent.preserve | `[]` | acceptable (direction preserves everything anyway) |
| project_context | carried through verbatim, incl. the wrong `spacing=unknown` | inherited miss |
| **`input: ["keyboard", "touch"]`** | "keyboard" extracted from the sentence's *on-screen* keyboard | **wrong sense.** The sentence is about an IME, not physical-keyboard input. This propagated into the bundle (see `interaction-drag-drop` selected to cover `interaction.keyboard_navigation`). Layer: `requirements`. |
| `screen: []`, `screen_subtype: []` | empty | miss — "transfer screen" + amount/reference fields + a Send button is a **form / payment** screen. Had `screen=form` been set, `comp-form` and `feedback.validation_errors` were reachable. Layer: `requirements`. |

Status CONFIDENT, `missing: []`. No platform failure.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

`status=PARTIAL`, bundle = 5 records, **core 0 / critical guardrails 5 / optional 0**, 612 tokens, coverage/1k 8.17, purity 0.75, SPECIFIC 2 / GENERIC 3.

| # | Record | Layer | Verdict | Category | Note |
|---|---|---|---|---|---|
| 1 | `mobile-keyboard-ime` | critical | **relevant** | — | Bullseye. Names both halves of the reported bug: "Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done)… keep the primary action reachable while the keyboard is open". SPECIFIC, 0.559 utility. |
| 2 | `mobile-density-touch` | critical | partial | `generic` | Its `touch.minimum_target` half is true for the Send button (48.dp already); the table→list-row, filter-sheet, bulk-selection body is about a screen this task is not. |
| 3 | `typo-scale-and-roles` | critical | partial | `generic` | Selected as the bundle's only *critical* concept carrier (`table.tabular_figures`). The project already has a full 13-role `Typography` and tabular figures. Says nothing this task needed. |
| 4 | `interaction-drag-drop` | critical | **off-target** | `generic` | Drag-and-drop grips, snapped drop targets, Escape-cancels. Entered only to cover `interaction.keyboard_navigation`, which itself came from the mis-sensed `input=keyboard`. Pure noise for a Compose IME bug — and the largest record in the bundle (`overlong` also applies). |
| 5 | `layout-states-empty-loading-error` | critical | partial | `generic` | Real but unrelated: the transfer screen has no loading/empty state in scope. One true clause ("Error: … keep entered data") is adjacent. |

Layer review: core `[]`, critical `[typo-scale-and-roles, mobile-keyboard-ime, mobile-density-touch, interaction-drag-drop, layout-states-empty-loading-error]`, optional `[]` (optional_useful 0, optional_noise 0).

**An empty CORE layer is the right call here** — the task is a defect fix on an existing screen, there is nothing new to build. No `should-abstain` / `should-not-abstain` defect.

### Concept recall

Expected 5, delivered (union of `concepts` on selected records) 10: `a11y.live_status, brand.type_roles, interaction.keyboard_navigation, perf.layout_shift, state.loading_empty_error, table.column_priority, table.tabular_figures, touch.gestures_discoverable, touch.ime_keyboard, touch.minimum_target`.

| Expected id | Critical | Delivered? | Layer if missing |
|---|---|---|---|
| `touch.ime_keyboard` | yes | **yes** (`mobile-keyboard-ime`, SPECIFIC) | — |
| `form.autofill_attributes` | yes | no | `expected-concepts` — never demanded; absent from `concept_trace` entirely. Its *content* is inside `mobile-keyboard-ime`'s prose ("keyboard type and autocomplete/textContentType/autofillHints per field") but the record is not tagged with the id, so a keyboard-type task can never demand it. |
| `touch.minimum_target` | no | yes (`mobile-density-touch`) | — |
| `feedback.validation_errors` | no | no | `expected-concepts` — never demanded. Transfer errors are Toast-only in this codebase; a finance form screen should have surfaced it. Root cause is `screen: []` (requirements). |
| `interaction.focus_visible` | no | no | `bundle-selection` — demanded as required, candidates `color-states-complete` / `a11y-nontext-contrast` existed, dropped by cap/utility. |

**concept_recall = 2/5 = 0.40 · critical_recall = 1/2 = 0.50.**

**Criticality-layer miss.** The skill's own `critical_concepts` for this query is `['table.tabular_figures']` — and `touch.ime_keyboard`, the concept the sentence is literally about, is merely `required`, `critical: False`. Critical coverage reads 1.0 on the wrong concept. If the bundle cap had bitten one record harder, the one record that mattered had no critical protection. Layer: `criticality`.

`PARTIAL` status note: uncovered required concern is `accessibility` (`interaction.focus_visible`). That split is honest.

## 4. Direction verdict (`04-direction.md` / `.json`)

12 of 13 slots `preserved` with the right reason ("existing system with change budget 'moderate'"); `validation: OK`; preservation metrics list every slot the task does not touch.

One slot `new`: **cta → `cta-single-primary`**, because "no repository evidence for this slot". The screen already has exactly one filled primary button (`NbButton` Primary, `fillMaxWidth`), so the direction is inventing a change where the codebase already complies. **`unjustified_direction_slots = 1`** (expected 0 on an existing UI at moderate budget).

Worse, the *alternatives considered* list shows `cta-sticky-bar` (0.344) ranked just below `cta-single-primary` (0.353). A sticky/pinned action bar is precisely the standard answer to "the primary action disappears under the keyboard", and `mobile-keyboard-ime` itself offers it ("or on the keyboard toolbar"). The direction layer picked the one CTA record that had nothing to do with the request over the one that did. Tag: `direction-mismatch`.

## 5. Implementation

**Files changed: 1** — `app/src/main/java/com/northbank/app/ui/screens/transfer/TransferScreen.kt` (copy in `before/`).
**Files added: 1** — `project/render/twin-transfer.html` (render harness, not app code).

Root cause, from the code:

1. The Amount `OutlinedTextField` had **no `keyboardOptions`**, so Compose defaults to `KeyboardType.Text` → the alphabetic IME on a currency field.
2. The Scaffold content `Column` is `fillMaxSize().padding(padding).verticalScroll(...)` with **no IME inset handling**. The manifest is `adjustResize` and `MainActivity` calls `enableEdgeToEdge()`, which opts the window out of automatic inset fitting — so the IME simply draws over the bottom of the scroll viewport and the `NbButton` at the end of the column is unreachable, not just off-screen.

Change:

- `keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal, imeAction = ImeAction.Next)` on the Amount field.
- `keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done)` + `keyboardActions = KeyboardActions(onDone = { keyboard?.hide() })` on the Reference field (`LocalSoftwareKeyboardController`).
- `.imePadding()` inserted **between** `.padding(padding)` and `.verticalScroll(...)` so the scroll viewport shrinks by the IME height and Send scrolls above the keyboard.

Nothing else changed: routes, `TransferViewModel`, state, `NbCard`/`NbButton`/`Spacing`/theme usage, string resources, content descriptions all untouched. No new component, no new token.

**Guidance used:** `mobile-keyboard-ime` — all three of keyboard type, Next/Done return action, and "keep the primary action reachable while the keyboard is open" came straight from it. The Next/Done wiring on Reference is the part I would plausibly have skipped.
**Guidance ignored:** `interaction-drag-drop` (no drag-and-drop on this screen), `typo-scale-and-roles` (type system already complete; changing it is out of budget and owned by a concurrent task), `layout-states-empty-loading-error` (no loading/empty state in this change), `mobile-density-touch` table/filter clauses (no table here; the touch-target clause was already satisfied at 48.dp).

**Process guidance check.** SKILL.md §2 / §7 were sufficient — I reused `NbButton`/`NbCard`/`Spacing` and rendered-and-inspected without `impl-reuse-before-new`, `impl-safe-modification` or `verify-render-and-inspect` in the bundle. `process.reuse_first` shows as "not surfaced" in the trace and its absence cost nothing. `process_records_needed: false`.

## 6. Render

**Mode: `html-twin`** (no gradle/Android SDK build available). `render/twin-transfer.html` mirrors `TransferScreen.kt` structure and the `ui/theme/*.kt` tokens; Playwright 1.63.0 / Chromium at **390×844**, dsf 2.

- `render/baseline-390x844-{idle,ime}.png` — the twin with the pre-fix code path (`KeyboardType.Text`, no `imePadding`). The IME-open shot reproduces the report exactly: QWERTY keyboard, Send button nowhere on screen.
- `render/first-390x844-{idle,ime}.png` — first render of the implemented fix.
- `render/final-390x844-{idle,ime}.png` — after re-render (identical; no fix iteration was needed).

**First-render defects (of my implementation): 0** — visual 0, interaction 0, accessibility 0, platform 0, existing-system-mismatch 0, implementation-bug 0. The IME-open shot shows the decimal keypad and the full-width Send button clear of the keyboard; the idle shot is pixel-equivalent to baseline idle, so the change is inert when no field is focused. **Final defects: 0. Iterations: 1.** Stated plainly: the fix was right the first time, so first and final are the same; the interesting comparison is baseline vs first.

Twin limits (`tooling-limit`): the twin cannot prove `imePadding()` modifier ordering or that `LocalSoftwareKeyboardController` resolves under this BOM — those rest on static review, and no compile was possible.

## 7. Preservation

navigation ✔ · theme ✔ · typography ✔ · component reuse ✔ (`NbButton`, `NbCard`, `Spacing` untouched) · unjustified structural changes **0**. Nothing outside the transfer screen was edited. `preservation-ok`.

## 8. Skill effect

**helped.** `mobile-keyboard-ime` is a direct, SPECIFIC hit that named both halves of the defect plus the Next/Done detail I would have under-specified. But 4 of 5 records were noise, the criticality layer protected `table.tabular_figures` instead of `touch.ime_keyboard`, and the direction layer proposed a CTA change the codebase already satisfied while ranking the genuinely relevant `cta-sticky-bar` below it.

## 9. Misses by earliest layer

| Layer | Miss |
|---|---|
| `requirements` | `input=keyboard` extracted from "letters keyboard" as physical-keyboard input, not IME. Pulled `interaction.keyboard_navigation` into required concepts, which pulled `interaction-drag-drop` into the bundle. |
| `requirements` | `screen: []` on a sentence naming "the transfer screen" with amount/reference fields and a Send button — no form/payment screen type, so `comp-form` and `feedback.validation_errors` were never reachable. |
| `criticality` | Only critical concept is `table.tabular_figures`; `touch.ime_keyboard` is non-critical on a query that is entirely about the IME. |
| `expected-concepts` | `form.autofill_attributes` never demanded for an input-type defect (and not tagged on `mobile-keyboard-ime`, which carries its content). |
| `bundle-selection` | `interaction.focus_visible` demanded, candidates existed, dropped. |
| `direction` | `cta` slot marked `new` with `cta-single-primary` on a screen that already has one primary button; `cta-sticky-bar`, the task-relevant option, ranked 0.009 lower. |
| `project-context` | `spacing=UNKNOWN` despite an explicit `Spacing.kt` 4-pt token object. |

## 10. Regressions to propose

1. **query:** "Typing an amount on the transfer screen brings up the letters keyboard and the Send button disappears under it." — **expect:** `touch.ime_keyboard` marked *critical*, not merely required; and `form.autofill_attributes` in required concepts.
2. **query:** same — **expect:** `interaction-drag-drop` not in the bundle. No drag affordance exists or is asked for; it enters only via a mis-sensed `input=keyboard`.
3. **query:** "the amount field on the transfer screen opens the wrong keyboard" — **expect:** requirements resolve `screen` to `form`/`payment` (currently `[]`), so `comp-form` and `feedback.validation_errors` become reachable.
4. **query:** same as (1), direction — **expect:** if any CTA record is chosen, `cta-sticky-bar` over `cta-single-primary`; ideally the `cta` slot stays `preserved` on an existing UI at moderate budget (`unjustified_direction_slots = 0`).
5. **project inspection:** a Compose project with a `Spacing`/`Dimens` object of named dp values — **expect:** `design_context.spacing` KNOWN with a 4-pt-grid value, not UNKNOWN.
6. **project inspection:** a Compose app whose shell is `Scaffold(bottomBar = NavigationBar)` with per-screen `TopAppBar` — **expect:** navigation reported as bottom-tabs (or bottom-tabs + top-bar), not top-bar on raw match count.

## Tags

`skill-helped`, `requirements-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `preservation-ok`, `partial-scope-ok`, `tooling-limit`
