# p5-01 — "The invoices table on the billing page is hard to scan once there are more than twenty rows."

- **Project / stack / platform:** `research/phase3-projects/p3-nextjs-saas/project` — Next.js 15.3 app router, React 19, Tailwind v4 (CSS-first `@theme inline`), shadcn new-york/zinc primitives, Geist Sans/Mono via `next/font`, Lucide icons. Platform: web.
- **Existing UI or new screen:** existing UI (`components/billing/invoice-history.tsx`, rendered on `/settings/billing`). Fixture extended 6 → 30 invoices in `lib/billing.ts` to reproduce the sentence (copied to `before/`).
- **Build hash:** start `bf034323…f0d8` = end `bf034323…f0d8` (equal). Nothing under `design-engineering/` was modified.
- **Note on continuity:** a previous agent ran steps 0–4, implemented, rendered `first-*`, did one fix iteration and re-rendered `final-*`. This agent verified the served build matched the source (BUILD_ID 14:48:28 > last edit 14:47:57), found two more defects, fixed them (iterations 2–3), rebuilt, and re-rendered every `final-*` file. The server is `next start`, so each iteration needed `npm run build` + restart.

## Design-context table (01-inspect.json vs the code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | `app-shell.tsx`: `<aside class="hidden w-56 … md:flex">` left rail + top header; settings sub-nav tabs; rail simply hidden below `md` (no drawer) | yes |
| theme | dual-theme, default light | KNOWN | `globals.css`: `:root` light tokens, `.dark` opt-in class, Tailwind v4 `@theme inline` mapping | yes |
| surfaces | bordered-flat | INFERRED | `rounded-lg border` panels, zero shadows | yes |
| radius | small (0.5) | INFERRED | `--radius: 0.5rem`, `sm/md/lg` derived | yes |
| spacing | 8 | INFERRED | Tailwind 4/8/12/16/24; table `h-10` header, `py-2 px-3` cells | yes |
| typography | custom — "font family Var (2 refs)", monospace, tabular numerals | KNOWN | Geist Sans + Geist Mono through `next/font` (`--font-geist-sans/mono`); mono invoice ids; `tabular-nums` on amounts | partial — value right, but the evidence never names the family; "font family Var" is a misparse of the CSS variable references |
| components | tailwind, radix, shadcn-style cva, **table:tanstack**, shadcn | KNOWN | shadcn Table/Badge/Button/Card/Dialog + radix dialog/slot + cva. `@tanstack/react-table` is in `package.json` but **imported nowhere** — both tables are plain shadcn `<Table>` | partial — `table:tanstack` is asserted from the manifest, not the code, and the guidance then says "TanStack Table (headless) is the convention" |

## Requirements verdict (02-requirements.json)

| item | resolved | expectation | verdict |
|---|---|---|---|
| platform | `web`, `platform_evidence: []` (from project inspection) | web | correct (sentence gives no platform evidence; project inspection supplied it — acceptable path) |
| intent.artifact_state | existing | existing | correct |
| intent.operations | diagnose, modify | modify (+diagnose fine) | correct |
| intent.problem_domain | layout (from "scan") | data-display / density | partial — "scan" is a data-display/legibility problem, and the domain drives the concern set (no `data` concern was required) |
| intent.change_scope | screen | component (one table) | partial |
| intent.utterance | observation | observation | correct |
| mode + mode_evidence | audit, refactor — "layout/structure defect on existing UI; structural fix follows" | polish or refactor | acceptable — refactor is in the accepted set; audit is defensible for an observation but it pulled audit-only recommended concepts (`a11y.contrast`, `a11y.accessible_names`) into the queue ahead of scan-related ones |
| scope.kind / reason | in-scope, "UI design / interaction task" | in-scope | correct |
| change_budget | moderate | moderate (one component) | correct |
| intent.preserve | [] with `constraints.preserve_existing_system: true` | preserve nav/theme/typography | acceptable — sentence carries no preserve wording; constraint flag is right |
| density | high (inferred from product=finance) | high | acceptable |
| project_context | see table above | — | 5 yes / 2 partial |

## Guidance verdict (03-guidance.json, bundle = 2 core + 4 guardrails, 1324 tokens)

