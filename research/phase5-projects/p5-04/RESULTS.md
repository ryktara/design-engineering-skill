# p5-04 — "The product page never tells shoppers when it will arrive or that returns are free."

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` (skill untouched).

## Task / project
- Codebase: `research/phase3-projects/p3-ecommerce-web/project` — Trailhead Supply storefront. Plain HTML + one CSS file (`@layer tokens/base/components/utilities`, semantic custom properties, 4px spacing scale) + one vanilla `app.js`. No framework, no build. `checkout.html` (changed by p5-03) not touched — md5 unchanged.
- Platform: web. Existing UI, no new screen. Screen: `product.html` (PDP).
- What the code did before: a `.trust` list under the Add-to-cart row said "Free shipping over $99 · arrives in 2–4 days" and "60-day returns, no questions asked"; the stock note said "ships today if ordered by 2 pm" only after a size was chosen; the collapsed "Shipping & returns" accordion said "Returns accepted within 60 days in original condition". So: a relative range, never a date; a 60-day window, never the word free; the cut-off hidden until a size is picked; on phones all of it below the fold (the trust list sat at y≈1284 of an 844px viewport).

## Design-context table (`01-inspect.json`; identical output to p5-03 — same project)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | sticky top bar + breadcrumb | yes |
| theme | light-first | INFERRED | `color-scheme: light`, one light palette | yes |
| surfaces | elevated ("weak signal: shadow 1, border 1") | INFERRED | bordered flat cards + dividers; shadow only on sticky bar and dialog | partial |
| radius | pill (999 ×5) | INFERRED | controls 4px / 8px tokens; 999 only on badges/bars | no |
| spacing | irregular | UNKNOWN | explicit `--sp-1…--sp-12` 4px scale (the inspector lists the 9 tokens itself) | partial |
| typography | geometric-sans | INFERRED | Inter/system sans + Georgia display role (h1, brand) — display serif missed | partial |
| components | unknown | UNKNOWN | consistent `.btn`, `.trust`, `.option-group`, `.sticky-atc`, `<details>`, `<dialog>` | partial |

`icons: []` although the page has ~12 inline 2px-outline SVGs; this later feeds the wrong `icon-text-only` direction slot. `product_hints: []` despite "Add to cart", "checkout", "Size guide".

## Requirements verdict (`02-requirements.json`, status CONFIDENT)
| field | value | verdict |
|---|---|---|
| platform_evidence | `[]`; platform `web` from project inspection | correct (no "phone" trigger this time, so no override) |
| intent.artifact_state | existing | right |
| intent.operations | diagnose, modify | right |
| intent.problem_domain | `[]` | **miss** — the sentence is about content/feedback (trust information); nothing detected |
| intent.change_scope | screen | right |
| mode + evidence | audit ("problem statement on existing UI"), refactor ("fix follows the diagnosis") | acceptable — `refactor` is in my accepted set; `audit` is weak (the sentence already names the defect, no review is needed) but harmless |
| scope.kind / reason | in-scope, "UI design / interaction task" | right |
| change_budget | moderate | acceptable (actual change: 3 files, ~30 lines; `small` would fit) |
| intent.preserve | `[]` | partial — nothing named although `preserve_existing_system: true` |
| product / screen | ecommerce / detail | right (from "product page") |
| project_context | passthrough of the inspect table | same errors as above |

## Guidance verdict (`03-guidance.md/json`, 6 records: 2 core + 4 guardrails, ≈909 tokens)
| record | role | verdict | BAD category | note |
|---|---|---|---|---|
| `comp-product-detail-page` | core | relevant | — | "shipping, returns and stock are stated next to the price, not in a tab" is the one line that answers the task's *where*. It says nothing about the *what*: an arrival date rather than a range, a cut-off, or stating that returns are free. |
| `imagery-thumbnails` | core | off-target | generic | Chosen as "highest-scoring pattern with lexical evidence" (0.251) for a sentence with no imagery content. Second core slot wasted. |
| `a11y-keyboard-operable` | guardrail | partial | — | Standing web guardrail; nothing interactive is added by this task. |
| `a11y-focus-visible` | guardrail | partial | — | Same; the scroll-padding rule it names is already in the project. |
| `layout-states-empty-loading-error` | guardrail | off-target | generic | Demanded for "asynchronous or remote data on this screen" — there is none (static page, local state). Same false demand as p5-03. |
| `web-responsive-breakpoints` | guardrail | relevant | — | Used: verified at 1440 and 390 that the promise fits on one line at the narrow width. |

Totals: relevant 2 · partial 2 · off-target 2. Omitted list (`dir-product-marketing-site`, `chart-heatmap-matrix`) was right. Platform filter was right (`web` only).

### Concept recall (expected from `00-expectation.json`)
Delivered (union over the 6 records): `a11y.accessible_names, adaptive.breakpoint_matrix, adaptive.navigation_transform, feedback.trust_signals, interaction.focus_visible, interaction.hover_independence, interaction.keyboard_navigation, layout.one_primary_action, perf.layout_shift, state.loading_empty_error, touch.minimum_target`.

| expected id | delivered? | layer if missing (from `concept_trace`) |
|---|---|---|
| feedback.trust_signals (critical) | yes (via `comp-product-detail-page`) | — |
| layout.focal_hierarchy | no | **expected-concepts** — never in the trace. Carriers exist (`layout-hierarchy-one-thing`, `typo-measure-and-rhythm`). The task is about putting decision-critical information where the decision is made. |
| layout.one_primary_action | yes | — |
| process.reuse_first | no | **bundle-selection** — recommended ("existing repository: reuse its primitives"), candidate `impl-reuse-before-new` 0.238, "bundle cap or lower utility left them out". Cap was 6 and one core slot went to `imagery-thumbnails`. |
| a11y.semantics | no | **expected-concepts** — never demanded; carrier `a11y-semantics-structure` [web] exists. (Relevant here: `<ul aria-label>`, `<time datetime>`, no live region for a once-a-minute countdown.) |

Recall 2/5 = 0.40 · critical 1/1 = 1.00. Forbidden concepts delivered: none.

Search (`03-search.txt`, k=12): `comp-product-detail-page` 0.609, then `grid-single-tab-stop` 0.401, `imagery-thumbnails` 0.395, `nav-orientation-and-back`, `a11y-color-not-only`, `cta-single-primary`, `comp-photo-capture-field` 0.325, `a11y-modal-dialog`, `layout-rails` (TV)… Nothing in the base speaks to a delivery promise (cut-off, business-day arrival window, countdown) or to stating return *cost*; the checkout record carries "cost transparency" but is not retrieved for a PDP sentence. **Knowledge gap**: no delivery-estimate / shipping-promise pattern record.

## Direction verdict (`04-direction.md/json`, exit 3 = validation VIOLATIONS)
Preserved: navigation (top-bar), surface (elevated), typography (geometric-sans), color (neutral-accent) — all justified; `preservation.changed = []`. Validation: "non-media product: poster (media) card geometry selected" — reported, slot still emitted (same as p5-03).

| slot | choice | status | justified? |
|---|---|---|---|
| layout | `layout-grid-catalog` | new | **no** — requirements say `screen: detail`; a catalog grid contradicts the page (two-column PDP grid). Alternative `layout-single-column` 0.312 would at least be harmless. |
| density | `density-medium` | new | harmless default, unused |
| cards | `card-poster-landscape` | new | **no** — no cards; its own validation flags it |
| motion | `motion-crossfade` (View Transitions, 250–350ms) | new | unused; project has 150ms `--dur` transitions only |
| focus | `focus-ring-standard` | new | yes — matches the project's global 3px `:focus-visible` ring (better than p5-03's `focus-none-touch-only`, which the mobile override had caused) |
| cta | `cta-single-primary` | new | yes — Add to cart stays the single filled button; the promise adds no CTA |
| imagery | `imagery-thumbnails` | new | fine, irrelevant to the task |
| icon | `icon-text-only` ("words for everything") | new | **no** — contradicts the codebase (inline 2px outline SVGs in the header, trust list, dialog). Alternative "Outline icon set, one weight" 0.384 is the actual system. Root cause: inspect `icons: []`. |
| metadata | `metadata-inline-badges` | new | harmless |

## Implementation
Files changed (copies in `before/`; CRLF kept): `product.html` (+13/−5 lines), `styles.css` (+7), `app.js` (+35/−2).
- **Delivery promise next to the price** (`<ul class="delivery" id="delivery" aria-label="Delivery and returns">` in `.pdp-head`, under the rating): "**Free delivery** Fri, Sep 11 – Tue, Sep 15" (`<time datetime>` × 2, fallback "in 2–4 business days" without JS) and "**Free 60-day returns** · prepaid label". On phones `.pdp-head` is first in the grid, so the promise sits at y≈295 — above the fold; on desktop it is in the right column between rating and colour swatches.
- **Cut-off countdown in the trust list** (`#cutoff-note`, replacing "Free shipping over $99 · arrives in 2–4 days"): "Order within 3 h 12 min and it ships today" before 2 pm on a business day, "Order now and it ships Thu, Sep 10" after it / at weekends. Recomputed every 60 s; deliberately **no live region** (not a response to user input; a once-a-minute announcement would be noise). Second trust line now "Free returns within 60 days — prepaid label, no questions asked".
- `app.js`: `shippingWindow()` (2 pm local cut-off, Mon–Fri, dispatch +2…+4 business days, `Intl.DateTimeFormat en-US`), `renderDelivery()`, `setInterval` 60 s. Stock note simplified to "In stock" / "Only N left in M" (dispatch timing now lives in `#cutoff-note`, visible without choosing a size).
- Accordion copy: same-day-dispatch rule + an explicit free-returns paragraph (prepaid label, refund to original payment within 5 days of receipt).
- CSS: `.delivery` reuses the `.trust` row grammar (18px outline icon + `--fs-sm` secondary text, `--sp-1/--sp-2` gaps, `min-height: 1.5em` so the JS fill cannot shift layout, `tabular-nums` on the dates). One new outline glyph (truck) drawn in the existing 2px stroke style. No new colour, font, or component.

