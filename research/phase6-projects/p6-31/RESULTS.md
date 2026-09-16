# p6-31 — "The + and − buttons for the number of tickets are fiddly for older passengers."

- **Project:** `research/phase6-projects/p6-kiosk-transit/project` — MetroLink TVM front end.
- **Stack / platform:** plain HTML + CSS + ES5, no build step / **kiosk** (1080×1920 portrait touch).
- **Existing UI**, no new screen. Only the `quantity` step and its styles were touched.
- **Build hash:** start `ea8eed72…d9947`, end `ea8eed72…d9947` — **equal**.

## 1. Design context (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | hub-spoke | KNOWN | linear wizard `attract → choose-ticket → quantity → review → pay → printing → done`; attract doubles as idle hub | partial |
| theme | light-first | INFERRED | single light theme, dark mode explicitly rejected in README | yes |
| surfaces | elevated | INFERRED | `--shadow-1/2` on cards and buttons, 1px borders | yes |
| radius | small (5px) | INFERRED | `--radius: 16px`, `--radius-sm: 8px`; the 5px figure comes from the SVG logo, not the UI | no |
| spacing | 4 | INFERRED | 8-pt scale `--sp-1..8` = 8/16/24/32/48/64 | no |
| typography | unknown | UNKNOWN | `--font: "Inter", system-ui, …` declared in `css/tokens.css`, full 28/36/48/64 scale | no (value is in the code) |
| components | unknown | UNKNOWN | BEM component classes (`.btn`, `.ticket-card`, `.zone-chip`, `.qty__*`) in one stylesheet | partial |

Three misses (radius, spacing, typography) all point at the same gap: the detector does not read `css/tokens.css` custom properties even though `tokens` in the same JSON lists `--sp* (6)`, `--radius* (2)`, `--fs* (4)`, `--font* (1)`. `--touch: 72px` — the single most relevant token for this task — is not surfaced anywhere in `design_context`. Layer: `project-context`.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Value | Verdict |
|---|---|---|
| platform / platform_evidence | `kiosk`, WEAK_INFERENCE from "tickets" + project README | correct (project-derived) |
| artifact_state | existing | correct |
| operations | diagnose, modify | correct |
| problem_domain | interaction | correct |
| change_scope | local | correct |
| mode / mode_evidence | `audit`, `refactor` — "interaction defect on existing UI" / "fix follows the diagnosis" | acceptable (I pre-registered polish/refactor/accessibility; `accessibility` never appears as a mode despite "older passengers", but all five `accessibility` flags are set true, so nothing was lost downstream) |
| scope.kind | in-scope, "UI design / interaction task" | correct |
| change_budget | moderate | correct |
| intent.preserve | `[]` | thin — the sentence implies preserving the flow, but `constraints.preserve_existing_system: true` carries it |
| project_context | as above | inherits the three detection misses |

"older passengers" produced no visible signal anywhere in the requirements (no `a11y.text_scaling`, no motor-impairment cue, no `accessibility` mode). The kiosk platform prior did all the work.

## 3. Guidance verdict (`03-guidance.md`)

`status=PARTIAL`, bundle = **1 record** (core 0, guardrails 1, optional layer absent), 132 tokens.

| Record | Layer | Verdict | Category |
|---|---|---|---|
| `kiosk-public-use` | critical guardrail | partial | `generic` |

`kiosk-public-use` carries the one thing that mattered — "targets ≥60 px, body ≥20 px, audio/visual feedback on every tap, reachable-height controls (ADA 380–1220 mm)" — and the reach clause caught a real defect in my first render. The other half of the record (idle timeout with countdown, attract screen as hub, privacy on shared devices, cancel at every step) is about screens this task is not on, and one clause (idle timeout) is owned by a concurrent task I was told not to touch. Useful ≈ 50% of its tokens.

Bundle-level defect: **`missing-critical`** — my pre-registered critical concept `a11y.accessible_names` is absent, although the two stepper buttons are exactly where a label defect lives (`aria-label="Fewer"` / `"More"`, glyph-only, no announcement of the changing count).

### Concept recall

