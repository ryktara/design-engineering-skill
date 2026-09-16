# p4-03 — stock adjustments page: keyboard shortcuts + command bar (existing WinUI UI)

## Task
"add keyboard shortcuts and a command bar to the existing stock adjustments page without changing its navigation or theme"

## Project / stack / platform
`phase3-projects/p3-winui-erp-audit/project` — WinUI 3 (Windows App SDK 1.7), CommunityToolkit.Mvvm + Toolkit DataGrid, `NavigationView` shell in `MainWindow.xaml`, Fluent theme resources with an accent override in `App.xaml`. Desktop, existing UI.

Render mode: **html-twin + static review** at 1440×900 (320 px NavigationView + 1088 px content). `dotnet build` was attempted in a scratch copy for both the pre-task and the post-task XAML: both fail identically at `XamlCompiler.exe` exit 1 with no diagnostic (Windows App SDK build tooling is not installed; same **tooling limit** as Phase 3), so the failure is not attributable to this change. The XAML was reviewed statically against the winui stack file and mirrored 1:1 in `render/after.html` (`render/before.html` is the Phase 3 twin of the page as it was).

## Important premise note
The page **already had** a `CommandBar` with four `AppBarButton`s, `KeyboardAccelerator`s (Ctrl+N, Ctrl+Shift+A, Ctrl+Shift+R, F5, Ctrl+F, F2), `AccessKey`s and accelerator text in tooltips — added by the Phase 3 refactor. The task sentence asks to "add" what exists. I treated it as "complete the command bar and shortcut system of the existing page": what was missing was the documentation of shortcuts in one place, the secondary/overflow commands, region cycling, a selection indicator next to the commands, accelerator text in the context menu, Esc/clear behaviour, and the un-toggleable "Created by" column left over from Phase 3.

## Design-context table (`01-inspect.json`)
| Field | Detected | Status | Actual (`MainWindow.xaml`, `App.xaml`, `StockAdjustmentsPage.xaml`) | Correct? |
|---|---|---|---|---|
| navigation | left-rail (also "menu-bar: 9 matches") | KNOWN | `NavigationView` `PaneDisplayMode=Auto` with a `Frame`; no menu bar (the 9 hits are `MenuFlyout`/`MenuFlyoutItem`) | partial (rail right; menu-bar candidate is a false signal) |
| theme | dual-theme | INFERRED | `ThemeDictionaries` Light/Dark with `SystemAccentColor` #0F6CBD / #479EF5, `MicaBackdrop`, every brush a `ThemeResource` | yes |
| surfaces | bordered-flat ("weak signal") | INFERRED | `CardBackgroundFillColorDefault` card with 1 px `CardStrokeColorDefault`, `OverlayCornerRadius`, Mica canvas | yes (weakly stated) |
| radius | unknown | UNKNOWN | `OverlayCornerRadius` (8) and `ControlCornerRadius` (4) theme resources | **no** — resource-based radius not read |
| spacing | 4 | INFERRED | 4 epx grid: 16/12/8/4 paddings and spacings | yes |
| typography | unknown | UNKNOWN | WinUI type ramp via `TitleTextBlockStyle` / `BodyTextBlockStyle` / `CaptionTextBlockStyle` (Segoe UI Variable) | **no** — style-based typography not read |
| components | winui3, community-toolkit | KNOWN | + `CommandBar`, `DataGrid`, `InfoBar`, `MenuFlyout` on the page; **existing `KeyboardAccelerator`s (12) and `AccessKey`s (5)** not surfaced | partial — the one signal this task needed (the page already has a command bar and accelerators) is absent |

The Phase 3 `ListView`→`isTV` false positive is gone: `platforms = ["desktop"]` only. Fixed since Phase 3.

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| Field | Value | Verdict |
|---|---|---|
| scope | UI_INTERACTION, in_scope | right |
| mode | create ("default (no mode cue)") | **wrong** — "add … to the existing page" is an extension of an existing screen; `intent.existing=true` was detected but no mode reflects it |
| platform / input | desktop (from "keyboard shortcuts"); keyboard (stated), pointer | right |
| product / stack | erp; winui | right |
| screen / screen_subtype | [] | missing (stock adjustments = table working screen; "page" + product erp) |
| components | navigation | **wrong** — should be toolbar/command-bar + keyboard-shortcuts; "navigation" comes from the negative clause |
| primary_jobs | "create navigation" | wrong (same source) |
| density | high | right (erp) |
| constraints | preserve_existing_system, **preserve_navigation** | navigation right; **theme not preserved**: "without changing its navigation or theme" yielded no `preserve_color`, unlike p4-01 where "theme" → color worked ("its theme" phrasing?) |
| negative_constraints | [] | wrong — expected navigation-change (+ theme) |
| change_budget | moderate | acceptable |
| project_context | as table | radius/typography unknown propagated |

