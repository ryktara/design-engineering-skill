# p4-09 — results

## Task
"accessibility audit and fix of the identify step of the pick-up kiosk: the date-of-birth keypad and name entry"

## Project / stack / platform
`phase3-projects/p3-kiosk-pharmacy/project` — plain HTML + CSS (cascade layers, custom-property tokens) + vanilla ES modules, public touch kiosk, portrait 1080×1920, hub-and-spoke flow. **Existing UI** (identify-dob and identify-name screens).

**Render mode: html (Playwright Chromium 1.63, 1080×1920, `hasTouch`).** `render/identify.js` reuses the Phase 3 static server and Playwright install; it screenshots both identify screens in standard and accessible mode (`first-*` / `final-*`) and runs 68 checks (`05-interaction-first.json`, `05-interaction-final.json`).

Note: another Phase 4 task added a first-visit language/view chooser to the attract screen of this project while this task ran; the `before/` copies already contain it, and the tests pass `?chooser=off` so the identify step is reached the same way as in Phase 3.

## Design-context table (`01-inspect.json`)
| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | hub-spoke | KNOWN | attract hub → linear spokes (identify → list → confirm → done), utility bar on every screen | yes |
| theme | unknown ("25 near-white, 17 near-black") | UNKNOWN | light theme plus a high-contrast accessible mode (black / yellow) switched by `html[data-a11y]` — two token sets in `tokens.css` | partial — the two-theme structure is exactly what the mixed palette means; not recognised |
| surfaces | elevated | INFERRED ("shadow 1, border 1") | flat surfaces with 3–4 px borders; the only shadow is the attract pulse | **no** |
| radius | medium (12; 20, 32) | INFERRED | `--radius-sm` 12, `--radius` 20, start button 32, pills 999 | yes |
| spacing | irregular ("6, 10") | UNKNOWN | an 8 px scale in tokens (`--space-1..7` = 8/16/24/32/48/64/96); 6 and 10 were two literals (caret margin, the key gap this audit removed) | **no** — the token scale was missed, the two off-scale literals were promoted to the verdict |
| typography | humanist-sans (Nunito, 700/800/600/500, tabular) | INFERRED | `--font-family: Nunito, Segoe UI Variable…`; sizes 24/28/32/40/60/84 as tokens | yes |
| components | unknown | UNKNOWN | hand-written BEM-style components (`.btn`, `.key`, `.field`, `.rxrow`, `<dialog>`), no library | acceptable (nothing to detect); "custom html-css" would be more useful |

## Requirements verdict (`02-requirements.json`, exit 4 AMBIGUOUS)
| field | value | verdict |
|---|---|---|
| scope | UI_ACCESSIBILITY, in_scope | right |
| mode / evidence | audit + accessibility (explicit) + polish ("change request about look/feel") | right; polish is a stretch for "fix" |
| change_budget | low | right |
| intent | existing=true, problem=false, diagnose_only=false, preserve=[] | partial — an audit implies problems; `problem:false` is odd but harmless |
| platform / input / environment | kiosk (KNOWN), touch (inferred), public | right; **keyboard is missing** — a kiosk with a scanner wedge and a tactile keypad has keyboard input, and the audit's biggest findings were keyboard/focus ones |
| product | healthcare, government | healthcare right; government wrong (README/data mention ADA/508 compliance, not a government product) |
| stack | html-css (KNOWN) | right (fixed since Phase 3) |
| screen / components | [] / [] | miss — "identify step", "keypad", "name entry" name a form/identify screen and keypad/keyboard components |
| accessibility flags | keyboard, screen_reader, touch_targets, reduced_motion, contrast | right |
| status | AMBIGUOUS: "platform conflict request kiosk vs project web" | **wrong** — the README says kiosk and the viewport is 1080×1920; the inspector reports `web` for any HTML project, and the resolver then flags a conflict against the correct request platform |

## Guidance verdict (`03-guidance.md`, AMBIGUOUS; 2 core + 4 guardrails; concepts 4/4, coverage/1k 4.31, purity 0.67, contaminated none)
| record | role | verdict |
|---|---|---|
| `comp-form` | core | partial — labels above, help text below, inline errors with recovery: applied (hint line, specific messages); autofill/IME/autosave/unsaved-guard do not apply |
| `nav-wizard` | core | partial — step indicator and back-without-loss already existed; not an audit target |
| `kiosk-public-use` | guardrail | relevant — "targets ≥60 px … ≥16 px spacing" (platform file) found the 10 px key gap; feedback on every tap, visible cancel, idle countdown re-tested |
| `shared-device-privacy` | guardrail | partial — "clear the session on idle" re-tested (live region wiped too); masking does not apply while a value is being typed |
| `a11y-labels-names` | guardrail | relevant — visible labels kept, `role=group` for the keypads (aria-label on a div was inert), "Hyphen" name for the "-" key |
| `anti-no-states` | guardrail | partial — "enumerate states" led to the invalid-date and short-name error states |

