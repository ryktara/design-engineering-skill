# p5-05 — "Keyboard users can't get to the chart filters."

- **Task**: p5-05, sentence run verbatim.
- **Project / stack / platform**: `research/phase3-projects/p3-react-dashboard-polish/project` — React 18 + esbuild (`build.mjs` → `public/bundle.js`), plain CSS with custom-property tokens, static `public/index.html`. Platform web.
- **Existing UI or new screen**: existing UI (GridSense overview dashboard). The only chart-related filter is the page-level "Compare with" segmented control (`CompareSwitch.jsx`: native radios in `role=radiogroup`, inputs `opacity:0; position:absolute`, focus ring painted on the sibling span).
- **Build hash**: start `bf034323…f0d8` = end `bf034323…f0d8` (skill untouched).
- **Note on the session**: a previous agent completed steps 0–7 (expectation, inspect, requirements, guidance, direction, implementation, first render + keyboard check) and was interrupted before iterating and writing deliverables. I verified the implementation against `before/`, rebuilt the bundle (identical output), found one defect in the first render, fixed it, re-rendered, and wrote this file.

## Pre-registered expectation (00-expectation.json, written before any advise call)
platform web · existing · modes accessibility (audit/polish acceptable) · in-scope · expected concepts `interaction.keyboard_navigation`, `interaction.focus_visible`, `interaction.selection_visible`, `a11y.semantics`, `a11y.accessible_names`, `process.safe_modification` · critical `interaction.keyboard_navigation`, `interaction.focus_visible` · forbidden: TV/D-pad/touch-gesture/brand/landing/rail concepts.

## Design-context table (01-inspect.json vs the code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `.topbar` with 4 nav links, `aria-current` | yes |
| theme | light-first | INFERRED | light canvas `#f4f6f8`, white surfaces, dark chrome top bar only | yes |
| surfaces | bordered-flat | INFERRED | `.module` 1px border, no shadows | yes |
| radius | small | INFERRED ("most common radius 4 (1×)") | `--radius: 6px` everywhere, 999px pills; no 4px radius exists | partial (value right, evidence wrong) |
| spacing | irregular | UNKNOWN | explicit 4/8/12/16/24/32/48 scale as `--sp-1…--sp-12`, documented in a comment | partial (UNKNOWN + wrong value while the code is explicit) |
| typography | unknown | UNKNOWN ("no font family declaration found") | `--font-ui: Inter, "Segoe UI Variable", "Segoe UI", system-ui` at `:root`, six `--fs-*` sizes | partial (declaration exists, missed because it lives in a custom property) |
| components | unknown | UNKNOWN | 7 components in `src/components/`, `.btn primary/secondary/tertiary`, segmented radio control, `<details>` data table | partial |

Also: `focus_handling: explicit focus handling in 1 files` is reported but the global `:focus-visible` ring token (`--color-focus-ring`, styles.css:54) does not surface in `design_context`, so `direction` later marks the focus slot "new / no repository evidence" (see Direction).

## Requirements verdict (02-requirements.json)
- platform: `web`, `platform_evidence: []` but `known: platform=web (project inspection)` — correct.
- artifact_state `existing` — correct. operations `diagnose, modify` — correct. problem_domain `accessibility, interaction` — correct. change_scope `unknown` (intent.scope `moderate`) — acceptable.
- mode `accessibility, audit` with evidence "accessibility defect on existing UI / diagnose the reported defect" — correct (expected acceptable set).
- scope `in-scope`, domain UI_ACCESSIBILITY, reason "UI design / interaction task" — correct.
- change_budget `low` — correct. preserve `[]` (constraints.preserve_existing_system true) — acceptable.
- **miss (requirements layer)**: `components: [chart, search]` and `primary_jobs: [accessibility chart, accessibility search]`. "filters" was mapped to the *search* component; the page has no search. This seeded two off-target records downstream (comp-filters, search-filter-feedback).
- project_context echoes inspect (same partials as above).

## Guidance verdict (03-guidance.json/.md) — 8 records, ≈1015 tokens, status CONFIDENT

| record | role | verdict | note |
|---|---|---|---|
| comp-chart-container | core | partial | chart-a11y checklist; the chart already has role=img, summary figcaption, data table. Tooltip advice n/a (no tooltip). Not about reaching the filter. |
| comp-filters | core | off-target — `contradicts-codebase` | prescribes a faceted filter row with chips/popovers/mobile sheet for a two-option segmented radio. The record's own `avoid_when` ("One or two filters") applies. Following it would be a redesign under a low budget. |
| search-filter-feedback | guardrail | off-target — `generic` | debounce, result counts, search screen on TV; no search on the page. Its "filter state in URL" point is already implemented (`#compare=`). |
| a11y-keyboard-operable | guardrail | relevant | the critical concept; Tab order in visual order, arrow keys inside the group — matches the native radiogroup. |
| a11y-semantics-structure | guardrail | partial | harmless; confirms keeping native semantics. |
| a11y-nontext-contrast | guardrail | relevant | "≥3:1 against adjacent colours … visible focus" — this is exactly the defect found in the first render (skip-link ring on dark chrome at 2.7:1). |
| a11y-labels-names | guardrail | partial | radiogroup already `aria-labelledby`; nothing to change. |
| a11y-color-not-only | guardrail | partial | selected segment already weight + background + native checked. |

