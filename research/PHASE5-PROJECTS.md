# Phase 5 real-project qualification round (22 tasks, 12 codebases)

Protocol: `research/phase5-projects/PROTOCOL.md`; tasks: `TASKS.md`. Round c1 ran on frozen candidate c1 (`bf034323a2b68202…`, identical start/end hash in every task folder). Each task pre-registered its expectation (`00-expectation.json`) before any `advise` call, implemented the change, rendered it, and routed every skill miss to the earliest wrong layer. The fixes routed from the round produced candidate c2 (`50966e8e6184f317…`); c2 was re-scored mechanically against the same expectations (`evals/rescore_projects.py`, `research/runs/phase5-c2-projects-rescore.json`) and its bundles were judged by independent reviewers (`<task>/c2/review.json`, `research/runs/phase5-c2-projects-review.json`). No implementation was re-run on c2; c2's real-project evidence is therefore weaker than c1's and is labelled as such.

## Codebases

| codebase | stack | platform | origin |
|---|---|---|---|
| p3-nextjs-saas | Next.js 15 + Tailwind + shadcn-style | web | Phase 3 |
| p3-ecommerce-web | HTML/CSS/JS storefront | web | Phase 3 |
| p3-react-dashboard-polish | React (esbuild) dashboard | web | Phase 3 |
| p5-sveltekit-clinic | SvelteKit 2 + Svelte 5 + Tailwind (new, builds) | web | Phase 5 |
| p3-android-tv-compose | Jetpack Compose for TV | tv | Phase 3 |
| p3-tvos-swiftui | SwiftUI tvOS (SwiftPM) | tv | Phase 3 |
| p3-kiosk-pharmacy | HTML/CSS/JS 1080×1920 touch kiosk | kiosk | Phase 3 |
| p3-erp-desktop-dotnet | WPF .NET (capture harness) | desktop | Phase 3 |
| p3-winui-erp-audit | WinUI 3 | desktop | Phase 3 |
| p5-avalonia-fleet | C# / Avalonia 11 (new, `dotnet build` clean) | desktop | Phase 5 |
| p3-mobile-flutter-field | Flutter field app (dual theme) | mobile | Phase 3 |
| p5-swiftui-habits | SwiftUI iPhone app (new, dual theme) | mobile | Phase 5 |

Coverage: web 8 · TV/kiosk 5 · desktop-native 4 · mobile 5 · native stacks 13 · existing-UI modification 18 · new screen on an existing codebase 4 · intended PARTIAL scope 1 · audit 1; 16 of 22 sentences have no explicit mode verb.

## Per task (c1 implemented round; c2 re-scored)

