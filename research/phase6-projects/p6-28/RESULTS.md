# p6-28 — "The player controls stay on screen for the whole film."

- **Project / stack / platform:** `p6-tv-iptv-web` (Meridian TV) — plain HTML/CSS/JS, no build step, Samsung Tizen 5.5 + LG webOS 5.0, fixed 1920×1080. Platform = **tv**.
- **Existing UI**, no new screen. Change confined to the player (`js/app.js` `PlayerScreen`, `css/tv.css` `.overlay`); the guide is being changed by another task and was not touched.
- **Build hash:** start `ea8eed72…d9947`, end `ea8eed72…d9947` — **equal**, as required.

## 1. Design context (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| platform | `web` | — | TV web app: `config.xml` (Tizen widget), `appinfo.json` (webOS), `tizen.tvinputdevice`, remote key codes 10009/461, fixed 1920×1080 | **no** |
| navigation | top-bar | KNOWN | `.topbar` + `#topnav`, hidden on the player screen | yes |
| theme | dark-first | INFERRED | `--bg #0E1116`, dark-only by README | yes |
| surfaces | bordered-flat | INFERRED | flat surfaces `--surface #171C24`, 1px `--line` borders, no shadows | yes |
| radius | small (4) | INFERRED | `--radius: 8px`; 4px only on the progress bar and badge | partial |
| spacing | 4 | INFERRED | 8-based: `--gap 24`, `--gap-lg 40`, safe area 5vw/5vh | partial |
| typography | unknown | UNKNOWN | `--font: "Roboto", …` and a 28/32/40/56/72 TV scale in `tokens.css` | partial |
| components | unknown | UNKNOWN | no component dir (screens are functions in `app.js`) — fair | yes |

The platform row is the consequential one: `inspect_project.py` treats "*.html without a framework manifest" as web and never looks at `config.xml` / `appinfo.json` / `tizen.*`, even though both TV manifests sit in the project root.

## 2. Requirements verdict (`02-requirements.json`)

| field | value | verdict |
|---|---|---|
| platform | `["web"]`, `platform_evidence: tv WEAK_INFERENCE ("player controls")`, status CONFIDENT, `missing: []` | **wrong** — it saw TV evidence, ranked project inspection above it, and emitted no MISSING confirm |
| artifact_state | existing | correct |
| operations | diagnose, modify | correct |
| problem_domain | interaction | correct |
| change_scope | local | correct |
| mode | audit + refactor (evidence: "interaction defect on existing UI" / "fix follows the diagnosis") | acceptable (expected refactor/polish; audit-then-fix is a fair reading of a complaint with no mode word) |
| scope.kind | in-scope, "UI design / interaction task" | correct |
| change_budget | moderate | correct |
| intent.preserve | `[]` | thin, but `constraints.preserve_existing_system: true` carries it |
| input | keyboard, pointer, **touch** | wrong, follows from platform=web — a TV has no touch or hover |

## 3. Guidance verdict (`03-guidance.md` / `.json`)

status `PARTIAL`, bundle = 2 core, 0 guardrails, 0 optional, 581 tokens.

| record | layer | verdict | category |
|---|---|---|---|
| `comp-player-controls` | core | **relevant** — carries the exact fix: "controls overlay auto-hides except while focused/hovered", plus labelling | — |
| `comp-mini-player` | core | **off-target** — picture-in-picture / mini-player state; the task is not about a mini player. It entered only to cover `state.loading_empty_error`. Its TV sentence about focus restoration on BACK was incidentally useful | `wrong-screen` |
| (bundle) | — | — | `missing-critical` does **not** apply: both pre-registered critical concepts were delivered |

Layer review: core `[comp-player-controls, comp-mini-player]`, critical `[]`, optional `[]`; optional_useful 0, optional_noise 0.

