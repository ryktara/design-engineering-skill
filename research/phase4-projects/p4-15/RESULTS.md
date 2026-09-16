# p4-15 — results

## Task
"add a first-visit language and accessibility-mode chooser to the kiosk attract screen without changing the pick-up flow"

## Project / stack / platform
`p3-kiosk-pharmacy/project` — plain HTML + CSS (cascade layers, custom-property tokens with a `html[data-a11y="on"]` high-contrast set) + vanilla ES modules; public touch kiosk, portrait 1080×1920, hub-and-spoke (attract → identify → list → confirm → done), idle reset. **Existing project, new flow element** on the attract screen.

Render mode: **html** (native): Playwright 1.63.0 at 1080×1920 against the project served by the Phase 3 `render/server.js` (`render/shoot.js`, `render/interact.js` in this task dir; NODE_PATH → Phase 3 `node_modules`).

## Design-context table (`01-inspect.json`)
| field | detected | status | actual (`tokens.css`, `kiosk.css`, `screens.js`) | correct? |
|---|---|---|---|---|
| navigation | hub-spoke (24 matches) | KNOWN | attract hub + linear spokes, utility bar with Start over on every spoke | yes |
| theme | unknown | UNKNOWN ("25 near-white, 17 near-black") | light brand theme (green field, off-white canvas) **plus** a high-contrast accessible theme switched by `html[data-a11y]` — a dual theme keyed on an attribute, not on dark/light | no |
| surfaces | elevated | INFERRED ("shadow 1, border 1") | flat surfaces with 3 px borders; the one `box-shadow` is the attract pulse halo | no |
| radius | medium (12) | INFERRED | `--radius: 20px` (primary), `--radius-sm: 12px`, 32 px on the start button | partial |
| spacing | irregular | UNKNOWN ("6, 10") | 8-based token scale `--space-1..7` = 8/16/24/32/48/64/96 (the 6/10 px hits are key gaps) | no |
| typography | humanist-sans (Nunito) | INFERRED | `--font-family: "Nunito", "Segoe UI Variable Text", …` — Nunito is named but not loaded (no font file / CDN), so the system fallback renders; weights 500–800; tabular numerals | partial |
| components | unknown | UNKNOWN | `.btn` (primary / secondary / util), `.key`, `.field`, `.rxrow`, `.summary`, `.ticket`, `.banner`, `<dialog>` pattern in `kiosk.css` | no |
Also: `platforms: ["web"]` for a kiosk (viewport `width=1080`, README "kiosk", body fixed 1080×1920); `product_hints: healthcare, government` (government from "counter"/"staff"? plausible but wrong); `i18n: []` despite `js/i18n.js` with en/es string tables; `fonts: Nunito` counted as present.

## Requirements verdict (`02-requirements.json`, status **AMBIGUOUS**, exit 4)
| field | value | verdict |
|---|---|---|
| scope | UI_ACCESSIBILITY, in_scope | right |
| mode | accessibility + create | right (create dominant) |
| platform | kiosk (request) — **conflict** with project "web" → AMBIGUOUS | right value; the status is wrong: the inspector mis-read a kiosk project as web, so the conflict is self-inflicted |
| input / environment | touch / public | right |
| product | government, healthcare | healthcare right; government wrong |
| screen / components | [] / [] | missing: attract screen, chooser / segmented choice |
| intent | existing **false**, scope **greenfield**, creation true | wrong — the sentence says "to the kiosk attract screen"; `existing` should be true |
| negative_constraints / preserve | [] / [] | **wrong** — "without changing the pick-up flow" is an explicit no-change constraint (`no_change: []`, `structural: ["flow"]`) |
| change_budget | low | right |
| accessibility | keyboard, screen_reader, touch_targets, reduced_motion, contrast | right; large-text / reach range absent again (as in Phase 3) |
| i18n | no field | the task is half about language; no signal recorded |

## Guidance verdict (`03-guidance.md/json`; status AMBIGUOUS; bundle 6 = core 1 + guardrails 5)
Metrics: concepts 6/7 (uncovered `a11y.semantics`), ≈726 tokens, coverage/1k 8.26, contaminated [], purity 1.0; concerns 0.8 (uncovered **component**).
| record | verdict | note |
|---|---|---|
| `comp-empty-state` (core) | off-target | selected as "highest-scoring component with lexical evidence" (lexical 0.117); an empty state has nothing to do with a chooser |
| `kiosk-public-use` | relevant | ≥60 px targets, feedback on every tap, attract as hub, idle countdown — used |
| `a11y-contrast-text` | relevant | chooser text measured ≥4.5:1 in both modes |
| `a11y-labels-names` | relevant | group names, `lang` attributes on language buttons, label-in-name |
| `shared-device-privacy` | relevant | "clear the session on idle" → choices reset per visitor |
| `a11y-live-status` | partial | status announcements; the chooser uses `aria-pressed` state instead |
Relevant 4 · partial 1 · off-target 1. The `component` concern is correctly reported uncovered.

