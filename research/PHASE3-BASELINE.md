# Phase 3 baseline (recorded before any Phase 3 change, 2026-09-08)

Source: `research/runs/phase3-baseline-release-check.json` (`python evals/release_check.py --heldout --real-activation --json`), `research/benchmark-results.json`, `research/KNOWLEDGE-GAPS.md`.

| Item | Value |
|---|---|
| records | 220 |
| lexicon sha256 (first 16) | `99164847347d4fdb` |
| scripts/de_core.py sha256 (first 16) | `ee52a9a9a03ade53` |
| validator | 0 errors, 0 warnings |
| development + regression | 157/157 (142 + 15 cases) |
| activation proxy (180, not blind after Phase 2 lexicon fixes) | precision 0.987, recall 0.987, FPR 0.014, FNR 0.013 |
| real activation | SKIPPED — `claude -p` not authenticated for non-interactive use |
| performance sanity | load 8 ms, search 207 ms (first call builds the index), direction 31 ms |

## Frozen held-out v1 (145 cases) — diagnostic baseline, not a tuning target

| Metric | Value |
|---|---|
| acceptable | 10 / 145 |
| mean concept recall (token match) | 0.184 |
| concept recall ≥ ½ | 15 / 145 |
| platform recall / precision | 123 / 137 of 145 |
| mode correct | 98 / 145 |
| input correct | 130 / 145 |
| negative constraints correct | 138 / 145 |
| MISSING correct | 112 / 145 |
| mean off-target rate | 0.178 |
| facet coverage complete | 72 / 145 |
| status distribution | CONFIDENT 91 · PARTIAL 32 · AMBIGUOUS 21 · ABSTAIN 1 |
| abstain cases | 6 / 6 |
| empty results | 1 |

Ranking-miss decomposition (Phase 2 analysis): 478 concept misses where the concept exists in the base but was not in the top 5; 192 where no record carries the concept; 148 hits. Category diversity is not reported per case in this baseline (added in Phase 3 metrics).

## Benchmark (method v2)

18 queries: relevant 0.200 (upstream) vs 0.879 (ours); off-target 0.189 vs 0.134; empty 3 vs 0; cold median 238 ms vs 332 ms (p95 403 vs 522); ours warm median 28 ms; mean facet coverage 0.722. Upstream is faster cold; that is accepted and not hidden.

## Failure classes carried into Phase 3 (from aggregate analysis, not individual cases)

1. Universal interaction/accessibility rules (touch targets, keyboard navigation, focus, contrast) do not enter create-mode result sets on touch/web platforms because they are not required facets there.
2. Data-heavy concepts (tabular figures, column priority, numeric alignment, selection/edit state) lose to product-specific layout records.
3. TV vocabulary mismatches (10-foot vs distance, pinned vs sticky, auto hide vs auto-hides).
4. Problem-statement phrasing defaults to `create` (47 mode misses).
5. Application states beyond loading/empty/error (offline, sync, saving, session) are thin.
6. Environmental context (outdoor, shared device, low bandwidth) is not modelled.

The held-out v1 set has been inspected and is no longer blind; it will be re-run once after the Phase 3 freeze as historical comparison only. A new blind held-out v2 (≥200 cases, generator/reviewer separation) is created after the freeze.
