# p4-01 — billing settings polish (existing UI)

## Task
"polish the billing settings page so plan cards, seat table and invoice history feel consistent with the rest of the admin, without changing navigation or theme"

## Project / stack / platform
`phase3-projects/p3-nextjs-saas/project` — Next.js 15.3 App Router, React 19, Tailwind v4 (`@theme inline`), shadcn-style primitives (Button/Card/Badge/Table/Dialog with `cva` + `cn`), Lucide, Geist via `next/font`. Web, existing UI (the billing page built in Phase 3; the "rest of the admin" is the shell with left rail, the settings tab bar and the dashboard stat cards).

Render mode: **native** (`next build` + `next start -p 3111`, Playwright 1.63 Chromium) at 1440×900 and 390×844 (mobile emulation).

## Design-context table (`01-inspect.json` → `design_context`)
| Field | Detected | Status | Actual (read from `app-shell.tsx`, `globals.css`, `card.tsx`, `dashboard/page.tsx`) | Correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | Left rail (`aside` 224 px, `PrimaryNav`, hidden below `md`) + a secondary tab bar inside `/settings` (`SettingsNav`) | partial (rail right; the settings tab bar, which is the page's own navigation, is not reported) |
| theme | dual-theme, default light | KNOWN | `:root` light zinc tokens + `.dark` block, light-first | yes |
| surfaces | flat-tonal | UNKNOWN ("no shadow or border declarations found") | Bordered cards: `Card` = `rounded-lg border bg-card shadow-sm`; tables in `rounded-lg border`; rail `border-r bg-muted/40` | **no** — Tailwind utility classes (`border`, `shadow-sm`) are not read as surface evidence |
| radius | small (0.5rem) | INFERRED | `--radius: 0.5rem` with `sm/md/lg` derivations, `rounded-md` on controls, `rounded-lg` on containers | yes |
| spacing | 8 | INFERRED | Tailwind 4 px scale, dominant 16/8/4/12/24; page `space-y-6`, card `p-6`, table cell `px-3 py-2` | yes |
| typography | custom ("font family globals") | INFERRED | Geist Sans / Geist Mono via `next/font/google` in `app/layout.tsx`; `text-2xl` h1, `text-lg` section h2, 14 px body, `tabular-nums`, mono IDs | partial (font not named; `fonts: ["globals (1)"]` still misses `next/font`) |
| components | tailwind, radix, shadcn-style cva, table:tanstack, shadcn | KNOWN | as detected (tanstack is a dependency but unused on this page) | yes |

## Requirements verdict (`02-requirements.json`, exit 0 CONFIDENT)
| Field | Value | Verdict |
|---|---|---|
| scope | UI_DESIGN, in_scope | right |
| mode | polish, refactor | polish right; **refactor wrong** — evidence is "structural words: navigation" taken from the *negative* clause "without changing navigation" |
| intent.preserve | navigation, color | right ("theme" → color) |
| negative_constraints / constraints | navigation-change; preserve_existing_system, preserve_navigation, preserve_color | right |
| change_budget | low | right |
| platform / stack / screen | web; nextjs, react, shadcn, tailwind; settings | right |
| product | finance, saas | finance still inherited from the README word "invoices" (Phase 3 miss, unchanged) |
| density | high | wrong (from finance); harmless here because the direction preserved the repo's density |
| components | card, navigation, settings, table | card/settings/table right; **navigation spurious** (same negative clause) |
| jobs | [] | missing (compare plans, manage seats, download invoices) — acceptable for a polish task |
| project_context | as in the table above | surfaces UNKNOWN propagated |

## Guidance verdict (`03-guidance.md/json`)
Bundle 8 = core 3 + guardrails 5. Metrics: concepts 8/8, tokens≈1113, coverage/1k 7.19, purity 0.89, redundancy 0.5, uncovered required concerns none.

| Record | Role | Verdict | Why |
|---|---|---|---|
| `comp-plan-comparison` | core | relevant | New record since Phase 3; names plan cards / seat table / invoice list explicitly. Its "radio group of cards, arrows move between plans" clause does not fit cards that each carry their own CTA (I kept per-card buttons). |
| `card-bordered` | core | relevant | "1 px border, 6–8 px radius, header row with title and one action, selectable cards use stronger border + check mark" — matches the existing `Card` primitive and the current-plan treatment. |
| `comp-settings-screen` | core | partial | Generic settings-screen advice; only "current values visible / destructive with confirmation" applies and was already there. |
| `a11y-keyboard-operable` | guardrail | relevant | Held (36/32 stops, dialog escapable). |
| `anti-oversized-hero-text` | guardrail | relevant | Decided the summary cards keep 16 px values (not the dashboard's 24 px KPI size) so the plan price stays the one display-size element. |
| `a11y-focus-visible` | guardrail | relevant | Verified on every stop. |
| `layout-spacing-scale` | guardrail | relevant | Drove the "one inset per container type" cleanup (all cards `p-6`, section gap 32 px, inside-group 16 px). |
| `layout-states-empty-loading-error` | guardrail | relevant | `loading.tsx` skeleton re-shaped to the new card sizes. |

Relevant 7, partial 1, off-target 0.

Missing guidance:
- **Reuse the project's own primitives** (Card/Button/Badge) instead of restyled divs — the single most useful instruction for a "feel consistent with the rest of the admin" task. SKILL.md says "reuse → extend → compose", but no record carries it, so the bundle never mentions `Card`/`buttonVariants`. **Knowledge gap.**
- `data-tables-numeric` was rank 6 in `search -k 12` (0.396) but not selected; the invoice table already complied, so no harm. Ranking miss, low impact.
- Nothing about **secondary navigation tabs inside a settings section** (still absent from the base; noted in Phase 3).

## Direction verdict (`04-direction.md/json`, validation OK)
Change budget low · preserved [navigation, density, typography, color] · changed [].

| Slot | Choice | Status | Justified? |
|---|---|---|---|
| navigation | nav-left-rail (existing) | preserved | yes |
| layout | layout-table-first | new ("no repository evidence") | **no** — a settings page with four sections is a sectioned single column; `layout-form-stack` was 2nd (0.337). Same miss as Phase 3. |
| density | spacing base 8 (existing) | preserved | yes |
| surface | surface-bordered-panes | new | wrong reason — the repo *has* bordered cards + `shadow-sm`; the slot was "new" only because surfaces were UNKNOWN. Outcome compatible by luck. |
| cards | card-bordered | new | fits the existing `Card` primitive |
| typography | custom (existing) | preserved | yes |
| color | light-first dual theme (existing) | preserved | yes |
| motion | functional-minimal | new | fits (project has `transition-colors` only) |
| focus | focus-ring-standard | new | fits (project ring token) |
| cta | cta-toolbar-commands | new | **no** — nothing is selection-driven on a settings page; `cta-contextual-inline` (0.211) is what the page does. Phase 3 picked sticky-bar; now toolbar; still wrong. |
| imagery | imagery-data-graphics | new | n/a (no charts) |
| icon | icon-outline-system | new | fits (Lucide) |
| metadata | metadata-rich | new | partial (mono IDs, status text+colour yes; column chooser no) |

Preservation metrics: 4 preserved / 9 new / 0 changed; unjustified new choices: layout, cta (2). No slot asked me to change navigation, theme, type or density — the preserve mechanism worked.

## Implementation
Files changed (copies in `before/`):
- `app/settings/billing/page.tsx` — summary strip (`dl` in a bordered grid) replaced by four `Card`s using the dashboard's exact stat-card structure (`CardHeader pb-2` + `CardDescription` + `CardTitle` + `CardContent text-xs`), `dl/dt/dd` semantics kept via `asChild`; open-invoice notice becomes its own `rounded-lg border bg-muted/40` row with a ghost `buttonVariants` download link (was a bare underlined anchor); section gap `space-y-10` → `space-y-8`.
- `components/ui/card.tsx` — **extended** `CardTitle`/`CardDescription` with `asChild` (Radix `Slot`, same convention as `Button`).
- `components/ui/button.tsx` — base classes gain `aria-disabled:opacity-50 aria-disabled:cursor-not-allowed` so the seat-blocked "Downgrade" button uses the primitive's disabled look instead of an ad-hoc `opacity-60`.
- `components/billing/plan-comparison.tsx` — plan cards are `Card/CardHeader/CardContent/CardFooter` (same surface, radius, `p-6`, `shadow-sm` as the dashboard); seat-limit note moved above the button so all three CTAs share a baseline; badge `-my-1` so the "Current" chip no longer shifts the title row.
- `components/billing/status-badge.tsx` (new, composed from `Badge`) — one `StatusBadge` with tones success/warning/destructive/info/neutral used by both tables (removed two duplicated badge implementations).
- `components/billing/seat-table.tsx` — uses `StatusBadge`; seat meter is a 160 px `h-1.5` track with "70% used" next to it instead of a full-width 2 px bordered rule (Phase 3's "reads as a stray rule" defect).
- `components/billing/invoice-history.tsx` — uses `StatusBadge`; download link uses `buttonVariants({variant:"ghost", size:"sm"})` like the seat row actions.
- `app/settings/billing/loading.tsx` — skeleton matches the new card dimensions.

Not changed: routes, `lib/billing.ts`, dialog logic, aria names, test ids, `globals.css`, navigation, theme.

## First-render defects (`render/first-*.png`, `05-interaction-first.json`)
1. **visual** — "Current" badge made the Team card's title row 2 px taller than its siblings (prices at y 593/595/593).
2. **visual** — Starter's CTA sat 24 px above the other two because the seat-limit note was below it inside the footer (CTAs at 795/819/819).
No interaction, accessibility, platform, existing-system-mismatch or implementation-bug defects: 36/32 stops all with a visible ring, 0 hover-only controls, dialog opens/escapes/returns focus, no horizontal overflow, 0 animated elements under reduced motion.

## Final defects (`render/final-*.png`, `05-interaction.json`)
- visual 0 (prices 593/593/593, CTAs 817/817/817).
- Mobile: 8 stops in the 32–40 px band (segmented control, Update, Invite, plan CTAs, tabs) — unchanged from Phase 3, above the 24 px web floor; not introduced by this task.
- Mobile: four stacked summary cards take ~380 px before "Plans" (the old strip took ~300 px). Accepted: it is the dashboard's own mobile behaviour, which is what "consistent with the rest of the admin" asks for.
- Prefetch 404s for stub routes (fixture).

## Iterations
2 renders (first → fix 1–2 → final).

## Interaction test summary
1440×900: 36 Tab stops in DOM order, all with the 2 px `#18181b` ring (17.7:1 on white); 0 targets < 24 px; 0 hover-only actions; seat rows show 0/3/3/3/3/3/4/1 visible actions; remove dialog: Enter opens, focus moves in, Escape closes, focus returns to the trigger; reduced motion: 0 animated elements. 390×844: 32 stops, same results; download links and row actions 44×44. Contrast (tokens.py): success #15803d 5.02:1, warning #a16207 4.92:1, destructive #dc2626 4.83:1 on white; dark variants 11.4–13.0:1.

## Preservation verdict
Navigation (rail + settings tabs) untouched; theme tokens untouched (no new hex, all new styles go through existing tokens/variants); typography scale unchanged; component language *more* consistent (Card/Button/Badge primitives now used where restyled divs were). Structural changes: summary strip → stat cards (justified: it is the admin's existing stat pattern), plan cards → Card primitive (justified). Unjustified structural changes: 0.

## Regressions to propose
- query: "polish the billing settings page … without changing navigation or theme" → expect mode = [polish] only; `components` must not contain `navigation`; `negative_constraints` = [navigation-change] (already right).
- query: "make this settings page consistent with the rest of the admin" (nextjs+shadcn project) → expect a core record that says reuse the project's existing primitives (Card/Button/Badge) before restyling; expect layout slot ≠ table-first and cta slot ≠ toolbar-commands for `screen=settings`.
- inspector: a project whose `components/ui/card.tsx` contains `border` + `shadow-sm` Tailwind classes → expect `design_context.surfaces` = bordered/elevated with KNOWN status, not UNKNOWN.
- inspector: `app/layout.tsx` importing `Geist` from `next/font/google` → expect `fonts` to name Geist and typography status KNOWN.

## Tags
`mode-miss` (refactor from the negative clause), `requirements-miss` (components=navigation, product=finance/density=high carried over), `context-detection-miss` (surfaces UNKNOWN, font unnamed, settings tab bar unreported), `knowledge-gap` (reuse-existing-primitives rule; settings sub-navigation), `ranking-miss` (data-tables-numeric, low impact), `direction-mismatch` (layout-table-first, cta-toolbar-commands), `render-defect-fixed` (2), `render-defect-remaining` (0 new; pre-existing mobile 32–40 px targets), `skill-helped` (comp-plan-comparison + card-bordered named the right containers; spacing-scale and oversized-text guardrails decided the card padding and value sizes; preserve mechanism kept nav/theme/type/density), `preservation-ok`.

## Provenance note
Nothing under `design-engineering/` was written by this task. Files there (`data/lexicon.json`, `data/rules.jsonl`, `data/patterns.jsonl`, `data/components.jsonl`, `data/antipatterns.jsonl`, `docs/USAGE.md`, `docs/MAINTENANCE.md`, `evals/development/*.json`) show mtimes 12:16–12:23 from another process; the skill commands for this task ran at 12:20–12:21 (inspect) and immediately after (requirements/guidance/direction/search), so the recorded outputs reflect the data as it was at that moment and may not reproduce byte-for-byte later.
