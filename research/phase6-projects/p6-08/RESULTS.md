# p6-08 — "The products table is unusable once the warehouse has 200 SKUs."

- **Project / stack / platform**: `p6-vue-inventory` (StockRoom) — Vue 3 + Vite + Pinia + vue-router, TypeScript, plain CSS with a token file. Web.
- **Existing UI**, no new screen. Target screen: `src/views/ProductsView.vue` + `src/components/DataTable.vue`.
- **Build hash**: start and end both `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` — unchanged, nothing under `design-engineering/` was touched.
- **What the code actually did before**: `ProductsView` rendered all 200 seeded products into one `<table>` — no pagination, no sorting, no sticky header, no numeric alignment, numbers in the proportional body font, and no visible record of which filters/search are applied. Rows were mouse-only (`@click` on `<tr>`, no tabindex, no key handler).

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | `top-bar` | KNOWN | top bar **and** a 240 px left sidenav (`SideNav.vue`, 5 destinations) | partial |
| theme | `unknown` | UNKNOWN | explicit light + `[data-theme='dark']` palettes in `tokens.css` | partial |
| surfaces | `bordered-flat` | INFERRED | `.panel` = 1 px border, no elevation except one popover shadow | yes |
| radius | `small` | INFERRED | single `--radius: 6px` | yes |
| spacing | `irregular` | UNKNOWN | documented 4-pt scale `--space-1…8` (4/8/12/16/24/32) | no |
| typography | `humanist-sans` | KNOWN | IBM Plex Sans + Plex Mono, 6-step scale — but the reported feature `tabular_numerals: true` is **false**, no `font-variant-numeric` anywhere | partial (one confidently wrong feature) |
| components | `unknown` | UNKNOWN | `src/components/` has 9 reusable SFCs incl. `AppButton`, `DataTable`, `AppDialog` | partial |
| routing | `[]` | — | `src/router.ts`, 6 vue-router routes | no |
| breakpoints | `[]` | — | correct: no `@media` anywhere in the project | yes |

The `tabular_numerals: true` claim is the worst one here: the absence of tabular figures is literally part of the defect the task is about, and the inspector told the pipeline it was already handled. The critical concept was still demanded downstream, so it did no damage this time.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform_evidence | `[]`, platform `web` from project inspection | correct (sentence carries no platform word; project evidence is the right source) |
| intent.artifact_state | `existing` | correct |
| intent.operations | `diagnose`, `modify` | correct |
| intent.problem_domain | `[]` | thin — "unusable at 200 SKUs" is a data-volume/scale problem and nothing records that; the volume cue `200 SKUs` appears only as `scope_evidence.technical.DATA: ["warehouse"]` |
| intent.change_scope | `screen` | correct |
| mode + mode_evidence | `["audit","refactor"]` — "problem statement on existing UI" / "fix follows the diagnosis" | correct, matches pre-registration |
| scope.kind | `in-scope` (UI design / interaction task) | correct |
| change_budget | `moderate` | correct |
| intent.preserve | `[]`, but `constraints.preserve_existing_system: true` | acceptable |
| project_context | as above | inherits the inspect misses |
| status | CONFIDENT, `missing: []` | reasonable |

`components: ["table"]`, `product: erp`, `density: high` were all right and clearly drove the bundle.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Bundle = 4 records (core 1 + guardrails 3), OPTIONAL layer empty, ≈883 tokens, purity 0.81.

| layer | record | verdict | category |
|---|---|---|---|
| CORE | `comp-data-table` | relevant | — |
| CRITICAL | `data-tables-numeric` | relevant | — |
| CRITICAL | `grid-single-tab-stop` | relevant | — |
| CRITICAL | `layout-states-empty-loading-error` | partial | `generic` |

`comp-data-table` is a dense list that named, in order, every structural thing this screen was missing: sticky header, sort indicator with `aria-sort`, virtualised rows, pagination, keyboard grid navigation, empty state in the table body. `data-tables-numeric` is DIRECT on the numeric columns. `grid-single-tab-stop` converted "rows should be clickable by keyboard too" into a specific design (one Tab stop, arrows/Home/End, Enter activates) that I would otherwise have implemented as 50 tab stops. `layout-states-empty-loading-error` is self-labelled GENERIC and mostly restated an empty state the table already had; there is no async loading in this seeded Pinia store, so its loading/error/partial half was inapplicable.

