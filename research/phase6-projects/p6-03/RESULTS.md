# p6-03 — product listing filtering (p3-ecommerce-web)

**Task sentence (verbatim):** "On the product listing, shoppers cannot narrow 120 products down to what fits them."
**Project / stack / platform:** `research/phase3-projects/p3-ecommerce-web/project` · static HTML + CSS + vanilla JS (no framework) · web
**Existing UI or new screen:** existing UI (`products.html` already has category/price/feature facets, applied chips, live count, sort, URL state, empty state)
**Build hash start = end:** `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` (matches the frozen c3 hash)

## 1. Design-context table (`01-inspect.json` vs the code)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | top bar + menu-btn disclosure in every page shell | yes |
| theme | light-first | INFERRED | single light palette, no dark block | yes |
| surfaces | elevated | INFERRED | product cards are **flat tinted tiles** — no shadow, no border; the only shadows are the sticky mobile bar and the size-guide dialog | **no** |
| radius | pill | INFERRED | tokens are `--radius-sm: 4px` / `--radius-md: 8px`; `999px` is used only for chips, tags and the cart badge | partial |
| spacing | irregular | UNKNOWN | explicit 4px-based token scale `--sp-1 … --sp-12` | partial |
| typography | geometric-sans | INFERRED | Inter body **plus a Georgia display face** (`--font-display`) for h1/product titles — the pairing is missed | partial |
| components | unknown | UNKNOWN | clear vocabulary: `.chip`, `.btn`, `.product-card`, `.facet`, `.applied` | partial |

`surfaces=elevated` is the consequential one: the direction then rejected `card-flat-tile` as "incompatible with surface-elevated-cards", which is exactly what the codebase uses.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform / platform_evidence | `web`, from project inspection (no request evidence) | correct |
| intent.artifact_state | `existing` | correct |
| intent.operations | `diagnose`, `modify` | correct |
| intent.problem_domain | `responsive` | **wrong** — the only evidence is the word "narrow" (`intent_evidence.domains.responsive: ["narrow"]`), which here means *narrow a result set*, not a narrow viewport. The task is findability/filtering. |
| intent.change_scope | `unknown` | acceptable |
| mode + mode_evidence | `["responsive","audit"]` — "responsive: responsive defect", "audit: diagnose first" | **wrong** vs expected `refactor / polish / create`; a direct consequence of the `responsive` domain read |
| scope.kind / reason | `in-scope`, "UI design / interaction task" | correct (and `scope_evidence.ui` is `concept:data.filter_chips`, i.e. the concept layer read the sentence correctly while the mode layer did not) |
| change_budget | `moderate` | correct for an existing UI |
| intent.preserve | `[]`, but `constraints.preserve_existing_system: true` | acceptable |
| project_context | as in the table above | partial |

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Bundle: **1 record** (core 1, guardrails 0, optional layer absent), 122 tokens, soft cap 6 / hard cap 8.

| record | layer | verdict | category |
|---|---|---|---|
| `layout-grid-catalog` (Catalog grid) | CORE | relevant | — |
| *(bundle as a whole)* | — | — | `missing-critical`: pre-registered critical concept `a11y.live_status` is absent; there is no guardrail at all on a filtering task whose whole point is telling the shopper what changed |

`layout-grid-catalog` earned its place: it is the DIRECT carrier of `data.filter_chips` ("applied filters as removable chips with counts") and of `data.pagination_strategy`, and its "filter/sort bar that stays reachable" line matches the existing `.filters__bar`. Nothing in the bundle was off-platform, wrong-screen or contradictory.

**layer_review:** core `["layout-grid-catalog"]`, critical `[]`, optional `[]`, optional_useful 0, optional_noise 0.

### Concept recall

expected 7 · delivered 2 → **recall 0.29**; critical 2 · delivered 1 → **critical recall 0.50**

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| data.filter_chips | yes (CRITICAL, DIRECT) | — |
| data.pagination_strategy | yes | — |
| a11y.live_status | no | `expected-concepts` — never demanded; no trace entry |
| navigation.deep_link_state | no | `expected-concepts` — never demanded; no trace entry |
| state.loading_empty_error | no | `bundle-selection` — demanded (recommended), candidates `layout-states-empty-loading-error`, `comp-empty-state`, dropped |
| interaction.keyboard_navigation | no | `bundle-selection` — demanded, candidates `a11y-keyboard-operable`, `grid-single-tab-stop`, dropped |
| process.reuse_first | no | `bundle-selection` — demanded, candidate `impl-reuse-before-new`, dropped |

Five recommended concepts were demanded and then dropped into `not_surfaced` while the bundle stood at 1 record against a soft cap of 6. `coverage_ratio` for required concerns is 0.2 (`adaptive`, `interaction`, `accessibility`, `data-display` all uncovered) yet the selector still stopped at one record. That is the single biggest ranking observation in this task.

Status is `PARTIAL` (concern coverage), not `PARTIAL_SCOPE`, so there is no design/engineering split note to judge.

## 4. Direction verdict (`04-direction.md`)

All 12 filled slots `preserved`, 0 `changed`, 0 `new`, `cards` unfilled. `validation: OK`.
**`unjustified_direction_slots`: 0** — correct for an existing UI at a moderate budget.

