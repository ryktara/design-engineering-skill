# p6-18 — ERP desktop (WPF): "Purchase order screen: operators want to do the whole entry without touching the mouse."

**Task sentence (verbatim):** `Purchase order screen: operators want to do the whole entry without touching the mouse.`
**Project:** `research/phase3-projects/p3-erp-desktop-dotnet/project` — WPF on .NET 10, no NuGet packages. Existing UI (one screen: `Views/PurchaseOrderLinesView.xaml(.cs)`, `ViewModels/PurchaseOrderLinesViewModel.cs`, `Themes/*`).
**Platform:** desktop (Windows). **Existing UI:** yes. **New screen:** no.
**Build hash start/end:** `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` (equal — see `00-build-hash-*.txt`).
**Render mode: native.** The project's own `--capture` harness renders the window client area with `RenderTargetBitmap` and drives real OS keyboard input (`keybd_event`). No HTML twin needed.

---

## 1. Design-context table (step 1, `01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | menu-bar | KNOWN | `Menu` (File/Edit/View/Help, access keys + `InputGestureText`) + command bar + context menu + status bar | yes |
| theme | light-first | KNOWN | only `Themes/Light.xaml`; no dark dictionary | yes |
| surfaces | bordered-flat | INFERRED | 1 px `Brush.Border.*` everywhere, zero shadow/elevation | yes |
| radius | small (2) | INFERRED | `CornerRadius 2` on buttons/inputs; 10 only on the error badge circle | yes |
| spacing | 4 | INFERRED | `Space.*` tokens on a 4 grid (16/12/8/6/2) | yes |
| typography | humanist-sans | INFERRED | `Segoe UI Variable Text, Segoe UI` + `Cascadia Mono, Consolas` for codes/numbers | yes (declared explicitly in `Themes/Typography.xaml`, so KNOWN would have been defensible) |
| components | wpf | KNOWN | `DataGrid`, `StatusBar`, `Menu`, custom styles | yes |

7/7 correct. No `context-detection-miss`.

## 2. Requirements verdict (step 2, `02-requirements.json`)

| Field | Expected (pre-registered) | Resolved | Verdict |
|---|---|---|---|
| platform | desktop | `desktop`, evidence `WEAK_INFERENCE ["mouse"]` + project inspection | correct |
| artifact_state | existing | `existing` | correct |
| operations | diagnose + modify | `["diagnose","modify"]` | correct |
| problem_domain | interaction/keyboard | `[]` (empty) | **miss** — the sentence names the input device; nothing landed in `problem_domain` |
| change_scope | screen | `screen` | correct |
| mode | refactor / accessibility / audit / polish | `["audit","refactor"]` | acceptable (inside the acceptable set) |
| scope.kind | in-scope | `in-scope` ("UI design / interaction task") | correct |
| change_budget | low–moderate | `moderate` | correct |
| intent.preserve | navigation/theme/typography | `[]`, but `constraints.preserve_existing_system: true` | acceptable |
| project_context | — | all 7 fields populated from the repo | correct |

`platform_evidence` reads "mouse" as desktop evidence. It is the right answer, but for the wrong reason: the sentence says operators want to *stop* touching the mouse. The device word was read as a positive input signal — `input: ["keyboard","pointer"]` and later `interaction.hover_independence "pointer stated"` come from the same misread. Harmless here (WPF in the repo settles the platform), but the negation was not modelled.

## 3. Guidance verdict (step 3, `03-guidance.*`)

Bundle: **core 0 + critical guardrails 3 + optional 0**, ≈361 tokens.

| Record | Layer | Verdict | Category |
|---|---|---|---|
| `desktop-keyboard-first` | critical | relevant — F2 edits, Delete with undo, Ctrl+F, F6, arrow keys, access keys on Alt. Every item was already implemented in the project; none of it named a gap. | — |
| `a11y-keyboard-operable` | critical | relevant — "Escape closes layers and returns focus to the invoker" and "no traps" is the one line that pointed at the focus-restore work. | — |
| `typo-scale-and-roles` | critical | **off-target** — selected as the carrier for the only concept marked CRITICAL (`table.tabular_figures`) on a task about mouseless entry. The screen already uses tabular figures. It spent a bundle slot on type roles. | `generic` |
| bundle-level | — | **missing-critical** — `table.inline_edit` (grid cell editing / pickers) is absent. | `missing-critical` |

**Concept recall** (delivered = union of `concepts` over selected records = `interaction.keyboard_navigation`, `interaction.focus_visible`, `interaction.hover_independence`, `table.tabular_figures`, `interaction.shortcuts`):