Totals: relevant 2 · partial 4 · off-target 0. Thin for an accessibility audit: only one accessibility record, none about forms/errors, focus, keyboard, or status announcements.

Misses:
- **ranking-miss** — `a11y-forms-errors` (search rank 4, 0.311: "error message next to the field, programmatically associated, what is wrong and how to fix, keep entered data") is the record for "date-of-birth … name entry" errors; not selected. Layer: bundle-selection.
- **ranking-miss** — `a11y-live-status` (0.641 on a targeted search) not selected; it drove the polite live region for typed digits. Layer: bundle-selection.
- **expected-concepts** — for mode audit+accessibility the required concepts were only touch target / privacy / session expiry / masking; forms_errors, live_status, focus_visible/keyboard were not required, so the bundle could be CONFIDENT on 4 concepts while the real audit findings sat outside it. Layer: expected-concepts.
- **knowledge-gap** — focus loss when a screen is re-rendered from a string (`innerHTML`) after every key: nothing in the base (the search returns TV focus rules). This was the most serious finding (keyboard/switch users fell back to `<body>` after every key). Layer: expected-concepts.
- **knowledge-gap** — on-screen keypad / keyboard pattern for kiosks (key size, spacing, delete/clear placement, value read-out, hint) still absent (same as Phase 3). Layer: expected-concepts.
- **knowledge-gap** — scanner keyboard-wedge and tactile keypad sharing the same keyboard input (burst vs human speed). Layer: expected-concepts.
- **requirements-miss** — input = touch only; the repository's `keydown` scanner handler and the platform file's "tactile keypad where regulations require" both imply keyboard. Layer: requirements.
- **scope/status** — AMBIGUOUS from a false platform conflict (inspector says `web` for every HTML project). Layer: scope.

## Direction verdict (`04-direction.md`, validation OK, budget low)
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | hub-spoke | preserved | yes |
| surface | "elevated" | preserved | preserved on a wrong detection (actual: flat bordered); harmless because nothing was changed |
| typography | humanist-sans | preserved | yes |
| layout | form stack with sections | new | yes (label → value → hint → error → keypad → primary action) |
| density | low, with the kiosk floor note (≥64 px, ≥20 px) | new | yes — the platform-floor clause fixed the Phase 3 platform-invariant defect |
| cards | flat tiles | new | n/a (keys already are flat bordered tiles) |
| color | neutral + one accent | new | matches the existing canvas + brand green; not changed |
| motion | functional minimal | new | yes (unchanged) |
| focus | touch-only focus handling "(mobile)" | new | **partial/wrong emphasis** — the audit needed keyboard focus retention for switch and tactile-keypad users; the record leaves the ring on but says nothing about keeping focus |
| cta | single primary | new | yes (unchanged) |
| imagery | illustration system | new | not used (audit task) |
| icon | filled | new | yes (unchanged) |
| metadata | moderate | new | n/a |

`preservation`: 3 preserved, 0 changed. Unjustified changes: none applied. For an audit the direction step is mostly noise; its value was the density floor clause.

## Audit findings → fixes (files; before-copies in `before/`)
| # | finding (criterion) | fix |
|---|---|---|
| 1 | Every key tap re-rendered the whole screen and dropped focus to `<body>`; keyboard/switch users lost their place after each key (WCAG 2.4.3, 2.1.1) | `render()` records the active control's `data-action/field/key` and re-focuses its replacement (`js/app.js`) |
| 2 | Keypad containers carried `aria-label` on a `<div>` with no role (not exposed) | `role="group"` on both keypads (`js/screens.js`) |
| 3 | No feedback for screen-reader users on what was typed; the value box was a non-focusable `role=textbox` (4.1.3, 2.1.1) | persistent polite live region `#live-polite` announcing "Date of birth so far: 0 4 1 2"; value box `tabindex=0` (`index.html`, `js/app.js`, `js/screens.js`) |
| 4 | Format hint only in the placeholder, gone once typing starts (3.3.2) | persistent `.field__hint` under each field (`dobHint`, `nameHint`, EN/ES), referenced by `aria-describedby` |
| 5 | Error not marked on the field (3.3.1) | `aria-invalid="true"` + error-coloured border while an error is shown (colour plus icon plus text) |
| 6 | Any 8 digits accepted (13/45/1968) — the user only learnt later as "no match" (3.3.1, 3.3.3) | `dobProblem()`: month 1–12, day within month, year 1900–today, not in the future; message `errDobInvalid` |
| 7 | A one-letter name produced "We could not find a match" (wrong recovery guidance, 3.3.3) | `errName`: "Enter at least the first 2 letters of your last name." |
| 8 | 10 px between keys; kiosk floor is ≥16 px | `--key-gap: 16px`, `--key-size` 88→84 so 10 keys + 9 gaps = the 984 px content width (`css/tokens.css`, `css/kiosk.css`) |
| 9 | "-" key announced as "hyphen-minus" | `aria-label="Hyphen"` (`hyphen` string) |
| 10 | Physical/tactile keypad keystrokes were swallowed by the scanner-wedge buffer; Enter/Backspace did nothing (2.1.1; platform: keypad where regulations require) | human-speed keys (>80 ms apart) go to the field, Enter = Continue/Find, Backspace deletes; a scanner burst (<80 ms) stays in the scan buffer and is looked up on Enter; an unknown burst does not leak into the field |
| 11 | Accessible mode: after 4 and 8 the value box sat at y = 701 (< 768 reach zone) | keypad rows at the accessible key size (84 px) in accessible mode; block starts at ≥ 768 |
Idle countdown, privacy wipe (now including the live region), `:focus-visible`-only rings, reduced motion: re-tested, unchanged.

