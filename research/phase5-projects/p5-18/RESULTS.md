# p5-18 — results

## Task
"Photos attached to a defect report are tiny thumbnails you can't check in the field." (run verbatim)

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8`. Nothing under `design-engineering/` was touched.

## Project / stack / platform
`research/phase3-projects/p3-mobile-flutter-field/project` — Flutter 3.22+ / Material 3, Riverpod, go_router. Utility field-inspection app (outdoor sunlight, gloves, offline-first). Hand-tuned light + dark `ColorScheme`, `StatusColors` ThemeExtension, `FieldSizes` tokens (56 dp controls, 12 dp gaps, radius 8), in-app high-contrast switch. Platform: mobile.

## Existing UI or new screen
Existing UI: `lib/screens/defect_report_screen.dart`. Before the task each attached photo was a 104×104 dp `_PhotoThumb` (`Image.file(cacheWidth: 208)`); the only interaction was tap → bottom sheet (Retake / Replace from gallery / Remove). There was no way to see a photo larger than 104 dp, no zoom, no next/previous. The fix adds one new full-screen route (`_PhotoViewer`) and enlarges the strip; no other screen changes.

Render mode: **html-twin + static review**. `flutter`/`dart` are not on PATH, so no `flutter analyze`. The Phase 3 twin was copied to `p5-18/render/twin.html` (the Phase 3 file is untouched, verified by diff) and extended with the 2-up strip, the viewer, `theme=dark`, and a `zoom`/`more` state; shot at 390×844 @2x with Playwright 1.63.0.

## Design-context table (`01-inspect.json`)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `AppBar` on every screen, go_router stack, modal bottom sheets for secondary actions | yes (but `routing: []` although `GoRouter(routes:…)` is in `main.dart`) |
| theme | dual-theme, default light | KNOWN | `theme:` + `darkTheme:` + `highContrastTheme`, `ThemeMode.system`, light is the working theme | yes |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations") | flat, elevation 0, 1–3 dp `BorderSide` outlines everywhere (`OutlinedButton`, `OutlineInputBorder`, `Material(shape: … side:)`), `surfaceContainerHighest` tonal fills | partial — value right, but borders are declared in a dozen places and status is UNKNOWN |
| radius | small (4) | INFERRED ("most common radius 4 (1×)") | `FieldSizes.radius = 8` used for every control, input and tile; 4 is only the index chip | no |
| spacing | irregular ([2, 12]) | UNKNOWN | explicit scale `FieldSizes.space1..space8` = 4/8/12/16/24/32, `controlGap` 12 | partial (wrong value, but not confident) |
| typography | unknown; type_scale true, tabular_numerals false | UNKNOWN | system font (no family — correct); explicit `TextTheme` 36/28/24/22/18/16/14; `FontFeature.tabularFigures()` on the checklist count | partial (family right, tabular figures wrong) |
| components | "go_router, riverpod" | KNOWN | those are routing/state libraries; the component layer is `lib/widgets/` (`BottomActionBar`, `StatusBadge`, `OfflineBanner`, state views, sheets) which inspect lists separately under `component_dirs` | partial |
| product_hints | erp, iot | — | utility field-inspection / field service | no (propagated into requirements density and the direction violation) |
| tests | [] | — | `test/checklist_test.dart` exists | no |

## Requirements verdict (`02-requirements.json`, status CONFIDENT)
| field | value | verdict |
|---|---|---|
| platform_evidence | mobile, STRONG_INFERENCE from "in the field"; MISSING "confirm platform" | correct. Minor: the project inspect already has `platforms: ["mobile"]` KNOWN from pubspec, yet the ledger lists platform as inferred from wording and asks to confirm. |
| intent.artifact_state | existing (present-tense observation) | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | [] | miss — "tiny thumbnails / can't check" is a legibility / media-size problem; nothing was extracted |
| intent.change_scope | unknown | acceptable |
| mode + evidence | audit, refactor ("problem statement on existing UI", "fix follows the diagnosis") | acceptable — I expected polish/refactor; refactor is present, audit is defensible for an observation sentence |
| scope.kind / reason | in-scope, "UI design / interaction task" (ui terms: report, field, photo, thumbnail) | correct |
| change_budget | low | acceptable — everything else on the form is preserved; the fix is one component plus one pushed screen |
| intent.preserve | [] | acceptable |
| product | erp, iot (ledgered KNOWN from README) | wrong — field inspection; this is a Phase 3 miss that persists |
| screen / components | [] / [form] | partial — the sentence names photos and thumbnails; no photo/media component was recognised, only "form" |
| density | medium ("implied by product erp") | wrong for a gloves app; the direction later overrides to low and then flags itself |
| risk | low | arguably wrong (safety-critical defects) |
| environment | outdoor (from "in the field") | correct and useful |
| concerns.required | includes **data-display** ("numbers, tables or charts are the content") and required concept `table.tabular_figures` ("numeric data") | wrong — there is no numeric content; this pulled `typo-scale-and-roles` into the bundle |

## Guidance verdict (`03-guidance.md/json`; status PARTIAL; bundle 6 = core 3 + guardrails 3; 1065 tokens)
| record | role | verdict | note |
|---|---|---|---|
| `comp-photo-capture-field` | core | partial → **missing-critical** | Describes exactly what the code already does (row of ≥96 dp tiles, tap → sheet with Retake / Replace / Remove, per-photo sync state, announce "Photo 1, retake or remove"). It has no "view at full size / zoom / verify before saving" step, which is the whole task. The flutter hint ("a ListView of 104 dp tiles") literally prescribes the size the user is complaining about. |
| `imagery-none` | core | off-target → **generic** | "Remove stock photos, abstract blobs and hero illustrations from working screens." The photos here are the evidence; selected for "secondary mode, product erp". Read literally it points the wrong way. Ignored. |
| `comp-form` | core | partial | General form rules, all already implemented in Phase 3; selected for "mode audit". Nothing about photos. |
| `mobile-field-use` | guardrail | relevant | ≥7:1 contrast, very high-contrast dark surfaces allowed, ≥48 dp + ≥12 dp, no precision gestures with gloves, next action in thumb reach — used for the viewer (dark theme, 56 dp buttons, button zoom + Previous/Next, actions in the bottom bar). The codebase already embodies it, so it confirmed rather than informed. |
| `typo-scale-and-roles` | guardrail | off-target → **generic** | Selected for "data-display / tabular figures"; there is no numeric content in this task. Ignored. |
| `mobile-safe-areas` | guardrail | partial | Relevant to the viewer's bottom bar; satisfied by reusing `BottomActionBar`, which already handles insets. |

Relevant 1 · partial 3 · off-target 2. `comp-media-card` was omitted as "contamination (ecommerce/education/media vs erp/iot)" — that is fine, a media card is not the answer either.

### Real concept recall
Delivered concepts (union over the 6 selected records): touch.minimum_target, state.offline_sync, onboarding.permission_priming, a11y.accessible_names, state.unsaved_changes_guard, feedback.validation_errors, touch.ime_keyboard, form.autofill_attributes, env.outdoor_readability, env.glanceable_status, table.tabular_figures, brand.type_roles, touch.safe_areas (13).

| expected id | critical | delivered? | layer if missing |
|---|---|---|---|
| perf.image_sizing | yes | no | **expected-concepts** — never demanded; `mobile-perf-images-overdraw` carries it and ranked 0.324 in the k=12 search ("never load original-resolution images into thumbnails" is one half of this bug: the tiles were decoded at 208 px) |
| touch.minimum_target | yes | yes (`comp-photo-capture-field`, `mobile-field-use`) | — |
| touch.gestures_discoverable | yes | no | **bundle-selection** — demanded (recommended), candidate `mobile-gestures-discoverable` 0.348 (0.456 on a "viewer with pinch zoom" query), dropped by the cap; its "pinch zoom needs a visible equivalent" is the guardrail a viewer needs |
| env.outdoor_readability | yes | yes (`mobile-field-use`) | — |
| a11y.accessible_names | no | yes (`comp-photo-capture-field`) | — |
| interaction.back_semantics | no | no | **expected-concepts** — never demanded; also a knowledge gap for mobile: the only carriers are `tv-back-behavior`, `tv-player-controls`, `comp-mini-player`, `media-resume-and-details` (all filtered by platform) |
| process.reuse_first | no | no | **bundle-selection** — demanded (recommended), candidate `impl-reuse-before-new` 0.207, dropped |

Recall 3/7 = **0.43**; critical recall 2/4 = **0.50**.

Knowledge gap (confirmed with `search -k 12` and a direct "full-screen photo viewer with pinch zoom on mobile" query): no record in the base carries a full-size / zoomable photo viewer or a "verify the capture before submitting" behaviour. The closest hits are `comp-photo-capture-field` (no viewer), `mobile-gestures-discoverable` (mentions pinch zoom generically) and `layout-split-player` (a video player). The bundle therefore re-prescribed the status quo.

## Direction verdict (`04-direction.md/json`)
Change budget low. Preserved: navigation, layout, surface, cards, typography, color (light-first dual theme), motion, focus, cta, icon, metadata — all correct. Changed/new slots:
| slot | choice | justified? |
|---|---|---|
| density | `density-low` (new) — "outdoor/gloves: low density unless stated" | yes; matches the codebase (56 dp controls). |
| imagery | `imagery-none` (new) — "no repository evidence for this slot" | **no** — the task is about functional photographs; the alternatives list shows `imagery-thumbnails` ("Functional thumbnails", 0.345) was considered and lost to a record that says to remove imagery from working screens. |

`validation.ok = false`: "dense product: low/spacious density selected". The violation is wrong: it comes from `product = erp` (a README misread), and low density is exactly right here. A correct choice was flagged because of an upstream context-detection miss. Core guidance in the direction repeats `comp-photo-capture-field`, `imagery-none`, `comp-form`; guardrails repeat the three above. The fingerprint `image_strategy: none` is wrong for a photo-evidence form.

## Implementation
Files changed (copies of the originals in `before/`):
- `project/lib/screens/defect_report_screen.dart` (+~250 lines):
  - `_PhotoThumb`: two tiles per row via `LayoutBuilder` (`(maxWidth − 12) / 2` → ~173×130 dp 4:3 at 390 wide, was 104×104), `cacheWidth = width × devicePixelRatio` (was fixed 208 px), semantics "Photo n of m — Opens full size to check it"; strip wrapped in `Semantics(label: 'Photos, N added')`. Tap → viewer; long-press → the existing actions sheet (a shortcut, never the only path).
  - `_PhotoViewer` (new, `MaterialPageRoute(fullscreenDialog: true)` so system back / predictive back closes it): wraps itself in `Theme(data: AppTheme.dark(highContrast: settings.highContrast))` so the existing `AppBar` (72 dp, 56 dp icon buttons), `OutlinedButton`, `FilledButton.tonal` and `BottomActionBar` render high-contrast on the near-black surface. `PageView` + `InteractiveViewer` (pinch 1–4×, pan only when zoomed so swipes page between photos), double-tap and an explicit Zoom in/out button (centred 2.5× via a translate+scale matrix), labelled 56 dp Previous/Next buttons (hidden for a single photo), Remove (outlined, error colour) and Retake in the bottom bar, "More" opens the shared Retake / Replace / Remove sheet using the viewer's themed context. Title "Photo n of m" is a live region. Reduced motion: `jumpToPage` instead of animate; zoom is instant.
  - `_photoActions` refactored into a static `_showPhotoActionsSheet(context, index:, count:)` shared by the strip and the viewer; results flow back as `_ViewerResult(action, index)` so Retake/Replace/Remove keep replacing in place.
- `render/twin.html` (p5-18 copy) + `render/shoot.js`: 2-up tiles with stand-in photographs, `#screen-viewer`, `.dark` token block copied from `AppTheme.dark`, `theme=dark`, `zoom=1`, `state=more`, `count=1`.

