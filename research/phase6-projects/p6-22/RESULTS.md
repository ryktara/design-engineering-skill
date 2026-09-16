# p6-22 — FleetDesk (Avalonia desktop), Dispatch job form

**Task sentence (verbatim):** "Dispatchers say the job form asks for the same driver details twice."
**Project:** `research/phase5-projects/p5-avalonia-fleet/project` — C# / Avalonia 11 / net8.0, MVVM, light-first bordered-flat theme.
**Platform:** desktop. **Existing UI**, not a new screen. Concurrency rule respected: only `Views/DispatchView.axaml`, `ViewModels/DispatchViewModel.cs` and the Dispatch sections of `render/twin.html` were touched; the Vehicles map/list view was not opened for edit.
**Build hash start = end = `ea8eed72…d9947`** (matches the c3 freeze).

## Premise check (done before any advise command — see `00-expectation.json`)

The complaint is **literally false against the code**. The job form's fields are Title, Customer, Priority, Pickup, Drop-off, Assigned vehicle, Notes. There is **no driver field at all**, let alone two. `Driver` exists only on `Models/Vehicle.cs` and is rendered only on the Vehicles screen.

The real defect the complaint describes: driver identity is implied by an opaque vehicle-id combo (`V-102`), so a dispatcher must cross-reference the Vehicles grid and then re-state the driver in Notes — the data is entered a second time because the form never shows what the system already knows. The correct fix is therefore to **derive and display** the driver read-only from the vehicle record, and explicitly **not** to add an editable Driver field (that would create the duplication the complaint imagines).

## Design-context table (step 1)

| Field | Detected | Status | Actual (README ground truth) | Correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | menu bar + toolbar, no rail | yes (the "also left-rail: 1 matches" note is a false secondary signal; primary value right) |
| theme | light-first | INFERRED | light-first, `ThemeVariant.Light` requested explicitly | partial (code is explicit; should be KNOWN) |
| surfaces | bordered-flat | INFERRED | bordered flat, 1px `#D9DDE3`, no shadows | yes (value right; "shadow/elevation in 1" is the scrim, not elevation) |
| radius | small (4) | INFERRED | 4px everywhere, `AppCornerRadius` + `ControlCornerRadius` overridden | partial (a named 4px token is stated, not inferred) |
| spacing | 4 | INFERRED | 8px scale (8/16/24/32); 4/6/2 are only padding sub-values | partial — the dominant scale is 8, the detector picked the most frequent literal |
| typography | humanist-sans (Segoe UI / Inter) | KNOWN | Segoe UI, Inter fallback | yes |
| components | avalonia | KNOWN | Avalonia 11 + DataGrid | yes |

## Requirements verdict (step 2)

| Field | Value | Verdict |
|---|---|---|
| platform_evidence | desktop, WEAK_INFERENCE from "dispatchers"; resolved desktop from project inspection | correct |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | `[]` | miss — the sentence names a concrete domain (duplicated data entry in a form); nothing was extracted |
| intent.change_scope | screen | correct |
| mode + evidence | `audit, refactor` ("problem statement on existing UI" / "fix follows the diagnosis") | correct, and correctly derived with no mode word in the sentence |
| scope.kind | in-scope, "UI design / interaction task" | correct |
| change_budget | moderate | acceptable (low would also be right; nothing was over-changed) |
| intent.preserve | `[]` | acceptable — `constraints.preserve_existing_system: true` carries it |
| project_context | as table above | correct on values |

Note: `activation` classified "driver" as a **non-UI term** (ui_score 2.0 vs non_ui 1). The one noun the whole task turns on is treated as noise.

## Guidance verdict (step 3) — status PARTIAL, bundle = 4 (core 2 + guardrails 2), ≈762 tokens

| Record | Layer | Verdict | Category | Why |
|---|---|---|---|---|
| `comp-form` | core | relevant | — | labels above, field widths to content, unsaved-changes guard, primary action last — all matched what the screen already does and what I had to preserve |
| `layout-master-detail` | core | partial | generic | true of the screen, says nothing about the reported problem; contamination 0.25 (TV/narrow-width advice) |
| `desktop-keyboard-first` | guardrail | partial | generic | platform-correct but F2/Delete/Ctrl+F/grid selection has no bearing on a duplicated-field complaint |
| `layout-states-empty-loading-error` | guardrail | off-target | generic | there is no async/remote data on this screen (deterministic in-memory `SampleData`); entered as "required coverage (GENERIC)" |

Bundle-level: **missing-critical** — neither `process.reuse_first` nor `a11y.accessible_names` reached the bundle, and both were exactly what this task needed.

**Concept recall** — delivered = union of concepts on selected records = {feedback.validation_errors, touch.ime_keyboard, form.autofill_attributes, state.unsaved_changes_guard, interaction.keyboard_navigation, interaction.shortcuts, interaction.focus_visible, state.loading_empty_error}.

| Expected id | Delivered? | Layer if missing |
|---|---|---|
| process.reuse_first (critical) | no | bundle-selection — demanded as *recommended*, candidate `impl-reuse-before-new` existed and was dropped |
| a11y.accessible_names (critical) | no | bundle-selection — candidates `a11y-native-semantics`, `a11y-labels-names` existed and were dropped |
| state.unsaved_changes_guard (critical) | yes (comp-form) | — |
| layout.settings_grouping | no | expected-concepts — never demanded |
| desktop.spacing_grid | no | expected-concepts — never demanded |
| interaction.keyboard_navigation | yes (desktop-keyboard-first) | — |