## First-render defects (`render/first-*`, `05-interaction-first.json`: 64/68)
| # | type | defect |
|---|---|---|
| 1 | accessibility / platform | accessible mode: the (now focusable) value box at y = 701, above the 768 px reach line, after the hint line was added |
| — | — | the other three first-run failures were wrong expectations in the test script (typed "5" is shown as "5", not "05"; three Enters give "51 / 11"; the Shift+Tab probe skipped the textbox before recording) — not product defects |

## Final defects (`render/final-*`, `05-interaction-final.json`: 68/68)
| # | type | defect |
|---|---|---|
| 1 | visual (minor) | in accessible mode the invalid-date message wraps to two lines and the alert icon is vertically centred on the block, not on the first line |
| 2 | platform (unverified) | live-region announcements and `aria-describedby` reading not verified with a real screen reader; the 80 ms burst threshold not verified against a real scanner |
| 3 | content | the name hint mentions "the keypad below the screen", which is installation-dependent |

## Iterations
2 renders (first → 1 CSS rule + test corrections → final).

## Interaction test summary (`05-interaction-final.json`, 68 checks, all pass)
Both screens × both modes: every target ≥ 64 px (keys 84×84, pad keys 84×104 / 84×84 in accessible mode), key spacing = 16 px, every key named, keypads `role=group` with a label, value box labelled by a visible label, focusable, described by the visible hint and the alert line (both ids resolve), error line `role=alert`, text ≥ 24 px, contrast ≥ 4.5:1 for all sampled text, nothing clipped (h1 below the top bar, screen bottom 1730/1721 ≤ 1920), accessible mode: all interactive controls at y ≥ 768. Flow: incomplete date → "Enter a complete date…" + `aria-invalid`; 13/45/1968 → "That date is not valid…"; typed digits announced ("0 4 1 2"); one-letter name → "Enter at least the first 2 letters…"; no-match keeps the entered name. Focus: tap keeps focus on the tapped key with no ring; Tab + Enter ×3 keeps focus on the "1" key with a 6 px ring; Shift+Tab reaches the value box. Tactile keypad: "0412196" + Backspace + "68" at 130 ms → "04 / 12 / 1968", Enter → name step, "okafor" → "OKAFOR", Enter → list. Scanner: 8 ms burst "RX-48Q2-7L" + Enter → list; unknown burst leaves the date field empty. Idle (1 s / 1 s) on the identify step: countdown shown, session cleared, no DOB left in the DOM or the live region. Reduced motion: no entry animation.

## Preservation verdict
Hub-and-spoke navigation, tokens (one new `--key-gap`, `--key-size` 88→84), Nunito typography, and the `.field`/`.key`/`.btn` component classes preserved; one CSS rule for the invalid border, one accessible-mode rule; strings added in both languages. Structural additions limited to the hint line and the polite live region, both required by the audit. `preservation-ok`, unjustified structural change 0.

## Regressions to propose
- "accessibility audit of a kiosk keypad and name entry" → bundle covers forms/errors (`a11y-forms-errors`), status announcements (`a11y-live-status`), keyboard/focus, and target size + spacing; requirements input includes keyboard when the project handles `keydown`.
- inspect_project on an HTML project whose README/viewport say kiosk 1080×1920 → platform kiosk (no false AMBIGUOUS conflict); tokens with `--space-N` scale → spacing = 8, not "irregular".
- inspect_project on `html[data-a11y]` / mixed palettes → theme "light + high-contrast mode", surfaces flat-bordered when borders ≥ 2 px and no box-shadow on surfaces.
- knowledge: a record for focus retention across string re-renders (re-focus the equivalent control), and one for on-screen keypads (size, spacing, read-out, hint, delete/clear placement, physical keypad and scanner coexistence).

## Tags
`scope-miss` (false platform conflict → AMBIGUOUS), `requirements-miss` (keyboard input, screen/components), `context-detection-miss` (surfaces, spacing, theme), `ranking-miss` (a11y-forms-errors, a11y-live-status), `knowledge-gap` (focus retention on re-render, on-screen keypad, scanner/keypad input), `direction-mismatch` (focus slot emphasis), `render-defect-fixed`, `render-defect-remaining`, `skill-helped` (kiosk-public-use spacing floor, a11y-labels-names, comp-form label/hint/error layout, anti-no-states), `preservation-ok`.
