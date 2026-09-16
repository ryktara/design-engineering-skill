# p6-07 — "Front desk on a tablet: the appointment chips are too small to tap."

- **Project**: `research/phase5-projects/p5-sveltekit-clinic/project` (ClinicBoard)
- **Stack / platform**: SvelteKit 2 + Svelte 5 runes + Tailwind 3 · web, used on a tablet
- **Artifact state**: existing UI (`/appointments` day grid). No new screen.
- **Build hash start = end = `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`** (matches the frozen c3 candidate).
- Another task owns the patient billing tab; nothing under `src/routes/patients/` was touched.

## 1. Design context (inspect_project.py)

| field | detected | status | actual | correct? |
|---|---|---|---|---|
| navigation | left-rail | KNOWN | fixed 240px left rail in `+layout.svelte` | yes |
| theme | light-first | INFERRED | `color-scheme: light` only, explicitly light-only | yes |
| surfaces | bordered-flat | INFERRED | `Card` = white + `border-neutral-200`, almost no shadow | yes |
| radius | unknown | UNKNOWN | `tailwind.config.ts` defines a full radius scale (sm 4 / DEFAULT 6 / lg 8 / xl 12) | **partial** (clear in code, reported UNKNOWN) |
| spacing | 4 | INFERRED | Tailwind 4px base, used consistently | yes |
| typography | custom | INFERRED | Source Sans 3 + tabular numerals | yes |
| components | tailwind | KNOWN | 9 local primitives in `src/lib/components` | partial (local component library not named) |
| breakpoints | `[]` | — | Tailwind defaults, no custom breakpoints | acceptable |

## 2. Requirements verdict

- `platform`: `tablet` (DIRECT, from the word "tablet"); project platform `web` recorded as a conflict, "request kept". Correct in spirit — but see the candidate-compatibility miss below, where `tablet` is then treated as *incompatible with* `web`.
- `intent.artifact_state`: `existing` yes · `operations`: `["diagnose","modify"]` yes · `problem_domain`: `["responsive","interaction","visual"]` yes · `change_scope`: `unknown` (moderate elsewhere) — acceptable.
- `mode`: `["responsive","audit"]` — acceptable (pre-registration allowed refactor/responsive/polish/accessibility). The sentence carried no mode word.
- `scope.kind`: `in-scope` (matches pre-registration).
- `change_budget`: `moderate`. `intent.preserve`: `[]` but `constraints.preserve_existing_system: true`.
- `accessibility.touch_targets: true`, `input: touch` — the skill read the real problem.
- `status: AMBIGUOUS`, `missing: []`.

## 3. Guidance verdict

Bundle: **0 core + 6 critical guardrails**, no optional layer. ~815 tokens.

| record | layer | verdict | category |
|---|---|---|---|
| `a11y-target-size` | critical | **relevant** — the record that drove the fix (44px touch, "extend the hit area rather than the glyph") | — |
| `impl-reuse-before-new` | critical | relevant | — |
| `layout-spacing-scale` | critical | partial | generic |
| `layout-hierarchy-one-thing` | critical | partial | generic |
| `mobile-orientation-size-classes` | critical | partial | off-platform (bottom nav / safe areas / IME — a phone record applied to a tablet web app with a left rail) |
| `shared-device-privacy` | critical | **off-target** | generic — selected as a *critical* concept from the `healthcare` product hint alone; masking/PIN/idle-reset has nothing to do with a tap-target defect, and it is the largest single record in a 6-record bundle |

Counts: relevant 2 · partial 3 · off-target 1. `layer_review`: core `[]`, critical 6 ids, optional `[]` (optional_useful 0, optional_noise 0).

### Concept recall

| expected id | delivered? | layer if missing |
|---|---|---|
| `touch.minimum_target` (**critical**) | yes (`a11y-target-size`, SPECIFIC) | — |
| `adaptive.breakpoint_matrix` | yes (`mobile-orientation-size-classes`, GENERIC) | — |
| `layout.spacing_scale` | yes (`layout-spacing-scale`) | — |
| `interaction.hover_independence` | no | candidate-compatibility — `anti-hover-only-actions` was *filtered out*: "platform ['desktop','web'] not in request ['tablet']". A tablet is a web browser; this is the clearest skill miss of the task. `comp-menu` and `comp-filters` were dropped the same way. |
| `touch.gestures_discoverable` | no | bundle-selection — `mobile-gestures-discoverable` / `interaction-drag-drop` were candidates and lost on utility. The chips *are* a drag-to-reschedule surface, so this was a real gap. |
| `interaction.focus_visible` | no | expected-concepts (never demanded) — low severity, the project already has focus-visible rings. |

**concept_recall = 3/6 = 0.50 · critical_recall = 1/1 = 1.00.**

Bundle also delivered, unasked: `privacy.shared_device`, `privacy.sensitive_masking`, `state.session_expiry`, `touch.safe_areas`, `layout.focal_hierarchy`, `layout.one_primary_action`, `data.exception_first`, `adaptive.navigation_transform`, `process.reuse_first`.

## 4. Direction verdict

12 slots `preserved` (navigation, layout, density, surface, cards, typography, color, motion, focus, cta, imagery, icon) — correct for an existing UI at a moderate budget. Validation: OK.

1 slot `new`: **metadata — "Moderate metadata with a hierarchy"**, reason "no repository evidence for this slot". The task did not justify changing how chip metadata is ranked, and the repository plainly *does* have a metadata convention (name · time / reason · status badge). `unjustified_direction_slots = 1`.

## 5. Implementation

Files changed (copies in `before/`):
- `src/routes/appointments/+page.svelte`

