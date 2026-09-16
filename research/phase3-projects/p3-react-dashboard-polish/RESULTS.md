# p3-react-dashboard-polish — results

## Task
"our React energy dashboard looks cramped and inconsistent, facility managers complain the numbers are hard to read and they don't know which button to press"

Polish/audit case. The project was created from scratch under `project/` as an existing-looking GridSense energy dashboard (React 18, JSX compiled by esbuild, no CDN, one CSS file, no token layer) with eight defects baked in: spacing mix 6/10/14/22 px, KPI tiles as cards inside the "Today" card and the chart in a card inside a card, three `.btn.primary` buttons in the page header (plus a fourth primary in the promo banner), KPI values in proportional figures with left/right/centre alignment mixed per tile, colour-only status dots, an SVG chart with no role/name/summary, an Alerts widget that renders an empty `<ul>` when the API returns `[]`, and a promo banner inserted 800 ms after mount that pushed `<main>` down 52 px.

## Stack / platform
web · React 18.3.1 + react-dom, esbuild 0.24 bundle (`npm run build` → `public/bundle.js`), plain CSS. Rendered natively in Playwright 1.63 Chromium from `file://…/public/index.html` at 1440×900 and 390×844. `render_mode: native`.

## Inspection verdict (`01-inspect.json`)
- Right: stack react (KNOWN from package.json), platform web, css_architecture ".css (1 file)", fonts Inter, component_dirs `src/components/ (5 files)`, tokens [] (true: none existed), package_manager npm.
- Missed: product domain (no `product_hints` although `index.html` says "Energy Monitor" and `data.js` has kWh/kW/meters/carbon — the requirements step therefore had `product=[]`), the esbuild build step (no "build tool" finding), the hand-rolled SVG chart (a data-viz hint would have pulled chart guidance), the navigation model (a top bar with 4 destinations is visible in `App.jsx`; not reported, so the direction step could not reconcile its `nav-left-rail` choice against it).
- Odd: `focus_handling: ["explicit focus handling in 0 files"]` reads as a finding when it is an absence.

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| field | value | verdict |
|---|---|---|
| mode | polish, audit | right — key check for this case; "looks cramped / inconsistent / hard to read" mapped to polish with audit following. Not create. |
| platform | web (KNOWN, inspection) | right |
| stack | react (KNOWN, request) | right |
| screen | dashboard (KNOWN) | right |
| input | keyboard, pointer, touch (INFERRED) | right |
| product | [] | wrong/missing — "energy dashboard", "facility managers" not recognised (vocabulary gap: no energy/facilities/utilities vocabulary) |
| jobs / primary_jobs | [] / "polish dashboard" | missing — the request names two user complaints (read numbers, choose an action); neither became a job |
| components | [button] | partial — "numbers" should have implied KPI/numeric display; chart not inferable from request (but was in the repo) |
| problems | general, visual | partial — "hard to read" is a readability/typography problem and "don't know which button to press" is an action-hierarchy problem; both collapsed into "visual" |
| density | null | acceptable (nothing to derive it from) |
| risk | low | acceptable |
| constraints | preserve_existing_system: true | right |
| MISSING | brand | right; but "users = facility managers" should have been KNOWN, not absent |

## Guidance verdict (`03-guidance.md/.json`, bundle 7 = core 3 + guardrails 4, coverage 1.0)
| record | verdict | note |
|---|---|---|
| comp-kpi-tile (core) | relevant | tabular figures, sign+arrow+colour delta, consistent precision, lead KPI larger — used directly |
| dir-analytical-console (core) | partial | "large readable numerics, modules sized by importance" relevant; "dark-first tonal surfaces, signature numeric typeface" off for an existing light-themed tool being polished |
| layout-dashboard-grid (core) | relevant | "each module … its own loading/empty/error states" and "a divider grid with headings is often clearer than nested boxes" — the only place empty states and nested boxes were mentioned |
| anti-inconsistent-spacing (guardrail) | relevant | exact diagnosis of the 6/10/14/22 mix; does not itself give the scale |
| a11y-keyboard-operable (guardrail) | partial | true but not part of the complaint; no composite widgets on this page |
| layout-hierarchy-one-thing (guardrail) | relevant | one focal point, "not the page title"; does not say "one primary button" |
| a11y-focus-visible (guardrail) | partial | useful (I added a 2 px ring) but not asked |

Relevant 4 · partial 3 · off-target 0.

Knowledge gaps (needed, absent from the base): none found. Every topic I needed exists: `cta-single-primary`, `a11y-color-not-only`, `comp-empty-state` / `layout-states-empty-loading-error` / `anti-no-states`, `anti-card-everything` / `card-none`, `a11y-labels-names` / `comp-chart-container`, `data-tables-numeric`, `layout-spacing-scale`, `web-cls-and-lcp` / `anti-interruptive-upsell` (verified with targeted `search` calls).