Nothing off-platform survived: the TV/mobile records were filtered correctly.

### Concept recall

| expected id | delivered? | layer if missing |
|---|---|---|
| `data.pagination_strategy` (critical) | yes (`comp-data-table`) | — |
| `table.tabular_figures` (critical) | yes (`data-tables-numeric`, DIRECT) | — |
| `table.virtualization` | yes (`comp-data-table`) | — |
| `state.loading_empty_error` | yes (`layout-states-empty-loading-error`) | — |
| `data.filter_chips` | no | `expected-concepts` (never demanded; not in the trace at all) |
| `data.search_results` | no | `expected-concepts` (never demanded; not in the trace at all) |

**Concept recall 4/6 = 0.67 · critical recall 2/2 = 1.00.** No forbidden concept appeared.

Delivered-but-unexpected: `table.selection_bulk`, `table.inline_edit`, `interaction.selection_visible`, `interaction.keyboard_navigation`, `interaction.focus_visible`. The interaction three were genuinely useful; `table.inline_edit` and the bulk-selection column are surplus for a read-only catalogue that routes to a detail page.

Trace-reported uncovered items worth naming: `table.column_priority` was **filtered before ranking** ("platform ['mobile','tablet'] not in request ['web']"). An 8-column table at a 390 px web viewport is exactly the case that concept covers; the platform tag on its carriers is too narrow. `interaction.hover_independence` was demanded and dropped by bundle cap — also relevant, since the pre-change rows were hover/click-only.

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`, `changed: []`, validation OK, fingerprint (`top-bar` / `bordered` / `none` / `sharp` / `humanist-sans`) matches the codebase except the navigation model omitting the rail. **`unjustified_direction_slots` = 0.** The only noise is boilerplate: the navigation and typography slots print full generic prescriptions (font suggestions like "Source Sans 3, Nunito Sans…") before saying "Existing system: do not replace it for this task" — harmless but wasted lines on a fully-preserved direction.

## 5. Implementation

Files changed (originals in `before/`):

- `src/components/DataTable.vue` — added opt-in `paginated`, `pageSize`, `sort`, `rowsActivatable` props and `numeric` / `sortable` per column. Sticky `<th>`; sortable headers as `<button>` inside `<th scope="col">` with `aria-sort` and a direction glyph; right-aligned `tabular-nums lining-nums` numeric columns; pager (rows-per-page 25/50/100, Previous/Next, "Showing 51–100 of 200" in an `aria-live="polite"` region) outside the scroll region; a bounded scroll region so the header stays; roving-tabindex rows (one Tab stop, ↑/↓/Home/End, Enter/Space opens) with a focus-visible ring.
- `src/views/ProductsView.vue` — sort state + comparator (supplier sorts by resolved name; `localeCompare` with `numeric: true`), columns marked sortable/numeric, pagination and keyboard rows enabled, a specific empty-state sentence, and a row of read-only chips showing the applied category / supplier / low-stock / search filters.

Everything is opt-in, so `SuppliersView` (the other `DataTable` consumer) renders unchanged — verified in `render/final-desktop-suppliers.png`. Routes, the `?q=` param, the store, slot API, ids and the token system are untouched; no new dependency; `npm run build` clean.

**Guidance used**: all four records (see `artifacts.json`). **Ignored**: from `comp-data-table` — column resize/reorder/visibility persistence, the selection checkbox + bulk-action column, inline edit, skeleton loading (out of scope at a moderate budget for a read-only catalogue with synchronous data); virtualisation was consciously traded for pagination, which the same record also offers, because it needs no dependency. From `data-tables-numeric` — "unit in the header not each cell": `formatMoney()` prints a per-cell currency symbol across the whole app and changing that is a house convention, not this task.

**Process guidance check**: no. SKILL.md §2 (inspect and reuse first) and §7 (render and inspect) were enough — the reuse decision here was forced by the code (one shared `DataTable` with a second consumer), and I rendered and looked before claiming done. `process_records_needed: false`.

## 6. Render and defects

Render mode: **native** — `npm run build` + `vite preview` on :4173, Playwright 1.63.0 Chromium, 1280×800 and 390×844.

First render (`render/first-*.png`), 3 defects of mine + 1 inherited:

| type | defect |
|---|---|
| visual | Sticky header did not stick: `.table-wrap { overflow-x: auto }` is itself the scroll container, so at `main.content` scrollTop 500 the column headers were gone (`first-desktop-scrolled.png`). This is the guidance's "sticky header" instruction shipped broken by me — it counts against me, not the skill. |
| interaction | Clicking Next kept the outer page scrolled to the bottom, so page 2 opened mid-table with row 51 off-screen (`first-desktop-page2.png`). |
| interaction | The pager scrolled away with the content, so on a 50-row page the paging controls were only reachable by scrolling to the bottom. |
| existing-system-mismatch | At 390 px the whole shell is broken: the 240 px sidenav never collapses and the table overflows (`first-mobile.png`). **Pre-existing** — the shell CSS has no `@media` at all and I did not touch it; `first-mobile.png` and `final-mobile.png` are byte-identical. |

Fix (1 iteration): the table body became its own bounded scroll region (`max-height: min(60vh, 620px)`) with the pager lifted outside it, and page/sort changes reset that region to the top.

Final render: sticky header verified while scrolling the region (`final-desktop-region-scrolled.png`), pager always visible (`final-desktop-scrolled.png`), keyboard row focus ring after Tab + ↓↓ (`final-desktop-rowfocus.png`, active row CS-1002), sort by On hand with `aria-sort` (`final-desktop-sorted.png`, SKU header reports `aria-sort=ascending`), page 2 showing 51–100 of 200, empty state + filter chip (`final-desktop-empty.png`), row click still routes to `/products/CS-1000`. Zero console errors at both viewports.

**Final defects**: 0 of mine; 1 remaining `existing-system-mismatch` (the pre-existing mobile shell), deliberately out of scope at a moderate budget — and the one concept that would have covered the table half of it, `table.column_priority`, was filtered out of the bundle as mobile-only.

**Iterations: 1.**

## 7. Preservation

Navigation, theme, typography, spacing tokens, surfaces and the component API all preserved; component reuse rather than a new table; 0 unjustified structural changes. `preservation-ok`.

## 8. Skill effect

**helped.** `grid-single-tab-stop` produced a design I would plausibly have got wrong (per-row tab stops), and `comp-data-table` named `aria-sort` and the sticky header before I looked for them. The critical numeric guardrail landed on exactly the right columns. Nothing in the bundle caused a change I reverted.

## 9. Misses by earliest layer

1. `project-context` — `tabular_numerals: true` asserted with no supporting code (confidently wrong).
2. `project-context` — `routing: []` with `src/router.ts` present; `spacing` UNKNOWN/"irregular" against an explicit 4-pt token scale; `theme` UNKNOWN against a full dark palette; `components` UNKNOWN against 9 SFCs; navigation reported as top-bar only, ignoring the sidenav rail.
3. `expected-concepts` — `data.filter_chips` and `data.search_results` never demanded for a screen whose only narrowing is a filter bar plus a `?q=` search.
4. `candidate-compatibility` — `table.column_priority` filtered out by a mobile/tablet platform tag although narrow web viewports need it.

## 10. Regressions to propose

- Same sentence: the bundle must carry `data.pagination_strategy` **and** `table.tabular_figures`, and name an explicit sort affordance with `aria-sort`.
- Same sentence on a web project: `table.column_priority` must not be filtered out by a mobile/tablet platform tag — narrow web viewports are in its scope.
- New knowledge check: a record (or a line in `comp-data-table`) stating that `position: sticky` on `<th>` only works when the scroll container is the table's own region — an `overflow-x: auto` wrapper silently breaks it. This is the single defect the current guidance reliably produces on web tables.

## Tags

`skill-helped`, `context-detection-miss`, `concept-miss`, `render-defect-fixed`, `render-defect-remaining`, `preservation-ok`
