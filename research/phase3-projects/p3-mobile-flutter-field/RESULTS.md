# p3-mobile-flutter-field — results

## Task
"Flutter field inspection app for utility technicians working outdoors with gloves and patchy connectivity: checklist, defect report form, offline sync"

Built: inspection checklist screen (large glanceable count, per-row status badge, Pass/Fail/Skip bottom sheet), defect report form (photo, severity, notes; inline validation; IME-aware sticky action bar), offline banner with pending-sync queue sheet and last-synced time, empty/loading/error states.

## Stack / platform
Mobile (Android + iOS), Flutter 3.22+, Material 3, Riverpod, go_router. Started from `evals/fixtures/flutter-app` (a 1-line `PatientList` stub, pubspec with go_router + riverpod) and replaced it with a real app in `project/` (`lib/theme`, `lib/models`, `lib/state`, `lib/screens`, `lib/widgets`, `test/`, `design-tokens.json`).

**Render mode: html-twin + static review.** Flutter is not installed, so the Dart was reviewed statically against the guidance and an HTML twin (`render/twin.html`, values mirrored 1:1 from `app_theme.dart`) was screenshotted at 390x844 with Playwright 1.63.0. The Dart itself was never compiled or run; the widget test in `test/checklist_test.dart` is the intended verification, not an executed one.

## Inspection verdict (`01-inspect.json`, re-run as `01b-inspect-after.json`)
Right: stack=flutter KNOWN (pubspec), platform=mobile, ui_libraries go_router + riverpod, `lib/widgets/` as component dir (after implementation), a11y attributes in 7 files (after), `design-tokens.json` as tokens (after).
Wrong / missed:
- `product_hints: ["erp"]` from a README that says "utility field technicians … inspect poles". There is no field-service / inspection product vocabulary; this wrong hint then propagated into requirements and direction.
- `routing: []` even though `go_router` is a dependency and `GoRouter(routes: …)` is in `main.dart`; go_router is filed under `ui_libraries` instead.
- `tokens: []` on the first run despite `ThemeData`/`ThemeExtension<StatusColors>` in `lib/theme/app_theme.dart`; only the JSON file was picked up later. Flutter theme files are not recognised as a token layer.
- `tests: []` with a `test/` directory containing `*_test.dart`.
- After implementation: `INFERRED: DPAD / remote key handling found in source` and `DPAD/remote/TV-focus handling in 4 files` — false positive (the code has `FocusNode`/`requestFocus` for a text field and `Focus`-free widgets; nothing DPAD or TV).
- `fonts: []` is correct (system font).

## Requirements verdict (`02-requirements.json`, status CONFIDENT)
| field | value | verdict |
|---|---|---|
| mode | create | right (default) |
| platform | mobile | right |
| input | touch (INFERRED) | right |
| product | erp (KNOWN from README) | **wrong** — field-service / utility inspection; and it was ledgered KNOWN although it is a heuristic guess |
| screen | form | **partial** — "checklist" (a list screen) was not recognised; only the form was |
| stack | flutter | right |
| density | medium | acceptable default, but "gloves" should bias toward low density / large targets; not reflected |
| components | form | **partial** — missed list/checklist, status badge, banner, photo capture |
| environment | gloves, low-bandwidth, outdoor | right (all three, from the request) |
| jobs / primary_jobs | [] / "create form" | **wrong** — the job is record inspection results and report defects, not create a form |
| risk | low | **arguably wrong** — utility inspections record safety hazards (critical severity = isolate and dispatch); medium at least |
| constraints | preserve_existing_system, performance_sensitive | right |
| accessibility | screen_reader, touch_targets, reduced_motion, contrast all true | right |
| missing | brand | right |