**The two records that actually describe this task were both kept out.** `advise.py search` ranks `layout-split-player` 2nd (0.546) — *"show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause"* — and `tv-player-controls` 3rd (0.447) — *"overlay auto-hides after 3–5 s of no input (any key resets the timer)"*. `layout-split-player` was **omitted** with the reason "no positive task evidence (screen / subtype / component / job / product / wording) for a core record", despite screen=player and product=media matching. `tv-player-controls` and every other TV record (`anti-desktop-scaled-to-tv`, `comp-tv-side-sheet`, `dir-cinematic-media-tv`, `dir-broadcast-guide-tv`) were **platform-filtered out** by `platform ['tv'] not in request ['web']`. I wrote the implementation against the omitted records' content, which I only saw because the protocol asks for `search --explain`.

### Concept recall

delivered = `tv.player_autohide`, `a11y.accessible_names`, `media.track_selection`, `interaction.focus_restore`, `interaction.back_semantics`, `state.loading_empty_error`, `tv.safe_margins`.

| expected id | delivered? | layer if missing |
|---|---|---|
| `tv.player_autohide` (critical) | yes (`comp-player-controls`) | — |
| `interaction.focus_restore` (critical) | yes (`comp-mini-player`) | — |
| `interaction.dpad_reachability` | no | expected-concepts — never demanded; the requirements never asked for D-pad concepts because platform=web |
| `interaction.focus_visible` | no | bundle-selection — trace: "candidates existed but the bundle cap or a lower utility left them out (a11y-focus-visible, focus-ring-standard)" |
| `a11y.reduced_motion` | no | bundle-selection — candidates `a11y-reduced-motion`, `a11y-time-and-auto` existed, not surfaced |
| `tv.no_touch_hover` | no | expected-concepts — the opposite was asserted (`input` includes touch and pointer) |

concept recall **2/6 = 0.33**; critical recall **2/2 = 1.00**.

The skill's own required-concept set is a different list and it scores itself 1/4 (0.25), with `interaction.keyboard_navigation`, `interaction.hover_independence` and `interaction.focus_visible` uncovered and `adaptive.breakpoint_matrix` / `touch.minimum_target` demanded — both wrong for a TV app with "do not add responsive breakpoints" written in its README.

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`, 0 `changed`, 0 `new`. Validation OK. **`unjustified_direction_slots: 0`** — correct for an existing UI at a moderate budget. The colour slot even volunteers the right TV note ("On TV target ≥7:1 … avoid saturated reds/oranges"), so TV knowledge leaks through the slot text while being filtered out of the bundle. The navigation slot text ("collapse to a menu button below the container width") is web boilerplate, harmless because the slot is preserved.

## 5. Implementation

Files changed (copies in `before/`): `js/app.js` (`PlayerScreen` only), `css/tv.css` (`.overlay` only).

- `OVERLAY_MS = 5000` idle timer; the overlay fades out when nothing has been pressed.
- Any remote key brings it back (`showOverlay`) and resets the timer; the first press *only* wakes the controls, it does not also move focus or activate the control underneath.
- **Never hides while paused** — `hideOverlay` returns early when `playing` is false.
- Focus restoration: the control that was focused is remembered and re-focused on wake; `F.clear()` while hidden so the d-pad has no invisible target.
- Hidden state is `opacity:0; visibility:hidden` with `aria-hidden`, `inert` and `tabindex=-1` on both controls; `prefers-reduced-motion` drops the fade to 0s.
- Added the missing `aria-label` on the subtitles button (it had none) and kept it in sync with state.
- `destroy()` clears the hide timer alongside the existing tick timer.

Existing conventions reused: `h()` helper, `F.setFocus/clear`, the `.hidden`-style class toggle idiom, amber focus ring, `--safe-x/--safe-y`, the existing `onKey` contract. No token, navigation, type or colour change.

**Guidance used:** `comp-player-controls` (auto-hide + accessible names), `comp-mini-player` (focus restoration on return — the only part that applied). **Guidance ignored:** `comp-mini-player`'s mini-player/PiP construction (not the task); `comp-player-controls`' "except while focused/hovered" taken literally (on TV a control is always focused, so obeying it verbatim would make auto-hide impossible — I used "any key resets the timer" instead, which is what the filtered-out `tv-player-controls` says); `input: touch/pointer` and `adaptive.breakpoint_matrix` (README forbids breakpoints).

**Process guidance check:** SKILL.md §2/§7 was enough — I reused the existing focus manager and class-toggle idiom and rendered before claiming anything. `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` were **not** needed in the bundle (`process_records_needed: false`), and their absence saved tokens for a bundle that was already too thin.

## 6. Render and defects

Render mode: **native** (Playwright/Chromium, `file://`, 1920×1080), `render/shoot.js` + `render/edge.js`. Screens captured: detail → player visible → 6 s idle → wake → paused. No console or page errors in either pass.

