# p4-04 — compare-to-last-week view (GridSense energy dashboard)

**Task:** "add a compare-to-last-week view to the energy dashboard KPIs and the hourly chart, keeping the existing top bar and light theme"
**Project / stack / platform:** `phase3-projects/p3-react-dashboard-polish/project` · React 18.3 + esbuild bundle, one plain CSS file with `:root` tokens · web
**Existing UI:** yes (Phase 3 result: dark top bar, light canvas, bordered white modules, KPI divider grid, hand-rolled SVG chart)
**Render mode:** native (esbuild build → Playwright 1.63 Chromium, `file://…/public/index.html`, 1440×900 and 390×844, both comparison states)

## 1. Design context (inspect) — detected vs actual

| field | detected | status | actual (read from `styles.css` / `App.jsx`) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | 52 px dark top bar, 4 destinations, active = underline + aria-current | yes |
| theme | light-first | INFERRED | light canvas `#f4f6f8`, white surfaces, dark chrome only in the bar | yes |
| surfaces | bordered-flat | INFERRED | `.module`: white, 1 px `--color-border-default`, no shadows | yes |
| radius | small (6) | INFERRED | `--radius: 6px`; 999 px only on status chips | yes |
| spacing | 4 ("most used [4, 8, 12, 16, 20]", "tailwind spacing classes (5)") | INFERRED | `--sp-1…--sp-12` = 4/8/12/16/24/32/48; no Tailwind anywhere (no dependency, no utility classes) | partial — base right, evidence wrong (20 is not in the scale; Tailwind is a false positive that also leaks into `css_architecture: "tailwind-classes (1 files)"`) |
| typography | unknown | UNKNOWN | `--font-ui: Inter, "Segoe UI Variable", "Segoe UI", system-ui` on `:root`, applied through `font-family: var(--font-ui)`; size roles `--fs-*`; tabular numerals | no — declared, but the detector does not follow the custom-property indirection (`fonts: []` too) |
| components | unknown | UNKNOWN | `.btn` primary/secondary/tertiary/icon, `.module`, `.kpi`, `.status-text` chip, `.meter` row, `.promo` | no |
| product_hints | [] | — | energy monitor: kWh/kW, meters, carbon intensity, site name | no (same miss as Phase 3) |

## 2. Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)

| field | value | verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope | right |
| mode | create ("default (no mode cue)") | acceptable — a new view inside an existing screen; but the evidence string says the classifier saw nothing, not that it recognised "add … view" |
| platform / stack | web (project), react (project) | right |
| product | finance (from "kpi"), iot (from "energy") | half wrong — "kpi" ≠ finance; the wrong family then drives `density=high` |
| screen / subtype | dashboard / **calendar** | subtype wrong — "last week" was read as a calendar screen |
| components | [chart] | partial — "KPIs" in the sentence did not yield a KPI component |
| jobs / primary_jobs | compare / compare, "create dashboard" | compare right; "create dashboard" wrong (it exists) |
| density | high (implied by finance) | wrong — existing UI is medium (24 px insets, 40 px rows) and the task says keep it |
| change_budget | moderate | right |
| intent.preserve | [] | **wrong** — "keeping the existing top bar and light theme" names two things to preserve; `negative_constraints` is also empty. The direction step preserved navigation only because the repository said top-bar, not because the request did |
| project_context | copied from inspect | as above |
| constraints | preserve_existing_system: true | right |

## 3. Guidance verdict (`03-guidance.md`, bundle 7 = core 4 + guardrails 3; metrics: concepts 9/9 covered, ≈952 tokens, coverage/1k 9.45, purity 0.9, uncovered required concerns none)

