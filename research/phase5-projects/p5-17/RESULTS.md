# p5-17 — FleetDesk (Avalonia 11): unsaved-job guard on the dispatch form

**Task (verbatim):** The dispatch job form lets you lose an unsaved job by clicking another one.
**Project / stack / platform:** `p5-avalonia-fleet/project` · C# / Avalonia 11.2, net8.0, hand-rolled MVVM · desktop. p5-16's Service column kept untouched.
**Existing UI or new screen:** existing UI (Dispatch: ListBox of 8 pending jobs + job detail form inside the menu-bar / toolbar / status-bar shell). No new screen; one new modal prompt state.
**Render mode:** html-twin (`project/render/twin.html`, Playwright 1.63.0 Chromium, 1440×900) + static code review; GUI not launched. `dotnet build`: 0 warnings, 0 errors, twice (bin/obj deleted afterwards). Line endings: .cs/.axaml LF as before; twin.html CRLF as before.
**Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (skill untouched).

## 1. Design-context table (01-inspect.json vs code)

Same detector output as p5-16 (the codebase has only gained p5-16's changes since).

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | menu bar + toolbar + bottom status bar (`MainWindow.axaml`) | yes ("left-rail: 1 match" candidate is spurious) |
| theme | light-first | INFERRED | `ThemeVariant.Light` requested explicitly in `App.axaml` | yes (value right; should be KNOWN) |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations found") | flat **bordered**: `BorderThickness=1` + `LineBrush` on every surface/button/input, no shadows | partial (uncertainty flagged, value wrong) |
| radius | unknown | UNKNOWN | `AppCornerRadius=4`, Fluent `ControlCornerRadius=4` | partial |
| spacing | 4 | INFERRED | 8-px scale (`Space1..4` = 8/16/24/32) | no |
| typography | geometric-sans, semibold, no tabular | KNOWN | Segoe UI / Inter (humanist / neo-grotesque); semibold; no tabular figures | partial |
| components | avalonia | KNOWN | Avalonia + DataGrid | yes |

`tokens: []`, `fonts: []` again — `Theme.axaml` is a named token dictionary.

## 2. Requirements verdict (02-requirements.json)

| item | skill | expectation | verdict |
|---|---|---|---|
| platform | `desktop` (project inspection; `platform_evidence: []` from the sentence) | desktop | correct |
| intent.artifact_state | existing | existing | correct |
| intent.operations | diagnose, modify | modify (add a guard) | correct |
| intent.problem_domain | `["interaction"]` (from "click") | interaction / data loss / unsaved state | partial — "lose an unsaved job" (data loss, dirty state) produced no domain signal |
| intent.change_scope | unknown (`intent.scope = moderate`) | small-moderate | acceptable |
| mode + evidence | audit, refactor ("interaction defect on existing UI"; "fix follows the diagnosis") | refactor / polish / audit | yes |
| scope.kind / reason | in-scope, `UI_INTERACTION`, "UI design / interaction task"; `activation.ui_score = 2.0` from the one word "form" | in-scope | correct — but fragile: activation hangs on "form"; "lose", "unsaved", "clicking another one" scored nothing (compare p5-16, which abstained on a sentence without a component noun) |
| change_budget | moderate | low-moderate | correct |
| intent.preserve | `[]` (`constraints.preserve_existing_system: true`) | navigation, theme, typography, component reuse | partial |
| project_context | propagated from inspect | — | inherits spacing=4 / surfaces-tonal errors |
| required concepts (concerns) | keyboard_navigation, focus_visible, validation_errors | `state.unsaved_changes_guard`, `feedback.confirmation_destructive` | **miss** — the concept the sentence is literally about is only *recommended*; `validation_errors` is required although nothing in the task is about validation |

## 3. Guidance verdict (03-guidance.json)

Bundle: core 2 + guardrails 4, `bundle_tokens` 1083, status CONFIDENT, concept coverage 3/3 (of the wrong required set), recommended-concept coverage 0.6.

| record | role | verdict | note |
|---|---|---|---|
| `comp-form` | core | partial | One clause — "unsaved-changes guard" — is the task. The remaining ~90% (label placement, inline validation on blur, error summary, autofill attributes, TV one-field-per-row) is off-task for a fix to an existing, correctly laid-out form. |
| `cta-single-primary` | core | partial | "destructive actions separated and confirmed" and "label is a verb phrase" are usable for the prompt; the rest restates what the form already does. |
| `desktop-keyboard-first` | guardrail | relevant | "every dialog has a default and cancel button" — used (Enter = Save, Esc = Keep editing). F2/Delete/F6 text unused. |
| `a11y-hover-not-required` | guardrail | off-target | BAD `generic`: nothing in the task is hover-revealed. Selected only to tick the "accessibility" concern. |
| `a11y-forms-errors` | guardrail | off-target | BAD `generic`: validation/error recovery; the task has no validation. Selected as "specialist rule for inline validation messages". |
| `desktop-status-bar-and-error-navigation` | guardrail | partial | "sync/save state" region in the status bar — used (`Unsaved changes - J-2041`). F8 error navigation and cell tinting are off-task. |

relevant 1 · partial 3 · off-target 2. Additional BAD: bundle as a whole → `missing-critical`: no record on modal dialogs (focus into the dialog, focus trap, focus return, `aria-modal` / AutomationProperties), no record on confirmation copy for destructive choices (safe default, "cannot be undone"), no record on marking the dirty record visibly. The KB has `comp-dialog` (feedback.confirmation_destructive + a11y.dialog_focus, platforms any) and `a11y-modal-dialog` (a11y.dialog_focus + interaction.focus_restore, desktop) — neither reached the bundle, and neither is in the top-12 search either: lexical retrieval has no purchase because the sentence never says "dialog" or "confirm".

Concept recall (delivered = union over the 6 selected records: `feedback.validation_errors`, `touch.ime_keyboard`, `form.autofill_attributes`, `state.unsaved_changes_guard`, `layout.one_primary_action`, `interaction.keyboard_navigation`, `interaction.shortcuts`, `interaction.focus_visible`, `interaction.hover_independence`, `a11y.live_status`, `a11y.contrast`, `desktop.persist_workspace`):

| expected concept | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| state.unsaved_changes_guard | yes | yes (via `comp-form`, one clause) | — (but only *recommended*, never required: concerns-layer weakness) |
| feedback.confirmation_destructive | yes | no | `expected-concepts` — never demanded (not in required or recommended). KB: `comp-dialog`, `states-persistence-and-session` (rank 6 in search, desktop-eligible), `comp-settings-screen`. |
| a11y.dialog_focus | no | no | `expected-concepts` — never demanded. KB: `comp-dialog`, `a11y-modal-dialog`. |
| interaction.focus_restore | no | no | `expected-concepts` — never demanded. KB (desktop-eligible): `a11y-modal-dialog`. |
| state.saving_conflict | no | no | `bundle-selection` — recommended, and `states-persistence-and-session` (carries it, platform desktop) is rank 6 in search, yet the bundle spent its 6-record soft cap on two generic accessibility rules instead. |
| process.reuse_first | no | no | `candidate-retrieval` — recommended, `impl-reuse-before-new` (platforms any) not in the top 12; no lexical hook. |

**Recall 1/6 = 0.17 · critical recall 1/2 = 0.50.** No knowledge gaps: every missing concept has a desktop-eligible record in the base. `touch.ime_keyboard` was delivered to a desktop task (harmless, inside the composite `comp-form`).

## 4. Direction verdict (04-direction.md/json)

Preserved: navigation, typography, color (correct). Changed: **density** "existing 4 → density-medium" — a phantom change: the codebase already is medium/8-px; the "change" exists only because inspect mis-read spacing as 4. New (no repository evidence): layout `layout-form-stack`, surface `surface-bordered-panes`, cards `card-list-row`, motion, focus `focus-ring-standard`, cta, imagery, icon, metadata. Validation: OK.

- **layout = form-stack: wrong.** The Dispatch screen is a master–detail (360-px ListBox + detail form in `Grid ColumnDefinitions="360,16,*"`); "Master–detail (list + detail pane)" was listed as an alternative at 0.188. Following the slot would restructure the screen. Ignored. `direction-mismatch`.
- surface = bordered panes: matches the code by coincidence; "no repository evidence for this slot" is false (every `Border.surface` has a 1-px border).
- focus = "new": `TextBox:focus … AccentBrush` exists in `Theme.axaml`.
- typography slot text again lists Manrope / Outfit / Urbanist / Sora … under a slot marked *preserve* → `contradicts-codebase`. Ignored.
- cta slot ("destructive actions separated and confirmed") and the navigation slot text ("commands enabled/disabled by state, never hidden") are the two useful lines; both followed.
- imagery / icon / metadata slots are irrelevant to a guard on a form.

## 5. Implementation summary

Files changed (copies in `before/`):

| file | change |
|---|---|
| `ViewModels/DispatchViewModel.cs` | `SelectedJob` setter no longer calls `LoadEditor()` unconditionally: when `HasChanges` and another job is clicked it keeps the dirty job selected (re-notifies `SelectedJob` on the dispatcher so the ListBox snaps back), opens the prompt and stores the click as `_pendingLeave`. New `TryLeave(destination, action)` used for selection, navigation and window close; `IsPromptOpen`, `PromptTitle`, `PromptMessage` ("J-2041 - Pallet delivery - Al Quoz has unsaved changes. Save them before switching to J-2043 - Office relocation?"), `PromptSaveCommand` / `PromptDiscardCommand` / `PromptKeepEditingCommand`; `UnsavedLabel` for the status bar. |
| `ViewModels/MainWindowViewModel.cs` | `Navigate` routes through `Dispatch.TryLeave` (Vehicles / Settings from menu or toolbar cannot silently drop a dirty job); `TryClose` for the window; `UnsavedLabel` forwarded to the status bar; File > Exit now calls `MainWindow.Close()` instead of `Shutdown()` so it passes the guard. |
| `Views/MainWindow.axaml` | Shell wrapped in a `Panel`; window-wide modal prompt: `ScrimBrush` overlay, `Border.surface` 480 px with `Pad3`, section heading, wrapped message, muted "Discard cannot be undone.", buttons **Keep editing · Discard · Save (accent, default)**; `KeyBinding` Enter → Save, Escape → Keep editing; the shell `DockPanel` gets `IsEnabled="{Binding !Dispatch.IsPromptOpen}"` (menu, toolbar, list and form are all unreachable while the prompt is up — the focus trap). `AutomationProperties.Name/HelpText` on the dialog. Status bar gains a save-state region bound to `UnsavedLabel`. |
| `Views/MainWindow.axaml.cs` | Focus into `PromptSaveButton` when the prompt opens, focus returned to the previously focused element when it closes; `OnClosing` → `vm.TryClose`, cancels the close until the user answers. |
| `Views/DispatchView.axaml` | Editor heading becomes heading + `Border.badge.warning` "Unsaved changes" (visible when `HasChanges`); everything else untouched. |
| `Styles/Theme.axaml` | +`ScrimBrush` (CanvasColor at 70 % opacity; flat, no blur, no shadow). |
| `render/twin.html` | `#dispatch` shows the dirty state (edited Title, heading badge, status-bar region); new `#dispatch-prompt` section shows the prompt after clicking "Office relocation" (dirty job still selected, scrim over the whole window, Save focused). |

Guidance used: "unsaved-changes guard" (`comp-form`); "every dialog has a default and cancel button" (`desktop-keyboard-first`); "save state in the status bar" (`desktop-status-bar-and-error-navigation`); "destructive actions separated and confirmed", verb-phrase labels (`cta-single-primary`); navigation-slot "commands disabled by state, never hidden" (menu/toolbar disabled, not hidden, while modal). Ignored: `a11y-hover-not-required`, `a11y-forms-errors` (nothing to apply); direction layout = form-stack (wrong for a master–detail); typography font list; density "change"; imagery/icon/metadata slots. Brought in without skill support (from the expectation, not the bundle): focus trap + focus restore, `AutomationProperties` on the dialog, safe-default ordering with an explicit "cannot be undone" line, the visible dirty marker in text, guarding navigation and window close as the same defect class.

Engineering choices worth recording: the prompt is an in-window modal overlay rather than a `Window.ShowDialog` — keeps the hand-rolled MVVM free of a dialog service and lets the twin render it; the trade-off is that it is not an OS-level dialog (no separate taskbar entry, no OS-level Enter/Esc semantics — those are supplied by `KeyBinding`). Save is the default because it is the non-destructive choice; Discard is the middle button and never triggered by a key. Not done: autosave / draft restore (would change the data model's semantics; the sentence asks for a guard, not autosave).

## 6. Render and defects

Screenshots: `render/first-dispatch-1440x900.png`, `render/first-dispatch-prompt-1440x900.png`, `render/final-*` (same two states). Geometry from `shot.js`: dialog 480×199 at (480, 350), horizontally centred; message wraps to 2 lines; buttons 96–98 × 30; "Save" carries the focus adorner; the dirty job stays the selected row in the prompt state; heading row 22 px with the badge inline; status bar reads "Dispatch view · Unsaved changes - J-2041 · …".

First-render defects: visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · **implementation-bug 1** — the twin showed the scrim over the whole window (menu bar and toolbar included) while the first Avalonia implementation hosted the overlay inside `DispatchView`, i.e. only over the content area, leaving the menu bar and toolbar clickable during the "modal" prompt (Vehicles / Save job would still fire). Fixed by moving the prompt to `MainWindow` and disabling the shell `DockPanel` while it is open; the twin was already right, so `final-*` is pixel-identical to `first-*`. Contrast (static): warning badge text 4.51:1 on its tint; dialog body text 12.6:1; muted line 5.4:1; accent button 5.2:1 (12 px+ semibold-free 13 px, AA). No colour-only state: dirty = badge with words + status-bar text; prompt = words + default-button emphasis.

Final defects: all 0. **Iterations: 1** (one code fix, one re-render).

## 7. Preservation verdict

navigation ✓ (menu bar, toolbar, status bar unchanged in structure; one status-bar text region added; shell disabled — not hidden — while modal) · theme ✓ (light; one new brush derived from `CanvasColor`) · typography ✓ (Segoe UI/Inter, section/body/small roles reused) · component reuse ✓ (`Border.surface`, `Border.badge.warning`, `Button`, `Button.accent`, `TextBlock.section/.muted`, `Pad3`, `Space2`, `MarginRight1`) · 4-px radius, 1-px borders, no shadows, no blur ✓ · unjustified structural changes 0. Routes/ids/commands intact: `SaveCommand` / `CancelCommand` / Ctrl+S / toolbar "Save job" behave as before. **preservation-ok.**

## 8. Regressions to propose

1. Query: the task sentence verbatim with the Avalonia project. Expect: `state.unsaved_changes_guard` and `feedback.confirmation_destructive` in *required* concepts (not merely recommended); bundle contains `comp-dialog` or `a11y-modal-dialog` (dialog focus / focus restore) and `states-persistence-and-session`; `a11y-hover-not-required` and `a11y-forms-errors` not selected when the sentence has no hover and no validation cue.
2. Query: "Users lose their edits when they switch records in the settings page" (web, existing). Expect: not abstain even though "form" is absent (p5-16 showed the gate depends on a component noun); same two critical concepts.
3. Query: "The editor lets you close the window with unsaved changes" (desktop). Expect: `state.unsaved_changes_guard`, `feedback.confirmation_destructive`, `a11y.dialog_focus` demanded; a desktop dialog record in the bundle.
4. Direction: an existing screen with `ListBox` + detail `Grid ColumnDefinitions="360,16,*"` (or any list + detail pair) → layout slot **preserved as master–detail**, not "new: form-stack"; surface slot marked preserved when `BorderThickness`/`BorderBrush` resources exist.
5. Requirements: `feedback.validation_errors` must not be *required* for a form task whose sentence contains no validation cue ("invalid", "error", "required", "wrong"); `validation_errors` currently displaces the on-task concept.
6. Inspect (carried from p5-16): `Theme.axaml` with `CornerRadius`/`Thickness`/`x:Double Space1..4` → radius 4 KNOWN, surfaces flat-bordered, spacing 8, tokens non-empty; direction must then not report a density "change".

## 9. Tags

`requirements-miss` (problem_domain / required-concept set), `concept-miss`, `ranking-miss` (two generic accessibility rules outrank `states-persistence-and-session`), `context-detection-miss`, `direction-mismatch` (layout form-stack vs master–detail; phantom density change; typography font list), `render-defect-fixed`, `skill-helped`, `preservation-ok`, `tooling-limit` (Avalonia rendered via HTML twin, GUI not launched).

Skill effect: **helped, marginally.** In-scope this time, and three lines of the bundle were used (guard, default + cancel button on every dialog, save state in the status bar). Everything that makes the prompt a correct modal — focus in, focus trap, focus return, safe default, "cannot be undone", visible dirty marker, guarding navigation and close as the same defect — came from outside the bundle although the base holds records for all of it. Two of six records were pure filler chosen to satisfy the "accessibility" concern, and the direction's layout slot would have been harmful if followed.
