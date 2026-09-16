# p5-16 — FleetDesk (Avalonia 11): "overdue for service" visibility

**Task (verbatim):** Dispatchers want to see which vehicles are overdue for service without opening each one.
**Project / stack / platform:** `p5-avalonia-fleet/project` · C# / Avalonia 11.2, net8.0, hand-rolled MVVM · desktop.
**Existing UI or new screen:** existing UI (Vehicles DataGrid of 30 rows inside the menu-bar + toolbar + status-bar shell). No new screen.
**Render mode:** html-twin (`project/render/twin.html`, Playwright 1.63.0 Chromium, 1440×900) + static code review; GUI not launched. `dotnet build`: 0 warnings, 0 errors (bin/obj deleted afterwards).
**Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (skill untouched).

Note on session continuity: a previous agent ran steps 0–5 and the build; this session reviewed the implementation against `before/`, restored LF line endings that the previous agent had flipped to CRLF in `Styles/Theme.axaml` and `Views/MainWindow.axaml` (whole-file diffs → now 14-line and 2-line diffs), rewrote `render/shot.js` (its `path.replace(/\/g, '/')` was an invalid regex literal; no PNGs had ever been produced), verified the twin against `Services/SampleData.cs`, rendered, and wrote the deliverables.

## 1. Design-context table (01-inspect.json vs code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | Menu bar (File/Vehicles/Dispatch/Help) + toolbar + bottom status bar, `MainWindow.axaml` | yes (the "also left-rail: 1 match" candidate is spurious; value right) |
| theme | light-first | INFERRED | `App.axaml` requests `ThemeVariant.Light` explicitly; light palette in `Theme.axaml` | yes (value right; should be KNOWN — the request is explicit) |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations found") | flat **bordered**: every surface/button/input/grid has `BorderThickness=1` `LineBrush`, no shadows (`Border.surface`, `Border.badge`, README) | partial (uncertainty flagged, but the code is unambiguous and the value "tonal" is wrong — bordered) |
| radius | unknown | UNKNOWN | `AppCornerRadius=4`, Fluent `ControlCornerRadius=4` | partial (explicit resource missed) |
| spacing | 4 | INFERRED | 8-px scale (`Space1..4` = 8/16/24/32, `Pad1..3`); 4 only appears inside compound paddings (`8,4`, `6,2`) | no (confident wrong value) |
| typography | geometric-sans, weights semibold, tabular false | KNOWN | `Segoe UI, Inter` (humanist / neo-grotesque, not geometric); semibold used; no tabular figures | partial (family found; character label wrong; features right) |
| components | avalonia | KNOWN | Avalonia + Avalonia.Controls.DataGrid | yes |

`tokens: []` and `fonts: []` at the top level are also misses: `Theme.axaml` is a 260-line named token dictionary (colours, brushes, font sizes, radius, spacing) and the font family is declared twice.

## 2. Requirements verdict (02-requirements.json)

| item | skill | expectation | verdict |
|---|---|---|---|
| platform | `desktop` (from project inspection; `platform_evidence: []` from sentence) | desktop | correct |
| intent.artifact_state | existing | existing | correct |
| intent.operations | diagnose, modify | modify the existing grid | correct |
| intent.problem_domain | `[]` | table / status / exception visibility | miss |
| intent.change_scope | unknown (intent.scope = moderate) | small, one column + filter | acceptable |
| mode + evidence | audit, refactor ("problem statement on existing UI"; "fix follows the diagnosis") | refactor / polish / create | acceptable (refactor is in the set; audit is a harmless secondary) |
| scope.kind / reason | **abstain** — "no UI vocabulary found; not a UI design task as written"; `activation.ui_score = 0` | in-scope (partial acceptable for the service-interval rule) | **wrong** |
| change_budget | low | low | correct |
| intent.preserve | `[]` (but `constraints.preserve_existing_system: true`) | navigation, theme, typography, component reuse | partial |
| project_context | propagated from inspect (same errors as §1) | — | inherits spacing=4 error |

The activation gate scored zero UI terms in a sentence that is about a list of rows ("which vehicles", "without opening each one") and a status ("overdue for service"). Status ABSTAIN propagated into guidance and direction.

## 3. Guidance verdict (03-guidance.json)

`core: []`, `guardrails: []`, `bundle_tokens: 0`, note "OUT_OF_SCOPE … Nearest supported UI task: describe the screen, component, or user-facing problem." There is no record to grade: relevant 0 · partial 0 · off-target 0.

