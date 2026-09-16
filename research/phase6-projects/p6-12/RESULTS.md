# p6-12 — "Add an offline banner and retry to the report list for when the site has no signal."

**Project:** `research/phase3-projects/p3-mobile-flutter-field/project` · Flutter 3 / Riverpod / go_router · platform **mobile** (390×844).
**Existing UI:** yes — the change is a new element on the existing checklist ("report") screen. No new screen.
**Build hash:** start `ea8eed72…d9947` = end `ea8eed72…d9947` (matches the frozen c3 hash).

## What the code actually contains (read before any advise command)

The codebase **already ships** `lib/widgets/offline_banner.dart` — a five-state connectivity strip (offline / sending / failed / all-sent / waiting) with a live region, a determinate progress bar and a `Retry` action in the *failed* state — mounted at the top of `ChecklistScreen` (the only list surface reports are filed from) and of `DefectReportScreen`. `ErrorView` already offers "Try again" + "Open last saved copy", and `SyncQueueSheet` already has "Retry sync now".

So the honest reading of the sentence for **this** codebase is reuse-first: the gaps are (a) the *offline* state offers only `Queue`, no manual retry — the connectivity stream lags when an inspector walks back into coverage, and (b) nothing lets one tap both flush the queue and reload the list. That is what I implemented. There is no separate "report list" screen in the app; the checklist screen is it.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `AppBar` on all three screens + `BottomActionBar`; no bottom nav | partial (top-bar right, the persistent bottom action bar is not reported) |
| theme | dual-theme (default light) | KNOWN | `AppTheme.light/dark` + high-contrast variants, `themeMode.system` | yes |
| typography | custom (System, w400/600/700) | KNOWN | `AppTheme` text theme with encoded scale, system font | yes |
| surfaces | flat-tonal | **UNKNOWN** | `RoundedRectangleBorder` + `BorderSide(outlineVariant)` on every tile — borders are explicit in `checklist_screen.dart` | **partial** (code is clear; "no shadow or border declarations found" is wrong) |
| spacing | irregular `[2, 88, 12]` | **UNKNOWN** | a named 4-based scale exists: `FieldSizes.space1..6` (4/8/12/16/24/32) + `control 56`, `controlGap 12` | **partial** (the scale is in `app_theme.dart` as named constants; the detector reads only literals) |
| radius | small (4) | INFERRED | `FieldSizes.radius` = 8 in `app_theme.dart` | partial (right family, wrong number, same cause as spacing) |
| components | go_router, riverpod | KNOWN | correct, but none of the project's own widgets (OfflineBanner, StatusBadge, BottomActionBar, state views) are listed | partial |

Detection miss worth fixing: token-constant files (`class FieldSizes { static const space3 = 12; }`) are invisible to the spacing/radius/surface detectors, so a project with a clean token layer is reported as "irregular / UNKNOWN".

## 2. Requirements verdict (`02-requirements.json`)

| field | expected | resolved | verdict |
|---|---|---|---|
| platform | mobile | **web** (`platform_evidence: DIRECT, evidence ["site", "banner"]`) | **WRONG** |
| artifact_state | existing | existing | ok |
| operations / mode | create | create (`build/create request on an existing surface`) | ok |
| problem_domain | — | `[]` | ok (no defect language in the sentence) |
| change_scope | local | local | ok |
| scope.kind | in-scope | in-scope | ok |
| change_budget | low/moderate | moderate | acceptable |
| intent.preserve | — | `[]` (but `constraints.preserve_existing_system: true`) | acceptable |
| project_context | see table above | see table above | partial |

**The platform miss is the headline result.** "the **site** has no signal" means the physical work site; the skill read "site" (plus "banner") as a *web* signal at strength `DIRECT`, then hit a real conflict against the repository — `conflicts: [{field: platform, request: [web], project: mobile, resolution: "request kept"}]` — and **kept the request over the repository**. `status` is `AMBIGUOUS`, but nothing in the output asks the user to confirm the platform; it just proceeds as web. Downstream: `input: [pointer, keyboard, touch] "implied by platform web"`, `required_concepts` gained `interaction.keyboard_navigation` and `interaction.hover_independence` (meaningless on a gloved-hands Flutter phone app), the navigation slot got web collapse-to-hamburger advice, and the target-size guardrail leads with "Web: ≥24×24 CSS px (WCAG 2.5.8)" instead of Android's 48 dp. For a repository the skill itself detected as Flutter/mobile, a two-word lexical cue should not outrank the codebase — at minimum the conflict should resolve to the project, or emit a MISSING/confirm entry.

