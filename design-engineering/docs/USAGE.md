# Usage examples

The skill activates automatically for UI/UX requests; `/design-engineering <request>` forces it. Commands below are what Claude runs under the hood; you can run them yourself.

## Requirements contract (what every other step consumes)

```bash
python scripts/inspect_project.py . --out .design-inspect.json
python scripts/advise.py requirements "Build an Android TV EPG in Compose." --project .design-inspect.json --pretty --explain
```
Prints the `design-requirements/v1` object: modes, platforms, inputs, product, screen, stack, density, constraints, accessibility flags, negative constraints, and the KNOWN / INFERRED / MISSING ledger with reasons (e.g. `platform=tv (request: android tv)`, `input=remote (implied by platform tv)`, `stack=compose-tv (Compose on a TV platform uses androidx.tv)`, `missing: brand`). Exit code 0 CONFIDENT, 3 PARTIAL, 4 AMBIGUOUS, 5 ABSTAIN. Pass the same project file to `search` and `direction`.

## Guidance bundle (the retrieval every task uses)

```bash
python scripts/advise.py guidance "Fire TV live guide with 300 channels" --project .design-inspect.json --explain
```
Derives the task's concerns (REQUIRED / RECOMMENDED / OPTIONAL with reasons) and the concept ids the context demands (e.g. `tv.epg_pinned_channels`, `interaction.dpad_reachability`, `tv.ten_foot_typography`), then prints three layers (Phase 6): **CORE** (what to build: `comp-epg`, `layout-epg-grid`, the TV direction), **CRITICAL GUARDRAILS** (rules/anti-patterns that must hold, each with `covers: …` labels and its coverage quality DIRECT / SPECIFIC / GENERIC) and **OPTIONAL NOTES** (recommended coverage; omitted when empty), plus `metrics`: covered/uncovered required and critical concepts, concept coverage, bundle size (1–8, no minimum: an empty layer is better than a generic record), diversity, redundancy. `status` is CONFIDENT only when every required concern is covered and the platform is known. `--size N` overrides the cap; `search` remains the raw ranked list for debugging.

Problem statements are handled as work on existing UI: "users keep missing the save button on the web invoice editor" → modes `audit, refactor`; "the spacing looks cramped and inconsistent" → `polish, audit`; "Build a new settings page; the current one is confusing" → `create` (explicit build verb wins) with audit as secondary.

Environment and jobs only count with evidence: "inspectors working in bright sunlight with gloves" → environment `outdoor, gloves` → `mobile-field-use` guardrail; "approve a wire transfer" → risk `high` → confirmation guardrail. "SaaS" or "Android" alone give an INFERRED platform plus a MISSING entry asking to confirm.

## Scope, mode evidence, change budget (Phase 4)

```bash
python scripts/advise.py requirements "Users keep losing focus after closing the dialog." --pretty --explain
```
→ `scope.domain=UI_INTERACTION`, `mode=[audit, refactor]`, `mode_evidence=["audit: interaction problem on existing UI", "refactor: fix follows the diagnosis"]`, `change_budget=moderate`. "Why is my React component re-rendering?" → `scope.in_scope=false`, exit 5, with the reason and the nearest supported UI task. "Review this screen but don't change code" → `review, audit`, `preserve=[behaviour]`, budget `low`.

## Codebase-aware direction (Phase 4)

```bash
python scripts/inspect_project.py . --out .design-inspect.json      # now includes design_context
python scripts/advise.py direction "polish the billing settings page" --project .design-inspect.json
```
With a left-rail, light-first, Geist-based admin detected, the direction's compatibility table reads `navigation: preserved (repository evidence with change budget 'low')`, `color: preserved`, `typography: preserved`, and only layout-level slots may change. "redesign the billing page navigation from scratch" lifts the budget to `high`; changed slots are listed with their reason.

## Platform evidence, task semantics, partial scope (Phase 5)

```bash
python scripts/advise.py requirements "the rail flies past when you hold right on the remote" --pretty
```
gives `platform=[tv]` with `platform_evidence.candidates=[{platform: tv, strength: STRONG_INFERENCE, evidence: [remote, hold right]}]`; "the media browser" is not a web browser; "a settings screen for the app" stays UNKNOWN with `missing: [platform: target platform/form factor needs confirmation]` rather than guessing. `intent` now carries `artifact_state` (new / existing / unknown), `operations`, `problem_domain`, `change_scope` and `utterance`; "The invoices table is hard to scan once there are more than twenty rows." is existing UI, operations `diagnose, modify`, modes `audit, refactor`, and never `create`.

