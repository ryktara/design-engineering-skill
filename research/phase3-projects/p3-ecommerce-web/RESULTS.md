# p3-ecommerce-web — results

## Task
"Design the product detail page and checkout for our outdoor gear web store; must convert well on phones"

## Stack / platform
Web (mobile web is the conversion target). Plain HTML + CSS (`@layer tokens/base/components/utilities`, semantic custom properties in `:root`) + one vanilla JS file (`app.js`: variant state, size-guide `<dialog>`, sticky-bar visibility, header menu, checkout validation, order-summary collapse). No framework, no CDN, no build. Files: `project/index.html`, `project/product.html`, `project/checkout.html`, `project/styles.css`, `project/app.js`, `project/img/*.svg` (local placeholder product art with intrinsic width/height).

Rendered for real with Playwright 1.63.0 Chromium (`render_mode: html`) at 1440×900 and 390×844, served over `python -m http.server`.

## Inspection verdict (`01-inspect.json`)
- **Missed: stack.** Five HTML/CSS/JS files with a `<link rel=stylesheet>` and no package.json → "no recognised UI stack; treat stack as MISSING". A plain html-css stack should be INFERRED from `.html` + `.css` + no framework markers. This miss then propagated to requirements (`stack: []`, "no repository evidence") and guidance.
- **Missed: platform.** Empty. `<meta name=viewport>`, `.html` files and `@media (max-width…)` are enough to infer `web`.
- **Missed: product hints.** Empty, although `checkout.html`, "Add to cart", "Order summary", prices and `autocomplete="postal-code"` are unambiguous e-commerce signals.
- **Missed: fonts and icons.** `--font-sans/--font-display` declarations and ~10 inline `<svg>` icons were not reported.
- **Right:** tokens (18 colour, 9 spacing, 6 type roles), breakpoints 900/720/560/901 with rule counts, "a11y attributes present in 5 files", "explicit focus handling in 1 files", css architecture ".css (1 files)".
- **Odd:** token group `--primary* (2)` — there is no `--primary` prefix; it appears to be a substring match on `--color-action-primary-hover/-active`.

## Requirements verdict (`02-requirements.json`, exit 4 AMBIGUOUS)
| field | value | verdict |
|---|---|---|
| mode | create | right |
| platform | web + mobile | **wrong** — "web store … on phones" is mobile *web*, one platform. Treating "phone" as a second platform produced status AMBIGUOUS and pulled mobile-native records (`mobile-field-use`, `icon-filled-system`, `focus-touch-only` alternative) into ranking. |
| input | keyboard, pointer, touch (INFERRED) | right |
| product | ecommerce | right |
| screen | detail, checkout | right |
| environment | outdoor | **wrong** — "outdoor gear" is a product category, not the usage environment (a shopper is on a sofa, not a ridgeline). Vocabulary gap: category noun vs. environment adjective. |
| stack | [] MISSING | **wrong** given the repo (inspection miss, see above). |
| brand | MISSING | right |
| density | null | acceptable (not stated) |
| accessibility | all six flags true | right |
| negative_constraints / constraints | empty | right |

Requirements errors: `platform-mobile-from-phone`, `environment-outdoor-from-product-category`, `stack-missing-despite-html-css`.

## Guidance verdict (`03-guidance.md`, 7 records: 3 core + 4 guardrails)
| record | verdict | note |
|---|---|---|
| `comp-wizard-stepper` (core) | partial | Checkout is one page by requirement; "one primary action", "error summary with links", "validate before submit" applied; step indicator/routes-per-step did not. |
| `dir-product-marketing-site` (core) | off-target | Its own use-when is "landing/marketing sites for software products". Selected because of lexical overlap with "product". A PDP is a transactional screen, not a marketing site. |
| `comp-form` (core) | relevant | Labels above, hints below, one column on phone, blur validation, error summary linking to fields, autofill attributes, primary action last — all implemented verbatim. |
| `layout-states-empty-loading-error` (guardrail) | partial | Error state (size not chosen, invalid fields, keep entered data) applied; empty/loading/partial have no meaning on a static PDP/checkout. |
| `mobile-field-use` (guardrail) | off-target | Sunlight/gloves/one-handed field use, triggered by the false `environment=outdoor`. |
| `a11y-keyboard-operable` (guardrail) | relevant | Drove: Escape closes size guide and returns focus, radio groups arrow-navigable, no traps. Verified in `05-interaction.json`. |
| `a11y-focus-visible` (guardrail) | relevant | "sticky UI gets scroll-padding so a focused control scrolls into clear view" — this predicted first-render defect #5 exactly (sticky bar covering focused size control). Fixed with `scroll-padding-bottom`. |

Totals: relevant 3 · partial 2 · off-target 2.

