# p6-14 — `VoiceOver reads the streak ring as "image".`

**Project** `research/phase5-projects/p5-swiftui-habits/project` · Swift 5 / SwiftUI, iOS, SPM · platform **mobile**
**Existing UI** yes (Today screen, `Components/ProgressRing.swift`) · new screen no
**Build hash** start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` ✅
**Constraint honoured:** only the streak-ring view was touched (`ProgressRing.swift` + the ring block of the shared HTML twin). `HabitsView.swift` / `EmptyStateView.swift` (the concurrent p6-13 task) were not opened for edit.

## Design-context table (step 1)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | bottom-tabs | KNOWN | `RootTabView` — 4-tab `TabView` | yes |
| theme | dual-theme, default light | KNOWN | `Color(light:dark:)` throughout `AppTheme.swift`, light default | yes |
| surfaces | elevated | INFERRED | `cardSurface()` = surface + radius 16 + shadow | yes |
| radius | small (`most common radius 5`) | INFERRED | `cornerRadius 16`, `cornerRadiusSmall 10` | **no** — confidently wrong; 5/3/8 are stroke widths and icon sizes, not radii |
| spacing | irregular `[6, 32, 2, 3, 4]` | UNKNOWN | explicit 4/8/12/16/24 scale in `Theme.Spacing` | **no** — the scale is declared in one file and is a clean 4-pt ramp |
| typography | custom (`font family System`) | KNOWN | `Nunito` with an explicit `.rounded` system fallback | partial — verdict right, evidence names the fallback as the family |
| components | unknown | UNKNOWN | `Sources/Streaks/Components/` with 5 reusable views | partial — a conventional component dir was not found |

## Requirements verdict (step 2)

| field | value | verdict |
|---|---|---|
| platform | `mobile` (project inspection), `platform_evidence: []` | correct (from project, not sentence — acceptable) |
| artifact_state | `existing` | correct |
| operations | `diagnose`, `modify` | correct |
| problem_domain | `accessibility`, `visual` | correct |
| change_scope | `unknown` / `intent.scope: moderate` | acceptable; `change_budget: low` is the operative value and is right |
| mode | `accessibility`, `audit`; evidence `explicit: voiceover` | correct (matches pre-registered `accessibility`/`audit`) |
| scope.kind | `in-scope` ("UI design / interaction task") | correct |
| change_budget | `low` | correct |
| intent.preserve | `[]` | thin, but `constraints.preserve_existing_system: true` carries it |
| project_context | as above | radius + spacing wrong (see table) |

No requirements-layer miss. `activation.decision: "ambiguous"` with `ui_score 1.0 / non_ui_score 0` is odd bookkeeping but did not change the outcome.

## Guidance verdict (step 3) — status PARTIAL, 0 core + 5 critical guardrails, 583 tokens

| record | layer | verdict | category |
|---|---|---|---|
| `a11y-native-semantics` | critical | **relevant** — names the exact mechanism (SwiftUI `accessibilityLabel`/`accessibilityAddTraits`, merge descendants, test with VoiceOver not by reading code) | — |
| `a11y-color-not-only` | critical | partial | `generic` — true of the ring (arc + numeral, not colour alone) but the code already satisfied it |
| `a11y-contrast-text` | critical | partial | `generic` — text contrast was never the complaint; the ring's real contrast problem is *non-text* (1.4.11), which this record does not cover |
| `interaction-drag-drop` | critical | **off-target** | `wrong-screen` — nothing on Today is draggable; it entered as the bundle's only *critical* record |
| `mobile-density-touch` | critical | **off-target** | `wrong-screen` — tables → list rows, filter sheets, bulk selection; no table, no filter, no selection on this screen |

Relevant 1 · partial 2 · off-target 2. No OPTIONAL layer was emitted.

**The headline defect is in criticality, not selection.** `metrics.critical_concepts = ["interaction.keyboard_navigation"]` — for a VoiceOver labelling bug on a touch-only iOS screen. That single mis-flagged critical is what pulled `interaction-drag-drop` in as a CRITICAL GUARDRAIL, and `critical_coverage_ratio: 1.0` therefore reports success on the wrong thing. The two concepts that actually had to be present (`a11y.accessible_names`, `a11y.semantics`) were merely "required" and were covered by a single GENERIC carrier. `a11y-labels-names` ranks #2 in `search` and carries the same concept more directly, but was correctly dropped as redundant.

### Concept recall

expected 6 · delivered ∩ expected 3 → **recall 0.50** · critical 2/2 → **critical recall 1.00**

| expected id | delivered? | layer if missing |
|---|---|---|
| `a11y.accessible_names` (critical) | yes (`a11y-native-semantics`) | — |
| `a11y.semantics` (critical) | yes (`a11y-native-semantics`) | — |
| `a11y.color_not_only` | yes (`a11y-color-not-only`) | — |
| `data.accessible_chart_alternative` | no | `expected-concepts` — never demanded; a progress ring is a data graphic and the textual alternative to the arc is the whole fix, but nothing in the request model connects "ring" to chart accessibility |
| `a11y.text_scaling` | no | `bundle-selection` — trace: "candidates existed but the bundle cap or a lower utility left them out (candidates a11y-text-scaling)" |
| `process.safe_modification` | no | `expected-concepts` — never demanded (`process.reuse_first` was demanded and then not surfaced) |

Delivered-but-unasked: `interaction.keyboard_navigation`, `a11y.live_status`, `perf.layout_shift`, `touch.gestures_discoverable`, `table.column_priority`, `touch.minimum_target`, `interaction.selection_visible`, `a11y.contrast` — 8 of 11 delivered concepts are noise for this task (purity 0.75 as reported, but concentrated in two records).

PARTIAL_SCOPE note: status is `PARTIAL` because required concern `component` is uncovered, not because of a design/engineering split. Reasonable.

## Direction verdict (step 4)

12 of 13 slots `preserved` with correct reasons ("change budget 'low': the task does not concern this slot"), fingerprint matches the codebase, `Validation: OK`.

**`unjustified_direction_slots = 1`** — `imagery` → "Functional thumbnails" marked **new**, justified as "no repository evidence for this slot", with alternatives (poster art, hero imagery, illustration system) considered. The task is a VoiceOver label on a vector ring; there is no imagery slot to fill, and on an existing UI with budget `low` a slot with no evidence should stay preserved/absent rather than be invented. Harmless here (I ignored it) but it is a direction-layer miss.

## Implementation

Files changed (originals in `before/`):

1. `Sources/Streaks/Components/ProgressRing.swift` — the ring is published as **one non-image element**: kept `.accessibilityElement(children: .ignore)`, added `.accessibilityRemoveTraits(.isImage)` (a view built only from `Shape`s is what surfaces as an unnamed image element), `.accessibilityAddTraits(.updatesFrequently)` so the animated value is re-announced, kept the name "Today's progress" and the spoken value "40 percent" as the textual alternative to the arc, added `.monospacedDigit()` to the centred numeral (matches `WeeklySummaryCard`'s `.monospacedDigit()` convention), and documented why in the doc comment.
2. `render/twin.html` (ring block only) — mirrored the same semantics using the twin's existing convention from `.week-card`: `role="group" aria-label="Today's progress" aria-description="40 percent"`, with `aria-hidden="true" focusable="false"` on the inner `<svg>` and on the centred label. Added `.ring .stat { font-variant-numeric: tabular-nums; }`.

No call-site change: `TodayView` already announces "2 of 5 habits done" as its own element, so the ring did not need new parameters. Routes, state, theme, geometry, colours and tests untouched.

**Guidance used:** `a11y-native-semantics` (traits + names + "merge descendants so a card is one element" + "test with VoiceOver, not only by reading code" → I dumped the CDP accessibility tree rather than eyeballing the markup).
**Guidance ignored:** `interaction-drag-drop` (nothing draggable), `mobile-density-touch` (no table/filter/selection on this screen), `a11y-contrast-text` (text contrast unchanged and already passing; the ring's contrast issue is non-text), direction slot `imagery` (no imagery in a vector ring).

**Process guidance check:** `process_records_needed: false`. SKILL.md §2/§7 was enough — I copied originals to `before/` before editing, reused the existing `WeeklySummaryCard` accessibility convention rather than inventing one, and rendered + inspected the tree before claiming done. `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` would have added tokens without changing any decision.

## Render (step 6/7) — `render_mode: html-twin`

Playwright 1.63 / Chromium, twin at 390×844 @2x, light and dark, plus a CDP `Accessibility.getFullAXTree` dump of the ring subtree.

Ring subtree after the change:
```
none [ignored]
  group "Today's progress" desc="40 percent"