Guidance used: `comp-product-detail-page` ("next to the price, not in a tab" → placement in `.pdp-head`; "sticky add-to-cart … one add-to-cart action" → no extra CTA), `web-responsive-breakpoints` (checked 390 and 1440), `cta-single-primary` (direction). Ignored: `imagery-thumbnails` (nothing to apply), `layout-states-empty-loading-error` (no async data), `layout-grid-catalog`, `card-poster-landscape`, `motion-crossfade`, `icon-text-only` (contradict the page/codebase). The content decisions — an arrival *date window* computed from a cut-off, a countdown, "free" stated for returns, the accordion made consistent — came from the pre-registered expectation, not from the skill.

## Render
Mode: `html` — Playwright 1.63.0 Chromium (reused `p3-ecommerce-web/render/node_modules`), `python -m http.server`, viewports 1440×900 and 390×844 (isMobile + hasTouch). Clock fixed with `page.clock.setFixedTime` at Wed 2026-09-09 10:48 (`pre` cut-off) and 16:45 (`post`). Script: `render/render.js`. Shots: `first-*` / `final-*` × {desktop-pre, desktop-pre-full, desktop-post, phone-pre, phone-pre-full, phone-pre-buybox, phone-post, phone-post-buybox}.

First-render defects:
1. **visual** — duplicated copy: with a size chosen, the stock note said "In stock — ships today if ordered by 2 pm" 60px above the new "Order within 3 h 12 min and it ships today" line. Fixed by reducing the stock note to "In stock" (dispatch timing has one home, visible without a size).

