# p6-32 — "Add a Welsh language option to the ticket machine."

- **Project / stack / platform:** `p6-kiosk-transit` · dependency-free HTML/CSS/ES5 single-page app · kiosk (1080×1920 portrait, fixed layout, no reflow, Chromium kiosk build)
- **Existing UI or new screen:** existing UI, new element (a language control in the persistent footer + a second locale)
- **Build hash start = end =** `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` ✅
- **Concurrency note:** two other tasks edited this codebase while I worked. The idle timeout became a two-stage warn dialog and the quantity stepper was rebuilt *after* my first read. I re-copied `before/` immediately before my own edits so `before/` reflects the state my diff applies to, and I touched neither `IDLE_WARN_MS`/`IDLE_GRACE_MS` nor any stepper logic — only string keys and `aria-label`s on their markup.

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | hub-spoke | KNOWN | linear wizard `attract → choose → quantity → review → pay → printing → done`; attract is an idle/attract screen, not a hub of entry points | **no** (confident wrong; "hub-spoke" was matched from README prose about the attract screen) |
| theme | light-first | INFERRED | single light theme, deliberately no dark mode (README) | yes |
| surfaces | elevated | INFERRED | white cards on warm bg with `--shadow-1` | yes |
| radius | small (5px) | INFERRED | `--radius: 16px`, `--radius-sm: 8px`; 16px on all cards/buttons | **no** (5px comes from the logo SVG, not the token file) |
| spacing | 4 | INFERRED | 8-pt scale `--sp-1..--sp-8` = 8/16/24/32/48/64 | **no** |
| typography | unknown | UNKNOWN | `--font: "Inter", system-ui, …` declared in `css/tokens.css`; scale 28/36/48/64 | **partial** (UNKNOWN where the code is explicit) |
| components | unknown | UNKNOWN | BEM components in one stylesheet (ticket-card, zone-chip, btn, promo, pay) | partial |
| i18n | `[]` (empty) | — | `js/i18n.js` with a `t()` helper and 30 `data-i18n` attributes in the markup | **no** — the one field this task is about was reported as absent |

Tags: `context-detection-miss` (navigation, radius, spacing, i18n).

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform | `kiosk`, DIRECT ("ticket machine") | correct |
| artifact_state | `existing` | correct |
| operations | `["create"]` | correct |
| problem_domain | `["content"]` (from "language") | correct |
| change_scope | `unknown` | acceptable |
| mode / evidence | `create` — "build/create request on an existing surface" | correct (sentence carries no mode word) |
| scope.kind | `in-scope`, "UI design / interaction task" | correct |
| change_budget | `moderate` | acceptable (`low` would have been tighter for a footer control + strings) |
| intent.preserve | `[]`, but `constraints.preserve_existing_system: true` | acceptable |
| project_context | carries the four wrong/unknown context values from step 1 | inherited miss |

No requirements-layer miss.

## 3. Guidance verdict (`03-guidance.md` / `.json`) — status PARTIAL, bundle = 2 records (**core 0**, guardrails 2, 263 tokens)

| record | layer | verdict | category |
|---|---|---|---|
| `kiosk-public-use` | critical | relevant — gave the ≥60 px target floor, "one visible way out at every step", and the idle-clears-the-session rule I used for the language reset | — |
| `impl-reuse-before-new` | critical | partial | `generic` — true, but SKILL.md §2 already says it; contributed nothing this task needed that inspecting `js/i18n.js` didn't |

`layer_review`: core `[]`, critical `[kiosk-public-use, impl-reuse-before-new]`, optional `[]` (optional_useful 0 / optional_noise 0).

**Bundle-level defect: `missing-critical`.** The task is *"add a second language"* and the bundle contains **nothing about internationalisation**. The record that covers it exactly — `i18n-text-expansion-rtl` — is the **top search hit at 0.483**, 49 % above the next record, and its text is almost a spec for this task ("a language switch is one visible control on every screen of the flow, labelled in its own language (Español, not 'Spanish'); switching keeps the session, typed input, selection and focus, … re-renders every label"). It never reached the bundle because `content.i18n_expansion` was **never demanded**: it is absent from `concept_trace`, from `omitted` and from `rejected`. `problem_domain` was correctly set to `content` and the word "language" was captured in `intent_evidence.domains.content` — the signal was there and was not turned into a required concept.

