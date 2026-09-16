# p4-13 — results

## Task
"refactor the defect report form so it stays usable with the keyboard open and photos can be retaken, keeping the app's existing theme and navigation"

## Project / stack / platform
`p3-mobile-flutter-field/project` — Flutter 3.22 / Material 3, Riverpod, go_router; Android + iOS phone (outdoor, gloves, offline-first). **Existing UI** (refactor of `lib/screens/defect_report_screen.dart`).

Render mode: **html-twin + static review**. No Flutter SDK; the Dart was patched and reviewed statically (bracket balance checked, no compile). The Phase 3 twin `p3-mobile-flutter-field/render/twin.html` was extended in place (before copy in `before/render/twin.html`) and shot at 390×844 with Playwright 1.63.0 (`render/shoot.js`, `render/interact.js`, NODE_PATH pointing at the Phase 3 `node_modules`).

## Design-context table (`01-inspect.json` → `design_context`)
| field | detected | status | actual (from `app_theme.dart`, screens, widgets) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN (`AppBar` ×2) | go_router **stack**: checklist → defect form, each screen a 72 dp `AppBar` with back; secondary actions in modal bottom sheets | partial (bar detected, model not) |
| theme | dual-theme, default light | KNOWN | `AppTheme.light()` / `dark()`, `ThemeMode.system`, light is the working theme | yes |
| surfaces | elevated | INFERRED ("shadow 1, border 0") | **flat**: `elevation: 0` on the app bar, outlined tiles (`BorderSide(outlineVariant)`), no shadows. The "shadow" hit is the literal `elevation: 0` / `shadow:` scheme slot; the 10 `BorderSide` uses were not counted as borders | no |
| radius | unknown | UNKNOWN | `FieldSizes.radius = 8` everywhere | no |
| spacing | 4 | INFERRED (most used 12) | `FieldSizes.space1..8` = 4/8/12/16/24/32, controls 56, gap 12 | yes |
| typography | unknown; weights 400/600/700, type scale yes, tabular no | UNKNOWN | system font (no family), explicit `TextTheme` 36/28/24/22/18/16/14, `FontFeature.tabularFigures()` on the count | partial (scale right, tabular missed, "unknown" should be "platform system font") |
| components | go_router, riverpod | KNOWN | those are libraries; the component language is `lib/widgets/` (BottomActionBar, OfflineBanner, StatusBadge, state views, SyncQueueSheet) + Filled/Outlined buttons at 56 dp, 56 dp `ListTile` sheets | no |

Other inspector output: `platforms: ["mobile","tv"]` and `focus_handling: "DPAD/remote/TV-focus handling in 1 files"` — **false positive**: `DPAD_RE` is case-insensitive and `AnimatedPadding` (bottom_action_bar.dart) contains "dPad". This single hit turned the project into a TV project for every later step. `product_hints: ["erp","iot"]` from README ("utility"). `routing: []`, `tests: []` despite go_router + `test/`.

## Requirements verdict (`02-requirements.json`, status CONFIDENT, exit 0)
| field | value | verdict |
|---|---|---|
| scope | UI_INTERACTION, in_scope | right |
| mode | refactor ("explicit: refactor"; structural words refactor, navigation) | right |
| platform | mobile, **tv** (KNOWN) | wrong — TV comes from the AnimatedPadding false positive, ledgered KNOWN |
| input | keyboard (request), **remote** (project), touch | keyboard right (it means the IME, not a hardware keyboard — treated as keyboard navigation later); remote wrong |
| product | erp, iot | wrong (field-service / utility inspection) |
| screen / components | form / form, navigation | screen right; "navigation" as a component to build is wrong — the sentence says keep it |
| environment | large-display, shared-device | wrong (from tv); gloves/outdoor/offline from the README not picked up |
| jobs / primary_jobs | [] / "refactor form" | thin |
| risk | low | arguable (safety-hazard reporting) |
| intent.preserve | [] | **wrong** — "keeping the app's existing theme and navigation" names two things to preserve; `no_change: []`, `preserve: []` |
| change_budget | moderate | right |
| constraints | preserve_existing_system true | right |
| project_context | copied from the inspector (surfaces elevated, radius unknown) | inherits the inspector errors |

