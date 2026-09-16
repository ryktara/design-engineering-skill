# p3-kiosk-pharmacy — results

## Task
"Pharmacy prescription pick-up kiosk flow: identify the patient, show ready prescriptions, confirm; public touch screen in the store"

Built from scratch: attract → identify (DOB keypad → last-name keyboard, or scanner keyboard-wedge at any time) → ready list (masked names, price, not-ready row) → confirm summary → done (ticket number, auto-clear countdown). Idle warning dialog with extendable countdown that wipes the session; Help / call staff and an Accessible-mode toggle in a bottom utility bar on every screen; Start over on every non-attract screen; EN/ES strings.

## Stack / platform
Public touch kiosk, portrait 1080×1920. Plain HTML + CSS (cascade layers, custom-property tokens) + vanilla ES modules; no build, no CDN, system font stack. Static fixture `data/prescriptions.json` fetched at lookup time. Project: `project/` (index.html, css/tokens.css, css/kiosk.css, js/app.js, js/screens.js, js/lookup.js, js/i18n.js, js/icons.js, tokens.json).

## Inspection verdict (`01-inspect.json`)
Run on the scaffold (index.html + 2 css + 2 js + README + json). Detected: custom-property tokens with role counts (correct, useful). Missed:
- Stack: reported "no recognised UI stack" although `index.html` + `.css` + `<script type="module">` is the plain html-css stack the skill itself lists. Requirements then reported `stack: MISSING`.
- Platform: `<meta viewport width=1080>` and README text "kiosk", "portrait 1080x1920" gave no platform hint; `platforms: []`.
- Product hints: "pharmacy", "prescription" in README/data gave `product_hints: []`.
- Focus handling: "0 files" was correct for the scaffold. Re-run on the finished project (`rerun-after-skill-edit/01-inspect.json`) it correctly reports focus handling in 2 files, a11y attributes in 5 files, `tokens.json`, and the Nunito font reference — but still no stack, no platform, no product hints, and `i18n: []` although `js/i18n.js` with `en`/`es` string tables exists.
Verdict: tokens/fonts/a11y right; stack/platform/product/i18n missed (`vocabulary-gap`).

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| Field | Value | Verdict |
|---|---|---|
| mode | create (inferred) | right |
| platform | kiosk (KNOWN from "kiosk") | right |
| input | touch (KNOWN) | right |
| product | ecommerce (from "store"), healthcare (from "patient, pharmacy") | healthcare right; **ecommerce wrong** — "in the store" is a location, not a shop product; it later pulled `imagery-hero`, `motion-crossfade`, `color-dominant-brand` via product=ecommerce |
| environment | public (inferred from kiosk) | right |
| jobs / risk | high-risk-action, risk high | right (prescription hand-over) |
| screen / screen_subtype | [] | **missing** — "identify the patient", "show ready prescriptions", "confirm" name three screen types (form/identify, list, confirmation) |
| stack | MISSING | wrong given repo evidence (inspector miss propagated) |
| accessibility | screen_reader, touch_targets, reduced_motion, contrast | right; **missing** large-text / reach-range / timeout-adjustable although kiosk+public implies them |
| negative_constraints | [] | right |
| brand | MISSING | right (none given) |