| record | role | verdict | note |
|---|---|---|---|
| comp-kpi-tile | core | relevant | "comparison (vs previous period) with sign + arrow + colour, consistent precision" — used directly; also the only record that says what a period comparison looks like |
| comp-chart-container | core | relevant | title states the question, unit/time range, direct labels instead of a legend, table alternative, no refresh animation — all applied |
| layout-dashboard-grid | core | partial | true, but already implemented in Phase 3; adds nothing to a compare view |
| dir-analytical-console | core | partial | "modules sized by importance, large numerics" fine; "dark-first tonal surfaces" contradicts "keeping the light theme" |
| anti-generic-sidebar-dashboard | guardrail | off-target | selected "for request wording"; the request is not building a dashboard skeleton |
| a11y-keyboard-operable | guardrail | relevant | drove the native-radio segmented control (arrow keys, no roving-tabindex code) |
| a11y-focus-visible | guardrail | relevant | ring on the option label via `input:focus-visible + span` |

Relevant 4 · partial 2 · off-target 1.

Missing guidance:
- `chart-trend-line` — "line per series with distinct style (colour + dash/marker), direct end labels instead of a legend" is exactly the second-series guidance this task needs. Present in the base; top hit for a targeted search; omitted from the bundle as "same category as a core pick" (deduplicated against `comp-chart-container`, which does not cover multi-series styling). **Layer: bundle-selection (ranking-miss).**
- A view switch / segmented control (period selector) — no record exists; `comp-tabs` is the nearest (search on "segmented control to switch a view" returned ABSTAIN). **Layer: expected-concepts (knowledge-gap).**
- `nav-orientation-and-back` ("URL/route reflects state") — present, rank 3 in a targeted search, not in the bundle. Minor. **Layer: candidate-retrieval.**
- `data-tables-numeric` (signed differences, tabular alignment for the new Difference column) — present, not selected. **Layer: bundle-selection.**

## 4. Direction verdict (`04-direction.md`, validation OK, budget moderate, preserved [navigation, surface, color], changed [])

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-top-bar (preserve) | preserved | yes — matches the repo (fix of the Phase 3 left-rail miss) |
| layout | layout-dashboard-grid | new | yes (matches existing) |
| density | density-high | new | **no** — existing is medium; "finance" inference. Ignored |
| surface | surface-bordered-panes (preserve) | preserved | yes |
| cards | card-bordered | new | yes (existing modules are bordered) |
| typography | typography-neutral-sans | new | compatible ("if the codebase already uses a system font, keep it") — but only "new" because inspect did not detect the declared Inter/Segoe stack |
| color | color-neutral-accent (preserve) | preserved | yes |
| motion | motion-functional-minimal | new | yes |
| focus | focus-ring-standard | new | yes (matches the existing 2 px ring) |
| cta | cta-toolbar-commands | new | **no** — selection-driven command bar for a page with one primary action. Ignored |
| imagery | imagery-data-graphics | new | yes |
| icon | icon-outline-system | new | n/a |
| metadata | metadata-rich | new | no — column visibility/order controls are not this task. Ignored |

Preservation metrics: 3 preserved by repository evidence, 0 changed. Two of the ten "new" slots contradict the existing UI (density, cta); they are not flagged because inspect has no evidence for those slots, so the compatibility check has nothing to compare against.

## 5. Implementation (files changed; `before/` holds the originals)

