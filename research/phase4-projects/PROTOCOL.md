# Phase 4 real-project protocol (one directory per task)

Purpose: measure whether the skill now understands the design system already present in a codebase and leads implementation toward a compatible, better direction. Most tasks modify EXISTING interfaces. The skill is under test; **do not modify anything under `design-engineering/`**. Report gaps instead. Skill root: `D:\indigo pro\MYownSkills\design-engineering` (Python 3). Task root: `D:\indigo pro\MYownSkills\research\phase4-projects\<task-id>\`. Projects live under `D:\indigo pro\MYownSkills\research\phase3-projects\<case>\project` (real code from Phase 3); work on them in place (they are research artifacts), but keep a copy of any file you change as `<task>/before/<relative path>`.

## Steps (commands from the skill root)

1. **Inspect** — `python scripts/inspect_project.py <project> --json > <task>/01-inspect.json`. Read `design_context` (navigation, theme, surfaces, radius, spacing, typography, components; each KNOWN / INFERRED / UNKNOWN with evidence). Then look at the code yourself and write the **actual** design language (what a human sees in the shell/theme files). Record both in RESULTS.md as a table: field · detected · status · actual · correct? (yes / partial / no).
2. **Requirements** — `python scripts/advise.py requirements "<task sentence>" --project <task>/01-inspect.json --pretty --explain > <task>/02-requirements.json`. Judge: scope (`scope.domain`, `in_scope`), modes (`mode`, `mode_evidence`), `change_budget`, `intent.preserve`, `project_context`, platform/product/screen/jobs. Say which are right/wrong.
3. **Guidance** — `python scripts/advise.py guidance "<task>" --project <task>/01-inspect.json --explain > <task>/03-guidance.md` (+ `--json > 03-guidance.json`). For each core/guardrail record: relevant / partial / off-target. Note the `metrics` (concept coverage, coverage_per_1k_tokens, contaminated, purity). List missing guidance: is the concept absent from the base (knowledge gap) or present but not selected (ranking miss; check `advise.py search "<task>" -k 12 --explain`)? Note any `uncovered required concepts`.
4. **Direction** — `python scripts/advise.py direction "<task>" --project <task>/01-inspect.json --explain > <task>/04-direction.md` (+ `--out <task>/04-direction.json`). Record the **compatibility** table (preserved / changed / new per slot with reason), `preservation` metrics, `change_budget`, and `validation`. Judge every *changed* slot: justified or not.
5. **Implement** the task following the guidance and direction, reusing the project's conventions. Keep routes, state, tests, ids, accessibility semantics intact unless the task is about them.
6. **Render** — as in Phase 3: Playwright screenshots for web/kiosk/HTML twins (`npm i playwright@1.63.0` in `<task>/render/` if not already present in the project's earlier render dir; Chromium is installed); native WPF via the project's existing `--capture` harness if present; Compose/SwiftUI/Flutter via HTML twin + static review. Viewports: web 1440×900 + 390×844; TV 1920×1080; kiosk 1080×1920; mobile 390×844. Say which mode you used.
7. **Inspect the render** and classify each first-render defect by type: `visual`, `interaction`, `accessibility`, `platform`, `existing-system-mismatch` (new element clashes with the existing navigation/theme/typography/spacing), `implementation-bug`. Fix, re-render, re-run the interaction test, record final defects by type.
8. **Diagnose every skill miss by the earliest wrong layer**: `scope` → `mode` → `requirements` → `concerns` → `expected-concepts` → `candidate-retrieval` → `bundle-selection` → `direction` → `project-adaptation`. One layer per miss.

## Deliverables in `<task>/`

- `RESULTS.md`: Task · Project/stack/platform · Existing-UI or greenfield · Design-context table (detected vs actual) · Requirements verdict · Guidance verdict (per record + misses with layer) · Direction verdict (compatibility table, unjustified changes) · Implementation summary (files changed) · First-render defects by type · Final defects by type · Iterations · Interaction test summary · Preservation verdict (did the result keep navigation / theme / typography / component language? was any structural change unjustified?) · Regressions to propose (query + expectation, no record ids required) · Tags from: `scope-miss`, `mode-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-helped`, `preservation-ok`, `preservation-violated`.
- `artifacts.json`:
```json
{"task": "<id>", "project": "<case>", "platform": "...", "stack": "...", "existing_ui": true, "mode": "...", "change_budget": "...",
 "render_mode": "native|html|html-twin|static-review", "screenshots": [...],
 "context_detection": {"navigation": "yes|partial|no", "theme": "yes|partial|no", "typography": "yes|partial|no", "surfaces": "yes|partial|no", "spacing": "yes|partial|no"},
 "preservation": {"navigation": true, "theme": true, "typography": true, "component_reuse": true, "unjustified_structural_change": 0},
 "first_render_defects": {"visual": 0, "interaction": 0, "accessibility": 0, "platform": 0, "existing-system-mismatch": 0, "implementation-bug": 0},
 "final_defects": {"visual": 0, "interaction": 0, "accessibility": 0, "platform": 0, "existing-system-mismatch": 0, "implementation-bug": 0},
 "iterations": 0, "guidance_relevant": 0, "guidance_partial": 0, "guidance_offtarget": 0,
 "misses": [{"layer": "mode", "what": "..."}], "knowledge_gaps": [], "regressions": [{"query": "...", "expect": "..."}], "tags": []}
```
- `render/first-*.png`, `render/final-*.png`, `before/` copies of changed files.

Be factual. Do not pad. A result where the skill got the context wrong and you had to ignore it is valuable data; write it down.