Guidance used: `mobile-field-use` (dark high-contrast viewer, 56 dp buttons, no gesture-only actions, actions in thumb reach); the sheet/target-size parts of `comp-photo-capture-field` (kept as-is); `mobile-safe-areas` (via `BottomActionBar`). Guidance ignored: `imagery-none` (contradicts the task), `typo-scale-and-roles` (no numeric content), `comp-form` (already implemented, not about photos), the direction's density "violation". Everything that actually solves the sentence — larger decode size, a full-screen viewer, zoom with a button equivalent, next/previous, back closes — came from the codebase and my own expectation, not from the bundle.

Static review notes (no compiler): `Matrix4` comes from `flutter/widgets`; `..translate/..scale` are deprecated in favour of `translateByDouble/scaleByDouble` in Flutter ≥3.27 (warning only, project pins ≥3.22); `settingsProvider` imported from `state/settings.dart`; Dart 3 switch statements match the existing style; `_transform` is handed only to the current page's `InteractiveViewer`.

## Renders
`render/first-*.png` and `render/final-*.png`: form (light, dark, high-contrast, keyboard), viewer (photo 1, photo 2, zoomed, single photo, high-contrast, More sheet).

First-render defects: 1 × **implementation-bug** (twin only) — in dark mode every heading that inherits colour (app-bar title, item title, section labels, sheet title) was invisible because `color` was set on `body` and resolved against the light variables before `.dark` on `.phone` redefined them. Fixed with `.phone{color:var(--on-surface)}`; the Flutter code is unaffected (text colours come from the `ColorScheme`). Visual 0, interaction 0, accessibility 0, platform 0, existing-system-mismatch 0.
Final defects: 0. Iterations: 1.

