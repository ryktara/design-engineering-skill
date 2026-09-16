# p6-09 — Stock adjustment form: Save and Discard look identical

**Task sentence (verbatim):** "Stock adjustment form: Save and Discard look identical and people click the wrong one."
**Project:** `research/phase6-projects/p6-vue-inventory/project` — Vue 3 + Vite + Pinia + vue-router, CSS custom-property token layer (`src/styles/tokens.css`), light + `[data-theme='dark']`. Platform: web.
**Artifact state:** existing UI (`src/views/StockAdjustmentView.vue`, `src/components/AppButton.vue`). No new screen.
**Build hash:** start `ea8eed72…d9947`, end `ea8eed72…d9947` — identical, as required.
**Root cause in the code (read before any advise run):** both footer buttons were `<AppButton variant="primary">`, so Save and Discard rendered as the same solid indigo button; there was no confirmation on Discard. Separately `AppButton`'s `.btn-danger` was a copy-paste of `.btn-primary`, so the "destructive" variant was also indistinguishable from primary.

## Design-context table (step 1)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | persistent left `SideNav` **and** a `TopBar` (App.vue renders both) | partial — the rail is the primary navigation and was not detected |
| theme | unknown | UNKNOWN | explicit light + `[data-theme='dark']` token sets in tokens.css | partial |
| surfaces | bordered-flat | INFERRED | bordered panels, one popover shadow | yes |
| radius | small | INFERRED | `--radius: 6px` everywhere | yes |
| spacing | irregular | UNKNOWN | clean 4-pt scale `--space-1…8` | partial — the scale is explicit in tokens.css |
| typography | humanist-sans | KNOWN | IBM Plex Sans + IBM Plex Mono, encoded scale, tabular figures | yes |
| components | unknown | UNKNOWN | `src/components/` with AppButton/AppDialog/DataTable/… | partial |

## Requirements verdict (step 2)

- platform `web` from project inspection — correct (`platform_evidence` empty, the sentence carries no platform word; resolved from the repo, acceptable).
- `intent.artifact_state = existing` — correct. `operations = [diagnose, modify]` — correct. `problem_domain = [visual, interaction, brand]` — `brand` is wrong; it comes from the lexical trigger "look identical" and it is the seed of the bad guardrail below.
- `mode = [polish, audit]` with evidence "visual defect on existing UI / diagnose first" — matches expectation (`polish`, `audit`).
- `scope.kind = in-scope`, reason "UI design / interaction task" — correct.
- `change_budget = low`, `constraints.preserve_existing_system = true` — correct for a two-button defect.
- `intent.preserve = []` (empty) while `intent.scope = moderate` and `change_scope = unknown` — harmless here because the budget is low.
- `project_context` passed through intact.

## Guidance verdict (step 3)

Bundle: 6 records (core 3 + guardrails 3), ≈1059 tokens, token_coverage 0.91.

| Layer | Record | Verdict | Category |
|---|---|---|---|
| core | `comp-dialog` | relevant | — (gave the destructive-confirm + safe-default-focus rule I implemented) |
| core | `comp-form` | partial | generic — form-wide advice (labels, autofill, IME, validation); only "primary action last / unsaved-changes guard" touched the task |
| core | `layout-form-stack` | partial | generic — restates form layout rules the project already satisfies; says nothing about action hierarchy |
| critical | `anti-brand-cosmetic-only` | off-target | wrong-product — multi-brand differentiation, tells me to run `fingerprint.py compare`. There is one brand. Pure lexical bleed from "look identical" |
| critical | `layout-states-empty-loading-error` | off-target | generic — loading/empty/error states for a 5-field form that has none of those problems |
| optional | `layout-hierarchy-one-thing` | relevant | — carries `layout.one_primary_action`, the actual fix |

`layer_review`: core `[comp-dialog, comp-form, layout-form-stack]`, critical `[anti-brand-cosmetic-only, layout-states-empty-loading-error]`, optional `[layout-hierarchy-one-thing]`; optional_useful 1, optional_noise 0.

**The load-bearing record for this task sits in the OPTIONAL layer while both CRITICAL GUARDRAILS are off-target.** `brand.structural_differentiation` was promoted to a *critical* concept because `problem_domain` picked up `brand` from "look identical"; `layout.one_primary_action` was only "recommended". That is a criticality inversion, not a retrieval failure — the right record was retrieved, just demoted.

### Concept recall

| Expected concept | Delivered? | Carrier / layer if missing |
|---|---|---|
| layout.one_primary_action | yes | `layout-hierarchy-one-thing` (optional layer, SPECIFIC) |
| feedback.confirmation_destructive | yes | `comp-dialog` (GENERIC carrier) |
| state.unsaved_changes_guard | yes | `comp-form` |
| a11y.accessible_names | no | `expected-concepts` — never demanded, absent from the trace entirely |
| interaction.focus_visible | no | `candidate-retrieval` — listed in `not_surfaced` as "no sufficiently specific guidance" |
| process.reuse_first | no | `bundle-selection` — candidate `impl-reuse-before-new` existed, cap/utility dropped it |

Recall 3/6 = **0.50**. Critical recall (my two pre-registered criticals) 2/2 = **1.00**. No forbidden concept appeared; the platform filter correctly dropped all tv/kiosk/mobile records.

Bundle-level defect: `missing-critical` does **not** apply — both of my criticals are present. The bundle's own `critical_concepts` list (`brand.structural_differentiation`) is what is wrong.

## Direction verdict (step 4)

