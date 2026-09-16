# p6-16 — "Freezing a card happens the instant you touch the switch."

- **Project / stack / platform**: `p6-compose-banking` (NorthBank) · Kotlin, Jetpack Compose, Material 3, androidx.navigation, in-memory `FakeAccountRepository` (350 ms simulated latency) · mobile.
- **Existing UI**: yes — `ui/screens/cards/CardsScreen.kt`. No new screen.
- **Build hash**: start `ea8eed72…d9947`, end `ea8eed72…d9947` — equal, matches the frozen c3 candidate.
- **Render mode**: `html-twin` (no gradle build available) at 390×844, plus static code review of the Kotlin.

Baseline behaviour in code: the `Switch` calls `repository.setCardFrozen` straight from `onCheckedChange`. No confirmation for an action that stops the card working, no in-flight state during the 350 ms suspend call (the switch stays on the old value and then jumps), no result announcement, no undo. Frozen state is carried only by a `Color.White.copy(alpha = 0.55f)` wash over the card art plus a subtitle word.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `NorthBankBottomBar` (4 `NavigationBarItem` tabs) is the shell; each screen also has a `TopAppBar` | partial |
| theme | dual-theme, default light | KNOWN | `NorthBankTheme` with `LightColors`/`DarkColors`, light default | yes |
| surfaces | bordered-flat | INFERRED | `NbCard` = `OutlinedCard`, 1 dp `outlineVariant`, no elevation | yes |
| radius | small (4) | INFERRED | `CardCornerRadius = 12.dp`; 4 dp only for the gold chip and `extraSmall` | partial |
| spacing | unknown | UNKNOWN | `Spacing.kt`, explicit 4-pt object (`xs`…`xxl`, `screen`), used by every screen | no |
| typography | custom, type scale, tabular figures | KNOWN | `NorthBankTypography`, full M3 role set, `tnum` on the PAN | yes |
| components | compose, material3 | KNOWN | correct | yes |

Navigation is counted `partial`: the detector saw the per-screen `TopAppBar` (30 matches) and demoted `bottom-tabs` (5 matches) to a candidate, so the primary navigation grammar of the app is misreported.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform | `mobile`, `platform_evidence: []` | correct (resolved from project inspection) |
| intent.artifact_state | `unknown` (`existing:false`, `problem:false`) | **wrong** — the sentence reports a defect in an existing screen |
| intent.operations | `[]` | miss |
| intent.problem_domain | `["performance-ux"]` from the stem `freez` | **wrong** — "freeze a card" is a banking action, not UI jank |
| intent.change_scope | `unknown` | miss |
| mode | `["create"]`, evidence `create: default (no cue at all)` | **wrong** — expected refactor/polish |
| scope.kind | `in-scope`, "UI design / interaction task" | correct |
| change_budget | `moderate` | acceptable |
| intent.preserve | `[]` (but `constraints.preserve_existing_system: true`) | acceptable |
| project_context | as above | partial |

Two false positives worth naming: `components: ["card"]` and `primary_jobs: ["create card"]` both come from the payment-card noun in the sentence being read as a UI card component. That single token drives the core guidance pick below.

## 3. Guidance verdict (`03-guidance.md` / `.json`) — status PARTIAL, 5 records, 609 tokens

| layer | record | verdict | category |
|---|---|---|---|
| CORE | `card-none` | off-target | `contradicts-codebase` |
| CORE | `focus-none-touch-only` | partial | `generic` |
| GUARDRAIL | `typo-scale-and-roles` | off-target | `generic` |
| GUARDRAIL | `impl-reuse-before-new` | relevant | — |
| GUARDRAIL | `mobile-density-touch` | off-target | `wrong-screen` |
| bundle | — | — | `missing-critical` |

Relevant 1 · partial 1 · off-target 3 · optional layer empty (0 useful / 0 noise).

