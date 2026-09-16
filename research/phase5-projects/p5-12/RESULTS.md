# p5-12 — "Older customers time out on the identify step before they finish typing."

**Task:** p5-12 · sentence run verbatim.
**Project / stack / platform:** `research/phase3-projects/p3-kiosk-pharmacy/project` — plain HTML + CSS (`@layer`, token custom properties) + vanilla JS modules, no build. Public pharmacy pick-up **kiosk**, fixed portrait 1080×1920 panel (`body { width:1080px; height:1920px; overflow:hidden }`, README line 3: "Public touch kiosk (portrait 1080x1920)"), EN/ES, standard + accessible (black/yellow, reach-zone) mode.
**Existing UI or new screen:** existing UI — the identify step (DOB keypad, last-name QWERTY) and the shared `#idle-dialog`.
**Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (see `00-build-hash-*.txt`). Nothing under `design-engineering/` was modified.

## Pre-registered expectation (00-expectation.json, written before any advise command)
platform kiosk · existing · modes refactor/polish/accessibility · in-scope · expected concepts `state.session_expiry`*, `privacy.shared_device`*, `a11y.live_status`, `a11y.dialog_focus`, `interaction.focus_restore`, `touch.minimum_target`, `process.safe_modification` (* critical) · forbidden: TV/adaptive-breakpoint/mobile-thumb/desktop records · preserve navigation, theme, typography, keypad, privacy wipe, accessible-mode layout.

Code facts behind it: `idleWarnMs` = 40 s of no tap → modal `#idle-dialog` (Escape blocked) with a 20 s countdown → `resetSession()` wipes the DOM. Every tap/key calls `touch()`, so the failure is inter-keystroke gaps > 40 s plus a 20 s modal an older person must find and dismiss.

## 1. Design-context table (01-inspect.json vs code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| platform | web | KNOWN | kiosk — README says "Public touch kiosk", body is a fixed 1080×1920 panel, `touch-action: manipulation`, `--target-min: 72px` | **no** |
| navigation | hub-spoke | KNOWN | attract hub → linear 3-step flow (`steps: 3`, "Step 1 of 3") | yes |
| theme | unknown | UNKNOWN | light green brand theme + `html[data-a11y="on"]` high-contrast black/yellow mode, all in `tokens.css` | partial |
| surfaces | elevated | INFERRED | flat/tonal: 3–4 px borders, no card shadows (only the attract pulse halo); dialogs bordered, not shadowed | **no** |
| radius | medium (12) | INFERRED | `--radius: 20px` primary, `--radius-sm: 12px` keys; 32 px start button | partial |
| spacing | irregular | UNKNOWN | regular 8 px token scale `--space-1..7` = 8/16/24/32/48/64/96 | **no** |
| typography | humanist-sans (Nunito) | KNOWN | Nunito, weights 500–800, tabular numerals | yes |
| components | unknown | UNKNOWN | `.btn` (primary/secondary/util/choice), `.key`/`.keys--pad`/`.keys--qwerty`, `.field__value`, `.rxrow`, `dialog`, `.ticket`, `.banner` — all in `kiosk.css` | partial |

Context detection: navigation yes · theme partial · typography yes · surfaces no · spacing no. The platform miss is the root of most of what follows.

## 2. Requirements verdict (02-requirements.json)
- `platform`: **web** — wrong (kiosk). `platform_evidence` is empty; the value came straight from the inspector. No MISSING confirm entry, so this is a confident wrong platform, not an honest unknown. **Failure.**
- `intent.artifact_state`: existing — correct.
- `intent.operations`: diagnose + modify — correct.
- `intent.problem_domain`: `[]` — miss; `scope_evidence.ui` already found `concept:state.session_expiry` from "time out", but it never became a problem domain. `intent.change_scope`: unknown — should be "small/local" (one dialog, one timer).
- `mode`: audit + refactor, evidence "problem statement on existing UI / fix follows the diagnosis". refactor is acceptable; audit is not what the sentence asks (it reports a known failure, not a review) and it drove `required_concerns` towards a generic accessibility audit. Verdict: **acceptable**. accessibility mode (older users, WCAG 2.2.1 timing) was not detected.
- `scope.kind`: in-scope, reason "UI design / interaction task" — correct.
- `change_budget`: low — correct.
- `intent.preserve`: `[]` — `constraints.preserve_existing_system: true` compensates, but nothing names the privacy wipe or the keypad.
- `project_context`: carried over from the inspector, including the wrong `surfaces=elevated`, `spacing=irregular`.
- `status`: CONFIDENT — over-confident given the platform.