**First render defects — 1:** `accessibility` 1 — `aria-hidden="true"` was set on the overlay while its two `<button>`s stayed in the tab order (the axe "aria-hidden-focus" violation). Found by inspecting the hidden state, not by the guidance. All behaviour assertions passed on the first pass (hidden after idle, restored on any key with focus back on Pause, second press moves focus, controls stay up while paused, BACK from the hidden player returns to Detail with focus on Play, no stray timer after leaving the screen).
`visual` 0, `interaction` 0, `platform` 0, `existing-system-mismatch` 0, `implementation-bug` 0.

**Fix:** `inert` + `tabindex=-1` on the controls when hidden. **Iterations: 1. Final defects: 0 in every category.**

No defect the guidance warned about was shipped.

## 7. Preservation

Navigation, theme, typography, tokens, component reuse all intact; 0 unjustified structural changes. The topbar is still hidden on the player as before; the overlay's layout, gradient and control geometry are unchanged — only its visibility over time changed, which is the task.

## 8. Misses by earliest layer

1. `platform-evidence` — TV project resolved as `web`, status CONFIDENT with no MISSING confirm, despite `platform_evidence` listing tv. Root cause upstream in `inspect_project.py` (see `project-context` below), but the resolver had the tv evidence in hand and dropped it.
2. `project-context` — `inspect_project.py` ignores `config.xml`/`appinfo.json`/`tizen.tvinputdevice` and reports `platforms: ["web"]`; it also reports typography UNKNOWN when `tokens.css` declares `--font`.
3. `bundle-selection` — `layout-split-player` (the single best record for this sentence, score 0.546, screen and product both matching) omitted as "no positive task evidence"; `interaction.focus_visible` and `a11y.reduced_motion` candidates dropped.
4. `candidate-compatibility` — every TV record filtered by the wrong platform, so `tv-player-controls` never reached selection.

## 9. Regressions to propose

- query: `The player controls stay on screen for the whole film.` with a project whose root has `config.xml` + `appinfo.json` + `tizen.tvinputdevice` → expect platform `tv` (or `unknown` with a MISSING confirm), never a CONFIDENT `web`, and no `touch` input.
- query: `inspect_project.py` on a plain-HTML project containing a Tizen `config.xml` or webOS `appinfo.json` → expect `platforms` to include `tv`.
- query: any player-overlay sentence on a media product with `screen=player` → expect `layout-split-player` in the core bundle; it must not be omitted for "no positive task evidence".
- query: `The player controls stay on screen for the whole film.` on a TV project → expect `tv-player-controls` in the bundle and `interaction.dpad_reachability` in the required concepts.
- query: any TV task → `adaptive.breakpoint_matrix` and `touch.minimum_target` must not appear in required/recommended concepts.

## 10. Tags

`platform-miss`, `context-detection-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch` (no), `render-defect-fixed`, `preservation-ok`, `skill-helped`, `partial-scope-ok`

Actual tag list: `platform-miss`, `context-detection-miss`, `concept-miss`, `ranking-miss`, `render-defect-fixed`, `preservation-ok`, `skill-helped`.

**skill_effect: helped** — `comp-player-controls` named auto-hide as the defect and `comp-mini-player` named focus restoration on return; the focus-restore requirement is the part I would most plausibly have under-specified (restoring the previously focused control rather than resetting to play/pause). It helped *despite* resolving the platform wrong, and it would have helped considerably more had it not filtered its own TV player record out of the bundle.
