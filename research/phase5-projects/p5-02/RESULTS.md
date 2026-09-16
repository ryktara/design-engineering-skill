# p5-02 — Team members page with an invite flow (p3-nextjs-saas)

**Task (verbatim):** "Add a team members page with an invite flow, consistent with the rest of the settings area."
**Project / stack / platform:** `research/phase3-projects/p3-nextjs-saas/project` — Next.js 15.3 app router, React 19, Tailwind v4 (`@theme inline`), shadcn new-york/zinc primitives (Table, Badge, Button, Card, Dialog, Skeleton), Radix Dialog, Lucide, Geist via next/font. Platform: web.
**Existing UI or new screen:** new screen (`/settings/members`) inside an existing settings area. The settings layout, tab-style `SettingsNav` (which already linked `/settings/members` → 404), left rail, header, and the billing page's seat table + confirm dialog + live region all pre-exist. Billing files were off-limits (p5-01 editing them concurrently) and were not touched.
**Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (identical; skill untouched).

## Design-context table (inspect_project)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | left rail (`app-shell.tsx`, hidden <md) + top header; settings area adds a horizontal tab sub-nav (`settings-nav.tsx`) | partial — primary nav right; the settings sub-navigation (tabs with `aria-current`) is the pattern this task must match and is not detected |
| theme | dual-theme, default light | KNOWN | `:root` light + `.dark` opt-in class | yes |
| surfaces | bordered-flat | INFERRED | `Card` = `border` + `shadow-sm`; tables in `rounded-lg border` wrappers; dialog `border` + `shadow-lg` | yes (shadow-sm is the only elevation; "bordered" is the right read) |
| radius | small (0.5rem) | INFERRED | `--radius: 0.5rem`, `rounded-md` on controls, `rounded-lg` on panels | yes |
| spacing | 8 | INFERRED | Tailwind 4-px scale; `space-y-8` between sections, `gap-4` grids, `p-6` cards | yes |
| typography | custom | KNOWN | Geist Sans + Geist Mono via `next/font`, `tabular-nums`, `font-mono` for ids; `text-2xl` h1 / `text-lg` h2 / `text-sm` body | partial — "custom" is correct but the font family (Geist) and the h1/h2/body scale visible in `layout.tsx` + `settings/layout.tsx` are not reported |
| components | tailwind, radix, shadcn-style cva, table:tanstack, shadcn | KNOWN | correct; note `@tanstack/react-table` is a dependency but unused in source (tables are the plain shadcn `Table`) | yes (dependency-level) |

## Requirements verdict

| item | resolved | verdict |
|---|---|---|
| platform | web (`platform_evidence: []`, from project inspection; `known` lists `platform=web (project inspection)`) | correct |
| artifact_state | existing (`intent_evidence.existing: ["consistent with"]`) | acceptable — pre-registered as "new"; "existing" was declared acceptable because preservation of the settings shell is what matters and `constraints.preserve_existing_system=true` |
| operations | create | correct |
| problem_domain | [] | correct (feature request, not a defect) |
| change_scope | screen | partial — the sentence names a page **and** a flow; `intent_evidence.scope.flow` caught "flow" but the resolved scope dropped it |
| mode | create (`mode_evidence: "build/create request on an existing surface"`) | correct |
| scope.kind | in-scope, reason "UI design / interaction task" | correct. `scope_evidence.technical.BACKEND: ["rest"]` fired on "the **rest** of the settings area" — a false lexical hit that did not affect the verdict |
| change_budget | moderate | correct |
| preserve | ["system"] | correct but coarse; navigation/typography/color preservation flags are set in `constraints` |
| project_context | mirrors inspect | see table above |
| screen / components | [] / [] | miss — "team members page" and "invite" produced no screen type (settings/members list) and no component hint (dialog/form/table) |

## Guidance verdict (bundle: 3 core + 3 guardrails, 1081 tokens, status CONFIDENT)