## 3. Guidance verdict (03-guidance.json/.md) — status PARTIAL, bundle 6 (core 2 + guardrails 4), 844 tokens

| record | role | verdict | BAD category | why |
|---|---|---|---|---|
| `nav-wizard` | core | off-target | generic | Step indicator / one primary action per step. The kiosk already has "Step 1 of 3" and one primary per screen; nothing about the timeout. Selected on lexical "step". |
| `surface-flat-tonal` | core | off-target | contradicts-codebase | Declared `incompatible with surface-elevated-cards`, which is the exact slot the direction says to preserve. The skill contradicts itself; either way surfaces are not the task. |
| `states-persistence-and-session` | guardrail | partial | — | The only record touching the problem: "warn before a session expires with a way to extend … on shared or public screens clear it instead". But its own `avoid_when` says "Public kiosks and shared screens … (see shared-device-privacy)" — the skill selected a record that disclaims this platform, because the platform was web. |
| `a11y-keyboard-operable` | guardrail | partial | — | Physical keypad/scanner wedge must keep working — relevant. But "the modal itself must be escapable (Escape)" contradicts the codebase's deliberate `cancel` → `preventDefault()` on the privacy countdown. Ignored that clause. |
| `a11y-focus-visible` | guardrail | off-target | generic | The kiosk already has a `:focus-visible` ring token; not the task. |
| `web-responsive-breakpoints` | guardrail | off-target | off-platform | 320–1920 px breakpoint matrix and drawer↔rail transforms for a fixed 1080×1920 panel. Direct consequence of platform=web. |

Relevant 0 · partial 2 · off-target 4. Filtered on platform grounds (`rejected`): `kiosk-public-use` (concepts `touch.minimum_target`, `privacy.shared_device`, `state.session_expiry` — the record that says "idle timeout with countdown that clears the session"), `comp-kiosk-keypad` (the very component being fixed: live region, focus never falls to body, physical keypad into the same field, reach zone), `nav-hub-spoke`. `shared-device-privacy` and `a11y-time-and-auto` ("kiosks show a visible countdown before resetting") were candidates but scored below the web record (0.136 vs 0.571).

Concerns: required accessibility/interaction/component, `component` uncovered — because the only component record for this screen (`comp-kiosk-keypad`) was platform-filtered.

### Concept recall
Delivered concepts (union over selected records): `feedback.progress_indicator`, `onboarding.linear_wizard`, `state.saving_conflict`, `state.session_expiry`, `feedback.confirmation_destructive`, `interaction.keyboard_navigation`, `interaction.hover_independence`, `interaction.focus_visible`, `adaptive.breakpoint_matrix`, `adaptive.navigation_transform`.

| expected id | delivered? | layer if missing (from `concept_trace`) |
|---|---|---|
| `state.session_expiry` (critical) | yes (`states-persistence-and-session`) | — |
| `privacy.shared_device` (critical) | no | expected-concepts — never demanded; the records that carry it (`kiosk-public-use`, `shared-device-privacy`) are kiosk-scoped and were platform-rejected |
| `a11y.live_status` | no | expected-concepts — not in the trace (`a11y-live-status` and `comp-kiosk-keypad` carry it) |
| `a11y.dialog_focus` | no | expected-concepts — not in the trace (`a11y-modal-dialog`, `comp-dialog` carry it) |
| `interaction.focus_restore` | no | expected-concepts — not in the trace (`a11y-modal-dialog`, `comp-kiosk-keypad`) |
| `touch.minimum_target` | no | bundle-selection — demanded as recommended ("touch on web"), candidate `a11y-target-size` 0.27, "bundle cap or lower utility left them out" |
| `process.safe_modification` | no | expected-concepts — only `process.reuse_first` was demanded, and that was dropped too |