Two defects inside preserved slots:
- **typography** is marked *preserved* but its guidance text is the create-mode text: "Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist…)". Following it would have replaced Inter + Georgia on a task that has nothing to do with type. Ignored.
- **surface / cards**: `surface-elevated-cards` and the rejection of `card-flat-tile` and `card-bordered` contradict the codebase (flat tinted tiles). Ignored. Root cause is the `01-inspect` surfaces miss, so it routes to `project-context`, not to `direction`.

## 5. Implementation

Files changed (originals copied to `before/` first):
- `products.html` — added a **Size** facet (XS–XXL) and a **Shoe size (US)** facet (8–12), both `data-facet="size"`, built from the same `.chip` / `aria-pressed` / `data-count` markup as the existing facets; added `data-sizes` to all 12 cards (tents/pads intentionally empty); updated the meta description.
- `app.js` — introduced `FACETS = ['category','size','price','feature']` so URL read/write, applied chips, counts and clear-all pick the new facet up automatically; added `listOf` / `cardHas` helpers; added the size predicate to `matches()` (OR within the facet, AND across facets); `labelOf` prefixes applied-row labels with "Size " / "US " because a bare "M" or "10" is ambiguous in the applied row.
- `styles.css` — `.facet__hint` for the in-stock note, and `align-items: center` on `.chips` (see defects).

Deep-link state, the live `role="status"` count, the empty state, the phone disclosure, sort order and the focus-restoration on chip removal all continue to work with the new facet because it was threaded through the existing machinery rather than bolted on.

**Guidance used:** `layout-grid-catalog` — removable applied chips with counts, and keeping the filter bar reachable.
**Guidance ignored:** the direction's typography slot text (would replace the type system on a filtering task) and `surface-elevated-cards` / the `card-flat-tile` rejection (contradicts the codebase).

**Not implemented:** a load-more / pagination strategy for the "120 products" in the sentence. The catalog is 12 static cards; adding pagination to 12 cards would be a change the code does not justify. `data.pagination_strategy` was delivered by the bundle and deliberately not acted on.

**Process guidance check:** SKILL.md §2 and §7 were enough — reuse-before-new and render-and-inspect were both applied without `impl-reuse-before-new`, `impl-safe-modification` or `verify-render-and-inspect` in the bundle. `process_records_needed: false`.

## 6. Render and defects

Render mode: **Playwright (real browser, Chromium)**, `products.html` over `file://`, viewports 1280×800 and 390×844, each captured at rest and after selecting Size M + US 10. Screenshots inspected visually, not just captured.

First render (`render/first-*.png`), behaviour verified: count "9 of 12 products", URL `?size=M,us10`, applied row "Size M ✕ / US 10 ✕ / Clear all", no page errors at either viewport.

| type | first | final |
|---|---|---|
| visual | 1 | 0 |
| interaction | 0 | 0 |
| accessibility | 0 | 0 |
| platform | 0 | 0 |
| existing-system-mismatch | 0 | 0 |
| implementation-bug | 0 | 0 |

**Iterations: 1.**

The one defect: on desktop the five shoe-size chips measured 77–82 × **70px** against 44px for every other chip, rendering as circles. Cause: `.chips` is a flex row with default `align-items: stretch`, and the `.facet__hint` paragraph I added made the Size fieldset taller, stretching the adjacent grid cell's chips. Fix: `align-items: center` on `.chips` (all chip rows were already 44px, so nothing else moved). Re-measured after the fix: every chip 44px. The guidance did not warn about this, and nothing in the bundle would have.

## 7. Preservation verdict

Navigation, theme, typography, spacing tokens, chip/card components, routes, ids, `role="status"` count, URL state and the empty state are all intact; the new facet reuses existing classes and adds one CSS declaration plus one hint class. **preservation: ok**, 0 unjustified structural changes.

## 8. Skill misses routed to the earliest wrong layer

| layer | miss |
|---|---|
| `requirements` | `problem_domain` read "narrow" as a viewport cue → `responsive`; the sentence means narrowing a result set. This propagates into the mode. |
| `expected-concepts` | `a11y.live_status` (critical) and `navigation.deep_link_state` were never demanded for a filtering task. |
| `bundle-selection` | `state.loading_empty_error`, `interaction.keyboard_navigation`, `process.reuse_first` demanded with live candidates, dropped at bundle size 1 of soft cap 6. |
| `project-context` | `surfaces=elevated` is wrong (flat tinted tiles); `radius=pill` and `spacing=UNKNOWN` misread an explicit token scale; the Georgia display face is missed. |
| `direction` | the typography slot is marked *preserved* but carries create-mode "choose a new typeface" text. |

## 9. Regressions to propose

1. *Query:* "On the product listing, shoppers cannot narrow 120 products down to what fits them." — *Expect:* mode contains `refactor` or `polish` and not `responsive`; "narrow N products" must not count as a viewport cue.
2. *Query:* same. — *Expect:* the bundle demands `a11y.live_status` and `navigation.deep_link_state` for a filter/facet task, and carries at least one guardrail (result-count live region, keyboard operability) rather than an empty guardrail layer.
3. *Query:* same. — *Expect:* when required-concern coverage is 0.2 and five recommended concepts have live candidates, the bundle does not stop at 1 record against a soft cap of 6.
4. *Project-context regression:* `p3-ecommerce-web` — *Expect:* `surfaces` resolves to flat/tinted, not `elevated`, and `spacing` resolves to a 4px token scale rather than `irregular`/UNKNOWN.

## 10. Tags

`requirements-miss`, `mode-miss`, `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`
