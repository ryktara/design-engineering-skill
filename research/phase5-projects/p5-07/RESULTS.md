# p5-07 — Patient search that finds nothing just shows a blank area.

**Task**: p5-07 (verbatim sentence above). **Project**: `p5-sveltekit-clinic` (ClinicBoard) — SvelteKit 2 + Svelte 5 runes + Tailwind 3.4, light only, left rail + top header. **Platform**: web. **Existing UI**: yes (`/patients` list page); **new screen**: no. p5-06's waiting-room change was left intact.

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` (skill not modified).

## Baseline (what "blank area" actually was)

`Table.svelte` already had an `{:else}` row rendering `No patients match your search.` as one line of `text-neutral-500` in a `colspan` cell under the column headers. Rendered at 1440×900 it is a faint single line inside an otherwise empty bordered table — it reads as blank at a glance. At 390×844 the shell is not responsive (fixed 240 px rail, `w-72` search field), the table overflows its card inside `overflow-x-auto`, and the centred message is scrolled out of view: the visible card body is genuinely blank (`render/baseline-*-empty.png`).

## Design-context table (`01-inspect.json` vs code)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | `+layout.svelte`: 240 px left rail + 56 px top header | yes |
| theme | light-first | INFERRED | `app.css` `color-scheme: light`, comment "light theme only" | yes |
| surfaces | flat-tonal, evidence "no shadow or border declarations found" | UNKNOWN | bordered-flat: `border border-neutral-200` on Card, rail, header, table rows, menus; no shadows | no (value and evidence both wrong) |
| radius | unknown | UNKNOWN | Tailwind `borderRadius` theme (sm 4 / DEFAULT 6 / lg 8 / xl 12); `rounded`, `rounded-sm`, `rounded-full` used throughout | partial |
| spacing | 4 | INFERRED | Tailwind 4 px scale; gaps 1/2/3/4/6 | yes |
| typography | custom; `tabular_numerals: false` | INFERRED | `"Source Sans 3"` in `fontFamily.sans`; `tabular-nums` used in Table, waiting, reports | partial |
| components | tailwind | KNOWN | Tailwind + local primitives in `src/lib/components/` (8 files; inspect lists this under `component_dirs`) | yes |

Same detection misses as p5-06 (same codebase).

## Requirements verdict (`02-requirements.json`)

| field | resolved | verdict |
|---|---|---|
| platform | web (`known`: "platform=web (project inspection)"; `platform_evidence` = []) | correct |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | navigation ("find"), performance-ux ("blank") | wrong — the domain is states/feedback (empty state); "find" is search, "blank" is a missing state, not perceived performance |
| intent.change_scope | unknown; `scope: moderate` | acceptable |
| mode + evidence | audit, refactor — "audit: navigation defect on existing UI" | acceptable (refactor is in my acceptable set); the evidence string is wrong (not a navigation defect) and `polish` would fit better than `audit` |
| scope.kind / reason | in-scope — "UI design / interaction task" | correct. Note: `activation.decision = ambiguous`, `ui_score 1.0`, `ui_terms []`; the gate passed on `screen=search` rather than UI vocabulary. p5-06 on the same codebase abstained; the difference is the word "search". |
| change_budget | moderate | acceptable (low would be right for this fix) |
| intent.preserve | [] | miss — nothing declared; navigation/theme/typography/search store should be preserved |
| product | healthcare (from "patient"), ecommerce (README) | ecommerce wrong (same as p5-06) |
| screen | search | correct |
| project_context | as in the table above | carries the surfaces/radius misses |

## Guidance verdict (`03-guidance.md/json`) — status CONFIDENT, 6 records (2 core + 4 guardrails), 795 tokens, purity 0.89

| record | kind | verdict | note |
|---|---|---|---|
| `comp-search` | core | partial | "clear button, result count announced, empty-result guidance" is on target; suggestions listbox, recent searches, URL query, full-screen mobile search and the TV paragraph are beyond the task. Carries `media.search_tv` into a web bundle. |
| `dir-clinical-workstation` | core | off-target — **generic** | Patient banner, master-detail, autosave, destructive confirmation: none applies to an empty state on a list page. Selected as "highest-scoring direction with lexical evidence" (lexical 0.18). It then drove the direction's master-detail / rich-metadata slots. |
| `a11y-keyboard-operable` | guardrail | partial | Tab reachability of the new action is relevant; roving tabindex / drag alternatives are not. |
| `a11y-focus-visible` | guardrail | partial | Relevant to the new button (existing `focus-visible:ring-2` reused). |
| `layout-states-empty-loading-error` | guardrail | relevant | The key record: "Empty: what this is, why it is empty, one action" — shaped the implementation directly. |
| `search-filter-feedback` | guardrail | relevant | "result count announced, empty results suggest next steps" — used (live region + guidance text). Chips/debounce/URL state not needed here but the record is on target. |

Counts: relevant 2 · partial 3 · off-target 1. BAD: `dir-clinical-workstation` → generic.

Ranking note: `concept_trace` shows `comp-empty-state` (0.216) was a candidate for `state.loading_empty_error` — the single most on-target component for a sentence that literally describes a missing empty state — but the second core slot went to a direction record instead. Layer: bundle-selection.

### Concept recall (expected from `00-expectation.json`; delivered = union of `concepts` over the 6 selected records)

Delivered: `data.search_results, media.search_tv, navigation.deep_link_state, interaction.keyboard_navigation, interaction.hover_independence, interaction.focus_visible, state.loading_empty_error, a11y.live_status, data.filter_chips`.

| expected id | delivered? | layer if missing |
|---|---|---|
| state.loading_empty_error (critical) | yes | — |
| data.search_results (critical) | yes | — |
| a11y.live_status | yes (recommended, via `search-filter-feedback`) | — |
| process.reuse_first | no | bundle-selection (demanded as recommended "existing repository: reuse its primitives"; candidate `impl-reuse-before-new` 0.225; dropped for cap/utility) |
| layout.one_primary_action | no | expected-concepts (never demanded; record exists — `cta-one-primary` appears in direction alternatives) |
| interaction.focus_restore | no | expected-concepts (never demanded) |
| perf.layout_shift | no | expected-concepts (never demanded; soft expectation) |

Recall 3/7 = 0.43 · critical recall 2/2 = 1.0. Forbidden concept delivered: `media.search_tv` (inside `comp-search`). No knowledge gaps (`03b-search.txt`: `search-filter-feedback` and `comp-search` rank 1–2; also confirms `comp-empty-state`, `anti-no-states` exist in the base).

## Direction verdict (`04-direction.md/json`) — exit code 3, validation `ok: false`

Budget moderate · preserved `navigation, typography, color` · changed `density` · 9 slots "new".

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-left-rail | preserved | yes |
| layout | layout-master-detail | new | no — the page is a list with row → `/patients/[id]` route; master-detail is a structural rewrite for an empty-state fix (driven by `dir-clinical-workstation`) |
| density | density-high | changed ("existing 4 (INFERRED) → density-high") | no — conflates the 4 px spacing value with a density level; nothing in the task touches density |
| surface | surface-elevated-cards | new | no — contradicts codebase (bordered flat, zero shadows); consequence of the surfaces detection miss |
| cards | card-poster-landscape | new | no — self-flagged VIOLATION "non-media product: poster card geometry"; emitted anyway |
| typography | preserve custom | preserved | yes |
| color | preserve light-first | preserved | yes |
| motion | motion-functional-minimal | new | harmless, unused |
| focus | focus-ring-standard | new, "no repository evidence" | wrong status — inspect reports "explicit focus handling in 3 files"; Button/Input/layout define `focus-visible:ring-2 ring-primary-500`; should be preserved |
| cta | cta-sticky-bar | new | no — contradicts one-primary-action; the header already holds the single primary |
| imagery | imagery-poster | new | no — clinic admin list |
| icon | icon-text-only | new | contradicts codebase (inline outline SVG icons in the rail) |
| metadata | metadata-rich | new | acceptable but unused |

Preservation metrics: 3/13 preserved, 1 changed, 9 new, of which 6 contradict or overreach the codebase. Direction was ignored except the preserved slots; the guardrails were used.

## Implementation

Files changed (before-copies in `before/`):
- `src/routes/patients/+page.svelte` — when `rows.length === 0` the Card renders an `EmptyState` instead of the header-only table: title `No patients match “<query>”`, one description line saying what search covers (name, phone, email) and the next steps, one action `Clear search` (secondary Button; empties `$patientSearch` and returns focus to the field via a stable `id`). Separate copy for the no-patients-at-all case. The `N of 40 patients` count line gets `aria-live="polite"` so the result count is announced. Table, columns, row click, search store, header, primary `Add patient` untouched.
- `src/lib/components/EmptyState.svelte` — new small primitive (title, description, `actions` snippet) using existing tokens only (`neutral-100/500/800`, `rounded-full`, text-sm, 4 px spacing); `px-4 py-10 sm:px-6 sm:py-12`.
- `Table.svelte` not modified (its `empty` prop remains for other callers).

Guidance used: `layout-states-empty-loading-error` (what / why / one action — this is why the empty state has exactly one button and the second CTA is a sentence pointing at the existing primary), `search-filter-feedback` (count announced → live region; next steps), `comp-search` (clear + empty-result guidance; the native `type=search` clear glyph was already there), `a11y-keyboard-operable` / `a11y-focus-visible` (verified: Tab order search → Add patient → Clear search, teal 2 px ring, Enter clears and refocuses the field). Ignored: `dir-clinical-workstation` and the direction's layout / density / surface / cards / cta / imagery / icon slots — all would have changed things the task did not ask for or contradicted the codebase.

Pre-existing, not touched: `svelte-check` reports one error in `Table.svelte` line 4 (`export type` inside a `generics` script); `npm run build` passes.

## Render (mode: native — Playwright 1.63 Chromium against `vite preview`, 1440×900 and 390×844)

`render/shot.mjs` navigates to `/patients`, types the no-match query `zzqx 99999` (empty screenshots), dumps DOM facts (text, live regions, buttons, overflow, focus), clicks `Clear search` and verifies recovery, then types `ma` (results screenshots). Screenshots: `baseline-*`, `first-*`, `final-*` × `{desktop,mobile}` × `{empty,results}`.

Interaction check results (final): desktop/mobile empty — `0 of 40 patients` in a polite live region, empty text present, one button `Clear search`, no console errors; after clear — query `""`, 40 rows, focus on the search field. Keyboard: Tab from the field reaches `Add patient` then `Clear search`; ring present; Enter clears and refocuses.

First-render defects: **visual 1** — at 390 px the empty state sits in a ~100 px column because the shell is not responsive (240 px rail + `w-72` field; overflow-x is pre-existing on every page, recorded in p5-06 too). Interaction 0, accessibility 0, platform 0, existing-system-mismatch 0, implementation-bug 0.
Fix iteration: 1 (narrow-width padding `px-4 py-10` with `sm:` upgrades) — mitigation only; the column width is set by the shell, which is out of this task's scope. Final defects: visual 1 (remaining, pre-existing root cause). Iterations: 1 (2 post-change renders).

## Preservation

Navigation, theme, typography untouched; Card / Button / Input reused; one new primitive composed from them (reuse → extend → compose rung, no library added); unjustified structural change 0. The table header row disappears in the empty case — deliberate: five column labels above no rows were part of the "blank" impression.

## Regressions to propose

1. Query: the task sentence. Expect: `problem_domain` includes a states/feedback domain, not `navigation` + `performance-ux`; mode polish or refactor (not audit with "navigation defect"); `intent.preserve` non-empty on an existing repo.
2. Query: the task sentence. Expect: core contains `comp-empty-state` or `layout-states-empty-loading-error`, not `dir-clinical-workstation`; `process.reuse_first` delivered when `component_dirs` is non-empty; no `media.*` concept delivered for platform web.
3. Query: direction on this project with budget moderate. Expect: focus slot `preserved` when inspect reports focus handling; surfaces bordered-flat (not elevated); a validation VIOLATION (poster card on a non-media product) must be resolved or the slot dropped, not emitted with exit 3.
4. Query: "The filter on the orders list returns nothing and the page goes empty." Expect: in-scope, `state.loading_empty_error` + `data.search_results` delivered, mode polish.
5. Query: inspect on this codebase. Expect: surfaces bordered-flat KNOWN/INFERRED; radius from the Tailwind `borderRadius` theme; `tabular_numerals: true`.

## Tags

`requirements-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-remaining`, `skill-helped`, `preservation-ok`
