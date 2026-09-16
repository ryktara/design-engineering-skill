# p6-10 — "Make the dashboard tell the manager which items need reordering today."

- **Project / stack / platform**: `p6-vue-inventory` (StockRoom) · Vue 3 + Vite + Pinia + vue-router, plain CSS with a token file · web.
- **Existing UI**: yes (DashboardView already had 4 KPI tiles + "Needs reordering" list). New screen: no.
- **Build hash start / end**: `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` — identical at both ends, matches candidate c3.
- **Concurrency rule honoured**: only `src/views/DashboardView.vue` and `src/components/KpiTile.vue` touched. The store, products table and adjustment form were not modified.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | top bar **plus** a persistent 240 px left sidenav (`SideNav.vue`, 5 destinations, active indicator) | partial |
| theme | unknown | UNKNOWN | explicit light palette + `[data-theme='dark']` block in `tokens.css` | partial |
| surfaces | bordered-flat | INFERRED | `.panel` = white surface, 1 px border, `--radius: 6px`, one popover shadow | yes |
| radius | small | INFERRED | single `--radius: 6px` token | yes |
| spacing | irregular | UNKNOWN | strict 4-pt scale `--space-1..8` (4/8/12/16/24/32) — the evidence line even shows 4/8-multiples | no (confident wrong value) |
| typography | humanist-sans | KNOWN | IBM Plex Sans + IBM Plex Mono, 6-step scale, tabular numerals | yes |
| components | unknown | UNKNOWN | 9-component library in `src/components/` (KpiTile, DataTable, StatusBadge, AppDialog…) — the same JSON reports `component_dirs: src/components/ (9 files)` | partial |
| routing | `[]` | — | vue-router 4 with 6 routes (`router.ts`) | no |

Tag: `context-detection-miss` (spacing wrong, theme/components/routing under-detected despite unambiguous code).

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform_evidence | `[]`, platform `web` from project inspection | correct (project-derived) |
| intent.artifact_state | existing | correct |
| intent.operations | `modify` | correct |
| intent.problem_domain | `[]` | acceptable — the sentence names no defect facet, but "tell … which items need reordering" is an information-design problem; an empty domain is why no data-density concept was demanded |
| intent.change_scope | screen | correct |
| mode / mode_evidence | `refactor` ("modification of existing UI: make") | acceptable (expectation allowed refactor/polish/create) |
| scope.kind | in-scope, "UI design / interaction task" | correct |
| change_budget | moderate | correct |
| intent.preserve | `[]` | acceptable; direction preserved everything anyway |
| project_context | carried through inspect verbatim, including the wrong `spacing=irregular` | inherits the context-detection miss |
| screen | `dashboard` | correct |
| status | CONFIDENT | correct |

No `requirements-miss`.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

Status `PARTIAL` (exit code 3), bundle = 3 core + 4 guardrails + 1 optional, ≈989 tokens.

| layer | record | verdict | category |
|---|---|---|---|
| CORE | `comp-chart-container` | off-target | `wrong-screen` — the dashboard has no chart and the task does not call for one; it was picked as the carrier for `a11y.color_not_only` and `state.loading_empty_error` |
| CORE | `layout-dashboard-grid` | relevant | — (module sizing by importance; used) |
| CORE | `chart-relationship` (scatter/bubble) | off-target | `generic` — entered with *no* task evidence (lexical 0.049); a scatter plot answers no question this task asks |
| GUARDRAIL | `impl-reuse-before-new` | partial | `generic` — true, but SKILL.md §2 already says it |
| GUARDRAIL | `interaction-drag-drop` | off-target | `wrong-screen` — nothing on this dashboard is draggable; selected only as a `interaction.keyboard_navigation` carrier |
| GUARDRAIL | `a11y-color-not-only` | relevant | — (drove word+icon+colour urgency labels) |
| GUARDRAIL | `data-exceptions-first` | relevant | — **the single most useful record in the bundle**, yet it is ranked as an OPTIONAL note in the markdown ordering while two chart records sit in CORE |
| BUNDLE | — | — | `missing-critical`: `data.drilldown` and `layout.focal_hierarchy` (pre-registered critical) absent |

