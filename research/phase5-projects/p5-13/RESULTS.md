# p5-13 — "Add a Spanish language switch to the pick-up flow."

**Task:** p5-13 · sentence run verbatim.
**Project / stack / platform:** `research/phase3-projects/p3-kiosk-pharmacy/project` — plain HTML + CSS (`@layer`, token custom properties) + vanilla JS modules, no build. Public pharmacy pick-up **kiosk**, fixed portrait 1080×1920 panel, EN/ES string tables already in `js/i18n.js`, standard + accessible (black/yellow, reach-zone) mode. p5-12's identify-step timing (90 s / 30 s) kept and asserted.
**Existing UI or new screen:** existing UI — a new control (language switch) added to the utility bar that already sits on every flow screen (identify-dob, identify-name, list, confirm, done). No new screen.
**Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (see `00-build-hash-*.txt`). Nothing under `design-engineering/` was modified.

## Pre-registered expectation (00-expectation.json, written before any advise command)
platform kiosk · existing · modes create/refactor/accessibility · in-scope · expected concepts `content.i18n_expansion`*, `process.reuse_first`*, `touch.minimum_target`, `a11y.live_status`, `interaction.focus_restore`, `a11y.accessible_names`, `privacy.shared_device` (* critical) · forbidden: TV / adaptive-breakpoint / mobile-thumb / desktop / media-track / settings-page records · preserve navigation, theme, typography, utilbar and keypad components, typed entry + session across the switch, language reset with the session, accessible-mode layout.

Code facts behind it: `js/i18n.js` already holds complete EN and ES tables; `app.js` already has `state.lang`, `applyLang()`, a `lang` action and `resetSession()` restoring the default language. The i18n.js comment says "the switcher lives on the attract screen only" and `screens.js` confirms it: the toggle is rendered only in the attract chooser/foot. The flow's utilbar (view toggle, Help, Start over; 3 equal columns, 104 px tonal buttons) has no language control, so a visitor who touched Start in English cannot switch once inside. Spanish labels are 25–35 % longer on a fixed 984 px content width.

## 1. Design-context table (01-inspect.json vs code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| platform | web | KNOWN | kiosk — README line 3 "Public touch kiosk (portrait 1080x1920)", fixed 1080×1920 body, `touch-action: manipulation`, `--target-min: 72px` | **no** |
| navigation | hub-spoke | KNOWN | attract hub → linear 3-step flow with a persistent bottom utility bar | yes |
| theme | unknown | UNKNOWN | light green brand theme + `html[data-a11y="on"]` black/yellow high-contrast mode, all in `tokens.css` | partial |
| surfaces | elevated | INFERRED | flat/bordered: 3–4 px borders, no card shadows | **no** |
| radius | medium (12) | INFERRED | `--radius: 20px` primary, `--radius-sm: 12px` keys | partial |
| spacing | irregular | UNKNOWN | regular 8 px scale `--space-1..7` = 8/16/24/32/48/64/96 | **no** |
| typography | humanist-sans (Nunito) | KNOWN | Nunito, 500–800, tabular numerals | yes |
| components | unknown | UNKNOWN | `.btn` (primary/secondary/util/choice), `.key`, `.field__value`, `.rxrow`, `dialog`, `.ticket`, `.banner` | partial |
| i18n | `[]` | — | `js/i18n.js` exports `strings.en` / `strings.es` (~90 keys each); `<html lang>` switched at runtime | **no** — directly relevant to this task and missed |

Context detection: navigation yes · theme partial · typography yes · surfaces no · spacing no. Same inspector output as p5-12 (same project), plus the i18n miss that matters here.

## 2. Requirements verdict (02-requirements.json)
- `platform`: **web** — wrong (kiosk). `platform_evidence: []`, no MISSING entry, `status: CONFIDENT`. Same failure as p5-12.
- `intent.artifact_state`: existing — correct. `intent.operations`: create — correct. `intent.change_scope`: **flow** — correct, and the one place the sentence was read well ("the pick-up flow").
- `intent.problem_domain`: `[]` — miss. The sentence says "Spanish language"; the repository has `i18n.js`; nothing became a localisation domain. `intent_evidence.domains` is `{}`.
- `mode`: create, evidence "build/create request on an existing surface" — **acceptable** (in the pre-registered set).
- `scope.kind`: in-scope, "UI design / interaction task" — correct.
- `change_budget`: moderate — acceptable (a control on five screens + a keypad row).
- `intent.preserve`: `[]` — miss; nothing names the existing string tables, the `lang` action, or the utilbar.
- `project_context`: carries the inspector's wrong `surfaces=elevated`, `spacing=irregular`.
- `activation`: `ui_score 0, non_ui_score 0, decision skip` — the sentence carries no UI term the activation layer recognises ("switch", "language", "flow" all scored 0); it ran on the project file alone.