| task | codebase | platform | sentence | c1 platform / scope / mode | c1 recall / critical | c1 effect | c2 platform / scope / mode | c2 recall / critical | c2 review vs c1 | c2 would have |
|---|---|---|---|---|---|---|---|---|---|---|
| p5-01 | p3-nextjs-saas | web | The invoices table on the billing page is hard to scan once there are more than twenty rows. | yes / ok / acceptable | 0.43 / 0.67 | neutral | yes / ok / acceptable | 0.571 / 0.667 | better | helped |
| p5-02 | p3-nextjs-saas | web | Add a team members page with an invite flow, consistent with the rest of the settings area. | yes / ok / yes | 0.43 / 0.33 | neutral | yes / ok / yes | 0.571 / 0.667 | better | helped |
| p5-03 | p3-ecommerce-web | web | Checkout on phones: the order summary pushes the pay button below the fold. | wrong / ok / yes | 0.571 / 0.333 | neutral | yes / ok / yes | 0.714 / 0.667 | better | neutral |
| p5-04 | p3-ecommerce-web | web | The product page never tells shoppers when it will arrive or that returns are free. | yes / ok / acceptable | 0.4 / 1.0 | neutral | yes / ok / acceptable | 0.6 / 1.0 | better | helped |
| p5-05 | p3-react-dashboard-polish | web | Keyboard users can't get to the chart filters. | yes / ok / yes | 0.83 / 1.0 | neutral | yes / ok / yes | 0.667 / 1.0 | better | helped |
| p5-06 | p5-sveltekit-clinic | web | The waiting room board: nothing tells the front desk how long each patient has been sitting there. | yes / MISS / acceptable | 0.0 / 0.0 | neutral | yes / ok / acceptable | 0.571 / 0.667 | better | helped |
| p5-07 | p5-sveltekit-clinic | web | Patient search that finds nothing just shows a blank area. | yes / ok / acceptable | 0.43 / 1.0 | helped | yes / ok / acceptable | 0.429 / 1.0 | better | neutral |
| p5-08 | p5-sveltekit-clinic | web | The appointments grid re-renders the whole day when one chip is dragged, so dragging stutters. | yes / MISS / yes | 0.29 / 0.33 | neutral | yes / ok / yes | 0.714 / 0.667 | better | helped |
| p5-09 | p3-android-tv-compose | tv | When you hold right on the remote the rail flies past too fast to read the titles. | yes / ok / acceptable | 0.8 / 1.0 | neutral | yes / ok / acceptable | 1.0 / 1.0 | better | helped |
| p5-10 | p3-android-tv-compose | tv | Add a subtitles and audio language chooser to the player. | yes / ok / yes | 0.71 / 0.67 | helped | yes / ok / yes | 1.0 / 1.0 | better | helped |
| p5-11 | p3-tvos-swiftui | tv | From the sofa nobody can tell which row is selected on the living-room screen. | yes / ok / acceptable | 0.43 / 0.5 | neutral | yes / ok / yes | 0.857 / 1.0 | same | neutral |
| p5-12 | p3-kiosk-pharmacy | kiosk | Older customers time out on the identify step before they finish typing. | wrong / ok / acceptable | 0.14 / 0.5 | neutral | yes / ok / yes | 0.714 / 1.0 | better | helped |
| p5-13 | p3-kiosk-pharmacy | kiosk | Add a Spanish language switch to the pick-up flow. | wrong / ok / yes | 0.0 / 0.0 | neutral | yes / ok / yes | 1.0 / 1.0 | better | helped |
| p5-14 | p3-erp-desktop-dotnet | desktop | Purchase-order lines: operators keep typing the quantity into the price column. | yes / ok / acceptable | 0.857 / 1.0 | neutral | yes / ok / acceptable | 0.714 / 1.0 | better | helped |
| p5-15 | p3-winui-erp-audit | desktop | Review the stock adjustments page against our accessibility checklist. | yes / ok / yes | 0.714 / 0.75 | neutral | yes / ok / yes | 1.0 / 1.0 | better | helped |
| p5-16 | p5-avalonia-fleet | desktop | Dispatchers want to see which vehicles are overdue for service without opening each one. | yes / MISS / acceptable | 0.0 / 0.0 | hurt | yes / ok / acceptable | 0.667 / 1.0 | better | helped |
| p5-17 | p5-avalonia-fleet | desktop | The dispatch job form lets you lose an unsaved job by clicking another one. | yes / ok / yes | 0.167 / 0.5 | helped | yes / ok / yes | 0.5 / 1.0 | better | helped |
| p5-18 | p3-mobile-flutter-field | mobile | Photos attached to a defect report are tiny thumbnails you can't check in the field. | yes / ok / acceptable | 0.43 / 0.5 | neutral | yes / ok / acceptable | 0.857 / 1.0 | better | helped |
| p5-19 | p3-mobile-flutter-field | mobile | Sync status is a spinner that never says what is happening. | yes / ok / acceptable | 0.29 / 0.25 | neutral | yes / ok / yes | 0.714 / 1.0 | better | helped |
| p5-20 | p5-swiftui-habits | mobile | Stats screen in dark mode: the bars are barely visible. | yes / ok / acceptable | 0.17 / 0.0 | neutral | yes / ok / yes | 0.333 / 0.0 | better | neutral |
| p5-21 | p5-swiftui-habits | mobile | Add a weekly summary card to the top of the Today screen. | yes / ok / yes | 0.14 / 0.0 | hurt | yes / ok / yes | 0.286 / 0.667 | better | helped |
| p5-22 | p5-swiftui-habits | mobile | Make the Add Habit sheet work when the keyboard is up. | yes / ok / no | 0.29 / 0.0 | hurt | yes / ok / yes | 0.429 / 0.5 | better | helped |

## Aggregates

