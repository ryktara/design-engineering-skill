# p6-02 — "Add a usage page showing this month's API calls against the plan quota."

- **Project / stack / platform:** `research/phase3-projects/p3-nextjs-saas/project` — Next.js 15 App Router, React 19, Tailwind v4, shadcn-style components (zinc / new-york), Radix, lucide. Platform: web.
- **Existing UI or new screen:** new screen (`/settings/usage`) inside an existing settings shell with an existing tab nav.
- **Build hash:** start `ea8eed72…d9947`, end `ea8eed72…d9947` — identical, nothing under `design-engineering/` was touched.

## 1. Design context (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | `app-shell.tsx` left rail (`PrimaryNav`) + a secondary tab bar in `settings/layout.tsx` (`SettingsNav`) | partial — the rail is right; the settings tab strip, which this task has to extend, is not reported |
| theme | dual-theme, default light | KNOWN | `:root` light + `.dark` block in `globals.css`, light default | yes |
| surfaces | bordered-flat (INFERRED) | INFERRED | borders everywhere, but the dominant surface is `Card` = `rounded-lg border bg-card shadow-sm` | partial — "flat" understates the shadowed rounded card that every screen uses |
| radius | small (INFERRED) | INFERRED | `--radius: 0.5rem`, `rounded-lg`/`rounded-md`/`rounded-full` | yes |
| spacing | 8 (INFERRED) | INFERRED | Tailwind 4px scale, sections on `space-y-8`, cards `p-6` | yes |
| typography | custom (KNOWN), evidence "font family Var (2 refs)", mono, tabular | KNOWN | Geist + Geist_Mono via `next/font/google`, `tabular-nums` used in billing | partial — features right, the family names were not recovered ("Var" is the `--font-…` variable, not a font) |
| components | tailwind, radix, shadcn-style cva, table:tanstack, shadcn | KNOWN | exactly that (tanstack is a dependency but unused in these screens) | yes |

## 2. Requirements verdict (`02-requirements.json`)

- **platform_evidence:** empty list, but `platform=["web"]` assigned from project inspection — correct, no MISSING confirm needed.
- **artifact_state:** `existing`; I pre-registered `new`. Definitional mismatch rather than a behavioural defect: the axis is the codebase (which exists), and `intent.operations=["create"]` plus `mode_evidence` "build/create request on an existing surface" carry the new-screen part. Recorded as incorrect in artifacts.json for honesty.
- **operations:** `["create"]` — correct. **problem_domain:** `[]` — correct (no defect stated). **change_scope:** `screen` — correct.
- **mode:** `["create"]` with evidence — correct, and the sentence does carry a mode word ("Add").
- **scope.kind:** `in-scope` ("UI design / interaction task") — correct; note `activation.decision` is `ambiguous` (ui 1.0 vs non_ui 1 because of "api call"), which did not harm the outcome here but is thin for a sentence that literally asks for a page.
- **change_budget:** `moderate` — right for a new page in a preserved shell.
- **intent.preserve:** `[]`, but `constraints.preserve_existing_system: true` — acceptable.
- **project_context:** carried through in full.
- **screen / screen_subtype:** both empty. A "usage page" is a recognisable screen type (metering / KPI screen); the empty `screen` is what later made every component record fail the "positive task evidence" gate (see §3).

## 3. Guidance verdict (`03-guidance.md` / `.json`)

`status=PARTIAL`, bundle = 4 records (core 2 + guardrails 2), 446 tokens, soft cap 6. Optional layer empty.

| record | layer | verdict | category | note |
|---|---|---|---|---|
| `chart-progress-gauge` | core | relevant | — | DIRECT carrier of `data.kpi_comparison`. Drove the whole quota meter: measure bar + target tick + value and target labelled numerically. |
| `chart-compare-bar` | core | partial | generic | Zero marginal contribution (`new_critical/required/recommended/concerns` all empty). Its rules (zero-based, single colour, sorted by value, no rounded ends) were usable for the by-key bars; "sorted by value" is wrong for the daily time series, where order is meaningful. |
| `impl-reuse-before-new` | critical guardrail | relevant | — | GENERIC but correct and acted on. SKILL.md §2 says the same thing (see process check). |
| `typo-scale-and-roles` | critical guardrail | partial | generic | Only "numeric role uses tabular lining figures" applied. The rest is a build-a-type-scale record aimed at a slot the direction itself marked **preserved**; following it literally would have restyled the shadcn type system. |
| *(bundle)* | — | — | missing-critical | `state.loading_empty_error` and `navigation.orientation_and_back` absent — see the recall table. |