## Guidance verdict (`03-guidance.md/json`; bundle 7 = core 2 + guardrails 5)
| record | verdict | note |
|---|---|---|
| `comp-form` (core) | relevant | labels above, inline validation, error summary, primary action sticky — all used |
| `layout-form-stack` (core) | relevant | one column, sections as headings, aria-describedby — used |
| `states-offline-and-sync` (guardrail) | relevant, high value | shaped the banner: persistent strip not modal, pending marker per item, last-synced, manual retry, "nothing is lost" copy |
| `mobile-field-use` (guardrail) | relevant, high value | ≥7:1 text, glanceable word+icon+colour status, ≥48 dp with ≥12 dp spacing, large numerals, next action in thumb reach — it is the reason the pass green was darkened from 6.65:1 to 8.4:1 |
| `mobile-density-touch` (guardrail) | partial | no tables in this app; the row-height ≥48 and "fewer things not smaller" parts apply. Selected for "data-display: numbers, tables or charts" which is not this task |
| `anti-no-states` (guardrail) | relevant | states enumerated before coding |
| `typo-scale-and-roles` (guardrail) | partial | the type-scale advice is fine and was followed; the stated selection reason ("required concept table.tabular_figures") is off |
Relevant 5 · partial 2 · off-target 0.

**Ranking misses** (present in the base, not in the bundle; found with `advise.py search`, see `03-search-k12.md` and `03-search-gaps.md`):
- `mobile-keyboard-ime` (score 0.40 in the k=12 search, 0.71 on a keyboard query) — the single most task-specific rule for "form usable with keyboard open"; not selected.
- `mobile-safe-areas` — IME/home-indicator insets; not selected.
- `layout-states-empty-loading-error` and `comp-empty-state` — the bundle chose only the anti-pattern `anti-no-states` for states.
- `a11y-live-status` — announcing connectivity changes; directly relevant to the banner.
- `a11y-target-size` — the concrete target-size rule.
- `comp-list-row-mobile` / `card-list-row` — the checklist and the sync queue are list rows.
- `mobile-gestures-discoverable` — "no swipe-only actions" matters for gloves.
- `comp-setup-checklist` (a setup/progress checklist; partially applicable) and `comp-toast-notification` (covers banners).

**Knowledge gaps** (no record found):
- Photo / camera capture field in a form (thumbnails, retake/remove, compression, offline storage).
- Single-select severity chooser as large toggle buttons (radio group semantics; why not a 4-segment SegmentedButton at 390 dp).
- Per-item tri-state result selection (pass / fail / skip) for inspection checklists.
- Product vocabulary for field service / inspection / utilities (`erp` was the nearest hint and it is wrong).

## Direction verdict (`04-direction.md/json`, validation OK)
| slot | choice | fit |
|---|---|---|
| navigation | bottom tabs | **off** — the app is a stack (work order → checklist → defect); `mobile.md` itself recommends hub-and-spoke for service apps and it was only the alternative. Driven by product=erp |
| layout | form stack | right for the form; the checklist is a list, no slot for that |
| density | medium (INFERRED default) | acceptable; the field-use guardrail then overrides toward 56 dp controls |
| surface | elevated cards | **off** — contradicts `mobile-field-use` (mid-tone surfaces/shadows wash out in glare); I used flat surfaces with outlined tiles. Reason list says "product mismatch" |
| cards | poster-landscape 16:9 media cards | **off / invariant** — 16:9 media cards for an inspection checklist; chosen because `card-list-row` and `card-flat-tile` were rejected as incompatible with the (also wrong) elevated-cards surface. Validation still said OK |
| typography | neutral sans (system font kept) | right |
| color | neutral canvas + one accent | right; the field-use rule adds the 7:1 floor |
| motion | spring | partial — functional/minimal fits a work tool better; not harmful |
| focus | touch-only, keep platform focus visuals | right |
| cta | sticky bar | right, and the IME note in its guidance was used |
| imagery | none | right |
| icon | filled system icons ≥24 dp | right |
| metadata | inline status badges, text in pill | right |
Validation reported no violations even though surface/cards are irrelevant for the task and contradict a guardrail in the same output.

## First-render defects (numbered)
1. Checklist rows separated by a 1 px divider only: adjacent 72 dp targets measured 1 px apart (glove rule ≥8 px). Interaction test failed on checklist and offline screens.
2. Error state: the "Try again" button icon inherited the state hero-icon rule (rendered red, pushed to the far left of the button) — twin CSS bug.
3. Loading skeleton had no header block, so the header (asset type, address, big count) would jump in when data arrives.
4. Offline banner detail "3 pending · last synced 42 min ago" wrapped to two lines at 390 dp.
5. Double line where the last, partially hidden row's divider met the action-bar top border.
6. With the 300 px keyboard and the notes field centred, the clipped top of the "High" severity button sat 4 px below the app-bar back button (56 dp button in a 64 dp bar).
7. Static review (Dart): `Image.network(file.path)` used for a local `XFile` from image_picker; must be `Image.file`.
Also fixed before the first render, at design time: pass green `#0B6B2E` measured 6.65:1 with `tokens.py contrast` and was replaced by `#085A26` (8.4:1) to satisfy the 7:1 field-use rule.