Observed and accepted: a 4:3 landscape photo shown `contain` on a portrait phone leaves black bands above and below (Flutter `BoxFit.contain` behaves the same); zoom fills the stage. Tiles are 173×130 which still crop the photo (cover); the viewer is the check step.

## Preservation
Navigation preserved (AppBar back, go_router routes untouched; the viewer is a pushed route inside the existing navigator). Theme preserved (viewer uses `AppTheme.dark` with the current high-contrast flag; no new colours). Typography preserved (theme text styles only). Component reuse: `AppBar`, `IconButton`, `OutlinedButton`, `FilledButton.tonalIcon`, `BottomActionBar`, the existing bottom-sheet idiom, `FieldSizes`. Unjustified structural changes: 0. Form state, validation, save flow, sync queue, tests untouched.

## Regressions to propose
1. Query: the task sentence with this project. Expect: a record carrying "tap a captured photo to view it full-screen with zoom (button equivalent) before saving" in core; `mobile-gestures-discoverable` and `mobile-perf-images-overdraw` in the bundle; `imagery-none` and `typo-scale-and-roles` absent; `data-display` not a required concern; `perf.image_sizing` and `touch.gestures_discoverable` demanded.
2. Query: "photo thumbnails are too small to check" on any mobile project. Expect: `perf.image_sizing` required (decode at display size), `imagery-none` never selected when the request's nouns are photo/thumbnail/image.
3. Direction: outdoor/gloves context with `density-low` chosen. Expect: `validation.ok = true`; a product hint must not produce a "dense product" violation against an environment-driven density.
4. Inspect on this project. Expect: radius 8 (`FieldSizes.radius` via `BorderRadius.circular`), spacing scale 4/8/12/16/24/32 from the `abstract final class` constants, surfaces "flat + outlined" KNOWN, tabular numerals true, tests detected, product hint field-service not erp/iot.
5. Requirements on this sentence with `platforms: ["mobile"]` KNOWN in the project file. Expect: platform ledgered KNOWN from the project, no MISSING confirm.

## Tags
`context-detection-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `tooling-limit`, `skill-neutral`, `preservation-ok`