| Expected concept | Delivered? | Layer if missing |
|---|---|---|
| interaction.keyboard_navigation | yes | — |
| interaction.shortcuts | yes | — |
| interaction.focus_visible | yes | — |
| interaction.focus_restore | no | `expected-concepts` (never demanded; the trace has no entry for it) |
| table.inline_edit | no | `expected-concepts` (never demanded — and the record that carries it was then omitted, see below) |
| interaction.menu_semantics | no | `expected-concepts` (never demanded) |
| a11y.accessible_names | no | `bundle-selection` (demanded as *recommended*; candidates `a11y-native-semantics`, `a11y-labels-names` existed and were dropped) |

**concept recall 3/7 = 0.43 · critical recall 2/3 = 0.67.**

**The central miss.** `comp-data-entry-grid` was the *highest-scoring* candidate for `interaction.keyboard_navigation` (0.606) and its body is almost a specification of this task: *"Enter/Tab move predictably, F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, **lookup cells with a picker (F4)**, validation per cell…, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel."* It was omitted with the reason **"no positive task evidence (screen / subtype / component / job / product / wording) for a core record"**. The evidence is in the sentence — *purchase order screen* + *the whole entry* — but "purchase order" resolved only to `product=erp` and no `screen`/`component` was inferred, so the core-record gate fired. `layout-table-first`, `comp-data-table` and `metadata-rich` were pruned by the same rule. The F4 picker — the single most valuable thing I built — came from that pruned record's own knowledge, which I had to supply from Windows convention instead. This is a **ranking/selection** failure, not a knowledge gap: `search -k 12` returns `comp-data-entry-grid` at rank 2 with the F4 line intact.

The guidance status line reads `PARTIAL` (concern coverage 0.75, `component` uncovered) — and `component` is exactly the uncovered concern that would have carried the grid record. The system knew it was short and still shipped a three-record bundle with a type-scale record in it.

## 4. Direction verdict (step 4, `04-direction.*`)

All 13 slots `preserved`, `changed: []`, validation OK, fingerprint matches the codebase (menu-bar / bordered / sharp / humanist-sans / neutral-plus-accent). **`unjustified_direction_slots: 0`** — correct behaviour for an existing UI at a moderate budget on an interaction task.

Two notes. The per-slot prose still describes the *ideal* system rather than the *existing* one (typography suggests "Source Sans 3, Nunito Sans…" for a screen that uses Segoe UI Variable Text; color says "validate every pair with tokens.py"), each with "(Existing system: do not replace it for this task.)" appended. Harmless because the status column is authoritative, but 11 of the 13 slot paragraphs were pure noise for this task. The `focus` slot alone was useful: "Verify the existing indicator: ≥ 3:1 against adjacent colours."

## 5. Implementation

