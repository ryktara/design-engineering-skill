# p6-05 — "Review the alerts panel against our accessibility checklist."

- **Task sentence (verbatim):** `Review the alerts panel against our accessibility checklist.`
- **Project / stack / platform:** `research/phase3-projects/p3-react-dashboard-polish/project` — React 18 + esbuild, hand-rolled CSS tokens in `public/styles.css`; web.
- **Existing UI or new screen:** existing UI (GridSense dashboard, Alerts module in `App.jsx` → `AlertsWidget.jsx`). No new screen.
- **Build hash:** start `ea8eed72…d9947`, end identical (see `00-build-hash-end.txt`).
- **Note on resumption:** the previous agent had already produced 00–04 and implemented the change (`before/src/components/AlertsWidget.jsx` vs project confirms one changed file; `before/public/styles.css` and `before/src/App.jsx` are byte-identical copies, i.e. untouched). I re-verified the implementation against the guidance, rendered it, probed it in the browser, and completed steps 6–9. The first render below is the first render of that implementation.

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `.topbar` + `nav.nav` with 4 links, `aria-current="page"` | yes |
| theme | light-first | INFERRED | canvas `#f4f6f8`, surface `#ffffff`, dark chrome bar only | yes |
| surfaces | bordered-flat | INFERRED | `.module` = white + 1px `--color-border-default`, no shadows | yes |
| radius | small | INFERRED | `--radius: 6px`, pills `999px`, chips `4px` | partial — value right, evidence ("most common radius 4") misreads the token |
| spacing | irregular / UNKNOWN | UNKNOWN | explicit scale `--sp-1..--sp-12` = 4/8/12/16/24/32/48 | partial — the code is unambiguous; also a false "tailwind spacing classes (5)" signal in a project with no Tailwind |
| typography | unknown | UNKNOWN | `--font-ui: Inter, "Segoe UI Variable", …` + a full `--fs-*` ramp, applied on `body` | partial — evidence string "no font family declaration found" is factually wrong |
| components | unknown | UNKNOWN | 7 local components in `src/components/`, no library | partial |

Layer for the typography/spacing misses: `project-context`.

## 2. Requirements verdict (`02-requirements.json`)

| Item | Resolved | Expected | Verdict |
|---|---|---|---|
| platform | `web` (project inspection), `platform_evidence: []` | web | correct (from the project, not the sentence — acceptable) |
| artifact_state | `existing` | existing | correct |
| operations | `["review"]` | review | correct |
| problem_domain | `["accessibility"]` | accessibility | correct |
| change_scope | `unknown` (intent.scope `moderate`) | — | acceptable; sentence carries no scope word |
| mode | `["accessibility","audit","review"]` | review / accessibility / audit | correct, evidence is sound |
| scope.kind | `in-scope` (UI_ACCESSIBILITY) | in-scope | correct |
| change_budget | `low` | low | correct |
| intent.preserve | `[]` | navigation, theme, typography, component reuse | miss in name only — the direction preserves 12/13 slots anyway; not routed as a separate defect |
| project_context | see table above | — | two UNKNOWNs that should be KNOWN |

`diagnose_only: true` is set. The task as briefed still ends in an implementation, which the skill cannot know; it is not a defect.

## 3. Guidance verdict (`03-guidance.json`, 7 records: core 1 + guardrails 6, ≈931 tokens)

| Record | Layer | Verdict | Category | Why |
|---|---|---|---|---|
| `comp-toast-notification` | core | partial | wrong-screen | Selected as the only core record; the panel is an inline list, not a toast/snackbar/banner. Its one useful line ("live region polite") is what carried `a11y.live_status`. |
| `layout-hierarchy-one-thing` | guardrail | off-target | generic | Dashboard focal-point advice; nothing in it applies to an accessibility review of one panel. |
| `interaction-drag-drop` | guardrail | off-target | wrong-screen | There is no drag and drop anywhere in the alerts panel. It entered only as a GENERIC carrier for `a11y.live_status` + `interaction.keyboard_navigation`, while SPECIFIC carriers (`a11y-live-status`, `a11y-keyboard-operable`) were candidates and were not selected. |
| `a11y-skip-link` | guardrail | partial | wrong-screen | Page-level bypass guidance; the skip link already exists in `App.jsx`. It did carry `a11y.semantics`, which is what backed `role="list"`. |
| `a11y-color-not-only` | guardrail | relevant | — | Real checklist item; verified — severity is glyph + label + tint already, no change needed. |
| `a11y-contrast-text` | guardrail | relevant | — | Real checklist item; verified the acknowledged chip / muted text (≈4.6:1 at 12px/600, AA pass). |
| `a11y-labels-names` | guardrail | relevant | — | Drove the actual fix: per-alert accessible name on each Acknowledge button. |
| *(bundle-level)* | — | — | missing-critical | `interaction.focus_restore` — the panel's single worst defect — is absent from the bundle, and `interaction.focus_visible` was demanded and dropped. |

