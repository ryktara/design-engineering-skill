# p6-06 — "The patient detail billing tab shows amounts that do not line up."

- **Task sentence (verbatim):** The patient detail billing tab shows amounts that do not line up.
- **Project / stack / platform:** `research/phase5-projects/p5-sveltekit-clinic/project` — SvelteKit 2 + Svelte 5 runes, Tailwind 3, TypeScript. Platform: web.
- **Existing UI or new screen:** existing UI (`/patients/[id]`, Billing tab). No new screen.
- **Build hash:** start `ea8eed72…d9947`, end `ea8eed72…d9947` — equal (candidate c3, unmodified).
- **Sentence carries no mode word** (it is an observation, not an instruction).

## 1. Design-context table (`01-inspect.json` → `design_context`)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | fixed 240px left rail in `+layout.svelte` + breadcrumb on detail | yes |
| theme | light-first | INFERRED | light only, no dark variant anywhere | yes |
| surfaces | bordered-flat | INFERRED | `Card` = `bg-white border border-neutral-200 rounded`; shadow only on Modal and the drag ghost | yes |
| radius | unknown | UNKNOWN | `tailwind.config.ts` defines a full radius scale (sm 4 / DEFAULT 6 / lg 8 / xl 12) and components use `rounded` / `rounded-sm` / `rounded-full` | **partial** (UNKNOWN where the config is explicit) |
| spacing | 4 | INFERRED | Tailwind default 4px base, 119 spacing classes | yes |
| typography | custom (tabular_numerals=true, type_scale=false) | INFERRED | `fontFamily.sans = "Source Sans 3"` in the Tailwind theme; no custom type scale; `tabular-nums` used in Table and the summary `dl` | yes (family not named, but the classification is right) |
| components | tailwind | KNOWN | Tailwind is the *styling* layer; the *component model* is a hand-rolled local library (`Card`, `Table`, `Badge`, `Tabs`, `Button`, `Input`, `Select`, `Modal`, `EmptyState`) in `src/lib/components/` | **partial** (names the CSS system, not the component model; `component_dirs` does find the directory elsewhere in the JSON) |

Tag: `context-detection-miss` (radius, components).

## 2. Requirements verdict (`02-requirements.json`)

| field | resolved | expected | verdict |
|---|---|---|---|
| platform_evidence | `platform=web` from project inspection, `platform_evidence: []` | web | **correct** (assigned from the project, not the sentence — honest: the sentence alone gives no platform evidence) |
| intent.artifact_state | `existing` | existing | correct |
| intent.operations | `["diagnose","modify"]` | diagnose + modify | correct |
| intent.problem_domain | `["visual"]` | visual (with a data-consistency component) | correct for the literal reading |
| intent.change_scope | `screen` | screen | correct |
| mode + mode_evidence | `["polish","audit"]`, evidence "visual defect on existing UI" / "diagnose first" | polish / refactor / audit | **correct** and well-evidenced with no mode word in the sentence |
| scope.kind | `in-scope`, reason "UI design / interaction task" | in-scope | correct |
| change_budget | `low` | low | correct |
| intent.preserve | `[]` | — | acceptable (nothing named in the sentence; the direction still preserved everything) |
| project_context | as in §1 | — | partial (radius, components) |
| components | `["tabs"]` | should also carry `table` / data-display | **miss** — the sentence says "billing **tab** shows **amounts**"; only the tab component was extracted. This is the root of the biggest guidance failure (§3). |

Tag: `requirements-miss`.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

status `PARTIAL`, bundle = 4 records (core 3 + guardrail 1), 701 tokens, no OPTIONAL layer emitted.

| record | layer | verdict | category | why |
|---|---|---|---|---|
| `layout-master-detail` | core | **off-target** | `wrong-screen` | Tells me how to build a list+detail pane. The task is a defect inside one tab of an already-built detail screen; nothing here is actionable. |
| `comp-tabs` | core | partial | `generic` | Correctly identifies the Tabs component on the screen, but roving tabindex / URL state / lazy panels are not the reported defect. True, contributes nothing to it. |
| `dir-clinical-workstation` | core | partial | `generic` | One clause ("strict status colour language with text and icons — never colour alone", "large legible numerics") touches the screen; the rest (patient banner, autosave, destructive confirmation) is off-task. |
| `typo-scale-and-roles` | guardrail | **relevant** | — | Carries the pre-registered critical concept `table.tabular_figures` ("numeric role uses tabular lining figures"). Caveat: for a low-budget alignment fix, delivering the critical concept via a whole type-scale rule is close to `overlong` — the direct carrier would have been `data-tables-numeric`. |