```
Before, the same subtree exposed an unnamed `image` node (the bare `<svg>`) — the reported symptom, reproduced and gone.

**First-render defects — 2** (iterations: 2)
- `existing-system-mismatch` (1): the twin's ring numeral did not carry the tabular figures I had just added in Swift — the twin would have drifted from the source. Fixed with `.ring .stat { font-variant-numeric: tabular-nums; }`.
- `implementation-bug` (1, my harness): I captured "dark" via Playwright's `colorScheme` emulation, but the twin switches on `:root[data-theme="dark"]`, so the first dark shot was identical to the light one. Fixed by setting the attribute before capture; `first-today-dark-390x844.png` is kept as the record of it.

**Final defects — 1**
- `accessibility` (1, **pre-existing, out of scope, not introduced by me**): the ring track is `accentSoft` (`#4A2A22`) on `surface` (`#1E1C1A`) in dark — roughly 1.3:1, so the arc's extent is not perceivable (WCAG 1.4.11 non-text contrast). Visible in `final-today-dark-390x844.png`. The codebase already solved this for the mini rings with a dedicated `chartTrack` token (`#8E6152`, 3.2:1) and says so in `WeeklySummaryCard`'s comment — the large ring was never migrated. Not changed: the sentence is about VoiceOver, budget is `low`, and direction preserves the colour slot. Proposed as a follow-up, not shipped.

