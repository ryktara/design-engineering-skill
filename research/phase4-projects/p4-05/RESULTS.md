# p4-05 — exceptions first (GridSense energy dashboard)

**Task:** "facility managers don't notice new alerts; make exceptions the first thing they see on the dashboard without redesigning it"
**Project / stack / platform:** `phase3-projects/p3-react-dashboard-polish/project` (state after p4-04) · React 18.3 + esbuild, plain CSS tokens · web
**Existing UI:** yes — Alerts module was the last section on the page and its data was `[]`
**Render mode:** native (esbuild → Playwright Chromium, `file://`, 1440×900 + 390×844; states t0 / arrived / acknowledged / clear)

## 1. Design context — detected vs actual
Same inspection as p4-04 (identical project); the table there applies: navigation yes, theme yes, surfaces yes, radius yes, spacing partial (false Tailwind, 20 in evidence), typography no (declared `--font-ui` not detected), components no, product hints none.

## 2. Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)

| field | value | verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope | right |
| mode / evidence | audit + refactor: "problem statement on existing UI", "fix follows the diagnosis" | right — the key check for this case; not create |
| platform / stack / screen | web, react, dashboard | right |
| product | iot (from "facility managers") | right (vocabulary fix since Phase 3) |
| components | [notification] | partial — alerts ≈ notification, but what is needed is an alert **region** with priority and a live announcement |
| jobs / primary_jobs | monitor / monitor, "audit dashboard" | right |
| problems | [] | **wrong** — "don't notice" is a salience / visual-hierarchy problem; nothing captured |
| density | null | fine |
| risk | low | fine |
| change_budget | low | right — "without redesigning it" |
| intent.preserve | [] | **wrong** — "without redesigning it" should preserve layout, navigation, theme, component language |
| constraints | preserve_existing_system: true | right |
| missing | [] | fine |

## 3. Guidance verdict (`03-guidance.md`, bundle 6 = core 4 + guardrails 2; concepts 10/10, ≈806 tokens, coverage/1k 12.41, purity 0.94; required concerns accessibility, interaction, component, data-display; **feedback and states only "recommended"**)

| record | role | verdict | note |
|---|---|---|---|
| dir-analytical-console | core | partial | "accent reserved for alerts and selection" is on point; "dark-first tonal surfaces" is not (light theme, low budget) |
| comp-kpi-tile | core | off-target | KPIs are not part of this task |
| comp-chart-container | core | off-target | chart untouched; selected "for accessibility coverage" |
| chart-realtime | core | partial | carries `data.exception_first` and "alert states via colour + icon + text" — the only bundled record that mentions exceptions — but it is a real-time chart record |
| a11y-keyboard-operable | guardrail | relevant | Acknowledge reachable by Tab, activated with Enter |
| a11y-focus-visible | guardrail | relevant | 2 px ring on the button |

Relevant 2 · partial 2 · off-target 2. Nothing in the bundle says "announce it", "put it at the top of the region it concerns", "one action", or "reserve the slot so nothing shifts".

Missing guidance (all present in the base, none selected at the default size):
- `a11y-live-status` — polite live region with a complete phrase; appears only at `--size 12`. The task's core accessibility need. **Layer: concerns** (feedback derived as RECOMMENDED, so the concept was never required) → bundle-selection.
- `comp-toast-notification` — "Banner: inline at the top of the region it concerns, dismissible if non-critical"; rank 3 in a targeted search, not in the bundle. **Layer: candidate-retrieval.**
- `layout-hierarchy-one-thing` — carries `data.exception_first` and `layout.focal_hierarchy`; not in the bundle or the top 12 of the task search. **Layer: bundle-selection** (the concept was credited to `chart-realtime` instead).
- `web-cls-and-lcp` — layout shift; rank 8 in the task search, not selected. **Layer: bundle-selection.**
- `cta-single-primary`, `a11y-color-not-only` — not selected. **Layer: bundle-selection.**
- Knowledge gap: no record describes a persistent **exception / alert strip** on a dashboard (severity ranking, acknowledge flow, fixed slot, "n more open"); `comp-toast-notification` covers banners in one sentence. **Layer: expected-concepts (knowledge-gap).**

## 4. Direction verdict (`04-direction.md`, validation OK, budget low, preserved [navigation, density, surface, color], changed [])

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-top-bar (preserve) | preserved | yes |
| layout | layout-dashboard-grid | new | yes (existing) |
| density | preserve spacing base 4 | preserved | yes — the low budget correctly locked density |
| surface | surface-bordered-panes (preserve) | preserved | yes |
| cards | card-flat-tile ("no border unless contrast < 1.2:1") | new | **no** — existing modules are bordered; a flat tile would be an existing-system mismatch. Ignored |
| typography | typography-geometric-sans (Manrope/Outfit/…) | new | **no** — existing Inter/Segoe; a font change under a "do not redesign" budget. Ignored; only "new" because inspect did not detect the font |
| color | color-neutral-accent (preserve) | preserved | yes |
| motion / focus | functional-minimal / ring | new | yes |
| cta | cta-contextual-inline | new | partial — "actions visible, at most one emphasised per item" fits the strip; does not say the alert must be the focal point |
| imagery / icon / metadata | data-graphics / outline / moderate ("status via badge + text") | new | yes |

Preserved 4 by repository evidence; 2 of the 9 "new" slots (cards, typography) would break the existing system and are invisible to validation because inspect reports no typography or component evidence.

## 5. Implementation (files changed; originals in `before/`)