Counts: relevant 1 · partial 2 · off-target 1. `layer_review`: core `[layout-master-detail, comp-tabs, dir-clinical-workstation]`, critical `[typo-scale-and-roles]`, optional `[]` (optional_useful 0, optional_noise 0).

**Bundle-level defect (the headline finding).** `data/rules.jsonl` contains `data-tables-numeric` — *"Numeric tables: alignment, figures, units, precision … Right-align numbers with tabular lining figures, one precision per column … **totals visually distinct** …"* — with keywords `numeric alignment`, `align numbers`, `right-align`, `totals`. It is the single most on-point record in the base for this sentence, and **it never appeared at all**: not in the bundle, not in `omitted`, not in `rejected`, not in the top-12 of `advise.py search` (`03-search-k12.md` returns `media-resume-and-details`, `nav-tv-top-tabs`, `chart-trend-line`, `comp-product-detail-page` instead). Same for `table-column-disambiguation`. The paraphrase "do not line up" is not lexically bridged to "align / alignment / numeric table", and requirements never added `component=table` to give it a structural path. Everything I actually shipped (a totals footer that makes the amounts add up) is literally in that record's text, and I got it from reading the code, not from the bundle.

### Concept recall

Delivered concepts (union over selected records): `interaction.tabs_roving`, `navigation.deep_link_state`, `table.tabular_figures`, `brand.type_roles`.

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `table.tabular_figures` (**critical**) | yes (SPECIFIC, via `typo-scale-and-roles`) | — |
| `data.kpi_comparison` | no | `expected-concepts` — never demanded; also **no record in `data/rules.jsonl` carries this id at all** (knowledge-gap for the "figure vs. its reference figure" idea that this task is really about) |
| `layout.spacing_scale` | no | `bundle-selection` — trace: "candidates existed … `anti-inconsistent-spacing`, `layout-spacing-scale`" |
| `a11y.semantics` | no | `expected-concepts` — never demanded, though `a11y-semantics-structure` / `a11y-native-semantics` carry it (the task adds a `tfoot`/`th scope="row"`) |
| `a11y.color_not_only` | no | `expected-concepts` — never demanded; `a11y-color-not-only` exists in the base (Status column is a badge that already uses text, but nothing checked it) |
| `process.reuse_first` | no | `bundle-selection` — trace: "candidates existed … `impl-reuse-before-new`" |
| `process.render_verify` | no | `expected-concepts` — never demanded; `verify-render-and-inspect` exists in the base |

**concept_recall = 1/7 = 0.14 · critical_recall = 1/1 = 1.00.**

`status=PARTIAL` (not PARTIAL_SCOPE) — concern coverage 0.5, uncovered required concerns `anti-pattern` and `accessibility`. The note is accurate; the uncovered `accessibility` concern is real (nothing in the bundle addressed the semantics of a totals row).

## 4. Direction verdict (`04-direction.md`)

All **13 slots preserved, 0 changed, 0 new**. Budget `low`, validation `OK`, fingerprint (left-rail / bordered / card-geometry none / sharp corners / neutral-plus-accent) matches the codebase except `card_geometry: "none"` — the project does wrap content in a bordered `Card` with a 6px radius, so "none" is slightly off, but it is advisory and did not cost anything.

**`unjustified_direction_slots` = 0.** Correct behaviour for an existing UI at a low budget. The per-slot text is generic boilerplate ("Keep the current X; inspect and reuse it") but it is honest boilerplate, and the "Existing system: do not replace it for this task" suffix is the right instruction. Tag: `preservation-ok`.

## 5. Implementation

**Diagnosis (from code + render, `render/pre-*.png`).** The Amount column is *not* mis-aligned typographically: `Table.svelte` already applies `text-right tabular-nums` to right-aligned cells, and measured DOM boxes confirm every amount and the header share the right edge at x=1239.0. The real "do not line up" is arithmetic and cross-screen:

1. The Billing tab lists invoice amounts with **no total** — there is nothing for them to line up *to*.
2. The header `Balance` badge showed `patient.balance`, a separately generated number. `sample.ts` derives invoices *from* the balance but an invoice can overshoot the remaining target, so e.g. patient P-1007 showed **Balance $219.00** over a single outstanding invoice of **$244.00**. The patients list (`Balance` column) and the reports KPI (`Outstanding balance`, summed over `p.balance`) inherited the same wrong number.

**Files changed** (originals in `before/`):

- `src/lib/components/Table.svelte` — added an optional `footer?: Snippet<[Column<Row>[]]>` prop rendered as a `<tfoot class="border-t border-neutral-300 bg-neutral-50">`, only when there are rows. Additive; the other `Table` call sites (patients list, visits tab) are untouched.
- `src/routes/patients/[id]/+page.svelte` — `billedTotal` / `outstandingTotal` `$derived` from `data.invoices`; a two-row totals footer ("Total billed", "Outstanding balance") using `th scope="row"` + `colspan`, `text-right … tabular-nums` in the Amount column so the totals sit on the same right edge as the rows.
- `src/lib/data/sample.ts` — after invoice generation, reconcile `p.balance` to the sum of that patient's unpaid invoices, so the header badge, the patients list and the reports KPI all agree with the amounts on the billing tab.

Routes, tab ids, `Tabs` state, `Badge`/`Card`/`Button` usage, focus handling and the Table's row semantics are unchanged. `svelte-check`: 1 error before and 1 error after — the same pre-existing `Table.svelte 4:3 "Modifiers cannot appear here"` (svelte-check's known limitation with `export type` in an instance script). No new type errors.

**Guidance used:** `typo-scale-and-roles` — tabular lining figures on the new totals cells (the only bundle content that reached the diff; the project already used `tabular-nums`, so the marginal contribution is small).
**Guidance ignored:** `layout-master-detail` (the master–detail shell already exists and the task is not about it), `comp-tabs` (tab behaviour is not the defect and changing it would break tab state), most of `dir-clinical-workstation` (banner / autosave / destructive-confirmation clauses are outside a low budget and outside the billing tab).

## 6. Render

**Render mode:** `html` — real app, `vite dev` on :5199, Playwright 1.63.0 Chromium, viewports 1280×800 and 390×844, patients P-1000 / P-1003 / P-1007 plus the patients list and reports screens. Screenshots in `render/`: `pre-*` (before any edit), `first-*`, `final-*`, `zoom-first.png`, `zoom-final.png`. All were inspected visually; DOM box/baseline measurements in `render/probe*.mjs`.

### First-render defects (4)

| # | type | defect |
|---|---|---|
| 1 | visual | The `tfoot` was two `h-11` rows (88px) with no divider between them — heavier than the two data rows above and reading as one undifferentiated block. |
| 2 | existing-system-mismatch | I had reconciled the balance only on the detail screen, so `/patients` (Balance column) and `/reports` (Outstanding balance KPI) now disagreed with it — I had moved the inconsistency instead of removing it. Caught only because I rendered the other two screens. |
| 3 | visual (pre-existing) | Status-column `Badge` text sits ~1px below the row baseline (`inline-flex` centres the 20px badge box, so its 12px text baseline ≠ the 14px cell baseline; measured 291.5 vs 290.0). |
| 4 | platform (pre-existing) | At 390×844 the whole app is broken: the 240px rail is not collapsible and the content is clipped. Identical in `pre-mobile-*.png`. |

### Fixes and final defects (2, both pre-existing and out of budget)

Iteration 1 → 2: rows to `h-10`, a `border-t border-neutral-200` above "Outstanding balance" to separate subtotal from total; reconcile `p.balance` at the data source and revert the local badge derivation so all three screens read the same number (verified: P-1007 → $244.00 in header, list and footer; P-1003 → $235.00; five all-paid patients → "No balance" + `$0.00` outstanding).