## Guidance verdict (`03-guidance.md/json`; status PARTIAL; bundle 8 = core 3 + guardrails 5)
Metrics: concepts 8/10 required covered (uncovered `interaction.keyboard_navigation`, `table.tabular_figures`), ≈1175 tokens, coverage/1k 6.81, contaminated [], purity 0.9; concerns 0.89 (uncovered performance).
| record | verdict | note |
|---|---|---|
| `comp-form` (core) | relevant | "on-screen keyboard (IME) aware layout, unsaved-changes guard" — the annotation covers the task even though the record body is generic |
| `nav-tv-top-tabs` (core) | off-target | TV tabs for a phone form; and the task says keep navigation |
| `layout-form-stack` (core) | relevant | already how the form is built |
| `a11y-tv-focus-always` | off-target | TV |
| `mobile-density-touch` | partial | ≥48 dp rows applies; tables/filters do not |
| `tv-dpad-axes` | off-target | TV |
| `tv-typography-distance` | off-target | TV |
| `tv-safe-area` | off-target | TV |
Relevant 2 · partial 1 · off-target 5. Every off-target record traces to platform=tv.

Missing guidance:
- `mobile-keyboard-ime` — **ranking miss at bundle selection**: it is rank 1 in `search -k 12` (0.542, "never let the keyboard cover the focused field or the submit button") and scores 0.629 on a keyboard-focused query, yet the bundle chose `nav-tv-top-tabs` (0.485) and `layout-form-stack` (0.414) as core. The concept `interaction.keyboard_navigation` was declared uncovered even though this record is the IME rule; the concept name (keyboard *navigation*) does not match the IME concept.
- `mobile-safe-areas` (0.518 on the keyboard query) — ranking miss.
- `impl-safe-modification` (rank 5, 0.423, "never rename props/ids/routes… as part of a visual change") — exactly the "keep theme and navigation" constraint; not selected.
- Photo capture / retake / replace-in-place — **knowledge gap**: searches return `imagery-none`, `imagery-thumbnails`, `comp-media-card`; nothing about camera fields, thumbnails as targets, retake vs remove.
- Keyboard dismissal affordance (tap outside, drag, explicit "Done/Hide keyboard" when Return inserts a newline) — knowledge gap (not in `mobile-keyboard-ime` text).

## Direction verdict (`04-direction.md/json`)
Change budget moderate · preserved navigation, surface, color · changed [] · validation **VIOLATIONS**: "non-media product: poster (media) card geometry selected".
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | preserve top-bar (KNOWN) | preserved | yes (right outcome; the detected model is only partly right) |
| layout | form stack | new | fine (matches existing) |
| density | medium | new | acceptable default; the 56 dp field convention is stricter |
| surface | preserve **elevated** (INFERRED) | preserved | preserving is right, the value is wrong (flat) — inherited from inspector |
| cards | poster-landscape 16:9 | new | unjustified; now flagged by validation (improvement over Phase 3, where the same choice passed) |
| typography | neutral sans, "keep system font if used" | new | fine |
| color | preserve light-first dual theme | preserved | yes |
| motion | functional minimal | new | fine |
| focus | scale + glow (TV) | new | unjustified (tv) |
| cta | sticky bar with IME clause | new | right — the record text ("bar must not obscure a focused field, scroll it into view") is the task |
| imagery / icon / metadata | none / filled / inline badges | new | fine |
The direction was not needed for a refactor; used only as a cross-check. Slots contradicting the repo (surface, focus, cards) were ignored.

## Implementation summary
Files changed (before copies in `before/`):
- `project/lib/screens/defect_report_screen.dart`
  - Photos: `_PhotoThumb` is now one 104 dp `InkWell` target (index chip on inverse surface, no overlaid 48 dp remove button) that opens a bottom sheet — same idiom as the checklist "More actions" sheet — with **Retake photo** (camera, replaces in place so "Photo 2" stays "Photo 2"), **Replace from gallery**, **Remove photo**; 56 dp `ListTile`s with 8 dp gaps; `_pick()` wraps `image_picker` errors in a snackbar; focus is dropped before opening the camera.
  - Keyboard: `GestureDetector(translucent)` around the form unfocuses on tap outside (drag-to-dismiss already existed); a **"Hide keyboard"** `TextButton.icon` appears in the Notes label row while Notes has focus (Return inserts newlines, so there is no Done key); `scrollPadding`/`viewInsets` handling and the IME-riding `BottomActionBar` kept.
  - Routes, `PopScope` discard guard, validation, semantics labels, provider calls: unchanged.