BAD categories:
- bundle as a whole → `missing-critical`: nothing on exception-first ordering, colour-not-only status, or badge reuse reached the implementer.
- direction slot text for typography (see §4) → `contradicts-codebase`.

Concept recall (delivered = ∅):

| expected concept | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| data.exception_first | yes | no | scope (abstain) → never reached expected-concepts. KB carries it: `layout-hierarchy-one-thing`, `anti-generic-sidebar-dashboard`, `chart-realtime`; `layout-hierarchy-one-thing` even appears at rank 4 in `03-search.txt`. |
| a11y.color_not_only | yes | no | scope → expected-concepts. KB: `a11y-color-not-only`, `comp-chart-container`, `chart-accessible-colour`. |
| env.glanceable_status | no | no | scope → expected-concepts; **additionally knowledge-gap for desktop**: the only record carrying it is `mobile-field-use`, which is environment-gated (filtered out in search: "environment ['gloves','outdoor'] not in request"). |
| process.reuse_first | no | no | scope → expected-concepts. KB: `impl-reuse-before-new`. |
| interaction.selection_visible | no | no | scope → expected-concepts. KB: `comp-data-table`, `a11y-color-not-only`, `grid-single-tab-stop` (rank 1 in search). |
| table.tabular_figures | no | no | scope → expected-concepts. KB: `data-tables-numeric`, `comp-data-table`, `typo-scale-and-roles`. |

**Recall 0/6 = 0.00 · critical recall 0/2 = 0.00.** Five of six are not knowledge gaps: the base has the records, the pipeline stopped at the scope gate. `search` (which ignores the gate) ranks `grid-single-tab-stop` first and then checkout / onboarding / glassmorphism records — lexical retrieval also has no purchase on "overdue", "service", "vehicles".

## 4. Direction verdict (04-direction.md/json)

Compatibility table: 12 slots preserved, 0 changed, 1 new (`focus` → `focus-ring-standard`, "no repository evidence for this slot"). Preservation metric: all of navigation / layout / density / surface / cards / typography / color / motion / cta / imagery / icon / metadata preserved. Validation: **VIOLATIONS** — "audit: no accessibility constraints attached".

- Preserved slots: correct and justified (change budget low, existing system).
- `focus` marked new: not justified by the task, and the repository does have focus evidence (`TextBox:focus … AccentBrush` in `Theme.axaml`); harmless because nothing was changed.
- `density` "spacing base 4": wrong (8-px scale), inherited from inspect.
- `typography` slot text: "Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist …)" — printed under a slot labelled *preserve*; contradicts the codebase (Segoe UI / Inter). Ignored.
- `color` slot text is generic system-building advice ("validate every pair with tokens.py"); not wrong, not useful here.
- Validation message is internally inconsistent: `requirements.accessibility` has every flag true, yet validation says no accessibility constraints are attached.

## 5. Implementation summary

Files changed (copies in `before/`; `Models/ServicePolicy.cs` is new):