relevant 3 · partial 2 · off-target 2. OPTIONAL NOTES layer was empty (`optional_useful` 0, `optional_noise` 0).

### Concept recall

| Expected id | Critical | Delivered? | Carrier / layer if missing |
|---|---|---|---|
| `a11y.accessible_names` | yes | yes | `a11y-labels-names` (SPECIFIC) |
| `a11y.live_status` | yes | yes | `comp-toast-notification`, `interaction-drag-drop` (GENERIC carriers; `a11y-live-status` was a candidate and lost) |
| `interaction.focus_restore` | yes | **no** | `expected-concepts` — never demanded. No trace entry at all. |
| `a11y.color_not_only` | no | yes | `a11y-color-not-only` |
| `a11y.contrast` | no | yes | `a11y-contrast-text` |
| `a11y.semantics` | no | yes | `a11y-skip-link` |
| `interaction.keyboard_navigation` | no | yes | `a11y-skip-link`, `interaction-drag-drop` |
| `interaction.focus_visible` | no | **no** | `bundle-selection` — demanded as `recommended`, candidates `focus-ring-standard` / `a11y-focus-visible` / `grid-single-tab-stop` existed, cap/utility dropped them |

**concept recall 6/8 = 0.75 · critical recall 2/3 = 0.667.**

No forbidden concept appeared. `status` was CONFIDENT, not PARTIAL_SCOPE, so the design/engineering split question does not apply.

### Knowledge gap behind `interaction.focus_restore`

Grepping the base: `interaction.focus_restore` is carried only by `comp-tv-rail`, `comp-mini-player`, `media-resume-and-details`, `comp-kiosk-keypad`, `comp-tv-side-sheet`, `layout-rails`, `layout-immersive-rails`, `a11y-modal-dialog`, `a11y-tv-focus-always` — TV, kiosk and modal records. `advise.py search "<sentence>" -k 12` returns none of them. There is **no web, non-modal record for "the control you activated disappears / the row re-sorts — where does focus go"**, which is the most common focus-management failure in a list of actionable rows. Earliest wrong layer is still `expected-concepts` (an accessibility review never demanded the concept), with this as the underlying gap.

## 4. Direction verdict (`04-direction.json`)

Budget `low`; 12 of 13 slots `preserved`, 0 `changed`, **1 `new`**.

| Slot | Status | Justified? |
|---|---|---|
| navigation, density, surface, cards, typography, color, motion, focus, cta, imagery, icon, metadata | preserved | yes — correct for an accessibility review of an existing UI |
| layout → "Table-first working screen" (`layout-table-first`, virtualised, sticky header, filter chips) | **new** | **no** — an accessibility review of one panel does not justify proposing a new page layout, and the alerts panel is a list, not a table. Rationale given is only "no repository evidence for this slot", on a codebase whose layout is visible in `App.jsx`. |

`unjustified_direction_slots: 1`. The `focus` slot's "Verify the existing indicator ≥3:1, visible in every theme and state" was the one genuinely useful direction line and I did verify it. Validation: OK.

## 5. Implementation

Files changed (1): `src/components/AlertsWidget.jsx` (copy in `before/`). `public/styles.css` and `src/App.jsx` were **not** changed — existing `.sr-only` and the global `:focus-visible` 2px ring were reused rather than adding new CSS.

Defects found in the review and fixed:
1. **Duplicate accessible names** — every row's button read "Acknowledge". Fixed with a visually hidden per-alert suffix (`Acknowledge<span class="sr-only">: {title}</span>`), reusing the project's `.sr-only`.
2. **Focus loss on acknowledge** — the button is replaced by a `<span>` and the row re-sorts to the bottom, dropping focus to `<body>`. Fixed by moving focus to the row (`tabIndex={-1}` + `data-alert-id` lookup in an effect), so the row re-reads severity, title and the new "Acknowledged" state.
3. **List semantics** — `<ul class="alerts">` with `list-style:none` loses list role in WebKit. Fixed with `role="list"`.

Checked and deliberately not changed: severity is already glyph + label + tint (colour-not-only passes); acknowledged-chip and muted-text contrast pass AA; target size 104×32 px ≥ 24×24 (WCAG 2.2 AA); the state change is already announced by the ExceptionStrip's `role="status" aria-live="polite"` open-count summary, so no second live region was added.

