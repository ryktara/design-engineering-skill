# p4-06 — product listing page with filters (Trailhead Supply)

**Task:** "add a product listing page with filters to our outdoor gear web store, matching the existing product and checkout pages"
**Project / stack / platform:** `phase3-projects/p3-ecommerce-web/project` · plain HTML/CSS (`@layer tokens, base, components, utilities`, semantic `--color-*` / `--sp-*` / `--fs-*` tokens) + one vanilla JS IIFE · web
**Existing UI:** yes — existing project, **new page** (`products.html`); PDP, checkout and a 4-product index existed
**Render mode:** html (static files over `python -m http.server`, Playwright Chromium 1440×900 and 390×844 with touch emulation; states default / filtered / empty / phone sheet / focus)

## 1. Design context (inspect) — detected vs actual

| field | detected | status | actual (`styles.css`, `product.html`, `checkout.html`) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | sticky white top bar, brand + 4 category links + cart; collapses to a "Menu" button ≤720 px; checkout has a reduced header | yes |
| theme | light-first | INFERRED | `color-scheme: light`, warm canvas `#f6f4ee`, white surfaces | yes |
| surfaces | elevated ("shadow 1, border 1") | INFERRED | bordered-flat: cards/inputs/order summary use 1 px `--color-border`; the only shadows are the sticky add-to-cart bar and the dialog | **no** |
| radius | pill ("most common radius 50 (3×)") | INFERRED | `--radius-sm: 4px` / `--radius-md: 8px` on every container and button; `50%` only on colour swatches and step circles, 999 px on the cart count | **no** — counted `50%` occurrences as the radius language |
| spacing | irregular ("most used [4, 14]") | UNKNOWN | rem-based 4 px scale `--sp-1…--sp-12` (0.25–3 rem) used throughout; the `14px 8px` is one hit-area hack | **no** — rem values are not parsed, only px |
| typography | unknown | UNKNOWN | `--font-sans: "Inter", "Segoe UI", …` body and `--font-display: Georgia` for h1/brand/prices, `--fs-*` scale, `--lh-*` | no |
| components | unknown | UNKNOWN | `.btn--primary/--secondary/--block`, `.icon-btn`, `.size` toggle labels, `.swatch`, `.field`, `.radio-card`, `.product-card`, `.breadcrumb`, `.sticky-atc`, `.toast` | no |
| product_hints | [] | — | e-commerce (cart, checkout, price, reviews) | no (the requirements step got `ecommerce` from the request instead) |

Only navigation and theme are right; three of the five INFERRED/UNKNOWN fields are wrong in a way that would mislead a direction (surfaces "elevated", radius "pill").

## 2. Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)

| field | value | verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope | right |
| mode | create (default) | right |
| platform / stack | web (request), html-css (project) | right |
| product | ecommerce (product listing, checkout, web store) | right |
| screen | [checkout, list] | **partial** — "checkout" is named as a page to *match*, not to build; `primary_jobs` then contains "create checkout", and `comp-checkout-one-page` enters the bundle as a core record |
| components | [search] | wrong — "filters" mapped to search; no filter/chip/product-tile component |
| jobs | [] | miss — browse, filter, compare |
| density | null | fine |
| risk / change_budget | medium / moderate | fine |
| intent | existing: true (our, existing); preserve: [] | preserve should be non-empty from "matching the existing … pages" |
| constraints | preserve_existing_system: true | right |
| missing | brand | fine |

## 3. Guidance verdict (`03-guidance.md`, bundle 7 = core 3 + guardrails 4; concepts 7/7, ≈1031 tokens, coverage/1k 6.79, purity 0.84; uncovered required concerns none)

| record | role | verdict | note |
|---|---|---|---|
| comp-filters | core | relevant | chips for applied filters, counts, clear all, count updates, mobile filter button with badge + sheet, URL persistence — followed almost line by line |
| comp-checkout-one-page | core | off-target | checkout is not in scope (screen misread) |
| dir-utility-commerce | core | partial | "identity via tile geometry, price typography, and the filter chip language" applied; "search dominates the header" not applied (no search in the store) |
| a11y-keyboard-operable | guardrail | relevant | native `<button aria-pressed>` chips, no custom key handling |
| search-filter-feedback | guardrail | relevant | result count announced, removable chips, empty results suggest next steps, URL state |
| a11y-focus-visible | guardrail | relevant | site's 3 px ring on every stop |
| layout-states-empty-loading-error | guardrail | relevant | empty state: what, why, one action |