The day grid positions chips at `durationMin x PX_PER_MIN`, with `PX_PER_MIN = 2`. The shortest booking is 15 min, so a chip was **28px** tall: well under 44px, and that is exactly the front-desk complaint.

1. `PX_PER_MIN` became `$derived` on a `touchScale` flag driven by `matchMedia('(pointer: coarse), (max-width: 1024px)')` (registered in an `$effect`, SSR-safe default `false`). Touch scale = **3.2 px/min** (192px/hour), so a 15-min slot is 48px.
2. `CHIP_INSET` (`$derived`, 2 on touch / 1 otherwise) replaced the hard-coded `+1 / -2` on both the chip and the drop ghost: a 15-min chip is a **44px target with a 4px gap** to the next booking, so adjacent bookings are not one continuous strip of mis-taps.
3. The "show reason + status" condition changed from `durationMin >= 30` to a *rendered-height* test (`>= 44px`). At touch scale a 15-min chip now shows reason and status badge; at pointer scale the behaviour is identical to before (28px < 44 hidden, 58px shown). This removes the tablet's dependence on the `title=` tooltip, which no touch user can see.

`GRID_HEIGHT`, `top()`, `height()`, drag snapping (`SNAP_MIN = 15`) and the arrow-key reschedule path all follow the derived scale; no routes, stores, ids, `aria-label`s or the live-region status line were touched.

- **guidance used**: `a11y-target-size` (the 44px number and "extend the hit area, not the glyph" — I scaled the time axis instead of inflating chip text), `impl-reuse-before-new` (no new component; the existing chip block was parameterised), `layout-spacing-scale` (the 4px inter-chip gap came off the project's 4px scale).
- **guidance ignored**: `shared-device-privacy` (nothing to mask; acting on it would have changed a screen the task is not about), `mobile-orientation-size-classes` (bottom-nav/safe-area advice does not apply — this app has a left rail and no native chrome), `layout-hierarchy-one-thing` (would have meant re-ranking the grid's focal point; out of budget), the direction's `metadata: new` slot (unjustified).

**Process guidance check**: `impl-reuse-before-new` was in the bundle and was directionally right, but SKILL.md §2/§7 already say the same thing; I did not need it in the bundle to reuse the existing chip markup or to render-and-inspect. `process_records_needed: false` — in a 6-record bundle it cost a slot that `anti-hover-only-actions` or a gesture record would have used better.

## 6. Render

Mode: **native web** — Playwright 1.63.0 + Chromium against `vite preview` of the production build. Three contexts: 1024x768 `hasTouch`, 1280x800 `hasTouch`, 1280x800 pointer (the unchanged desktop baseline). Screenshots in `render/`; measurements taken in-page from `getBoundingClientRect()`.

| context | first render min chip height | final |
|---|---|---|
| tablet 1024x768 | 43px (1 chip under 44) | **44px, 0 under 44** |
| tablet 1280x800 | 43px | **44px, 0 under 44** |
| desktop 1280x800 | 28px | 28px (unchanged by design; above the 24px WCAG 2.5.8 pointer minimum) |

**First-render defects (1): accessibility 1** — the first attempt used 3 px/min, giving 45px minus the 2px inset = 43px measured: one pixel short of the target the guidance named. Caught by measuring, not by eye. Fixed by moving to 3.2 px/min and a touch-aware inset. Iterations: **1**. **Final defects: 0.**

Not a defect from this change, but visible in the desktop shot: two overlapping bookings (Charlie Xu 09:15 / Alfie Zielinski 09:30) paint over each other — the grid has no overlap-collision layout. Pre-existing, out of scope, left alone.

## 7. Preservation

Left rail, header, teal token palette, Source Sans 3, `Card`/`Badge`/`Select`/`Modal` primitives, drag + arrow-key reschedule, the `aria-live` move status and every `aria-label`: unchanged. No new component, no new token, no arbitrary hex. Desktop rendering is behaviourally identical to `before/`. `preservation-ok`, `unjustified_structural_change: 0`.

## 8. Miss routing (earliest layer, one per miss)

1. `interaction.hover_independence` missing — **candidate-compatibility**: resolved platform `tablet` filtered out every record tagged `web`/`desktop`, including `anti-hover-only-actions`, `comp-menu`, `comp-filters`. A tablet request against a web codebase must stay compatible with web records.
2. `touch.gestures_discoverable` missing — **bundle-selection**: candidates existed (`mobile-gestures-discoverable`, `interaction-drag-drop`) and lost on utility, on a screen whose whole interaction is drag-to-reschedule.
3. `shared-device-privacy` promoted to critical on a tap-target task — **criticality**: the `healthcare` product hint alone marked `privacy.shared_device` / `privacy.sensitive_masking` as critical required concepts.
4. `metadata` slot `new` — **direction**: a slot the task did not justify, on an existing UI at a moderate budget.
5. `radius` reported UNKNOWN — **project-context**: `tailwind.config.ts` states the radius scale explicitly.

## 9. Regressions to propose

1. Query: *"Front desk on a tablet: the appointment chips are too small to tap."* against a SvelteKit/Tailwind web project. Expect: records whose platform is `web` or `desktop` are **not** filtered out when the resolved platform is `tablet`; `anti-hover-only-actions` should be reachable.
2. Same query. Expect: `privacy.shared_device` / `privacy.sensitive_masking` are **not** critical required concepts when the request is a touch-target defect and the only privacy evidence is a `healthcare` product hint.
3. Query: any touch task on a screen with drag-based interaction. Expect: a gesture-discoverability concept is delivered alongside `touch.minimum_target`.
4. Direction on an existing UI with `change_budget: moderate` and no metadata wording. Expect: `metadata` stays `preserved`, not `new`.

## 10. Tags

`skill-helped`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `preservation-ok`