| Expected id | Delivered? | Layer if missing |
|---|---|---|
| `touch.minimum_target` | yes (CRITICAL, SPECIFIC) | — |
| `a11y.accessible_names` | no | bundle-selection (trace: candidates `a11y-labels-names`, `comp-kiosk-keypad` existed, dropped on utility/cap) |
| `a11y.live_status` | no | bundle-selection (candidates `a11y-live-status`, `comp-kiosk-keypad`, `search-filter-feedback`) |
| `a11y.contrast` | no | bundle-selection (candidates `a11y-nontext-contrast`, `a11y-contrast-text`) |
| `layout.spacing_scale` | no | expected-concepts (never demanded) |
| `interaction.selection_visible` | no | expected-concepts (never demanded) |

Real concept recall **1/6 = 0.17**; critical recall **1/2 = 0.50**. The skill's own metrics report `concept_coverage_ratio 1.0` and `critical_coverage_ratio 1.0` — measured against its own three demanded concepts (`touch.minimum_target`, `privacy.shared_device`, `state.session_expiry`), two of which are off-task for a stepper-button sentence. Perfect self-scored coverage of the wrong concept set.

Inconsistency worth a regression: `metrics.not_surfaced` says each of the seven missing concepts had "no sufficiently specific guidance", while `concept_trace` for the same concepts says "candidates existed but the bundle cap or a lower utility left them out" and names them. The two explanations contradict each other.

PARTIAL_SCOPE note: status is `PARTIAL` on concern coverage (accessibility and component uncovered), not a design/engineering split — correctly flagged, and correctly so: the two uncovered concerns are precisely the ones the task needed.

## 4. Direction verdict (`04-direction.md`)

12 of 13 slots `preserved` with explicit "existing system: do not replace it for this task" reasons — right call on a moderate budget. `focus` carried a useful verify-don't-replace note. `cta` is `new` ("One primary action per screen") with reason "no repository evidence for this slot", which is false — `index.html` has exactly one `.btn--primary` per screen and the README states the rule. **`unjustified_direction_slots: 1`** (`cta`). It did no harm; its "disabled only with an explanation nearby" clause is the one clause I actually used.

`density` slot printed "Kiosk floor: targets ≥ 64 px, body ≥ 20 px" while simultaneously preserving the *detected* density of "spacing base 4" — the detected value is wrong (project is 8-pt), so "preserve" here preserves a fiction. Harmless because I read the real tokens, but it is a `project-context` miss surfacing in the direction.

Validation: OK. Preservation metrics: all slots preserved except `cta`.

## 5. Implementation

Files changed (before copies in `before/`):

- `css/kiosk.css` — `.qty` / `.qty__btn` / `.qty__value`, new `.qty__glyph`, `.qty__btn:disabled`, new `.qty__limit`.
- `index.html` — quantity section only: stepper reordered to `[−] [value] [+]`, real accessible names, `role="status" aria-live="polite"` on the value, `#qty-limit` line.
- `js/app.js` — two lines inside `renderQty()` to set the max-quantity explanation. Idle timer and i18n strings untouched.

What changed and why:

- Buttons **40×40 px → 224×224 px**. The project's own `--touch` is 72px and the README promises a "72 px minimum touch target"; the steppers were the only controls in the app violating it. 224px is deliberately well above the 60px guidance floor: these are the two controls named as fiddly, pressed repeatedly, by older passengers.
- Vertical stack (12px gap, both buttons to the right of the number) → **horizontal `− value +`** with a 48px (`--sp-6`) gap, so target separation matches the conventional mental model and mis-taps cannot hit the opposite control.
- Circle → `var(--radius)` 16px, border 2px → 3px, `--shadow-1`: aligns the steppers with `.btn--secondary`, the system's existing outlined-control language, instead of being a one-off shape.
- Glyph 24px → 96px (`.qty__glyph`), value 120px → 160px with tabular figures.
- **Disabled state**: `.qty__btn` has no `.btn` class, so `.btn:disabled { opacity: .4 }` never applied — at qty 1 and at max the buttons looked fully enabled and simply did nothing. Now a muted border/fill/glyph plus a plain-language reason line at the maximum.
- **Announcement**: the count is a live region; the buttons are named "One ticket fewer" / "One ticket more" rather than "Fewer" / "More".

Guidance used: `kiosk-public-use` (≥60px targets, reachable height, feedback on every tap); direction `cta` slot ("disabled only with an explanation nearby"). Guidance ignored: the idle-timeout / attract-hub / privacy clauses of `kiosk-public-use` (another task owns the idle timeout; not this screen), and the direction's `color` slot prose (generic; the existing palette is preserved verbatim).