relevant 2 · partial 4 · off-target 2. Both core "what to build" records were wrong for the task; the fix came from reading the code, not from the core records. Platform filtering correctly excluded TV/kiosk/desktop/mobile-only records (none of the forbidden concepts were delivered).

**Concept recall** — delivered = union of `concepts` over the 8 selected records: a11y.color_not_only, data.chart_by_question, data.accessible_chart_alternative, state.loading_empty_error, data.filter_chips, navigation.deep_link_state, a11y.live_status, data.search_results, interaction.keyboard_navigation, interaction.hover_independence, a11y.semantics, a11y.contrast, interaction.focus_visible, a11y.accessible_names, interaction.selection_visible.

| expected id | delivered? | via | layer if missing |
|---|---|---|---|
| interaction.keyboard_navigation (critical) | yes | a11y-keyboard-operable | — |
| interaction.focus_visible (critical) | yes | a11y-nontext-contrast | — |
| interaction.selection_visible | yes | a11y-color-not-only | — |
| a11y.semantics | yes | a11y-semantics-structure | — |
| a11y.accessible_names | yes | a11y-labels-names | — |
| process.safe_modification | no | — | `expected-concepts` (not in `required_concepts`; the base carries it in `impl-safe-modification`, data/rules.jsonl) |

recall 5/6 = **0.83** · critical recall 2/2 = **1.0**. The `--explain` output for `guidance` contains no `concept_trace` section (grep count 0 in both the .md and .json), so the layer above was determined from `metrics.required_concepts` and the search output.

**Knowledge gap (not an expected concept, but the actual fix)**: nothing in the ontology or the record base covers a skip link / bypass-blocks (WCAG 2.4.1) — grep for "skip", "bypass" in ONTOLOGY.md and the data files returns nothing. `search -k 12` (03-search-k12.md) returns `desktop-keyboard-first`, `focus-ring-standard`, `a11y-focus-visible`, `grid-single-tab-stop`, `mobile-keyboard-ime` — none about reaching a control past repeated chrome. The sentence "can't get to" is a reach-distance complaint, and the skill has no concept for it.

## Direction verdict (04-direction.json/.md)
Compatibility: preserved navigation, layout, surface, cards, typography, color, motion, cta, imagery, icon, metadata; **new**: density (`density-high`), focus (`focus-ring-standard`); changed: none. `preservation` list = 11 slots, `validation.ok = true`.
- Preserved slots: all justified (low budget, task does not concern them).
- focus → `focus-ring-standard` marked **new / "no repository evidence"**: the codebase already has exactly this (global `:focus-visible` 2px ring token, white override on the chrome). The choice is right; the "new" status is wrong — it comes from `design_context` having no focus slot even though inspect saw focus handling. Layer: `direction` (context-detection input). Harmless here because the guidance text ("ring must remain visible on the accent surface, use a two-tone ring or offset") is what the fix in iteration 1 applied.
- density → `density-high` marked new: not justified by the task; no repository evidence was consulted for a slot the task does not touch. Ignored.