| type | count | note |
|---|---|---|
| visual | 1 | #3 badge baseline — fixing it means editing the shared `Badge` used on 6 screens; outside a `low` budget for an alignment task on one tab. Recorded, not shipped. |
| platform | 1 | #4 390px shell — pre-existing, whole-app responsive work, explicitly outside this task's budget and the direction's preserved `layout` slot. |
| all other types | 0 | |

**Iterations: 2.** No defect the guidance warned about was shipped (the guidance warned about none of these).

## 7. Preservation verdict

navigation ✅ · theme ✅ · typography ✅ · component reuse ✅ (extended the existing `Table` with an optional snippet instead of writing a bespoke summary block; reused `Badge`/`Card`/`Tabs`) · routes and tab ids ✅ · unjustified structural changes: 0. Tag `preservation-ok`.

## 8. Process guidance check

**Did I need `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` in the bundle?** **No.** SKILL.md §2 (inspect before deciding), §6 ("build in the project's stack and component model", "do not break routes, state, test ids, accessibility semantics") and §7 ("compilation is not visual success … capture the representative viewports, look at the images, fix and re-capture") already produced the reuse decision and the render loop that caught defect #2. `process_records_needed: false`. Noting honestly that `impl-reuse-before-new` and `verify-render-and-inspect` *were* demanded as recommended concepts and dropped at bundle selection — that dropping cost nothing here because §2/§6/§7 covered it.

## 9. Skill misses, routed to the earliest wrong layer

| # | layer | miss |
|---|---|---|
| 1 | `requirements` | "billing **tab** shows **amounts**" yielded `components: ["tabs"]` only. No `table` / data-display component, no `screen_subtype`. Without it, the table records have no structural path into the candidate set. |
| 2 | `candidate-retrieval` | "amounts that do not line up" does not retrieve `data-tables-numeric` (keywords `numeric alignment`, `align numbers`, `totals`) or `table-column-disambiguation` — they are absent from the top 12 of `search`. The paraphrase "line up" → "align" is unbridged. TV/mobile/ecommerce records (`media-resume-and-details`, `nav-tv-top-tabs`, `comp-product-detail-page`) outrank them on a web healthcare table task. |
| 3 | `expected-concepts` | `a11y.semantics`, `a11y.color_not_only`, `process.render_verify` were never demanded although carriers exist in the base. |
| 4 | `criticality` / `expected-concepts` | `data.kpi_comparison` — "a figure shown next to the reference figure it must agree with" is the actual subject of this task, was never demanded, and **no record carries the id** (knowledge gap). |
| 5 | `bundle-selection` | `layout.spacing_scale` and `process.reuse_first` had live candidates and were dropped; three of four bundle slots went to records that contributed nothing to the reported defect. |

## 10. Regressions to propose

| query | expectation (in words) |
|---|---|
| "The patient detail billing tab shows amounts that do not line up." | `data-tables-numeric` in the bundle (core or guardrail); `components` includes `table`. |
| "The invoice amounts in the billing table don't line up." | Same — the paraphrase "line up" must map to numeric alignment without the word "align". |
| "The totals under this table don't match the number in the header." | A record covering "a displayed figure and its reference figure must agree" (`data.kpi_comparison` or a new `table.totals_reconcile` concept); currently no carrier exists. |
| "The amounts in the table are right-aligned but the totals row isn't." | `data-tables-numeric` ("totals visually distinct") plus `a11y.semantics` for `tfoot` / `th scope="row"`. |
| any web + `screen=detail` + `product=healthcare` polish query | `nav-tv-top-tabs` and `media-resume-and-details` must not appear in the top 5 of `search`. |

## 11. Tags

`requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `skill-neutral`, `preservation-ok`

**Skill effect: neutral.** The critical concept was delivered (`table.tabular_figures`) but the codebase already satisfied it, so it changed nothing. Every part of the fix I actually shipped — diagnose the arithmetic, add a totals footer, reconcile the balance at the source — came from reading the code and looking at the render, not from the bundle, even though a record that states exactly that ("totals visually distinct") sits unretrieved in the base. Nothing in the bundle led me to a change I reverted, so not `hurt`.

## 12. Build hash

`00-build-hash-start.txt` = `00-build-hash-end.txt` = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`. The skill directory was not modified.