Nothing the guidance warned about was shipped.

## Preservation

navigation ✅ · theme ✅ (both polarities rendered, identical geometry/colour) · typography ✅ (theme fonts only) · component reuse ✅ (reused the `WeeklySummaryCard` accessibility idiom and the twin's `role=group` + `aria-description` convention) · unjustified structural change 0.

## Regressions to propose

| query | expectation |
|---|---|
| `VoiceOver reads the streak ring as "image".` | criticals must be `a11y.accessible_names` + `a11y.semantics`; `interaction.keyboard_navigation` must NOT be critical and `interaction-drag-drop` must not enter the bundle for a touch-only iOS screen |
| `VoiceOver reads the streak ring as "image".` | `data.accessible_chart_alternative` must be demanded — a ring/gauge/donut is a data graphic and needs a spoken textual alternative |
| `The progress ring on the dashboard is announced as an unlabelled graphic.` (web variant) | same concepts, no `mobile-density-touch` and no `imagery` direction slot |
| any low-budget existing-UI accessibility task | direction must not mark `imagery` (or any evidence-free slot) as `new` |
| inspect `p5-swiftui-habits` | `radius` must resolve to 16 (or UNKNOWN), not `small`; `spacing` must resolve to the declared 4/8/12/16/24 scale, not `irregular` |

## Misses by earliest layer (step 8)

| layer | what |
|---|---|
| `criticality` | `interaction.keyboard_navigation` flagged as the only critical concept for a touch-only VoiceOver task; the two real criticals were only "required" |
| `expected-concepts` | `data.accessible_chart_alternative` never demanded for a progress-ring accessibility task |
| `bundle-selection` | `a11y.text_scaling` dropped although `a11y-text-scaling` was a candidate |
| `direction` | `imagery` slot marked `new` on a low-budget existing-UI fix |
| `project-context` | `radius: small` (confidently wrong) and `spacing: irregular/UNKNOWN` against a file that declares both explicitly |

## Tags

`skill-helped`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `preservation-ok`, `partial-scope-ok`
