# Phase 4 baseline (recorded before any Phase 4 change, 2026-09-09)

Source: `research/runs/phase4-baseline.json` (`python evals/release_check.py --heldout-v1 --heldout-v2 --projects --real-activation --json`), `research/benchmark-results.json`, `research/runs/phase3-output-size.json`, `research/runs/phase3-freeze.json`. Phase 3 artifacts are left untouched.

| Item | Value |
|---|---|
| records | 232 (pattern 88 · rule 63 · component 31 · antipattern 21 · direction 15 · chart 14) |
| concepts / concerns | 57 concept ids · 16 concerns · 87 records declaring concept ids |
| eval cases | development 181 · regression 32 · heldout v1 145 · heldout v2 212 · activation 180 |
| sha256 (first 16) | de_core.py `d2352454f5f5f095` · lexicon.json `1f01ba61cd5ad92c` · inspect_project.py `0c3c255c5fa03e8e` |
| validator | OK, 0 errors, 0 warnings |
| development + regression | 213 / 213 |
| activation proxy | precision 0.987 · recall 1.000 · FPR 0.014 · FNR 0.000 |
| real activation | SKIPPED (CLI not authenticated for non-interactive use) |
| performance | load 8 ms · search 186 ms (cold index) · direction 15 ms; benchmark warm search 3 ms, warm guidance 4 ms, cold 196 ms vs upstream 113 ms |
| output size (tokens ≈ chars/4) | guidance markdown mean 992 (p95 1218) · direction markdown mean 2282 (p95 2659) · bundle median 6 |
| benchmark v2 (18 queries) | relevant: upstream 0.200 · search k=5 0.902 · guidance 0.849; off-target: 0.189 · 0.134 · 0.157; empty 3 · 0 · 0 |

## Historical held-out v1 (145, non-blind)

acceptable 37 · mean concept recall 0.336 · mode correct 113 · platform correct 132 · off-target 0.181 · concern coverage 0.961 · bundle bytes 7213.

## Historical held-out v2 (212, inspected at class level in Phase 3; now non-blind)

acceptable 18 (8.5 %) · concept recall 0.206 · required-concern coverage 0.808 · off-target 0.159 · platform 201/212 · mode 129/212 (61 %) · abstain 14/20 · forbidden violations 7 · derived-required agreement 0.601 · thresholds met 3/8 (off-target, platform, empty).

## Torture tests (Phase 3, 9 projects)

74 first-render defects → 36 · 23 iterations · guidance 40 relevant / 18 partial / 6 off-target.

## Inspector behaviour at baseline

Detects stacks, platforms (Apple targets, leanback-only TV, plain HTML), UI libraries, CSS architecture, tokens (CSS variables, tailwind/shadcn config), fonts, routing dirs, component dirs, breakpoints, a11y/focus/D-pad handling, tests, i18n, README product hints. Does **not** detect navigation topology, theme polarity, surface/radius/spacing language, typography scale, or the layout shell; Flutter `ThemeData`/`go_router`, SwiftUI tokens, `next/font` are missed (Phase 3 torture findings).

## Known direction limitations at baseline

Direction slots are chosen from requirements and lexical fit only: a light-first codebase received a dark-first colour slot, a top-bar app received a left rail, a WPF grid received command-palette navigation, and polish tasks could replace typography/navigation. There is no change budget and no compatibility check against the existing system. Bundle selection covers concerns and concept ids but ignores record size and semantic contamination (a record entering for one concept while its other guidance is off-task).
