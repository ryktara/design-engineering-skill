# p6-29 — RxPoint pharmacy kiosk: done screen never states completion

**Task sentence (verbatim):** "The confirmation screen prints the receipt but never says the pick-up is complete."

**Project:** `research/phase3-projects/p3-kiosk-pharmacy/project` · plain HTML/CSS/ES-modules, no build · platform **kiosk** (1080×1920 portrait panel) · **existing UI**, no new screen. The target is the `done` screen (`js/screens.js` → `screens.done`).

**Build hash:** start `ea8eed72…d9947` = end `ea8eed72…d9947` (match).

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | hub-spoke | KNOWN | Linear 3-step flow (attract → identify-dob → identify-name → list → confirm → done) that always returns to an attract/hub screen. "hub-spoke" is defensible for the attract-as-hub kiosk shape but the working model is a linear wizard with a topbar stepper. | partial |
| theme | unknown | UNKNOWN | Explicitly light (`--color-bg-canvas: #F5F7F6`, dark text) with a **second** high-contrast black/yellow theme under `html[data-a11y="on"]`. `tokens.css` is unambiguous. | no (UNKNOWN where the code is clear, and it misses the dual-theme fact entirely) |
| surfaces | elevated | INFERRED ("weak signal: shadow 1, border 1") | Border-first, not elevation: cards use 3–4 px borders (`.summary`, `.ticket`, `.banner`); shadows are almost absent. | no |
| radius | medium | INFERRED | `--radius: 20px`, `--radius-sm: 12px` — medium is right. | yes |
| spacing | irregular | UNKNOWN | A clean 8 px scale, `--space-1…7` = 8/16/24/32/48/64/96. Marking this UNKNOWN/irregular is wrong: `tokens.css` names the scale. | no |
| typography | humanist-sans | KNOWN | Nunito, weights 500–800, tabular numerals, 28 px body floor. | yes |
| components | unknown | UNKNOWN | No component directory (string-template screens), so UNKNOWN is honest. | yes (acceptable) |

`tokens.json` + `css/tokens.css` were both detected as token sources, yet theme and spacing still came back UNKNOWN — the token file is found but not read for values. Tag: `context-detection-miss`.

## 2. Requirements verdict (`02-requirements.json`)

| Facet | Resolved | Expected | Verdict |
|---|---|---|---|
| platform | `kiosk` (project inspection) | kiosk | correct (`platform_evidence` empty — it came from the project, not the sentence; acceptable) |
| artifact_state | existing | existing | correct |
| operations | diagnose, modify | diagnose + modify | correct |
| problem_domain | `[]` | content/status-legibility | **miss** — the sentence is a *content/feedback* defect ("never says"); `problem_domain` stayed empty, so nothing downstream demanded status-legibility concepts |
| change_scope | screen | screen | correct |
| mode | audit, refactor | polish / refactor | acceptable (audit+refactor is a fair reading of a defect report; no mode word in the sentence) |
| scope.kind | in-scope | in-scope | correct |
| change_budget | moderate | moderate/low | correct |
| intent.preserve | `[]` | navigation, theme, typography, ticket, countdown, i18n | miss, but harmless: the direction preserved everything anyway |
| screen | `form` | confirmation / success | **miss** — "confirmation screen" was read as a form. This one wrong facet is what pulled the keypad and dialog records into the bundle |
| project_context | as inspected | — | carries the inspect errors forward |

Status CONFIDENT, `missing: []` — no confirm question asked. Given `screen=form` was wrong, a MISSING/confirm on screen kind would have been better than confidence.

## 3. Guidance verdict (`03-guidance.md`)

Bundle: 5 records (core 3 + guardrails 2), 991 tokens, no OPTIONAL layer.

| Record | Layer | Verdict | Category | Why |
|---|---|---|---|---|
| `comp-kiosk-keypad` | core | off-target | `wrong-screen` | The longest record in the bundle (keys ≥64 px, masking, scanner wedge, format hints). The done screen has no input at all. Selected on "task evidence: screen" after `screen=form`. Also `overlong` for its contribution. |
| `nav-wizard` | core | relevant | — | "Show step count and current step" is exactly the fix for the topbar, which rendered *nothing* on the done screen so "3 of 3" never read complete. I used this line. |
| `comp-dialog` | core | off-target | `wrong-screen` | Selected for "confirmation of destructive or high-risk actions" — a lexical trap on the word "confirmation" in the sentence. There is no dialog and nothing destructive on this screen. `feedback.confirmation_destructive` is on my pre-registered forbidden list. |
| `feedback-progress-async` | guardrail | relevant | — | "on completion confirm briefly"; "a stable-phrase live region that announces start, failure and **completion** once per run". This is the record that produced the announcement I shipped. |
| `kiosk-public-use` | guardrail | partial | `generic` | Every clause (≥60 px targets, ≥20 px body, idle timeout with countdown, cancel at every step) is already implemented in this codebase. Useful only as a preservation reminder. |

