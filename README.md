# design-engineering — a context-first UI/UX skill for Claude Code

A Claude Code skill that helps an AI coding agent design and change user interfaces in **real codebases** across web, mobile (SwiftUI, Compose, Flutter, React Native), desktop (WinUI, WPF, Avalonia), TV (Android TV, tvOS, Tizen/webOS) and kiosks. It inspects the project first, derives navigation, layout and density before visual style, retrieves a small bundle of verified guidance, and verifies the result by rendering.

This repository is the skill plus the complete research record behind it: six development phases, five blind held-out sets, four real-project qualification rounds and every evaluation run, published as-is. The current verdict by the skill's own pre-registered standard is **personal-production-ready, not stable-candidate** (see [Status](#status)).


## What it does

When Claude Code works on a UI task the skill runs three Python commands (stdlib only, no network, no packages) and reads their output instead of loading design knowledge into context:

| Step | Command | Output |
|---|---|---|
| Inspect the project | `scripts/inspect_project.py <repo> --out .design-inspect.json` | Stack, platforms, UI libraries, tokens, fonts, breakpoints, routing, focus/DPAD handling, and the **design context** already present: navigation topology, theme polarity, surface and radius language, spacing base, typography, component library — each marked KNOWN / INFERRED / UNKNOWN with evidence. |
| Understand the request | `scripts/advise.py requirements "<request>" --project .design-inspect.json --explain` | A `DesignRequirements` contract: scope (is this a UI task at all), platform with typed and graded evidence (UNKNOWN beats wrong), modes (create, refactor, polish, audit, accessibility, responsive, brand, design-system, reconstruct), operations, change scope, change budget, preservation constraints, and the concepts the task demands with a priority and a `critical` flag. |
| Get guidance | `scripts/advise.py guidance "<request>" --project .design-inspect.json --explain` | A 1–8 record bundle in three layers — **CORE** (what to build), **CRITICAL GUARDRAILS** (must hold), **OPTIONAL NOTES** — from 248 hand-written records (components, layout patterns, rules, charts, anti-patterns, whole-product directions) over a 114-concept ontology. Every record says why it entered; every demanded concept that stayed uncovered says why. |

`advise.py direction` assembles a slot-based design direction (navigation, layout, cards, typography, colour, motion, focus, CTA…) that **preserves what the codebase already decided** unless the task asks to change it, and `advise.py search` is the raw ranked lookup for debugging. The skill's operating procedure is [design-engineering/SKILL.md](design-engineering/SKILL.md); platform, stack and topic references live under `platforms/`, `stacks/` and `references/`.

Design principles, in order: understand product, users, environment and input first; reuse → extend → compose → new primitive; precision before coverage ("no guidance" beats generic guidance); critical concepts before generic completeness; verify by rendering, never by compiling.

## Install

Requires Claude Code and Python 3.10+. Link the skill directory into your personal skills folder so the repository stays the single source of truth:

```bash
ln -s "$(pwd)/design-engineering" ~/.claude/skills/design-engineering
```

Windows PowerShell:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\design-engineering" -Target "$PWD\design-engineering"
```

Or copy `design-engineering/` to `<repo>/.claude/skills/` to scope it to one project. Details: [docs/INSTALL.md](design-engineering/docs/INSTALL.md), usage examples: [docs/USAGE.md](design-engineering/docs/USAGE.md), how to extend or debug it: [docs/MAINTENANCE.md](design-engineering/docs/MAINTENANCE.md).

Try it without installing:

```bash
python design-engineering/scripts/advise.py guidance "From the sofa nobody can tell which row is selected." --explain
```

## Status

Stability labels are earned only by blind evidence under thresholds written before the test set exists. Phase 6 (September 2026) judged candidate **c4** by an implemented round of 32 tasks on 16 codebases and by held-out **v5** (525 natural-language prompts written and scored by separate sessions that never saw the records, lexicon, cases or code):

| what | result |
|---|---|
| Implemented project round | helped on 22 of 32 tasks, hurt on none; critical-concept recall 0.64–0.68 against a 0.80 bar; round **failed** 4 of 9 pre-registered criteria |
| Held-out v5 | 5 of 11 pre-registered thresholds met. Met: false platform 0.025, platform correctness 0.77, mode 0.92, forbidden concepts 0.049, wrong-screen defects 0.072. Failed: critical recall 0.45, required recall 0.35, human GOOD+PARTIAL 0.72, BAD 0.28, generic defects 0.137, scope-as-scored 0.84 (78 empty bundles counted as abstentions) |
| Verdict | **personal-production-ready**; phase-chasing stopped |

The honest one-line summary: a precise retriever with a lexical demand layer that does not generalise to unseen phrasings. Wrong-screen and wrong-platform guidance are largely solved; missing critical concepts and empty bundles on plain build requests are not. Everything behind these numbers is in the repository — read [research/PHASE6-RESULTS.md](research/PHASE6-RESULTS.md) first.

## Repository layout

| Path | Contents |
|---|---|
| `design-engineering/` | The skill: `SKILL.md`, `scripts/` (advise, inspect_project, de_core, de_semantic, validate_skill, tokens, fingerprint), `data/` (six JSONL record files + `lexicon.json`), `platforms/`, `stacks/`, `references/`, `docs/`, `evals/` |
| `design-engineering/evals/` | Development suites (885 cases), regression suite (54), held-out sets v1–v5 with pre-registered `THRESHOLDS.md` and hashes, activation set, the runner (`run_evals.py`), release check, benchmark harness, platform confusion matrix, output-size and rescoring tools |
| `research/PHASE*-BASELINE.md`, `PHASE*-RESULTS.md`, `PHASE*-PROJECTS.md` | Per-phase baseline recorded before changes, results with one verdict each, and real-project round reports |
| `research/phase3-projects/` … `phase6-projects/` | The qualification rounds: protocol, task sentences, fixture codebases (16 small but real apps across all five platforms), and one directory per task with pre-registered expectations, skill outputs, `RESULTS.md` and `artifacts.json`. Render screenshots are kept out of the repository. |
| `research/runs/` | Every archived run: freezes with build hashes, held-out runs, human reviews, rescoring, benchmark, output size |
| `research/NEW-ARCHITECTURE.md` | Design decisions, rejected alternatives and per-phase additions |
| `research/UPSTREAM-AUDIT.md`, `UPSTREAM-VS-NEW.md`, `BENCHMARK-RESULTS.md` | The audit of the upstream project, an honest comparison including where upstream is stronger, and the regression benchmark |

## Evaluation discipline

- Development cases are written **before** the code that makes them pass; a case is never edited to pass — a wrong case gets a dated note.
- Held-out sets are generated and scored by independent sessions, run **once** on a frozen build whose hash is recorded first, and become historical (non-blind) afterwards. Thresholds are pre-registered and never lowered.
- Real-project rounds run on a frozen build with pre-registered per-task expectations; the build hash is checked at the start and end of every task; a fix means a new candidate and a rescore.
- Every defect is routed to the earliest wrong layer (scope → platform evidence → mode → requirements → concerns → expected concepts → criticality → retrieval → compatibility → selection → project context → direction → implementation → verification) and fixed there or recorded as open.

Reproduce the deterministic gates:

```bash
python design-engineering/evals/release_check.py
```

## Licence

MIT. See [LICENSE](LICENSE) and [NOTICE-SOURCES.md](NOTICE-SOURCES.md).
