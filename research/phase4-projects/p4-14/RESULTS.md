# p4-14 — results

## Task
"add a settings screen (sync frequency, units, high-contrast mode) to the field inspection app in its existing style"

## Project / stack / platform
`p3-mobile-flutter-field/project` — Flutter 3.22 / Material 3, Riverpod, go_router; Android + iOS phone. **Existing project, new screen** (`/settings`).

Render mode: **html-twin + static review** (no Flutter SDK). The Phase 3 twin (already extended by p4-13; that state is `before/render/twin.html`) gained a `screen=settings` section, a `state=hc` high-contrast variant and a `state=freq` picker sheet; shot at 390×844 with Playwright 1.63.0.

## Design-context table
Same `01-inspect.json` as p4-13 (same project, inspected before either task's changes):
| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | go_router stack, per-screen 72 dp `AppBar` with back; secondary actions in modal bottom sheets (the natural entry point for a settings screen is the checklist's "More actions" sheet) | partial |
| theme | dual-theme, default light | KNOWN | light + dark `ThemeData`, `ThemeMode.system` | yes |
| surfaces | elevated | INFERRED | flat, outlined tiles, `elevation: 0` | no |
| radius | unknown | UNKNOWN | 8 dp | no |
| spacing | 4 | INFERRED | 4/8/12/16/24/32, controls 56, gap 12 | yes |
| typography | unknown | UNKNOWN | system font, explicit scale 36…14, tabular figures | partial |
| components | go_router, riverpod | KNOWN | `lib/widgets/` + 56 dp Filled/Outlined buttons, 56 dp `ListTile` sheets, `StatusBadge`, `OfflineBanner`, `BottomActionBar` | no |
Plus the same TV false positive (`AnimatedPadding` ⇒ DPAD) and erp/iot product hints.

## Requirements verdict (`02-requirements.json`, CONFIDENT)
| field | value | verdict |
|---|---|---|
| scope | UI_ACCESSIBILITY ("contrast") | acceptable; the task is a create with one accessibility feature |
| mode | create (default) | right |
| platform / input | mobile, tv / remote, touch | tv + remote wrong (inspector) |
| product | erp, iot | wrong |
| screen / components | settings / form, settings | right |
| environment | large-display, shared-device | wrong (tv); the README's gloves/outdoor/offline not used |
| intent | existing true, facet accessibility, preserve [] | "in its existing style" should populate `preserve` (theme, typography, components) |
| change_budget | moderate | right |
| missing | brand | right |
| accessibility | screen_reader, focus, touch_targets, reduced_motion, contrast | right |

## Guidance verdict (`03-guidance.md/json`; PARTIAL; bundle 8 = core 3 + guardrails 5)
Metrics: concepts 9/11 (uncovered `state.loading_empty_error`, `table.tabular_figures`), ≈1120 tokens, coverage/1k 8.04, contaminated [], purity 0.8; concerns 0.88 (uncovered performance).
| record | verdict | note |
|---|---|---|
| `comp-settings-screen` (core) | relevant, high value | "grouped rows, current values visible, toggles with immediate effect, pickers for enums, grouped lists on mobile, save behaviour explicit" — this is the screen |
| `comp-form` (core) | partial | labels/sections apply; validation/submit do not (no Save button) |
| `layout-form-stack` (core) | partial | one column + section headings apply |
| `a11y-tv-focus-always` | off-target | tv |
| `mobile-density-touch` | partial | ≥48 dp rows |
| `tv-dpad-axes` | off-target | tv |
| `tv-typography-distance` | off-target | tv |
| `tv-safe-area` | off-target | tv |
Relevant 1 · partial 3 · off-target 4.

Missing guidance:
- `impl-reuse-before-new` (rank 10 in search, 0.402) and `color-semantic-tokens` (rank 8, 0.417) — both directly "in its existing style"; not selected (bundle-selection).
- `states-offline-and-sync` is rank 1 in search (0.533) — relevant to the sync-frequency group and the sync-queue row; not in the bundle (bundle-selection).
- High-contrast mode as an in-app theme variant (what changes: stroke widths, secondary text, outline roles; relation to the OS "increase contrast" setting / `MaterialApp.highContrastTheme`) — **knowledge gap**: targeted search returns `a11y-nontext-contrast`, `a11y-contrast-text`, `desktop-fluent-materials`; nothing describes building the mode.
- Units / measurement preference and sync-frequency semantics — covered generically by `comp-settings-screen` ("pickers for enums"); acceptable.
- `state.loading_empty_error` reported uncovered — not needed for a settings screen; the concern derivation does not know that settings has no async content.

## Direction verdict (`04-direction.md/json`)
Budget moderate · preserved navigation, surface, color · changed [] · validation VIOLATIONS (poster cards).
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | preserve top-bar | preserved | yes |
| layout | form stack | new | fine |
| density | medium | new | default; project is 56 dp |
| surface | preserve elevated (INFERRED) | preserved | value wrong (flat) |
| cards | poster-landscape | new | unjustified (flagged) |
| typography | **rounded friendly sans** (Nunito…) | new | unjustified: the project uses the system font and the inspector said typography UNKNOWN; "in its existing style" should preserve it. A knock-on of product=iot |
| color | preserve dual theme | preserved | yes |
| motion | focus-scale (TV) | new | unjustified (tv) |
| focus | scale + glow (TV) | new | unjustified (tv) |
| cta | single primary | new | fine (there is none on this screen) |
| icon | platform set | new | fine (Material icons) |
| imagery / metadata | none / moderate | new | fine |
Unjustified changed/new slots: cards, typography, motion, focus (all traceable to tv / erp-iot / UNKNOWN typography). Direction was cross-checked and the repo won.

## Implementation summary
- New `project/lib/state/settings.dart` — `SyncFrequency` (4 values with label + detail), `Units` (metric/imperial), `AppSettings`, `SettingsNotifier` (Riverpod `Notifier`, immediate effect, `_persist` hook; no new dependency).
- New `project/lib/screens/settings_screen.dart` — same shell as the other screens (72 dp `AppBar` + back, `OfflineBanner`, `ListView` at 16 dp): "Changes apply immediately." line; groups SYNC (Sync frequency → 4-option bottom sheet with radio semantics and 8 dp gaps; Sync queue → existing `showSyncQueueSheet`, value = pending count + last synced), UNITS (two 56 dp toggle buttons with 12 dp gap, the severity-grid idiom), DISPLAY (`SwitchListTile.adaptive` High-contrast mode, `Text size` info row). Flat outlined `_Tile` = the checklist row container. Every row shows its current value as subtitle.
- `project/lib/theme/app_theme.dart` — `AppTheme.light({highContrast})` / `dark({highContrast})`: scheme split into `_scheme()` + `_theme()`; high contrast maps `onSurfaceVariant → onSurface`, `outlineVariant → outline`, outline → near-black/near-white, stroke 2 → 3 dp (outlined buttons, inputs, dividers, switch track), focus stroke 3 → 4. Status colours untouched (already ≥7:1).
- `project/lib/main.dart` — `/settings` route; `FieldInspectApp` is a `ConsumerWidget` that watches `settingsProvider.highContrast` and also sets `highContrastTheme` / `highContrastDarkTheme` so the OS setting picks the same variant.
- `project/lib/screens/checklist_screen.dart` — "Settings" tile added to the existing "More actions" sheet (`context.push('/settings')`).
- `project/README.md` — screen documented. Before copies of all touched Dart files in `before/project/`.
- Twin: settings section, `.hc` variable overrides, frequency sheet; `render/shoot.js`, `render/interact.js`.

## First-render defects (`05-interaction-first.json`: 15/17)
1. **existing-system-mismatch** (also interaction) — units built as a Material `SegmentedButton`: adjacent segments have 0 px between them; the project's own convention (severity chooser, Phase 3) is separate 56 dp toggle buttons with a 12 dp gap for gloves. Failed `settings_targets` / `settings_targets_hc`.

## Final defects (`05-interaction.json`: 17/17)
- None measured. Unverified: Dart not compiled (`SwitchListTile.adaptive` `minTileHeight`, `WidgetStatePropertyAll` require Flutter ≥3.22 as pinned); dark + high-contrast combination only reasoned about; the twin's "3 pending" value is static.

## Iterations
2 renders. Fix: `SegmentedButton` → `Row` of Filled/Outlined buttons (`FieldSizes.controlGap`), twin `.seg` → gapped buttons.

## Interaction test summary (390×844)
- Grouped rows: 3 `role=group` blocks labelled by headings SYNC / UNITS / DISPLAY, every row with a non-empty visible value.
- Immediate effect: toggling the switch flips `aria-checked`, adds `.hc`, changes tile border colour (#C4C7CC → #5C636D) and secondary text (#3A4048 → #1B1F24, 16.9:1 on white), updates the row value text; toggling back restores. Units toggle updates value text and `aria-checked`; frequency sheet (4 radio rows ≥48 px, one checked, background `inert`) updates the row value and closes.
- Targets: settings 6 (Back 56, rows 356×72, toggles 163×56) and sheet 4 — all ≥48 px, ≥8 px apart, in both modes.
- Contrast ≥7:1 on all sampled text in standard and high-contrast modes; offline strip present on the screen (`role=status`); Tab shows a focus ring; "Changes apply immediately." stated.

## Preservation verdict
Navigation: new route on the existing go_router stack, entry via the existing sheet, same app bar. Theme: all through `Theme.of` / `FieldSizes`; high contrast is a variant of the same `ColorScheme`s, not a new palette. Typography: same `TextTheme` roles. Components: outlined tile container, 56 dp `ListTile` sheets, Filled/Outlined toggle idiom, `OfflineBanner`, `showSyncQueueSheet` reused. Unjustified structural change: 0 (the `SegmentedButton` was caught before final). **preservation-ok**.

## Regressions to propose
- query: "add a settings screen … in its existing style" (mobile project) — expect `comp-settings-screen` core (kept), plus `impl-reuse-before-new` / `color-semantic-tokens` as guardrails; `intent.preserve` non-empty; typography slot = preserve/system font when the repo declares no family.
- query: "high-contrast mode toggle for a mobile app" — expect a record on building an in-app high-contrast variant (stroke, outline, secondary-text roles, OS setting parity) once added.
- concern derivation: settings screen should not require `state.loading_empty_error`.
- same inspector regressions as p4-13 (AnimatedPadding, elevation: 0, radius).

## Skill misses by layer
- requirements: platform tv / input remote / env (inspector false positive); product erp/iot; `preserve` empty for "in its existing style".
- bundle-selection: `states-offline-and-sync` (rank 1), `impl-reuse-before-new`, `color-semantic-tokens` not selected; five TV records selected.
- concerns: `state.loading_empty_error` required for a settings screen.
- candidate-retrieval / knowledge gap: in-app high-contrast mode.
- direction: typography rounded-friendly as "new" despite an existing system font; motion/focus TV; cards poster.
- project-adaptation: the direction's `density-medium` (40–48 dp) would have under-sized the controls; the repo's 56 dp convention was used instead.

## Tags
`context-detection-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `tooling-limit`, `skill-helped` (`comp-settings-screen` dictated the structure: grouped rows, visible values, immediate toggles, explicit save behaviour), `preservation-ok`.