## Guidance verdict (`03-guidance.md/.json`)
Core:
- `dir-public-kiosk` — **relevant**. The attract → linear spokes → one giant primary, ≥60 px, countdown, cancel-always-visible list is exactly the skeleton built.
- `icon-filled-system` — **relevant** (filled SVG set, always labelled).
- `focus-none-touch-only` — **partially**. The kiosk clause (≥60 px, no hover) is right; the record is titled "(mobile)" and its body talks 44 pt / 48 dp / platform focus visuals; the useful kiosk content is one trailing sentence.
Guardrails:
- `kiosk-public-use` — **relevant** (reach ranges, countdown clears session, one task per screen).
- `states-persistence-and-session` — **partially / conflicting**: "never discard entered data on expiry (restore the draft after re-authentication)" is the opposite of the kiosk privacy requirement; only the "warn before expiry with a way to extend" clause applied. Selected because "states" was a required concern; platform tag is `any`.
- `nav-orientation-and-back` — **partially**: "URL/route reflects state, deep-linkable" is off-target for a kiosk; the step indicator / back-returns-selection part applied.
Ranking misses (in `search -k 12` but not in the guidance bundle):
- `shared-device-privacy` (rank 7, 0.368; platform includes kiosk, product healthcare): mask by default with explicit reveal, announce masked values, clear on idle. This was the most task-specific record in the base and drove the masked names + 10 s reveal; the bundle claimed the privacy concern was covered by `kiosk-public-use`.
- `a11y-target-size` (rank 8): the concrete kiosk ≥60 px rule.
- `a11y-time-and-auto` (found only by a targeted search): "session timeouts, kiosk idle resets" controllable — directly the WCAG 2.2.1 requirement for the idle dialog.
Knowledge gaps (no record found by targeted searches):
- On-screen keypad / keyboard for kiosks (numeric DOB entry, QWERTY, key size, delete/clear placement) — searches returned `comp-form` / `layout-form-stack`.
- Accessible-mode toggle for kiosks (large text + high contrast + relocating controls into the lower reach zone for seated users) — searches returned generic contrast/labels/text-scaling rules; nothing about the layout consequence.
- "Help / call staff" pattern for unattended kiosks.
- Scanner (keyboard-wedge / QR) input handling and its on-screen instruction.
- Confirmation-summary-before-hand-over; `comp-dialog` and `cta-single-primary` came back instead.
Counts: relevant 3, partial 3, off-target 0 (the off-target content sits inside two partial records).

## Direction verdict (`04-direction.md/.json`)
Validation: `ok: true, violations: []`. Slots:
- navigation hub-and-spoke, layout single-column, cards none, cta single-primary, icon filled, focus touch-only — fit and were used.
- density `density-medium` — **platform-invariant**: body text "16 px on web/mobile, 40–48 px interactive heights" contradicts the kiosk guardrail (≥20 px, ≥60 px) selected in the same output; chosen "mode create" only. Used 28 px body / 72–112 px targets from the platform file instead.
- typography `rounded-friendly` — plausible but unbuildable without a font file (no CDN); system stack used; slot reasoning ("product healthcare, kiosk") fine.
- color `dominant-brand`, motion `crossfade`, imagery `hero` — all justified by product=ecommerce (the wrong requirement). Brand field on attract and header was kept because the kiosk direction also asks for it; hero imagery replaced by a single explanatory pictogram; motion reduced to an entry fade + one attract pulse.
- metadata moderate — fit (name → price/status → muted supporting facts, tabular numerals).
Fingerprint is coherent. Nothing in the direction mentions the accessible mode, reach zone layout, or privacy masking; those came from the platform file and the ranking-missed records.

## First-render defects (render/first-*.png)
1. Identify-DOB, identify-name, confirm and done screens captured **blank** in both modes: the whole `.screen` fade-in animation restarted on every re-render (each keypad tap), so the screen flashed from opacity 0 on every key press; screenshots landed inside the 220 ms fade. Real flicker defect, not only a capture artefact.
2. Accessible-mode attract: "Touch to start" had no visible fill (surface token = black on black canvas), only the grey pulse halo marked it.
3. Accessible-mode attract: ambient pulse halo still ran in high-contrast mode (grey ring on black).
4. Standard mode: interactive block (keypad / list / summary) anchored at the top with a ~500 px void before the bottom primary action — long hand travel, weak grouping.
5. Not-ready row's dashed checkbox at 50 % opacity on the light theme falls under 3:1 (non-interactive indicator; text label carries the state).

## Final defects (render/final-*.png)
- (4) is now a void between the intro and the low interactive block on identify/list/confirm/done in standard mode; accepted trade-off for reach, but the middle third of the panel is empty.
- (5) unchanged.
- Typography slot not honoured (system font, no self-hosted rounded face).
- "Done" and "Start over" both reset on the done screen (redundant control).
- Spanish strings and audio tap feedback not visually/aurally verified (headless).