Missing guidance:
- Language switcher / first-visit chooser on a kiosk attract screen — **knowledge gap**: `platforms/kiosk.md` has one clause ("large language switcher on the attract/hub screen"); the record base returns `anti-style-before-product`, `states-offline-and-sync`, `dir-public-kiosk` for "language selector chooser kiosk first visit". Nothing about: each language named in itself, immediate effect, per-visitor reset, not blocking Start.
- Accessible-mode chooser / reach-zone consequences — knowledge gap (already logged in Phase 3).
- `onboarding-first-run` (0.513 on "onboarding first run choose language accessibility mode") is about mobile permission priming; partial at best — candidate-retrieval returns the nearest wrong thing.
- `impl-safe-modification` (rank 10, 0.284) matches "without changing the pick-up flow"; not selected (bundle-selection).
- `a11y-time-and-auto` (idle reset must stay controllable) — rank 4 on a "dismissible chooser overlay attract idle" query; not selected.
- `nav-hub-spoke` is rank 1 in search (0.371) and became the preserved navigation slot — fine.

## Direction verdict (`04-direction.md/json`, validation OK)
Budget low · preserved navigation, surface, typography · changed [].
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | preserve hub-spoke | preserved | yes |
| layout | single column | new | fine |
| density | low, kiosk floor ≥64 px / ≥20 px | new | right — the platform floor now overrides the generic numbers (fixed since Phase 3) |
| surface | preserve elevated (INFERRED) | preserved | value wrong (flat, bordered); preserving is right |
| cards | flat tiles | new | fine |
| typography | preserve humanist-sans (Nunito) | preserved | fine (system fallback in practice) |
| color | neutral canvas + one accent | new | partial — the repo has a dominant brand-green field on attract; theme UNKNOWN made this "new" instead of preserved |
| motion | functional minimal | new | fine |
| focus | touch-only (kiosk clause) | new | fine |
| cta | single primary | new | right — the chooser must not add a second filled button (it uses secondary/choice styles) |
| imagery | **illustration system** | new | unjustified for a chooser; nothing to illustrate |
| icon / metadata | filled / moderate | new | fine |
Unjustified new slots: imagery; colour "new" instead of preserved (context detection). Change budget low was respected: 3 files of JS/CSS, no flow change.

## Implementation summary (before copies in `before/`)
- `project/js/i18n.js` — en/es strings: chooser title, Language / View labels, Standard view / Accessible mode, hint, Continue.
- `project/js/screens.js` — attract renders a `.chooser` block (role=group, heading; two labelled rows of paired `aria-pressed` buttons: English / Español with `lang` attributes; Standard view / Accessible mode with a hint) below the brand field while `state.chosen` is false; the foot language switch renders after dismissal instead; `utilbar()` gained `a11yToggle` so the bottom bar's mode toggle is hidden (aria-hidden, tabindex −1, layout kept) while the chooser already offers the choice.
- `project/js/app.js` — `defaults` from URL params (`lang`, `a11y`, new `chooser=off`), `state.chosen`; actions `set-lang`, `set-a11y` (immediate, reuse the existing lang/a11y code paths), `chooser-done`; `start` marks chosen; `resetSession()` restores defaults so the next visitor gets the default language/view and the chooser again; `__kiosk.state` test hook. Idle timer, session, lookup, screens: untouched.
- `project/css/kiosk.css` — `.chooser`, `.chooser__row`, `.chooser__hint`, `.btn--choice` (+ a11y-layer border overrides).
- `project/README.md` — chooser documented.

## First-render defects (render/first-*.png, `05-interaction-first.json`: 24/24 after a selector fix in the test itself — `[data-a11y="on"]` matched `<html>`)
1. **visual** — "Accessible mode: larger text, high contrast, controls lower down" as the button label wrapped to 3 lines at 24 px (4 in a11y mode), making the two rows unequal and the button noisy.
2. **existing-system-mismatch** — two controls for the same setting on one screen: the existing utility-bar toggle (label = the action, "Standard view" while accessible mode is on) and the chooser's pressed-state buttons (label = the state); in a11y mode both read "Vista estándar" with opposite meanings.

