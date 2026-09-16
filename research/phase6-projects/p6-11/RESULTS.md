# p6-11 — "Inspectors in gloves keep missing the small checkbox on each defect row."

- **Project / stack / platform**: `research/phase3-projects/p3-mobile-flutter-field/project` — Flutter (Material 3, riverpod, go_router), mobile.
- **Existing UI**, no new screen. Screen touched: the inspection checklist (`lib/screens/checklist_screen.dart`) plus `lib/widgets/status_badge.dart`.
- **Build hash**: start `ea8eed72…d9947`, end `ea8eed72…d9947` — equal.
- **Premise note (pre-registered)**: the code has no checkbox. Each row is one 72 dp full-width `InkWell` with an 80×56 dp `StatusBadge` that is `ExcludeSemantics` visual-only. The sentence was read as: the per-row check affordance must become an explicit ≥56 dp control with a visible checked state and word+icon (not colour alone), keeping the whole-row target and the Pass/Fail/Skip sheet.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual code | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `AppBar` on all three screens, no tabs/rail | yes |
| theme | dual-theme, default light | KNOWN | `AppTheme.light()/.dark()` + `StatusColors.light/dark`, light root | yes |
| typography | custom | KNOWN | hand-written `TextTheme` (18 sp body, w400/w600/w700), system family | yes |
| surfaces | flat-tonal ("no shadow or border declarations found") | UNKNOWN | flat, but every tile **does** declare a border (`BorderSide` in `RoundedRectangleBorder`, `Border.all(width: 2)`); elevation explicitly 0 | partial — value right, evidence wrong (Dart `BorderSide`/`Border.all` not recognised as a border declaration) |
| spacing | irregular, "[2, 12]" | UNKNOWN | a declared 4-based scale: `FieldSizes.space1..space8 = 4/8/12/16/24/32`, `control 56`, `controlGap 12` | partial (UNKNOWN where the code is explicit); the reported value is also wrong |
| radius | small (4) | INFERRED | `FieldSizes.radius = 8`, used everywhere | no (confident wrong value) |
| components | go_router, riverpod | KNOWN | correct | yes |

`accessibility: a11y attributes present in 8 files` and `environment_hints: outdoor, gloves, low-bandwidth` are both correct and load-bearing.

## 2. Requirements verdict (`02-requirements.json`)

| field | resolved | verdict |
|---|---|---|
| platform | `mobile` (KNOWN, from project inspection) | correct. `platform_evidence` from the sentence alone is weak (`inspectors`→mobile, `gloves`→kiosk, both WEAK_INFERENCE) — the project file saved it |
| artifact_state | `existing` | correct |
| operations | `diagnose`, `modify` | correct |
| problem_domain | `interaction`, `responsive` | `interaction` correct; `responsive` is a **false positive** — it comes from the word "small" in `intent_evidence.domains.responsive = ["small"]`, and there is no viewport/size-class cue in the sentence |
| change_scope | `unknown` (scope "moderate") | acceptable |
| mode + evidence | `audit`, `responsive`, `refactor` | acceptable. `audit`+`refactor` match the pre-registered `polish/accessibility/refactor`; `responsive` is wrong for the same "small" reason, and it pulled `mobile-orientation-size-classes` / `mobile-keyboard-ime` into the candidate pool |
| scope.kind | `in-scope` ("UI design / interaction task") | correct |
| change_budget | `moderate` | correct |
| intent.preserve | `[]` | thin — the sentence names no preservation, but on an existing UI with `preserve_existing_system: true` the empty list carries no signal |
| project_context | echoed from inspect | inherits the radius/spacing errors above |

## 3. Guidance verdict (`03-guidance.*`)

Bundle = 4 records (core 1 + guardrails 3), no optional layer. 596 tokens.

