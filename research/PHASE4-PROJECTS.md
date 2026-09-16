# Phase 4 real-project round (15 tasks, 9 applications, 2026-09-09)

Source: `research/phase4-projects/<task>/RESULTS.md` + `artifacts.json`, aggregated by `release_check.py --projects` into `research/runs/phase4-projects-aggregate.json`. Protocol: `research/phase4-projects/PROTOCOL.md`. All 15 tasks worked on the real Phase 3 codebases; 15 / 15 are classified `existing_ui` by the agents (11 modify an existing interface, 4 add a screen inside an existing app). Agents could not modify the skill.

| Task | Project · stack | Mode / budget (skill) | Render | First → final defects | Iter. | Guidance rel/part/off |
|---|---|---|---|---|---|---|
| p4-01 billing polish | Next.js + shadcn | polish / low | native | 2 → 0 | 2 | 7/1/0 |
| p4-02 seat table a11y | Next.js + shadcn | accessibility / low | native | 0 → 0 | 1 | 5/1/1 |
| p4-03 shortcuts + command bar | WinUI 3 | create / moderate | html-twin | 2 → 0 | 2 | 4/2/2 |
| p4-04 compare-to-last-week | React dashboard | create / moderate | native | 2 → 0 | 2 | 4/2/1 |
| p4-05 exceptions first | React dashboard | audit / moderate | native | 3 → 1 | 2 | 2/2/2 |
| p4-06 listing page + filters | HTML store | create / moderate | html | 1 → 1 | 2 | 5/1/1 |
| p4-07 WPF polish | WPF .NET 10 | polish / low | native | 3 → 0 | 2 | 4/2/2 |
| p4-08 column-defaults dialog | WPF .NET 10 | create / moderate | native | 2 → 0 | 3 | 3/2/3 |
| p4-09 kiosk identify a11y | HTML kiosk | accessibility / low | html | 11 → 0 | 2 | 1/2/2 |
| p4-10 focus restoration | Compose TV | audit / moderate | html-twin + static | 5 → 0 | 3 | 4/2/2 |
| p4-11 match details | Compose TV | create / moderate | html-twin | 5 → 0 | 3 | 5/2/1 |
| p4-12 tvOS search | SwiftUI tvOS | create / moderate | html-twin | 4 → 0 | 3 | 2/3/3 |
| p4-13 form with keyboard open | Flutter | refactor / moderate | html-twin + static | 2 → 0 | 2 | 3/2/4* |
| p4-14 settings screen | Flutter | create / moderate | html-twin + static | 1 → 0 | 2 | 3/2/3* |
| p4-15 kiosk chooser | HTML kiosk | create / moderate | html | 2 → 0 | 2 | 3/1/2 |

\* before the D-pad regex fix; the TV records in those bundles came from the `AnimatedPadding` false positive.

## Aggregates

- Defects by type, first → final: visual 11 → 6, interaction 3 → 0, accessibility 2 → 0, platform 4 → 2, existing-system mismatch 3 → 2, implementation bug 7 → 0 (32 iterations).
- Guidance verdicts: 55 relevant / 27 partial / 27 off-target (27 % off-target; Phase 3: 9 %). The off-target share is dominated by three causes fixed after the round: the Flutter→TV inspector false positive (2 tasks), reference clauses read as targets (3 tasks), and category-specific rules entering on concern gain (fixed by category contamination).
- Design-context detection (agent judgement, detected vs actual): navigation 7 yes / 8 partial / 0 no; theme 13 / 1 / 1; typography 1 / 5 / 9; surfaces 5 / 2 / 8; spacing 6 / 3 / 6. Navigation and theme are usable; typography, surfaces and spacing were mostly wrong or unknown before the parser fixes (CSS variables, Tailwind classes, rem, Flutter/XAML declarations, `elevation: 0`).
- Preservation (result judged by the agent): navigation 15 / 15, theme 15 / 15, typography 15 / 15, component reuse 15 / 15; unjustified structural change 0. In every polish/refactor/audit task the delivered UI kept the existing system; the direction's preserved slots held, and where unpreserved slots drifted (table-first layout for a settings page, dashboard grid for a WPF polish, poster cards for a store) the agent ignored them — this is why the low-budget "slots the task does not mention stay as implemented" rule was added.
- Misses by earliest wrong layer (agent-assigned): requirements 18, bundle-selection 17, expected-concepts 16, direction 15, project-adaptation 15, candidate-retrieval 5, concerns 3, mode 2, scope 1. Scope and mode — the Phase 3 blockers — were almost never the wrong layer on real tasks.

## Class fixes derived from the round (all with regression cases, `evals/regression/guidance.json`)

1. `AnimatedPadding` matched the D-pad regex → Flutter tagged TV (`reg-animatedpadding-is-not-dpad`; fixture carries the widget).
2. Kiosk/TV requests on web-technology projects raised a platform conflict → AMBIGUOUS (`reg-kiosk-on-web-not-conflict`).
3. Reference clauses ("without changing its navigation", "matching the existing checkout pages", "consistent with the existing dark rails home") became build targets (`reg-negative-clause-not-target`, `reg-matching-existing-pages-not-targets`).
4. Preservation phrases ("keeping the existing top bar and light theme", "in its existing style", "without redesigning it", "its theme") not captured (`reg-keeping-existing-is-preserve`, `reg-alerts-need-live-status`).
5. "KPI" → finance product (`reg-keeping-existing-is-preserve`).
6. Alerts tasks lacked live-status / one-primary-action / exception-first concepts (`reg-alerts-need-live-status`).
7. "validation errors are hard to read" demanded no validation or contrast concept; low-budget direction proposed layouts for a polish (`reg-polish-validation-readability`).
8. Consistency polish in an existing repository had no "reuse the project's primitives" guidance (`reg-polish-in-existing-reuses-primitives`).
9. Knowledge gaps seen twice (Phase 3 + Phase 4): desktop status bar with next-error navigation, kiosk on-screen keypad, photo capture field → three records with sources and development cases.

## Still open after the round

- Typography detection for style-resource XAML, Compose `Typography(...)`, SwiftUI `Font.system`; component directories on native stacks.
- "Hoist place state above the screen" (TV focus restoration in Compose) and focus-lift reservation at the safe edge: seen twice on TV, not yet a record (needs a source beyond our own projects).
- tvOS system keyboard / `.searchable` model; segmented control / view switch; dashboard exception strip as a component; kiosk language chooser.
- Two agents re-ran their skill commands after the mid-round edits; one task (p4-10) lost `screen=home` because "without changing the home layout" is now a reference clause — acceptable (the target is the rail) but recorded.
- No Kotlin/Swift/Flutter compilers: native TV/mobile code remains statically reviewed and rendered through HTML twins.
