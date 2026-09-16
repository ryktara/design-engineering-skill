# p4-02 — seat management table: accessibility review and fix (existing UI)

## Task
"accessibility review and fix of the seat management table: keyboard users can't reach row actions and the status column is colour only"

## Project / stack / platform
Same project as p4-01 (`p3-nextjs-saas`, Next.js 15 + Tailwind v4 + shadcn-style), run **after** p4-01's changes (before-copies in `before/` are the p4-01 final state). Web, existing UI. Render mode **native** (`next build` + `next start`, Playwright Chromium) at 1440×900 and 390×844.

## Design-context table
Identical inspect output to p4-01 (same repo, `01-inspect.json` copied): navigation left-rail KNOWN (partial — settings tab bar unreported), theme dual-theme light-first KNOWN (yes), surfaces flat-tonal UNKNOWN (no — bordered cards/tables), radius small INFERRED (yes), spacing 8 INFERRED (yes), typography custom INFERRED (partial — Geist unnamed), components KNOWN (yes).

## Audit finding first: the reported defects were not reproducible
Before touching code I ran the Phase 3 traversal against the p4-01 build (`../p4-01/05-interaction.json`): all 15 seat-table controls (7 role selects, 6 Remove, Resend, Reactivate) were plain `<button>`/`<select>` Tab stops with a visible ring, 0 hover-only controls, and every status badge already carried text ("Active" / "Invited" / "Deactivated") next to a coloured dot. So the two sentences in the task are false for this codebase as it stands. What *was* true, judged against the guidance and the a11y references:
1. The table produced **15 Tab stops** (8 rows × up to 3 controls) between "Invite member" and the invoice links — the `grid-single-tab-stop` guardrail says a table with row actions must be one stop with arrow-key access.
2. Status was text + a **coloured dot whose shape is identical for every status**: not colour-only (text is there), but the non-text cue was colour-only, and the row/dot pairing relied on hue alone (`a11y-color-not-only`, "status as text + icon").
3. The table had no accessible name / instructions of its own (section heading only), no `aria-rowcount`/row names.
4. If a member was removed from the dialog, the Remove button vanished and focus fell back to the section heading rather than the row.
5. "Resend" had no handler and announced nothing.

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| Field | Value | Verdict |
|---|---|---|
| scope | UI_ACCESSIBILITY, in_scope | right |
| mode | accessibility, audit | right ("audit: diagnose the reported defect") |
| problems / primary_jobs | accessibility; "accessibility table" | right |
| intent | existing, problem, facet accessibility, preserve [] | right (nothing to preserve was stated; preserve_existing_system=true covers it) |
| change_budget | low | right |
| components | table | right but incomplete (status badge, row actions, select) |
| screen / screen_subtype | [] | missing — the project's route `app/settings/billing` says settings/billing |
| platform / stack | web; nextjs react shadcn tailwind | right |
| product / density | finance, saas; high | finance/high still wrong (README "invoices"); no effect on this task |
| negative_constraints | [] | right |

## Guidance verdict (`03-guidance.md/json`)
Bundle 8 = core 2 + guardrails 6. Metrics: concepts 8/8, tokens≈1452, coverage/1k 5.51, purity 0.93, redundancy 0.47, uncovered none.

| Record | Role | Verdict | Why |
|---|---|---|---|
| `comp-plan-comparison` | core | partial | Selected on the lexical match "seat management"; its one relevant clause ("seat management is a data table … row actions reachable from the keyboard") restates the task. |
| `comp-data-table` | core | relevant | "row actions visible on focus as well as hover, keyboard grid navigation (arrows, Home/End)", `role=grid` when interactive. |
| `anti-hover-only-actions` | guardrail | relevant to the claim | Verified: 0 hover-only controls (claim false). |
| `grid-single-tab-stop` | guardrail | relevant — drove the fix | "Tab enters once and leaves once; arrows move between rows; row actions reachable when the row is focused; announce row index; keep a visible indicator on the active cell" — implemented literally. |
| `a11y-semantics-structure` | guardrail | relevant | `th scope`, table name, row names. |
| `a11y-contrast-text` | guardrail | relevant | Status text colours measured with tokens.py (see below). |
| `a11y-labels-names` | guardrail | relevant | Row `aria-label`, select and button names kept. |
| `layout-states-empty-loading-error` | guardrail | off-target | No state work in this task. |

