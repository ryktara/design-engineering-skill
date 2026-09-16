# p5-20 — "Stats screen in dark mode: the bars are barely visible."

- **Task:** p5-20 · sentence run verbatim.
- **Project / stack / platform:** `p5-swiftui-habits` ("Streaks") · SwiftUI + Swift Charts, iOS 17 · **mobile**.
- **Existing UI or new screen:** existing screen (`Views/StatsView.swift`), defect fix.
- **Build hash:** start `bf034323…5f0d8` = end `bf034323…5f0d8` (identical; nothing under `design-engineering/` was touched).
- **Render mode:** `html-twin` (no Xcode on this machine). The project twin only had Today + Add Habit; I added a Stats section that mirrors `StatsView.swift` (palette values from `Theme/AppTheme.swift`, radius 16/5/10, spacing 16/12/8/4, `Chart.frame(height:160)`, 2×2 `LazyVGrid`) **before** changing anything, so the first render shows the real defect. Swift changes are additionally static-reviewed.

## Root cause (from code, before running the skill)

`StatsView.weeklyChart` draws the per-day **Total** `BarMark` with `theme.color.accentSoft`. That token is designed as a chip / ring-track tint; its dark value `#4A2A22` sits on the dark card surface `#1E1C1A` at **1.33:1** (WCAG). The **Completed** mark (`accent`, `#FF8A6E`) is 7.37:1 and fine. So "the bars are barely visible" = the total/track bars. Light mode's track is 1.18:1 vs white — also below the 3:1 non-text threshold, but the sentence scopes dark mode and the pale tint reads as a track there; I preserved it.

Second, theme-independent finding from static review: two `BarMark`s at the same x stack by default in Swift Charts (`MarkStackingMethod.standard`), so the total mark sits *under* the completed mark and every bar reaches total + completed instead of the track sitting behind the completed portion. The pre-fix twin mirrors that stacking (inferred from the framework default; not verifiable here — see `tooling-limit`).

Contrast measured from palette values (WCAG 2.x relative luminance):

| Pair | Before | After |
|---|---|---|
| dark track vs card surface `#1E1C1A` | `#4A2A22` **1.33:1** | `#8E6152` **3.22:1** (passes 1.4.11 ≥3:1) |
| dark track vs page background `#121110` | 1.48:1 | 3.58:1 |
| dark track vs completed bar `#FF8A6E` | 4.97:1 (but track itself invisible) | 2.29:1 (unavoidable: no colour is ≥3:1 from both `#1E1C1A` and `#FF8A6E`; saturation difference carries the rest) |
| dark completed vs surface | 7.37:1 | 7.37:1 (unchanged) |
| light track vs surface `#FFFFFF` | 1.18:1 | 1.18:1 (unchanged by choice; noted as follow-up) |

Computed colours in the twin at render time confirmed: dark track `rgb(74,42,34)` → `rgb(142,97,82)`, surface `rgb(30,28,26)`.

## Design-context table (`01-inspect.json`)

| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| navigation | bottom-tabs | KNOWN | `TabView` with 4 tabs, each owning a `NavigationStack` | yes |
| theme | dual-theme | INFERRED ("hex palette: 0 near-white, 0 near-black") | explicit dual theme: `Color(light:dark:)` for every token + light/dark colorsets; palette has `#FFFFFF` and `#121110` | partial — value right, but the code is explicit and the hex evidence is wrong (the Swift `0xRRGGBB` form is not parsed) |
| surfaces | elevated | INFERRED | elevated cards (`cardSurface`: surface + shadow 0.08/16/6) | yes |
| radius | medium ("most common radius 8 (1×)") | INFERRED | 16 global, 10 chips (defined once in `Theme.Shape`); the "8" is one `border-radius: 8px` in the twin | partial — label acceptable, evidence wrong |
| spacing | 4 ("most used [2,4,12,16]") | INFERRED | 4-pt base, scale 4/8/12/16/24 in `Theme.Spacing` | yes |
| typography | humanist-sans, Nunito (1 ref) | INFERRED | Nunito via `Theme.Typography` with `.rounded` system fallback | yes |
| components | unknown | UNKNOWN | `Components/HabitCard`, `ProgressRing`, `PrimaryButton`; `StatTile` in StatsView | partial (UNKNOWN while the code is clear) |
| product | ecommerce (README) | KNOWN | habit tracker (README first line: "A small SwiftUI habit tracker") | **no** — confident wrong value; downstream it caused `comp-kpi-tile` and `color-dark-accent` to be rejected as "product-specific vs ['ecommerce']" |

## Requirements verdict (`02-requirements.json`)