**Recall 1/7 = 0.14 · critical recall 1/2 = 0.50.** Forbidden concepts delivered: `adaptive.breakpoint_matrix`, `adaptive.navigation_transform` (2 of the forbidden list).

Knowledge gap check (`03-search-k12.txt`, `search -k 12`): the base has every expected concept; no knowledge-gap. The search run (no project file) even flags `MISSING: platform` — the honest answer the guidance run lost by trusting the inspector's "web".

## 4. Direction verdict (04-direction.json/.md)
Compatibility: 11 slots preserved (navigation, layout, surface, cards, typography, color, motion, cta, imagery, icon, metadata), 0 changed, 2 **new**: `density-high` and `focus-ring-standard`. Validation OK; `preservation` metric effectively 11/13.
- `density-high` ("32 px row height, 13–14 px body") — **not justified**: a public kiosk for older customers with 72–112 px targets and 28 px+ body is the opposite; "no repository evidence" is wrong, the evidence is in `tokens.css`. Ignored.
- `focus-ring-standard` — harmless but mis-labelled "new": `:focus-visible { outline: var(--ring) … }` already exists. Context-detection miss.
- Preserved slots and the closing line ("preserved slots are the existing system and win") are right and were followed.
The direction never mentions the timeout, the dialog, or timing — it has no slot for interaction/state, so the task's actual subject is absent from it.

## 5. Implementation (files changed; `before/` holds the originals)
`js/app.js`, `js/i18n.js`, `index.html`, `css/kiosk.css` (+8/+4/+1/+8 lines, no removals; CRLF preserved).
- Identify screens get their own window: `entryWarnMs` 90 s (was the shared 40 s) and `entryCountdownS` 30 s (was 20 s); `touch()` picks the window from `screen.startsWith('identify')`. List/confirm/done keep 40 s / 20 s — fetched prescription data still clears on the old schedule.
- Warning dialog on the identify step: title "Take your time", lede says the typed value is kept *and* that the screen will clear, a "So far: 04 / 12 / 19" echo of the typed value in the existing `.field__value` treatment, primary action "Keep typing". List/confirm keep "Are you still there? / I'm still here" and no echo (no PHI in the dialog).
- Presence: any touch on the dialog or its backdrop = keep typing; any `pointerdown` on the panel resets the timer (a finger that misses a key counts); a physical-keypad key while the warning is up dismisses it *and* types. Escape still blocked; "Finish now" still wipes; countdown expiry still wipes (verified: no DOB/name text left in the DOM).
- Both languages; both view modes; dialog sits over the keypad (`margin-top: 560px`) so it reads as part of the step and stays in the accessible-mode reach zone.
- Guidance **used**: `states-persistence-and-session` ("warn before expiry with a way to extend; shared screens clear instead" — which the code already did), `a11y-keyboard-operable` (physical keypad keeps working through the modal). **Ignored**: `nav-wizard`, `surface-flat-tonal` (contradicts preserved surface), `a11y-focus-visible` (already present), `web-responsive-breakpoints` (fixed panel), the Escape-must-close clause (privacy), direction `density-high`. The kiosk-specific rules the fix actually follows (`kiosk-public-use`, `comp-kiosk-keypad`, `a11y-time-and-auto`) came from reading the codebase and the reviewer expectation, not from the bundle.

## 6. Render — mode `html` (native HTML in Chromium via Playwright 1.63, 1080×1920, `hasTouch`)
`render/first-*.png` (5 standard + 5 accessible) and `render/final-*.png` (same set); `render/baseline-idle-during-dob.png` is the pre-change dialog for comparison. Shots: identify-DOB mid-entry, warning during DOB, warning during name, name screen after dismiss (focus back on the last key), warning on the list screen.

**First-render defects:** accessibility 1 — the entry lede said "Touch the screen or press a key to keep going." without saying the screen would clear; a 30 s number with no stated consequence fails the WCAG 2.2.1 "warned before time expires" intent. Visual 0, interaction 0, platform 0, existing-system-mismatch 0, implementation-bug 0.
**Fix (iteration 1):** lede now "…to keep going before the screen clears." (EN/ES). Re-rendered.
**Final defects:** 0 in every type. **Iterations: 1.**