## 3. Guidance verdict (`03-guidance.md` / `.json`) — status AMBIGUOUS, ~1114 tokens

| layer | record | verdict | category |
|---|---|---|---|
| core | `comp-toast-notification` | relevant | — (banner idiom, live region, "inline at the top of the region it concerns" — matches what is there) |
| core | `comp-pagination` | **off-target** | `wrong-screen` (a 6-item checklist; `marginal` shows it contributed **zero** new concepts and zero concerns — pure noise from the word "list") |
| core | `card-list-row` | partial | `generic` (true of the existing rows, contributes no concept; and the rows belong to task p6-11) |
| guardrail | `states-offline-and-sync` | relevant | — DIRECT, carried `state.offline_sync`; "let the user retry manually", "persistent status strip, not a blocking modal", "never lose entered data" is exactly the change |
| guardrail | `layout-states-empty-loading-error` | relevant | — ("error: … retry that works") |
| guardrail | `a11y-target-size` | partial | `off-platform` (correct requirement, web-first framing from the platform miss; the Android 48 dp line is buried mid-record) |
| guardrail | `impl-reuse-before-new` | relevant | — the single most valuable record here, see §Process |
| guardrail | `data-exceptions-first` | partial | `generic` (exceptions-first sorting in tables; only `env.glanceable_status` was actually useful) |

No OPTIONAL NOTES layer was emitted. `layer_review`: core 3 (1 relevant, 1 partial, 1 off-target), critical 5 (3 relevant, 2 partial), optional 0.

### Concept recall

| expected id | delivered? | by |
|---|---|---|
| state.offline_sync (critical) | yes | states-offline-and-sync |
| state.loading_empty_error (critical) | yes | layout-states-empty-loading-error |
| a11y.live_status | yes | comp-toast-notification |
| touch.minimum_target | yes | a11y-target-size |
| a11y.color_not_only | yes | data-exceptions-first |
| process.reuse_first | yes | impl-reuse-before-new |