- `card-none` ("remove nested rounded rectangles, group with whitespace and a hairline") is the worst pick: the project's entire surface language is `NbCard`, and the freeze row lives inside one. Following it would have deleted a deliberate component. It entered on `task evidence: component, lexical_strong` — i.e. on the payment-card noun.
- `mobile-density-touch` is table/filter/bulk-selection guidance; there is no table on this screen.
- `typo-scale-and-roles` entered only as the carrier for the "critical" concept `table.tabular_figures`, which this task does not touch.
- `impl-reuse-before-new` matched what I did (reuse `NbCard`/`NbListRow`/`Spacing`), but SKILL.md §2 already says it.

### Concept recall

Expected 6, delivered 0. **Recall 0.00 · critical recall 0.00.**

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `feedback.confirmation_destructive` | no | `expected-concepts` (demanded only as *recommended*; `not_surfaced` reason "no sufficiently specific guidance", although `comp-dialog`, `states-persistence-and-session` and `comp-settings-screen` all carry it) |
| `state.saving_conflict` | no | `expected-concepts` (never demanded; carriers `states-persistence-and-session`, `states-offline-and-sync` exist) |
| `a11y.live_status` | no | `expected-concepts` (carriers `a11y-live-status`, `feedback-progress-async`, `comp-toast-notification` exist) |
| `a11y.accessible_names` | no | `expected-concepts` |
| `a11y.color_not_only` | no | `expected-concepts` |
| `state.loading_empty_error` | no | `expected-concepts` |

Delivered instead: `layout.no_nested_cards`, `table.tabular_figures`, `brand.type_roles`, `process.reuse_first`, `table.column_priority`, `touch.minimum_target`. The skill reports `concept_coverage_ratio 1.0` and `critical_coverage_ratio 1.0` against its own demand list — the demand list is what is wrong, not the retrieval. No knowledge gap: every missing concept has a carrier in `data/`.

PARTIAL status here is not a design/engineering split — it is "required concern `component` uncovered", which is a bookkeeping artefact of the `component` concern having been raised by the same false-positive "card" token.

## 4. Direction verdict (`04-direction.md`)

12 slots preserved, 1 changed: **`cards` → `card-none`, status `new`, "no repository evidence for this slot"**. `unjustified_direction_slots = 1`. It also contradicts the neighbouring `surface` slot, which is correctly preserved as `bordered-flat` on repository evidence. Preservation metrics and `Validation: OK` are otherwise right, and every "the task does not concern this slot" line is correct.

## 5. Implementation

Files changed (copies in `before/`):
- `app/src/main/java/com/northbank/app/ui/screens/cards/CardsScreen.kt`
- `app/src/main/res/values/strings.xml` (additive only: `action_cancel`, `action_undo`, `card_freezing`, `card_unfreezing`, `card_freeze_confirm_*`, `card_freeze_done`, `card_unfreeze_done`)

What was built, all inside `CardSection`:
1. **Confirmation before freezing.** Material 3 `AlertDialog` — "Freeze this card?" / "Card ending 4417 will stop working straight away. Payments and cash withdrawals will be declined until you unfreeze it. Standing orders and Direct Debits are not affected." Cancel · Freeze card. Unfreezing is the restoring direction and applies directly.
2. **Pending state.** `pendingTarget` holds the in-flight target; the switch shows it optimistically, is disabled while in flight, and a 16 dp `CircularProgressIndicator` sits beside it; the subtitle and the card-art badge both read "Freezing…" / "Unfreezing…".
3. **Result + undo.** A `SnackbarHost` on the screen Scaffold shows "Card frozen" / "Card unfrozen" with an **Undo** action that applies the reverse (and does not re-offer undo). This is what actually covers the accidental touch.
4. **Accessibility.** `Modifier.semantics { contentDescription = "Freeze card"; stateDescription = Active/Frozen/Freezing… }` on the `Switch`; the snackbar gives the live result; status is no longer colour/wash-only — a "Frozen" label sits on the card art.
5. The frozen wash went from `alpha 0.55f` to `0.22f` because at 0.55 the white PAN and metadata on the card art fall to ≈1.9:1 contrast; the status is now carried by the label, so the wash only needs to dim.