## Guidance verdict (`03-guidance.md/json`, status PARTIAL)
Bundle 6 = core 3 + guardrails 3. Metrics: concepts 3/3, tokens≈807, coverage/1k 3.72, purity 0.83, redundancy 0.27; concerns covered 0.83, **uncovered required: component**.

| Record | Role | Verdict | Why |
|---|---|---|---|
| `cta-toolbar-commands` | core | relevant — exact | "labelled buttons, overflow into a menu, disabled not hidden when no selection, accelerators in tooltips, count of selected items visible near the commands"; winui note "CommandBar + AppBarButton + KeyboardAccelerator; IsEnabled bound to selection". Drove the overflow (`SecondaryCommands`), the selection caption, and confirmed the existing enablement. |
| `imagery-none` | core | off-target | Nothing to remove; selected as a "pattern with lexical evidence" (0.1). |
| `layout-table-first` | core | partial | Describes what the page already is; harmless. |
| `desktop-keyboard-first` | guardrail | relevant — drove the work | "Document shortcuts in menus and tooltips; F2 edits, Ctrl+F finds, F6 cycles panes; every dialog has a default and cancel button; access keys shown on Alt" → F6/Shift+F6 region cycling, accelerator text in the context menu, F1 reference with a default Close button. |
| `a11y-hover-not-required` | guardrail | partial | Tooltips are hover-only in WinUI; the F1 list is the non-hover path for the documentation. |
| `desktop-state-persistence` | guardrail | relevant | "never lose selection on refresh; persist layout" → the `Created by` toggle is stored in `ApplicationData.LocalSettings`; selection-by-key on refresh was already there. |

Relevant 3, partial 2, off-target 1. Omitted-as-contamination list was right: `comp-command-palette`/`nav-command-palette` (a palette is not a command bar), `nav-menu-bar-desktop` (top search hit 0.704, but navigation is preserved), `comp-data-entry-grid`.