Counts: relevant 2 · partial 1 · off-target 2. Bundle-level defect: **`missing-critical`** — two of my three pre-registered critical concepts are absent (below).

### Concept recall

Delivered (union over the 5 selected records): `a11y.accessible_names`, `a11y.dialog_focus`, `a11y.live_status`, `feedback.confirmation_destructive`, `feedback.progress_indicator`, `feedback.validation_errors`, `interaction.focus_restore`, `onboarding.linear_wizard`, `privacy.sensitive_masking`, `privacy.shared_device`, `state.offline_sync`, `state.session_expiry`, `touch.minimum_target`.

| Expected concept | Critical | Delivered? | Earliest wrong layer |
|---|---|---|---|
| `layout.focal_hierarchy` | yes | no | `expected-concepts` — never demanded. `layout-hierarchy-one-thing` ("One clear focal point per screen", platform `any`) and `typo-measure-and-rhythm` both carry it and were never asked for; it is absent from the concept trace entirely, not just uncovered. Not a knowledge gap. |
| `a11y.color_not_only` | yes | no | `expected-concepts` — never demanded. `a11y-color-not-only` exists, platform `any`, and ranks **3rd** in `advise.py search` on this exact sentence (score 0.347), so retrieval finds it easily. Nothing asked for it. This is the sharpest miss: the *only* completion cue on the screen was a green tick. |
| `a11y.live_status` | yes | **yes** | — (DIRECT, via `feedback-progress-async`) |
| `feedback.progress_indicator` | no | **yes** | — (DIRECT) |
| `state.session_expiry` | no | **yes** | — (via `kiosk-public-use`) |
| `env.glanceable_status` | no | no | `bundle-selection` — demanded and traced UNCOVERED, candidate `data-exceptions-first` existed but lost on utility/cap. |

**Concept recall 3/6 = 0.50 · critical recall 1/3 = 0.33.**

Two pre-registered **forbidden** concepts were delivered: `feedback.confirmation_destructive` and `onboarding.linear_wizard`. The second turned out useful anyway (the stepper line); the first is pure noise from the word "confirmation".

Status was CONFIDENT, not PARTIAL_SCOPE, so no design/engineering split note to judge.

## 4. Direction verdict (`04-direction.md`)

12 of 13 slots `preserved` with correct reasons ("existing system with change budget 'moderate': the task does not concern this slot"). `validation: OK`. One slot is `new`:

- **cta** → `cta-single-primary`, reason "no repository evidence for this slot". The done screen already has exactly one filled primary (`Done`) plus the utility bar. The task does not concern the CTA. **`unjustified_direction_slots: 1`** (expected 0 on an existing UI at moderate budget). It caused no change in the implementation — the slot is noise, not harm.

The per-slot guidance was otherwise exactly right: "Existing system: do not replace it for this task" on every visual slot is what an existing-UI copy/status fix needs.

## 5. Implementation

Files changed (originals in `before/`):

- `js/i18n.js` — `doneTitle` 'You are all set' → **'Pick-up complete'** / 'Todo listo' → **'Recogida completada'**; new keys `doneStatus`, `stepComplete`, `doneAnnounce(code, counter)` in **both** languages.
- `js/screens.js` — `topbar()` takes a `complete` flag; `done` now calls `topbar(t, icons, 2, true)` so the stepper reads "Step 3 of 3 · Confirm · Complete" instead of vanishing. Added a `.statusline` (check icon + sentence) between the h1 and the lede.
- `css/kiosk.css` — `.statusline` and `.step--done` in the existing `@layer components`, built from existing tokens (`--space-*`, `--radius`, `--color-bg-muted`, `--color-action-primary`, `--font-lede`); inherits the accessible black/yellow theme automatically because it uses semantic tokens only.
- `js/app.js` — after `go('done')`, the existing `#live-polite` (`role=status`) region is set to `doneAnnounce(...)`: "Pick-up complete. Your ticket is B-16 at pick-up counter 2."