| item | resolved | expectation | verdict |
|---|---|---|---|
| platform | mobile (from project: Package.swift iOS target) | mobile | correct |
| artifact_state | existing | existing | correct |
| operations | diagnose, modify | diagnose + modify | correct |
| problem_domain | visual, design-system | visual / accessibility (contrast) / design-system | partial — accessibility not named although `accessibility.contrast: true` is set as a generic mobile baseline |
| change_scope | screen | screen (one chart mark + one token) | correct |
| mode | polish, audit | accessibility / polish / refactor | acceptable — polish is in the set; the sharper mode (accessibility: a contrast defect) was not recognised; "audit: diagnose first" is harmless |
| scope.kind | in-scope, "UI design / interaction task" | in-scope | correct |
| change_budget | low | low | correct |
| intent.preserve | [] | navigation, theme, typography | partial — nothing listed, though `constraints.preserve_existing_system: true` |
| screen / components | [] / [] | screen=stats/dashboard, component=chart | **miss** — "Stats screen" and "bars" produced no screen or component; this is the root of the chart-record filtering below |
| project_context | as in the table above | — | product wrong; rest acceptable |

## Guidance verdict (`03-guidance.md/json`, bundle 8 = core 2 + guardrails 6, ≈952 tokens, "concepts required 1.0 covered (4/4)")

| record | kind | verdict | BAD category | note |
|---|---|---|---|---|
| `cta-sticky-bar` | core | off-target | `generic` | Selected as "highest-scoring pattern with lexical evidence" (lexical 0.154): the word **bars** matched a sticky action **bar**. Stats has no CTA. |
| `nav-bottom-tabs` | core | partial | — | Right context (bottom tabs, each tab its own stack), but the task is not navigation; only useful as a preservation note. |
| `anti-dark-mode-inversion` | guardrail | relevant | — | "define dark chart palettes … re-validate every pair" is the fix direction. |
| `color-dark-mode-rules` | guardrail | relevant | — | Same concept as the previous record ("charts get a dark palette; re-validate every contrast pair"); redundancy 0.46. |
| `typo-measure-and-rhythm` | guardrail | off-target | `generic` | Line length / heading rhythm; nothing to do with a bar's contrast. Chosen to cover `layout.focal_hierarchy`, which this task never needed. |
| `layout-spacing-scale` | guardrail | off-target | `generic` | Spacing guidance for a contrast defect. |
| `a11y-target-size` | guardrail | off-target | `generic` | No touch target is involved. |
| `impl-reuse-before-new` | guardrail | partial | — | Generic but actually applied: extend the existing token layer (Palette + colorset) rather than a literal colour in the view. |
| *(bundle as a whole)* | — | — | `missing-critical` | No record states the non-text 3:1 requirement (`a11y-nontext-contrast` exists in `rules.jsonl` and was never a candidate). |

Omitted set is telling: `chart-compare-bar`, `chart-composition` ("chart record outside a data-visualisation task"), `comp-kpi-tile` and `color-dark-accent` ("product-specific vs ['ecommerce']"). The sentence *is* about a chart on a stats screen; the omission reasons follow from the requirements miss (no chart component) and the wrong product tag.

Counts: relevant 2 · partial 2 · off-target 4.

### Concept recall

Delivered concepts (union over selected records): `navigation.platform_grammar`, `brand.dark_mode_redesign`, `content.readable_measure`, `layout.focal_hierarchy`, `layout.spacing_scale`, `touch.minimum_target`, `process.reuse_first`.

| expected id | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| `a11y.contrast` | yes | no | `expected-concepts` — never demanded (trace has no entry); `a11y-nontext-contrast` / `a11y-contrast-text` exist in the base, so not a knowledge gap |
| `brand.token_layers` | yes | no | `expected-concepts` — never demanded; `color-semantic-tokens` ranked #3 in `search` (0.363) but was not a bundle candidate because no concept asked for it |
| `brand.dark_mode_redesign` | no | **yes** | — |
| `process.safe_modification` | no | no | `bundle-selection` — demanded (recommended), candidate `impl-safe-modification` 0.254, dropped ("bundle cap or lower utility") while four generic guardrails were kept |
| `process.render_verify` | no | no | `expected-concepts` — never demanded; `verify-render-and-inspect` exists |
| `a11y.color_not_only` | no | no | `expected-concepts` — never demanded; upstream cause is the requirements miss (no chart component → no chart concern); `a11y-color-not-only`, `chart-accessible-colour`, `comp-chart-container` exist |

**Recall 1/6 = 0.17 · critical recall 0/2 = 0.00.** Required concepts the skill chose instead (`layout.spacing_scale`, `layout.focal_hierarchy`, `process.reuse_first`, `touch.minimum_target`) are the generic "polish on mobile" set; the reported "required 1.0 covered" measures coverage of the wrong list.

## Direction verdict (`04-direction.md/json`)

All 13 slots **preserved**, none changed, none new; budget low; `validation: OK`, no violations. Every preserved slot is justified (the task changes one chart colour). The color-slot text ("Charts get their own categorical palette. Validate every pair with tokens.py") is the one line that points at the actual fix. Fingerprint (bottom-tabs / elevated / medium radius / humanist-sans / neutral-plus-accent) matches the codebase. Nothing to disagree with; also nothing task-specific.

## Implementation

Files changed (before-copies in `before/`):