## Final defects (render/final-*.png, `05-interaction.json`: 25/25; Phase 3 `interact.js` re-run: 70/70)
- None measured. Pre-existing and unchanged: foot language switch occupies one of two grid columns after dismissal; large empty band above the field in a11y mode (accepted in Phase 3).

## Iterations
2 renders. Fix: button label "Accessible mode" + one-line hint under the row (`aria-describedby`); utility-bar mode toggle hidden while the chooser is shown, restored after Continue/Start.

## Interaction test summary (1080×1920)
- Targets on attract with chooser: 7 standard / 7 a11y, all ≥64 px (min 72 px; choice buttons 366×80–96); Start remains present; no `:hover` rules.
- Chooser and both rows have accessible names; exactly one pressed button per row; contrast ≥4.5:1 on all chooser text (both modes).
- Immediate effect: Español → `html lang=es`, attract title in Spanish, pressed state; Accessible mode → `data-a11y=on`, black canvas, utility-bar state agrees (and is hidden while the chooser shows).
- Dismissible: Continue removes the chooser, foot language switch and utility toggle return, choices kept, no session started; Start dismisses implicitly; Start over brings it back; `?chooser=off` restores the original attract.
- Persistence: es + accessible hold on identify-dob, list and confirm (Spanish headings, `data-a11y=on`).
- Idle reset unaffected: from the list with es + a11y chosen, the warning dialog appears in Spanish with a countdown, returns to attract, session null, dialog closed, no personal data in the DOM, defaults restored (en, standard) and chooser shown.
- Accessible-mode reach zone: every attract control at y ≥ 768 (chooser rows at ≈1400–1600).
- Keyboard: Tab reaches the chooser with the 6 px `:focus-visible` ring.
- Phase 3 regression suite (`05-phase3-interaction-after.json`): 70/70 — pick-up flow, scan path, privacy masking, focus and motion checks unchanged.

## Preservation verdict
Navigation (hub-and-spoke, action names, screens) unchanged; theme tokens and the `data-a11y` mechanism reused; typography tokens reused; components: `.btn--secondary` for Continue, `.btn--choice` derived from the util-button pressed style, `.utilbar` API extended with one option. Structural changes: chooser block on attract (the task), utility-bar toggle hidden on attract while the chooser shows (justified by the duplicate-control defect), per-visitor reset of language/view (justified by `shared-device-privacy` and "first-visit"). Unjustified structural change: 0. **preservation-ok**.

## Regressions to propose
- inspector: an HTML project with `<meta viewport width=1080>`, README "kiosk", fixed 1080×1920 body — expect `platforms: ["kiosk"]` so the request/project platform conflict (AMBIGUOUS) does not occur.
- inspector: `html[data-a11y="on"]` token override set — expect theme = dual (attribute-keyed high-contrast), surfaces = bordered-flat, spacing = 8-based, i18n = js/i18n.js.
- query: "add a … chooser to the kiosk attract screen without changing the pick-up flow" — expect `intent.existing = true`, `negative_constraints`/`preserve` ⊇ [flow], `impl-safe-modification` selected, core ≠ `comp-empty-state`.
- query: "language selector on a kiosk attract screen" — expect a kiosk language-switcher/first-visit chooser record (each language in its own name, immediate effect, per-visitor reset, never blocks Start) once added.

## Skill misses by layer
- requirements: status AMBIGUOUS from an inspector platform miss (web vs kiosk); `existing=false / greenfield` for a change to an existing screen; "without changing the pick-up flow" not captured as a negative constraint; screen/components empty.
- concerns: `component` required and uncovered — correct report; the selected core still filled it with `comp-empty-state`.
- bundle-selection: `comp-empty-state` as core on lexical 0.117; `impl-safe-modification`, `a11y-time-and-auto` not selected.
- candidate-retrieval / knowledge gap: kiosk language switcher, first-visit chooser, accessible-mode chooser semantics.
- direction: imagery illustration; colour slot "new" because theme was UNKNOWN.
- project-adaptation: the platform file's "large language switcher on the attract/hub screen" clause was the only concrete guidance and had to be read manually.

## Tags
`context-detection-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `render-defect-fixed`, `skill-helped` (kiosk-public-use + a11y-labels-names + shared-device-privacy set the target floor, naming and per-visitor reset; `cta-single-primary` kept the chooser from adding a second filled button), `preservation-ok`.
