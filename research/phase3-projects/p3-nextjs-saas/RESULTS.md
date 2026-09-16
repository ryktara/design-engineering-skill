# p3-nextjs-saas — torture-test results

## Task
"Add a team billing settings page with plan comparison, seat management table and invoice history to our Next.js SaaS admin"

## Stack / platform
Web. Next.js 15.3.0 (App Router, server components + small client islands), React 19.1, Tailwind v4.1 (CSS-first `@theme inline`), shadcn-style components (`components.json` new-york/zinc, `cva`, `cn()`, Radix Dialog/Slot, Lucide). Project started as a copy of `evals/fixtures/nextjs-shadcn` (a 7-file stub: one-line button, two-line layout) and was first extended into an honest baseline admin (shell with left rail, dashboard page, Button/Card/Badge/Table primitives, real `globals.css` token set with `.dark`) before inspection, so the skill saw a realistic "existing project".

Rendered with a real `npm install` + `next build` + `next start -p 3111`, screenshotted with Playwright 1.63.0 Chromium 153 at 1440×900 and 390×844 (mobile emulation on). `render_mode: native`.

## Inspection verdict (`01-inspect.json`)
Right (KNOWN): next/react/tailwind/shadcn stack groups; platform web; ui_libraries tailwind/radix/cva/tanstack/recharts/shadcn; tokens (`shadcn cssVariables=True baseColor=zinc` plus the CSS custom-property families); icons lucide; routing `app/`; jsx-a11y; playwright; next-intl; component dirs; product_hints `finance`, `saas`.

Missed / weak:
- `fonts: ["globals (1)"]` — did not detect `Geist`/`Geist_Mono` via `next/font/google` in `app/layout.tsx` (the nextjs stack file explicitly says to detect `next/font`).
- `breakpoints: []` — Tailwind v4 has no config file; the inspector did not fall back to the default `sm/md/lg/xl` screens nor to the `md:`/`sm:`/`lg:` prefixes used in the code. Direction and responsive steps therefore had no breakpoint evidence.
- Dark-mode strategy (`.dark` class with a full second variable set) not reported anywhere.
- Navigation model (left rail already present in `app-shell.tsx`) not reported; the direction later "recommended" a left rail with no knowledge that it already existed.
- `package_manager: null` — fair (no lockfile at inspection time).
- `product_hints: finance` came from the README word "invoices"; it is a SaaS admin with an invoices module, not a finance product. This mislabel propagated (see below).

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| Field | Value | Verdict |
|---|---|---|
| mode | create | right |
| platform | web (KNOWN, inspection) | right |
| input | keyboard, pointer, touch (INFERRED) | right |
| product | finance, saas | **partly wrong** — `finance` inferred from "invoice"; the product is SaaS. It drove `density=high`. |
| screen | settings | right |
| screen_subtype | [] | missing — "billing" / "account settings" would be the natural subtype |
| stack | nextjs, react, shadcn, tailwind | right |
| density | high (INFERRED from finance) | **wrong** for a settings page; medium is right (I built medium: 40 px rows, 14 px body) |
| components | settings, table | **incomplete** — no "plan cards / pricing comparison", no "invoice list / download", no "dialog (destructive confirm)" |
| jobs / primary_jobs | compare; "create settings" | partly — `compare` right; "manage" (seats) and "download/export" (invoices) missing; "create settings" is a nonsense compound |
| risk | medium | arguable — billing/money → trust requirement, I would expect high |
| constraints | preserve_existing_system=true, brand_system_present=false | right |
| accessibility | all six true | right |
| negative_constraints | [] | right |
| missing | brand | right |

Requirements errors recorded: `product=finance (should be saas only)`, `density=high (should be medium)`, `components missing plan-cards/pricing, invoice-list, dialog`, `jobs missing manage, download`.

## Guidance verdict (`03-guidance.md/json`)
Bundle: 3 core + 4 guardrails, coverage 1.0.

Core:
- `dir-operational-workbench` — **partial**. The "tabular figures, hairline borders, one accent, no cards-in-cards, monospace for IDs" advice was useful and I applied it (mono invoice IDs, tabular-nums, quiet neutral surfaces). But a workbench direction for a settings page over-states density; plan cards *are* the right container here and the record says "no hero, no cards".
- `comp-data-entry-grid` — **off-target**. Seat management is a small manage table with row actions, not spreadsheet entry (F2/F4/paste). It was selected only because "table" matched lexically, and it caused the relevant `comp-data-table` to be dropped as "redundant (same category)".
- `comp-settings-screen` — **relevant**. "Current values visible, destructive actions with confirmation, save behaviour explicit" all applied (summary strip, remove-member alertdialog, immediate-effect role select).