| record | role | verdict | BAD category | why |
|---|---|---|---|---|
| `comp-plan-comparison` | core | partial | wrong-mode/off-target (recorded as `generic`) | Chosen as "highest-scoring component with lexical evidence" — the evidence is "settings"/"billing". Its seat-management clause (data table name/role/status/last active, keyboard-reachable row actions, confirm dialog that returns focus) is exactly right; the plan-radio-group, invoice-history and "bulk selection state" clauses are off-task for a members page. |
| `comp-form` | core | relevant | — | Labels above, required marked in text, inline validation with `aria-describedby`/`aria-invalid`, autofill attributes: all used. "Unsaved-changes guard" and "autosave" are irrelevant for a two-field invite. |
| `cta-sticky-bar` | core | off-target | contradicts-codebase | Nothing in the settings area uses a sticky bar; actions live in the section header (`Invite member`) and dialog footer. Following it would have broken consistency, which the task sentence explicitly demands. |
| `a11y-keyboard-operable` | guardrail | relevant | — | Escape closes and returns focus to the invoker: implemented and verified. |
| `a11y-focus-visible` | guardrail | relevant | — | 2 px ring on every control; the invalid field swaps to a destructive-coloured ring. Verified. |
| `web-responsive-breakpoints` | guardrail | partial | generic | Correct but generic; "dialogs transform (sheet ↔ dialog)" was not needed — the existing `DialogContent` is already `w-[calc(100%-2rem)] max-w-md`. |

Omitted `comp-settings-screen` ("same category as a core pick") — it lost to `comp-plan-comparison`, the wrong record of the two for this task. Never retrieved: `comp-dialog` / `a11y-modal-dialog` (a targeted search "invite member dialog email validation focus return" returns `a11y-modal-dialog` at 0.567 — the knowledge exists), `impl-reuse-before-new`, `layout-states-empty-loading-error`, `a11y-live-status`.

### Concept recall

Delivered (union over the 6 selected records): a11y.color_not_only, adaptive.breakpoint_matrix, adaptive.navigation_transform, data.comparison_structure, feedback.confirmation_destructive, feedback.validation_errors, form.autofill_attributes, interaction.focus_visible, interaction.hover_independence, interaction.keyboard_navigation, layout.one_primary_action, state.unsaved_changes_guard, table.selection_bulk, table.tabular_figures, touch.ime_keyboard.

| expected | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| process.reuse_first | yes | no | bundle-selection — demanded (recommended: "existing repository: reuse its primitives"), candidate `impl-reuse-before-new` 0.243, dropped ("bundle cap or lower utility"); `cta-sticky-bar` took a core slot instead |
| feedback.validation_errors | yes | yes (`comp-form`) | — |
| a11y.dialog_focus | yes | no | expected-concepts — never demanded; the sentence's "invite flow" + the repo's `@radix-ui/react-dialog` / `components/ui/dialog.tsx` were not turned into a dialog concept. Records `a11y-modal-dialog`, `comp-dialog` carry it |
| layout.one_primary_action | no | yes (`comp-plan-comparison`) | — |
| state.loading_empty_error | no | no | expected-concepts — never demanded (`states` concern was only "recommended: few states; still handle failed media" — a media-oriented reason on a data page). Records `layout-states-empty-loading-error`, `comp-empty-state` carry it |
| a11y.live_status | no | no | expected-concepts — never demanded. Records `a11y-live-status`, `comp-toast-notification` carry it |
| form.autofill_attributes | no | yes (`comp-form`) | — |

**Recall 3/7 = 0.43 · critical recall 1/3 = 0.33.** No forbidden concept was delivered. Off-task concepts delivered: `table.selection_bulk`, `data.comparison_structure`, `state.unsaved_changes_guard`, `touch.ime_keyboard`, `adaptive.navigation_transform` (5 of 15 — purity 0.64 as the metrics say).

## Direction verdict