## 3. Guidance verdict (03-guidance.json/.md) — status CONFIDENT, bundle 6 (core 1 + guardrails 5), ≈758 tokens

| record | role | verdict | BAD category | why |
|---|---|---|---|---|
| `cta-sticky-bar` | core | off-target | generic | "Bottom-fixed on mobile inside the safe area, sticky footer on desktop … scroll the field into view". The only core record, selected as "highest-scoring pattern with lexical evidence" (lexical 0.2); its `concepts` list is **empty**. Nothing about language, labels, or text length. The kiosk already has a fixed bottom bar and never scrolls. |
| `a11y-keyboard-operable` | guardrail | partial | — | Tab must reach the new control — true and verified. "The modal itself must be escapable" again contradicts the deliberate `cancel → preventDefault()` on the privacy countdown. |
| `a11y-focus-visible` | guardrail | off-target | generic | `:focus-visible` ring token already exists. |
| `states-persistence-and-session` | guardrail | off-target | off-platform | Session expiry / autosave / permission-denied; the task does not touch the session. Its own `avoid_when` disclaims public kiosks. |
| `web-responsive-breakpoints` | guardrail | off-target | off-platform | 320–1920 px matrix and drawer↔rail transforms for a fixed 1080×1920 panel. Consequence of platform=web. |
| `anti-no-states` | guardrail | partial | — | "Enumerate states per component … test with long strings" is the one sentence in the bundle that points at what actually went wrong (Spanish label overflow, stale error string). Generic, but it was usable. |

Relevant 0 · partial 2 · off-target 4. Filtered on platform: `dir-public-kiosk`, `nav-hub-spoke`. Concerns: required structure/states/interaction/accessibility all "covered" — coverage 1.0 on a bundle with nothing about the task.

### Concept recall
Delivered concepts (union over selected records): `adaptive.breakpoint_matrix`, `adaptive.navigation_transform`, `feedback.confirmation_destructive`, `interaction.focus_visible`, `interaction.hover_independence`, `interaction.keyboard_navigation`, `state.loading_empty_error`, `state.saving_conflict`, `state.session_expiry`.

| expected id | delivered? | layer if missing (from `concept_trace` / rules.jsonl) |
|---|---|---|
| `content.i18n_expansion` (critical) | no | **expected-concepts** — never demanded. `i18n-text-expansion-rtl` (platform `any`, "never hard-code widths around English strings", "allow 30–50 % expansion") is in the base and carries exactly this concept; it was not a candidate, and `search -k 12` did not surface it either (only `typo-font-loading-coverage`). |
| `process.reuse_first` (critical) | no | **bundle-selection** — demanded (recommended, "existing repository: reuse its primitives"), candidate `impl-reuse-before-new` 0.243, "bundle cap or lower utility left them out" |
| `touch.minimum_target` | no | **bundle-selection** — demanded (recommended, "touch on web"), candidate `a11y-target-size` 0.27, dropped |
| `a11y.live_status` | no | expected-concepts — not in the trace (`a11y-live-status` carries it) |
| `interaction.focus_restore` | no | expected-concepts — not in the trace |
| `a11y.accessible_names` | no | expected-concepts — not in the trace (`a11y-labels-names`, platform any) |
| `privacy.shared_device` | no | expected-concepts — never demanded; carriers `kiosk-public-use` / `shared-device-privacy` are kiosk-scoped and would have been platform-rejected anyway |

**Recall 0/7 = 0.00 · critical recall 0/2 = 0.00.** Forbidden concepts delivered: `adaptive.breakpoint_matrix`, `adaptive.navigation_transform`. Knowledge gap: none — every expected concept has a carrier in `data/rules.jsonl` (checked directly). The `search` run without a project file honestly reports `MISSING: platform`; the guidance run lost that by trusting the inspector.

