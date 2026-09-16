# p6-30 — MetroLink transit kiosk, idle timeout / session reset

**Task (verbatim):** "People walk away mid-purchase and the next person finds the previous ticket half bought."
**Project:** `research/phase6-projects/p6-kiosk-transit/project` · plain HTML/CSS/JS, no build · platform **kiosk** (1080×1920 portrait touch).
**Existing UI**, no new screen. Build hash start == end == `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`.
Two sibling tasks edited the quantity stepper and the language strings in the same repo while this task ran; I touched only the idle/session-reset logic and its overlay.

## What the code actually did (read before running any advise command)

`js/app.js` already had a 20 s idle timer that called `resetState()` + `show('attract')`. Two real holes:

1. **No warning, no way to continue.** A customer who paused to find their card lost the basket silently.
2. **`resetState()` cleared state but not the DOM.** Selected `.ticket-card` / `.zone-chip` kept `is-selected`, `#qty-value`, `#rv-*`, `#pay-amount`, `#done-ref` and the pay-terminal status class kept the previous customer's values — literally "the next person finds the previous ticket half bought".

## 1 · Design-context table (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | hub-spoke | KNOWN | attract screen as hub, but a single linear 7-step wizard as the only spoke | partial |
| theme | light-first | INFERRED | light only, `--c-bg #F7F4EF`; README: "No dark mode" (intentional) | yes |
| surfaces | elevated | INFERRED | white cards on warm bg with `--shadow-1` | yes |
| radius | small (5px) | INFERRED | `--radius: 16px` on every card and button | no |
| spacing | 4 | INFERRED | 8-pt scale (`--sp-1..8` = 8/16/24/32/48/64) | no |
| typography | unknown | UNKNOWN | `--font: "Inter", system-ui…` + 28/36/48/64 scale in `tokens.css` | partial |
| components | unknown | UNKNOWN | no component dir; BEM classes only | yes |

The inspector did not read `css/tokens.css` custom-property *values* — it counted literal px in `kiosk.css` (12 px card icon radius, 6/8/12 px one-off gaps) and missed the token file that declares radius, spacing and the font. That is the whole context-detection miss on this project.

## 2 · Requirements verdict (`02-requirements.json`)

| item | value | verdict |
|---|---|---|
| platform_evidence | kiosk, WEAK_INFERENCE ("ticket", "next person") + project inspection | correct |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | **navigation** | wrong — the domain is session/state on a shared device; "navigation" came from the token "find" |
| intent.change_scope | unknown (scope: moderate) | acceptable |
| mode + evidence | audit, refactor ("navigation defect on existing UI") | acceptable (expected refactor/polish/audit) |
| scope.kind | in-scope | correct |
| change_budget | moderate | correct |
| intent.preserve | [] but `constraints.preserve_existing_system: true` | acceptable |
| project_context | carried through from inspect, including the wrong radius/spacing | inherited miss |

## 3 · Guidance verdict (`03-guidance.md` / `.json`)

status=PARTIAL. Bundle = **1 record, 132 tokens**: CORE empty, CRITICAL GUARDRAILS 1, OPTIONAL absent.

| layer | record | review | category |
|---|---|---|---|
| critical | `kiosk-public-use` | relevant | — |

The one record earns its place: "…idle timeout with countdown that clears the session, attract screen as the hub … a visible way to cancel at every step" is exactly the shape of the fix. No off-target or harmful record. `layer_review`: core [], critical [`kiosk-public-use`], optional [], optional_useful 0, optional_noise 0.

### Concept recall

| expected id | critical | delivered? | layer if missing |
|---|---|---|---|
| state.session_expiry | | yes (`kiosk-public-use`) | — |
| privacy.shared_device | ✓ | yes | — |
| feedback.confirmation_destructive | | no | expected-concepts (never demanded; concern `feedback` was only "recommended" and then "not surfaced") |
| feedback.progress_indicator | | no | expected-concepts |
| touch.minimum_target | ✓ | yes | — |
| a11y.live_status | | no | expected-concepts |