Relevant 5, partial 1, off-target 1 (+1 relevant-to-claim).

Missing guidance:
- `a11y-color-not-only` — rank 6 in `search -k 12` (0.484, "Status, validation errors … never colour alone"); the request literally says "colour only" and it was not selected because `comp-plan-comparison` claimed the "no colour alone for status" concept. **Ranking miss** (bundle-selection).
- Nothing tells an *audit* to **reproduce the reported defect before fixing**; both false claims would have been "fixed" blind by a less careful run. **Knowledge gap** (audit-mode process rule).
- No recipe for "status chip = text + per-state icon *shape*" (dot vs check vs clock) — the difference between "not colour-only" and "shape-distinct". **Knowledge gap.**
- `a11y-focus-visible` not in the bundle (covered via `grid-single-tab-stop`'s clause); fine.

## Direction verdict (`04-direction.md/json`, validation OK)
Change budget low · preserved [navigation, density, typography, color] · changed []. New slots: layout-table-first (no — settings page), surface-bordered-panes (wrong reason, compatible outcome), cards card-list-row (irrelevant), motion/focus/icon fit, cta-toolbar-commands (no), imagery-data-graphics (n/a), metadata-rich (partial). Unjustified changes: 0 (nothing was changed); unjustified new choices: layout, cta, cards (3). For an accessibility task the direction adds nothing beyond the focus slot; the preserve mechanism did its job.

## Implementation
Files changed (copies in `before/`):
- `components/billing/seat-table.tsx` — `Table role="grid"` with `aria-labelledby="seats-heading"`, `aria-describedby` → sr-only keyboard instructions, `aria-rowcount`; rows get `data-seat-id`, `aria-rowindex`, an `aria-label` ("Marcus Ellery, Admin, Active"), **roving `tabIndex`** (one row 0, others −1) and a visible inset ring + `focus-within:bg-muted/50` row highlight; every select/button inside gets `tabIndex={-1}`; a `tbody` key handler implements ↑/↓/Home/End between rows (skipped when focus is on a native `<select>` so its own arrow behaviour survives), →/← between the row and its rendered, enabled controls (`offsetParent !== null` filters the breakpoint-hidden duplicate role select), Escape back to the row; `focusin` moves the roving index to the row the user last worked in (also after pointer use); dialog `onCloseAutoFocus` returns to the trigger, else the member's row (`id="seat-row-…"`), else the heading; "Resend" now announces via the existing live region. Status badges use per-state icons (CircleCheck / Clock / CircleMinus).
- `components/billing/status-badge.tsx` — `icon?: LucideIcon` prop (replaces the dot) so the shape differs per state; label remains the accessible name.
- `components/billing/invoice-history.tsx` — same chip with CircleCheck / CircleDashed / CircleAlert / Ban so both tables keep one status language (the p4-01 consistency result is preserved).
Not changed: `table.tsx`, routes, data, dialog copy, theme, navigation.

## First-render defects (`render/first-*.png`, `05-interaction-first.json`, `05-interaction-tab-first.json`)
None. The purpose-built grid test passed at both viewports on the first render: Tab enters the grid exactly once (row `u_01`, visible ring) and leaves to "Download invoice INV-2026-0042"; arrows reached 14/14 rendered controls (7 selects, 6 Remove, Resend, Reactivate — the owner row has none) with a visible ring on every row and control; Escape returns to the row; status 8/8 rows text + icon with 3 distinct shapes; remove dialog via Enter from an arrow-reached button, focus in, Escape closes, focus returns to the trigger. Page-level: 23 Tab stops (was 36) desktop, 19 (was 32) mobile, all with a ring; 0 hover-only; no horizontal overflow; 0 animated elements under reduced motion.

## Final defects
- accessibility 0, interaction 0, visual 0, platform 0, existing-system-mismatch 0, implementation-bug 0.
- Design trade-off, recorded: the grid pattern makes row actions *one arrow-key away* rather than *one Tab away*; discoverability rests on the sr-only instructions (`aria-describedby`) and the conventional grid semantics. Sighted keyboard users get the row ring + row highlight and the arrows work from the row.
- Native `<select>` inside the grid: ↑/↓ change the value (browser default) instead of moving rows; ←/→/Escape/Tab still work. Documented in the instructions ("Right and Left arrows to reach a member's role and actions").

## Iterations
1 render (no fix pass needed).

## Interaction test summary (`05-interaction.json` = final grid test; `05-interaction-tab.json` = page traversal)
| Check | 1440×900 | 390×844 |
|---|---|---|
| Grid Tab stops (enter once, leave once) | 1 → leaves to invoice download link | 1 |
| Controls reached by arrows / rendered controls | 14/14, 0 missing | 14/14 |
| Rows and controls with visible focus indicator | 8/8 rows, 14/14 controls | same |
| Escape from a control returns to its row | yes | yes |
| Status cells text + icon (distinct shapes) | 8/8; circle-check, clock, circle-minus | 8/8 |
| Remove dialog from arrow-reached button: opens, focus in, Esc closes, focus returns | yes | yes |
| Grid semantics | labelledby seats-heading, describedby present, rowcount 9, th scope=col 5/5, 8 rows named, 1 row tabindex=0, all controls tabindex=−1 | same |
| Page Tab stops (all with ring) | 23 (was 36) | 19 (was 32) |
| Contrast (tokens.py) | success #15803d 5.02:1, warning #a16207 4.92:1, destructive #dc2626 4.83:1, muted #71717a 4.83:1 on white (AA text and ≥3:1 non-text); dark: #4ade80 11.4:1, #facc15 13.0:1 on #09090b | — |

## Preservation verdict
Navigation, theme, typography untouched; component language kept (Badge/Button/Table primitives, existing ring token). Structural change: none visible; semantic change (grid + roving tabindex) is the task. Unjustified structural changes: 0.

## Regressions to propose
- query: "… the status column is colour only" → expect `a11y-color-not-only` in the bundle (not only the concept claimed by a component record).
- query: "accessibility review and fix of … : keyboard users can't reach row actions" → expect audit-mode guidance to state "reproduce the reported defect (keyboard traversal) before changing code; report if not reproducible".
- query: "seat management table" with project route `app/settings/billing` → expect `screen` = settings and `screen_subtype` = billing from project context.
- query: "status badge text plus icon" → expect a record that distinguishes colour-coded dot (shape identical) from per-state icon shapes.

## Tags
`requirements-miss` (screen empty; components incomplete), `ranking-miss` (a11y-color-not-only), `knowledge-gap` (reproduce-before-fix in audit mode; per-state icon shapes), `direction-mismatch` (layout/cta/cards slots irrelevant to an a11y task), `context-detection-miss` (as p4-01), `skill-helped` (grid-single-tab-stop and comp-data-table specified the fix exactly; contrast rule → measured values), `preservation-ok`. No render defects: neither `render-defect-fixed` nor `render-defect-remaining`.

## Provenance note
Nothing under `design-engineering/` was written by this task. Files there (`data/lexicon.json`, `data/rules.jsonl`, `data/patterns.jsonl`, `data/components.jsonl`, `data/antipatterns.jsonl`, `docs/USAGE.md`, `docs/MAINTENANCE.md`, `evals/development/*.json`) show mtimes 12:16–12:23 from another process; the skill commands for this task ran at 12:20–12:21 (inspect) and immediately after (requirements/guidance/direction/search), so the recorded outputs reflect the data as it was at that moment and may not reproduce byte-for-byte later.