## Final defects
1. Offline banner detail still wraps to two lines at 390 dp with the Queue button beside it (now "3 pending · synced 42 min ago"); the banner grows gracefully, but a one-line version would need a shorter label or a narrower button.
2. Unverified: the Dart was not compiled or run (no Flutter SDK); text scale 1.6, TalkBack/VoiceOver, dark theme and the real IME behaviour of `viewInsets`/`scrollPadding` are asserted from code reading only.

## Iterations
- Iteration 1: rows → flat outlined tiles with 8 dp gaps (Dart `_ItemRow` + `SliverList.separated`, twin CSS); scoped the error-state icon rule; skeleton header block (Dart `LoadingView` + twin); shorter banner text (both); `Image.file` fix; twin marks the background `inert` while the sheet is open (Flutter's modal barrier); interaction script now measures only the visible part of a target inside its scroll container. Result: 17/18.
- Iteration 2: app bar 64 → 72 dp in `AppBarTheme.toolbarHeight` and the twin so a 56 dp icon button leaves 8 dp to scrolling content. Result: 18/18.

## Interaction test summary (`05-interaction.json`; first run kept as `05-interaction-first.json`)
Playwright 1.63.0, 390x844, `reducedMotion: reduce`. 18 checks, all pass on the final render:
- Tap targets ≥48x48 with ≥8 px spacing: checklist (6 targets), offline (7), form (10), form+keyboard (6), queue sheet (0 enabled targets; background inert). Smallest target is the 48x48 photo-remove button; everything else is 56 dp.
- Text contrast ≥7:1 on all sampled body/status/label text on every screen; minimum measured 7.82:1 (`#A3151F` fail red on white).
- Primary action in the bottom 40%: Complete button top at 742/844, Save defect at 742/844.
- 300 px keyboard: action bar bottom = keyboard top (544), Save 476–532 visible, notes field 227–347 visible above the bar and focused; form still scrolls to the photo buttons.
- Offline banner: in-flow (`position: static`), `role=status aria-live=polite`, content starts below it, ≥3 rows fully visible.
- Validation association: textarea `aria-invalid=true`, `aria-describedby="notes-error notes-help"`, error has `role=alert`, `label[for]` present, severity `radiogroup` and photo `group` labelled.
- Focus visible on textarea (3 px primary border) and on buttons (UA outline kept).
- `prefers-reduced-motion` respected (transitions 0 s).
- Empty / loading / error states render with one action each.

## Tokens
`python scripts/tokens.py validate project/design-tokens.json --platform mobile` → OK, 0 errors, 3 warnings (default border 1.7:1 — dividers, non-essential; light elevated == canvas — deliberate flat surfaces). Output in `06-tokens-check.txt`.

## Time spent (rough)
About 2 hours: 20 min project + skill runs, 45 min Dart, 30 min twin + scripts, 25 min render/fix/re-render, 15 min write-up.

## Failure taxonomy tags
`requirements-miss` (product=erp, screen/components only "form", jobs/risk wrong) · `vocabulary-gap` (no field-service/inspection product; "checklist" not a screen) · `ranking-miss` (mobile-keyboard-ime, mobile-safe-areas, layout-states-empty-loading-error, a11y-live-status, a11y-target-size, comp-list-row-mobile, mobile-gestures-discoverable) · `knowledge-gap` (photo capture, severity toggle group, tri-state checklist result) · `direction-invariant` (poster-landscape media cards + elevated cards for an inspection tool passed validation) · `render-defect-fixed` (6 fixed) · `render-defect-remaining` (banner wrap) · `tooling-limit` (no Flutter; html-twin) · `skill-helped` (`mobile-field-use` and `states-offline-and-sync` were exactly right and `tokens.py contrast` caught the 6.65:1 green before render).