Completion is now stated four ways, none of them colour-only: the heading, the status line, the stepper, and the spoken announcement. Preserved: routes/screen names, session wipe on confirm, ticket block, 20 s auto-reset countdown, utility bar, `data-a11y` accessible mode, both languages, `window.__kiosk` test hooks.

**Guidance used:** `feedback-progress-async` (announce completion once through a stable live region; confirm briefly on completion), `nav-wizard` (show step count and current step), `kiosk-public-use` (kept the idle/auto-reset countdown and the reach-zone utility bar untouched).
**Guidance ignored:** `comp-kiosk-keypad` (no input on this screen), `comp-dialog` (no dialog, nothing destructive).

**Process guidance check:** `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` were **not** needed in the bundle. SKILL.md §2 (inspect first), §6 (implement) and §7 (verify by rendering) already carried it: I read `tokens.css` before writing CSS, reused `#live-polite` rather than adding a region, and rendered before reporting. `process_records_needed: false`.

## 6. Render

**Render mode: native (Playwright 1.63.0, Chromium), 1080×1920 kiosk viewport**, driven through the real flow (start → DOB 04121968 → name OKAFOR → review → confirm), 4 permutations: {en, es} × {standard, accessible}. Screenshots `render/first-done-*.png`, `render/final-done-*.png`; all four were opened and looked at. Zero console/page errors, no overflow past 1920 px in any permutation.

**First-render defects (1, type `visual`):** the `.statusline` used a 999 px pill radius with left-aligned text; at 1080 px it wrapped to two lines in both languages, giving a stadium-shaped box with a ragged second line inside an otherwise centred success block. Everything else was correct on the first render: stepper text, both languages, both themes, live-region text, ticket and countdown intact.

Fix: `border-radius: var(--radius)`, `text-align: center`, `max-width: 30ch; margin: 0 auto`. **Iterations: 1.** **Final defects: 0.**

No defect the guidance warned about was shipped.

## 7. Preservation

navigation ✔ · theme ✔ (both themes, semantic tokens only) · typography ✔ (no new sizes/families) · component reuse ✔ (existing `#live-polite`, existing topbar, existing token scale) · unjustified structural changes **0**.

## 8. Skill misses, routed to the earliest layer

| Miss | Earliest layer |
|---|---|
| "confirmation screen" classified as `screen: form` → keypad + dialog records | `requirements` |
| `intent.problem_domain` empty for an explicit content/status defect ("never says") | `requirements` |
| `layout.focal_hierarchy` never demanded (carrier exists, platform `any`) | `expected-concepts` |
| `a11y.color_not_only` never demanded (carrier exists and ranks 3rd in search on this sentence) | `expected-concepts` |
| `env.glanceable_status` demanded but dropped for `data-exceptions-first` | `bundle-selection` |
| theme UNKNOWN, spacing "irregular", surfaces "elevated" with `tokens.css`/`tokens.json` both detected | `project-context` |
| `cta` slot marked `new` on an untouched slot at moderate budget | `direction` |

## 9. Regressions to propose

1. **query:** "The confirmation screen prints the receipt but never says the pick-up is complete." · **expect:** the bundle carries a never-colour-alone record; `a11y.color_not_only` is demanded as critical whenever a sentence says a screen fails to *say* / *state* / *tell* something.
2. **query:** any "screen never says / does not tell the user X" sentence · **expect:** `intent.problem_domain` includes a content/status-legibility domain, and `layout.focal_hierarchy` is demanded — the fix is always "make the statement the focal point", not a component.
3. **query:** "confirmation screen" on an existing kiosk/web flow · **expect:** `screen` resolves to a confirmation/success screen, not `form`; `comp-dialog` is not selected on `feedback.confirmation_destructive` unless the sentence names a destructive action.
4. **project-context:** a project with `tokens.css` defining `--space-1…7` on an 8 px scale and an explicit light palette · **expect:** `spacing` KNOWN/8pt and `theme` KNOWN/light (plus a high-contrast variant), not UNKNOWN.

## 10. Tags

`requirements-miss`, `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `skill-helped`, `preservation-ok`