Counts: relevant 3, partial 1, off-target 3. Optional layer: 1 record, 1 useful, 0 noise.

### Concept recall

Delivered (union of selected records' `concepts`): `a11y.color_not_only`, `data.chart_by_question`, `data.accessible_chart_alternative`, `state.loading_empty_error`, `process.reuse_first`, `touch.gestures_discoverable`, `interaction.keyboard_navigation`, `a11y.live_status`, `perf.layout_shift`, `interaction.selection_visible`, `data.exception_first`, `env.glanceable_status`, `table.tabular_figures`.

| expected id | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| data.exception_first | yes | yes (optional layer) | — |
| data.drilldown | yes | no | `bundle-selection` — trace: "candidates existed (comp-kpi-tile) but the bundle cap or a lower utility left them out"; `comp-kpi-tile` was omitted as "no positive task evidence … for a core record" on a screen resolved as `dashboard` |
| layout.focal_hierarchy | yes | no | `bundle-selection` (candidates `layout-hierarchy-one-thing`, `metadata-rich`) |
| data.kpi_comparison | no | no | `bundle-selection` (candidates `comp-kpi-tile`, `chart-compare-bar`) |
| a11y.color_not_only | no | yes | — |
| table.tabular_figures | no | yes (via `data-exceptions-first`) | — |
| data.refresh_timestamp | no | no | `expected-concepts` — never demanded at all (absent from the trace) although the base carries it (`data/rules.jsonl`) and the sentence says "today" |

**Concept recall 3/7 = 0.43. Critical recall 1/3 = 0.33.**

`comp-kpi-tile` being omitted is the headline defect: the project's dashboard literally renders a `KpiTile.vue` component, the requirements resolved `screen=dashboard`, and the KPI record alone carried both missing non-critical/critical concepts (`data.kpi_comparison`, `data.drilldown`). The "no positive task evidence" filter treats `screen=dashboard` as insufficient evidence for a KPI record while admitting `chart-relationship` with none at all.

PARTIAL status: the note is about `interaction.hover_independence` / `interaction.focus_visible` being uncovered, not about a design/engineering split. The split question does not arise here; the task is wholly design.

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`, 0 `changed`, 0 `new`. **`unjustified_direction_slots` = 0** — correct for an existing UI at a moderate budget. Validation OK. Preservation metrics: navigation/surface/typography/radius pinned to repository evidence.

One inherited flaw: the navigation slot prescribes top-bar guidance ("collapse to a menu button below the container width") for an app whose primary navigation is a sidenav. Harmless because the slot is preserved, but it would mislead if the budget were higher — routed to `project-context`, not `direction`.

## 5. Implementation

Files changed (copies in `before/`):
- `src/views/DashboardView.vue`
- `src/components/KpiTile.vue`

What was built:
- **Exception-first reorder panel**: "Needs reordering today" with a count chip in the heading, the exception rule stated under it ("On hand at or below the reorder point · longest lead time first"), a column header row, and rows ranked out-of-stock → critical (≤ ½ reorder point) → below point, then by supplier lead time, then shortfall. Each row: urgency as word + icon glyph + colour, SKU link (drill-down to the product detail route), name, supplier · lead time, `on hand / reorder point` and a suggested order quantity, all tabular-numeric. Empty state ("Nothing to reorder today…") and an overflow line linking to the full list.
- **KPI tiles re-pointed at the decision**: the first tile is now "Needs reordering today" (47) with tone emphasis and hint "1 out of stock · 26 urgent", and it is a drill-down link to Products; a new "Suggested order value" tile prices the action; "Total SKUs" carries a comparison hint. Stock value kept.
- **KpiTile extended, not replaced**: optional `tone` and `to` props, default `neutral`/undefined, so the other three call sites render exactly as before. Focus-visible ring and a non-colour link affordance added for the linked variant.
- All values come from existing store getters (`lowStock`, `outOfStock`, `supplierById`, `supplierName`); no store edits, no new dependency, existing tokens only.

Guidance used: `data-exceptions-first` (status computed in the model, word+icon+colour, count in the header, rule stated, exceptions sorted first), `a11y-color-not-only`, `layout-dashboard-grid` (importance-ordered modules, per-module heading and empty state), `impl-reuse-before-new` (extended KpiTile through its API instead of a new tile).

Guidance ignored: `comp-chart-container` and `chart-relationship` (no chart on this screen and none warranted — adding one would have been a defect), `interaction-drag-drop` (nothing is draggable here).

**Process guidance check**: SKILL.md §2 / §7 was enough. `impl-reuse-before-new` restated it and consumed a critical-guardrail slot that a KPI or hierarchy record needed. `process_records_needed: false`.

## 6. Render and defects

Render mode: **native web** — `npm run build` + `vite preview` on :4173, Playwright 1.63, Chromium. Viewports 1280×800 and 390×844, plus a 1280×800 dark-theme pass. Screenshots inspected, not merely produced.

First render defects (1 total):
- `visual` 1 — the numeric columns (`0 / 14`, `order 28`) had no visible labels; only screen-reader text explained them, so a manager could not read the ratio at a glance.
- (`interaction` 0, `accessibility` 0, `platform` 0, `existing-system-mismatch` 0, `implementation-bug` 0; zero console/page errors in both viewports and in dark mode.)

Fix: added a compact uppercase column-header row (Status · Item · Supplier · lead time · On hand / point · Suggested), hidden under 600 px where rows wrap. **Iterations: 1.**

Final defects: 0 in every category on the changed surface.

Pre-existing, not introduced, not fixed (out of scope — shell files are off-limits for this task): at 390 px the app shell never collapses the 240 px sidenav, so the content column is ~110 px wide and everything is clipped. `baseline-phone.png` is the unmodified dashboard at the same viewport and is *worse* (four KPI tiles side by side in a 110 px column); my media queries at 900/600 px stack the tiles and the rows, which is all a view-level file can do. Tagged `tooling-limit` only in the sense of scope, not counted as a defect I shipped.

## 7. Preservation verdict

Navigation, theme (verified in dark mode), typography, tokens, spacing scale, `.panel`/`.recent-row` conventions and all routes intact. Components reused (`KpiTile` extended through props, `ReasonTag` untouched). `unjustified_structural_change: 0`. `preservation-ok`.

## 8. Routing of misses (one layer each, earliest)

1. `bundle-selection` — `comp-kpi-tile` omitted on a `screen=dashboard` task, dropping `data.drilldown` (critical) and `data.kpi_comparison`.
2. `bundle-selection` — `layout.focal_hierarchy` (critical) had candidates, none selected.
3. `expected-concepts` — `data.refresh_timestamp` never demanded despite "today" in the sentence and a dashboard screen.
4. `candidate-compatibility` — `chart-relationship` and `interaction-drag-drop` admitted into CORE/guardrails with zero task evidence on a screen with no chart and no drag interaction.
5. `project-context` — `spacing=irregular` on a strict 4-pt token system; `navigation=top-bar` on a top-bar + sidenav shell; `components=unknown` with a 9-file component directory; routing `[]` with vue-router present.

## 9. Regressions to propose

- query: "Make the dashboard tell the manager which items need reordering today." → expect `comp-kpi-tile` in the bundle and `data.drilldown` + `data.kpi_comparison` delivered when `screen=dashboard`.
- query: any dashboard/overview request → expect `data.refresh_timestamp` demanded as a required concept.
- query: dashboard request with no chart evidence in the project → expect `chart-relationship` NOT in CORE.
- inspect: `p6-vue-inventory` → expect `spacing` KNOWN/regular (4-pt scale from `--space-*` tokens) and `theme` KNOWN light+dark from a `[data-theme='dark']` block.
- inspect: any project with `src/components/` (9 files) → expect `components` not UNKNOWN.

## 10. Tags

`concept-miss`, `ranking-miss`, `context-detection-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`, `partial-scope-ok`

**Skill effect: helped.** `data-exceptions-first` supplied the specifics I would otherwise have under-specified — computing status in the model, stating the exception rule on screen, the count in the header, and sorting exceptions first — and `a11y-color-not-only` forced the word+icon urgency label rather than a coloured number. That is real value delivered from an *optional* note, while two CORE records were dead weight.