**Knowledge gaps (needed, absent from the base):**
- Product detail page pattern: variant swatches/size chips as radio groups, disabled/out-of-stock chip, low-stock messaging, "choose a size" error with `role=alert` on Add to cart, quantity stepper, price anchoring (was/save), reviews summary + histogram, size-guide dialog.
- One-page checkout pattern: order-summary placement (sticky aside on desktop, collapsed disclosure at top on phone showing the total), trust/secure header, `autocomplete` token map for address forms, shipping-option radio cards, place-order button showing the total.
- Cart-add feedback: polite live region + toast with a checkout link.
- Header collapse to a menu button on phones is in `nav-top-bar` but that record was not in the guidance bundle (see ranking misses); first render simply hid the nav.

**Ranking misses (in the base, surfaced by `search -k 12` and/or direction, but not in the guidance bundle):**
- `cta-sticky-bar` (score 0.471 in search; chosen as the direction CTA slot) — the single most task-specific record and it was left out of guidance in favour of `dir-product-marketing-site`.
- `nav-top-bar` (0.432) — would have prevented the hidden-nav defect on phone.
- `imagery-thumbnails` / `imagery-hero` — carry the width/height + CLS rule that the task demanded.
- `layout-master-detail` ranked first in search (0.495) purely because the screen keyword is "detail"; a PDP is not a master–detail layout.

## Direction verdict (`04-direction.md`, validation: OK, no violations)
| slot | choice | fit |
|---|---|---|
| navigation | `nav-wizard` | wrong for a one-page checkout; PDP uses a top bar. Alternative `nav-top-bar` (0.44) was the right one. |
| layout | `layout-master-detail` | wrong — "detail" keyword match; alternative "Single column, one task" fits the checkout, catalog/two-column fits the PDP. |
| density | `density-low` | acceptable; used the 4-px scale as the rule says. |
| surface | `surface-elevated-cards` | partial — bordered flat cards for reviews and the order summary only; the PDP itself is dividers, not cards. |
| cards | `card-poster-landscape` (16:9, "progress bar inside the art", "channel logo for live") | wrong — a TV/media card; product art is 4:5 portrait. |
| typography | `typography-humanist-sans` | fine but generic; a display serif + system sans was used for identity. |
| color | `color-monochrome-light` | partial — alternative "Neutral canvas + one accent" (0.388) is what was built (moss green action, ember accent). |
| motion | `motion-crossfade` | acceptable; minimal transitions only, reduced-motion guard. |
| focus | `focus-ring-standard` | right; one 3-px `--color-focus-ring` token, applied globally incl. hidden-radio siblings. |
| cta | `cta-sticky-bar` | right; sticky Add to cart on phone, body padding, safe-area inset, hidden while the in-page button is visible. |
| imagery | `imagery-hero` | partial — it is a gallery, but the "reserve aspect box, width/height, no lazy LCP" rule was applied. |
| icon | `icon-filled-system` | wrong (mobile-native inference); 2-px outline SVG icons used. |
| metadata | `metadata-inline-badges` | partial — "Save $60" and stock note as text, ≤2 per item. |

Validation reported OK even though wizard + master–detail + poster-landscape cards is an incoherent combination for a PDP + one-page checkout; the compatibility matrix checks pairwise slot conflicts, not fit to the screen type (`direction-invariant`). The fingerprint (`wizard / master-detail / poster-landscape / filled`) does not describe what was built.

## First-render defects (numbered)
1. Breadcrumb `<ol>` rendered list numerals ("1. Home") and stray markers overlapping the links — `ul` was reset, `ol` was not (both viewports).
2. Touch targets under 44 px on the phone: breadcrumb links 19 px tall, brand link 27 px, footer "terms" / "returns policy" links 16 px tall, skip link 40 px (measured, `05-interaction-first.json`).
3. Accent `#b8532a` on canvas `#f6f4ee` = 4.43:1 — fails AA for the small "Save $60" and low-stock text (`tokens.py contrast`).
4. Star colour `#c98a12` = 2.95:1 on white — fails 3:1 non-text.
5. Sticky Add-to-cart bar obscured the focused size control when scrolled to the end (WCAG 2.4.11) — no `scroll-padding-bottom` (measured: `focused_control_obscured_when_scrolled_to_end: true`).
6. Phone PDP hierarchy: title, price and rating were below a 448-px gallery, so the first screen showed an image and a sticky "$329 Add to cart" with no product name; a shopper had to scroll to learn what and how much.
7. Two identical Add-to-cart CTAs on screen at once on the phone when the in-page button was in view (sticky bar always shown).
8. Phone header hid the primary nav entirely (no menu button) — destinations lost below 720 px.
9. Colour legend put the selected value ("Moss") flush right, visually detached from its label.
10. Reviews section had no visible heading; the "4.6" block floated without context on desktop.
11. Phone checkout: order summary (item, totals) was at the very bottom, after Place order — the buyer filled eight fields without seeing what they were paying for.