Missing guidance:
- **Shortcut reference / help surface** (F1 or Ctrl+/ list, `KeyboardAcceleratorTextOverride` for menu items that must show but not re-register an accelerator, accelerator conflicts with the shell's own keys) — absent from the base. **Knowledge gap.**
- **Check whether the requested component already exists** before "creating" it — neither inspection nor requirements can say "this page already has a CommandBar with 6 accelerators"; the skill classified the task as create. **Knowledge gap / context-detection** (a per-view component inventory).
- The uncovered `component` concern is honest: there is no record for a WinUI command bar component beyond the cta pattern's one-line winui note.
- `a11y-focus-visible` / focus in flyouts and dialogs not in the bundle (search rank 12+); WinUI system focus visuals cover it, verified in the twin.

## Direction verdict (`04-direction.md/json`, validation OK)
Change budget moderate · preserved [navigation, surface, color] · changed [].

| Slot | Choice | Status | Justified? |
|---|---|---|---|
| navigation | nav-left-rail (existing NavigationView) | preserved | yes |
| layout | layout-three-pane | new | **no** — the page is a single table-first screen; master-detail (0.609) and table-first (0.456) were alternatives; nothing in the task asks for panes |
| density | density-high | new | fits (matches the page's 36 epx rows) |
| surface | bordered-flat (existing) | preserved | yes |
| cards | card-bordered | new | n/a (no cards; the table card is the existing surface) |
| typography | typography-system-native | new | fits — it *is* the existing WinUI type ramp, but the inspector could not see that so it was proposed as new rather than preserved |
| color | light-first dual theme (existing) | preserved | yes — preserved from repository evidence even though the requirements dropped "theme" |
| motion | functional-minimal | new | fits |
| focus | focus-ring-standard | new | fits (system focus visuals) |
| cta | cta-toolbar-commands | new | fits — this is the task |
| imagery | imagery-none | new | fits, trivial |
| icon | icon-platform-native | new | fits (Segoe Fluent Icons) |
| metadata | metadata-rich | new | fits ("columns with user-controlled visibility" → the Created-by toggle) |

Unjustified new choices: layout (1). Preservation: 3 preserved / 10 new / 0 changed; typography should have been "preserved" (context-detection miss), not "new".

## Implementation (static review of the XAML; twin mirrors it)
Files changed (copies in `before/`):
- `Views/StockAdjustmentsPage.xaml`
  - `CommandBar` (named `Commands`, `OverflowButtonVisibility=Auto`, automation name) gains `CommandBar.Content` = caption bound to `ViewModel.SelectionLabel` ("Selected: ADJ-10421" / "No adjustment selected", `LiveSetting=Polite`) and `SecondaryCommands`: `AppBarToggleButton` "Show 'Created by' column" (AccessKey C), "Clear filters" (Ctrl+Shift+L, AccessKey L), separator, "Keyboard shortcuts" (F1, AccessKey K). Primary commands unchanged (Ctrl+N / Ctrl+Shift+A / Ctrl+Shift+R / F5, access keys N A J R).
  - Search `TextBox`: Escape accelerator scoped to the box (`ScopeOwner`) clears the search text only when there is text, otherwise Escape bubbles.
  - Context menu: `KeyboardAcceleratorTextOverride="Ctrl+Shift+A|R"` on Approve/Reject so the flyout documents the shortcuts without registering them twice (F2 on Edit was already there).
  - Root grid: `F6` / `Shift+F6` accelerators cycle Commands → Filters → Grid.
  - `CreatedByColumn` named so the toggle can show it; `Filters` panel named.
  - `ContentDialog` "Keyboard shortcuts" (`DefaultButton=Close`) listing `ViewModel.Shortcuts` as key-cap + description rows with theme brushes.
- `Views/StockAdjustmentsPage.xaml.cs` — restore/persist the column toggle in `ApplicationData.Current.LocalSettings`; `ShowShortcuts_Click` sets `XamlRoot` and awaits the dialog (focus returns to the invoker); `ClearSearch_Invoked`; `FocusRegion` uses `FocusManager.GetFocusedElement` + visual-tree ancestry to find the current region and `FindFirstFocusableElement` for non-tab-stop regions.
- `ViewModels/StockAdjustmentsViewModel.cs` — `SelectionLabel` (raised with `Selected`), `Shortcuts` list (13 entries, single source for the F1 dialog), `ShortcutInfo` record.
Navigation (`MainWindow.xaml`), theme (`App.xaml`), the DataGrid columns/density and the filter row are untouched.

Not verified (toolchain): XAML compile, `ScopeOwner="{x:Bind SearchBox}"` on a `KeyboardAccelerator`, `FindFirstFocusableElement` on the `CommandBar`, KeyTip rendering, Narrator, Dark/High Contrast.

## First-render defects (`render/first-after*.png`, `05-interaction-first.json`)
1. **implementation-bug (twin)** — with the "Created by" column shown, the twin's `table-layout: fixed` let Description collapse to ~60 px ("Euro pa…"); the XAML has `MinWidth=160` on that column and would scroll instead. Twin fixed with a `min-width` equal to the XAML budget (1172 px).
2. **platform (twin fidelity)** — the overflow "…" button showed an Alt key tip "M" that WinUI's CommandBar does not provide for its overflow button; removed.
No interaction or accessibility defects: every check passed on the first run (13 Tab stops all with the system focus visual; every command / row action / menu item carries its accelerator in tooltip or menu text; F1 opens the reference with all 12 required shortcuts, Esc closes, focus returns to the row; F6 cycles New adjustment → Search → active row, Shift+F6 back; overflow menu opens on Enter, arrows/Home/End move, Esc returns to the "…" button; column toggle persists across reload; Esc clears only the search, Ctrl+Shift+L clears all; Shift+F10 opens the row context menu with 3 accelerator texts, Esc returns to the row; selection caption and Approve/Reject enablement follow the selection; grid stays one Tab stop with arrow access to row actions; no horizontal overflow at rest; transitions 0 s under reduced motion).

## Final defects (`render/final-after*.png`, `05-interaction.json`)
- 0 visual / interaction / accessibility / implementation-bug in the twin.
- **Documented trade-off**: with the opt-in "Created by" column at a 1440-wide window the grid is 1172 px in 1086 px → 86 px horizontal scroll, Actions column reachable by scrolling or keyboard (the grid scrolls the focused cell into view). Off by default and persisted per user; matches the Phase 3 column-budget decision.
- Access-key tips shown for 4 primary commands only (WinUI shows tips for secondary commands once the overflow is open — not simulated).
- XAML unverified by compilation (tooling limit, same as before the task).

## Iterations
2 twin renders (first → 2 twin-fidelity fixes → final). XAML: 1 pass + 1 code-behind correction (F6 focus target) found during static review.

## Interaction test summary (`05-interaction.json`, final)
| Criterion | Result |
|---|---|
| Shortcuts documented | 4/4 command-bar buttons show the accelerator in the tooltip; 6/6 menu items (3 overflow, 3 context) show it as text; 24/24 row actions show it in the tooltip; F1 reference lists 13 entries incl. Ctrl+N, Ctrl+Shift+A/R, F2, F5, Ctrl+F, Esc, Ctrl+Shift+L, F6, Shift+F10, Alt, F1 |
| Accelerator keys reachable | F1 → dialog (focus on Close, Esc closes, focus back to row); F6 ×3 = cmdNew → search → row, Shift+F6 → search; Ctrl+F → search; Esc in search clears search only (Location kept); Ctrl+Shift+L clears all (8 rows, Clear disabled); Shift+F10 → context menu first item; overflow via Tab + Enter, ↓/End, Esc |
| Focus visible | 13/13 Tab stops; menu items, dialog Close, row, row action all with the 2 px system visual |
| Access keys | accesskey N A J R S C L K present; 4 key tips visible while Alt is held |
| Selection near commands | "Selected: ADJ-10421" on an actionable row with Approve enabled; on a Posted row Approve disabled, caption updated |
| Column toggle | shown after toggle, persisted after reload (LocalSettings twin = localStorage) |
| Grid regression | 1 Tab stop; → from the row focuses "Edit ADJ-10421" with a visible ring |
| Overflow / motion | 1086/1086 at rest; transition 0 s under `prefers-reduced-motion` |

## Preservation verdict
`NavigationView` shell untouched; theme untouched (all new visuals use `ThemeResource`/`StaticResource` brushes and the type ramp; the dialog key-caps use `ControlFillColorSecondaryBrush` / `ControlStrokeColorDefaultBrush` / `ControlCornerRadius`); typography via existing text styles; component language WinUI-native (`CommandBar.SecondaryCommands`, `AppBarToggleButton`, `ContentDialog`, `KeyboardAccelerator`). Structural changes: none to the page layout (a caption in the command bar, an overflow menu, a hidden dialog). Unjustified structural changes: 0.

## Regressions to propose
- query: "add keyboard shortcuts and a command bar to the existing stock adjustments page without changing its navigation or theme" → expect mode ≠ create (extend/refactor of an existing screen); `components` includes toolbar/command-bar and keyboard-shortcuts, not navigation; `constraints.preserve_color` true and `negative_constraints` = [navigation-change] ("its theme" must parse like "theme").
- query: "document keyboard shortcuts in a desktop app" (winui) → expect a record about a shortcut reference (F1 / Ctrl+/), `KeyboardAcceleratorTextOverride` for mirrored menu items, and avoiding conflicts with shell accelerators.
- inspector: a Views folder whose page already contains `CommandBar` + `KeyboardAccelerator` → expect a per-view component inventory (or at least `focus_handling`/`keyboard` counts) so a "create command bar" request can be flagged as already present.
- inspector: XAML using `TitleTextBlockStyle`/`BodyTextBlockStyle` and `OverlayCornerRadius`/`ControlCornerRadius` → expect typography = platform type ramp (KNOWN) and radius from theme resources, not UNKNOWN.
- direction: winui table page + "command bar" → expect layout slot table-first, not three-pane.

## Tags
`mode-miss` (create for an existing page), `requirements-miss` (components/primary_jobs = navigation; theme not preserved in the contract; screen empty), `context-detection-miss` (existing CommandBar/accelerators not surfaced; radius and typography UNKNOWN; menu-bar false candidate), `knowledge-gap` (shortcut reference / menu accelerator text; "check if it already exists"), `direction-mismatch` (layout-three-pane; typography 'new' instead of preserved), `render-defect-fixed` (2 twin-fidelity), `render-defect-remaining` (documented horizontal scroll with the opt-in column), `tooling-limit` (XamlCompiler exit 1 before and after; no Narrator/KeyTip verification), `skill-helped` (cta-toolbar-commands and desktop-keyboard-first specified the overflow, selection caption, F6, documented accelerators, dialog default button; desktop-state-persistence → persisted toggle; navigation/color preserved), `preservation-ok`.

## Provenance note
Nothing under `design-engineering/` was written by this task. Files there (`data/lexicon.json`, `data/rules.jsonl`, `data/patterns.jsonl`, `data/components.jsonl`, `data/antipatterns.jsonl`, `docs/USAGE.md`, `docs/MAINTENANCE.md`, `evals/development/*.json`) show mtimes 12:16–12:23 from another process; the skill commands for this task ran at 12:20–12:21 (inspect) and immediately after (requirements/guidance/direction/search), so the recorded outputs reflect the data as it was at that moment and may not reproduce byte-for-byte later.