| file | change |
|---|---|
| `Models/ServicePolicy.cs` (new) | `IntervalDays = 90`, `DueSoonDays = 14`, fixed `Today = 2026-09-09` so sample data, twin and screenshots agree |
| `Models/Vehicle.cs` | computed `NextServiceDue`, `DaysPastDue`, `IsServiceOverdue`, `IsServiceDueSoon`, `NeedsServiceAttention`, `ServiceLabel` ("Overdue 40 d" / "Due in 8 d" / "Due today" / "OK") |
| `Services/SampleData.cs` | `JobDay = ServicePolicy.Today` (was a duplicate literal) |
| `Styles/Theme.axaml` | +`Border.badge.warning` / `Border.badge.danger` on the existing badge component using existing `Warning*`/`Danger*` brushes |
| `ViewModels/VehiclesViewModel.cs` | `OverdueOnly` filter, `OverdueCount`, `DueSoonCount`, `ServiceSummary`; free-text filter also matches `ServiceLabel`; Clear resets both |
| `ViewModels/MainWindowViewModel.cs` | status-bar `FleetSummary` gains "… - 10 overdue for service" |
| `Views/VehiclesView.axaml` | "Overdue for service only" CheckBox in the existing header; new `Service` `DataGridTemplateColumn` (140 px, `SortMemberPath=DaysPastDue`): badge with text for overdue/due-soon, muted "OK" otherwise; header line "30 of 30 vehicles shown - 10 overdue for service - 2 due soon" |
| `Views/MainWindow.axaml` | Vehicles menu: "Show _overdue for service only" check item bound to the same flag (menu-bar mirrors the toolbar-level control, per the project's own navigation model) |
| `render/twin.html` | mirrors all of the above; every row's label recomputed from `SampleData.cs` with the 90/14-day rule — 30 rows, 10 overdue, 2 due soon, 0 mismatches |

Guidance used: none from the bundle (empty). From direction: the preserve-everything table (followed — no slot changed). Ignored: the ABSTAIN status itself (the sentence is plainly a UI task on the existing grid); the typography slot's font suggestions; the `focus` "new" slot; density base 4. The service-interval rule is an engineering decision the skill could have flagged as partial scope; instead it abstained entirely.

Not done, deliberately: overdue-first default sort (the column is sortable and the filter exists; changing default order of a dispatcher's grid is a behaviour change the sentence does not ask for). Observation: the "10 overdue for service" header count is plain muted text — glanceable but not emphasised.

## 6. Render and defects

Screenshots: `render/first-vehicles-1440x900.png`, `render/first-dispatch-1440x900.png`, `render/final-*` (identical content).
Twin geometry: section 1440×900, table width 1406 (fits, no horizontal overflow), header row 48 px single line, 30 rows, 10 danger badges, 2 warning badges.

First-render defects: visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
Checks behind that: badge text on tint — danger 5.50:1, warning 4.51:1 (AA at 12 px); muted "OK" on white 5.43:1 and on the AccentSoft selected row 4.70:1; danger badge on a selected row 5.61:1, so an overdue selected row stays distinguishable from the blue selection. Every state carries words, never colour alone. Badge reuses `Border.badge` (4 px radius, 1 px border, no shadow). The grid clipping at row 18 is the twin's pre-existing mirror of a scrolling DataGrid (identical in `before/render/twin.html`), not counted.
Final defects: all 0. **Iterations: 0** (no render fix needed; the tooling fixes — line endings, shot.js — are not render iterations).

## 7. Preservation verdict

navigation ✓ (menu bar + toolbar + status bar untouched; one menu item added inside the existing Vehicles menu) · theme ✓ (light, existing brushes only) · typography ✓ (Segoe UI/Inter, 13/12 px roles) · component reuse ✓ (`Border.badge`, `TextBlock.muted`, default CheckBox, existing header StackPanel) · unjustified structural changes 0 · 4 px radius, 1 px borders, no shadows kept. **preservation-ok.**

## 8. Regressions to propose

1. Query: the task sentence verbatim with the Avalonia project context. Expect: scope in-scope (or partial with a design/engineering split naming the service-interval rule), `problem_domain` includes table/status, concepts `data.exception_first` + `a11y.color_not_only` demanded; bundle contains `a11y-color-not-only` and `comp-data-table` (or `layout-hierarchy-one-thing`).
2. Query: "Ops wants to see which orders are late in the list without opening each one" (web, existing table). Expect: not abstain; same two critical concepts — checks the general "see which X are Y in a list" phrasing, which has no component noun.
3. Inspect: an Avalonia `Theme.axaml` with `CornerRadius` / `BorderThickness` / `Thickness` resources and `x:Double Space1..4`. Expect: radius 4 KNOWN, surfaces flat-bordered KNOWN, spacing 8, tokens non-empty.
4. Direction validation: when `requirements.accessibility` flags are all true, "audit: no accessibility constraints attached" must not be reported.
5. Concept `env.glanceable_status`: at least one non-environment-gated (desktop/table) record should carry it, otherwise desktop status tasks can never recall it.

## 9. Tags

`scope-miss`, `requirements-miss`, `concept-miss`, `context-detection-miss`, `knowledge-gap` (env.glanceable_status only), `direction-mismatch` (typography slot text, spurious focus slot, validation message), `skill-hurt`, `preservation-ok`, `tooling-limit` (Avalonia rendered via HTML twin, GUI not launched).

Skill effect: **hurt**. Followed literally, the skill refuses an in-scope task ("not a UI design task as written"); nothing it did deliver (an all-preserve table any careful engineer would produce, plus a font suggestion that contradicts the codebase) improved the implementation. The implementation succeeded by ignoring the skill's primary verdict.