Recall **2/6 = 0.33**; critical recall **1/3 = 0.33**.

`touch.ime_keyboard` was delivered on a desktop task (carried inside `comp-form`'s TV/IME sentence) — off-platform payload riding in an on-platform record.

**Knowledge gap (confirmed with `search … -k 12` and a grep over `data/*.jsonl`):** no record in the base carries *"do not ask for data the system already holds; derive it read-only from the source record and show it"* — the single idea this task is about. The nearest hits are `comp-form`, `a11y-forms-errors`, `layout-form-stack`, all about how to lay a field out, none about whether the field should exist. There is also no ontology id for it in `heldout-v4/ONTOLOGY.md`.

**PARTIAL status judgement:** the note is driven by the uncovered `accessibility` concern, not by a design/engineering split. The split itself is not at issue here — the task is fully a UI task and `scope.kind = in-scope` is right.

## Direction verdict (step 4)

All 13 slots `preserved`, 0 `changed`, 0 `new`. Budget moderate, validation OK, fingerprint (menu-bar / bordered / sharp / humanist-sans / neutral-plus-accent) matches the README ground truth. **`unjustified_direction_slots` = 0.** The per-slot prose is padding on a preserved-everything task (typography slot recommends Source Sans 3 / Nunito Sans on a project whose typography it just said to preserve), but it is tagged "Existing system: do not replace it", so it did no harm.

## Implementation

Files changed (originals in `before/`):
- `ViewModels/DispatchViewModel.cs` — added derived `SelectedVehicle`, `DriverLabel`, `DriverDetail`; `EditVehicleId` setter and `LoadEditor()` now raise change notifications for them. No new editable state, no change to `HasChanges`, `Save()`, `Cancel()` or the unsaved-changes prompt.
- `Views/DispatchView.axaml` — row 3 column 2 (previously an empty grid cell) now holds a read-only "Driver (from vehicle record)" readout: name + plate/status, borderless `SurfaceAltBrush` block, 4px radius, `PadInput`. Added `AutomationProperties.LabeledBy` on the vehicle combo and on the readout (labels are visual-only in Avalonia otherwise).
- `render/twin.html` — same cell added to both Dispatch sections + a `.readout` class, so the twin still mirrors the app.

`dotnet build` succeeds, 0 warnings, 0 errors (XAML compiled).

**Guidance used:** `comp-form` (labels above / field width to content / unsaved-changes guard preserved).
**Guidance ignored:** `layout-master-detail` (nothing to change in the list/detail split), `layout-states-empty-loading-error` (no async data on this screen; adding loading/skeleton states would be a defect), the TV/IME sentence inside `comp-form` (off-platform).

## Render and defects

Render mode: **html-twin** at 1280×800 (Avalonia has no capture harness; the project ships `render/twin.html`), screenshots looked at, plus a real `dotnet build` and static review of the XAML/VM.

First render — 1 defect:
- `visual`: the derived driver block was given the same 1px `LineBrush` border and radius as the editable inputs beside it, so a read-only value was distinguishable from an input by fill alone.

Fix: dropped the border, kept the alt fill and radius. **Iterations: 1.** Final render: 0 defects of any type.

No defect the guidance had warned about was shipped.

Verified by static review only (no interactive twin state): the `(unassigned)` path renders "No driver - vehicle unassigned" / "Assign a vehicle to see its driver."

## Preservation

Navigation, theme, typography, surfaces, radius, spacing scale all untouched; the new element reuses `SurfaceAltBrush` / `LineBrush` / `AppCornerRadius` / `PadInput` / `MarginBelow2` and the existing `label` and `muted` classes. No new control type, no new token. Unsaved-changes guard, ListBox selection guard, Save/Cancel commands, ids and bindings unchanged. **preservation-ok**, 0 unjustified structural changes.

## Process guidance check

**Yes, needed.** `impl-reuse-before-new` (`process.reuse_first`) is not a nicety here — it *is* the fix ("reuse the Vehicle record instead of adding a field"), and it was a live candidate that bundle selection dropped. SKILL.md §2/§7 got me to inspect first and to render and look, but the specific "derive, don't re-ask" move came from reading the code, not from the bundle. `process_records_needed: true`.

## Skill effect

**neutral.** The bundle confirmed things the project already did (labels above, unsaved-changes guard) and contributed one off-target guardrail I discarded. The decisive judgement — that the complaint's premise is false and the fix is a derived read-only field — came from the codebase. Nothing in the bundle led me to a change I reverted, so not `hurt`.

## Regressions to propose

1. query: "Dispatchers say the job form asks for the same driver details twice." → expect a record carrying "do not ask for data the system already holds; derive it read-only from the source record" in CORE; today no such record exists (knowledge gap).
2. query: same sentence, desktop existing-UI project → expect `impl-reuse-before-new` in the bundle whenever `intent.operations` contains `modify` on an existing artifact; today it is demanded as *recommended* and dropped.
3. query: same sentence → expect `intent.problem_domain` to be non-empty (duplicated/redundant data entry), and "driver" not to be scored as a non-UI activation term.
4. query: any desktop form task on a project with deterministic in-memory data → expect `layout-states-empty-loading-error` not to be selected as a required-coverage guardrail without evidence of async data.

## Tags

`concept-miss`, `ranking-miss`, `knowledge-gap`, `requirements-miss`, `render-defect-fixed`, `preservation-ok`, `skill-neutral`, `partial-scope-ok`