- `Sources/Streaks/Theme/AppTheme.swift` — new semantic token `Palette.chartTrack = Color(light: #FFE7E0, dark: #8E6152)` with a doc comment stating the 3.2:1 rationale. `accentSoft` untouched (still used by icon chips and the progress-ring track, where it is a background behind an accent glyph and fine).
- `Sources/Streaks/Views/StatsView.swift` — Total mark uses `theme.color.chartTrack`; both marks get `stacking: .unstacked` so the completed bar overlays the track on a shared baseline (comment explains the default stacking).
- `Sources/Streaks/Assets.xcassets/Colors/ChartTrack.colorset/Contents.json` — new, mirroring the token (project rule: every colour defined once in Palette and mirrored in the catalog).
- `README.md` — palette table row `chartTrack`; twin description now lists Stats.
- `render/twin.html` — Stats section added (pre-fix state kept as `p5-20/render/twin-first.html`); `--chart-track` token in both themes; overlay chart.

Guidance used: `color-dark-mode-rules` / `anti-dark-mode-inversion` ("charts get a dark palette; re-validate every pair") and `impl-reuse-before-new` (extend the token layer). Ignored: `cta-sticky-bar`, `typo-measure-and-rhythm`, `layout-spacing-scale`, `a11y-target-size` (irrelevant to a contrast defect). Supplied by me, not by the skill: the 3:1 non-text threshold, the measurement, the choice not to repaint `accentSoft`, and the stacking fix.

Unchanged: routes/tabs, `Store`, tests (`StoreTests` do not touch the view), accessibility (`StatTile` `.accessibilityElement(children: .combine)` kept), fonts, radii, spacing.

## Renders and defects

- `render/first-stats-dark.png`, `render/first-stats-chart-dark.png` (pre-fix, 390×844 @2x, `?theme=dark`), `render/first-stats-light.png` for reference.
- `render/final-stats-dark.png`, `render/final-stats-chart-dark.png`, `render/final-stats-light.png`.

First render (pre-fix, faithful twin): **visual 1** (track bars at 1.33:1 read as a murky plinth on the dark card — the reported defect), **implementation-bug 1** (default stacking sums total + completed; visible in both themes as a constant-height base under every bar).

Iteration 1 (fix applied, re-rendered): track visible, overlay correct, but my twin still scaled bar heights to the stacked maximum (10) so the plot sat in the lower half of the 160 px frame — a twin implementation-bug, not a project defect. Iteration 2: scale to max total (5); final render clean.

Final defects: none. **Iterations: 2.** Remaining, out of scope: light-mode track 1.18:1; the chart has no accessibility label/summary (`data.accessible_chart_alternative`).

## Preservation verdict

Navigation ✓ · theme ✓ (one token added, none changed) · typography ✓ · component reuse ✓ (`cardSurface`, `Theme.Shape`, `Theme.Spacing`) · unjustified structural changes 0. The `stacking: .unstacked` change alters chart geometry, which is beyond the literal sentence; it is justified because the intended "track behind completed" rendering is otherwise wrong in both themes, and it is one argument on the same two lines.

## Skill misses by earliest wrong layer

1. **requirements** — "Stats screen … the bars" produced `screen=[]`, `components=[]`; a chart component was never recognised, so chart records were filtered as "outside a data-visualisation task".
2. **requirements / context-detection** — product tagged `ecommerce` from a habit-tracker README (confident wrong); it rejected `comp-kpi-tile` and `color-dark-accent`.
3. **mode** — accessibility (a contrast defect) not recognised; polish+audit is acceptable but blunter.
4. **expected-concepts** — `a11y.contrast` (critical), `brand.token_layers` (critical), `process.render_verify`, `a11y.color_not_only` never demanded.
5. **candidate-retrieval / ranking** — `cta-sticky-bar` became the top core record on a lexical hit of "bars".
6. **bundle-selection** — `impl-safe-modification` dropped in favour of generic polish guardrails.
7. **context-detection** — theme evidence wrong because Swift `0xRRGGBB` hex is not parsed; radius evidence from a single twin value; components UNKNOWN.

## Skill effect: **neutral**

The two dark-mode records point in the right direction ("dark chart palette, re-validate pairs") and match what the code already implied, but the bundle omitted the critical requirement (non-text 3:1), never mentioned tokens, and half of it (sticky bar, typography measure, spacing, target size) had to be ignored. The fix was fully derivable from the code and the palette table.

## Regressions to propose

1. Query: `Stats screen in dark mode: the bars are barely visible.` — expect `a11y.contrast` in required concepts (non-text ≥3:1 record selected), a chart component detected, `cta-sticky-bar` absent, mode includes accessibility.
2. Query: `the chart bars are hard to see in dark mode` — expect component=chart; `a11y-nontext-contrast` and `color-semantic-tokens` (or a chart-palette record) in the bundle; chart records not omitted as "outside a data-visualisation task".
3. Inspect fixture `p5-swiftui-habits`: product must not be `ecommerce`; theme evidence should count `#FFFFFF`/`#121110` from `Color(hex: 0x…)`; components should list `Components/*.swift`.
4. Lexical guard: the token "bar(s)" in a chart/stats context must not retrieve `cta-sticky-bar` / toolbar records.

## Tags

`requirements-miss`, `mode-miss`, `concept-miss`, `ranking-miss`, `context-detection-miss`, `render-defect-fixed`, `tooling-limit`, `skill-neutral`, `preservation-ok`