- `p3-mobile-flutter-field/render/twin.html` — thumbnails as buttons, photo sheet (`?state=photosheet`), hide-keyboard control, tap-outside behaviour.
- New: `render/shoot.js`, `render/interact.js` (task-specific), `05-interaction-first.json`, `05-interaction.json`.

## First-render defects (render/first-*.png, `05-interaction-first.json`: 12/14)
1. **interaction** — photo sheet: three 56 dp full-width rows with 0 px between them (glove rule ≥8 px; the checklist rows were fixed for the same reason in Phase 3). Dart and twin.
2. **implementation-bug** — "Hide keyboard" placed under the helper text sat below the action bar with the 300 px IME open (the field is scrolled into view, not what follows it); `hide_keyboard_visible_when_open` failed.

## Final defects (render/final-*.png, `05-interaction.json`: 14/14)
- None measured. Unverified: Dart not compiled; real IME/`scrollPadding` behaviour, `ListenableBuilder` on a `FocusNode`, TalkBack order of the thumbnail sheet.

## Iterations
2 renders. Fix: 8 dp `SizedBox` between sheet tiles; "Hide keyboard" moved into the Notes label row (`Row(Expanded(_SectionLabel), ListenableBuilder(...))`), twin `.labelrow`.

## Interaction test summary (390×844, 300 px IME)
- Save 476–532 px, Cancel reachable, action bar bottom = keyboard top (544), Notes 231–351 px visible above the bar and focused; form still scrolls to the photo buttons with the IME open.
- Targets: form 8, form+keyboard 6, photo sheet 3 — all ≥48×48 (thumbnails 104×104, sheet rows 390×56), spacing ≥8 px.
- Thumbnail is a single labelled button with `aria-describedby` hint; no nested remove button; sheet is `aria-modal` with background `inert`; Retake/Replace/Remove rows ≥48 px in the lower half; scrim dismisses.
- "Hide keyboard" hidden when closed, visible (56 px) above the bar when open, closes the IME and returns the bar to the safe area; tap on empty form space closes it.
- Focus visible on the textarea (3 px primary border).

## Preservation verdict
Navigation (route, back with discard guard), theme (all colours via `Theme.of`, `FieldSizes`), typography, component language (Filled/Outlined buttons, 56 dp ListTile sheets, BottomActionBar) kept. Structural changes: thumbnail overlay button → sheet (justified by the glove spacing rule and the retake requirement); "Hide keyboard" control (justified by `textInputAction.newline`). Unjustified structural changes: 0. **preservation-ok**.

## Regressions to propose
- query: "form usable with the keyboard open on a phone (Flutter)" — expect `mobile-keyboard-ime` and `mobile-safe-areas` in the bundle core/guardrails; no `nav-tv-*` records when platform is mobile-only.
- query: "keep the app's existing theme and navigation" — expect `intent.preserve` ⊇ [theme, navigation], `components` not to include "navigation", `impl-safe-modification` selected.
- inspector: a Flutter project whose only "dpad" match is `AnimatedPadding` — expect no TV platform, no DPAD focus finding (word-boundary the `dpad` alternative).
- inspector: `elevation: 0` + ≥10 `BorderSide`/`Border.all` uses — expect surfaces = flat/bordered, not elevated.
- query: "photos can be retaken in a defect report form" — expect a photo/camera-field record (thumbnail as target, retake replaces in place, remove confirmed) once added.

## Skill misses by layer
- requirements: platform=tv / input=remote / env large-display+shared-device (root cause: inspector `DPAD_RE` matches `AnimatedPadding`).
- requirements: `intent.preserve` empty for "keeping the app's existing theme and navigation"; "navigation" listed as a component to build.
- requirements: product erp/iot for a utility field-inspection app.
- bundle-selection: `mobile-keyboard-ime` (rank 1 in search) not in the bundle; `impl-safe-modification` not selected.
- expected-concepts: `interaction.keyboard_navigation` derived from "keyboard" — the request means the IME, so the uncovered concept is the wrong concept.
- candidate-retrieval / knowledge gap: photo capture & retake; keyboard-dismiss affordance.
- direction: cards poster-landscape (now caught by validation), focus scale-glow, surface elevated (context-detection).
- project-adaptation: none needed beyond ignoring the TV items.

## Tags
`context-detection-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `tooling-limit`, `skill-helped` (comp-form's IME/unsaved-guard annotation and cta-sticky-bar's WCAG 2.4.11 clause matched the task; `search` surfaced `mobile-keyboard-ime`), `preservation-ok`.
