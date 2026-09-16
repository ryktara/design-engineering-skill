# Phase 2 baseline (recorded before any Phase 2 change)

Date: 2026-09-08. Skill: `design-engineering` v1 as delivered at the end of Phase 1, installed as a junction at `~/.claude/skills/design-engineering`.

## Repository state

Not a git repository (`git rev-parse` fails). Workspace: `D:\indigo pro\MYownSkills`. No commit hash is available; the baseline is identified by the file set and the numbers below. Record count 220, `validate_skill.py`: 0 errors, 0 warnings.

## Evaluation totals (`python evals/run_evals.py`)

| Suite | Result |
|---|---|
| activation (deterministic proxy) | 30/30 |
| retrieval | 19/20 |
| platform | 3/3 |
| brand | 4/4 |
| accessibility | 14/14 |
| anti-generic | 12/12 |
| project | 5/5 |
| greenfield | 6/6 |
| tools | 15/15 |
| **total** | **108/109** |

Failing case: `retrieval/winui-erp-grid` ("WinUI desktop ERP data grid with keyboard shortcuts") expects `desktop-keyboard-first` in the top 5; it ranks 7th behind five ERP-fit table/layout/direction records and `density-high`. Known limitation from Phase 1: universal interaction rules can be crowded out by several product-specific records that share the same structural signals.

Three cases carry dated notes documenting threshold adjustments made in Phase 1 (`platform/media-browse-by-platform`, `platform/settings-by-platform`, `retrieval/tv-banking-kiosk`).

All eval cases were written alongside the implementation; there is no held-out set.

## Benchmark (research/BENCHMARK-RESULTS.md, method v1)

18 queries, term-coverage scoring. Upstream 0.20 vs ours 0.88 relevant-term coverage; off-target 0.19 vs 0.13; empty results 3 vs 0; "mean latency" 0.360 s vs 0.041 s. Methodology defect: upstream latency is a cold subprocess per query while ours is warm in-process; the numbers are not comparable. Numbers are also hand-copied into `research/UPSTREAM-VS-NEW.md`, so they can drift.

## Activation probe status

`evals/probe_activation_with_claude.py` cannot run: `claude -p` returns "Not logged in · Please run /login" when invoked as a subprocess from this environment. The probe aborts (it no longer scores silently). Real-model activation is therefore unmeasured at baseline. Only 30 proxy cases exist (16 positive, 10 negative, 4 ambiguous); no competing-skill cases.

## Script latency (baseline machine, Python 3.14, warm process unless noted)

| Operation | Median | p95 | n |
|---|---|---|---|
| load 220 records | 53 ms | — | 1 |
| classify | 1.4 ms | 1.8 ms | 15 |
| search (k=5) | 34 ms | 41 ms | 15 |
| direction | 63 ms | 66 ms | 5 |
| cold subprocess `advise.py search --json` | 480 ms | — | 5 |
| inspect_project on the Next.js fixture (cold subprocess) | 229 ms | — | 3 |

## Known limitations carried into Phase 2

- No requirements contract: `search`, `direction`, and evals each call `classify()` and read loosely related signal dicts.
- Diversification is a flat per-category cap (2), not facet-aware.
- Confidence labels (high/medium/low/none) are thresholds on score and token coverage; never checked against observed accuracy.
- Negative constraints cover eight device words; no "keep navigation", "no dependencies", "remote only" handling.
- Direction output is not validated against requirements (no invariants).
- Benchmark timing mixes cold and warm; results duplicated in prose.

## Documentation vs executable output inconsistencies found

- `UPSTREAM-VS-NEW.md` states a benchmark latency comparison that the harness measured with mismatched methods (cold vs warm).
- `SKILL.md` describes `advise.py classify/search/direction/show`; there is no requirements command yet (this phase adds it).
- Case counts in `NEW-ARCHITECTURE.md` (109 cases) match the runner; suite names match.
