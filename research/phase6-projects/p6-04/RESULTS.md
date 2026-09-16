# p6-04 — "The cart page: removing an item happens instantly and people do it by accident."

- **Project:** `research/phase3-projects/p3-ecommerce-web/project` (Trailhead Supply) · plain HTML/CSS/JS, no framework · platform **web**
- **Existing UI**, no new screen. The "cart page" in this codebase is the **order summary on `checkout.html`** (the header cart icon links to `checkout.html`; there is no separate cart route).
- **Build hash start == end == `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`** ✔
- **Premise check (important):** the sentence's premise is false against this code. Before the change there was **no remove control at all** on the line item — nothing removed instantly, because nothing could be removed. The honest fix is therefore to introduce removal *with* the reversible pattern the sentence asks for, rather than to "slow down" an existing one. Recorded in `00-expectation.json` before any advise command.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `.site-header` top bar + menu button under 720px | yes |
| theme | light-first | INFERRED | `color-scheme: light`, single light palette | yes |
| surfaces | elevated | INFERRED | border-first: 1px `--color-border` on every surface; the only shadow is `--shadow-sticky` for the sticky bar | **no** (confident wrong) |
| radius | pill | INFERRED | tokens are `--radius-sm: 4px` / `--radius-md: 8px`; 999px is used only for chips/badges | **no** (confident wrong) |
| spacing | irregular (UNKNOWN) | UNKNOWN | explicit 4px scale `--sp-1…--sp-12`, used everywhere | partial (code is unambiguous) |
| typography | geometric-sans (Inter, tabular numerals) | INFERRED | Inter + Georgia display, `--fs-*` scale, tabular figures | yes |
| components | unknown | UNKNOWN | clear class-based component set: `.btn`, `.chip`, `.radio-card`, `.line-item`, `.product-card` | partial |

Context-detection miss: `surfaces` and `radius` are both scored off raw CSS counts rather than the semantic tokens the file defines; the direction then proposed "elevated cards" for a border-first system.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform | `web`, `platform_evidence: []` (from project) | correct |
| artifact_state | existing | correct |
| operations | diagnose, modify | correct |
| problem_domain | `[]` | **miss** — the sentence names an accidental destructive action; no feedback/undo domain was derived |
| change_scope | screen | correct |
| mode | audit + refactor (`audit: problem statement on existing UI`) | acceptable (expected refactor/polish) |
| scope.kind | in-scope | correct |
| change_budget | moderate | correct |
| intent.preserve | `[]` | thin, but `constraints.preserve_existing_system: true` carries it |
| screen | `checkout` (from the word "cart") | correct **for this codebase** — the cart really is the checkout summary here |
| project_context | as inspected | carries the two wrong values above |

## 3. Guidance verdict (`03-guidance.md`) — status PARTIAL, bundle 5 (core 2 + guardrails 3), ≈778 tokens, no OPTIONAL layer

| record | layer | verdict | category | note |
|---|---|---|---|---|
| `comp-checkout-one-page` | core | partial | `generic` | a whole-checkout composite; it does carry `feedback.confirmation_destructive`, but its text never mentions removing a line, undo, or a safe default — nothing in it told me what to build for this task |
| `cta-sticky-bar` | core | off-target | `wrong-screen` | the sticky pay bar already exists and is not the task |
| `layout-states-empty-loading-error` | guardrail | relevant | — | the one record that actually changed my implementation: it made me design the **empty-cart** state and block submit instead of shipping a cart that could be emptied into a $0 order |
| `layout-hierarchy-one-thing` | guardrail | off-target | `generic` | true in general, says nothing about this change |
| `ecommerce-delivery-promise` | guardrail | off-target | `wrong-screen` | delivery/returns copy next to the price; unrelated to accidental removal |

Bundle-level defect: `missing-critical` — `a11y.live_status` (announcing the removal and the undo) was never demanded, never retrieved, never delivered.

### Concept recall (delivered = union of `concepts` over the 5 selected records)

| expected id | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| `feedback.confirmation_destructive` | yes | yes (inside `comp-checkout-one-page`, carrier quality poor) | — |
| `a11y.live_status` | yes | **no** | `expected-concepts` — never entered `required_concepts`; `comp-toast-notification` ("undo where applicable, live region polite") exists in `data/components.jsonl` and was never a candidate. Not a knowledge gap. |
| `a11y.accessible_names` | — | no | `bundle-selection` (trace: candidates `a11y-labels-names`, …; `not_surfaced` = "no sufficiently specific guidance") |
| `touch.minimum_target` | — | no | `bundle-selection` (candidates `a11y-target-size`, …) |
| `interaction.focus_restore` | — | no | `expected-concepts` (never demanded) |
| `a11y.dialog_focus` | — | no | `expected-concepts` (never demanded; acceptable — I chose undo over a dialog) |

**Real concept recall 1/6 = 0.17 · critical recall 1/2 = 0.50.** No forbidden concept appeared. The skill's own required set (`interaction.keyboard_navigation`, `hover_independence`, `focus_visible`) was 50% uncovered by its own bundle; the required concerns list left `accessibility` uncovered while the bundle nevertheless spent 2 of 5 slots on checkout-wide and PDP-adjacent copy.