## 4. Direction verdict (04-direction.json/.md) — exit code 3, **Validation: VIOLATIONS**
Compatibility: 3 slots preserved (navigation, surface, typography), 0 changed, **10 new**: layout `master-detail`, density `high`, cards `poster-landscape`, color `neutral-accent`, motion `functional-minimal`, focus `ring-standard`, cta `sticky-bar`, imagery `data-graphics`, icon `outline-system`, metadata `rich`. Preservation 3/13. Validation: "non-media product: poster (media) card geometry selected" — the skill emitted a fingerprint it knows is invalid.
- Justified: none of the ten. `master-detail` on a one-task-per-screen kiosk; `density-high` (13–14 px body, 32 px rows) for 28–34 px body and 104 px targets; poster cards for a prescription list; `icon-outline-system` on a codebase whose icon file is titled "Filled icon set"; `metadata-rich` (user-controlled columns) for a three-row list; `imagery-data-graphics` where there is none. `color-neutral-accent`, `motion-functional-minimal` and `focus-ring-standard` roughly describe what exists and are mis-labelled "new … no repository evidence" (context-detection). `cta-sticky-bar` — the bar exists; the fitting alternative `cta-single-primary` (0.27) scored higher than the pick (0.22) in "Alternatives considered" yet lost.
- The direction has no slot for content, language, or labels; the task's subject is absent from it. Followed only the closing line: preserved slots win.

## 5. Implementation (files changed; `before/` holds the originals)
`js/screens.js` (31 diff lines), `js/app.js` (24), `js/i18n.js` (7), `js/icons.js` (1), `css/kiosk.css` (3), `README.md` (1). LF preserved. `index.html` untouched.
- **Switch in the utility bar** (`utilbar()` in screens.js): a fourth `.btn--util` with the existing `data-action="lang"`, labelled in the language it switches *to* with a matching `lang` attribute ("Español" / "English"), new filled globe glyph in the existing icon set. Rendered on every flow screen; the attract screen keeps its chooser and foot switch (`langToggle: false`). `nav aria-label` localised (`t.kioskOptions`) — it was hard-coded English.
- **Grid** (`kiosk.css`): `.utilbar` now `grid-auto-flow: column; grid-auto-columns: 1fr` — 3 equal columns on attract (unchanged geometry, verified: Help still at x=384, 312 wide), 4 in the flow (228 px each, 24 px gaps). Spanish labels wrap to 2–3 lines inside the 104 px-min buttons; heights grow to ≤ 200 px in accessible mode and the screen above still fits (verified on all five screens, both modes, both languages).
- **Behaviour** (`app.js`): `applyLang()` re-renders from `session` (typed DOB/name, selection, error all kept — `render()` was already session-driven), repaints both dialogs, and writes "Idioma: español" / "Language: English" to the polite live region. Focus stays on the switch across the full re-render through the existing `focusKeyOf()`. Language still resets with the session (`resetSession` → `defaults`).
- **Stale error text** (found by the interaction check): `session.error` stored the already-translated string, so an English error stayed English after the switch. Now stores a key (`errDob`, `errDobInvalid`, `errNoMatch`, `errName`, `noneSelected`); `errorLine(session, icons, t)` translates at render; `dobProblem(d)` returns the key.
- **Text expansion on the keypad** (found in the first render): "Limpiar" overflowed the single 84 px Clear key on the QWERTY in both modes. Clear moved to the bottom row as a 2-wide key in the two cells that were empty spacers; row 3 starts with a spacer. Same key count, same ids, same `data-key`; targets unchanged (84 px min).
- Guidance **used**: `a11y-keyboard-operable` (Tab/Enter on the new control — verified), `anti-no-states` ("long strings" → the two defects above). **Ignored**: `cta-sticky-bar` (nothing to apply), `a11y-focus-visible` (exists), `states-persistence-and-session` (not the task; disclaims kiosks), `web-responsive-breakpoints` (fixed panel), the Escape clause (privacy), and all ten "new" direction slots. The rules the change actually follows — `i18n-text-expansion-rtl` (30–50 % expansion, no widths around English), `impl-reuse-before-new` (existing action, strings, button class, icon set), `a11y-labels-names`, `a11y-live-status`, `kiosk-public-use` targets/reach — are all in the base and none reached the bundle.

## 6. Render — mode `html` (native HTML in Chromium via Playwright 1.63, 1080×1920, `hasTouch`)
`render/first-*.png` (9 standard + 9 accessible) and `render/final-*.png` (same set). Walk: identify-dob EN → switch → ES (digits kept) → name ES → switch back EN → find → list ES → confirm ES → help dialog ES → done ES → idle warning ES on identify. Interaction check `render/interact.js` → `05-interaction-first.json` (74/76) and `05-interaction.json` (**84/84** on the final state).

**First-render defects:** implementation-bug 1 (error message frozen in the language it was raised in), visual 1 ("Limpiar" overflowing the 84 px Clear key — pre-existing text-expansion defect surfaced by the switch in both view modes). Interaction 0, accessibility 0, platform 0, existing-system-mismatch 0.
**Fix (iteration 1):** error keys + render-time translation; Clear key to a 2-wide bottom-row cell. Re-rendered and re-checked.
**Final defects:** 0 in every type. **Iterations: 1.**

