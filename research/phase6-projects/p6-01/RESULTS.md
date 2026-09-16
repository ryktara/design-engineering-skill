# p6-01 — "Nobody can find the API keys section; it is buried at the bottom of the settings page."

- **Project / stack / platform:** `research/phase3-projects/p3-nextjs-saas/project` — Next.js 15.3 app router, React 19, Tailwind v4, shadcn (new-york/zinc), Geist; web.
- **Existing UI:** yes (settings area with a tab strip: General / Members / Billing / Security; only `/settings/billing` and `/settings/members` exist).
- **Premise note (pre-registered before any advise run):** the codebase contains **no** API keys section anywhere. The sentence was run verbatim; the fix was realised as the findability outcome the sentence asks for — API keys gets its own named entry in the settings sub-nav and its own deep-linkable route, built from the project's own primitives.
- **Build hash:** start `ea8eed72…d9947`, end identical (see `00-build-hash-*.txt`).

## 1. Design-context table (`01-inspect.json`)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | left rail (`app-shell.tsx`, hidden `<md`) + top header + settings tab strip (`settings-nav.tsx`) | partial — the rail is right, the **settings sub-nav tab strip** (the structure this task is about) is not detected at all |
| theme | dual-theme, default light | KNOWN | `:root` light, `.dark` opt-in in `globals.css` | yes |
| surfaces | bordered-flat | INFERRED | borders everywhere, `shadow-sm` only on Card | yes |
| radius | small (0.5) | INFERRED | `--radius: 0.5rem` | yes |
| spacing | 8 | INFERRED | Tailwind 4/8/12/16/24 | yes |
| typography | custom | KNOWN | Geist Sans + Geist Mono via `next/font`, tabular numerals | yes |
| components | tailwind, radix, shadcn cva, tanstack, shadcn | KNOWN | `components/ui/*` shadcn primitives, Radix dialog/slot, tanstack in deps | yes |

Detection miss: no notion of *secondary / in-page navigation*. For an information-architecture task that is the one field that mattered.

## 2. Requirements verdict (`02-requirements.json`)

| field | resolved | verdict |
|---|---|---|
| platform | `web` (project inspection), `platform_evidence: []` | correct |
| artifact_state | `existing` | correct |
| operations | `diagnose`, `modify` | correct |
| problem_domain | `navigation`, `layout` | correct |
| change_scope | `screen` | correct |
| mode | `audit`, `refactor` (evidence: "navigation defect on existing UI" / "fix follows the diagnosis") | acceptable — pre-registered `refactor`/`polish`; `audit` is defensible for a reported defect, `refactor` is present |
| scope.kind | `in-scope` ("UI design / interaction task") | correct. Note `scope_evidence.technical.BACKEND: ["api", "api keys"]` — the phrase "API keys" registered as a backend signal but did not flip the verdict |
| change_budget | `moderate` | acceptable, slightly generous — this is a low-budget IA fix; nothing downstream abused it (direction changed 0 slots) |
| intent.preserve | `[]` | miss — `constraints.preserve_existing_system: true` carries it, but the explicit preserve list is empty |
| project_context | echoed in full | correct |
| status | CONFIDENT, `missing: []` | fine |

## 3. Guidance verdict (`03-guidance.md` / `.json`) — status PARTIAL, bundle 4 (core 2 + guardrails 2), ~683 tokens

| record | layer | verdict | category |
|---|---|---|---|
| `comp-settings-screen` | core | relevant — "never bury frequently changed settings three levels deep", grouped rows, platform idiom: this is the task | — |
| `comp-plan-comparison` | core | partial | `wrong-screen` — billing/plan guidance (plan radio cards, seat table, invoice download, tabular prices). One clause ("settings sub-navigation … with aria-current") applied; the rest is another page. Selected on a *critical* concept `table.tabular_figures` that this task never needed |
| `layout-states-empty-loading-error` | guardrail | partial | `generic` — true, and the project already ships `loading.tsx`/`error.tsx` per route, which is where I got the pattern |
| `typo-scale-and-roles` | guardrail | off-target | `generic` — a full type-scale rule on a screen whose typography the same run marks **preserved**; entered only as the "specialist" carrier for tabular figures |
| bundle | — | — | `missing-critical` — pre-registered critical `process.reuse_first` absent, and `privacy.sensitive_masking` (masking API key values) was never even demanded on a page whose whole content is secrets |