| record | layer | verdict | category | why |
|---|---|---|---|---|
| `media-photo-viewer` | CORE | **off-target** | `wrong-screen` | A full-screen photo viewer (thumbnails, pinch-zoom, retake/remove). This task is a checklist row control; the photo viewer belongs to `defect_report_screen.dart`, which the sentence does not mention. Its own `selected for` line says "task evidence: " — empty — and it still won the core slot |
| `mobile-field-use` | GUARDRAIL | **relevant** | — | The one useful record: ≥48 dp targets with ≥12 dp spacing, no precision gestures with gloves, glanceable status as word+colour+icon. Directly sized the new control |
| `states-offline-and-sync` | GUARDRAIL | partial | `generic` | True for this app (and the status write does enqueue a `PendingSync`), but it says nothing about the row control the task is about |
| `layout-hierarchy-one-thing` | GUARDRAIL | partial | `generic` | Generic focal-point advice; useful only as a negative check (don't let the new control outshout the "3 / 6 checked" numeral) |
| — bundle level — | — | — | `missing-critical` | `a11y.color_not_only` is never demanded (see below) |

`layer_review`: core `[media-photo-viewer]`, critical `[mobile-field-use, states-offline-and-sync, layout-hierarchy-one-thing]`, optional `[]` (0 useful / 0 noise).

### Concept recall (against the pre-registered expectation)

Delivered concepts (union over selected records): `data.exception_first, data.refresh_timestamp, env.glanceable_status, env.outdoor_readability, interaction.back_semantics, layout.focal_hierarchy, layout.one_primary_action, perf.image_sizing, state.offline_sync, state.saving_conflict, touch.gestures_discoverable, touch.minimum_target`.

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `touch.minimum_target` (critical) | yes (DIRECT, `mobile-field-use`) | — |
| `a11y.color_not_only` (critical) | **no** | `expected-concepts` — never demanded (absent from `required_concepts`, `recommended` and `not_surfaced`). Carriers exist (`a11y-color-not-only`, `data-exceptions-first`, +7), so this is not a knowledge gap. Partly rescued in prose by `mobile-field-use` ("word plus colour plus icon") |
| `env.glanceable_status` | yes (DIRECT) | — |
| `a11y.semantics` | **no** | `expected-concepts` — never demanded; carriers `a11y-semantics-structure`, `a11y-native-semantics`, `a11y-skip-link` exist |
| `interaction.selection_visible` | **no** | `expected-concepts` — never demanded; carriers `a11y-color-not-only`, `color-states-complete`, `comp-data-table`, `grid-single-tab-stop` exist. This is the concept the task is *about* (a checked state that reads at a glance) |
| `a11y.accessible_names` | **no** | `bundle-selection` — demanded as recommended, candidates `a11y-labels-names` / `a11y-native-semantics` existed, dropped by the cap/utility (`not_surfaced`: "no sufficiently specific guidance") |

**Concept recall 2/6 = 0.33. Critical recall 1/2 = 0.50.** The skill's own self-report is `concept_coverage_ratio 1.0` / `critical_coverage_ratio 1.0` — it scores itself against the concepts it chose to demand, which is exactly where the miss is.

None of the forbidden concepts were delivered. `status` was CONFIDENT, not PARTIAL_SCOPE, so there is no design/engineering split to judge.

## 4. Direction verdict (`04-direction.*`)

12 of 13 slots preserved with correct reasons ("the task does not concern this slot"), which is right for a moderate budget on an existing UI. The density slot even appends the field-use floor ("targets ≥ 48 dp with ≥ 12 dp spacing") — the most useful line in the file.

- `cards` → **new** (`card-list-row`), justified as "no repository evidence for this slot". The repository plainly has list rows (bordered 72 dp tiles with an 8 dp gap, an explicit comment saying so). The slot is only "new" because the surfaces/spacing detection above came back UNKNOWN. Its advice also half-contradicts the codebase ("trailing chevron only when it navigates" — the chevron here opens a sheet).
- **`unjustified_direction_slots = 1`** (`cards`). Routed to `project-context`, not `direction`.
- Validation: OK. Preservation metrics matched what I implemented.

## 5. Implementation

Files changed (originals in `before/project/`):

1. `lib/widgets/status_badge.dart` — added optional `onTap` + `semanticLabel`. Without them the badge is byte-for-byte the old visual-only `ExcludeSemantics` container (it is also the idiom referenced by `offline_banner.dart`). With them it becomes the row's check control: `Material` + `InkWell`, **88 × 64 dp** (project floor is `FieldSizes.control = 56`), same colours, same border, same icon+word face, wrapped in `Semantics(button: true, checked: status == pass, label: …)`.
2. `lib/screens/checklist_screen.dart` — `_ItemRow` passes `onTap`/`semanticLabel` to the badge and drops the outer `MergeSemantics` (merging would have swallowed the one node the task is about; the title/detail column is already `ExcludeSemantics`, so the row still announces as one button). Added `_toggleCheck`: pending → pass and pass → pending in one tap (its own undo), fail/skip open the existing Pass/Fail/Skip sheet so their reason is never silently dropped. Row horizontal padding 12 → 8 dp (see defect 1).
3. `test/checklist_test.dart` — one added assertion for the labelled 88 × 64 control. Not executed (no Flutter SDK in this environment), as the file's own header already notes.
4. `../render/twin.html` (HTML twin) — each row goes from one `<button class="row">` to `<div class="row">` + `<button class="check">` + `<button class="rowmain">`, mirroring the Flutter nesting; new `.check` (88×64) and `.rowmain` rules.

Preserved: top bar, dual theme, type scale, `FieldSizes` tokens, `StatusColors`, row tile geometry (72 dp min, 8 dp gap, radius 8, 1 dp outline), the Pass/Fail/Skip sheet, the offline banner, the sync queue path (`setStatus` still enqueues a `PendingSync`), routes, riverpod state, ids.

- **guidance used**: `mobile-field-use` (≥48 dp / ≥12 dp floors, glove rule, word+icon+colour).
- **guidance ignored**: `media-photo-viewer` (wrong screen); `states-offline-and-sync` (no offline behaviour change — the existing queue path was reused); `layout-hierarchy-one-thing` (focal point untouched by design).

**Process guidance check**: `process_records_needed = false`. SKILL.md §2/§7 plus the protocol were enough — I extended `StatusBadge` rather than adding a widget, copied files to `before/` first, and rendered-and-inspected twice. `impl-reuse-before-new` in the bundle would not have changed any of it.

## 6. Render

`render_mode: html-twin` (Flutter, no SDK / device here) at 390 × 844, deviceScaleFactor 2, plus static code review of the Dart. Screenshots looked at, not just written.

**First render** (`render/first-*.png`) — 1 defect:

| type | defect |
|---|---|
| visual | The 88 dp control stole 8 dp from the title column, so "Crossarm and insulators" wrapped to two lines and the visible row count per screen dropped from 4.5 to 3.75 against the baseline render — a density regression on a screen whose whole point is scanning a checklist. |

**Fix**: row horizontal padding 12 → 8 dp (Flutter and twin), restoring the original text column width.

**Final render** (`render/final-*.png`) — 0 defects. Measured in the final twin: check control 88 × 64 in all 6 rows, 12 dp to the row body target, 38 dp between vertically adjacent controls, row heights back to the baseline 76 px. Also checked the high-contrast variant (`final-checklist-hc.png`, 2 dp borders hold) and the loading skeleton (`final-loading.png`, bone resized to 88 × 64).

**Iterations: 1.** No defect that the guidance had warned about was shipped.

## 7. Preservation verdict

`preservation-ok`. Navigation, theme, typography, tokens and component reuse intact; 0 unjustified structural changes. The only geometry change outside the control itself is the 4 dp row padding reduction, made to *undo* a regression the control introduced.

## 8. Misses, routed to the earliest layer

| layer | miss |
|---|---|
| `mode` | `responsive` inferred from the word "small" in a sentence with no viewport cue; it widened the candidate pool with orientation/keyboard records |
| `expected-concepts` | `a11y.color_not_only`, `interaction.selection_visible` and `a11y.semantics` are never demanded for a "status control on a row, gloves, outdoors" task, although carriers for all three exist in the base |
| `bundle-selection` | `a11y.accessible_names` demanded, candidates present (`a11y-labels-names`, `a11y-native-semantics`), dropped |
| `candidate-compatibility` | `media-photo-viewer` took the CORE slot with an empty task-evidence line (`selected for: task evidence: ; lexical 0.098`) on a checklist-row task; meanwhile `comp-list-row-mobile` and `card-list-row` were omitted for "no positive task evidence" — the same test the winner failed |
| `project-context` | radius reported 4 (actual 8); spacing reported "irregular" where `FieldSizes` declares a 4-based scale; `BorderSide`/`Border.all` not read as border declarations. This also produced the one unjustified direction slot (`cards` = new) |

No knowledge gaps: every missing concept has carriers in `data/*.jsonl`.

## 9. Regressions to propose

1. Query: "Inspectors in gloves keep missing the small checkbox on each defect row." — expect `a11y.color_not_only` and `interaction.selection_visible` among the demanded concepts, and expect the CORE slot to be a list-row / target-size record, not `media-photo-viewer`.
2. Query: any mobile task naming a per-row control (checkbox, toggle, status chip) — expect a record carrying `a11y.accessible_names` to survive bundle selection when the task is about a control with no visible text label.
3. Query: a sentence whose only "size" word is an adjective on a control ("the small checkbox", "the tiny button") — expect mode NOT to include `responsive`.
4. `inspect_project.py` on this Flutter project — expect `radius = 8` (`FieldSizes.radius`) and `spacing = KNOWN, 4-based scale` from an `abstract final class` of `static const double` tokens, and expect `BorderSide` / `Border.all` to count as border declarations for the surfaces signal.

## 10. Tags

`mode-miss`, `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`

**Skill effect: neutral.** The only thing I took from the bundle was `mobile-field-use`'s target/spacing floors — and this codebase already encodes exactly those floors in `FieldSizes.control = 56 // min tap target (glove)` and `controlGap = 12`, with comments explaining why. Nothing in the bundle told me anything the project had not already told me, and its CORE record was for a different screen. It did not hurt either: the wrong record was easy to discard.