recall 3/6 = **0.50**; critical recall 2/2 = **1.00** (my pre-registered criticals were `state.session_expiry` + `privacy.shared_device`; the skill's own criticals were `privacy.shared_device` + `touch.minimum_target`).

Notable: `search` shows the base *does* carry three records that fit this task better than anything omitted — `a11y-time-and-auto` ("timeouts warn and allow extension; kiosks show a visible countdown before resetting", score 0.285), `shared-device-privacy` (0.287, and it was the top candidate for `privacy.shared_device` but lost selection to `kiosk-public-use`) and `states-persistence-and-session` (0.244, whose "avoid when" clause names public kiosks explicitly). None reached the bundle although the soft cap is 6 and the bundle used 1. No knowledge gap — a selection/criticality thinness. The three missing concepts were never *demanded* for this request, so the earliest wrong layer is `expected-concepts`, not `bundle-selection`.

## 4 · Direction verdict (`04-direction.md`)

12 slots preserved, 1 `new`: **cta → `cta-single-primary`** ("no repository evidence for this slot"). The project already states "One primary action per screen" in its README, so this is a detection gap surfacing as `new`; it pushed no change. `unjustified_direction_slots = 1` (cta), benign — nothing was restyled because of it. `preservation` metrics: navigation/layout/density/surface/cards/typography/color/motion/focus/imagery/icon/metadata all preserved. Validation: OK. The navigation slot note — "On kiosks, the hub also serves as the idle/attract screen and every spoke must time out back to it" — matched the existing architecture and was worth having.

## 5 · Implementation

Files changed (originals in `before/`): `index.html`, `css/kiosk.css`, `js/app.js`. No new files, no new tokens, no dependency.

- **Two-stage idle.** `IDLE_MS` → `IDLE_WARN_MS` (20 s, unchanged trigger point) + `IDLE_GRACE_MS` (10 s). At 20 s an `alertdialog` overlay appears over the current screen: "Are you still there?", a live countdown line "Clearing in N seconds", **Start over** (secondary) and **I'm still here** (primary), both 120 px tall, reusing `.btn--secondary`/`.btn--primary btn--lg`.
- **Only the explicit button extends the session.** The document-level `pointerdown/keydown/touchstart` listener returns early while the warning is up, so a passer-by brushing the glass cannot keep a stranger's basket alive. This is the deliberate reading of the task sentence.
- **`resetState()` now clears the DOM too**: `is-selected` on ticket cards and zone chips, `#qty-value`/`#qty-total`/`#qty-summary`/`#qty-limit`, `#rv-*`, `#pay-amount`, `#done-ref`, the `pay__terminal` status class and the confirm button's disabled state.
- Printing is still never interrupted; `done` is also skipped (it has its own 12 s auto-return). Approval arriving during the grace period calls `show('printing')`, which cancels the warning.
- `window.__kiosk` gained `warnIdle` / `goIdle` for QA scripts, matching the file's existing QA hook.
- Strings for the overlay were put inline in `index.html` rather than in `js/i18n.js`, because a concurrent task owns that file; it has since picked up `idle.title` / `idle.continue` on its own. The body sentence and the countdown line are still English-only — that is a handoff, not a finished i18n.

**Guidance used:** `kiosk-public-use` — the countdown-before-clearing, "one task per screen", ≥60 px targets and "visible way to cancel at every step" all landed in the overlay. **Guidance ignored:** none. The direction's `cta-single-primary` "new" slot was a no-op (the project already does this).

**Process guidance check.** `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` were *not* in the bundle and were not needed: the codebase's own conventions (BEM + token vars + the existing `.btn` modifiers) made reuse obvious, and render-verify is in my loop anyway. `process_records_needed: false`.

## 6 · Render

Playwright 1.63.0, Chromium, 1080×1920, real project files (`render/shot.js`). Six states per pass: mid-purchase review, warning, post-expiry attract, next person's choose-ticket, continue-path, warning over the pay screen. I looked at every final screenshot.

**First-render defects (3)** — `visual` 2, `platform` 1, others 0:
1. visual — the inline `<strong>` countdown inside the sentence rendered as "clears your ticket in  9  seconds" with a 2ch gap either side (`min-width: 2ch` + `inline-block`).
2. visual — the reserved `.idle__status` live-region paragraph left a 40 px dead band above the buttons.
3. platform — the overlay used `position: absolute` inside `.kiosk`, which is an unpositioned flex container; it resolved against the initial containing block by accident rather than by intent and did not reliably veil the kiosk header/footer chrome.

**Fix (1 iteration):** countdown moved to its own 36 px bold line, the status paragraph merged into it (one `role="status"` element), overlay switched to `position: fixed`. **Final defects: 0.**

Known tradeoffs, written down rather than fixed: the countdown live region updates every second (chatty for a screen reader, but this deployment is touch-only and has no SR); the dialog sets `aria-modal` without a JS focus trap (no keyboard on the hardware); the warning can fire while someone is fumbling for their card on the pay screen — "I'm still here" covers it and the terminal keeps polling.

## 7 · Preservation

Navigation model, screen flow, theme, tokens, type scale, button components, ids, `data-screen` contract and `window.__kiosk` all intact. No route, no state key and no existing id removed. The only structural addition is one overlay element. `preservation-ok`, unjustified structural changes: 0.

## 8 · Miss routing (earliest layer)

| miss | layer |
|---|---|
| `intent.problem_domain = navigation` instead of state/session | requirements |
| `feedback.confirmation_destructive`, `feedback.progress_indicator`, `a11y.live_status` never demanded | expected-concepts |
| radius=small, spacing=4, typography=UNKNOWN (token file not parsed) | project-context |
| direction slot `cta` marked `new` on a project that already does single-primary | project-context |
| overlay positioning, countdown typesetting | implementation |

## 9 · Regressions to propose

- query: "People walk away mid-purchase and the next person finds the previous ticket half bought." (project: kiosk) — expect the bundle to demand a *warn-before-clear* concept (`feedback.confirmation_destructive` or an idle-warning concept) and to surface `a11y-time-and-auto`, not only `kiosk-public-use`.
- query: any kiosk request whose project inspection reports `environment=public` — expect `state.session_expiry` to be demanded as **critical**, not merely recommended.
- inspector regression: a project whose radius/spacing/font live only in a `tokens.css` custom-property block — expect `radius=16px`, `spacing=8`, `typography=Inter`, not the literal px counted from the component sheet.

## Tags

`requirements-miss`, `concept-miss`, `context-detection-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`