Final interaction check covers: language button on every flow screen (and not in the attract utilbar); `<html lang>` / `state.lang` / h1 / keypad labels / error / dialogs follow the switch; typed DOB and name, list selection and totals kept; focus stays on the switch; polite announcement; localised nav label; language back to default after the session ends; on all five screens × both modes × both languages: 4 utilbar targets ≥ 72 px (≥ 84 px accessible), gaps ≥ 16 px, no label overflow, bar on the panel, primary action fully above it, accessible-mode controls at y ≥ 768, keypad labels fit and keys ≥ 64 px; Tab reaches the switch and Enter switches; p5-12 timings unchanged; no `:hover` rules.

## 7. Preservation verdict
navigation ✓ · theme ✓ (tokens untouched) · typography ✓ · utilbar component ✓ (same class, one more child) · keypad component ✓ (same keys/ids; Clear relocated within the grid — justified by text expansion, documented in code) · typed entry + session across the switch ✓ · language reset with session ✓ · accessible-mode layout ✓ (reach-zone assertions pass) · component reuse ✓ (`lang` action, `strings`, `.btn--util`, filled icon set, `focusKeyOf`, `paintChrome`, live region) · unjustified structural changes 0. **preservation-ok.**

## 8. Skill misses by earliest wrong layer
1. **platform** — inspector `web` for a README-declared 1080×1920 touch kiosk; requirements CONFIDENT with empty `platform_evidence`. Downstream: `dir-public-kiosk`, `nav-hub-spoke` rejected; `web-responsive-breakpoints` and `adaptive.*` pulled in.
2. **requirements** — `problem_domain` empty for "Spanish language switch" with `i18n.js` in the repo (inspector `i18n: []`); `preserve` empty; activation scored the sentence 0/0.
3. **expected-concepts** — `content.i18n_expansion` never demanded for a sentence about a second language; `a11y.live_status`, `a11y.accessible_names`, `interaction.focus_restore`, `privacy.shared_device` never demanded for a new control on a shared touch screen.
4. **bundle-selection** — `process.reuse_first` (`impl-reuse-before-new`) and `touch.minimum_target` (`a11y-target-size`) demanded and dropped, while `cta-sticky-bar` with zero concepts became the sole core record.
5. **direction** — 10 of 13 slots "new" on an existing codebase with budget moderate; a self-reported validation violation (poster cards on a healthcare product) left in the output; `density-high`, `master-detail`, outline icons, rich metadata all contradict the code.
6. **context-detection** — surfaces `elevated` (bordered flat), spacing `irregular` (8 px scale), theme UNKNOWN, components UNKNOWN, i18n `[]` with a full string module present.

**Skill effect: neutral.** Two partial guardrails restated things the codebase already did or that any state enumeration would find; everything specific to the task came from reading the code. It did not hurt because the ten new direction slots and the sticky-bar core were plainly inapplicable and easy to refuse.

## 9. Regressions to propose
1. `inspect_project` on `p3-kiosk-pharmacy/project` → `platforms` contains `kiosk`; `i18n` non-empty when a module exports per-locale string tables (`js/i18n.js` with `en`/`es`).
2. `requirements "Add a Spanish language switch to the pick-up flow." --project <inspect>` → `problem_domain` includes localisation/i18n; `preserve` names existing strings/language state; activation `ui_score > 0` for "language switch … flow".
3. `guidance` for the same sentence, any platform → bundle contains `i18n-text-expansion-rtl` (concept `content.i18n_expansion`) and, with `i18n` detected in the repo, `impl-reuse-before-new`; a record with an empty `concepts` list (`cta-sticky-bar`) must not be the only core record.
4. `guidance` with platform kiosk → `kiosk-public-use` or `shared-device-privacy` and `a11y-target-size` selected; `web-responsive-breakpoints` absent; delivered concepts include `touch.minimum_target`, `a11y.accessible_names`, `a11y.live_status`.
5. `direction` on an existing codebase → never emits a fingerprint whose own validation reports a violation (reject `card-poster-landscape` for non-media products before output); `icon` slot reads the existing filled set; no `density-high` on kiosk; when `cta-single-primary` outscores `cta-sticky-bar` in alternatives it must win.
6. `search "Add a Spanish language switch to the pick-up flow." -k 12` → `i18n-text-expansion-rtl` in the top 12 (currently absent; `chart-flow-sankey` and `media-resume-and-details` rank above every i18n record).

## Tags
`platform-miss` `requirements-miss` `concept-miss` `ranking-miss` `direction-mismatch` `context-detection-miss` `render-defect-fixed` `skill-neutral` `preservation-ok`
