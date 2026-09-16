# Phase 5 baseline (recorded before any Phase 5 change, 2026-09-09)

Source: `research/runs/phase5-baseline.json` (a copy of the Phase 4 final release check), `research/runs/phase4-freeze.json`, `research/PHASE4-RESULTS.md`.

| Item | Value |
|---|---|
| records | 237 (149 concept-labelled; the 88 unlabelled are slot patterns and directions) |
| concepts / namespaces / concerns | 109 · 22 · 16 |
| eval cases | development 269 · regression 40 · heldout v1 145 · heldout v2 212 · heldout v3 311 · activation 180 |
| sha256 (first 16) | de_core `4ecbca0ecca2e676` · de_semantic `2bbee02f0959f68e` · inspect_project `6e77763f547f2301` · lexicon `55341c3c720e75fe` |
| deterministic gates | validator OK · development + regression 309 / 309 · activation proxy precision 0.987 / recall 1.000 / FPR 0.014 · release check PASS |
| real activation | SKIPPED (CLI not authenticated) |
| performance | load 7 ms · search 246 ms (cold index) · direction 65 ms; benchmark cold 414 ms vs upstream 200 ms, warm 43 / 54 ms |
| output size | guidance markdown mean 1031 / p95 1302 tokens · direction 2236 / 2593 |
| benchmark | relevant 0.200 / 0.909 / 0.928 (upstream / search / guidance) · off-target 0.189 / 0.148 / 0.106 |

## Blind held-out v3 (now historical)

platform 0.79 ✗ · mode 0.64 ✗ · scope 0.92 ✓ · concern coverage 0.91 ✓ · concept recall 0.50 ✗ · forbidden 0.03 ✓ · empty 0.00 ✓ · human GOOD+PARTIAL 0.81 ✓ · human BAD 0.19 ✓ → 6 / 9 primary; verdict personal-production-ready.

Aggregate failure classes carried into Phase 5 (no individual v3 prompts were opened): platform misses were mostly *no platform detected* (43 of 58) rather than wrong platform; mode misses were mostly `create` where a change mode was expected (74 of 100), i.e. existing-UI modifications without an explicit change verb; concept recall was 0.50 with 40 zero-recall bundles; scope 19 false abstentions and 5 answered out-of-scope prompts.

## Historical v1 / v2 at baseline

v1: acceptable 38 / 145, recall 0.359, mode 119, platform 132. v2: acceptable 30 / 212, recall 0.234, mode 139, platform 201, abstain 17 / 20.

## Real projects at baseline

Phase 4 round: 15 tasks, 9 applications, preservation 15 / 15, unjustified structural change 0; context detection weak for typography / surfaces on native stacks.
