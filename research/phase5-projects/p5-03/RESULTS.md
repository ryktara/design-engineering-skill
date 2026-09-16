# p5-03 — "Checkout on phones: the order summary pushes the pay button below the fold."

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` (skill untouched).

## Task / project
- Codebase: `research/phase3-projects/p3-ecommerce-web/project` — Trailhead Supply storefront. Plain HTML + one CSS file (`@layer tokens/base/components/utilities`, semantic custom properties) + one vanilla `app.js`. No framework, no build.
- Platform: web (mobile web is the target). Existing UI, no new screen. Screen: `checkout.html`.
- What the code does before the change: one-page form (Contact → Shipping → Delivery → Payment) with the Place order button at the end; `<details class="order-summary">` is a sticky aside on ≥901px and is moved to the top (`order:-1`) and collapsed by JS on ≤900px. At 390×844 the page is 2007px tall (2327px with the summary open) and the pay button sits at y≈1793 / 2113 — always below the fold, further when the summary is open.

## Design-context table (`01-inspect.json`)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | sticky top bar (brand + nav/menu button; brand + "Secure checkout" on checkout) | yes |
| theme | light-first | INFERRED | `color-scheme: light`, single light palette | yes |
| surfaces | elevated ("weak signal: shadow 1, border 1") | INFERRED | bordered flat cards (1px `--color-border`, white) + dividers; shadow only on the sticky bar and the dialog | partial |
| radius | pill ("999 ×5") | INFERRED | controls use `--radius-sm` 4px / `--radius-md` 8px; 999px only on count badges, chips, tags | no |
| spacing | irregular | UNKNOWN | explicit 4px-base scale `--sp-1…--sp-12` (9 tokens, which the inspector itself listed) | partial |
| typography | geometric-sans | INFERRED | Inter/system sans for UI + Georgia serif display role for h1/brand; the display serif is missed | partial |
| components | unknown | UNKNOWN | consistent hand-rolled classes: `.btn`, `.field`, `.radio-card`, `.chip`, `.sticky-atc`, `<dialog>` | partial |

Other inspect fields: stack `html-css` KNOWN (fixed since Phase 3), platforms `["web"]` (correct), breakpoints 900/720/901/560 (correct), fonts/icons/product_hints still empty (there are `--font-*` tokens and ~10 inline SVGs; "checkout", "Add to cart", "Order summary" are unambiguous e-commerce hints). Token group `--primary* (2)` is still a substring artefact of `--color-action-primary-*`.

## Requirements verdict (`02-requirements.json`, exit 4 AMBIGUOUS)
| field | value | verdict |
|---|---|---|
| platform_evidence | `mobile` DIRECT from "phones"; conflict with project `web` recorded, "request kept" | **wrong**. A web storefront viewed on phones is mobile web; the inspector said `web` and the resolver overrode it. Same failure as Phase 3 (`platform-mobile-from-phone`). Consequence: every web-only record was filtered (`nav-top-bar`, `web-responsive-breakpoints`, `anti-hover-only-actions`, `layout-master-detail`) and mobile-native records entered (`mobile-platform-navigation`, `focus-none-touch-only`, `icon-filled-system`). |
| intent.artifact_state | existing | right |
| intent.operations | diagnose, modify | right |
| intent.problem_domain | layout, interaction, responsive | right |
| intent.change_scope | local | acceptable (evidence had both `flow: checkout` and `local: button`; "local" is fine for a one-screen fix) |
| mode + evidence | responsive (explicit "on phones"), audit, refactor | acceptable — `responsive` is in my accepted set; audit + refactor are reasonable companions |
| scope.kind / reason | in-scope, "UI design / interaction task" | right |
| change_budget | moderate | acceptable (small would also fit; the change is 3 files, ~25 lines) |
| intent.preserve | [] | partial — nothing named although `constraints.preserve_existing_system: true`; direction preserved navigation/theme/typography anyway |
| project_context | passthrough of the inspect design_context | same errors as the table above |
| status | AMBIGUOUS | caused only by the platform conflict; the sentence itself is not ambiguous |

## Guidance verdict (`03-guidance.md/json`, 6 records: 2 core + 4 guardrails, ≈878 tokens)
| record | role | verdict | BAD category | note |
|---|---|---|---|---|
| `comp-checkout-one-page` | core | relevant | — | Describes this exact page (summary collapsible-but-present at top on phones with total shown; pay button states the amount; cost transparency). Does not say what to do when the pay button is below the fold — the task's actual question. |
| `cta-single-primary` | core | partial | — | Generic. The sibling `cta-sticky-bar` (search 0.362, direction alternative 0.362) is the task-specific answer and was not in the bundle. |
| `a11y-target-size` | guardrail | relevant | — | 44/48px; bar button is 48px. |
| `layout-states-empty-loading-error` | guardrail | off-target | generic | Demanded by "asynchronous or remote data on this screen" — there is none; static checkout with local validation. |
| `mobile-safe-areas` | guardrail | relevant | — | `env(safe-area-inset-bottom)` on the bar; already the project convention. |
| `mobile-platform-navigation` | guardrail | off-target | off-platform | iOS tab bar / Android predictive back for an HTML page with a top bar. Direct consequence of the platform miss. |

Totals: relevant 3 · partial 1 · off-target 2. The omitted list was right (`comp-wizard-stepper`, `nav-wizard`, `comp-form`).

### Concept recall (expected from `00-expectation.json`)
Delivered (union over selected records): `feedback.confirmation_destructive, feedback.trust_signals, feedback.validation_errors, layout.one_primary_action, navigation.platform_grammar, state.loading_empty_error, state.saving_conflict, touch.ime_keyboard, touch.minimum_target, touch.safe_areas`.

| expected id | delivered? | layer if missing (from `concept_trace`) |
|---|---|---|
| touch.thumb_reach (critical) | no | **bundle-selection** — demanded only as *recommended* ("one-handed use"); candidate `mobile-thumb-reach` 0.321 existed, "bundle cap or lower utility left them out". For a sentence about a pay button below the fold on phones this should be *required*. |
| layout.one_primary_action (critical) | yes | — |
| adaptive.breakpoint_matrix (critical) | no | **candidate-retrieval** — required, but both carriers (`web-responsive-breakpoints` [web], `desktop-window-resizing` [desktop]) were filtered by platform=mobile before ranking. Root cause is the platform layer; the trace's `why` names only the desktop carrier. |
| touch.safe_areas | yes | — |
| feedback.trust_signals | yes | — |
| process.reuse_first | no | **expected-concepts** — never in the trace. Carrier `impl-reuse-before-new` exists (intent includes refactor) but "modify an existing artifact" does not demand it. |
| touch.minimum_target | yes | — |

Recall 4/7 = 0.57 · critical 1/3 = 0.33. Forbidden concepts: none delivered. Data note: `cta-sticky-bar` carries **no concept ids** (`[]` in `data/patterns.jsonl`), so even when selected it counts for nothing under concept coverage.

Search (`03-search.txt`, k=12): `comp-checkout-one-page` 0.75, `cta-sticky-bar` 0.362, `cta-single-primary` 0.351, `mobile-safe-areas` 0.342, `mobile-thumb-reach` 0.321 … the two records that answer the sentence (sticky bar, thumb reach) ranked 2nd and 8th and neither made the bundle.

## Direction verdict (`04-direction.md/json`)
Preserved: navigation (top-bar), surface (elevated), typography (geometric-sans), color (neutral-accent) — all justified (task is not about them). `preservation`: changed = []. Validation: **VIOLATIONS** — "non-media product: poster (media) card geometry selected" (self-reported, but the slot was still emitted).

| slot | choice | status | justified? |
|---|---|---|---|
| layout | `layout-single-column` | new | yes — its guidance line "primary action reachable without scrolling on the shortest supported viewport, **or sticky at the bottom**" is the one sentence in the whole output that addresses the task |
| density | `density-medium` | new | harmless default, unused |
| cards | `card-poster-landscape` (16:9, progress bar, channel logo) | new | **no** — no cards in a checkout fix; flagged by validation yet still output |
| motion | `motion-spring` | new | **no** — project uses 150ms `--ease` transitions; contradicts codebase; unused |
| focus | `focus-none-touch-only` | new | **no** — project has a global `:focus-visible` 3px ring system; off-platform consequence; ignored |
| cta | `cta-single-primary` | new | partial — alternative `cta-sticky-bar` (0.362) is the right value for this sentence |
| imagery | `imagery-thumbnails` | new | fine (line-item thumbnail already exists) |
| icon | `icon-filled-system` | new | **no** — project uses 2px outline SVG icons; contradicts codebase |
| metadata | `metadata-inline-badges` | new | harmless |

## Implementation
Files changed (copies in `before/`): `checkout.html` (+10 lines), `styles.css` (+3), `app.js` (+16/−3). CRLF line endings kept.
- Reused the product page's `.sticky-atc` bar as `#sticky-pay` on the checkout: total (`data-grand`, kept in sync by the existing `totals()`), a one-line meta "1 item · free shipping · tax incl." (updates when Express is chosen), and a 48px `Place order` submit button bound with `form="checkout-form"` so the existing validation / error-summary path runs unchanged.
- Same IntersectionObserver rule as the product page: bar hidden while the in-form `#place-order` is in view (never two identical CTAs on screen), `body.has-sticky` padding toggled; bar hidden and padding removed on the success state; both buttons get `aria-disabled` + "Placing order…" while submitting.
- Existing `html { scroll-padding-bottom: 104px }` (≤900px) already keeps a focused field clear of the bar (verified: `#phone` bottom 740 < bar top 772).
- Order summary stays collapsed-at-top with the total visible (matches `comp-checkout-one-page`); desktop two-column layout untouched.

