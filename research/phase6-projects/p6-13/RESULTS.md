# p6-13 — "The habit list has nothing to say the first time you open the app."

- **Project / stack / platform**: `research/phase5-projects/p5-swiftui-habits/project` (Streaks) · SwiftUI / SPM, iOS · mobile
- **Existing UI**, not a new screen. Target screen: `HabitsView` (Habits tab).
- **Build hash start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`** (matches the c3 freeze).

## 1. Design context (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | bottom-tabs | KNOWN | `RootTabView` = 4-tab `TabView` | yes |
| theme | dual-theme, default light | KNOWN | `Color(light:dark:)` palette, light-first | yes |
| surfaces | elevated | INFERRED | `cardSurface()` = surface + shadow | yes |
| radius | small (5px, "others 3, 8") | INFERRED | `cornerRadius 16`, `cornerRadiusSmall 10` | **no** — confidently wrong; the 3/5/8 values are SVG `rx`/`stroke` numbers scraped from `render/twin.html`, not the design radius |
| spacing | irregular, "[6, 32, 2, 3, 4]" | UNKNOWN | strict 4/8/12/16/24 scale in `Theme.Spacing` | **partial** — the code is unambiguous; the sampled numbers again come from the twin's SVG paths |
| typography | custom, "family System" | KNOWN | `Nunito` with `.rounded` system fallback | partial — right verdict (custom), wrong family name |
| components | unknown | UNKNOWN | `Sources/Streaks/Components/` with 4 components (`HabitCard`, `PrimaryButton`, `ProgressRing`, `WeeklySummaryCard`) | **partial** — a `Components/` directory with `struct X: View` files exists and was not detected |

Tag: `context-detection-miss` (radius, spacing, components). None of it changed my implementation — I read `AppTheme.swift` directly — but a less careful implementer told "radius small" and "spacing irregular" would have built a 5 px-radius, off-scale empty state.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Value | Verdict |
|---|---|---|
| platform / `platform_evidence` | `mobile`, evidence `[]` (from project inspection) | correct |
| `intent.artifact_state` | existing | correct |
| `intent.operations` | diagnose, modify | correct |
| `intent.problem_domain` | `[]` | miss — the sentence is a states/empty-state complaint ("nothing to say", "first time you open"); no domain was inferred. It did not hurt: the concern list added `states` as *recommended* anyway |
| `intent.change_scope` | screen | correct |
| mode / `mode_evidence` | `audit`, `refactor` ("problem statement on existing UI" / "fix follows the diagnosis") | acceptable (expectation: create/refactor/polish). The sentence has no mode word; audit+refactor is a defensible read and the audit mode is what pulled `a11y`/`interaction` concerns in |
| `scope.kind` | in-scope, "UI design / interaction task" | correct |
| `change_budget` | moderate | correct |
| `intent.preserve` | `[]` | acceptable — direction preserved everything anyway |
| `project_context` | as inspected | carries the radius/spacing errors forward |

## 3. Guidance verdict (`03-guidance.md`, `03-guidance.json`) — status PARTIAL, 2 records, ≈277 tokens

| Record | Layer | Verdict | Category |
|---|---|---|---|
| `comp-empty-state` | core | **relevant** — "short heading, one sentence of why/what next, one primary action, same layout region as the content it replaces" is exactly the component I built, and "same layout region" is what made me centre it in the list region rather than pin it to the top | — |
| `comp-list-row-mobile` | core | **partial** — correct screen and platform, but about rows/swipe/pull-to-refresh, i.e. the state the task says is *absent*. Contributed only ≥44 pt targets | `generic` |

Guardrails layer: empty. Optional notes layer: empty (`optional_useful` 0, `optional_noise` 0). The required concern `accessibility` was left uncovered and the bundle says so.

### Concept recall

| Expected id | Delivered? | Layer if missing |
|---|---|---|
| `state.loading_empty_error` (critical) | yes (`comp-empty-state`) | — |
| `layout.one_primary_action` (critical) | no | `expected-concepts` — never demanded. Note: the *prose* of `comp-empty-state` states "one primary action", so the substance arrived; only the concept id is missing |
| `touch.minimum_target` | yes (`comp-list-row-mobile`) | — |
| `a11y.accessible_names` | no | `bundle-selection` — demanded (recommended), candidates `a11y-native-semantics`, `a11y-labels-names` existed, cap/utility dropped them |
| `process.reuse_first` | no | `bundle-selection` — demanded, candidate `impl-reuse-before-new` existed, dropped |
| `layout.focal_hierarchy` | no | `expected-concepts` — never demanded |

Recall 2/6 = **0.33**; critical recall 1/2 = **0.50** (0.5 by id; substantively 1.0 — see note above).
Extra delivered, not expected: `touch.gestures_discoverable`, `data.pagination_strategy` (both from `comp-list-row-mobile`, both inert here).

No `forbidden_concepts` were delivered; the platform filter correctly dropped six web/desktop/TV records (`anti-hero-template`, `comp-data-table`, `chart-*`, …).

### Process guidance check
`process_records_needed: false`. SKILL.md §2 (reuse before new) and §7 (render and inspect) were enough: I reused `PrimaryButton`, `Theme` tokens and the existing icon-chip idiom without `impl-reuse-before-new`, and I rendered and looked before claiming done without `verify-render-and-inspect`. Dropping them cost nothing on this task.

## 4. Direction verdict (`04-direction.md/json`)

All 13 slots `preserved`, 0 `changed`, 0 `new`. Validation OK. **`unjustified_direction_slots: 0`** — correct for an existing UI at a moderate budget. The fingerprint (`bottom-tabs` / `elevated` / `neutral-plus-accent`) matches the app. One wart: `corner_language: "medium"` in the fingerprint while the slot table says radius "small (INFERRED)" — internally inconsistent, and "medium" happens to be the closer of the two to the real 16 px.

## 5. Implementation

Files changed (originals in `before/`):
- **new** `Sources/Streaks/Components/EmptyStateView.swift` — reusable zero state: 72 pt accent-soft icon chip at `cornerRadius` 16, `title2` heading, `callout` message, optional `PrimaryButton`. All values from `Theme`; icon marked `accessibilityHidden`, container `accessibilityElement(children: .contain)` + label.
- `Sources/Streaks/Views/HabitsView.swift` — `body` split into `emptyState` / `habitList`; `store.habits.isEmpty` ⇒ empty state, centred via `GeometryReader` + `frame(minHeight:alignment:.center)` inside a `ScrollView` so it survives large Dynamic Type. Added a secondary line for "active empty but archived present". Added a `Habits — first run` preview. Nav title, toolbar `+`, sheet, swipe actions, section headers, `.scrollContentBackground(.hidden)` untouched (the `List` block is unchanged apart from indentation).
- `render/twin.html` — new `#habits-empty` screen mirroring the SwiftUI change (`.empty-state`, `.nav-bar` rules).