Interaction check (`render/interact.js` → `05-interaction.json`, re-run on the final state): **23/23 pass** — identify window longer than data-screen window; data screens unchanged at 40 s/20 s; entry wording + echoed value; countdown uses the entry value; touch anywhere / backdrop / physical key dismiss; typed value kept; focus returns to a key not `body`; Escape still blocked; Finish now and expiry both wipe the DOM; list dialog keeps privacy wording with no echo; dialog buttons ≥ 64 px in both modes; dialog fully on the panel; accessible-mode controls at y ≥ 768 (reach zone); Spanish strings.

## 7. Preservation verdict
navigation ✓ · theme ✓ (tokens untouched) · typography ✓ · keypad component ✓ (unchanged) · privacy wipe ✓ (list/confirm timing untouched, expiry still wipes) · accessible-mode layout ✓ · component reuse ✓ (`.field__value` treatment, `.btn--primary/--secondary`, existing `dialog`, `paintChrome`, `t()` i18n) · unjustified structural changes 0. **preservation-ok.**

## 8. Skill misses by earliest wrong layer
1. **platform** — inspector returned `web` for a project whose README first line and body CSS say kiosk 1080×1920; requirements accepted it with no evidence and no MISSING entry. Downstream: `kiosk-public-use`, `comp-kiosk-keypad`, `nav-hub-spoke` rejected; `shared-device-privacy` out-scored; `web-responsive-breakpoints` and `adaptive.*` concepts pulled in; component concern left uncovered.
2. **mode** — audit chosen for a sentence that reports a known failure; accessibility (timing, older users) not detected.
3. **requirements** — `problem_domain` empty although the scope evidence found `state.session_expiry`; `change_scope` unknown; `preserve` empty.
4. **expected-concepts** — `privacy.shared_device`, `a11y.live_status`, `a11y.dialog_focus`, `interaction.focus_restore`, `process.safe_modification` never demanded (dialog/focus concepts should follow from a session-expiry dialog on an existing screen regardless of platform).
5. **bundle-selection** — `touch.minimum_target` demanded, `a11y-target-size` candidate, dropped; `surface-flat-tonal` selected as core although incompatible with the preserved surface.
6. **direction** — `density-high` as a new slot with change budget low; focus slot marked "new" for an existing ring.
7. **context-detection** — surfaces `elevated` (actually bordered/flat), spacing `irregular` (8 px scale), theme UNKNOWN (clear in tokens.css).

**Skill effect: neutral.** The bundle's one applicable sentence restated what the code already did; the wrong parts were easy to ignore; the fix came from the codebase and the expectation. It did not hurt only because the implementer refused `density-high`, `surface-flat-tonal` and the Escape clause.

## 9. Regressions to propose
1. `inspect_project` on `p3-kiosk-pharmacy/project` → `platforms` contains `kiosk` (README "Public touch kiosk", fixed 1080×1920 body, `--target-min ≥ 64px`), not `web`.
2. `requirements "Older customers time out on the identify step before they finish typing." --project <kiosk inspect>` → platform kiosk; `problem_domain` includes session/timing; mode includes accessibility or refactor, not audit; `change_scope` small.
3. `guidance` for the same sentence with platform kiosk → bundle contains `kiosk-public-use` or `shared-device-privacy` **and** `a11y-time-and-auto` (visible countdown, extendable); must not contain `web-responsive-breakpoints`; delivered concepts include `privacy.shared_device`, `a11y.dialog_focus`, `touch.minimum_target`.
4. `guidance` must never select a core record whose `incompatible_with` names the direction's preserved slot (`surface-flat-tonal` vs `surface-elevated-cards`).
5. `direction` with change budget low and a state/interaction task → no `new` density slot; density for platform kiosk is never `density-high`.
6. `requirements` with a project file whose platform is unsupported by the sentence → `platform_evidence` non-empty or a MISSING confirm entry, never a silent CONFIDENT.

## Tags
`platform-miss` `mode-miss` `requirements-miss` `concept-miss` `ranking-miss` `direction-mismatch` `context-detection-miss` `render-defect-fixed` `skill-neutral` `preservation-ok`