**Concept recall** (delivered = union of `concepts` over the 4 selected records = `data.chart_by_question`, `data.kpi_comparison`, `process.reuse_first`, `table.tabular_figures`, `brand.type_roles`):

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| data.kpi_comparison (critical) | yes (DIRECT) | — |
| navigation.orientation_and_back (critical) | no | expected-concepts — never demanded; "navigation" appeared only as a *recommended* concern and was reported "not surfaced" |
| state.loading_empty_error (critical) | no | criticality — demanded only as `recommended` although `states` is a required concern and every settings route in this codebase ships `loading.tsx` + `error.tsx`; it then lost bundle selection (candidates `layout-states-empty-loading-error`, `anti-no-states`, `comp-chart-container` all existed) |
| a11y.semantics | no | expected-concepts — `accessibility` was a required concern but no a11y concept beyond the three interaction ones was demanded |
| table.tabular_figures (critical per skill) | yes (GENERIC) | — |
| data.refresh_timestamp | no | expected-concepts — never demanded, although "this month's" is a period-bounded counter |
| process.reuse_first | yes (GENERIC) | — |

Recall 3/7 = **0.43**; critical recall 1/3 = **0.33** (the skill's own critical set was different — it reports `critical_coverage_ratio: 1.0` for `data.kpi_comparison` / `process.reuse_first` / `table.tabular_figures`).

Two further ranking observations, both visible in the JSON:
- `comp-kpi-tile` scored **0.511**, the top candidate for *both* `data.kpi_comparison` and `table.tabular_figures`, and was omitted for "no positive task evidence (screen / subtype / component / job / product / wording) for a core record" on a sentence that asks for a page "showing this month's API calls against the plan quota". Same for `comp-settings-screen` and `layout-states-empty-loading-error`.
- The bundle stopped at 4 of a soft cap of 6 while three required concerns (states, interaction, accessibility) were uncovered.

`PARTIAL_SCOPE` was not the status here (status is `PARTIAL` for concept coverage), so no design/engineering split note to judge.

**Process guidance check:** `process_records_needed = false`. `impl-reuse-before-new` restated SKILL.md §2, and I ran the render/inspect loop from §7 regardless — the bundle would have been more useful spending those 131 tokens on a states or navigation record.

## 4. Direction verdict (`04-direction.md/json`)

All 13 slots `preserved`, 0 `changed`, 0 `new` → **`unjustified_direction_slots: 0`**, which is the expected number for a moderate-budget addition to an existing UI. `preservation` metrics and `Validation: OK` agree. Two notes:

- The per-slot texts still print the from-scratch advice ("Fixed-width rail (collapsible to icons…)", "no rounded card containers inside panes", "Neutral scale with a slight brand tint… validate with tokens.py") before the "(Existing system: do not replace it for this task.)" suffix. Noise, not harm.
- The fingerprint says `card_geometry: "none"`, `corner_language: "sharp"` for a codebase built entirely out of `rounded-lg` shadow cards. Wrong, and only harmless because the slots are preserved — a `changed` budget would have made this a restyle instruction. Layer: `project-context`.

## 5. Implementation

New files (all in the project's own conventions, no new dependency, no client component):

- `lib/usage.ts` — quota per plan, a Sep 2026 period fixture (15 of 30 days elapsed), daily calls, per-key calls, `Intl`-based formatters, mirroring `lib/billing.ts` exactly.
- `app/settings/usage/page.tsx` — period header with "Day 15 of 30" + "Updated Sep 15, 1:40 PM", four stat cards in the dashboard/billing `dl` + `Card` idiom (calls this month, included in plan, remaining, projected), the quota meter, a projection warning strip, "Daily volume", "Calls by key".
- `app/settings/usage/loading.tsx`, `app/settings/usage/error.tsx` — skeleton and `role="alert"` recovery copy matching the billing and api-keys routes.
- `components/usage/quota-meter.tsx` — `role="meter"` with `aria-valuetext`, value + whole labelled numerically, projection tick, `bg-warning` at ≥90% and `bg-destructive` at ≥100% with the same text always present (colour never the only cue) — the seat-meter pattern already in `seat-table.tsx`.
- `components/usage/daily-usage-chart.tsx` — zero-based chronological column chart (`aria-hidden`) inside a `figure`, a `figcaption` stating range and peak, and a `<details>` table of the same numbers as the accessible alternative. Empty state for a period with no calls.
- `components/usage/usage-by-key.tsx` — real `Table`, bars sorted by value, single colour, share % and tabular call counts; empty state.

Changed file (copied to `before/`): `components/settings-nav.tsx` — one item, `Usage`, added after `Billing`. The API-keys tab added by another task was not touched.

`npx tsc --noEmit` clean; `npm run build` clean (`/settings/usage` 172 B, 105 kB first load — server-rendered, no recharts pulled in).

**Guidance used:** `chart-progress-gauge` (the meter's form: bar + target tick + numeric value and whole), `chart-compare-bar` (by-key bars: zero-based, one colour, sorted by value, square ends), `impl-reuse-before-new` (Card/Table/Badge/Skeleton/Button reuse, new files placed where their siblings live).
**Guidance ignored:** `typo-scale-and-roles` beyond the tabular-figures clause — the typography slot is preserved and the project already has a scale.
**Not in the bundle but needed:** the nav entry, the `loading.tsx`/`error.tsx` pair, the empty states, the `role="meter"` semantics and the chart's accessible alternative all came from reading the codebase, not from the guidance.

## 6. Render and defects

Render mode: **html** — Playwright 1.63.0 / Chromium against the production build on `http://localhost:3111/settings/usage`, 1280×800 and 390×844, plus a desktop shot with the daily table open. Screenshots inspected.

**First render defects (2):**
1. `visual` — the daily-volume columns were invisible: percentage heights on bars inside `li` elements with no resolved height collapsed to 0, leaving an empty 128 px box (`first-desktop.png`, `first-mobile.png`).
2. `implementation-bug` — the per-key fixture summed to 108,100 while the daily series summed to 108,310, so the "share of calls" column did not reconcile with the headline number.

Neither was warned about by the guidance.

**Fixes:** `li` given `flex h-full items-end` and the bar `w-full`; `key_01` set to 93,520 so the per-key total equals the daily total exactly.

**Final defects: 0** across visual / interaction / accessibility / platform / existing-system-mismatch / implementation-bug. **Iterations: 1.** (The four 404s in the console are the prebuilt app's missing favicon/invoice PDF assets, present on the untouched routes too.)

## 7. Preservation

Left rail, settings tab strip, theme tokens, Geist typography, `Card`/`Table`/`Button`/`Badge`/`Skeleton` primitives, 8px spacing rhythm, focus-ring convention and the per-route loading/error convention are all unchanged; the single edit to an existing file is one nav item. `unjustified_structural_change: 0` → **preservation-ok**.

## 8. Regressions to propose

1. *"Add a usage page showing this month's API calls against the plan quota."* → `navigation.orientation_and_back` must be demanded whenever mode=create adds a screen and the project context reports an existing navigation: a new route that is not placed in the nav is unreachable.
2. Same query → `state.loading_empty_error` must be **required**, not recommended, when `states` is a required concern and the repository already has per-route loading/error files; a states record must reach the bundle.
3. Same query → `comp-kpi-tile` must survive the "positive task evidence" gate: "quota", "this month" and a counted metric are KPI-screen evidence.
4. Same query → the bundle must keep filling toward the soft cap while required concerns (states, interaction, accessibility) are still uncovered instead of stopping at 4 records.

## 9. Skill effect

**helped.** `chart-progress-gauge` is a DIRECT carrier and changed the artefact: without it I would plausibly have shipped a bare percentage bar, not a bullet-style meter that labels value and whole numerically and marks the projected end-of-month total against the quota. Against that, half the bundle (`chart-compare-bar`, `typo-scale-and-roles`) added little, and the three things this page most needed from a skill on a *new* screen — put it in the nav, ship its loading/empty/error states, keep its semantics accessible — were all absent.

**Tags:** `concept-miss`, `ranking-miss`, `context-detection-miss`, `render-defect-fixed`, `skill-helped`, `preservation-ok`.