| record | kind | verdict | notes |
|---|---|---|---|
| `comp-plan-comparison` | core | partial | The billing-page record. One clause is on target (invoice history: date, amount tabular, status text + icon, real download link) and matches what the code already did; the rest is plans/seats/dialogs/sub-nav. Nothing about scanning 20+ rows. |
| `comp-data-table` | core | partial — BAD `generic` | Sticky header, keyboard grid navigation, empty state in body: relevant. Selection checkbox column + select-all, inline edit, column resize/reorder/visibility persisted, virtualised rows: wrong for a 30-row read-only invoice list (3 forbidden concepts: `table.virtualization`, `table.inline_edit`, `table.selection_bulk`). The shadcn adaptation says "add virtualisation for >200 rows", which self-limits, but the record still carries the forbidden concepts into the bundle and the fingerprint (`grid_behavior: virtualized`). |
| `grid-single-tab-stop` | guardrail | relevant | Directly applicable: the before-code had 30 `<a download>` tab stops. Implemented as a roving-tabindex grid, one Tab stop, arrows/Home/End, Enter downloads, Right reaches the link. Same pattern as the project's seat table. |
| `a11y-hover-not-required` | guardrail | partial | Applicable but the code already had persistent download links; no change needed. |
| `layout-states-empty-loading-error` | guardrail | partial | Empty state already existed; `loading.tsx`/`error.tsx` exist at the route. Not about scanability. |
| `web-responsive-breakpoints` | guardrail | relevant | The 390 test it prescribes is where the right-edge clipping defect was found. |

Counts: relevant 2 · partial 4 · off-target 0. Filtered-out list (mobile/TV/kiosk records) was correct.

### Concept recall

Delivered (union of `concepts` over the 6 selected records): `table.tabular_figures, layout.one_primary_action, a11y.color_not_only, feedback.confirmation_destructive, table.selection_bulk, data.comparison_structure, table.inline_edit, table.virtualization, data.pagination_strategy, interaction.selection_visible, interaction.keyboard_navigation, interaction.focus_visible, interaction.hover_independence, state.loading_empty_error, adaptive.breakpoint_matrix, adaptive.navigation_transform`.

| expected concept | critical | delivered? | layer if missing (from `concept_trace`) |
|---|---|---|---|
| `data.pagination_strategy` | yes | yes (tag on `comp-data-table`) — but the record text says "virtualised rows"; the record that actually describes a load-more/pagination strategy for tables, `comp-pagination` (search rank 3, 0.325), is not in the bundle. Tag-delivered only. | — (ranking-miss noted below) |
| `table.tabular_figures` | yes | yes | — |
| `table.column_priority` | no | no | `candidate-retrieval` — demanded (recommended, "table on narrower widths"); trace: "carriers filtered before ranking: platform ['mobile','tablet'] not in request ['web']". No web carrier exists for column priority although the sentence's own table hides columns at sm/md. |
| `data.exception_first` | no | no | `expected-concepts` — never demanded (only demanded for dashboard jobs, `de_semantic.py` line 1065). Also a `knowledge-gap`: no record in `data/*.jsonl` carries it (only lexicon phrases); `search -k 12` returns nothing about exceptions-first. |
| `a11y.color_not_only` | no | yes | — |
| `a11y.semantics` | no | no | `expected-concepts` — never demanded despite audit mode; `a11y-semantics-structure` exists (search rank 4, 0.306). |
| `process.reuse_first` | yes | no | `bundle-selection` — demanded (recommended, "existing repository: reuse its primitives"), candidate `impl-reuse-before-new` (0.207) dropped by the cap. Critical for an existing-UI fix. |

Recall = 3/7 = **0.43**. Critical recall = 2/3 = **0.67**. Forbidden concepts delivered: 4 (`table.virtualization`, `table.inline_edit`, `table.selection_bulk`, `adaptive.navigation_transform`).

Status was CONFIDENT (not PARTIAL_SCOPE) — correct.

## Direction verdict (04-direction.json)

Change budget moderate · preserved `navigation, surface, typography, color` · changed `[]` · new 9. Validation OK.

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-left-rail | preserved | yes |
| layout | layout-table-first ("fills viewport, internal scrolling, virtualise beyond a few hundred rows") | new | partly — sticky header yes; internal scroll box no (the page is a settings page with sections above; the table scrolls with the page) |
| density | density-high | new | yes (matches h-10/py-2) |
| surface | surface-bordered-panes | preserved | yes |
| cards | card-list-row | new | n/a, harmless |
| typography | keep | preserved | yes |
| color | color-neutral-accent | preserved | yes |
| motion | motion-functional-minimal | new | yes (no motion added) |
| focus | focus-ring-standard | new | yes — matches existing `ring` token; used `focus-visible:ring-2 ring-inset` |
| cta | **cta-toolbar-commands** ("selection-driven commands, count of selected items") | new | **no** — read-only invoice list with one row action; ignored |
| imagery | **imagery-data-graphics** ("sparklines in tables") | new | **no** — nothing to chart; ignored |
| icon | icon-outline-system | new | yes (Lucide) |
| metadata | **metadata-rich** ("user-controlled column visibility and order") | new | **no** for this budget; ignored. Its "IDs in monospace, status as text+colour" clauses match the existing code |
| fingerprint `grid_behavior` | **virtualized** | — | **no** — 30 rows |