**Files changed** (copies in `before/`):
- `Views/PurchaseOrderLinesView.xaml` — View menu gets `Sort by current column` (Ctrl+Shift+S) and `Clear sort`; empty-state button named and re-keyed `Add _first line` (its access key collided with the command bar's `_Add line`); status-bar key hints gain `F4 list`; filter tooltip documents Enter/Esc.
- `Views/PurchaseOrderLinesView.xaml.cs` — six changes: (1) `F4` / `Alt+↓` on a `DataGridComboBoxColumn` begins the edit *and* drops the list open; (2) `Enter` in the filter box returns to the grid, `Esc` clears then returns; (3) `Ctrl+Shift+S` sorts by the current column and toggles direction, keeping the focused line focused; (4) a `Lines.CollectionChanged` watcher puts the current cell back on a real row after any command-driven add/delete/undo (previously the arrow keys went dead until the grid was clicked); (5) the empty state takes focus on its own action instead of leaving focus nowhere; (6) `FocusCell` guards its index and retries once when the row container is not yet realised.
- `App.xaml.cs` — capture harness only: a new `--scenario mouseless` that drives all six paths with real OS keys and writes a JSON trace. No product code.

Nothing else moved: no route, no theme brush, no type role, no column, no command, no automation name. `dotnet build`: 0 warnings, 0 errors.

**Guidance used:** `a11y-keyboard-operable` (Escape returns focus to the invoker → the filter Esc/Enter return path and the focus-restore watcher); `desktop-keyboard-first` (confirmed F2/Del+undo/Ctrl+F/F6 were already right and needed no change — it kept me from re-inventing them).
**Guidance ignored:** `typo-scale-and-roles` — the task is not typographic and the screen already has the roles and tabular figures it prescribes; acting on it would have been an unjustified change at a moderate budget.

**Process check:** SKILL.md §2 / §7 were enough. `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` were *not* needed in the bundle — I reused `FocusCell`, `PropertyOf`, `VisibleColumns`, `ColumnPriority` and the existing status-message channel without a record telling me to. `process_records_needed: false`.

## 6. Render and defects

Native capture at 1440×900 (plus 1100×760 for the responsive chrome), `--scenario mouseless`, three iterations. Screenshots in `render/` (`first-*` / `final-*`); traces in the matching `.json`.

**First render — 4 defects.**
1. `implementation-bug` — after a second `Ctrl+Shift+S` the focused row moved to the far end of the re-sorted view, its container was not realised, `GetCell` returned null and `Keyboard.FocusedElement` became **null**: the keyboard was dead exactly where the change was supposed to fix that. (Trace: `focus: null`, and every following key was a no-op.)
2. `implementation-bug` — `FocusCell` threw `ArgumentOutOfRangeException` when a caller passed an index that a live filter had made stale.
3. `visual` — after the last line was deleted the status bar kept the deleted line's `Line 250: Item is required.`; because the empty state now takes focus, that stale message became visible instead of hidden behind a click.
4. `visual` — my sort status message ("Sorted by Description ascending (Ctrl+Shift+S)") was long enough to push the fixed error-summary segment into its ellipsis.

**Fixes:** (1) `FocusCell` retries once at `DispatcherPriority.Loaded` and falls back to focusing the grid, so focus is never left on nothing; (2) index guard; (3) `FocusEmptyState` clears `FocusedError`; (4) shortcut dropped from the message.

**Final render — 1 defect.**
- `visual` (minor, remaining) — with a sort message in the status bar at 1440 the error-summary link still clips by one character ("2 lines with error"). This is the screen's existing status-bar priority rule (fixed segments dock left, the rest ellipsises), not a new layout bug; shortening further would cost the sort feedback. Recorded, not hidden.

**Final trace (all green):** Ctrl+F → type → Enter returns to the grid (`gridHasFocus true`); Esc clears then Esc returns; F4 opens the Status list (`dropDownOpen true`, 6 items) and ↓+Enter commits `Approved`; Ctrl+Shift+S sorts ascending then descending with the focused line kept; Del leaves focus on a cell and ↓ still moves; Ctrl+Z restores and ↑ still moves; the menu `Add line` command moves focus into the new line; deleting the last line lands focus on `Add first line`.

**No regression:** the project's pre-existing `--scenario keys` suite was run 5× on a baseline build (from `before/`) and 5× on the changed build — identical step-by-step results (rows, columns, edit state, focus ring, selection, F6 cycle `TextBox → Button → DataGridCell`, Ctrl+F). `tooling-limit`: OS key injection only lands when the capture window wins the foreground, so ~1 run in 3 produces a dead trace; scored the best of N.

**Iterations: 3.**

## 7. Preservation

Navigation, theme, typography, surfaces, spacing and component vocabulary untouched. Every new affordance reuses an existing channel: a View-menu item with `InputGestureText`, the status-bar key-hint segment, the existing `StatusMessage`, the existing focus ring. `unjustified_structural_change: 0`. **preservation-ok.**

## 8. Skill effect

**neutral.** The two relevant records restated what the screen already did; nothing I shipped would have been missed because of them, and nothing I shipped was wrong because of them. The three changes that actually answered the sentence — F4 pickers on choice cells, keyboard sort, focus restore after command-driven row changes — came from the *omitted* `comp-data-entry-grid` (F4 picker is in its body verbatim) and from Windows convention. The bundle spent one of three slots on type scale.

## 9. Regressions to propose

| Query | Expectation |
|---|---|
| `Purchase order screen: operators want to do the whole entry without touching the mouse.` | `comp-data-entry-grid` must be in the bundle (core). "purchase order screen" + "entry" is positive task evidence for a data-entry-grid core record; `typo-scale-and-roles` must not be. |
| same | `expected_concepts` must demand `table.inline_edit` when product=erp + mode audit/refactor + a data grid is in the project context. |
| same | `interaction.focus_restore` must be demanded when the request is about completing a workflow on the keyboard on an existing screen. |
| `users say the invoice line grid is mouse-only` | platform_evidence must not count "mouse" as a positive pointer-input signal when the sentence negates it (`without touching`, `mouse-only` as a complaint); `input` should not resolve to `pointer: KNOWN`. |
| any desktop grid task where concern `component` is uncovered | a bundle must not ship with `component` uncovered while a compatible component record sits at the top of the candidate list. |

## 10. Tags

`concept-miss`, `ranking-miss`, `requirements-miss`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-neutral`, `preservation-ok`