Guardrails:
- `layout-states-empty-loading-error` — **relevant**; produced `loading.tsx` skeleton at final sizes, `error.tsx` with retry, invoice empty state, pending-invite partial state.
- `a11y-focus-visible` — **relevant**; verified ring 2 px `#18181b` on white (17.7:1) on all 36/32 stops.
- `anti-hover-only-actions` — **relevant**; row actions are always-visible buttons; test found 0 hover-only controls.
- `data-tables-numeric` — **relevant**; right-aligned tabular amounts, unit in header, one precision.

Knowledge gaps (needed, absent from the base — confirmed by grepping `data/*.jsonl`: no record mentions plan/pricing/seat/billing/invoice beyond lexicon words):
1. Plan / pricing comparison component (current-plan marking, upgrade vs downgrade affordance, seat-limit blocking, billing-cycle toggle, "changes apply at renewal" copy).
2. Seat / member management table (role change inline vs menu, owner protection, invited/deactivated states, seat-usage meter, reactivate path).
3. Invoice history / download list (status vocabulary paid/open/past-due/void, download link naming, receipt duplication in a banner).
4. Payment-method summary block and "past due" alerting.
5. Settings sub-navigation (tabs in the content header for peer settings sections) — `nav-left-rail` text mentions it in one clause but there is no record.

Ranking misses (present in the base, surfaced by `search -k 12`, not in the guidance bundle):
- `card-bordered` — scored **highest** in search (0.567) and its text literally says "selectable cards (plans) use a stronger border + check mark, never colour alone" — exactly this task; not in the bundle. I applied it anyway.
- `comp-data-table` — omitted as redundant with the off-target `comp-data-entry-grid`.
- `a11y-semantics-structure` (0.397) — relevant (th scope, one h1, landmarks); not selected.
- `anti-generic-sidebar-dashboard` (0.556) — off-target for this task but it outranked everything relevant in search; the lexical match on "SaaS admin" is noisy.
- `comp-dialog` (destructive confirm) — never surfaced despite `comp-settings-screen` saying "destructive actions … with confirmation".

## Direction verdict (`04-direction.md/json`)
Validation: OK, no violations. Slot fit for web/SaaS settings:
| Slot | Choice | Fit |
|---|---|---|
| navigation | nav-left-rail | fits; already in the codebase (inspection did not tell the direction that) |
| layout | layout-table-first ("screen mismatch" flagged in its own signals) | **poor** — a settings page with three sections is a sectioned single column; the direction knew it mismatched the screen and chose it anyway. `layout-form-stack` (0.435) was the better alternative. |
| density | density-high | wrong (inherited from `finance`) |
| surface | surface-bordered-panes | fits |
| cards | card-bordered | fits (used for plan cards) |
| typography | typography-neutral-sans | fits; codebase already has Geist |
| color | color-dark-accent (dark-first) | **conflicts with the codebase** (light-first `:root`, `.dark` opt-in); rule "codebase wins" applied; `color-neutral-accent` (0.331) was the right alternative |
| motion | motion-functional-minimal | fits |
| focus | focus-ring-standard | fits |
| cta | cta-sticky-bar | **wrong** — nothing to save; actions are inline per section. `cta-contextual-inline` (0.247) was right and was ranked last. |
| imagery | imagery-data-graphics | not applicable (no charts on this page); harmless |
| icon | icon-outline-system | fits (Lucide) |
| metadata | metadata-rich | partial (column visibility/reorder is overkill for 8 seats and 6 invoices) |

Of 13 slots: 8 fit, 2 partial/n-a, 3 wrong (layout, color, cta) plus density wrong. The fingerprint is therefore a generic "dark dense workbench", not this product. The ledger (KNOWN/INFERRED/MISSING) was accurate and useful.

## First-render defects (numbered)
From `render/first-*.png` and `05-interaction-first.json`:
1. Plan cards: price rows misaligned across the three cards (Business description is one line, others two) — the $10/$20 and $36 baselines differ by ~20 px.
2. Only 1 of 3 plan cards was keyboard-reachable: "Downgrade to Starter" used `disabled` (seat limit exceeded) and the current plan's button is disabled, so Tab skipped both and the explanatory text was undiscoverable.
3. Remove-member dialog: after Escape/Cancel focus fell to `<body>` (`focusReturnedToTrigger: false`) because the dialog is opened from state, not `DialogTrigger`.
4. Mobile: the role `<select>` was in a `hidden md:table-cell` column, so roles could not be changed at all below 768 px (functionality lost, not just hidden).
5. Mobile: 25 of 25 tab stops below 44 px (row action buttons 40×32, download links 32×32, tabs 40 high); desktop had 1 stop below 24 px (banner "Download invoice" link, 115×20).
6. Mobile invoice table: "Amount (USD)" header wrapped to two lines, invoice IDs wrapped mid-number ("INV-2026-" / "0042"), "Past due" badge wrapped.
7. Primary left-rail nav had no active/`aria-current` state (server component without pathname), so "Settings" was not marked while on a settings page.
8. Seat-usage meter read as a stray heavy rule rather than a meter (1.5 px, no boundary).
9. Console: 5 (desktop) / 3 (mobile) 404s from `Link` prefetch of routes that do not exist in the fixture (`/invoices`, `/inventory`, `/settings/general|members|security`). Fixture limit, not a design defect.

