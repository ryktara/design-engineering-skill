# Phase 6 baseline (recorded 2026-09-10, before any Phase 6 change)

Source: `research/runs/phase6-baseline.json` (assembled from the Phase 5 final artifacts plus an idle rerun of the deterministic gates on the unchanged build). Nothing from Phase 5 was overwritten.

| item | value |
|---|---|
| build (Phase 5 candidate c2) | sha256 `50966e8e6184f317…` (unchanged; verified with `evals/build_hash.py`) |
| records / concepts / alias groups / concerns | 247 · 114 · 60 · 16 |
| development / regression cases | 575 · 40 — 615 / 615 passing |
| activation proxy | precision 1.000 · recall 1.000 · FPR 0.000 · FNR 0.000; real activation SKIPPED |
| performance (idle gates) | load 8 ms · search 224 ms · direction 158 ms |
| benchmark v2 (idle) | relevant 0.200 / 0.915 / 0.927 (upstream / search / bundle); off-target 0.189 / 0.111 / 0.106; cold median 359 / 815 ms; warm 193 / 297 ms |
| output size (239 queries) | guidance md mean 1045 · median 1055 · p95 1370 tokens; bundle size mean 6.32 / p95 8; bundle tokens mean 950 / p95 1335 |

## Historical held-out sets (all non-blind from now on; trend only)

| set | passed / total | key numbers |
|---|---|---|
| v1 (145) | 34 / 145 | recall 0.369 · mode 106 · platform 122 · empty 7 |
| v2 (212) | 29 / 212 | recall 0.232 · mode 137 · platform 196 · abstain 17 / 20 |
| v3 (311) | 152 / 311 | scope 298 · platform 221 · mode 228 · recall 0.533 · forbidden 6 · abstain 24 / 30 |
| v4 (434) — inspected in Phase 5 analysis, therefore historical | 100 / 434 | platform claims 394: correct 208, UNKNOWN 174 (**44.2 %**), wrong 12 (3.0 %) · mode 366 / 414 · scope 406 / 434 · concern coverage 0.794 · concept recall 0.535 · **critical recall 0.630** · **forbidden 40 / 414 = 9.7 %** · bundle size 5.98 · tokens 895 |

v4 human review: GOOD 99 · PARTIAL 210 · BAD 101 · WRONG_ABSTAIN 15 · CORRECT_ABSTAIN 9 (GOOD+PARTIAL 0.754, BAD 0.246). Defects: generic 98 · wrong-screen 88 · missing-critical 83 · off-platform 25 · should-not-abstain 15 · should-abstain 12 · contradicts-request 5. Thresholds met 3 / 10.

## Real projects (Phase 5 c2 re-scoring, not implemented)

22 tasks / 12 codebases: platform 22 / 22 · scope 22 / 22 · mode yes 14 / acceptable 8 · concept recall 0.678 · critical recall 0.841 · forbidden-delivery tasks 5 · reviewer records relevant / partial / off-target 56 / 39 / 46 (BAD: generic 39, contradicts-codebase 8, missing-critical 6, off-platform 2, wrong-mode 1) · would-have-helped 18 / neutral 4 / hurt 0 · unjustified direction slots 10. Implemented round c1 (Phase 5): helped 3 / neutral 16 / hurt 3.

## Phase 6 targets (aggregate classes only; no v4 case is opened during implementation)

A. generic concern-filling guardrails · B. wrong-screen / wrong-product core records (including whole-product directions) · C. missing critical concepts · D. safe situational platform inference (UNKNOWN 44 % → lower without raising the 3 % false-assignment rate).