Three new slots (cta, imagery, metadata) and one fingerprint value would have widened the change beyond the sentence; a "modify one existing table" task should leave those slots "not applicable" rather than "new". Preserved slots were all right.

## Implementation summary

Files changed (originals in `before/`):
- `components/billing/invoice-history.tsx` — now a client component (state for collapse + roving focus; the seat table in the same folder already is one with the identical pattern).
  - Exceptions first: `open` / `past_due` invoices in a "Needs attention" group at the top (destructive colour + icon + text), then the rest newest-first grouped by year with per-year count and paid total in a muted band row (`th scope="rowgroup"`, one `<tbody>` per group).
  - Long-list strategy: collapsed to every exception + the 12 most recent regular rows with "Showing N of 30 · Show all 30 invoices"; after expanding, focus moves to the first newly revealed row (the button unmounts). Threshold 16 so short histories never collapse.
  - Sticky column header (`sticky top-0 bg-background`), page-level scrolling (`overflow-x-clip` on the primitive's wrapper instead of its `overflow-auto`).
  - Section header count: "30 invoices · 2 need attention".
  - Void rows de-emphasised (muted text, struck-through amount) so the eye skips them.
  - Keyboard: `role=grid`, one Tab stop, arrows/Home/End move rows, Enter downloads, Right/Left reach and leave the download link, `aria-rowcount`/`aria-rowindex`, row `aria-label`, sr-only usage note via `aria-describedby`.
  - Below `sm`, cell padding 8 px on this table only (`max-sm:[&_td]:px-2`) so the four remaining columns fit 358 px.
- `lib/billing.ts` — fixture 6 → 30 invoices (Apr 2024 – Sep 2026), same shape.

Guidance used: `grid-single-tab-stop` (fully); `comp-data-table` (sticky header, keyboard grid navigation, empty state kept); `comp-plan-comparison` (tabular figures, status text + icon, real download link — preserved from the existing code); `web-responsive-breakpoints` (1440 + 390 tests); direction density-high / focus-ring / icon-outline (consistent with what exists).

Guidance ignored and why: virtualisation (30 rows; the record itself says >200); inline edit, selection column, bulk actions, toolbar commands (nothing to select or edit); column resize/reorder/visibility persistence (over budget, not the problem); sort with `aria-sort` (grouping newest-first serves the scan job; sort would fight the exception-first order); sparklines/data graphics; loading skeleton rows (route-level `loading.tsx` exists); table-first "internal scroll box" (settings page, not a workbench).

Decisions that came from reviewer judgment, not the skill: exception-first grouping, year bands with totals, collapse/"Show all" with a count, void de-emphasis, header count line. These are the changes that address the sentence.

## Render

Mode: **native** (Next.js production build served by `next start`, Playwright 1.63 Chromium). Viewports 1440×900 and 390×844. Files: `render/first-*.png` (previous agent, pre-fix) and `render/final-*.png` (re-rendered by this agent after iteration 3): fold, full page, and invoice section collapsed / expanded-top / expanded-scrolled / keyboard-focus per viewport (24 files).

Console: 5 (1440) / 3 (390) 404s — Next.js prefetches of nav routes that do not exist in the fixture (`/invoices`, `/inventory`, `/settings/general|members|security`). Pre-existing, not caused by the change. No horizontal overflow at either viewport (`scrollWidth == clientWidth`, overflowing-elements: none).

### First-render defects (by type)

| type | count | what |
|---|---|---|
| visual | 3 | (1) Sticky year rows overlapped at each group transition with the outgoing row's text showing through the incoming one (semi-transparent overlap). (2) At 390 the table's min-content width (374 px) exceeded the 358 px container and `overflow-x-clip` cut the right edge — year "Paid" totals lost their last digits and the download cell's padding. (3) After (1) was made opaque, a 20 px strip of the outgoing sticky group row still peeked out under the column header at every transition (Chromium does not constrain a sticky `<tr>` to its `<tbody>`, so the per-tbody push technique does not work). |
| interaction | 0 | keyboard path verified: 1 Tab stop, arrows, Enter, Right → link; focus lands on the first newly revealed row after "Show all" |
| accessibility | 0 | |
| platform | 0 | |
| existing-system-mismatch | 0 | Table / StatusBadge / Button / tokens reused; radius, spacing, type unchanged |
| implementation-bug | 0 | tsc + next build + lint clean |

### Iterations: 3
1. (previous agent) opaque group-row background / z-order — removed the text bleed-through.
2. (this agent) 8 px cell padding below `sm` on this table — table 356 px in 358 px; overflow none.
3. (this agent) dropped `sticky` from the group rows (kept the sticky column header). The year is already on every row (Issued column on desktop, stacked date on mobile), so the band only needs to carry count + total. Overlap gone.

### Final defects: visual 0 · interaction 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.

## Preservation verdict

Navigation untouched · theme: only existing tokens used (`bg-muted`, `text-destructive`, `ring`, `bg-background`) · typography unchanged (Geist, mono ids, `tabular-nums`) · component reuse: `Table*`, `StatusBadge`, `Button`/`buttonVariants`, Lucide · structural changes: server → client component (justified by state; matches the sibling seat table), one `<tbody>` per group (semantic, harmless). Unjustified structural changes: 0. **preservation-ok**.

## Skill misses by earliest wrong layer

| layer | what |
|---|---|
| requirements | `problem_domain: layout` for "hard to scan … more than twenty rows"; the row-count cue ("twenty rows") was not read as a long-list/data-display signal, so no `data` concern and no pagination/exception concept was *required*. |
| expected-concepts | `data.exception_first` never demanded (only for dashboard jobs); `a11y.semantics` never demanded in audit mode although `a11y.accessible_names` / `a11y.contrast` were. |
| candidate-retrieval | `table.column_priority` has only mobile/tablet carriers; filtered out on web even though the table in question already hides columns at sm/md. |
| bundle-selection | `process.reuse_first` (`impl-reuse-before-new`, 0.207) dropped by the cap on an existing-UI polish where it is critical; `comp-pagination` (search 0.325, the only record describing a table load-more/pagination strategy) not selected, while `comp-data-table` (search 0.264) carried the pagination tag without the content. |
| knowledge-gap | No record carries `data.exception_first` ("exceptions and anomalies first"); `search -k 12` confirms. |
| direction | `cta-toolbar-commands`, `imagery-data-graphics`, `metadata-rich`, `grid_behavior: virtualized` proposed as *new* for a modify-one-table task; had to be ignored. |
| context-detection (project-adaptation) | `table:tanstack` asserted from `package.json` with no import in the code; the react/shadcn adaptations then recommend TanStack Table. Typography evidence "font family Var" instead of Geist/`next/font`. |

## Regressions to propose

1. **query:** "The invoices table on the billing page is hard to scan once there are more than twenty rows." (with a project context: web, existing UI, shadcn) — **expect:** `data.pagination_strategy` and `data.exception_first` in *required* concepts; `process.reuse_first` required (not recommended) whenever `artifact_state=existing` and mode ∈ {polish, refactor, audit}; a record that actually describes a load-more/pagination strategy for tables (`comp-pagination`) in the bundle; no core record whose text pushes virtualisation, inline edit or bulk selection for a list of < 100 read-only rows.
2. **query:** "On phones the invoice table drops the wrong columns." (web project) — **expect:** `table.column_priority` delivered on platform web (needs a web carrier record).
3. **inspect:** a project whose `package.json` lists `@tanstack/react-table` but no source file imports it — **expect:** `components` does not claim `table:tanstack` as KNOWN (INFERRED with "dependency only, no import" at most).
4. **direction:** a `diagnose+modify`, `change_scope=screen|component` task on an existing read-only table — **expect:** cta/imagery/metadata slots reported as not applicable / unchanged rather than new `cta-toolbar-commands` / `imagery-data-graphics` / `metadata-rich`; `grid_behavior` not `virtualized` below a few hundred rows.
5. **audit mode:** any table-heavy audit — **expect:** `a11y.semantics` demanded alongside `a11y.accessible_names` and `a11y.contrast`.

## Skill effect: **neutral** for the sentence's own goal

The bundle's one real win — the single-Tab-stop grid — is an accessibility improvement orthogonal to "hard to scan", and the breakpoint guardrail caught a render defect. But none of the three decisions that make a 30-row table scannable (exceptions first, year bands with totals, collapse with a count) came from the skill; the record that would have supplied the load-more strategy was ranked out, exceptions-first does not exist in the base, and three direction slots plus the fingerprint pointed at a heavier, wrong artefact that had to be ignored.

## Tags
`requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`
