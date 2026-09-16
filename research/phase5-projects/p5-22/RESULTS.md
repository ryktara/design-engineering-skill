# p5-22 — "Make the Add Habit sheet work when the keyboard is up."

- **Task:** p5-22 (sentence run verbatim).
- **Project / stack / platform:** `p5-swiftui-habits` — SwiftUI, iOS 17, Swift 5.9; mobile (iPhone 390×844). Bottom tabs, dual light/dark theme via `Theme.Palette` `Color(light:dark:)`, Nunito with `.rounded` fallback, elevated cards, radius 16/10, spacing 4/8/12/16/24.
- **Existing UI or new screen:** existing UI — `Views/AddHabitSheet.swift` (a `Form` inside a `.sheet` with `.presentationDetents([.large])`), presented from `HabitsView` via the `+` toolbar button. p5-20 (StatsView chart track) and p5-21 (WeeklySummaryCard on Today) changes were left in place and re-verified in the twin.
- **Build hash:** start `bf034323…0d8` = end `bf034323…0d8` (equal). Nothing under `design-engineering/` was touched.
- **Render mode:** `html-twin` (`project/render/twin.html`, Playwright 1.63.0 Chromium, 390×844 @2x, light + dark) + static Swift review. No Xcode available.

## Reviewer expectation (written before any advise run — `00-expectation.json`)

Platform mobile · existing · modes polish / refactor / responsive · in-scope. Expected concepts: `touch.ime_keyboard` (critical), `touch.safe_areas` (critical), `layout.one_primary_action`, `touch.thumb_reach`, `a11y.dialog_focus`, `process.safe_modification`, `process.reuse_first`. Forbidden: hardware-keyboard / desktop / TV concepts (`interaction.keyboard_navigation`, `interaction.shortcuts`, `interaction.dpad_reachability`, `desktop.spacing_grid`, `tv.no_touch_hover`, `brand.dark_mode_redesign`, `adaptive.breakpoint_matrix`).

Symptoms read from the code with the keyboard up: the `TextField` has no `@FocusState`, no `submitLabel`/`onSubmit`, the `Form` has no `scrollDismissesKeyboard`, and the in-form `PrimaryButton` (last section) sits under a ~336 pt keyboard, so the primary action is unreachable without scrolling or using the nav-bar `Save`.

## Design-context table (`01-inspect.json`)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | bottom-tabs | KNOWN | `RootTabView` `TabView` with 4 tabs, each its own `NavigationStack` | yes |
| theme | dual-theme | INFERRED (evidence "hex palette: 0 near-white, 0 near-black") | Dual theme, explicit: `Color(light:dark:)` for every token + `Assets.xcassets/Colors` light/dark appearances. Swift `0xRRGGBB` hex is not parsed, so the evidence is wrong and the status should be KNOWN | partial |
| surfaces | elevated | INFERRED | Elevated cards (`cardSurface`: surface + shadow 0.08/16/6) | yes |
| radius | medium ("most common radius 8 (1×)") | INFERRED | 16 global, 10 chips (`Theme.Shape`); the "8" is the twin's `.time` chip only | partial |
| spacing | 4 | INFERRED | 4-pt base, 4/8/12/16/24 | yes |
| typography | humanist-sans (Nunito 1 ref; "monospace usage") | INFERRED | Nunito via `Theme.Typography`, `.rounded` fallback; no monospace anywhere | partial |
| components | unknown | UNKNOWN | `Components/` with HabitCard, PrimaryButton, ProgressRing, WeeklySummaryCard | partial |

`product_hints = ['ecommerce']` again (README of a habit tracker) — the same context-detection bug recorded in p5-21; it drives the guidance and direction below.

## Requirements verdict (`02-requirements.json`)

| item | resolved | verdict |
|---|---|---|
| platform | `mobile` (Package.swift iOS target); `platform_evidence: []` | correct |
| `intent.artifact_state` | `new` | **wrong** — the sheet exists; `intent.existing=false`, `intent_evidence.existing=[]` |
| `intent.operations` | `["create","modify"]` | **wrong** — `create` was triggered by the token "add" inside the proper noun "Add Habit"; only `modify` is right |
| `intent.problem_domain` | `["interaction"]` (from "keyboard") | acceptable |
| `intent.change_scope` | `unknown`; `change_budget: moderate` | acceptable |
| mode + evidence | `create` — "build/create request" | **wrong** — expected polish / refactor / responsive; "make … work" is a fix |
| `scope.kind` | `in-scope`, domain UI_INTERACTION | correct |
| input | `keyboard` KNOWN ("request: keyboard"), `touch` inferred | **misread** — on a phone "the keyboard is up" is the IME; the skill treated it as hardware keyboard and demanded `interaction.keyboard_navigation`, `interaction.focus_visible`, `interaction.shortcuts` (all in my forbidden list); `touch.ime_keyboard` was never demanded |
| product | `ecommerce` KNOWN (project README) | wrong (inspect bug) |
| components | `dialog`; `primary_jobs: ["create dialog"]` | partial — sheet ≈ dialog is fine; "create dialog" is not the job |
| `intent.preserve` | `[]` | weak — should preserve the sheet, its form, toolbar actions |
| `project_context` | as in the table above | partial |