`status=PARTIAL` here is a coverage figure, not a scope split, and the note is fine.

## 4. Direction verdict (`04-direction.md`)

13 slots, all `preserved`, 0 `changed` / `new` → **`unjustified_direction_slots: 0`** — correct for an existing UI at a moderate budget. Validation OK. Two preserved-slot texts are wrong for this codebase (`surface`: "elevated cards" against a border-first system; `typography`: suggests picking a different typeface while marked preserved) — I ignored both, and the "(Existing system: do not replace it for this task.)" suffix made that safe.

## 5. Implementation

Files changed (originals in `before/`): `checkout.html`, `app.js`, `styles.css`.

- Line item gets a **Remove** control: `.link-btn`, 44px tall (measured 65.6×44 at both viewports), accessible name "Remove Ridgeline 3L Shell Jacket from your order", with a visible "You can undo this." hint wired via `aria-describedby`.
- Removal is **reversible, not confirmed**: the row is replaced in place by a persistent "Removed *item*. **Undo**" strip that stays until the order is placed (no timed toast that can expire before an older shopper reacts). Focus moves to **Undo** on removal and back to **Remove** on undo.
- Both directions are announced through the **existing** `#checkout-status` polite live region (reused, not added).
- Empty state: summary count → "(0 items)", totals → $0.00, an empty-cart line with a "keep shopping" link, both Place-order buttons get `aria-disabled` + a disabled treatment, and submit is guarded with a focused error-summary message instead of placing a $0 order.
- Everything uses existing tokens/classes (`--sp-*`, `--radius-sm`, `--color-bg-muted`, `.btn--secondary`, `.hint`). No new colours, fonts, or layout changes.

**Guidance used:** `layout-states-empty-loading-error` (empty state + announce), `comp-checkout-one-page` only for "protected against double submission / trust info before payment" which was already true.
**Guidance ignored:** `cta-sticky-bar` (already implemented, not the task), `ecommerce-delivery-promise` (wrong screen for this change), `layout-hierarchy-one-thing` (no hierarchy change justified), direction `surface`/`typography` slot prose (contradicts the codebase).

**Process guidance check:** SKILL.md §2/§7 was enough — I reused `#checkout-status`, `.btn--secondary` and the token set without `impl-reuse-before-new`, and rendered/inspected without `verify-render-and-inspect`. `process_records_needed: false`.

## 6. Render and defects

Render mode: **Playwright (real HTML)**, Chromium, 1280×800 and 390×844, three states each (cart / removed / undone) — `render/first-*.png`, `render/final-*.png`. Phone shots expand the `<details>` summary first, which is the existing collapsed-on-phone behaviour.

**First render — 2 defects**
- `implementation-bug` ×1 (counted twice in the shots, one root cause): `.line-item { display: grid }` and `.removed-row { display: flex }` override the `hidden` attribute, so the "Removed … Undo" strip was visible in the resting cart and the removed line item stayed on screen after removal.
- `visual` ×1: consequence of the above — two conflicting representations of the same line visible at once.

Fix: `.line-item[hidden], .removed-row[hidden], .cart-empty[hidden] { display: none; }`. **Iterations: 1.**

**Final render — 0 defects.** Verified in the screenshots and in-page assertions: live-region text, item count, totals, and focus target after both remove and undo, at both viewports; no console/page errors.

Not a defect but worth stating: on phones the order summary is collapsed by default, so Remove/Undo sit behind that disclosure. That is the pre-existing design of this page and I did not change it.

## 7. Preservation

Navigation, theme, typography, spacing scale, component classes and the checkout flow are untouched; no structural change. `preservation: ok`, unjustified structural changes 0.

## 8. Misses by earliest layer

| layer | what |
|---|---|
| `requirements` | `intent.problem_domain` empty for a sentence that explicitly describes an accidental destructive action |
| `expected-concepts` | `a11y.live_status` (and `interaction.focus_restore`) never demanded, so `comp-toast-notification` — the record that literally says "undo where applicable, live region polite" — never entered retrieval |
| `bundle-selection` | `a11y.accessible_names` and `touch.minimum_target` had candidates and were dropped, while `cta-sticky-bar` and `ecommerce-delivery-promise` took slots |
| `project-context` | `surfaces=elevated` and `radius=pill` confidently wrong against a border-first, 4/8px-radius token system |

## 9. Regressions to propose

1. query: "The cart page: removing an item happens instantly and people do it by accident." → expect `a11y.live_status` and `feedback.confirmation_destructive` in required concepts and `comp-toast-notification` (undo + polite live region) in the bundle.
2. query: "delete a saved address from the account page with no way to get it back" → expect an undo/confirm record, not a whole-screen composite.
3. inspect `p3-ecommerce-web`: expect `radius` ≈ medium (4/8px tokens) and `surfaces` = bordered/flat, not pill/elevated — count semantic `--radius-*` tokens above raw 999px occurrences.

## 10. Tags

`concept-miss`, `ranking-miss`, `requirements-miss`, `context-detection-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`, `partial-scope-ok`
