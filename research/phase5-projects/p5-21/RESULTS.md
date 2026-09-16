# p5-21 — "Add a weekly summary card to the top of the Today screen."

- **Task:** p5-21 · sentence run verbatim.
- **Project / stack / platform:** `p5-swiftui-habits` ("Streaks") · SwiftUI, iOS 17 · **mobile**.
- **Existing UI or new screen:** existing screen (`Views/TodayView.swift`), new component added to it (`Components/WeeklySummaryCard.swift`).
- **Build hash:** start `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` = end (identical; nothing under `design-engineering/` was touched).
- **Render mode:** `html-twin` (no Xcode). `project/render/twin.html` Today section updated to mirror the Swift change; Playwright 1.63.0 screenshots at 390×844 @2x, light and `?theme=dark`. Swift additionally static-reviewed.
- **p5-20 boundary:** `StatsView.swift`, the `chartTrack` token and its colorset were not modified. The new card *reads* `theme.color.chartTrack` for its mini-ring tracks (see Implementation).

## Design-context table (`01-inspect.json`)

Same fixture as p5-20; the inspector output is identical.

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | bottom-tabs | KNOWN | `TabView` with 4 tabs, each owning a `NavigationStack` | yes |
| theme | dual-theme | INFERRED ("hex palette: 0 near-white, 0 near-black") | explicit dual theme via `Color(light:dark:)` + light/dark colorsets | partial — value right, evidence wrong (Swift `0xRRGGBB` hex not parsed) |
| surfaces | elevated | INFERRED | elevated cards (`cardSurface`: surface + shadow 0.08/16/6) | yes |
| radius | medium ("most common radius 8 (1×)") | INFERRED | 16 global, 10 chips (`Theme.Shape`) | partial — label acceptable, evidence is one twin value |
| spacing | 4 ("[2, 4, 12, 16]") | INFERRED | 4-pt base, scale 4/8/12/16/24 | yes |
| typography | humanist-sans, Nunito (1 ref) | INFERRED | Nunito via `Theme.Typography`, `.rounded` fallback | yes |
| components | unknown | UNKNOWN | `Components/HabitCard`, `ProgressRing`, `PrimaryButton`; `StatTile` in StatsView | partial (UNKNOWN while the code is clear) |
| product | ecommerce (README) | KNOWN | habit tracker (README line 1) | **no** — confident wrong value; this time it did real damage (see Guidance and Direction) |

## Requirements verdict (`02-requirements.json`)

| item | resolved | expectation | verdict |
|---|---|---|---|
| platform | mobile (Package.swift iOS target) | mobile | correct |
| artifact_state | existing | existing | correct |
| operations | create | create | correct |
| problem_domain | [] | (none — it is a feature request) | acceptable |
| change_scope | screen | screen | correct |
| mode | create ("build/create request on an existing surface") | create | correct |
| scope.kind | in-scope, "UI design / interaction task" | in-scope | correct |
| change_budget | moderate | low–moderate (one new component, one insertion) | acceptable |
| intent.preserve | [] | navigation, theme, typography | partial — `constraints.preserve_existing_system: true` but nothing named |
| screen / components | [] / [card] | screen=today/home, component=card + KPI/summary | partial — "card" found; "weekly summary" (a KPI/summary) and "Today screen" produced nothing |
| product (project_context) | ecommerce | habit tracker | **wrong**, and this time load-bearing |

## Guidance verdict (`03-guidance.md/json`; bundle 6 = core 4 + guardrails 2, ≈1197 tokens, "concepts required 1.0 covered (1/1)")