Ranking misses (in the base, not selected at default size; `search -k 12` on the task sentence shown in brackets):
1. `cta-single-primary` — the request literally says "don't know which button to press"; not in the bundle, not in the top 12 of search, and the direction chose `cta-contextual-inline` over it (alternative score 0.253). Biggest miss of the case.
2. `layout-spacing-scale` — search rank 3 (0.389) but omitted from the bundle; the bundle had the anti-pattern without the scale.
3. `data-tables-numeric` — search rank 10; only appears in the bundle at `--size 14`. Carries "tabular lining figures, right-align, never colour alone for negatives".
4. `a11y-color-not-only` — absent at default size, present at `--size 14`. The colour-only dots were a real defect.
5. `anti-card-everything` — absent from guidance and search; nested cards surfaced only through the direction's `card-none` slot text.
6. `layout-states-empty-loading-error` / `comp-empty-state` / `anti-no-states` — none surfaced; empty state only implied in one clause of `layout-dashboard-grid`.
7. `comp-chart-container` — explicitly "Omitted (redundant): same category as a core pick"; it was the record that carried chart accessible-name/summary guidance, and the core pick it was deduplicated against (`comp-kpi-tile`) does not cover charts.
8. `web-cls-and-lcp` — search rank 9; not in the bundle. Fair: the request does not mention the banner, so no lexical evidence; but an audit of a dashboard should carry a states/CLS guardrail.
Note: `nav-orientation-and-back` (search rank 4) and `nav-left-rail` (rank 11, and in the size-14 bundle) outrank all of the above for a polish request that never mentions navigation.

## Direction verdict (`04-direction.md/.json`, validation OK)
| slot | choice | verdict |
|---|---|---|
| navigation | nav-left-rail | wrong — the project has a top bar with 4 destinations; the skill's own web platform file says top bar for ≤5. Reason given is only "platform web, input …" (direction-invariant). Inspect does not report the nav model, so nothing could contradict it. Rejected; kept the top bar. |
| layout | layout-dashboard-grid | right |
| density | density-low | doubtful — an operations dashboard for facility managers wants medium density; "cramped" seems to have pushed to "spacious". Used medium (24 px insets, 40 px rows). |
| surface | surface-flat-tonal | right (white modules on a tonal canvas, no shadows) |
| cards | card-none | right — and its text ("remove nested rounded rectangles … single hairline between rows") was the most useful sentence for this case |
| typography | typography-serif-editorial | off-target — serif body for an energy ops tool; reason "platform web" only (invariant default). Kept the project's Inter/Segoe. |
| color | color-multicolour-semantic | off-target — status is a feedback role, not a category palette |
| motion | motion-functional-minimal | right |
| focus | focus-underline | off — a button-heavy dashboard needs the ring; reason again generic. Used a 2 px ring. |
| cta | cta-contextual-inline | wrong for the request; `cta-single-primary` was the alternative at 0.253 |
| imagery | imagery-data-graphics | right; "accessible alternatives (table or summary) for each chart" was applied |
| icon | icon-outline-system | fine |
| metadata | metadata-moderate | right — "status via badge + text; align numbers" |
Validation reported no violations. It did not flag serif-editorial + analytical-console, and cannot flag a navigation slot that contradicts the codebase because inspection does not capture navigation. Six of thirteen slots were selected by platform/input alone.

## Baseline (before polish) — measured by `render/interact.mjs`, `05-interaction-before.json`
9/12 checks failed: layout shift 52 px from the banner; 4 primary buttons; 0/5 status rows with text; KPI text-align {left, right, center}, no tabular figures; chart role=null, no name, no summary; Alerts `<ul>` with 0 items and no empty text; 5 nested `.card .card`; spacing values {6, 10, 14, 22} all off a 4 px scale; no reduced-motion rule. Passing: targets ≥24 px, one h1, Tab order (browser default focus ring only). Screenshots `render/first-*.png`; mobile shows the 4-column KPI grid overflowing its card and the site name overflowing the top bar.

## Implementation (following guidance, reconciled with the codebase)
- Token layer added to the existing `styles.css` (`:root` custom properties): spacing 4/8/12/16/24/32/48, semantic colour roles, type roles; no hex in components except the SVG which uses CSS classes.
- One surface level: `.module` sections with `aria-labelledby` headings; KPIs are a `<dl>` divider grid, chart has no inner box.
- One primary ("Export report"); "Run optimisation" secondary (bordered); "Add meter" moved into the Meters module header as tertiary; banner CTA became a text link and the banner is dismissible.
- KPI values: `font-variant-numeric: tabular-nums lining-nums`, all left-aligned, one precision per unit, unit as a smaller suffix, lead KPI 32 px others 28 px, delta = arrow + sign + value + "vs yesterday" in colour.
- Status: glyph (● ▲ ✖) + text chip ("Normal / Warning / Fault") + colour; null reading shown as "No reading".
- Chart: `<figure role=group>` → `<svg role=img aria-labelledby aria-describedby>` with `<title>`, gridlines, axes, peak annotation, `<figcaption>` sentence summary, `<details>` hourly table. Question answered: when did demand peak and how far above the low.
- Alerts: empty state with title, explanation, and a tertiary "Alert rules" link.
- Banner: `.promo-slot` renders immediately at final height (48 px; 64 px ≤640) so the async banner never moves `<main>`.
- Focus ring 2 px + offset via `:focus-visible`; `prefers-reduced-motion: reduce` zeroes transitions; responsive breakpoints 1100/900/640.
- `tokens.json` (semantic roles) validated with `tokens.py validate --platform web`.