## Guidance verdict (`03-guidance.md/json`, ≈1156 tokens, 3 core + 3 guardrails)

| record | role | verdict | BAD category | why |
|---|---|---|---|---|
| `comp-product-detail-page` | core | off-target | contradicts-codebase | PDP for a habit-name form; picked via the `ecommerce` product tag and `touch.minimum_target`. Its one sentence "sticky add-to-cart on phones without covering focused controls" is the only echo of the actual task, buried in a page about galleries and reviews. |
| `comp-drawer-panel` | core | off-target | contradicts-codebase | A `.sheet` is not a drawer; the swiftui note recommends `.inspector`/`NavigationSplitView`, wrong for this app. |
| `comp-dialog` | core | partial | — | "one primary action, scroll inside the body" applies to the sheet; nothing about the keyboard. |
| `mobile-platform-navigation` | guardrail | off-target | generic | "sheets for secondary tasks" — already the case; no bearing on the keyboard. |
| `a11y-modal-dialog` | guardrail | relevant | — | "On open: focus the first meaningful control" — matches the `defaultFocus` decision. Tab-trap / Escape wording is web-flavoured. |
| `a11y-nontext-contrast` | guardrail | off-target | generic | Selected only to cover `interaction.focus_visible`, which was demanded because "keyboard" was read as hardware keyboard. |
| (bundle) | — | — | missing-critical | `mobile-keyboard-ime` (search rank #4, score 0.388, platform mobile, input touch, concept `touch.ime_keyboard`: "return key action Next/Done, scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open, never let the keyboard cover the submit button") is the exact answer and is absent. `mobile-safe-areas`, `mobile-thumb-reach`, `impl-reuse-before-new` were candidates and dropped. |

Counts: relevant 1 · partial 1 · off-target 4. Status CONFIDENT (not PARTIAL_SCOPE).

### Concept recall

Delivered (union over the 6 selected records): `a11y.accessible_names, a11y.contrast, a11y.dialog_focus, feedback.confirmation_destructive, feedback.trust_signals, interaction.drawer_focus, interaction.focus_restore, interaction.focus_visible, layout.one_primary_action, navigation.platform_grammar, perf.layout_shift, touch.minimum_target`.

| expected | delivered? | earliest wrong layer |
|---|---|---|
| `touch.ime_keyboard` (critical) | no | **expected-concepts** — absent from `concept_trace` entirely; carriers exist (`mobile-keyboard-ime`, `comp-form`, `comp-checkout-one-page`) |
| `touch.safe_areas` (critical) | no | bundle-selection — recommended, candidate `mobile-safe-areas` (0.339) dropped ("bundle cap or lower utility") |
| `layout.one_primary_action` | yes (via PDP) | — |
| `touch.thumb_reach` | no | bundle-selection — candidate `mobile-thumb-reach` (0.405) dropped |
| `a11y.dialog_focus` | yes | — |
| `process.safe_modification` | no | expected-concepts — never demanded; `impl-safe-modification` exists (intent includes refactor/polish, not reached because mode = create) |
| `process.reuse_first` | no | bundle-selection — `impl-reuse-before-new` (0.264) dropped |

Recall 2/7 = **0.29**; critical recall 0/2 = **0.0**. Knowledge gaps: none — every expected concept has a record in the base (checked in `data/*.jsonl` and `03-search.txt`).

## Direction verdict (`04-direction.md/json`, exit 3 — VIOLATIONS)

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-bottom-tabs | preserved | yes |
| layout | layout-grid-catalog | new | no — a catalog grid for a form sheet |
| density | density-medium (from 4-pt) | changed | no — nothing in the task touches density |
| surface | surface-elevated-cards | preserved | yes |
| cards | card-poster-landscape | new | no — validator itself flags "non-media product: poster card geometry"; emitted anyway |
| typography | typography-humanist-sans | preserved | yes |
| color | color-neutral-accent | preserved | yes |
| motion | motion-spring | new | not asked; harmless |
| focus | focus-none-touch-only | new | acceptable for touch, but it contradicts the guardrail that demanded `focus_visible` |
| cta | cta-sticky-bar | new | coincidentally right: "bottom-fixed on mobile inside the safe area; the bar must not obscure a focused field, scroll the field into view above it" — this is the closest the skill came to the task, reached through the ecommerce/PDP path, not the sentence |
| imagery / icon / metadata | thumbnails / filled / inline-badges | new | no — no imagery, no badges in the sheet |

Preservation: 4 preserved, 1 changed (density, unjustified), 8 new (7 unjustified). Validation `ok=false`.

## Implementation

Files changed (before-copies in `before/`):

- `Sources/Streaks/Views/AddHabitSheet.swift`
  - `@FocusState nameFieldFocused`; `TextField` gets `.focused`, `.submitLabel(.done)`, `.onSubmit { nameFieldFocused = false }`.
  - `.defaultFocus($nameFieldFocused, true)` so the name field takes focus when the sheet is presented (iOS 17 API; static review only, see caveats).
  - `Form.scrollDismissesKeyboard(.interactively)`.
  - `PrimaryButton("Save habit")` moved from the last `Form` section into `.safeAreaInset(edge: .bottom)` with `theme.spacing` padding, `theme.color.background`, and a `theme.color.separator` hairline (`theme.shape.hairline`) on top — same edge treatment as the tab bar. The inset keeps the button above the keyboard and gives the Form matching bottom padding.
  - `save()` drops focus before dismissing.
  - Unchanged: sections, icon grid, segmented picker, reminder rows, toolbar Cancel/Save, `.presentationDetents`, `.presentationCornerRadius`, all theme tokens.
- `render/twin.html`: `#add-habit` restructured (form = scroll region, `.save-bar` below it, home indicator); new `#add-habit-keyboard` section (name focused with caret, "Stretch" typed, sheet bottom = 336 px, iOS-style 336 px keyboard with QuickType bar and a `done` return key). Today and Stats sections untouched.

Guidance used: `a11y-modal-dialog` "focus the first meaningful control on open" (confirms `defaultFocus`); `comp-dialog` "one primary action" (kept the single pinned button; nav-bar Save stays because it is the app's existing convention). The `cta-sticky-bar` direction slot agrees with the pinned inset but I had already chosen it from `mobile-keyboard-ime`'s text in the raw search (which the bundle dropped).

Guidance ignored: PDP, drawer/inspector, catalog grid, poster cards, density change, imagery/badges, non-text-contrast-for-focus-ring (touch-only sheet), `interaction.keyboard_navigation` (hardware keyboard on a phone). Not added: a keyboard-toolbar "Done" button — the return key already reads Done, so a second bar would be 44 pt of redundant chrome above the pinned button.

## Render

Screenshots (`render/`): `baseline-addhabit-keyboard-{light,dark}.png` (pre-change twin with a 336 px keyboard injected — Save button is below the keyboard, only "Reminder" header visible above it), `first-addhabit-{light,dark}.png`, `first-addhabit-keyboard-{light,dark}.png`, `final-*` same four. Measured in the final twin: save bar y 471–540 (69 px = 52 button + 8 + 8 + 1 hairline), keyboard y 540–876, phone bottom 876.

First-render defects:

| type | count | what |
|---|---|---|
| visual | 2 | (1) pinned Save bar had no edge — the Frequency card was chopped flush against it; (2) twin-only: dark-theme `done` key rendered grey because `:root[data-theme=dark] .keyboard .key` out-specified `.key.done` |
| interaction / accessibility / platform / existing-system-mismatch / implementation-bug | 0 | — |

Fixes: separator hairline on the inset (Swift + twin); dark `done` key rule. Final defects: 0 in all types. Iterations: 1.

Static-review caveats (cannot verify without Xcode): `defaultFocus` on a `FocusState<Bool>` inside a presented sheet on iOS 17 — if it does not fire, fall back to `.onAppear` with a short delay; `safeAreaInset` content following the keyboard is standard SwiftUI keyboard avoidance but not rendered here. Tagged `tooling-limit`.

## Preservation

Navigation (tabs, sheet presentation, toolbar Cancel/Save) unchanged; theme tokens only; typography via `theme.font`; `PrimaryButton` reused; one structural change (button from Form section to bottom inset) — justified by the task. Verdict: preservation-ok.

## Regressions to propose

1. Query: the sentence with the p5-swiftui-habits inspect. Expect: `mobile-keyboard-ime` in the bundle; `touch.ime_keyboard` demanded as required when platform is mobile and "keyboard" appears; `interaction.keyboard_navigation` / `interaction.shortcuts` not demanded for a touch-only platform.
2. Query: "Make the Add Habit sheet work when the keyboard is up." (no project). Expect: `artifact_state = existing`, operations `[modify]`, mode polish or refactor; the proper noun "Add Habit" must not produce `create`.
3. Query: search of the same sentence. Expect: `mobile-keyboard-ime` ranks above `desktop-keyboard-first` and `a11y-keyboard-operable` when platform resolves to mobile.
4. Query: direction for a form/sheet task on a non-media, non-ecommerce app with a preserved elevated surface. Expect: layout slot not `layout-grid-catalog`; cards slot never `card-poster-*`; a validator violation falls back instead of being emitted; density preserved with budget "moderate".
5. Query: inspect p5-swiftui-habits. Expect: `product_hints` not `ecommerce`; theme status KNOWN from `Color(light:dark:)` / colorsets; components detected from `Components/*.swift`. (Same as p5-21 — still failing.)

## Tags

`requirements-miss`, `mode-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `tooling-limit`, `skill-hurt`, `preservation-ok`

Skill effect: **hurt**. The knowledge base contains the exact rule for this task; the requirements layer read "keyboard" as a hardware keyboard on a phone, demanded desktop/web concepts, classified a fix as `create`/`new`, and the bundle spent its budget on a product-detail page and a drawer for an ecommerce app that does not exist. Nothing in the delivered guidance changed the implementation beyond confirming initial focus.