"The appointments grid re-renders the whole day when one chip is dragged, so dragging stutters." gives `scope.kind=partial` and status `PARTIAL_SCOPE` with a note naming the design half (drag affordance, drop feedback, keyboard alternative, announcement) and the engineering half (keyed updates, one write on drop). With a repository supplied, a sentence such as "Dispatchers want to see which vehicles are overdue for service without opening each one." is in scope even though it names no UI component.

`--explain` on `guidance` ends with a **concept trace**: every required concept, covered or UNCOVERED, marked CRITICAL where it is one, with the carrier quality of the selected record, the earliest wrong layer and the candidate records, so a miss can be routed to expected-concepts, retrieval, selection or a knowledge gap without guessing. `marginal` (JSON) lists, per selected record, the new critical / required / recommended concepts it added, its evidence flags, quality and contamination; `omitted` and `not_surfaced` explain what stayed out.

`inspect_project.py` reads README platform and environment declarations (a "public touch kiosk" is a kiosk whose substrate is web; "outdoors, gloves" become environment evidence) and native design tokens (Avalonia / WPF resource dictionaries, SwiftUI `Font.system`, Tailwind classes in Svelte / Vue templates).

## Create (existing project)

"Add an invoices screen to this app: list, filters, and a detail panel."
Claude: inspects the repo → detects Next.js + shadcn + Tailwind → `advise.py guidance …` then `advise.py direction "invoices list with filters and detail panel" --project .design-inspect.json` → reuses the DataTable recipe and Sheet → implements → renders at the project breakpoints → Tab pass → reports the ledger.

## Audit

"Audit the checkout flow for UX and accessibility problems."
→ review-rubric + accessibility references, `tokens.py contrast` on suspicious pairs, keyboard walk, findings ranked by impact with evidence.

## Refactor / polish

"The settings page looks unprofessional and generic. Fix it without changing behaviour."
→ anti-generic self-check, spacing scale, one focal element, no nested cards; routes/state/test ids untouched; before/after screenshots.

## TV

"Make the home screen of our Android TV app DPAD friendly and add a Continue Watching rail."
→ `platforms/tv.md` + `stacks/compose-tv.md`; focusRestorer on rails, deterministic initial focus, 48/27 dp safe margins, landscape cards with progress; verified with `adb shell input keyevent` walks and screenshots.

```bash
python scripts/advise.py search "continue watching rail android tv" -k 4
python scripts/tokens.py validate tokens.json --platform tv
```

## Mobile

"Design the transaction history screen for our iOS banking app."
→ hub-and-spoke / list rows, Dynamic Type styles, safe areas, swipe actions with menu equivalents; Simulator screenshots at small and large sizes and AX text.

## Desktop

"Build a purchase-order entry window in WinUI 3 with keyboard-first data entry."
→ `platforms/desktop.md` + `stacks/winui.md`; NavigationView shell, CommandBar accelerators, Toolkit DataGrid with Enter/Tab movement and validation, 4 epx grid; verified at 800×600 and maximised, 150% DPI, Narrator.

## Multi-brand

"We run four IPTV brands on one backend. Make them genuinely distinct, not just recoloured."
```bash
python scripts/advise.py direction "<brand A signals>" --brand A --out brand-a.json
python scripts/advise.py direction "<brand B signals>" --brand B --out brand-b.json
python scripts/fingerprint.py compare brand-a.json brand-b.json brand-c.json brand-d.json
```
COSMETIC-ONLY pairs fail; change ≥2 structural axes and re-compare; implement as configurations of one component system.

## Accessibility

"Check keyboard accessibility of the admin dashboard."
→ keyboard operability, focus visibility/obscuring, roving tabindex in composites, dialog focus management; measured contrast; report with WCAG criteria.

## Screenshot reconstruction

"Implement this screenshot in React." (image attached)
→ `references/screenshot-reconstruction.md`: hierarchy, spacing snapped to scale, type roles, colour roles measured, fingerprint, mapped to existing components; rendered side by side at the inferred viewport.

## Design system

"Create a design token set with light and dark themes for our Vue app."
```bash
python scripts/tokens.py init > tokens.json      # edit values
python scripts/tokens.py validate tokens.json
python scripts/tokens.py scale --platform web --base 16 --ratio 1.25
```
→ tokens wired into the project's CSS variables/theme, both themes validated.

## Charts

"Which chart for revenue by region over the last 12 months?"
→ `advise.py search "revenue by region over time" --kind chart` → small multiples or a line chart with direct labels; accessible table alternative.