Guidance used: `comp-empty-state` (structure, copy shape, one action, same layout region); `comp-list-row-mobile` (≥44 pt for the toolbar button and the 52 pt primary button).
Guidance ignored: `comp-list-row-mobile`'s pull-to-refresh / selection-mode / sticky-header advice — the store is in-memory and there is no list to refresh in the empty state.

## 6. Render

`render_mode: html-twin` (SwiftUI; the project ships `render/twin.html`). Playwright 1.63.0, Chromium, 390×844 @2x, light and dark. I looked at all four images.

**First render defects (2)**
- `visual` — the empty state was top-aligned, leaving ~700 px of dead space below it; it did not occupy "the same layout region as the content it replaces". (`comp-empty-state` warned about exactly this and I still shipped it on the first pass — that counts against me, not the skill.)
- `existing-system-mismatch` — the twin put the toolbar `+` on the large-title row; `HabitsView` puts it in the navigation bar above the large title.

**Fixes** → centred via `GeometryReader`/`minHeight` in SwiftUI and `flex:1; justify-content:center` in the twin; split the twin's nav bar row from the title row.

**Final defects: 0.** **Iterations: 1** (2 render passes).

Contrast spot-check in dark: the primary button keeps `foregroundStyle(theme.color.surface)` (dark text on the light accent), which is the app's existing `PrimaryButton` behaviour, unchanged.

## 7. Preservation

Navigation (tab bar, nav title, toolbar `+`, sheet), theme tokens, typography scale and component reuse all preserved; 0 unjustified structural changes. `preservation-ok`.

## 8. Misses by earliest layer

1. `project-context` — radius "small (5)" and spacing "irregular" are confidently wrong; `components` UNKNOWN despite a `Components/` directory of SwiftUI `View` structs. Root cause: the inspector samples `render/twin.html` SVG path numbers as design values.
2. `expected-concepts` — `layout.one_primary_action` and `layout.focal_hierarchy` were never demanded for an empty-state task, although `comp-empty-state`'s text covers the first.
3. `bundle-selection` — `a11y.accessible_names` and `process.reuse_first` were demanded with live candidates and dropped; the bundle itself reports `accessibility` as an uncovered required concern and then ships zero guardrails.
4. `requirements` — `intent.problem_domain` empty on a sentence that is unmistakably about states.
5. `implementation` (mine, not the skill's) — first-pass top alignment against explicit guidance.

## 9. Regressions to propose

- Query: *"The habit list has nothing to say the first time you open the app."* (mobile SwiftUI project) → expect the bundle to demand `layout.one_primary_action` alongside `state.loading_empty_error` for a zero-state task.
- Query: same → expect at least one accessibility record (`a11y-labels-names` or `a11y-native-semantics`) when `metrics.uncovered_required_concerns` contains `accessibility` and the guardrail layer is empty.
- Inspector: a SwiftUI project whose `Theme` declares `cornerRadius = 16` and a 4/8/12/16/24 spacing scale must not report radius `small` / spacing `irregular` from `render/*.html` SVG attributes; `Components/*.swift` files containing `struct X: View` should set `design_context.components`.

## 10. Tags

`context-detection-miss`, `concept-miss`, `requirements-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`, `partial-scope-ok`