- `src/data.js` — `alerts` now holds one critical alert (Cold store 2 meter offline, matching the meter list's fault); `incomingAlerts` simulates a pushed warning 2 s after mount (Chiller plant above threshold, matching its warning status).
- `src/components/ExceptionStrip.jsx` (new) — `<section aria-labelledby="exceptions-h">` placed directly under the page head, before the KPIs. Fixed height (`--exc-h`: 72 px desktop, 156 px ≤640) so arrivals change text, never layout. Shows the highest-severity open alert: severity chip (reuses `.status-text` + `status-fault/-warn` glyph+label), title, meter · since · detail, "n more open" link to the Alerts module, and **one** action ("Acknowledge", `.btn.secondary`). `role=status aria-live=polite aria-atomic` text: "New warning: Chiller plant demand above threshold. 2 open exceptions: 1 critical, 1 warning." Clear state ("No open exceptions", success-coloured edge) keeps the same slot.
- `src/components/AlertsWidget.jsx` — list rows with severity chip, title, meta, tertiary Acknowledge; acknowledged rows stay, muted; empty state unchanged.
- `src/App.jsx` — alert state, arrival timers, `acknowledge(id)`; strip inserted after `.pagehead`; nothing else moved.
- `public/styles.css` — `--exc-h` token; `.exceptions` (tinted by severity: error-bg + 4 px error edge, warning-bg + warning edge, success edge when clear), `.exc-*`, `.alert*` rows, phone layout (stacked, full-width button, 2-line clamp on meta).
- Top bar, promo slot, page head, KPI/chart/meters modules untouched.

Judgement call: the page keeps "Export report" as its single filled button; the strip's action is a bordered secondary so the page still has one primary (the interaction test enforces both "one action in the region" and "one `.btn.primary` on the page"). Making Acknowledge the primary would have re-ranked the page head, which the budget forbids.

## 6. First-render defects (`render/first-*.png`, `05-interaction-first.json` 9/10 at both viewports)

| type | defect |
|---|---|
| accessibility | inline links in the strip ("Alert history", "1 more open") measured 16 px tall (< 24 px) |
| visual | phone: the meta line was clamped to one line with an ellipsis, hiding the "1 more open" link |
| existing-system-mismatch | the strip's Critical chip was filled solid red with white text; every other status chip in the product is a tinted chip with dark text |

## 7. Final defects (`render/final-*.png`, `05-interaction-final.json` 10/10 at both viewports)

| type | defect |
|---|---|
| visual (remaining) | in the warning-only state the strip's amber tint is the same as the promo banner's, so two amber bands stack under the top bar; the promo is outside this task's scope (`anti-interruptive-upsell` would demote it) |

## 8. Iterations
1. first — implementation (9/10).
2. final — links get `min-height: 24px`; chip reverts to the tinted system chip; phone slot 156 px with a 2-line meta clamp (10/10).

## 9. Interaction test summary (final; 1440×900 and 390×844 identical results)
Region: `<section aria-labelledby>` named "Exceptions", first section in `<main>` (index 2 after the page head and the compare status), before the KPIs · live region `role=status aria-live=polite`: "1 open exception: 1 critical." → on arrival "New warning: Chiller plant demand above threshold. 2 open exceptions: 1 critical, 1 warning." → after acknowledging both "No open exceptions." · featured alert is the critical one while it is open, then the warning, then the clear state · one `<button>` in the region; one `.btn.primary` on the page ("Export report") · layout shift on arrival / acknowledge / clear: 0 px for page head, strip, KPIs, chart, meters; strip height constant (72 / 132→156 px) · Alerts list 1 → 2 rows, 2 acknowledged at the end · Acknowledge reached in 9 Tabs with a 2 px ring; Enter acknowledges · every chip has text · no target < 24 px · top bar links/colours and canvas unchanged; page head still first; one h1.

## 10. Preservation verdict
Navigation, theme, typography, spacing, module language kept; the strip is built from existing tokens (`--color-feedback-*-bg`, `--color-border-default`, `--radius`, `.status-text`, `.btn.secondary`). One structural addition (a fixed-height region inserted after the page head) — justified by the task ("first thing they see"). Nothing was moved or removed. Unjustified structural changes: 0.

## 11. Regressions to propose
- query "facility managers don't notice new alerts; make exceptions the first thing they see on the dashboard without redesigning it" → expect mode audit/refactor (holds); `intent.preserve` non-empty; `problems` includes hierarchy/salience; concern **feedback REQUIRED**; bundle contains `a11y-live-status`, `comp-toast-notification` (banner clause), `layout-hierarchy-one-thing`, `web-cls-and-lcp`; `comp-kpi-tile` and `comp-chart-container` absent.
- query "alert banner at the top of a dashboard with one action, announced to screen readers, no layout shift" → expect a record for a persistent exception strip (currently none).
- direction with change_budget low on a project with bordered modules → expect cards ≠ flat-tile and typography ≠ a new family.

## 12. Tags
`requirements-miss` (problems empty, preserve empty) · `concept-miss` (feedback concern only recommended) · `ranking-miss` (a11y-live-status, comp-toast-notification, layout-hierarchy-one-thing, web-cls-and-lcp, cta-single-primary) · `knowledge-gap` (exception strip / alert region pattern) · `direction-mismatch` (card-flat-tile, typography-geometric-sans) · `context-detection-miss` (typography, components) · `render-defect-fixed` · `render-defect-remaining` · `skill-helped` (mode detection, low budget locking density, keyboard/focus guardrails) · `preservation-ok`