Preserved: navigation (left-rail), surface (bordered-flat), typography, color — all justified, all honoured. `validation: OK`. `preservation` metrics: preserved 4 slots, changed 0.

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | nav-left-rail | preserved | yes; but the slot guidance says "secondary navigation lives in the content header … Mark active section" — the repo's tab sub-nav already does this and is what had to be reused |
| layout | layout-form-stack | new | no — a members page is a table with a dialog form; `layout-table-first` scored the same (0.42) and matches the codebase (`SeatTable`, `InvoiceHistory`). Form-stack describes only the inside of the dialog |
| density | density-high | new | acceptable (finance/saas inference); the repo is medium-dense (`h-10` header rows, `py-2` cells) — followed the repo |
| surface | surface-bordered-panes | preserved | yes |
| cards | card-bordered | new | acceptable but unused (no cards on this page; kept the repo's bordered table wrapper) |
| typography / color | preserve | preserved | yes |
| motion | motion-functional-minimal | new | yes (repo's `motion-safe:animate-in`) |
| focus | focus-ring-standard | new | yes, matches repo `focus-visible:ring-2 ring-ring` — but "new" is wrong: the repo already has this |
| cta | cta-sticky-bar | new | no — contradicts the codebase (see guidance); alternative `cta-single-primary` (0.33) was the right one |
| imagery | imagery-thumbnails | new | no — no imagery on this page; harmless but noise |
| icon | icon-outline-system | new | yes (Lucide) — again "no repository evidence" is wrong: `icons: ["lucide"]` is in the inspect output |
| metadata | metadata-rich ("columns with user-controlled visibility and order") | new | partial — over-scoped for an 8-row members list; status-as-text+icon part is right |

Direction mismatch count: 3 unjustified (layout, cta, imagery) + 2 "new" slots that actually had repository evidence (focus, icon).

## Implementation summary

New files (nothing pre-existing was modified; billing untouched):
- `app/settings/members/page.tsx` — server component under the existing settings layout (Members tab becomes `aria-current="page"` automatically); `metadata.title` in the billing page's "X · Settings · Acme Console" form.
- `app/settings/members/loading.tsx`, `error.tsx` — skeleton and error boundary mirroring the billing ones.
- `components/members/members-table.tsx` — client roster: Member / Role / Status / Last active / Actions using `ui/table`, `StatusBadge` (same label + tone + icon shape as the seat table), role `<select>` per row, Resend / Revoke for invites, Remove (confirm `alertdialog`, focus returned to the trigger or heading), Reactivate; `role="status"` live region; column hiding sm/md/lg and stacked role+status on narrow widths, 44 px icon-only row actions <sm.
- `components/members/invite-member-dialog.tsx` — `Dialog` + `DialogTrigger` (Radix moves focus in and restores it to the trigger); email (`type=email`, `inputMode`, `autocomplete=email`, `autocapitalize=none`, required marked in text) + role select with a description; validation on submit and on blur-after-typing; error in a reserved slot with `role="alert"`, linked by `aria-describedby`/`aria-invalid`; duplicate/pending-invite detection; seat-availability sentence and disabled submit when no seats remain.
- `components/ui/input.tsx`, `components/ui/label.tsx` — shadcn-style primitives (the repo had none), sized to the existing role `<select>` (h-11 touch / h-9 md).
- `lib/members.ts` — `Member` = `Seat` (one roster shared with billing, read-only), invitable roles, `validateInviteEmail`.

Guidance used: `comp-form` (labels, required-in-text, inline errors with aria wiring, autofill attributes), the seat-management clause of `comp-plan-comparison` (table columns, keyboard-reachable row actions, confirm dialog returning focus), both a11y guardrails, direction's preserved slots.
Guidance ignored: `cta-sticky-bar` (contradicts the settings area), `layout-form-stack` as page layout (page is table-first; form-stack applied only inside the dialog), `metadata-rich` column controls, `imagery-thumbnails`, `table.selection_bulk`, `state.unsaved_changes_guard`. Added without guidance: dialog focus management, live-region announcements, loading/error states, seat-availability trust signal, duplicate detection.

## Render

Mode: native (Next dev server, Playwright 1.63 Chromium). Port 3111 was occupied by a `next start` serving p5-01's build, and `next dev` in the same directory would overwrite its `.next`, so the project sources were copied to `p5-02/render/project-copy` with a `node_modules` junction and served on 3112 (copy removed afterwards). A first attempt in the scratchpad on `C:` failed with a Tailwind/css-loader `RangeError: Invalid code point` on that path — tooling note only.
Screenshots: `render/first-*.png` and `render/final-*.png` at 1440×900 and 390×844: page fold, full page, `invite-open`, `invite-empty`, `invite-invalid`, `invite-sent`. Interaction evidence: `render/first-interaction.json`, `render/final-interaction.json` (open via keyboard → Enter on empty → invalid → duplicate → valid → Escape; focus target, aria wiring, live text, row count, action target sizes).

### First-render defects
- **interaction (1):** on a touch tap of "Send invite" with an invalid value, nothing submitted and focus stayed on the button. Traced with an event log (`render/probe2.js`): blur validation inserted the error line, the footer moved ~20 px, and the tap's `mouseup`/`click` landed on the form instead of the button (`click on FORM`, no `submit`). Desktop click was unaffected. Root cause is layout shift from on-blur validation — a real-phone defect.
- visual 0 · accessibility 0 · platform 0 · existing-system-mismatch 0 · implementation-bug 0.
Console errors: 0 at both viewports. No horizontal overflow (scrollWidth = clientWidth). Members tab active; `<title>` "Members · Settings · Acme Console".

### Fix and final
Iteration 1: deferred the refocus with `requestAnimationFrame` — did not help (the click never reached the button). Iteration 2: reserved a fixed `min-h-5` slot for the error message and shortened the duplicate messages to one line. Event log now: `click on BUTTON → submit on FORM → focusin on invite-email`. Final: all steps pass at both viewports; touch and mouse paths identical.
- **Final defects:** visual 1 (minor, accepted trade-off: an empty 20 px slot under the email field while there is no error — see `final-1440x900-invite-open.png`); interaction 0; accessibility 0; platform 0; existing-system-mismatch 0; implementation-bug 0.
- **Iterations:** 2.
- `tsc --noEmit`: clean. (`next lint` is not configured in this project — it prompts for setup; skipped.)

## Preservation verdict
Navigation preserved (rail, header, settings tab nav reused; Members tab now resolves). Theme preserved (only existing tokens: `border-input`, `ring-ring`, `text-destructive`, `text-warning`, `bg-muted`). Typography preserved (same h2 `text-lg font-semibold tracking-tight`, `text-sm` body, `tabular-nums`). Component reuse: Table, Dialog, Button, Badge via StatusBadge, Skeleton; Input/Label added in the same style because none existed. Unjustified structural changes: 0. Billing files: untouched.

## Regressions to propose
1. Query: "Add a team members page with an invite flow, consistent with the rest of the settings area." (project: nextjs+shadcn with `@radix-ui/react-dialog`) — expect `a11y.dialog_focus` and `process.reuse_first` demanded and delivered; expect `cta-sticky-bar` **not** in core when the request says "consistent with" an existing area; expect `comp-settings-screen` or a members/roster record to outrank `comp-plan-comparison`.
2. Query: any "invite / add member / add user" flow — expect `a11y.live_status` and `feedback.validation_errors` demanded; expect the message-slot / no-layout-shift-on-validation rule (`perf.layout_shift` or a validation rule) — the defect found here is a validation-on-blur classic.
3. Query: "Add a … page" on a project with `loading.tsx`/`error.tsx` conventions — expect `state.loading_empty_error` demanded (the `states` concern reason should not be media-specific for a data page).
4. Scope lexicon: "the rest of" must not register as `BACKEND: rest`.
5. Direction: a slot must not be reported as "new / no repository evidence" when inspect already reports it (`icons: lucide` → icon slot; `focus_handling` → focus slot).
6. Inspect: report the settings sub-navigation pattern (tabs with `aria-current`) and the font family from `next/font` imports.

## Tags
`concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `skill-neutral`, `preservation-ok`, `tooling-limit`

Skill effect: **neutral**. The requirements layer (platform, mode, scope, budget, preserve) was right and cost nothing. The guidance that mattered for the outcome (`comp-form` and the seat-table clause) restated what the codebase already demonstrates; the three concepts that decided quality here — dialog focus, live status, loading/error states — came from reading the repo, not the skill; and one core record (`cta-sticky-bar`) plus the direction's layout/cta slots had to be actively ignored to satisfy the task sentence. The defect that surfaced (blur validation causing layout shift on touch) was not covered by any delivered record.
