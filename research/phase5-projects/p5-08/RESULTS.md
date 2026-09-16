# p5-08 — The appointments grid re-renders the whole day when one chip is dragged, so dragging stutters.

**Task**: p5-08 (verbatim sentence above; pre-registered as intended PARTIAL scope). **Project**: `p5-sveltekit-clinic` (ClinicBoard) — SvelteKit 2 + Svelte 5 runes + Tailwind 3.4, light only, 240 px left rail + 56 px header. **Platform**: web. **Existing UI**: yes (`/appointments` day grid); **new screen**: no. p5-06 (waiting room) and p5-07 (patients empty state) changes left intact; the store shape both read is unchanged.

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` (skill not modified).

## Baseline (what the code actually did)

`src/routes/appointments/+page.svelte`: CSS-grid day view (72 px time gutter + one column per practitioner, 08:00–18:00 at 2 px/min), chips absolutely positioned from `start`/`durationMin`, keyed by `appt.id`, each column running its own `$visibleAppointments.filter(...)`. **There was no drag support at all** — no pointer/drag handlers, no cursor affordance, no keyboard way to move a chip, no move function in `stores.ts`. So the sentence's cause ("re-renders the whole day") could not be reproduced; the work was to add drag-to-reschedule in a way that never has that problem, plus the drag UX. Pre-existing and unrelated: three chips share 10:00/10:15 in the Okafor column and overlap (sample data); the shell is not responsive at 390 px (recorded in p5-06/07).

## Design-context table (`01-inspect.json` vs code)

Identical output to p5-06/p5-07 (same codebase):

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | 240 px left rail + 56 px header in `+layout.svelte` | yes |
| theme | light-first | INFERRED | `color-scheme: light`, "light theme only" | yes |
| surfaces | flat-tonal, "no shadow or border declarations found" | UNKNOWN | bordered flat: `border border-neutral-200` on Card/rail/header/chips; no shadows | no |
| radius | unknown | UNKNOWN | Tailwind `borderRadius` theme (4/6/8/12) used throughout | partial |
| spacing | 4 | INFERRED | 4 px Tailwind scale | yes |
| typography | custom; `tabular_numerals: false` | INFERRED | "Source Sans 3"; `tabular-nums` on times in this very page | partial |
| components | tailwind | KNOWN | Tailwind + `src/lib/components` primitives | yes |

## Requirements verdict (`02-requirements.json`)

| field | resolved | verdict |
|---|---|---|
| platform | web (project inspection; `platform_evidence` []) | correct |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | interaction, performance-ux | correct — this is the right reading of "dragged … stutters" |
| intent.change_scope | screen; `scope: moderate` | correct |
| mode + evidence | audit, refactor — "interaction defect on existing UI / fix follows the diagnosis" | acceptable (both in my set) |
| **scope.kind / reason** | **in-scope — "UI design / interaction task"**; `activation.decision = ambiguous`, `ui_terms ["grid"]` | **wrong vs the pre-registered PARTIAL**. No PARTIAL_SCOPE status, no note splitting "re-renders the whole day" (engineering: keyed per-item updates, no store writes per pointermove) from "dragging stutters" (design: drag affordance, drop feedback, no layout thrash, keyboard alternative). The gate passed on the single word "grid"; the sentence's engineering half ("re-renders") was not recognised as such. A plain in-scope is the acceptable-but-weaker outcome I pre-registered; scored `partial-scope-wrong` because the split the task exists to test was not made. |
| change_budget | moderate | acceptable |
| intent.preserve | [] | miss — existing repo, nothing declared (store shape, modal, chip colours, grid geometry) |
| product | healthcare + **ecommerce** (README) | ecommerce wrong (README has no commerce wording; same leak as p5-06/07) and it selected the first core record |
| screen / components | [] / [] | miss — "appointments grid" is a schedule/calendar day view with chips; nothing detected, so the retrieval had no screen anchor |
| project_context | as table above | carries the surfaces/radius/tabular misses |

## Guidance verdict (`03-guidance.md/json`) — status CONFIDENT, 6 records (2 core + 4 guardrails), ≈1279 tokens, purity 0.44

| record | kind | verdict | note |
|---|---|---|---|
| `comp-checkout-one-page` | core | off-target — **contradicts-codebase** | A checkout flow for a clinic scheduling grid. "Highest-scoring component with lexical evidence; lexical 0.326" — the lexical hit is the product tag `ecommerce` leaked from README detection. Nothing in it applies. |
| `comp-data-table` | core | partial | "keyboard grid navigation (arrows…)", "row actions visible on focus as well as hover", selection visible are usable; sticky header, sort, column resize, virtualised rows, skeleton rows are a table spec, not a time grid with 25 chips. Carries the forbidden `table.virtualization`. |
| `grid-single-tab-stop` | guardrail | partial | Arrow keys move within the grid / visible focus on the active cell: used (arrow keys reschedule, ring reused). Roving tabindex + aria-rowindex/colindex is a data-grid model; here each chip is one object with one action, so I kept one Tab stop per chip (25 stops) — recorded as ignored below. |
| `a11y-hover-not-required` | guardrail | partial | Justified the always-visible grip glyph (no hover reveal) and `touch-action: none` so touch can drag. Tooltip clause not relevant. |
| `web-responsive-breakpoints` | guardrail | off-target — **generic** | Breakpoint test matrix; the task is a drag interaction on one screen. |
| `anti-fashion-over-usability` | guardrail | off-target — **generic** | "Run aesthetic choices through contrast/target size" — no aesthetic choice is being made. |
| (bundle) | — | **missing-critical** | Nothing in the bundle mentions drag-and-drop, the perf/re-render cause, drop feedback, reduced motion, or announcing the result. `a11y-keyboard-operable` — the one record in the base that says "provide a keyboard alternative for every drag interaction" — was a candidate (0.333) for `interaction.keyboard_navigation` and lost to `grid-single-tab-stop`. |

Counts: relevant 0 · partial 3 · off-target 3. BAD: `comp-checkout-one-page` → contradicts-codebase; `web-responsive-breakpoints`, `anti-fashion-over-usability` → generic; bundle → missing-critical.

### Concept recall (expected from `00-expectation.json`; delivered = union of `concepts` over the 6 selected records)

Delivered: `feedback.validation_errors, touch.ime_keyboard, feedback.confirmation_destructive, state.saving_conflict, layout.one_primary_action, feedback.trust_signals, table.selection_bulk, table.inline_edit, table.virtualization, table.tabular_figures, data.pagination_strategy, interaction.selection_visible, interaction.keyboard_navigation, interaction.focus_visible, interaction.hover_independence, adaptive.breakpoint_matrix, adaptive.navigation_transform, process.decision_order, a11y.contrast` (19).

| expected id | delivered? | layer if missing |
|---|---|---|
| perf.js_budget (critical) | no | expected-concepts — never demanded although `problem_domain` = performance-ux; `web-hydration-js-budget` exists for web (about hydration/bundle size, not render cost, so even if demanded it would only partly fit) |
| touch.gestures_discoverable (critical) | no | knowledge-gap — the only carrier `mobile-gestures-discoverable` is platform mobile/tablet and is filtered for web; no web record covers gesture affordance; also never demanded |
| interaction.keyboard_navigation (critical) | yes (`grid-single-tab-stop`) | — |
| interaction.selection_visible | yes (`comp-data-table`, `grid-single-tab-stop`) | — |
| perf.layout_shift | no | expected-concepts — never demanded; `web-cls-and-lcp` (web) carries it |
| a11y.reduced_motion | no | expected-concepts — never demanded; `a11y-reduced-motion` (any) carries it |
| a11y.live_status | no | expected-concepts — never demanded (audit mode demanded `a11y.accessible_names` instead, then left it uncovered) |

Recall 2/7 = 0.29 · critical recall 1/3 = 0.33. Forbidden concepts delivered: `table.virtualization` (via `comp-data-table`), `adaptive.navigation_transform` (via `web-responsive-breakpoints`). Knowledge gaps confirmed with `03b-search.txt` (top-12 has no drag / perf / motion record; status there is PARTIAL with "MISSING: platform" because search runs without the project file) and a grep of `data/*.jsonl`: no record whose subject is drag-and-drop / drag feedback exists; drag is only mentioned inside `a11y-keyboard-operable`, `comp-tree-view`, `surface-flat-tonal` ("dragged items still need a shadow" — used) and TV/kiosk avoid-lists.

## Direction verdict (`04-direction.md/json`) — exit code 3, validation VIOLATION

Budget moderate · preserved `navigation, typography, color` · changed `density` · 10 slots "new".

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-left-rail | preserved | yes |
| layout | layout-dashboard-grid | new | no — the page is a time grid; a 12-column module dashboard is a rewrite |
| density | density-high ("existing 4 → density-high") | changed | no — spacing value confused with a density level; nothing in the task |
| surface | surface-elevated-cards | new | no — contradicts bordered-flat codebase (surfaces detection miss) |
| cards | card-poster-portrait | new | no — self-flagged VIOLATION "non-media product: poster card geometry", emitted anyway (third time on this codebase) |
| typography / color | preserve | preserved | yes |
| motion | motion-functional-minimal | new | content is right and was used (transform/opacity only, reduced-motion) — but "new, no repository evidence" is fine here since the codebase has no motion |
| focus | focus-ring-standard | new, "no repository evidence" | status wrong — `focus-visible:ring-2 ring-primary-500` exists in Button/Input/layout; should be preserved (reused) |
| cta | cta-single-primary | new | acceptable; matches the existing single primary |
| imagery | imagery-thumbnails | new | no — nothing to image |
| icon | icon-outline-system | new | matches the codebase's inline outline SVGs, so the value is right but the status should be preserved |
| metadata | metadata-inline-badges | new | matches `Badge` on every chip; status should be preserved |

Preservation metrics: 3/13 preserved, 1 changed, 9–10 new; 5 contradict or overreach; 3 "new" slots describe what the codebase already does. Used: motion slot guidance. Ignored: layout, density, surface, cards, imagery.

## Implementation

Files changed (before-copies in `before/`):
- `src/lib/stores.ts` — `moveAppointment(id, practitionerId, start)`: copies the list and replaces **only** the moved record; every other record keeps its object identity so keyed `{#each}` blocks leave their DOM alone. No-op if nothing changed. `appointments` / `visibleAppointments` shape untouched (p5-06 waiting room still reads them).
- `src/routes/appointments/+page.svelte` —
  - Engineering side: chips bucketed once per store change in a `$derived.by` map (`byPractitioner`) instead of a `filter` per column; drag geometry (column rects, origin) measured once at `pointerdown` into a non-reactive `dragCtx`; `pointermove` is arithmetic only and writes to a small `$state` view (`dx, dy, toPr, toTop, toStart`) field-by-field; the dragged chip moves with `transform: translate()` (no `top` writes, `will-change-transform` only while dragging); the store is written once, on drop; pointer capture; 4 px click tolerance; Escape / `pointercancel` abort.
  - Design side: grab cursor + always-visible 6-dot grip (no hover reveal), hint in the sub-header ("Drag a chip or use the arrow keys to reschedule") and in the chip `title`; while dragging the chip lifts (`shadow-md`, z-30 — the one place the flat system uses a shadow, per `surface-flat-tonal`'s own exception) and a dashed `primary-500` drop ghost shows the snapped 15-min slot with the target time label in the target column; on drop a one-line status "X moved to 10:45 with Dr. …" appears under the count line in a polite live region (fixed `h-5`, truncated with `title`, block is `flex-1 min-w-0` so the header never reflows); chips are `role=button tabindex=0` with an `aria-label` that states name/time/duration/practitioner and the arrow-key hint; ArrowUp/Down = ±15 min, ArrowLeft/Right = previous/next practitioner (when all columns are shown), focus restored after a cross-column move; existing `focus-visible:ring-2 ring-primary-500` reused; `touch-action: none` on chips so touch drags work; `select-none` on the grid during a drag. No animation is added, so there is nothing for reduced-motion to disable (the lift is an instant shadow/z change).
  - Untouched: header, Select filter, New appointment modal, `chipStyle`/`statusTone`/`Badge`, grid geometry, time labels, other pages.

Guidance used: `grid-single-tab-stop` (arrow keys operate the grid; visible focus on the active chip), `a11y-hover-not-required` (persistent grip, touch path), `comp-data-table` (row actions on focus as well as hover; selected/dragging state distinct), direction motion slot (transform/opacity only). Ignored with reason: `comp-checkout-one-page` (wrong product); `comp-data-table` sticky header / sort / virtualisation / skeleton (a table spec, 25 chips); `grid-single-tab-stop` roving tabindex + aria-rowindex (each chip is one object with one action; 25 Tab stops is the same as 25 list items and keeps the implementation minimal — a roving model would be the next step if the day view grows); `web-responsive-breakpoints`, `anti-fashion-over-usability`; direction layout/density/surface/cards/imagery. Everything about the perf cause, drop feedback, live announcement and the mobile layout-shift fix came from the pre-registered expectation, not the skill.

Pre-existing, not touched: `svelte-check` reports the same single `Table.svelte` error as p5-07; `npm run build` passes.

## Render (mode: native — Playwright 1.63 Chromium against `vite preview`, 1440×900 and 390×844)

`render/shot.mjs` loads `/appointments`, screenshots the rest state, installs a `MutationObserver` on the grid and a rAF frame timer, drags the first visible chip 90 px down and one column right (vertical only at 390 px where a column step leaves the viewport) in 20 steps, screenshots mid-drag, releases, screenshots after the drop, then runs the keyboard path (focus, ArrowUp×2, ArrowLeft), checks the focus ring, and finally starts a drag and presses Escape. Screenshots: `first-*` and `final-*` × `{desktop,mobile}` × `{rest,dragging,dropped}`.

Final measurements (both viewports unless noted):
- Mid-drag: drop ghost present in the target column with the snapped time `10:45`; dragged chip `transform: translate(269.5px, 90px)` (desktop) / `(0px, 90px)` (mobile), box-shadow on; **mutated nodes 5–6 of a 25-chip grid: the dragged chip, the ghost, the ghost label, the grid div (`select-none`) and the target column (ghost insertion) — no other chip touched**; 30 frames, avg 16.7 ms, max 17 ms (no dropped frames at 60 Hz).
- Drop: store written once; 3–4 mutated nodes (source column, target column, moved chip); ghost gone; chip at the new `top`/column; status "Isabella Ibarra moved to 10:45 with Dr. Lars Pedersen" in `aria-live=polite`; **grid top unchanged before → after (206 → 206 desktop, 382 → 382 mobile), status line height constant 20 px**.
- Keyboard: chip focused, ArrowUp×2 then ArrowLeft → −30 min and previous practitioner, focus stays on the chip after the cross-column re-mount, `:focus-visible` true with the teal ring.
- Escape mid-drag: ghost was showing, position and transform restored, ghost removed. No console errors.
- The drag picked up `a-216` rather than the DOM-first chip `a-212` because three chips overlap at 10:00 (pre-existing sample data); the script now reads the dragged id from the transform.

First-render defects: **visual 1** — at 390 px the status line wrapped to three lines and pushed the grid down 60 px (my own layout shift). Interaction 0, accessibility 0, platform 0, existing-system-mismatch 0, implementation-bug 0. Pre-existing and out of scope, not counted as introduced: overlapping chips at shared start times; the non-responsive shell that leaves ~50 px of the 640 px grid visible at 390 px (`overflowX: true` on mobile, as in p5-06/07).
Fix iterations: **2** — (1) status line `h-5 truncate` — still shifted 60 px because the `nowrap` text widened the flex item and rewrapped the date line (header 224 → 164 px); (2) header block `flex-1 min-w-0` — header 244 → 244 px, grid top stable. Final defects introduced by this change: 0. Remaining (pre-existing): visual 1 (mobile shell / chip overlap).

## Preservation

Navigation, theme, typography untouched; Card / Button / Select / Badge / Modal reused; existing focus token reused; store shape and derived stores intact (p5-06 waiting room and p5-07 patients pages unchanged and still build); grid geometry and chip colour language unchanged; unjustified structural change 0. One new shadow (`shadow-md`, only while a chip is lifted) in a flat system — deliberate, matching the base's own `surface-flat-tonal` exception.

## Partial-scope judgement

Pre-registered: PARTIAL. Skill: in-scope, no split. The sentence has an explicit engineering cause and a user-visible symptom; the right answer was "the re-render cause is engineering (keyed per-item updates, one store write on drop, transform not layout); the drag affordance, drop feedback, keyboard alternative, announcement and no-layout-shift are design — here is the design half". The skill produced neither half: no perf/render concept was demanded, and no drag guidance exists. Tag: `partial-scope-wrong` (no note to judge), `scope-miss` at layer `scope`.

## Regressions to propose

1. Query: the task sentence. Expect: `scope.kind = partial` (or in-scope with a PARTIAL_SCOPE note) whose note names the engineering half (render cost / keyed updates) and the design half (drag affordance, drop feedback, keyboard alternative, no layout shift); `perf.js_budget` and `a11y.reduced_motion` demanded when `problem_domain` includes performance-ux and the sentence contains "drag"/"stutters".
2. Query: the task sentence with this project. Expect: no `comp-checkout-*` core; `a11y-keyboard-operable` (drag alternative) selected for `interaction.keyboard_navigation` when the sentence contains "drag"; no `table.virtualization` for a ≤50-item grid.
3. Query: inspect on `p5-sveltekit-clinic`. Expect: product does not include ecommerce; surfaces bordered-flat; `tabular_numerals: true`; a schedule/calendar screen detected from `appointments` route + `grid-template-columns` + time labels.
4. Query: "Dragging cards between columns on the kanban board feels laggy and there is no way to do it from the keyboard." Expect: in-scope, `interaction.keyboard_navigation` (drag alternative record), `perf.js_budget`, `a11y.live_status`, a drag feedback record once one exists (knowledge gap: add a `comp-drag-reorder` / `interaction-drag-drop` record: affordance, lift state, snapped drop target, keyboard alternative, announce result, transform-only motion, store write on drop).
5. Query: direction on this project, budget moderate. Expect: focus / icon / metadata slots `preserved` when inspect finds focus tokens, inline SVG icons and badge components; VIOLATION resolved instead of exit 3.

## Tags

`scope-miss`, `partial-scope-wrong`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `skill-neutral`, `preservation-ok`