## First-render defects (fix1, `render/fix1-*.png`, `05-interaction-fix1.json`)
1. `border.strong` #9AA3AD used as the secondary button edge measured 2.36:1 against canvas — FAIL from `tokens.py validate` (skill caught it).
2. Promo "Learn more" inline link 19 px tall (<24 px target check).
3. Mobile: SVG tick labels shrank to ~5 px because the 640-unit viewBox scaled down to 342 px.
4. Mobile: "Settings" clipped at the right edge of the top bar.
5. Mobile: banner text truncated with an ellipsis, hiding the "Learn more" link.
6. "Alert rules" tertiary button indented 9 px from the text edge above it.
7. (Tooling, not UI) reduced-motion check reported false because Chromium blocks `cssRules` on `file://` stylesheets.

## Final defects (`render/final-*.png`, `05-interaction.json`)
1. `border.default` #D9DEE5 at 1.25:1 — advisory WARN; module boundaries are carried by the white surface on the tonal canvas, hairlines are decorative. Accepted.
2. Mobile meter rows wrap the reading under the name; the two-line rows read slightly uneven against the single-height status chip.
3. Desktop: the Demand module (with summary and table toggle) is taller than Meters, leaving canvas below Meters.
Judgment call, not a defect: the promo banner is still above app content (`anti-interruptive-upsell` would demote or remove it); the task allowed "reserve space or remove", and I reserved. Unverified: screen-reader pass, 200 % zoom, dark theme (none exists in the project).

## Iterations
1. fix1 — full polish pass (all of "Implementation" above). 12-check result: 10 pass, 2 fail (targets, reduced-motion) + tokens.py FAIL on strong border.
2. final — strong border → #6B7280 (4.5:1); inline link and `summary` min-height 24 px; chart viewBox follows container width via ResizeObserver with fewer x-ticks <480 px; mobile nav scrollable, banner slot 64 px with wrapping text; `.flush` tertiary alignment; interaction test reads the CSS file from disk for the reduced-motion rule and compares normal (0.12 s) vs reduced (0 s) transition durations. Result: 12/12 pass, tokens.py OK (0 errors, 1 advisory).

## Interaction test summary (final, 1440×900)
layoutShift 0 px (main top 100 → 100 with banner present) · onePrimaryPerView 1 ("Export report") · statusNotColourOnly 5/5 rows have text · numbers: 42/42 numeric nodes tabular, KPI text-align one value, meter readings right edges equal (1371) · chart: role img, name "Demand, last 24 hours", summary sentence, data table present · alertsEmptyState present · targets: none <24 px · h1 = 1 · reducedMotion: rule present, 0.12 s → 0 s · spacing values {8, 12, 16, 24}, none off-scale · nestedCards 0 · Tab order: Overview → Meters → Reports → Settings → Learn more → Dismiss → Run optimisation → Export report → Show hourly data → Add meter → Alert rules, 2 px ring visible on every stop.

## Concurrency note
`design-engineering/scripts/de_core.py`, `data/rules.jsonl`, `data/lexicon.json` and several evals files were modified at 00:33–00:37 on 2026-09-09, inside this session, by another process (this run wrote nothing under the skill directory). My `02/03/04` outputs were generated at ~00:31 with the earlier version. Re-running requirements, guidance, and direction after the change: requirements identical; guidance and direction select the same records and slots, the only difference being new `_(covers: …)_` annotations on each guardrail. The verdicts above therefore hold for both versions. One nuance from the new annotation: `layout-hierarchy-one-thing` is now tagged "covers: … one primary action per view", so the bundler treats one-primary-action as covered by proxy while `cta-single-primary` (the record that actually says it) still is not selected. The targeted `search` calls and the `--size 14` run were made at ~00:33–00:35 and may straddle the change.

## Time spent (rough)
~50 min: 12 project, 8 skill steps + reading output, 15 implementation, 10 render/test/fix, 5 write-up.

## Failure taxonomy tags
`requirements-miss` (product/jobs/problems empty or coarse) · `vocabulary-gap` (energy / facility manager / "which button" not mapped) · `ranking-miss` (cta-single-primary, layout-spacing-scale, data-tables-numeric, a11y-color-not-only, anti-card-everything, empty-state records, comp-chart-container dedupe, web-cls-and-lcp) · `direction-invariant` (navigation, typography, focus, density chosen from platform alone; nav contradicts codebase) · `render-defect-fixed` · `render-defect-remaining` · `tooling-limit` (file:// cssRules) · `skill-helped` (mode detection correct; tokens.py caught a real contrast failure; kpi-tile / spacing / hierarchy / dashboard-grid / card-none / metadata guidance drove the fixes).