Guidance used: `comp-checkout-one-page` (amount on the pay button, cost transparency → meta text), layout slot's "sticky at the bottom", `mobile-safe-areas`, `a11y-target-size`, and `cta-sticky-bar` from search/alternatives (not the bundle: bar must not obscure a focused field). Ignored: `mobile-platform-navigation` (off-platform), `focus-none-touch-only`, `icon-filled-system`, `motion-spring`, `card-poster-landscape` (contradict the codebase / irrelevant), `layout-states-empty-loading-error` (no async state here).

## Render
Mode: `html` — Playwright 1.63.0 Chromium (reused `p3-ecommerce-web/render/node_modules`), `python -m http.server`, viewports 1440×900 and 390×844 (isMobile + hasTouch). Script: `render/render.js`. Shots: `first-*` / `final-*` × {desktop, desktop-full, desktop-error, phone, phone-full, phone-summary-open, phone-midform, phone-focus-phone, phone-bottom, phone-error-from-sticky}.

First-render defects:
1. **visual** — sticky button wrapped to two lines ("Place / order") at 390px because `.sticky-atc .btn { flex:1 }` left it ~131px next to the meta text. Fixed with `.sticky-pay .btn { flex:0 0 auto; white-space:nowrap }`, meta `flex:1`, shorter meta string.