Final defects: none. Iterations: 1.

Verified in the final render (`render.js` metrics): promise at y=295 on the phone (above the fold), y=309 on desktop; dates correct on both sides of the cut-off (pre: ships Wed 9 → Fri 11 – Tue 15; post: ships Thu 10 → Mon 14 – Wed 16); `datetime` attributes ISO; countdown text "3 h 12 min" at 10:48; no wrap at 390px; Add to cart unchanged (y 605 desktop / 1207 phone, sticky bar still the only phone CTA).

## Preservation
navigation ✓ · theme ✓ · typography ✓ · component reuse ✓ (`.trust` grammar, tokens, outline icons, `<details>` accordion) · unjustified structural changes 0 · routes / ids / aria / checkout untouched.

## Skill effect
**neutral.** The PDP record confirmed the placement ("next to the price, not in a tab") that the expectation already held, and nothing in the bundle had to be un-followed in code; but the substance of the task — a date instead of a range, a cut-off countdown, saying "free" — is not in any record, one core slot went to thumbnails, and four direction slots (layout, cards, motion, icon) contradict the page.

## Misses by earliest wrong layer
- **requirements** — `problem_domain: []` for a content/feedback sentence; `preserve: []`.
- **expected-concepts** — `layout.focal_hierarchy` and `a11y.semantics` never demanded; `state.loading_empty_error` demanded on a false premise ("asynchronous or remote data").
- **bundle-selection** — `impl-reuse-before-new` dropped while `imagery-thumbnails` (0.251 lexical) took a core slot.
- **knowledge-gap** — no record for a delivery promise / arrival estimate / return-cost statement; `comp-product-detail-page` covers placement only.
- **direction** — `layout-grid-catalog` for `screen: detail`; `card-poster-landscape` despite its own violation; `icon-text-only` against a codebase full of outline SVGs.
- **context-detection** — `icons: []` (root of the icon slot miss); radius `pill`; spacing `UNKNOWN`; display serif missed; components UNKNOWN.

## Regressions to propose
1. Query: this sentence with the project → expect `layout.focal_hierarchy` demanded (decision-critical information placed where the decision is made) and `imagery-thumbnails` absent from core.
2. Query: any PDP/detail sentence on a static HTML project → `state.loading_empty_error` must not be *required* without evidence of async data.
3. Data: add a `comp-delivery-promise` (or extend `comp-product-detail-page`) carrying `feedback.trust_signals`: arrival as a date window computed from a stated cut-off, cut-off countdown, shipping and return *cost* stated in words, no live region for periodic recomputation.
4. Direction: `screen: detail` must never resolve `layout-grid-catalog`; a validation violation must drop the slot rather than print it.
5. Inspect: detect inline `<svg stroke="currentColor">` icon usage so `icons` is not empty and `icon-text-only` cannot be chosen.
6. Requirements: `operations: modify` on `artifact_state: existing` → demand `process.reuse_first` (same as p5-03).

Tags: `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`.