- `src/data.js` — `comparePeriods` (yesterday / same day last week), each KPI carries `yesterday` and `lastweek` reference values (deltas derived, so the existing "vs yesterday" numbers are unchanged), `hourlyDemandCompare` with 24 points per period.
- `src/components/CompareSwitch.jsx` (new) — "Compare with" radiogroup of native radios styled as a segmented control; selected = weight + selection background + checked state.
- `src/components/KpiGrid.jsx` — delta computed against the selected period; new muted reference line ("Same day last week: 17,690.2 kWh") with tabular figures.
- `src/components/DemandChart.jsx` — second series as a dashed 2 px line in `--color-chart-compare` (#6b7280, 4.8:1 on white), direct end labels ("Today" / "Last week") pushed apart when the series end close together, wider right gutter when a second series is drawn, y-axis top from both series, summary sentence extended with the reference peak/average, data table gains "… kW" and "Difference" columns.
- `src/App.jsx` — period state in the URL hash (`#compare=lastweek`, `replaceState`), `role=status` announcement, module headings carry the period ("Today vs last week").
- `public/styles.css` — `--color-chart-compare` token; `.compare`, `.segmented`, `.seg` rules (30 px option height desktop, 40 px + full width ≤640); `.kpi-ref`; `.chart-line-compare`, `.chart-series-label`; `.module-ctx`.
- Top bar, promo slot, tokens, module language, meters and alerts untouched.

## 6. First-render defects (`render/first-*.png`, `05-interaction-first.json` 10/10)

| type | defect |
|---|---|
| visual | chart heading context "today and same day last week" was wordy and wrapped to two lines on the phone while the KPI heading used "vs last week" |
| implementation-bug | summary sentence read "today's average is 0.0% higher" for the yesterday period (rounded delta of zero) |

No interaction, accessibility, platform or existing-system-mismatch defects on the first render.

## 7. Final defects (`render/final-*.png`, `05-interaction-final.json` 10/10)

None found at the two rendered viewports. Unverified: widths between 640 and ~1100 px where the page head now has three flex children (title, compare control, actions) and may wrap; screen-reader pass; 200 % zoom.

## 8. Iterations
1. first — full implementation (10/10 checks).
2. final — both module headings use `compare.short`; zero delta worded as "about the same" (10/10).

## 9. Interaction test summary (1440×900, final)
Compare switch reached in 7 Tabs, ring on the option label (2 px, `#1d4ed8`), ArrowRight selects "Same day last week", ArrowLeft returns, hash `#compare=lastweek` · KPI deltas change from "vs yesterday" to "vs last week" with a reference line for every KPI · chart: 2 `<path>`, end labels [Today, Last week], 4 table columns, summary mentions the period, SVG `<title>` updated · status text "Comparing today with same day last week." · switching the period moves no module (0 px on main, KPIs, chart, meters, alerts) · one `.btn.primary` ("Export report") · no target under 24 px · all numeric nodes tabular · top bar links and colours identical to before (`rgb(15,23,42)` bar, `rgb(244,246,248)` canvas) · Tab order: Overview → Meters → Reports → Settings → Learn more → Dismiss → Yesterday/Same day last week → Run optimisation → Export report → Show hourly data → Add meter → Alert rules, ring on every stop.

## 10. Preservation verdict
Navigation, theme, typography, spacing scale, module/button/chip language all kept; the new control reuses `--color-border-strong`, `--color-selection-bg`, `--radius`, `--dur-fast`. No structural change to the page (one control added to the existing page head, one line added per KPI, one series added to the chart). Unjustified structural changes: 0. The direction's density-high / toolbar-commands / metadata-rich choices were not followed.

## 11. Regressions to propose
- query "add a compare-to-last-week view to the dashboard KPIs and the hourly chart, keeping the existing top bar and light theme" → expect `intent.preserve` ⊇ {navigation, theme}; `screen_subtype` not calendar; product not finance from "kpi"; density not high without evidence; bundle contains `comp-kpi-tile` **and** `chart-trend-line` (multi-series styling must not be deduplicated away by `comp-chart-container`).
- query "period selector / segmented control to switch a dashboard view" → expect a component record for a view switch (currently ABSTAIN).
- inspect on a project whose font is declared as `--font-ui: Inter, …` → expect `typography` KNOWN and `fonts` non-empty; expect no `tailwind-classes` finding when no Tailwind dependency or utility classes exist.

## 12. Tags
`requirements-miss` (preserve/negative constraints empty, calendar subtype, finance product, density) · `ranking-miss` (chart-trend-line dedup, data-tables-numeric, nav-orientation) · `knowledge-gap` (view switch / segmented control) · `context-detection-miss` (typography, components, false Tailwind) · `direction-mismatch` (density-high, cta-toolbar-commands, metadata-rich) · `render-defect-fixed` · `skill-helped` (kpi-tile comparison spec, chart-container direct labels + table alternative, keyboard/focus guardrails) · `preservation-ok`