Layer review: core `[comp-settings-screen, comp-plan-comparison]`, critical `[layout-states-empty-loading-error, typo-scale-and-roles]`, optional layer empty (0 useful / 0 noise).
Platform filtering worked: 6 mobile/TV/kiosk records filtered out, 0 contaminated records in the bundle.

**Concept recall** (delivered = union of `concepts` over the 4 selected records):

| expected id | delivered? | earliest wrong layer |
|---|---|---|
| `layout.settings_grouping` (critical) | yes (`comp-settings-screen`, DIRECT) | — |
| `process.reuse_first` (critical) | no | `bundle-selection` — demanded as *recommended*, candidate `impl-reuse-before-new` existed, dropped ("no sufficiently specific guidance") |
| `navigation.rail_semantics` | no | `expected-concepts` — never demanded (carrier `comp-sidebar-nav` exists) |
| `navigation.deep_link_state` | no | `expected-concepts` — never demanded (carriers `comp-tabs`, `nav-orientation-and-back` exist) |
| `layout.focal_hierarchy` | no | `expected-concepts` — never demanded (carrier `layout-hierarchy-one-thing` exists) |
| `privacy.sensitive_masking` | no | `expected-concepts` — never demanded. Carriers exist (`shared-device-privacy`, `comp-kiosk-keypad`) but are kiosk/shared-device framed, so a web secrets page has weak coverage even if demanded |
| `process.safe_modification` | no | `expected-concepts` — never demanded (carrier `impl-safe-modification` exists) |

Recall **1/7 = 0.14**; critical recall **1/2 = 0.50**. The skill's own metrics report `critical_coverage_ratio: 1.0` against *its* criticals (`layout.settings_grouping`, `table.tabular_figures`) — the second of those is an artefact of `comp-plan-comparison` being pulled in, i.e. the run marks as critical a concept the task did not need. No knowledge gap: every expected concept has a carrier record in the base.

Three *required* concepts the run demanded were also left uncovered by the cap (`interaction.keyboard_navigation`, `interaction.hover_independence`, `interaction.focus_visible`) while a type-scale record occupied a guardrail slot — a ranking problem, not a knowledge problem.