Relevant 5 · partial 1 · off-target 1.

Missing guidance:
- `a11y-target-size` (≥44 px on touch) — in the base, appears only at `--size 12`; the interaction test's phone requirement. **Layer: bundle-selection (ranking-miss).**
- `layout-grid-catalog` — search rank 2 and chosen for the direction's layout slot, but not in the guidance bundle (auto-fill/minmax, consistent aspect, reserved image boxes, "filter/sort bar stays reachable"). **Layer: bundle-selection.**
- A product tile / card record — `comp-product-detail-page` exists, a listing tile does not (price + deciding fact, sale badge, whole tile as one link, image aspect). **Layer: expected-concepts (knowledge-gap).**
- Sort control — no bundled record mentions sorting; `comp-filters` covers filters only. **Layer: expected-concepts (knowledge-gap).**

## 4. Direction verdict (`04-direction.md`, **validation: VIOLATIONS** — "non-media product: poster (media) card geometry selected"; exit 3; budget moderate; preserved [navigation, surface, color])

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-top-bar (preserve) | preserved | yes |
| layout | layout-grid-catalog | new | yes |
| density | density-low | new | partial — a spacious catalog is fine; the store's controls are 44–48 px and its checkout is medium; not a change I made |
| surface | surface-elevated-cards (preserve) | preserved | wrong detection, but the preserve flag meant nothing was changed; I kept the bordered-flat cards the index already uses |
| cards | card-poster-landscape (16:9, progress bar, channel logo) | new | **no** — TV media card for a gear store; validation caught it |
| typography | typography-humanist-sans | new | not wrong, but the project already has Inter + Georgia display; "new" only because typography was undetected |
| color | color-neutral-accent (preserve) | preserved | yes |
| motion | motion-crossfade (shared element) | new | no — nothing in the store animates beyond 150 ms colour; ignored |
| focus | focus-ring-standard | new | yes (existing 3 px ring) |
| cta | cta-sticky-bar | new | no — belongs to the PDP (already there); a listing has no single action |
| imagery | imagery-hero | new | no — a hero on a listing page pushes the filters and grid down; ignored |
| icon | icon-outline-system | new | yes (matches the existing stroke icons) |
| metadata | metadata-inline-badges ("pill only for status/category; text inside; ≤2 per item") | new | yes — used for the Sale tag |

Preserved 3 by repository evidence (one of them on a wrong detection). Four "new" slots (cards, motion, cta, imagery) contradict the existing store; validation flagged one. As instructed, a direction with violations was not used as-is.

## 5. Implementation (files; originals in `before/`)

- `products.html` (new) — same header/skip link/breadcrumb markup as the PDP; page head (Georgia h1 + muted line, like the hero/PDP); `<form class="filters">` with three facets as native `<button aria-pressed>` chips (Category ×4 with counts, Price ×3 single-select, Features ×3 with counts) inside a `<details class="facets">` that is always open on wide screens and a "Filters (n)" disclosure on phones; filter bar with `role=status aria-live=polite` result count, applied chips (`aria-label="Remove filter X"`) + "Clear all" link-button, sort `<select>`; 12 products as the existing `.product-card` (image 4:5, name, price + was-price, rating) with a Sale tag; empty state with one action.
- `app.js` — listing block in the same IIFE style: URL ↔ state (`?category=…&price=…&feature=…&sort=…` via `replaceState`), show/hide + DOM reorder for sort (visual = Tab order), chip counts ("how many if I add this"), applied chips, title/breadcrumb/document.title/nav `aria-current` follow a single category, focus management after remove/clear, phone disclosure sync (same rule as the checkout order summary).
- `styles.css` — `/* ---- product listing ---- */` block in `@layer components` using existing tokens: `.plp*`, `.filters`, `.facets*`, `.chip` (44 px, pill, pressed = text-primary fill + white + ✓ with reserved width), `.filters__bar`, `.sort`, `.tag` (accent pill), `.plp-empty`, phone rules ≤720 px (2-column grid, collapsed facets with badge).
- `index.html`, `product.html` — nav links now point at `products.html?category=…` (previously `#anchors`); breadcrumb "Jackets" on the PDP links to the listing. No other change.