**concept recall 6/6 = 1.00 · critical recall 2/2 = 1.00.** No forbidden concept was delivered. Two concepts I did not expect were demanded because of the web platform (`interaction.keyboard_navigation`, `interaction.hover_independence`) — noise, not harm.

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`, `changed: []`, budget moderate, `validation: ok`. **`unjustified_direction_slots: 0`** — correct for a local add on an existing UI. The navigation slot text is web guidance ("collapse to a menu button below the container width", `aria-current`) on a Flutter app, but it is attached to a *preserved* slot and marked "Existing system: do not replace it", so it cost nothing. The density note ("targets ≥ 48 dp with ≥ 12 dp spacing") is genuinely field-correct and I measured against it.

## 5. Implementation

Files changed (originals in `before/`):

- `lib/widgets/offline_banner.dart` — extended through its API rather than replaced: new optional `onRetry` callback; the **offline** state's action button is now `Retry` (was `Queue`) wired to a new `retryNow()` that re-checks connectivity, drains the queue and reloads the host screen, and shows "Still no signal. Everything stays saved on the device." when there is still no radio; the headline/detail region became its own 56 dp control (`_BannerText`) that opens the sync queue, with a 20 dp chevron matching the settings "Sync queue" row; added `relativeShort()` so the detail stays on one line next to the chevron; offline detail says "Nothing waiting" instead of "0 pending".
- `lib/state/providers.dart` — `SyncQueue.retryNow()`: invalidates `connectivityProvider`, re-reads `Connectivity().checkConnectivity()`, requeues failed items and drains; returns whether the device is back online. Nothing is dropped when it is not.
- `lib/screens/checklist_screen.dart` — passes `onRetry: () => ref.refresh(inspectionProvider(inspectionId).future)` so one tap covers "send what is queued" and "fetch what I could not load". One-line change; the defect-row checkbox (task p6-11) was not touched.
- `render/twin.html` (task copy of the project twin) — banner text region as a button + chevron, Retry label, and a new `state=offline-nosignal` shot with the snackbar.

**Guidance used:** `states-offline-and-sync` (manual retry alongside automatic, persistent strip not a modal, keep content usable, nothing lost — this is the shape of the change), `impl-reuse-before-new` (reuse → extend: the decisive call not to build a second banner), `comp-toast-notification` (banner at the top of the region it concerns; live region wording), `layout-states-empty-loading-error` ("retry that works"), `a11y-target-size` (56 dp / 12 dp gap, measured).
**Guidance ignored:** `comp-pagination` (no pagination on a 6-item checklist), `card-list-row` (rows are another task's and unchanged), `data-exceptions-first` (no table here), the navigation slot's web advice (Flutter `AppBar`, and the slot is preserved).

### Process guidance check
`impl-reuse-before-new` in the bundle **was** needed and earned its place: the sentence says "Add an offline banner", the codebase already has one, and an implementer following the sentence literally would have shipped a duplicate strip. SKILL.md §2 says the same thing, but having it inside the CRITICAL layer for exactly this query is what made me open `offline_banner.dart` before writing anything. `impl-safe-modification` and `verify-render-and-inspect` were **not** in the bundle and §7 was enough for the render loop. → `process_records_needed: true`.

## 6. Render and defects

Render mode: **html-twin** (Flutter, no SDK on this machine) at 390×844, deviceScaleFactor 2, plus static code review and Playwright box measurements. 11 shots each of `first-*` and `final-*`.

First-render defects (3):
- `visual` — twin snackbar drawn over the bottom action bar; a Flutter fixed `SnackBar` sits above `bottomNavigationBar`. Twin fidelity, fixed.
- `interaction` — after moving `Queue` off the button, the queue was reachable only from an unmarked text region: no visible affordance. Fixed by the chevron.
- `visual` — (introduced by that fix, caught on re-render) the chevron pushed "3 pending · synced 42 min ago" onto a second line, so the strip grew 72 → 84 dp and broke the file's own invariant that the strip's height is identical in every state. Fixed with `relativeShort()` ("42m ago") + a 20 dp chevron; measured back to 72 dp.
- (also fixed) twin showed the chevron in the `pending` state where the Flutter code does not.

**Final defects: 0.** Measured on the final render: Retry 80×56, banner text control 226×56, 12 dp gap, banner 390×72 — meets the direction's field-use floor. **Iterations: 3.**

No defect the guidance warned about was shipped.

## 7. Preservation

Navigation, theme, typography, spacing scale, component set unchanged; the change reuses `_BannerButton`, `FieldSizes`, `StatusColors` and the existing sheet. `unjustified_structural_change: 0`. The one visible trade is inside the offline state: the strip's button is now `Retry` and the queue moved to the (larger) text control — justified by the task sentence, and the queue keeps a 56 dp target plus an accessible name.

## 8. Miss routing (earliest layer, one per miss)

1. **platform-evidence** — "site"/"banner" ⇒ web at DIRECT strength, kept over a detected Flutter/mobile repository with no confirm prompt.
2. **bundle-selection** — `comp-pagination` entered a core slot with zero marginal contribution and no list-size evidence.
3. **project-context** — spacing/radius/surface detectors miss named token constants in Dart (`FieldSizes`), reporting a tokenised project as irregular/UNKNOWN.

## 9. Regressions to propose

- query: `"Add an offline banner and retry to the report list for when the site has no signal."` with a Flutter/mobile project — expect platform **mobile** (or UNKNOWN + confirm), never `web`; "site" must not be a DIRECT web signal when the repository is a native mobile stack.
- query: any list task on a project whose largest list is a handful of items — expect `comp-pagination` **not** in core (no record with zero marginal concept contribution in the core layer).
- inspect: a Dart/Flutter project with `class FieldSizes { static const space3 = 12.0; ... }` — expect `spacing` KNOWN/4-based and `radius` = 8, not `irregular` / `4`.

**Tags:** `platform-miss`, `ranking-miss`, `context-detection-miss`, `render-defect-fixed`, `preservation-ok`, `skill-helped`
