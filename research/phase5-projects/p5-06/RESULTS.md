# p5-06 — Waiting room board: patient wait time

**Task (verbatim):** "The waiting room board: nothing tells the front desk how long each patient has been sitting there."
**Project / stack / platform:** `p5-sveltekit-clinic` — ClinicBoard, SvelteKit 2 + Svelte 5 (runes) + Tailwind 3.4, left rail + top header, light only. Platform: web.
**Existing UI or new screen:** existing screen (`/waiting`, 3-column board of white cards on neutral-100 columns). No new screen.
**Build hash:** start `bf034323…f0d8` = end `bf034323…f0d8` (skill untouched).

Note on handover: the previous agent's edits to `sample.ts`, `stores.ts` and `waiting/+page.svelte` HAD applied (verified by diff against `before/`); `first-*.png` (14:49) post-date the last page edit (14:48), so they are kept as the first render. This session added two iterations, the final render, and the deliverables.

## Design-context table (01-inspect.json vs code)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | `+layout.svelte`: `aside w-60` rail + top header; no responsive collapse | yes |
| theme | light-first | INFERRED | light only, no dark tokens, `--cb-*` vars in app.css | yes |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations found") | bordered-flat: `border border-neutral-200` in 9 files, `--cb-border` token, 1 shadow use; every card/column/header/rail is bordered | no (confident wrong evidence; value wrong) |
| radius | unknown | UNKNOWN | `rounded` / `rounded-sm` used in 13 files, consistent 4px/2px | partial |
| spacing | 4 | INFERRED | Tailwind default scale, gap-2/3/4, p-2/3/6 | yes |
| typography | custom; tabular_numerals=false | INFERRED | `Source Sans 3` via theme; `tabular-nums` used in 5 files pre-task | partial (family ok, tabular flag wrong) |
| components | tailwind | KNOWN | Tailwind + 8 local components (Badge, Button, Card, Table…) | yes (local component dir was found under `component_dirs`, not surfaced in design_context) |
| product | healthcare, ecommerce | — | healthcare only; "ecommerce" comes from README wording | partial |

## Requirements verdict (02-requirements.json)

- platform: `web`, `platform_evidence: []` — correct, from project inspection. OK.
- artifact_state: `existing` ("present-tense observation") — correct.
- operations: `diagnose, modify` — acceptable.
- problem_domain: `performance-ux` (evidence: the word "wait") — **wrong**. The problem is missing information on a status board (glanceable status / elapsed time), not perceived performance.
- change_scope: `unknown`; intent.scope `moderate`; change_budget `low` — budget acceptable (the fix is a small addition to one screen plus a data field).
- mode: `audit, refactor` with evidence "perceived-performance defect" — **acceptable by mode set** (refactor ∈ expected), but the evidence is a misreading; the sentence is a request to add a missing element (polish/create on an existing screen).
- scope.kind: **`abstain`**, reason "no UI vocabulary found; not a UI design task as written", activation ui_score 0 / non_ui 0 — **wrong**. "board", "front desk", "waiting room", "patient … sitting there" name a screen, a user, an environment and an operational display problem. Expected in-scope.
- preserve: `[]`; constraints.preserve_existing_system true — acceptable.
- project_context: navigation/theme/spacing/typography/components carried through; surfaces/radius dropped (UNKNOWN).
- environment: `shared-device` from "waiting room" — defensible reading (a board can be a wall display) but here the board is the front-desk operator's screen; harmless.

## Guidance verdict (03-guidance.json/.md)

status `ABSTAIN`. core = [], guardrails = [], concerns required/recommended = [], bundle_tokens = 0. There is no record to grade; relevant 0 / partial 0 / off-target 0. BAD category for the bundle as a whole: **missing-critical** (none of the three critical concepts delivered, no guardrail on colour-only status, nothing on live timers).

Concept recall = 0/7 = **0.0**; critical recall = 0/3 = **0.0**.

| expected id | delivered? | layer if missing |
|---|---|---|
| env.glanceable_status | no | expected-concepts (never demanded; root cause: scope abstain) |
| data.realtime_window | no | expected-concepts |
| a11y.color_not_only | no | expected-concepts |
| table.tabular_figures | no | expected-concepts |
| data.exception_first | no | expected-concepts |
| process.reuse_first | no | expected-concepts |
| perf.layout_shift | no | expected-concepts |

Knowledge-gap check: all seven ids exist in `data/rules.jsonl` / `charts.jsonl` / `components.jsonl` / `antipatterns.jsonl`, so this is not a knowledge gap. `advise.py search` (03b-search.txt) on the same sentence returns `shared-device-privacy` (0.408), `nav-orientation-and-back`, `mobile-gestures-discoverable`, `comp-wizard-stepper`, `nav-wizard`, `grid-single-tab-stop`, … — none about elapsed time, live status, or thresholds; retrieval is driven by `mode audit` + `product healthcare` structural weights, with lexical scores ≤0.37. So even if the scope gate had passed, ranking would likely have missed; but the earliest wrong layer is scope.

Forbidden concepts delivered: none (nothing was delivered).

## Direction verdict (04-direction.json/.md)

Compatibility: 12 slots preserved, 0 changed, 1 new (`focus` → `focus-ring-standard`, "no repository evidence"). Preservation of navigation/layout/density/surface/cards/typography/color/motion/cta is correct and justified for this task. Problems:
- `focus` marked **new / no repository evidence** — wrong: `Button.svelte` and `+layout.svelte` already use `focus-visible:ring-2 focus-visible:ring-primary-500`; inspect reported "explicit focus handling in 3 files". Should be preserved, not new.
- `validation.ok=false`, violation "audit: no accessibility constraints attached" — self-contradictory: `requirements.accessibility` has all six flags true.
- No slot speaks to the actual task (status readout, thresholds, live clock), because direction is slot-based and the concern layer was empty.