Reuse: `NbCard`, `NbListRow` (trailing slot), `Spacing`, `MaterialTheme.shapes`, the existing colour scheme. No new component file, no new route, no repository change, no theme change, no transfer-screen change.

Guidance used: `impl-reuse-before-new`. Guidance ignored: `card-none` (contradicts the codebase), `mobile-density-touch` (wrong screen), `typo-scale-and-roles` (nothing numeric here), `focus-none-touch-only` (already satisfied). Everything that made the change correct — confirm, pending, undo, announcement — I had to bring myself.

**Process guidance check**: not needed. SKILL.md §2 (reuse) and §7 (render and inspect) were enough; `impl-reuse-before-new` was in the bundle and simply restated §2. `process_records_needed: false`.

## 6. Render and defects

Twin: `render/twin.html` (tokens mirrored from `Color.kt` / `Spacing.kt` / `Type.kt`), five states — `instant` (baseline behaviour), `idle`, `confirm`, `pending`, `frozen`. Playwright, Chromium, 390×844 @2×. Screenshots inspected, not assumed.

First render defects (3):
- `implementation-bug` ×1 — twin harness: the `[hidden]` attribute was overridden by `display:flex` on `.scrim` / `.snack`, so the dialog and the snackbar appeared in every state.
- `accessibility` ×1 — frozen card art: white PAN/metadata over the 0.55 white wash ≈1.9:1. Pre-existing in the project, but my change makes the washed state appear more often (pending), so it is fixed here.
- `visual` ×1 — the card-art badge read "Frozen" while the row read "Freezing…" during the pending phase (I passed the optimistic value to a fixed label).

Fixes: `[hidden]{display:none!important}` in the twin; wash to 0.22 in `CardArt`; `statusLabel` threaded into `CardArt` so badge and subtitle always agree. Iterations: 2. Final defects: 0 in all five states.

No defect the guidance warned about was shipped — the guidance warned about nothing relevant.

## 7. Preservation

Navigation, theme, typography, spacing scale and component set all preserved; `NbCard`/`NbListRow` reused rather than replaced; 0 unjustified structural changes. `preservation-ok`.

## 8. Miss routing (one layer per miss)

1. **`mode`** — `create` on an existing-UI defect report ("default (no cue at all)"). Root cause of the whole off-target bundle.
2. **`requirements`** — `artifact_state unknown` / `existing false` / `problem false`; `problem_domain performance-ux` from the stem `freez`; `components ["card"]` and `primary_jobs ["create card"]` from the payment-card noun.
3. **`direction`** — `cards` slot changed to `card-none` on a moderate-budget existing UI, contradicting the preserved `surface` slot.
4. **`project-context`** — navigation `top-bar` instead of bottom tabs; spacing UNKNOWN despite `Spacing.kt`; radius `small` instead of the documented 12 dp.

## 9. Regressions to propose

- "Freezing a card happens the instant you touch the switch." → mode refactor/polish, not create; `feedback.confirmation_destructive` and `state.saving_conflict` demanded as critical; no card-container pattern in the `cards` slot.
- "The delete toggle applies immediately with no confirmation." → `feedback.confirmation_destructive` carried by a DIRECT record, with undo/reversibility.
- Same sentence → "card" as a payment-card noun must not set `components=["card"]` / `primary_jobs=["create card"]`, and `freez*` must not route `problem_domain` to `performance-ux`.

## Tags

`mode-miss` · `requirements-miss` · `concept-miss` · `ranking-miss` · `direction-mismatch` · `context-detection-miss` · `render-defect-fixed` · `skill-neutral` · `preservation-ok`