Process guidance: SKILL.md §2/§7 was enough — I read `tokens.css` and `kiosk.css` before writing, reused `--touch`, `--radius`, `--sp-*`, `--shadow-1` and the `.btn--secondary` visual language, and rendered before claiming done. `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` in the bundle would have been redundant tokens here. `process_records_needed: false`.

## 6. Render

Playwright 1.63.0, Chromium, `file://`, viewport **1080×1920**, quantity screen at qty 1 and at max (10). Screenshots: `render/first-quantity-1080x1920.png`, `render/first-quantity-max-1080x1920.png`, `render/final-*`.

Tooling note: a concurrent task left `js/app.js` mid-edit — `touchIdle()` still referenced `IDLE_MS` after the constant was renamed to `IDLE_WARN_MS`, which threw `ReferenceError` on every `show()`. I did not touch their code; the render script shims `window.IDLE_MS` in an init script so the state machine runs. Their bug, not mine, and it is still there.

**First-render defects (1):**

| Type | Defect |
|---|---|
| visual | With 224px buttons the whole stepper sat between y≈410 and y≈640 of a 1920px portrait screen — high reach on a standing kiosk, with ~1000px of dead space under it. Guidance explicitly warned about reachable height, so this one counts against me, not the skill. |

Fix: `auto` top margin on `.qty` and `auto` bottom margin on `.qty__limit` centres the group between the summary and the action bar (stepper now centred at y≈765). **Iterations: 1.**

**Final defects: 0.** No console/page errors. Both bound states verified (minus disabled at 1, plus disabled at 10 with the explanation line).

**Preservation:** navigation, flow, screen ids, `#qty-value` / `#qty-minus` / `#qty-plus` ids, `__kiosk` QA hook, i18n keys, header/footer, theme, type scale and all tokens unchanged. `preservation-ok`.

## 7. Misses by earliest layer

| Layer | Miss |
|---|---|
| `project-context` | radius (5 vs 16), spacing (4 vs 8), typography (UNKNOWN vs a declared Inter stack) read wrong from a project whose tokens file is one flat `:root` block; `--touch: 72px` never surfaced |
| `expected-concepts` | `layout.spacing_scale` and `interaction.selection_visible` never demanded; `privacy.shared_device` and `state.session_expiry` demanded *as critical* for a two-button sizing sentence |
| `bundle-selection` | `a11y.accessible_names`, `a11y.live_status`, `a11y.contrast` had candidates and were dropped; core layer ended empty on an in-scope, confidently-classified task |
| `direction` | `cta` marked `new` with "no repository evidence", contradicted by the codebase and the README |
| `implementation` | first-render placement defect (mine) |

## 8. Regressions to propose

1. `"The + and − buttons for the number of tickets are fiddly for older passengers."` on a kiosk project → bundle must carry `a11y.accessible_names` and `a11y.live_status`; a glyph-only stepper is the canonical accessible-name defect.
2. Any sentence naming an age or ability group ("older passengers", "customers with arthritis") → expected concepts must include at least one a11y concept; today the phrase changes nothing in `02-requirements.json`.
3. Project inspection on a repo with a `:root` tokens stylesheet → `design_context.radius` / `spacing` / `typography` must be read from the custom properties, not inferred from asset SVGs and stray literals; a `--touch`-style target token should surface in `design_context`.
4. `metrics.not_surfaced` reason strings must agree with `concept_trace`: do not say "no sufficiently specific guidance" for a concept whose trace names surviving candidates.
5. A local interaction fix on an existing UI with a moderate budget → `direction` should have 0 `new` slots; `cta` must not be `new` for a project whose HTML shows one primary button per screen.

## 9. Skill effect

**helped**, narrowly. One clause of one record ("targets ≥60 px … reachable-height controls") is the reason I sized the steppers against a physical floor rather than by eye, and the reach clause is what made me re-place the cluster after the first render. Everything else I shipped — accessible names, live announcement, disabled state, corner/border language — came from reading the codebase, not the bundle. A one-record, 132-token bundle whose other half is about the idle timeout is a thin return on an unambiguous, in-scope task.

**Tags:** `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `tooling-limit`, `skill-helped`, `preservation-ok`, `partial-scope-ok`