## Final defects (remaining)
1. Mobile: 8 stops in the 32–40 px band (segmented Monthly/Annual 32 h, Update 32 h, Invite member 32 h, plan CTAs 36 h, tabs 40 h, skip link 40 h, banner link 36 h). All meet WCAG 2.5.8 (24 px) and the web platform file's 24 px floor; they miss the 44 px "touch-heavy" recommendation. Row actions and download links (the tested set) are 44×44 on mobile.
2. Seat meter still visually heavy at 70 % fill (2 px, bordered now) — cosmetic.
3. Prefetch 404s for stub routes (fixture).
4. `--border` token at 1.27:1 (shadcn zinc default) flagged advisory by `tokens.py validate`; kept because it is the project's existing convention and borders here are not the only boundary cue.

## Iterations
2 renders.
- Iteration 1 (first render): built the page from guidance + direction reconciled with the codebase.
- Iteration 2 (final): fixed defects 1–8 — `min-h-10` on plan descriptions; downgrade button `aria-disabled` + `preventDefault` instead of `disabled`; `onCloseAutoFocus` returns focus to the triggering row button (ref) with a heading fallback; role select duplicated into the member cell below `md`; 44×44 row actions and download links below `sm` (`max-sm:size-11`), tabs `h-11 md:h-10`, banner link `h-9`; `whitespace-nowrap` on invoice IDs and the Badge primitive, unit suffix hidden below `md`; new `PrimaryNav` client component with `aria-current` + active background; meter `h-2` + border. Also tightened the interaction script's focus-indicator check to require a non-transparent, non-zero box-shadow layer (the first version accepted any `box-shadow !== none`, which Tailwind's ring stack always satisfies).

## Interaction test summary (`05-interaction.json`, final)
- 1440×900: 36 tab stops in DOM order — skip link → 4 rail links → 4 settings tabs → Update → banner Download → Monthly/Annual → Downgrade to Starter → Upgrade to Business → Invite member → per seat row (Role select, Remove | Resend, Remove | Reactivate) → 6 invoice Download links. Every stop has a visible indicator (`rgb(24,24,27) 0 0 0 2px` ring; native `<select>` also shows the UA outline). 0 targets < 24 px. 0 hover-only controls; seat rows expose 3/3/3/3/3/4/1 visible actions (owner row 0 by design). Remove dialog: opens with Enter, focus moves inside, Escape closes, focus returns to the trigger. Reduced motion: 0 animated elements under `prefers-reduced-motion: reduce`.
- 390×844: 32 stops (rail hidden), same order otherwise; all with visible focus (`inset` ring on tabs); download links 44×44, row actions 44×44; 8 stops 32–40 px (listed above); dialog and reduced-motion results identical.
- No horizontal overflow at either width (scrollWidth == clientWidth).

## Tokens
`tokens.json` (project palette mapped to the semantic-role schema) — `python scripts/tokens.py validate tokens.json --platform web`: OK, 0 errors, 3 warnings (default border 1.27:1 light / 1.34:1 dark advisory; elevated == canvas in light). Note: the protocol says `tokens.py check`; that subcommand does not exist (`contrast|validate|scale|init`).

## Provenance note
This case did not write under `design-engineering/`. However, several skill files (`data/lexicon.json`, `data/rules.jsonl`, `scripts/de_core.py`, `docs/USAGE.md`, `evals/run_evals.py`, others) have mtimes 00:33–00:37, i.e. they were changed by another process while this case ran. All skill outputs here (`01`–`04`) were produced at 00:29–00:30, before those edits, so the verdicts describe the skill as it was at 00:30 and may not reproduce byte-for-byte against the current data.

## Time spent (rough)
~75 min: baseline project 15, skill steps 5, implementation 25, render + interaction + fixes 20, write-up 10.

## Failure taxonomy tags
`requirements-miss` (finance/density/components/jobs), `ranking-miss` (card-bordered, comp-data-table, comp-dialog, a11y-semantics), `knowledge-gap` (plan comparison, seat management, invoice history, payment method, settings sub-nav), `direction-invariant` (dark-first colour, table-first layout and sticky CTA chosen despite settings screen and light codebase; density inherited from a mislabelled product), `render-defect-fixed` (8), `render-defect-remaining` (2 real + 2 fixture/advisory), `tooling-limit` (inspector misses next/font, Tailwind v4 default breakpoints, dark-mode strategy, existing nav; protocol names a non-existent `tokens.py check`), `skill-helped` (states guardrail, hover-independence, numeric-table rules, focus-ring rule, settings-screen record, card-bordered text via search, tokens.py contrast/validate, KNOWN/INFERRED ledger).