### Concept recall

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `content.i18n_expansion` | no | **expected-concepts** (record exists and ranks #1 in `search`; never demanded → never a candidate) |
| `touch.minimum_target` | yes (`kiosk-public-use`) | — |
| `interaction.selection_visible` | no | **expected-concepts** (a "add an option" task on a touch surface never demanded a selected-state concept) |
| `a11y.accessible_names` | no | **expected-concepts** (concerns listed `accessibility` as *required* and it stayed uncovered; no a11y record was demanded) |
| `state.session_expiry` | yes (`kiosk-public-use`, recommended) | — |
| `process.reuse_first` | yes (`impl-reuse-before-new`) | — |

- **concept recall = 3/6 = 0.50** · **critical recall = 1/3 = 0.33** (`touch.minimum_target` delivered; `content.i18n_expansion` and `interaction.selection_visible` missing).
- The skill's own metrics report `critical_coverage_ratio: 1.0` — it is measuring the concepts it demanded, not the concepts the task needed. That self-report is the miss made invisible.
- Forbidden concepts: none delivered. Platform filtering was clean (all six `rejected` records were correctly off-platform).
- PARTIAL status note: the split is fine; the MISSING items (product family, brand) are genuinely unstated.

## 4. Direction verdict (`04-direction.md`)

12 of 13 slots `preserved` with correct reasons, validation OK. **`unjustified_direction_slots: 1`** — `cta` is `new` ("One primary action per screen", reason "no repository evidence for this slot") on an existing UI with a moderate budget, for a task that adds a footer control and strings. The project already has an explicit one-primary-button rule in its README; the slot should have been `preserved`. Harmless here (I ignored it), but it is an unjustified change on an existing system.

No direction slot addressed where a language control belongs or what switching must preserve.

## 5. Implementation

Files changed (originals in `before/`): `js/i18n.js`, `index.html`, `css/kiosk.css`, `js/app.js`.

- **`js/i18n.js`** — flat `STRINGS` map → `STRINGS = { en, cy }` with `en` as fallback; `t()` falls back locale → English → key; `applyAll()` extended to `data-i18n-aria` and `data-i18n-placeholder`; new `setLang()` (re-applies every static string, sets `<html lang>`, notifies listeners, leaves the session untouched), `onChange()`, `LANGS` with endonyms. ~50 Welsh strings including fare names, fare descriptions, zone labels, the idle dialog and the countdown.
- **`index.html`** — static `<span class="footer__lang">EN</span>` → `<div class="lang-switch" role="group" aria-label="Language" id="lang-switch">`; added `data-i18n` / `-aria` / `-placeholder` to the nine strings that were still hard-coded English (Start over, Total, Amount due, Ref, promo placeholder, stepper aria-labels, idle title/body/continue).
- **`css/kiosk.css`** — `.footer__lang` → `.lang-switch` / `.lang-btn`, modelled on the existing `.zone-chip` (same 3px border, `--radius`, selected = filled `--c-primary`), `min-height: var(--touch)` = 72 px; `aria-pressed="true"` carries the selected state; `:focus-visible` outline added (the project had none on buttons). Footer 96→112 px and `.footer__kiosk { white-space: nowrap }` — see defect 1.
- **`js/app.js`** — `ticketName/ticketDesc/zoneLabel` helpers (i18n key, fare table as fallback so a new fare is never blank); `renderLangSwitch()`; `onLangChange()` re-renders the JS-built lists and re-runs only the *computable* screens (`quantity`, `review`, the pay amount) — deliberately not `pay`'s terminal session, `printing` or `done`, which own timers and the reference number; `resetState()` returns to the default locale so the next passenger starts in English.

**Guidance used:** `kiosk-public-use` — the 72 px target floor for the language buttons (I would probably have sized them like the old footer badge), and "clear the session on idle" which I extended to the locale. **Guidance ignored:** `impl-reuse-before-new` (generic; already SKILL.md §2), and the direction's `cta` slot (not this task).

**Process guidance check:** `process_records_needed: false`. SKILL.md §2 (reuse) and §7 (render and inspect) were enough; `impl-reuse-before-new` spent half the bundle restating §2 while the i18n record that would have earned its place was never a candidate.

## 6. Render and defects

Render mode: **native Playwright**, Chromium, 1080×1920, 10 screenshots per pass across attract / choose / quantity / review / pay / idle, in both locales plus a mid-flow switch. Zero console errors and zero page errors in both passes; a scripted overflow audit (`scrollWidth > clientWidth`, `scrollHeight > clientHeight` over every leaf in every screen) returned empty in both passes.

**First-render defects (2):**
1. `visual` — the footer became overcrowded: the help text *and* "Kiosk 04 · Central Station" both wrapped to two cramped lines inside the 96 px bar (`first-02-attract-cy.png`). Caused by replacing a 60 px "EN" badge with a 312 px switch.
2. `existing-system-mismatch` — the English footer help, previously one line, now wrapped too; the regression was not Welsh-specific.

**Fix (1 iteration):** narrowed `.lang-btn` to 136 px, footer 96→112 px, `white-space: nowrap` on the kiosk id, `line-height: 1.25` on the help. Re-rendered: footer reads cleanly in both locales (`final-01`, `final-08`).

**Final defects: 0** in every category. One thing I chose not to "fix": the Welsh price prefix renders as `o £2.80` — grammatically correct Welsh for "from £2.80" but a visually thin one-letter prefix. Left as-is rather than inventing non-standard copy.

Verified behaviours: mid-flow EN↔CY switch preserves ticket, zones, quantity, total and typed promo (`final-06`); `<html lang>` follows the locale; `aria-pressed` marks the current language; the idle dialog is fully Welsh including the live countdown ("Yn clirio ymhen 9 eiliad", captured on the real 20 s timer, not a forced state); Start over / idle reset returns to English.

**Preservation:** navigation, layout, theme, typography, tokens, component grammar and all ids/state/accessibility semantics intact. The only structural change is the footer height, forced by putting a 72 px kiosk-grade touch target plus longer copy into a 96 px bar — justified, and I reverted an earlier larger version of it. `preservation-ok`.

## 7. Miss routing (one layer each, earliest)

| miss | layer |
|---|---|
| `content.i18n_expansion` absent from the bundle on a task whose whole subject is a second language; carrier is the #1 search hit | `expected-concepts` |
| `interaction.selection_visible` never demanded for a new selectable control on a touch surface | `expected-concepts` |
| `accessibility` listed as a required concern and left uncovered; no `a11y.accessible_names` demanded for a new labelled control | `concerns` |
| navigation read as hub-spoke where the code is a linear wizard | `project-context` |
| radius `small`/5 px and spacing `4` where the tokens say 16 px and 8-pt | `project-context` |
| `i18n: []` on a project with `js/i18n.js` and 30 `data-i18n` attributes | `project-context` |
| `cta` slot marked `new` on an existing UI with a moderate budget | `direction` |

## 8. Regressions to propose

1. Query: *"Add a Welsh language option to the ticket machine."* — expect `content.i18n_expansion` in `required_concepts` and `i18n-text-expansion-rtl` in the bundle. Any sentence naming a language, locale, translation or "bilingual" should demand the i18n concept; `intent.problem_domain == content` + a language token is sufficient evidence.
2. Query: *"Add a second language to the checkout flow."* (no platform word) — same expectation, to prove the trigger is the language token and not the kiosk platform.
3. Query: *"Add a Welsh language option to the ticket machine."* — expect `interaction.selection_visible` demanded: any "add an option/choice/toggle" on a touch or D-pad surface needs a visible selected state distinct from focus.
4. Project fixture `p6-kiosk-transit` — `inspect_project.py` should report `i18n: ["js/i18n.js", "data-i18n attributes"]`, `radius: 16px`, `spacing: 8`, `typography: Inter`, and should not report `navigation: hub-spoke` from README prose alone when the markup is a single-`<main>` step flow.
5. Bundle metrics — when a required *concern* (`accessibility` here) is uncovered and `core_size == 0`, the status should be weaker than a `critical_coverage_ratio: 1.0` self-report.

## 9. Skill effect

**`helped`, narrowly.** `kiosk-public-use` supplied the 72 px target floor and the "clear the session on idle" rule that I extended to the locale reset — both things I would plausibly have under-specified (the control I replaced was a 32 px badge). Everything that made this change actually correct for a *language* feature — expansion-safe sizing, endonym labelling, session preservation across the switch, re-rendering every label — I brought myself, from the record the bundle left out.

**Tags:** `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `skill-helped`, `preservation-ok`, `partial-scope-ok`