## Iterations
3 renders.
1. `first-*`: baseline as described above.
2. `iter1-*`: entry fade applied only via `.screen--enter` added in `go()` (re-renders no longer animate); a11y attract CTA filled yellow with white border; shooter waits 350 ms for the legitimate entry fade.
3. `final-*`: a11y attract animation override moved into the `motion` layer (the `a11y` layer lost to the later `motion` layer); `.screen__body { margin-top: auto }` so the interactive block clusters low near the primary action in standard mode as well.

## Interaction test summary (`05-interaction.json`; baseline copy `05-interaction-first.json`)
70 checks, 70 pass on both first and final render (the first-render defects were visual/motion, not measurable by these checks).
- Targets: every interactive element ≥ 64 px on all 6 screens × 2 modes (min 72 px standard, 84 px accessible; keys 88/104 px).
- Idle: warning dialog with numeric countdown shown; reset returns to attract, `session === null`, and `body.innerHTML` contains no name/DOB/Rx/prescriber/code strings; "I'm still here" extends the session; Escape does not dismiss the dialog.
- Privacy: names masked by default (`Ator•••••••• 20 mg`, `O••••r`), explicit reveal shows full names (auto re-mask after 10 s); done screen carries no personal data.
- Help action present on every screen (bottom utility bar).
- No `:hover` rules in any stylesheet.
- Focus: tap on a key → no outline; keyboard Tab → 6 px outline (`:focus-visible` only); Tab traverses all controls.
- Contrast: every sampled text element ≥ 4.5:1 in both modes; tokens validated with `tokens.py validate --platform kiosk` (0 errors, 2 warnings: `primary-hover` identical to `primary` — irrelevant on touch).
- Accessible mode: every interactive element has `top ≥ 768 px` (lower 60 %) on all screens, dialogs included.
- Reduced motion: attract pulse `animation-name: none` under `prefers-reduced-motion: reduce`; runs otherwise and stops when the screen changes.
- Scan path: typed `RX-48Q2-7L` + Enter on the identify screen reaches the list.

## Time spent (rough)
~1 h 45 min: scaffold + scripts 15 min, reading skill outputs 15 min, implementation 40 min, render/inspect/fix loop 25 min, write-up 10 min.

## Skill version caveat
While this case ran (00:28–00:39), another process modified 12 files under `design-engineering/` (SKILL.md, data/lexicon.json, data/rules.jsonl, scripts/de_core.py, scripts/validate_skill.py, evals/*, docs/*). This session wrote nothing under the skill directory. The 01–04 outputs above were generated at ~00:30–00:33, partly before those edits. All four scripts were re-run afterwards into `rerun-after-skill-edit/`: requirements byte-identical; guidance and direction select the same records with the same slots (the only change is a new `_(covers: …)_` annotation on guardrail lines); inspect differs only because the project had been implemented in between. The verdicts therefore hold for the post-edit skill.

## Tooling notes
- PROTOCOL step 11 says `tokens.py check`; the CLI has `validate` (used).
- `tokens.py validate` warns about hover state on a kiosk platform (touch-only) — platform-invariant warning.
- `inspect_project.py` counts focus handling as 0 files despite a `:focus-visible` rule in CSS.

## Failure taxonomy tags
`requirements-miss` (product=ecommerce from "store"; stack MISSING with repo evidence; no screen types), `vocabulary-gap` (inspector: plain html-css stack, kiosk viewport/README, pharmacy product), `ranking-miss` (shared-device-privacy, a11y-target-size, a11y-time-and-auto), `knowledge-gap` (on-screen keypad/keyboard, accessible-mode reach layout, help/call staff, scanner input, confirmation summary), `direction-invariant` (density-medium web sizes on kiosk; ecommerce-driven hero/crossfade), `render-defect-fixed` (fade re-trigger, a11y CTA fill, halo, reach clustering), `render-defect-remaining` (mid-panel void, faint disabled box, font slot), `tooling-limit` (check vs validate, hover warning on kiosk), `skill-helped` (dir-public-kiosk + kiosk-public-use + platforms/kiosk.md set the skeleton, sizes, countdown, cancel-everywhere; tokens.py gave every contrast figure quoted; shared-device-privacy shaped masking/reveal).