## 6. First-render defects (`render/first-*.png`, `05-interaction-first.json` 7/8 at both viewports)

| type | defect |
|---|---|
| visual | a pressed chip grew by the width of its "✓" prefix and nudged the neighbouring chips |
| (harness) | the failing check was a test bug — it counted "Clear all" as an applied chip; removal and focus handling worked as designed |

No accessibility, interaction, platform or existing-system-mismatch defects: 44 px targets on the phone, 3 px ring on all 23 desktop / 15 phone stops, header/nav/fonts/canvas identical to the PDP.

## 7. Final defects (`render/final-*.png`, `05-interaction-final.json` 8/8 at both viewports)

| type | defect |
|---|---|
| visual (remaining, inherited) | on the phone's 2-column grid a two-line product name ("Ridgeline 3L Shell Jacket") pushes its price row lower than the neighbouring card's — the existing `.product-card` behaves the same on `index.html` |

Unverified: loading state (static data, so none designed beyond `loading="lazy"` with reserved 4:5 boxes), screen-reader pass, 200 % zoom, 768 px tablet width.

## 8. Iterations
1. first — page + logic (7/8; one harness bug).
2. final — chip reserves the check-mark width (`::before` hidden, `visibility` toggled) so width never changes; test counts only `[data-remove]` chips (8/8).

## 9. Interaction test summary (final)
**1440×900:** first chip reached in 9 Tabs (skip link → brand → 4 nav → cart → Home → Jackets); Space sets `aria-pressed=true`, Enter back to false; count "12 products" → "3 of 12 products" (role=status, aria-live=polite) → "12 products" after removing; URL `?category=jackets` → empty; applied chip "Remove filter Jackets" reached and activated by keyboard, focus lands on the count (tabindex -1) since no applied chip remains; 23 Tab stops, ring on every one; 21 controls checked, none < 24 px; empty state visible with one action, catalog hidden, "0 of 12 products", Clear restores 12 and focuses the first chip; nav = Jackets,Packs,Footwear,Camp with `aria-current` on the filtered category, canvas `rgb(246,244,238)`, Inter body, Georgia h1, one h1, breadcrumb follows the category, chips 44 px / 999 px, 5-column catalog.
**390×844 (touch):** same results; facets open via the "Filters" disclosure; 15 stops with ring; 19 controls checked, **none under 44×44**; 2-column catalog.

## 10. Preservation verdict
Header, navigation, breadcrumb, tokens, type pairing (Inter + Georgia display), 44 px control height, 4/8 px radii, bordered-flat surfaces and the `.product-card` were all reused; the chip is the one new primitive and it is built from the same tokens as `.size`. Structural change to existing pages: nav `href`s only — justified (the listing is now the category destination). Unjustified structural changes: 0. The direction's poster cards, hero, sticky bar and crossfade were not followed.

## 11. Regressions to propose
- query "add a product listing page with filters to our outdoor gear web store, matching the existing product and checkout pages" → expect `screen=[list]` only (checkout is a reference), `components` ⊇ {filters, product card}, `intent.preserve` non-empty; bundle has `comp-filters`, `layout-grid-catalog`, `search-filter-feedback`, `a11y-target-size`; no `comp-checkout-one-page`.
- direction for product=ecommerce, screen=list → expect cards not `card-poster-landscape` (validation already flags it; the selector should not pick it), imagery not hero, cta not sticky-bar.
- inspect on a stylesheet with rem spacing tokens and `50%` swatches → expect spacing = 4 (rem parsed), radius small, surfaces bordered-flat when shadows appear only on sticky/dialog rules, typography KNOWN from `--font-*`.

## 12. Tags
`requirements-miss` (checkout as screen, components=search, jobs empty, preserve empty) · `ranking-miss` (a11y-target-size, layout-grid-catalog) · `knowledge-gap` (product listing tile, sort control) · `context-detection-miss` (surfaces, radius, spacing, typography, components) · `direction-mismatch` (poster cards, hero, sticky bar, crossfade) · `render-defect-fixed` · `render-defect-remaining` · `skill-helped` (comp-filters + search-filter-feedback + empty-state guardrail drove the page; validation caught the media card) · `preservation-ok`