12 of 13 slots `preserved` with correct reasons; validation OK. **`unjustified_direction_slots = 1`**: `cards → List rows (new)`, reason "no repository evidence for this slot" — the task has nothing to do with cards and the budget is low; a preserved/NA status was the right answer. Minor mismatch: `cta` is marked *preserved* ("the task does not concern this slot") when the CTA hierarchy is precisely the task. The fingerprint also reports `corner_language: sharp` while the project uses a 6px radius everywhere.

## Implementation (step 5)

Files changed (copies in `before/`):
- `src/views/StockAdjustmentView.vue` — Discard → `variant="secondary"` (the project's existing neutral variant); Save relabelled "Save adjustment"; Discard now opens an `AppDialog` confirmation ("Keep editing" secondary / "Discard" danger), reusing the exact Cancel+danger footer pattern from `ProductDetailView`; focus moves to the safe action when the dialog opens and returns to the trigger (or the product field after a discard).
- `src/components/AppButton.vue` — `.btn-danger` now uses `--color-danger` instead of duplicating `.btn-primary`, plus a matching focus-ring colour. Without this the confirmation dialog would have reproduced the same "two identical buttons" defect.

No new component, no token, no layout, no route, no store change. `vite build` (to a temp outDir, so the concurrently-edited `dist/` was untouched) succeeds.

**guidance_used:** `layout-hierarchy-one-thing` (one primary action per view), `comp-dialog` (destructive confirmation + first focus on the safe action), `comp-form` (unsaved-changes guard → the confirm dialog).
**guidance_ignored:** `anti-brand-cosmetic-only` (single-brand app, `fingerprint.py compare` is meaningless here), `layout-states-empty-loading-error` (no loading/empty/error surface in this form beyond the notices that already exist), `layout-form-stack` (already satisfied by the existing markup).

**skill_effect: helped.** `comp-dialog`'s "safe default for destructive confirmations / first focus on the safe action" is the reason the confirm dialog opens focused on *Keep editing* and restores focus on close — I would plausibly have shipped the variant swap alone and left focus on the trigger.

**Process guidance check:** `process_records_needed = false`. SKILL.md §2 (reuse → extend → compose → new) and §7 (render and inspect) were enough: reuse pointed at the existing `secondary`/`danger` variants and `AppDialog` instead of new styles, and the render loop caught the focus defect. Having `impl-reuse-before-new` in the bundle would have cost tokens for advice I was already following.

## Render (step 6–7)

Render mode: **native web** — Playwright 1.63.0 / Chromium against `vite` dev on :5219, 1280×800 and 390×844, plus a dirty-state and open-dialog capture and a `data-theme=dark` capture. All screenshots inspected.

First render of the implementation (`render/first-*.png`): 1 defect.

| Type | Count | Detail |
|---|---|---|
| accessibility | 1 | opening the confirmation left focus on the form's Discard trigger; nothing moved into the dialog (`document.activeElement` verified in-browser) |

Fixed by a `watch` on the open state that focuses the safe action and restores focus on close. **Iterations: 1.**

Final render (`render/final-*.png`): 0 defects of the counted types. Verified in-browser: open → focus "Keep editing"; cancel → focus back on "Discard"; confirm → focus on the product field and the form cleared.

Remaining, **pre-existing and out of the permitted file set** (present identically in the before state, not counted):
- `AppDialog.vue` has no `role="dialog"`/`aria-modal`, no focus trap and no Escape handler. The task scope was the adjustment view and the button component; touching the shared dialog would also collide with the concurrent task. Worth a follow-up.
- At 390 px the whole app is broken (fixed 420 px form column, side rail never collapses) — app-shell responsive debt, identical before and after.

## Preservation

navigation, theme, typography, spacing tokens, surfaces, routes, ids, store and form semantics all unchanged. Component reuse: yes (existing variants + existing dialog). `unjustified_structural_change: 0`. **preservation-ok.**

## Misses by earliest layer (step 8)

1. `criticality` — `brand.structural_differentiation` was made a critical concept and `layout.one_primary_action` only recommended, from the phrase "look identical". For a two-button hierarchy defect the criticality is inverted; the one useful record landed in OPTIONAL and a `fingerprint.py compare` instruction landed in CRITICAL GUARDRAILS.
2. `expected-concepts` — nothing demanded button/CTA hierarchy or accessible naming of actions; `comp-form` and `layout-form-stack` cover the *fields*, and no record in the base speaks to "primary vs secondary vs destructive action styling in a form footer" directly (checked: `layout-hierarchy-one-thing` is the closest, and it is about screen focal points). Candidate `knowledge-gap` for a CTA-hierarchy record.
3. `direction` — one unjustified `new` slot (`cards`) on a low-budget existing UI.
4. `project-context` — navigation detected as top-bar only (misses the side rail), theme/spacing/components UNKNOWN although tokens.css states them explicitly.

## Regressions to propose

- Query: "Stock adjustment form: Save and Discard look identical and people click the wrong one." — expect `layout.one_primary_action` to be **critical** and `brand.structural_differentiation` to be absent from the bundle.
- Query: "the cancel button looks the same as the submit button" — expect a record about primary / secondary / destructive action hierarchy in the CORE layer; today no such record exists (knowledge gap).
- Project inspection of a Vue app whose `App.vue` renders both a rail and a top bar — expect `navigation` to report the rail, not `top-bar`.
- Project inspection with a `tokens.css` containing `[data-theme='dark']` — expect `theme` KNOWN (light+dark), not UNKNOWN.

## Tags

`concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`