| metric | c1 (implemented, frozen c1) | c2 (re-scored, frozen c2) |
|---|---|---|
| platform correct | {'yes': 19, 'wrong': 3} | {'yes': 22} |
| scope kind correct | {'True': 19, 'False': 3} | {'True': 22} |
| mode correct (yes / acceptable / no) | {'acceptable': 12, 'yes': 9, 'no': 1} | {'acceptable': 8, 'yes': 14} |
| artifact state correct | {'True': 21, 'False': 1} | {'True': 21, 'False': 1} |
| mean concept recall (against pre-registered expectations) | 0.387 | 0.678 |
| mean critical recall | 0.47 | 0.841 |
| tasks with full critical recall | 5 / 22 | 14 / 22 |
| tasks delivering a forbidden concept | 9 (c1 scorer) | 5 |
| empty bundles | 2 | 0 |
| mean bundle tokens | 955.6 | 1048.5 |
| guidance records relevant / partial / off-target (agent judged) | 32 / 50 / 47 | 56 / 39 / 46 |
| BAD guidance by category | {'off-platform': 6, 'wrong-mode': 1, 'generic': 36, 'contradicts-codebase': 14, 'missing-critical': 16, 'harmful': 0} | {'generic': 39, 'missing-critical': 6, 'contradicts-codebase': 8, 'off-platform': 2, 'wrong-mode': 1} |
| skill effect (c1: implementer; c2: reviewer estimate) | {'neutral': 16, 'helped': 3, 'hurt': 3} | would have: {'helped': 18, 'neutral': 4} |
| direction: unjustified structural change / unjustified slots | 0 structural; direction-mismatch tag on 20 tasks | 10 unjustified slots over 22 tasks |
| preservation (navigation / theme / typography / component reuse) | 22 / 22 / 22 / 22 | n/a (not re-implemented) |
| context detection yes/partial/no — navigation | {'yes': 21, 'partial': 1, 'no': 0, 'n': 22} | see c2 review notes |
| context detection — typography | {'yes': 4, 'partial': 17, 'no': 1, 'n': 22} | improved on WPF (system) and Avalonia (humanist); still partial elsewhere |
| context detection — surfaces | {'yes': 8, 'partial': 9, 'no': 5, 'n': 22} | bordered-flat now detected on Tailwind templates and Avalonia |
| first-render defects (c1) | {'visual': 18, 'interaction': 2, 'accessibility': 4, 'platform': 1, 'existing-system-mismatch': 1, 'implementation-bug': 5} | — |
| final defects (c1) | {'visual': 3, 'interaction': 0, 'accessibility': 1, 'platform': 0, 'existing-system-mismatch': 1, 'implementation-bug': 0} | — |
| iterations (c1) | 30 | — |
| misses by earliest layer (c1) | {'scope': 3, 'platform': 3, 'mode': 4, 'requirements': 28, 'concerns': 3, 'expected-concepts': 21, 'candidate-retrieval': 5, 'bundle-selection': 21, 'direction': 20, 'project-adaptation': 12} | — |
| concept misses by layer (c1) | {'expected-concepts': 61, 'candidate-retrieval': 4, 'bundle-selection': 23, 'knowledge-gap': 2} | — |

## What the round found (c1) and what c2 changed

- **Scope abstain on plain sentences (3 / 22, severe, systemic):** "Dispatchers want to see which vehicles are overdue…", "The waiting room board: nothing tells the front desk…" and the partial-scope drag sentence abstained or lost their split because no lexicon UI noun appeared. c2: with a repository supplied and no technical vocabulary the sentence is in scope; UX-symptom and UI vocab widened; `re-render*` + `stutters` yields PARTIAL_SCOPE. Decisive technical phrases still abstain (guarded by new cases).
- **Kiosk project read as web (2 / 22, severe, systemic):** the inspector saw only HTML. c2: README kiosk declaration makes kiosk the platform with web as substrate; environment hints (public, outdoor, gloves) enter requirements.
- **'on phones' overrode a web project (1 / 22):** c2 treats phone wording on a web project as a viewport (web + responsive).
- **Proper-noun create ('Add Habit sheet') and hardware-keyboard reading of 'keyboard is up' (1 / 22):** c2 rewrites screen names before cue matching and demands `touch.ime_keyboard` on mobile.
- **README product leaks (ecommerce on a habit tracker and a clinic; erp on a field app):** word-bounded product hints; media-only patterns rejected without a media signal.
- **Expected concepts never demanded (61 misses at that layer):** aliases and derivation rules for exceptions-first, unsaved-changes, dialog focus, progress feedback, i18n, soft keyboard, image sizing, KPI summary, track selection, pagination, drag alternatives, held D-pad pacing, readability.
- **Knowledge gaps with no carrier:** nine records added (skip link, D-pad hold pacing, background-work progress, drag and drop, exceptions first, column disambiguation, delivery promise, TV side sheet, full-size photo viewer) and five records corrected (empty concept lists on `cta-sticky-bar` and `metadata-rich`, TV/kiosk platforms on the modal-dialog rule, refresh timestamp on offline-sync, TV search concept moved to a TV record).
- **Direction 'new' slots contradicting the codebase (20 / 22 tasks):** c2 keeps unmentioned slots as implemented under moderate budgets on existing systems, preserves repository focus handling, never fills a slot with a media-only pattern without a media signal, and preserves density unless requested.
- **Still open after c2 (reviewer findings):** generic concern-filling guardrails (39 of 46 off-target records are `generic`), whole-product direction records reaching core with no lexical match, `process.reuse_first` dropped by the bundle cap in about a third of tasks, `a11y-skip-link` over-selected for the focus concern, context detection still partial for radius/spacing on token-based themes, one contradicts-codebase cluster (`desktop-fluent-materials` on a WPF app with its own tokens).
