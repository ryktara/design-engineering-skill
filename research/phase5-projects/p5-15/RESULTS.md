# p5-15 — results

## Task

"Review the stock adjustments page against our accessibility checklist." (verbatim, run as-is)

Audit task: deliverable is `05-review.md` (12 findings, 2 Blockers fixed, 10 documented). Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8`; nothing under `design-engineering/` was touched.

## Project / stack / platform

`research/phase3-projects/p3-winui-erp-audit/project` — WinUI 3 (Windows App SDK 1.7), CommunityToolkit DataGrid 7.1.2, CommunityToolkit.Mvvm 8.4, x64 desktop. Shell: `MainWindow` NavigationView (left pane, `PaneDisplayMode=Auto`) + `Frame`, Mica backdrop; `App.xaml` overrides `SystemAccentColor` per theme only. **Existing UI** (the page was refactored in Phase 3; this task reviews that result). No new screen.

Render mode: **static-review** (+ an HTML-twin screenshot reused from Phase 3 as a sanity check that the visible header text is unchanged). `dotnet build` is not possible here (no Windows App SDK build workload — Phase 3 tooling limit still applies), so Narrator / Accessibility Insights verification is listed per finding instead.

## Design-context table (`01-inspect.json`)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | left-rail (also menu-bar: 11) | KNOWN | `NavigationView` left pane + `Frame` in MainWindow.xaml | yes (the "menu-bar" candidate is `CommandBar`/`MenuFlyout` noise) |
| theme | dual-theme | INFERRED | Light/Dark `ThemeDictionaries` in App.xaml, `ThemeResource` brushes throughout, Mica | yes (could be KNOWN: the dictionaries are explicit) |
| surfaces | bordered-flat | INFERRED | card `Border` with `CardStrokeColorDefaultBrush` + `CardBackgroundFillColorDefaultBrush`, no shadows | yes |
| radius | unknown | UNKNOWN | `{StaticResource OverlayCornerRadius}` / `ControlCornerRadius` (WinUI 8/4 epx) used explicitly | partial (code is clear) |
| spacing | 4 | INFERRED | 16/12/8/4 epx paddings and spacings | yes |
| typography | unknown; `tabular_numerals: false` | UNKNOWN | WinUI text styles (`Body/Caption/Title/SubtitleTextBlockStyle` → Segoe UI Variable), `Typography.NumeralAlignment="Tabular"` present | partial (style-based typography not recognised; the tabular flag is wrong → no) |
| components | winui3, community-toolkit | KNOWN | DataGrid, CommandBar, InfoBar, ContentDialog | yes |
| platforms | desktop | KNOWN | desktop | yes (the Phase 3 `ListView`→`isTV` false positive did not trigger: the page no longer contains a ListView; the regex itself was not re-tested) |

Also: `accessibility: a11y attributes present in 2 files` and `focus_handling: 3 files` — right. Fonts/icons still empty (Segoe Fluent Icons glyphs present).

## Requirements verdict (`02-requirements.json`, exit 0, CONFIDENT)

| field | value | verdict |
|---|---|---|
| platform_evidence / platform | `[]` / desktop (from project inspection) | correct; evidence list empty but `known[]` records "platform=desktop (project inspection)" |
| intent.artifact_state | existing ("our", "the stock adjustments page") | correct |
| intent.operations | review | correct |
| intent.problem_domain | accessibility | correct |
| intent.change_scope | screen ("page") | correct |
| intent.diagnose_only | true | correct for an audit |
| mode + evidence | accessibility, audit, review — "explicit: review the", "explicit: accessibility", "assessment without changes" | correct, all three acceptable |
| scope.kind / reason | in-scope, UI_ACCESSIBILITY | correct |
| change_budget | low | correct |
| intent.preserve | `[]` | partial — `constraints.preserve_existing_system=true` is right but the preserve list is empty for a low-budget review |
| density | high (implied by erp) | correct |
| components / screen | `["list"]` / `[]` | partial — the repo has a Toolkit DataGrid and the sentence says "page"; "list" is weak, screen should be a table/working screen; `primary_jobs: ["accessibility list"]` is an odd artefact |
| accessibility flags | keyboard, screen_reader, focus, reduced_motion, contrast all true | correct |
| project_context | as in the table above | passed through |

## Guidance verdict (`03-guidance.md/json`, bundle 7 = core 2 + guardrails 5, 848 tokens, exit 0)

| record | role | verdict | BAD category | why |
|---|---|---|---|---|
| `comp-setup-checklist` | core | off-target | wrong-mode | Picked as "what to build" from the word "checklist" (lexical 0.408). The sentence's checklist is the review instrument, not a UI component; an audit with `diagnose_only=true` should not have a build-a-component core. |
| `imagery-none` | core | off-target | generic | Nothing on the page has imagery; harmless but zero information for an accessibility review. |
| `a11y-nontext-contrast` | guardrail | relevant | — | Focus ring / status glyph / control boundary 3:1 → F7 (High Contrast chrome). |
| `a11y-native-semantics` | guardrail | relevant | — | "WinUI/WPF AutomationProperties + AutomationPeer … announce async status with live regions … Test with Narrator, not only by reading code" — the family of the two Blockers (F1, F2) and F4. Generic; the WinUI-specific facts (string header name, LiveSetting needs RaiseAutomationEvent, Panels have no peer) are not in it. |
| `typo-scale-and-roles` | guardrail | partial | — | Tabular figures clause relevant (passes); "generate a type scale with tokens.py" is off for a review. |
| `a11y-keyboard-operable` | guardrail | relevant | — | "composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell" → F3 (row buttons unreachable); Escape/focus return → dialog check. |
| `layout-states-empty-loading-error` | guardrail | partial | — | Empty/loading exist; "announce completion" → F11. Mostly a create-mode record. |

Counts: relevant 3, partial 2, off-target 2.

Concept recall (expected from `00-expectation.json`; delivered = union of `concepts` over selected records = a11y.contrast, interaction.focus_visible, a11y.semantics, a11y.accessible_names, table.tabular_figures, brand.type_roles, interaction.keyboard_navigation, interaction.hover_independence, state.loading_empty_error, onboarding.setup_checklist, feedback.progress_indicator):

| expected id | delivered? | layer if missing |
|---|---|---|
| a11y.accessible_names | yes (a11y-native-semantics) | — |
| a11y.color_not_only | no | bundle-selection — demanded only as *recommended* ("related to a11y.contrast"), candidate `a11y-color-not-only` 0.271 existed, "bundle cap or lower utility left it out". Root cause is arguably expected-concepts (it should be *required* in an accessibility audit), but per protocol the earliest layer where it was actually dropped is bundle-selection. |
| a11y.contrast | yes (a11y-nontext-contrast) | — |
| interaction.keyboard_navigation | yes (a11y-keyboard-operable) | — |
| interaction.focus_visible | yes (a11y-nontext-contrast, via "covers: visible focus") | — |
| interaction.hover_independence | yes (a11y-keyboard-operable) | — |
| a11y.live_status | no | bundle-selection — recommended only; candidate `a11y-live-status` 0.243 dropped. This concept is the page's biggest real defect (F2). |

Recall 5/7 = **0.71**; critical (accessible_names, color_not_only, contrast, keyboard_navigation) 3/4 = **0.75**.

Other observations from `concept_trace`: `a11y.text_scaling` (candidate `a11y-text-scaling` 0.243) and `interaction.shortcuts` were demanded as recommended and dropped; text scaling turned out to be a Major finding (F5) and the skill's own record ("Windows: text scaling 100–225 %. Containers grow with text") would have named it. `grid-single-tab-stop` (0.324, WinUI note: "DataGrid: TabNavigation=Once … expose row actions in a CommandBarFlyout on Menu key / Shift+F10") was a candidate for keyboard_navigation and lost to the generic `a11y-keyboard-operable`; it describes F3 exactly. `comp-data-table` (0.324) was a candidate for tabular figures but the bundle took `typo-scale-and-roles`.

Forbidden concepts: none delivered (no TV/kiosk/brand records; `focus-scale-glow` correctly rejected as TV).

Search (`03-search-k12.md`, exit 3 PARTIAL without `--project`): rank 1 `comp-product-detail-page` (lexical 0.544 on "stock"/"page"), rank 2 `comp-setup-checklist`; `a11y-native-semantics` rank 3, `a11y-nontext-contrast` rank 4, `focus-ring-standard` rank 6. Without the inspect JSON the sentence alone retrieves e-commerce and onboarding components ahead of accessibility rules; with `--project` the platform filter removes the PDP/checkout ones but `comp-setup-checklist` survives because it is platform-agnostic.

## Direction verdict (`04-direction.md/json`, exit 0, Validation OK)

Change budget low; 12 slots **preserved**, 0 changed, 1 **new**: `focus` → `focus-ring-standard` "no repository evidence for this slot". Compatibility table: navigation `nav-left-rail` (matches NavigationView — the Phase 3 `nav-breadcrumb-tree` mismatch is gone), surface `surface-bordered-panes`, color `color-neutral-accent`, all other slots "keep as implemented". Fingerprint: left-rail / bordered / none / sharp / neutral-plus-accent / ring.

Judgement: every preserved slot is justified. The one "new" slot is a context-detection miss, not a design error — the repo has `UseSystemFocusVisuals="True"` and the inspector reports "explicit focus handling in 3 files", yet the focus slot is never populated from the repository; the recommendation itself (keep the platform ring, `UseSystemFocusVisuals=True`) is what the code already does, so no structural change was proposed. `corner_language: sharp` is wrong for WinUI (`OverlayCornerRadius` 8 epx / `ControlCornerRadius` 4 epx are in the page) — same radius UNKNOWN miss as the inspector. Nothing in the direction conflicts with an audit; nothing in it was needed for one either.

## Implementation summary

Files changed (originals in `before/`): `Views/StockAdjustmentsPage.xaml` (numeric column headers back to string `Header` + right-aligned `HeaderStyle`; `x:Name` on the two live-region TextBlocks), `Views/StockAdjustmentsPage.xaml.cs` (raise `LiveRegionChanged` on `ResultSummary`/`SelectionLabel` changes, subscribed in `Loaded`), `ViewModels/StockAdjustmentsViewModel.cs` (`Notify()` toggles `Message` so the InfoBar re-opens and announces). Only the two Blockers were fixed; the other 10 findings are documented with fixes in `05-review.md`.

Guidance used: `a11y-native-semantics` (frame for F1/F2/F4, and its "test with Narrator, not only by reading code" caveat is repeated in every finding), `a11y-keyboard-operable` (F3), `a11y-nontext-contrast` (F7), `layout-states…` "announce completion" (F11). Guidance ignored: `comp-setup-checklist` and `imagery-none` (irrelevant to a review); `typo-scale-and-roles` token generation (not a review action). What the audit needed and the skill did not supply: the WinUI-specific mechanics behind F1 (Toolkit header/cell peer naming from string content only), F2 (LiveSetting requires `RaiseAutomationEvent`; InfoBar announces only on open), F4 (Panels have no automation peer), F5 (Windows text scaling vs fixed `RowHeight`) — all verified from the Toolkit 7.1.2 source and Microsoft Learn, not from the skill.

## Render

`render/first-desktop.png`, `render/final-desktop.png` (1440×900, HTML twin `render/twin.html` copied from the Phase 3 after-twin; `render/shot.js` reuses the Phase 3 Playwright install). The twin is a web mirror and cannot show UIA names or live regions; it confirms the visible header labels and alignment are unchanged by the fixes (`["Status","Adjustment","SKU","Description","Location","Reason","Before","Change","After","Value (EUR)","Actions"]` before and after).

## Defects by type

Audit-only in the protocol's sense: the code changes are UIA-only. First-render (twin) defects: visual 0, interaction 0, accessibility 0 (the twin does not model UIA), platform 0, existing-system-mismatch 0, implementation-bug 0. Final: all 0. Iterations: 1 (edit → twin re-render, identical). The 12 accessibility findings of the review itself are in `05-review.md` (2 Blocker fixed, 3 Major, 3 Moderate, 4 Minor).

## Preservation verdict

Navigation, theme, typography, components, routes, state, ids untouched; the only user-visible behaviour change is that the InfoBar re-opens for every approve/reject (a fix). Unjustified structural changes: 0. **preservation-ok**.

## Misses by earliest wrong layer

| layer | what |
|---|---|
| requirements | `components=["list"]`, `screen=[]`, `primary_jobs=["accessibility list"]`, `preserve=[]` for a read-only review of a DataGrid page |
| expected-concepts | in an accessibility audit `a11y.color_not_only`, `a11y.live_status`, `a11y.text_scaling` are demanded only as *recommended*; they are checklist items, not nice-to-haves |
| bundle-selection | `a11y-color-not-only`, `a11y-live-status`, `a11y-text-scaling`, `grid-single-tab-stop` all had candidates and were dropped; `comp-setup-checklist` (a lexical hit on "checklist") took a core slot in diagnose-only mode |
| context-detection | radius UNKNOWN and `corner_language: sharp` despite `OverlayCornerRadius`/`ControlCornerRadius`; typography UNKNOWN and `tabular_numerals: false` despite `Typography.NumeralAlignment="Tabular"`; focus slot never read from the repo (`UseSystemFocusVisuals`) so direction marks it "new" |
| knowledge-gap | WinUI mechanics: XAML `LiveSetting` needs `RaiseAutomationEvent(LiveRegionChanged)`; `InfoBar` announces only on the closed→open transition; Panels (`StackPanel`/`Grid`/`Border`) have no automation peer so `AutomationProperties.Name` on them is not a cell/element name; Toolkit DataGrid header/cell names come only from string `Header` / direct `TextBlock` / `ClipboardContentBinding`; fixed `RowHeight` vs Windows text scaling 225 % (the generic `a11y-text-scaling` record exists but has no WinUI note) |

## Regressions to propose

1. Query: "Review the stock adjustments page against our accessibility checklist." with `--project` (desktop, winui, erp). Expect: in `diagnose_only` / audit-review mode no core "what to build" component is selected on lexical evidence alone; specifically `comp-setup-checklist` must not appear for the word "checklist".
2. Query: any accessibility-mode audit on desktop/web. Expect: `a11y.color_not_only`, `a11y.live_status`, `a11y.text_scaling` are *required* concepts (an accessibility checklist without them is incomplete), and the bundle delivers `a11y-color-not-only`, `a11y-live-status`, `a11y-text-scaling` or records covering those ids.
3. Query: same sentence, stack winui, repo with a DataGrid and per-row buttons. Expect: `grid-single-tab-stop` (or `comp-data-table`) is selected for `interaction.keyboard_navigation` ahead of the generic `a11y-keyboard-operable` when the project has a grid.
4. Inspector: a WinUI/WPF project using `OverlayCornerRadius`/`ControlCornerRadius` and `Typography.NumeralAlignment="Tabular"`. Expect: radius KNOWN (4/8 epx theme resources), typography KNOWN (system text styles), `tabular_numerals: true`; direction fingerprint `corner_language` ≠ sharp.
5. Direction on a low-budget review of a repo with `UseSystemFocusVisuals="True"` / focus handling detected. Expect: the focus slot is "preserved (system focus visuals)", not "new".
6. Knowledge: `a11y-live-status` and `a11y-native-semantics` gain WinUI notes ("`AutomationProperties.LiveSetting` + `RaiseAutomationEvent(AutomationEvents.LiveRegionChanged)` after the text changes; InfoBar announces on open only; Panels have no automation peer"); `a11y-text-scaling` gains a WinUI note ("no fixed `Height`/`RowHeight` on text rows; test 100–225 %"); `comp-data-table` WinUI note gains "keep `Header` a string or set `AutomationProperties.Name` on the header; template cells need `ClipboardContentBinding` for a UIA name".

## Tags

`requirements-miss` (components/screen/preserve), `concept-miss` (color_not_only, live_status as recommended-only), `ranking-miss` (setup-checklist core; grid-single-tab-stop / a11y-live-status / a11y-text-scaling dropped), `knowledge-gap` (WinUI UIA mechanics above), `context-detection-miss` (radius, typography/tabular, focus slot), `skill-neutral` (mode/platform/scope/budget/preservation all correct and the guardrails framed the review, but every actionable finding came from reading the Toolkit source and Microsoft Learn; the two off-target core records cost nothing but delivered nothing), `preservation-ok`, `tooling-limit` (no Windows App SDK build; Narrator unverified), `partial-scope-ok` not applicable (in-scope).