Final defects: none. Iterations: 1 (first → final).

Verified in the final render (metrics printed by `render.js`): bar visible at load on the phone (top 772, button 48px), still visible with the summary open (doc 2327px), hidden when scrolled to the in-form button, focused `#phone` not obscured, tapping the sticky button on an empty form shows and focuses the error summary; desktop unchanged (bar `display:none`, no body padding).

## Preservation
navigation ✓ · theme ✓ · typography ✓ · component reuse ✓ (`.sticky-atc`, `.btn--primary`, `data-grand`, existing observer rule) · unjustified structural changes 0 · routes / ids / aria untouched.

## Skill effect
**neutral.** Nothing in the bundle had to be un-followed in code, and the layout slot + checkout record confirm the sticky-bar fix, but the fix was pre-registered from reading the code; the task-specific records (`cta-sticky-bar`, `mobile-thumb-reach`) reached only the search list and the alternatives column, and four direction slots (cards, focus, icon, motion) contradict the codebase or the platform.

## Misses by earliest wrong layer
- **platform** — "on phones" + project `web` → `mobile`; the recorded conflict was resolved the wrong way. Cascades to `adaptive.breakpoint_matrix` filtering, `mobile-platform-navigation`, `focus-none-touch-only`, `icon-filled-system`.
- **expected-concepts** — `touch.thumb_reach` only *recommended* for a "pay button below the fold on phones" sentence; `process.reuse_first` never demanded for modify-existing.
- **bundle-selection** — `mobile-thumb-reach` (0.321) and `cta-sticky-bar` (0.362) dropped; `layout-states-empty-loading-error` kept for a screen with no async data.
- **direction** — `cta-single-primary` over `cta-sticky-bar`; `card-poster-landscape` emitted despite its own validation violation; `motion-spring` for a project with `--dur: 150ms` transitions.
- **context-detection** — radius `pill` (controls are 4/8px), spacing `UNKNOWN` despite a 9-token 4px scale, display serif missed, components UNKNOWN.
- **knowledge-gap (data)** — `cta-sticky-bar` carries no concept ids.

## Regressions to propose
1. Query: this sentence with `--project` where inspect says `platforms: ["web"]` → expect `platform: web` (mobile web), no `mobile-*` platform-standard records, `nav-top-bar` / `web-responsive-breakpoints` not filtered.
2. Query: "the pay button is below the fold on phones" (any checkout/form project) → expect `touch.thumb_reach` **required** and `cta-sticky-bar` in the core bundle.
3. Data: `cta-sticky-bar` must carry `touch.thumb_reach`, `touch.safe_areas`, `layout.one_primary_action` (and its WCAG 2.4.11 scroll-padding rule).
4. Direction: when validation reports a violation for a slot, drop the slot ("not applicable") instead of printing the violating choice; a project with `:focus-visible` rules must never receive `focus-none-touch-only`.
5. Requirements: `operations: modify` on `artifact_state: existing` → demand `process.reuse_first` (carrier `impl-reuse-before-new`).
6. Inspect: a stylesheet with `--radius-sm/--radius-md` tokens and 999px only on badges → radius `small`, not `pill`; `--sp-*` tokens on a 4px base → spacing KNOWN 4px scale.

## Tags
`platform-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `knowledge-gap`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`