| record | kind | verdict | BAD category | note |
|---|---|---|---|---|
| `comp-product-detail-page` | core | off-target | `contradicts-codebase` | Top core record (lexical 0.464 on "card"/"top"?, product=ecommerce). A PDP for a habit tracker's Today screen. |
| `comp-checkout-one-page` | core | off-target | `contradicts-codebase` | "Order summary … at the top on phones" — the word *summary* plus the ecommerce tag pulled in checkout. |
| `surface-elevated-cards` | core | relevant | — | "never nest a card inside a card; the whole card is the target with a single accessible name" — applied (sibling card, one accessibility element). |
| `nav-bottom-tabs` | core | partial | — | Correct context; preservation note only. |
| `a11y-modal-dialog` | guardrail | off-target | `generic` | No dialog anywhere in the task. Chosen to cover the "interaction" concern. |
| `mobile-safe-areas` | guardrail | off-target | `generic` | Card sits inside the existing `ScrollView`/`NavigationStack`; insets already handled. |
| *(bundle as a whole)* | — | — | `missing-critical` | No KPI/summary record (`comp-kpi-tile` exists and ranks #2 for "KPI summary card at the top of the home screen"), no hierarchy record (`layout-hierarchy-one-thing` exists), no reuse record (`impl-reuse-before-new` was a candidate and dropped). |

Counts: relevant 1 · partial 1 · off-target 4.

Omitted: `comp-media-card`, `media-resume-and-details` (correctly). The trace shows `card-none` (0.446) and `anti-card-everything` (0.431) as candidates for `layout.no_nested_cards` and both dropped, while two ecommerce components (~600 tokens) were kept.

### Concept recall

Delivered concepts (union over the 6 selected records): `a11y.accessible_names`, `a11y.dialog_focus`, `feedback.confirmation_destructive`, `feedback.trust_signals`, `feedback.validation_errors`, `interaction.focus_restore`, `layout.one_primary_action`, `navigation.platform_grammar`, `perf.layout_shift`, `state.saving_conflict`, `touch.ime_keyboard`, `touch.minimum_target`, `touch.safe_areas`.

| expected id | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| `data.kpi_comparison` | yes | no | `expected-concepts` — never demanded; carried by `comp-kpi-tile`, `chart-progress-gauge`, `chart-compare-bar` (not a knowledge gap) |
| `process.reuse_first` | yes | no | `bundle-selection` — demanded (recommended, "existing repository"), candidate `impl-reuse-before-new` 0.243, dropped |
| `layout.focal_hierarchy` | yes | no | `expected-concepts` — never demanded; `layout-hierarchy-one-thing` exists |
| `layout.no_nested_cards` | no | no | `bundle-selection` — demanded ("cards"), candidates `card-none` 0.446 / `anti-card-everything` 0.431, dropped |
| `a11y.accessible_names` | no | **yes** | — (delivered by `comp-product-detail-page`, an off-target record; the concept still arrived) |
| `brand.token_layers` | no | no | `expected-concepts` — never demanded; `color-semantic-tokens` exists |
| `env.glanceable_status` | no | no | `expected-concepts` — never demanded; only `mobile-field-use` carries it (a weak carrier: knowledge is thin, but not absent) |

**Recall 1/7 = 0.14 · critical recall 0/3 = 0.00.** The single "required" concept the skill chose (`touch.minimum_target`) is a mobile baseline, not a task concept, and the reported "required 1.0 covered" measures coverage of that one-item list.

## Direction verdict (`04-direction.md/json`; exit 3 PARTIAL, `validation: VIOLATIONS`)

| slot | choice | status | justified? |
|---|---|---|---|
| navigation | bottom-tabs | preserved | yes |
| surface | elevated cards | preserved | yes |
| typography | humanist-sans | preserved | yes |
| color | neutral + accent, dual theme | preserved | yes |
| density | 4 → `density-medium` ("8 px base") | changed | **no** — nothing in the task touches density; the codebase is a 4-pt base with an 8 rhythm and stays that way |
| layout | `layout-grid-catalog` | new | **no** — ecommerce-driven; Today is a single column |
| cards | `card-poster-landscape` (16:9 media cards) | new | **no** — the validator itself flags "non-media product: poster card geometry selected" |
| cta | `cta-sticky-bar` | new | **no** — no CTA in the task |
| imagery | `imagery-poster` | new | **no** — no imagery |
| motion | `motion-spring` | new | coincidentally fine (`ProgressRing` already uses `.spring`) |
| focus | touch-only | new | fine |
| icon | filled system icons | new | fine (SF Symbols `.fill` already used) |
| metadata | moderate | new | harmless |

Preserved 4 · changed 1 (unjustified) · new 8, of which 4 wrong. The compatibility engine even rejected `card-none`/`card-list-row` as "incompatible with surface-elevated-cards" while accepting poster cards for a habit tracker. Root cause is the `ecommerce` product tag flowing into every slot's product fit. The per-slot text that was usable: surface ("never nest a card in a card; whole card one accessible name"), color ("validate every pair").

## Implementation

Files changed (before-copies in `before/`):

- `Sources/Streaks/Components/WeeklySummaryCard.swift` — **new**. Takes plain data (`days: [DailyCompletion]`, `completed`, `total`) like `HabitCard` takes a `Habit`. `ViewThatFits(in: .horizontal)`: one row (`summary | Spacer | strip`) at default type sizes, stacked fallback at large Dynamic Type. `summary` = `title2` "71%" (`.monospacedDigit()`) over `caption` "This week · 25 of 35". `strip` = seven `DayRing`s (20 pt ring, 3 pt stroke, trim = day ratio, checkmark at 100%, day initial beneath). Uses `theme.font.*`, `theme.spacing.*`, `.cardSurface(theme)`; no literal colours, radii or sizes outside the ring geometry. `accessibilityElement(children: .ignore)` + label "This week" + value "71 percent of habits done, 25 of 35. Mon 4 of 5, …" so VoiceOver gets one element with the per-day counts (the strip is not colour-only: arc length carries the ratio, and the text carries the numbers).
- `Sources/Streaks/Views/TodayView.swift` — `weeklySummary` inserted as the first child of the existing `VStack(spacing: xl)`; header and habit list untouched.
- `Sources/Streaks/Models/Store.swift` — `weeklyCompletedCount` / `weeklyTotalCount` extracted; `weeklyCompletionRate` now uses them (same value).
- `Tests/StreaksTests/StoreTests.swift` — `testWeeklyCounts` (25 / 35 / 0.714).
- `README.md` — layout listing (component + TodayView line).
- `render/twin.html` — `.week-card` / `.week-strip` CSS and the card markup at the top of the Today `.content`; `--chart-track` token already existed from p5-20.

Design decisions taken from the code, not from the skill: reuse `store.weeklyCompletions` (the Stats "This week" data) rather than invent a model; week-to-date, no "vs last week" (no data exists); keep the card ~80 pt so the progress ring stays the focal point; mini rings reuse the ring language rather than introduce bars on Today; track colour is `chartTrack` (dark 3.2:1 on surface) because `accentSoft` (dark 1.33:1) makes an empty day vanish — exactly the p5-20 defect, reused rather than re-fixed. `ProgressRing` itself still uses `accentSoft` for its track; changing it is outside this sentence and is noted as follow-up. No "today" marker in the strip: `Store` is a deterministic fixture with no notion of the current weekday, and adding `Calendar.current` would break the fixture's determinism.

Guidance used: `surface-elevated-cards` (sibling card, not nested; one accessible name). Ignored: `comp-product-detail-page`, `comp-checkout-one-page` (wrong product), `a11y-modal-dialog` (no dialog), `mobile-safe-areas` (already handled by the container), the direction's grid/poster/sticky-bar/density slots (all wrong for this screen).

Static review of the Swift: `ViewThatFits` iOS 16+ (project is iOS 17); `Text(Substring)` uses the `StringProtocol` initializer; `.monospacedDigit()` iOS 15+; `DailyCompletion` is `Identifiable` so `ForEach(days)` is fine; `Store` derived properties are non-mutating and `@MainActor` like the rest. Not compiled (no Xcode) — `tooling-limit`.

## Renders and defects

- `render/first-today-light.png`, `render/first-today-dark.png`, `render/first-today-weekcard-*.png` — first implementation (two-row card: headline + caption row, then a 24 pt ring strip).
- `render/final-today-light.png`, `render/final-today-dark.png`, `render/final-today-weekcard-*.png` — after iteration 1.
- `render/twin-first.html`, `render/twin-final.html` — the twin at each render.

**First render** (measured by the probe in `shoot.js`): week card 140 px tall, header at y=280, "Habits" label at y=562, first habit at y=597 → two stacked cards of near-equal visual weight above the ring and only two habit rows visible. Defects: **visual 1** (card too tall; competes with the ring and pushes the list). **accessibility 1**: dark mini-ring track was `accentSoft` (`rgb(74,42,34)` on `rgb(30,28,26)`, 1.33:1) — a 0/5 day would be invisible in dark mode. interaction 0, platform 0, existing-system-mismatch 0, implementation-bug 0.

**Iteration 1:** single-row layout (`ViewThatFits`), 20 pt rings, `chartTrack` track. Final probe: week card **80 px**, header at y=220, "Habits" at y=502, first habit at y=537 (three rows reach the tab bar); dark track `rgb(142,97,82)` = 3.2:1. Nunito rendered; rate 22 px; surface/accent tokens match the palette.

**Final defects:** accessibility 1 remaining — light-mode track is `#FFE7E0` on white (1.18:1), inherited from the system's light `accentSoft`/`chartTrack` values (the big ring and the Stats chart have the same light value; p5-20 recorded it as follow-up). A partially-filled day is still visible in light mode through the accent arc; an empty day would show only a faint ring. Not fixed here because the fix is a light-value change to the p5-20 token. Everything else 0. **Iterations: 1.**

## Preservation verdict

Navigation ✓ · theme ✓ (no token added or changed; one existing token reused) · typography ✓ (`theme.font.title2/caption`) · component reuse ✓ (`cardSurface`, `Theme.Spacing`, ring language from `ProgressRing`, data from `Store.weeklyCompletions`) · unjustified structural changes 0. Routes, tab state, `HabitCard`, the header card, `StatsView`, existing tests: untouched.

## Skill misses by earliest wrong layer

1. **requirements / context-detection** — product `ecommerce` from a habit-tracker README (confident wrong). In p5-20 it only filtered records; here it *selected* the two top core records (PDP, checkout) and four wrong direction slots (grid catalog, poster cards, sticky bar, poster imagery). One layer: `requirements` (the value entered the request as KNOWN and was never questioned by the sentence's own evidence: "habits", "Today").
2. **requirements** — "weekly summary" not recognised as a KPI/summary component; screen "Today" not recognised.
3. **expected-concepts** — `data.kpi_comparison` (critical), `layout.focal_hierarchy` (critical), `brand.token_layers`, `env.glanceable_status` never demanded.
4. **bundle-selection** — `process.reuse_first` (critical) and `layout.no_nested_cards` had candidates and were dropped in favour of ~600 tokens of ecommerce components and two generic guardrails.
5. **direction** — density changed without justification; validator reported a violation but still emitted the slot.
6. **context-detection** — theme evidence / radius evidence / components UNKNOWN (same as p5-20).

## Skill effect: **hurt** (mildly)

One usable line (`surface-elevated-cards`) that the codebase already embodies; two-thirds of the bundle and half the direction slots were for a shop. Following the guidance literally would have produced a poster-card catalog grid with a sticky action bar on a habit tracker's Today screen. The cost was reading and discarding ≈1.2k tokens of guidance plus a direction file that had to be reconciled slot by slot; the design came from the codebase.

## Regressions to propose

1. Query: `Add a weekly summary card to the top of the Today screen.` with the `p5-swiftui-habits` inspect JSON — expect `comp-kpi-tile` (or a summary-card record) in core, `impl-reuse-before-new` and a no-nested-cards record in guardrails, `comp-product-detail-page` / `comp-checkout-one-page` absent; required concepts include `data.kpi_comparison` and `layout.focal_hierarchy`.
2. Inspect fixture `p5-swiftui-habits`: `product_hints` must not be `ecommerce` (README first line says "habit tracker"); a sentence containing "habits"/"Today" must down-weight a conflicting project product tag.
3. Direction on any non-media, non-ecommerce product with `surface-elevated-cards` preserved: cards slot must not resolve to `card-poster-*`; when validation reports a violation, the slot should fall back to the next compatible alternative or be marked unresolved instead of emitted.
4. Direction with change budget "moderate" and a task that does not mention density: density slot must stay preserved.
5. Query: `KPI summary card at the top of the home screen` (mobile) — already retrieves `comp-kpi-tile` at #2 in `search`; assert it survives into the `guidance` bundle.

## Tags

`requirements-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-hurt`, `preservation-ok`