## Iterations
- **Iteration 1** (fix pass): `ol` reset; 44-px hit areas for breadcrumb, brand, skip link, footer links (padding/negative-margin so layout is unchanged); accent → `#9a4320` (5.97:1), rating → `#8a5d05` (5.2:1); `scroll-padding-bottom: 104px` under 900 px; PDP regrouped with `grid-template-areas` so head (eyebrow/title/price/rating) precedes the gallery on phones and sits above the buy box on desktop; sticky bar hidden via IntersectionObserver while `#atc` is visible; phone menu button (`aria-expanded`/`aria-controls`, Escape closes) with a dropdown nav; legend "Colour: Moss"; visible "Customer reviews" heading with divider; checkout order summary became a `<details>` that is forced open ≥901 px and collapsed at top (`order:-1`) on phones showing the total in its summary row.
- **Iteration 2** (defects introduced by iteration 1): brand name wrapped to two lines on the phone header (menu button added width) → `white-space: nowrap`, tighter header gap, narrower menu padding; desktop order summary showed the grand total twice (summary row + Total line) → summary row hidden ≥901 px; skip link base height and "terms" link width brought to ≥44 px.
- Total: 2 fix iterations, 3 renders.

## Final defects (remaining)
1. Desktop review grid (`auto-fill, minmax(280px,1fr)`) leaves an empty right gutter with three cards at 1440 px — cosmetic.
2. Phone header keeps a search icon button with no search UI behind it (out of scope, but it is a dead control).
3. Checkout collects no payment details (deliberately deferred to a "provider frame" note) — the flow is honest about it but the page is therefore not a complete purchase.
4. Inline text links ("terms", "returns policy") reach 44 px only through padding; the visible text stays 12 px — acceptable under WCAG 2.5.8 but small.

## Interaction test summary (`05-interaction.json`, all_pass: true; first run `05-interaction-first.json`)
- Keyboard-only add to cart (1440×900): 25 Tab stops in visual order, every stop has a ≥2-px outline or box-shadow (0 without); Enter on "Add to cart" with no size → `#size-error` "Please choose a size before adding to cart." (`role=alert`), focus moved into the size radio group; ArrowRight ×2 selects M and clears the error; Enter adds → live region "Added 1 × Ridgeline 3L Shell, Moss, size M to cart.", toast visible, cart count 2. Size guide: opens with Enter, focus inside `<dialog>`, Escape closes, focus returns to the invoker.
- Keyboard-only checkout (1440×900): 21 Tab stops, all with visible focus; Enter on Place order with empty fields → `#form-summary` (`role=alert`, `tabindex=-1`) receives focus with "8 fields need your attention" and eight links; `#checkout-status` (`aria-live=polite`) announces the count; 8 `.field-error` messages, 8 `aria-invalid=true`, every invalid field's `aria-describedby` includes its error id; first summary link focuses `#email`. After typing all fields via keyboard and pressing Enter: success panel shown and focused, live region "Order placed. Confirmation sent to kai@example.com".
- Phone 390×844, both pages: cumulative layout shift 0 (PerformanceObserver); every `<img>` has width/height; 0 interactive targets under 44×44 (46 product, 34 checkout measured; hidden radio inputs measured by their label); sticky bar 72 px, bottom-aligned, body padding 88 px covers it; focused control no longer obscured when scrolled to end; `prefers-reduced-motion: reduce` collapses `.btn` transitions to 0.00001 s.

## Tokens
No `tokens.json` was authored (tokens live as CSS custom properties); `tokens.py check` not run. `tokens.py contrast` was used for 14 pairs — two failures found and fixed (defects 3, 4).

## Time spent (rough)
~45 min: project 12, skill steps 5, render/test scripts 10, inspection + two fix passes 13, write-up 5.

## Failure taxonomy tags
`requirements-miss` (phone→mobile platform; outdoor gear→outdoor environment; stack missing), `vocabulary-gap` (product-category noun read as environment; "detail" read as master–detail), `ranking-miss` (cta-sticky-bar, nav-top-bar, imagery rules not in guidance; marketing-site direction chosen as core), `knowledge-gap` (no PDP / one-page-checkout / cart-feedback patterns), `direction-invariant` (validation OK on an incoherent wizard + master–detail + poster-landscape set), `render-defect-fixed` (11 first-render defects fixed), `render-defect-remaining` (4 minor), `tooling-limit` (inspect_project does not recognise a plain html-css stack or infer web/product from HTML), `skill-helped` (comp-form, a11y-keyboard-operable, a11y-focus-visible and cta-sticky-bar guidance mapped directly onto the implementation; focus-visible's scroll-padding rule predicted a real defect; tokens.py contrast caught two AA failures).