**Process guidance check:** SKILL.md §2/§7 was **not** enough. My first render's worst defect was exactly a reuse failure — I invented a responsive table treatment instead of copying `members-table.tsx`'s column-folding convention. `impl-reuse-before-new` in the bundle would plausibly have prevented it. `process_records_needed: true`.

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`; `changed: []`; fingerprint `left-rail / bordered / sharp / neutral-plus-accent` matches the codebase; validation OK. **`unjustified_direction_slots: 0`** — the correct answer for an existing UI with this task. Slot prose is generic boilerplate ("Keep the current X; inspect and reuse it") but it is harmless and the navigation slot correctly says *do not replace the rail*.

## 5. Implementation

Files (backups of modified files in `before/`):

- `components/settings-nav.tsx` *(modified — backed up)* — added `{ href: "/settings/api-keys", label: "API keys" }` between Billing and Security. Existing `aria-current="page"`, focus ring and active underline apply unchanged.
- `lib/api-keys.ts` *(new)* — data module in the shape of `lib/billing.ts`/`lib/members.ts`; keeps `prefix`/`last4` separate from `secret` and exports `maskKey()`.
- `components/api-keys/api-keys-table.tsx` *(new)* — reuses `ui/table`, `ui/button` and `billing/status-badge`; `<th scope="col">`, status as badge **and** label (never colour alone), shared `formatDate`, `tabular-nums`, masked values with a per-row reveal toggle (`aria-pressed`, sr-only label that names the key), one row revealed at a time.
- `app/settings/api-keys/page.tsx`, `loading.tsx`, `error.tsx` *(new)* — same server-component + skeleton + `role="alert"` retry trio as `/settings/billing`, with page `metadata.title`.

Guidance **used**: `comp-settings-screen` (don't bury it; grouped rows, labels with visible current values, platform idiom = sections in the settings pane); the `aria-current` sub-nav clause from `comp-plan-comparison`; `layout-states-empty-loading-error` (loading/error routes).
Guidance **ignored**: `typo-scale-and-roles` (typography is a preserved slot; generating a new scale would be a regression) and the plan-card / seat-table / invoice-download body of `comp-plan-comparison` (different screen).

`npx next build` passes; `/settings/api-keys` prerenders as static.

## 6. Render

Playwright 1.63.0 against `next start -p 3111` (production build), Chromium, 1280×800 and 390×844, screenshots looked at.
`render/first-desktop.png`, `first-desktop-revealed.png`, `first-mobile.png`, `first-billing-nav.png`; `render/final-*.png` likewise.

First-render defects (4):

| type | defect |
|---|---|
| visual | Revealing a key re-flowed the whole table — every column to the right jumped. |
| existing-system-mismatch | At 390 px the Access / Created / Last used / Status columns were pushed off the table's scroll edge; the project's own `members-table.tsx` folds secondary columns under the name below `md`/`lg` instead. |
| accessibility | `aria-live="polite"` on the key text — revealing would read the full secret out loud; the toggle's `aria-pressed` + sr-only label already announce the state. |
| accessibility | Reveal toggle was 32 px high on touch viewports (project convention is `size-11` below `sm`). |

Fixes (2 iterations): reserved the revealed width (`md:min-w-[19.5rem]`) so columns stay put; folded Access/Status under the name below `md` and Created below `lg`; dropped `aria-live`; `max-sm:size-11` on the toggle.
**Final defects: 0** in all six categories. Remaining console 404s for static assets appear on the unchanged `/settings/billing` route as well — pre-existing, not introduced here.

## 7. Preservation

Rail, header, tab-strip pattern, theme, Geist typography, shadcn primitives, existing routes and the billing page all unchanged (`final-billing-nav.png`). No structural change beyond one nav entry and one new route. `preservation-ok`.

## 8. Skill effect

**neutral.** The one thing the bundle got right (`comp-settings-screen` → don't bury settings, group them with visible values) matched the fix I would have made from the codebase alone; nothing in the bundle covered the two things this page actually turns on — *reuse the existing settings-nav/table conventions* and *mask secret values* — and one guardrail (type scale) contradicted the run's own preserved-typography direction. No record caused a change I reverted, so not `hurt`.

## 9. Misses by earliest wrong layer

1. `expected-concepts` — `privacy.sensitive_masking` never demanded for a page about API keys (screen=settings, product=saas, the word "keys" in the query).
2. `expected-concepts` — `navigation.deep_link_state` / `navigation.rail_semantics` / `layout.focal_hierarchy` never demanded for a findability task whose `problem_domain` the run itself set to `navigation, layout`.
3. `bundle-selection` — `process.reuse_first` demanded, candidate present, dropped; the miss it enabled (mobile column convention) cost an iteration.
4. `criticality` — `table.tabular_figures` promoted to critical, pulling `comp-plan-comparison` (wrong screen) into core and `typo-scale-and-roles` into the guardrails, while three demanded interaction/a11y concepts were cut by the cap.
5. `project-context` — `inspect_project.py` reports only top-level navigation; the settings sub-nav (the object of the task) is invisible to it.
6. `requirements` — `intent.preserve` empty.

## 10. Regressions to propose

| query | expectation |
|---|---|
| "Nobody can find the API keys section; it is buried at the bottom of the settings page." | bundle carries `layout.settings_grouping` **and** `process.reuse_first`; does **not** carry `comp-plan-comparison` |
| "Show the workspace's API keys on the settings page." | `privacy.sensitive_masking` is demanded and delivered by a web-framed record (masked value + explicit reveal) |
| any existing-UI web task with `problem_domain=navigation` | `navigation.deep_link_state` demanded (route/URL reflects the section) |
| settings/IA task where typography is a preserved slot | `typo-scale-and-roles` is not selected as a guardrail |

## 11. Tags

`concept-miss`, `ranking-miss`, `context-detection-miss`, `requirements-miss`, `render-defect-fixed`, `skill-neutral`, `preservation-ok`, `partial-scope-ok`