- **guidance used:** `a11y-labels-names` (fix 1), `comp-toast-notification` — live-region line only (reuse of the existing live region, fix 2's announcement), `a11y-skip-link` — semantics line only (fix 3), `a11y-color-not-only` and `a11y-contrast-text` (verified, no change).
- **guidance ignored:** `layout-hierarchy-one-thing` (dashboard focal-point advice, nothing to act on in an a11y review), `interaction-drag-drop` (no drag and drop exists in this panel; the two concepts it carried were implemented from the codebase, not from the record).
- **Process guidance check:** `process_records_needed: false`. SKILL.md §2 (inspect first) and §7 (verify by rendering) were sufficient — reuse of `.sr-only` / the `:focus-visible` token and the single-file diff came from inspecting the project, not from `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect`.

## 6. Render and defects

**Render mode:** `html` — real build (`node build.mjs`) + Playwright 1.63.0 Chromium against `public/index.html`, viewports 1280×800 and 390×844, plus an interaction probe (click-acknowledge, keyboard Enter-acknowledge, computed focus state, target-size measurement). Screenshots: `render/first-1280x800.png`, `render/first-390x844.png`, `render/first-after-ack-1280x800.png`, same three as `final-*`, plus `render/kbd-focus-alerts.png`.

First render, inspected:
- desktop and mobile identical to the pre-change layout — the hidden suffix produces no visual change, and the alerts module, exceptions strip, KPI grid and chart are untouched;
- click-acknowledge probe: `document.activeElement` = `LI[data-alert-id=al-2201]` (the acknowledged row, now last), not `<body>`; `role="list"` present; the two buttons expose distinct names;
- keyboard Enter-acknowledge probe: the row matches `:focus-visible` and paints the 2px `#1d4ed8` ring at the correct offset, fully inside the panel (`kbd-focus-alerts.png`);
- mouse-acknowledge correctly does **not** paint a ring (`:focus-visible` false), so no stray outline for pointer users;
- ExceptionStrip live text changes from "2 open exceptions: 1 critical, 1 warning." to "1 open exception: 1 warning." on acknowledge, so the state change is announced.

| Defect type | First render | Final |
|---|---|---|
| visual | 0 | 0 |
| interaction | 0 | 0 |
| accessibility | 0 | 0 |
| platform | 0 | 0 |
| existing-system-mismatch | 0 | 0 |
| implementation-bug | 0 | 0 |

**Iterations: 0** — nothing needed fixing after the first render; `final-*` is a re-render of the same code. No defect that the guidance warned about was shipped.

## 7. Preservation

Navigation, theme, typography, spacing, surfaces and component structure all untouched; one component file changed; no new CSS; the ExceptionStrip live region and the `#compare=` URL-hash state were both left alone (the fix deliberately avoided adding a second live region). **preservation-ok**, 0 unjustified structural changes in the implementation. The *direction*, separately, proposed one unjustified slot (layout).

## 8. Skill misses, routed to the earliest layer

| # | Layer | What |
|---|---|---|
| 1 | `expected-concepts` | `interaction.focus_restore` was never demanded for a web accessibility review of a list whose action control disappears on activation — the panel's highest-severity defect. Underlying: no web/non-modal carrier exists for the concept (knowledge gap). |
| 2 | `candidate-compatibility` | `interaction-drag-drop` accepted as a GENERIC carrier for `a11y.live_status` and `interaction.keyboard_navigation` in a panel with no drag and drop, while SPECIFIC candidates `a11y-live-status` and `a11y-keyboard-operable` were available. Same for `comp-toast-notification` as the core record. |
| 3 | `bundle-selection` | `interaction.focus_visible` demanded (`recommended`), candidates `focus-ring-standard` / `a11y-focus-visible` present, dropped by the cap — in a task whose fix depends on a visible ring landing on a programmatically focused row. |
| 4 | `project-context` | typography reported UNKNOWN with evidence "no font family declaration found" although `--font-ui` is declared and applied; spacing UNKNOWN with a false "tailwind spacing classes (5)" signal against an explicit 4/8/12/16/24/32/48 token scale. |
| 5 | `direction` | `layout` slot emitted as `new` (table-first, virtualised) on an existing UI at budget `low` for a review task. |

## 9. Regressions to propose

1. Query: "Review the alerts panel against our accessibility checklist." — expect the bundle to deliver `interaction.focus_restore` and `interaction.focus_visible`, and to prefer `a11y-live-status` / `a11y-keyboard-operable` over `interaction-drag-drop` as carriers.
2. Query: "The Acknowledge button disappears when you press it and the row moves — check the keyboard experience." — expect focus-management guidance for a web list (where focus goes when the activated control is removed), not only modal/TV focus records.
3. Query: any web accessibility review at budget `low` on an existing UI — expect `unjustified_direction_slots == 0` (no `new` layout slot).
4. Project-context regression on this codebase: expect `typography` KNOWN (`--font-ui` / Inter stack) and `spacing` KNOWN (4/8/12/16/24/32/48), with no Tailwind signal.

## 10. Tags

`concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `skill-helped`, `preservation-ok`