## Implementation
Files changed (copies in `before/`): `src/App.jsx`, `public/styles.css`, `public/bundle.js` (rebuilt with `node build.mjs`).
- `App.jsx`: a `Skip to content` link as the first focusable element; `onClick` prevents navigation and focuses `<main id="main" tabIndex={-1}>` so the `#compare=…` hash (the filter's shareable state) survives.
- `styles.css`: `.skip-link` off-screen until `:focus-visible`, then a surface chip over the top bar using existing tokens (`--color-bg-surface`, `--color-action-primary`, `--color-border-strong`, `--radius`, `--sp-*`); `.content:focus { outline: none }` because `main` is a programmatic target, not a control. Iteration 1 added `outline-color: #ffffff` on the focused skip link (same override the codebase uses for `.topbar :focus-visible`). Line endings restored to the file's original CRLF (the previous agent's rewrite had converted the whole file to LF).
- `CompareSwitch.jsx` untouched: it was already reachable and operable (verified in `render/keyboard-before.json`: Tab #7, ring on the sibling span, ArrowRight changes the period, hash and chart labels).

Diagnosis vs the sentence: before the change the filter was reachable at Tab #7 (4 nav links + banner link + dismiss). "Can't get to" was reach distance, not a trap; the fix shortens the path to 3 keys (Tab → Enter → Tab) and keeps everything else as it was.

Guidance used: a11y-keyboard-operable (Tab order in visual order, do not add custom key handling to a native group), a11y-nontext-contrast + direction focus slot (two-tone/offset ring on the dark chrome → iteration 1), a11y-semantics-structure (keep native radios), search-filter-feedback's single applicable point (state stays in the URL — preserved by `preventDefault`). Ignored: comp-filters (faceted filter bar redesign; contradicts a 2-option control and the low budget), search-filter-feedback's search/debounce/result-count content (no search exists), comp-chart-container (chart already meets it; nothing to reach there), direction density slot.

## Render
Mode: **native** — Playwright 1.63.0 Chromium against `public/index.html` (`render/shot.mjs`), 1440×900 and 390×844, full page plus two keyboard states per viewport (skip link focused; filter focused after Tab → Enter → Tab). Keyboard-only check `render/keyboard.mjs` records every Tab stop (tag, name, ring presence/colour, viewport), whether the filter is reached, ArrowRight operation (checked value, hash, chart label), the `<details>` disclosure with Enter, and the skip-link path. Results: `keyboard-before.json`, `keyboard-first.json`, `keyboard-final.json`.

Final keyboard results (both viewports): 15 stops, 0 without a visible ring; skip link is Tab #1; Tab → Enter → Tab lands on the checked radio of the compare group with the ring; ArrowRight switches Yesterday → Same day last week and updates `#compare=lastweek`, the KPI/chart context labels and the chart; "Show hourly data" opens with Enter.

### First-render defects
- accessibility: **1** — the focused skip link's ring used the blue token (`#1d4ed8`) over the dark chrome (`#0f172a`), 2.7:1, below the 3:1 non-text floor (the same reason the codebase overrides `.topbar :focus-visible` to white). Visible in `first-*-skiplink.png`.
- visual 0 · interaction 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
- Observation, not counted: while focused the chip overlays the brand and clips the "Overview" link; transient and the standard overlay pattern, chosen over an in-flow link because the codebase reserves slot heights to avoid layout shift.

### Final defects
all 0. **Iterations: 1** (first render by the previous agent → ring fix → final render).

## Preservation verdict
navigation, theme, typography, spacing, component conventions preserved; `#compare=` hash state, native radiogroup semantics, chart summary + data table untouched; no new component, no structural change beyond one link and an id/tabIndex on `main`. `preservation-ok`.

## Skill effect
**neutral**. Platform, artifact state, mode, scope and budget were all correct, the six guardrails were the right ones, and one guardrail named the defect I found in the first render. But the two core records — the part that says what to build — were wrong for this task (faceted filters / search feedback for a two-option segmented control), the actual fix (bypass repeated chrome) has no concept or record in the base, and the direction marked the existing focus system as "new". A less careful implementer following the core records would have rebuilt the filter; the guardrails did not prevent that.

## Misses by earliest wrong layer
1. `requirements` — "filters" mapped to `components: search` / `primary_jobs: accessibility search`; no search on the page. Cascaded into comp-filters and search-filter-feedback selection.
2. `expected-concepts` — `process.safe_modification` never demanded for a low-budget modify task on an existing UI.
3. `knowledge-gap` — no ontology id or record for skip links / bypass blocks / reach distance to a control (WCAG 2.4.1).
4. `direction` — focus slot reported as new with "no repository evidence" although the global `:focus-visible` token exists (root cause: `design_context` has no focus slot, so inspect's `focus_handling` finding is not consumed).
5. `project-adaptation` (context detection) — typography UNKNOWN although `--font-ui` is declared; spacing "irregular/UNKNOWN" although an explicit `--sp` scale exists; radius evidence cites a 4px value that is not in the CSS.

## Regressions to propose
- query: "Keyboard users can't get to the chart filters." (web, react project) → expect: `components` must not include `search`; `comp-filters` / `search-filter-feedback` must not be core/guardrail for a project whose only filter is a ≤2-option segmented control; keyboard-operable and focus-visible/non-text-contrast guardrails required.
- query: "Keyboard users have to tab through the whole header before reaching the page" → expect: a record about bypass blocks / skip links (new knowledge) once one exists; until then the search must at least surface a11y-keyboard-operable + focus records and not desktop-shortcut / mobile-IME records.
- inspect on a project with `:focus-visible { outline: … var(--color-focus-ring) }` → expect: direction focus slot status `preserved` (repository evidence), not `new`.
- inspect on a project with `--font-ui:` / `--sp-*` custom properties → expect: typography KNOWN (family list), spacing KNOWN (scale).

## Tags
`requirements-miss`, `concept-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`