## Implementation summary

Files changed (before-copies in `before/`):
- `src/lib/data/sample.ts` — `Appointment.checkedInAt?` / `calledInAt?` (epoch ms); index-based seeding relative to boot time for checked-in (7/23/39 min), in-progress and done rows so the PRNG sequence for patients/visits/invoices is unchanged.
- `src/lib/stores.ts` — `setAppointmentStatus` stamps `checkedInAt` on first check-in, `calledInAt` on in-progress, clears both on scheduled/no-show; "Back" keeps the arrival time so the clock keeps counting from arrival.
- `src/routes/waiting/+page.svelte` — 30 s `$state` clock; per-card wait `Badge` (reused component) with tone neutral/warning/danger at 15/30 min AND a text label ("Waiting" / "Getting long" / "Long wait") so colour is not the sole carrier; `<time datetime>` with a "Checked in at HH:MM" title; digits in `tabular-nums` with a fixed 2ch slot so ticks do not reflow; checked-in column sorted longest-wait first; column header shows "N over 30 min" danger badge; page subtitle shows "longest wait N min" in warning/danger colour; "Waited N min" shown as muted text on in-progress and done cards; `aria-labelledby` on the column sections (was missing). Columns, Call in / Mark done / Back flow, Button variants, header, rail: unchanged.

Guidance used: none was delivered. The direction's "preserve everything, reuse existing" table matched what I would have done anyway (reuse `Badge`/`Button`, keep tokens) — neutral. Ignored: the `focus` "new" slot (already present in the codebase, nothing to add); the `shared-device-privacy` search hit (masking patient names on the front-desk screen would defeat the board). The implementation followed my pre-registered expectation, not the skill.

## Render

Mode: **native** — `npm run build` + `vite preview --port 4173`, Playwright 1.63 Chromium, 1440×900 and 390×844, full-page. Console errors: 0 at both viewports on every render. `svelte-check` reports one pre-existing error in `Table.svelte` (`export type` in a generics script), untouched and unrelated; build passes.

First-render defects:
- **visual (1):** the wait badge used `min-w-[6.5rem]` on the whole label+digits, so it could not shrink and clipped in a narrow column; the column header was fixed `h-11` so the "over 30 min" badge clipped instead of wrapping.
- **existing-system-mismatch (1):** at 390×844 the shell is desktop-only (fixed `w-60` rail, no breakpoints anywhere in `+layout.svelte`); main column is 150px wide; pre-existing content (user menu → 503px, Check-in buttons → 569px, Mark done → 405px) already overflows the viewport. Not introduced by this task.

Iterations: **2**.
1. Header `min-h-11 flex-wrap`; badge row `flex-wrap`; fixed width moved to the digits only (`<time class="tabular-nums inline-block min-w-[3ch] text-right">`).
2. Digit slot 3ch → 2ch (visible gap on "7 min"; only 100+ min waits would grow the slot once).

Final defects: visual 0, interaction 0, accessibility 0, platform 0, **existing-system-mismatch 1** (mobile shell overflow, pre-existing; my badges reach 400–412px vs the shell's 569px), implementation-bug 0. Desktop: no horizontal overflow, three labelled columns, `<time datetime>` present on each checked-in card.

## Preservation verdict

navigation ✓ · theme ✓ (only existing warning/danger/neutral tokens via `Badge` tones) · typography ✓ (existing sizes; `tabular-nums` already a project convention) · component_reuse ✓ (`Badge`, `Button`) · unjustified structural change 0. Routes, ids, store API shape (added optional fields only) intact. Verdict: **preservation-ok**.

## Skill misses by earliest wrong layer

1. **scope** — abstain on an in-scope UI sentence ("board", "front desk", "waiting room"); ui_score 0. Everything downstream empty.
2. **context-detection** — surfaces UNKNOWN/flat-tonal with the false evidence "no border declarations found" on a fully bordered Tailwind codebase; radius UNKNOWN despite consistent `rounded`; `tabular_numerals=false` despite 5 files using `tabular-nums`; "ecommerce" product from README.
3. **requirements** — problem_domain `performance-ux` from the token "wait"; mode evidence "perceived-performance defect".
4. **direction** — `focus` slot "new / no repository evidence" contradicts the codebase; validation violation contradicts the requirements' own accessibility flags.

Skill effect: **neutral** (no guidance; the preserve-everything direction was harmless and matched the obvious approach). Not "hurt": nothing it said was followed to a bad outcome.

## Regressions to propose

- Query: the task sentence verbatim. Expect: `scope.kind=in-scope`; mode polish/refactor; `env.glanceable_status`, `data.realtime_window`, `a11y.color_not_only` in delivered concepts; `problem_domain` not `performance-ux`.
- Query: "Nothing on the kanban board shows how long a card has been sitting in a column." Expect: in-scope; delivers `env.glanceable_status`, `data.realtime_window`, `table.tabular_figures`, `perf.layout_shift`.
- Inspect: Tailwind codebase with `border border-neutral-200` and `rounded` on every surface and `tabular-nums` in several files. Expect: surfaces = bordered-flat (not UNKNOWN), radius detected, `tabular_numerals=true`.
- Direction: project with `focus-visible:ring-*` in components. Expect: focus slot **preserved**, not "new / no repository evidence".

## Tags

`scope-miss`, `requirements-miss`, `concept-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `skill-neutral`, `preservation-ok`
