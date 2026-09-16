# Phase 6 real-project qualification protocol (Phase 5 steps + Phase 6 addendum at the end) (one directory per task)

Purpose: qualify a FROZEN candidate build of the `design-engineering` skill on real codebases. The skill is under test. **Never modify anything under `design-engineering/`** — not scripts, not data, not evals. If it is wrong, write that down. Skill root: `D:\indigo pro\MYownSkills\design-engineering` (Python 3, stdlib only). Task root: `D:\indigo pro\MYownSkills\research\phase6-projects\<task-id>\`. Projects live under `research\phase3-projects\<case>\project` (Phase 3 codebases) , `research\phase5-projects\<codebase>\project` (Phase 5) or `research\phase6-projects\<codebase>\project` (new in Phase 6). Work on the project in place, but copy every file you change to `<task>/before/<relative path>` first.

Task sentences are in `TASKS.md`. Run the sentence **verbatim** — do not rewrite it to help the skill.

## Steps (run commands from the skill root)

0. **Build hash + pre-registered expectation (BEFORE running any advise command).** `python evals/build_hash.py > <task>/00-build-hash-start.txt`. Then read the project shell/theme code (not the skill output) and write `<task>/00-expectation.json`:
   ```json
   {"platform": "web|mobile|desktop|tv|kiosk", "artifact_state": "new|existing", "acceptable_modes": ["..."], "scope_kind": "in-scope|partial|abstain",
    "expected_concepts": ["3-7 ids from evals/heldout-v4/ONTOLOGY.md"], "critical_concepts": ["subset; guidance without these is BAD"],
    "forbidden_concepts": ["ids that would be wrong for this task"], "preservation": ["navigation", "theme", "typography"]}
   ```
   Modes are from: create, refactor, polish, audit, review, accessibility, responsive, brand, design-system, reconstruct. This file is your reviewer opinion; the skill's output must not influence it.
1. **Inspect** — `python scripts/inspect_project.py <project> --json > <task>/01-inspect.json`. Compare `design_context` (navigation, theme, surfaces, radius, spacing, typography, components; KNOWN / INFERRED / UNKNOWN) with what the code actually does. Table in RESULTS.md: field · detected · status · actual · correct? (yes / partial / no). A value marked UNKNOWN when the code is clear is `partial`; a confident wrong value is `no`.
2. **Requirements** — `python scripts/advise.py requirements "<task sentence>" --project <task>/01-inspect.json --pretty --explain > <task>/02-requirements.json`. Judge against your expectation: `platform_evidence` (assigned platform correct / unknown-with-MISSING-confirm / wrong), `intent.artifact_state`, `intent.operations`, `intent.problem_domain`, `intent.change_scope`, `mode` + `mode_evidence`, `scope.kind` (in-scope / partial / abstain) and `scope.reason`, `change_budget`, `intent.preserve`, `project_context`. UNKNOWN platform with a confirm entry is acceptable when the sentence gives weak evidence; a WRONG platform is a failure.
3. **Guidance** — `python scripts/advise.py guidance "<task sentence>" --project <task>/01-inspect.json --explain > <task>/03-guidance.md` and `--json > <task>/03-guidance.json`. For each core/guardrail record: relevant / partial / off-target. Off-target or harmful records get a BAD category from: `off-platform`, `wrong-mode`, `generic`, `contradicts-codebase`, `missing-critical`, `harmful`. Compute **real concept recall**: delivered concepts = union of `concepts` over selected records (in the JSON); recall = |expected ∩ delivered| / |expected|; critical recall likewise. For every expected concept not delivered, use `concept_trace` in the explain output to name the earliest wrong layer: `expected-concepts` (never demanded), `candidate-retrieval` (demanded, no candidate), `bundle-selection` (candidate dropped), or `knowledge-gap` (no record in the base carries it; confirm with `python scripts/advise.py search "<sentence>" -k 12 --explain`). If `status` is PARTIAL_SCOPE, judge whether the design/engineering split in the note is right.
4. **Direction** — `python scripts/advise.py direction "<task sentence>" --project <task>/01-inspect.json --explain > <task>/04-direction.md` and `--out <task>/04-direction.json`. Record the compatibility table (preserved / changed / new per slot), `preservation` metrics, `validation`. Judge every changed slot: justified or not.
5. **Implement** the task following the guidance and direction, reusing the project's conventions. Keep routes, state, tests, ids, accessibility semantics intact unless the task is about them. Record which guidance you actually used and which you had to ignore (and why).
6. **Render** — web/kiosk/HTML twins: Playwright screenshots (`npm i playwright@1.63.0` inside `<task>/render/` if needed; Chromium is installed). Native WPF: the project's `--capture` harness if present, else an HTML twin. Compose / SwiftUI / Flutter / Avalonia: HTML twin (`project/render/twin.html` exists for the Phase 5 codebases; update the twin to reflect your change) + static code review. Viewports: web 1440×900 and 390×844; TV 1920×1080; kiosk 1080×1920; mobile 390×844; desktop 1440×900. Save `render/first-*.png` and `render/final-*.png`. State the render mode.
7. **Inspect the render**; classify first-render defects by type: `visual`, `interaction`, `accessibility`, `platform`, `existing-system-mismatch`, `implementation-bug`. Fix, re-render, record final defects and the iteration count.
8. **Diagnose every skill miss by the earliest wrong layer**: `scope` → `platform` → `mode` → `requirements` → `concerns` → `expected-concepts` → `candidate-retrieval` → `bundle-selection` → `direction` → `project-adaptation`. One layer per miss.
9. **Build hash at the end** — `python evals/build_hash.py > <task>/00-build-hash-end.txt`. It must equal the start hash; if not, say so loudly in RESULTS.md.

## Deliverables in `<task>/`

- `RESULTS.md`: Task · Project/stack/platform · Existing-UI or new screen · Design-context table · Requirements verdict (platform, artifact state, operations, domain, scope kind, modes, budget, preserve) · Guidance verdict (per record + BAD categories + concept recall table: expected id · delivered? · layer if missing) · Direction verdict · Implementation summary (files changed; guidance used / ignored) · First-render and final defects by type · Iterations · Preservation verdict · Regressions to propose (query + expectation in words) · Tags from: `scope-miss`, `platform-miss`, `mode-miss`, `requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-helped`, `skill-neutral`, `skill-hurt`, `preservation-ok`, `preservation-violated`, `partial-scope-ok`, `partial-scope-wrong`.
- `artifacts.json`:
```json
{"task": "<id>", "project": "<codebase>", "platform_expected": "...", "platform_resolved": "...|unknown", "platform_correct": "yes|unknown|wrong",
 "stack": "...", "existing_ui": true, "new_screen": false,
 "artifact_state_expected": "existing", "artifact_state_resolved": "existing", "artifact_state_correct": true,
 "mode_expected": ["..."], "mode_resolved": ["..."], "mode_correct": "yes|acceptable|no",
 "scope_kind_expected": "in-scope", "scope_kind_resolved": "in-scope", "scope_correct": true,
 "change_budget": "...", "render_mode": "native|html|html-twin|static-review", "screenshots": ["..."],
 "context_detection": {"navigation": "yes|partial|no", "theme": "yes|partial|no", "typography": "yes|partial|no", "surfaces": "yes|partial|no", "spacing": "yes|partial|no"},
 "preservation": {"navigation": true, "theme": true, "typography": true, "component_reuse": true, "unjustified_structural_change": 0},
 "expected_concepts": ["..."], "critical_concepts": ["..."], "delivered_concepts": ["..."], "concept_recall": 0.0, "critical_recall": 0.0,
 "concept_misses": [{"concept": "...", "layer": "expected-concepts|candidate-retrieval|bundle-selection|knowledge-gap"}],
 "first_render_defects": {"visual": 0, "interaction": 0, "accessibility": 0, "platform": 0, "existing-system-mismatch": 0, "implementation-bug": 0},
 "final_defects": {"visual": 0, "interaction": 0, "accessibility": 0, "platform": 0, "existing-system-mismatch": 0, "implementation-bug": 0},
 "iterations": 0, "guidance_relevant": 0, "guidance_partial": 0, "guidance_offtarget": 0,
 "bad_guidance": [{"record": "<id>", "category": "off-platform|wrong-mode|generic|contradicts-codebase|missing-critical|harmful", "why": "..."}],
 "skill_effect": "helped|neutral|hurt", "guidance_tokens": 0,
 "misses": [{"layer": "mode", "what": "..."}], "knowledge_gaps": [], "regressions": [{"query": "...", "expect": "..."}], "tags": [],
 "build_hash_start": "...", "build_hash_end": "..."}
```
- `render/first-*.png`, `render/final-*.png`, `before/` copies of changed files.

Be factual. Do not pad. A result where the skill got something wrong and you had to ignore it is the most valuable data; write it down exactly.
## Phase 6 additions to the protocol (read after the steps above)

The build under test is candidate **c3** — `research/runs/phase6-freeze-c3.json`, sha256 `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`. Step 0 and step 9 must both print exactly this hash. Task directories live under `research/phase6-projects/<task>/`; codebases are `research/phase3-projects/<case>/project`, `research/phase5-projects/<codebase>/project` and `research/phase6-projects/<codebase>/project` (see TASKS.md).

**Guidance output has three layers now**: CORE (what to build), CRITICAL GUARDRAILS (must hold) and OPTIONAL NOTES (recommended coverage; omitted when empty). Bundles have no minimum size — an empty layer is a valid result. `--explain --json` exposes `marginal` (why each record entered: new critical / required / recommended concepts, evidence, quality DIRECT / SPECIFIC / GENERIC, contamination, tokens), `omitted`, `not_surfaced` and the concept trace with `critical` and `carrier_quality`.

**Per-record review (step 3) uses the Phase 6 defect categories.** Mark every core / guardrail / optional record `relevant`, `partial` or `off-target`; for `partial` and `off-target` name exactly one category: `generic` (true in general, says nothing this task needed), `wrong-screen` (guidance for a screen the task is not about), `wrong-product` (guidance for another product family), `missing-critical` (a pre-registered critical concept is absent from the bundle — record it against the bundle, not a record), `off-platform`, `contradicts-request`, `contradicts-codebase`, `overlong` (the record is far longer than its contribution), `should-abstain` / `should-not-abstain` (scope). In `artifacts.json` the `bad_guidance[].category` field takes these values; also add `"layer_review": {"core": [...ids], "critical": [...ids], "optional": [...ids], "optional_useful": n, "optional_noise": n}`.

**Skill effect** (`skill_effect`): `helped` only if at least one critical or required concept you implemented came from the bundle and you would plausibly have missed or under-specified it; `hurt` if a record led you to a change you reverted or that a reviewer would call a defect; else `neutral`. Also record `"guidance_used": [ids]`, `"guidance_ignored": [{"id", "why"}]`.

**Direction (step 4).** Count `unjustified_direction_slots`: slots the direction changed (status `changed` / `new`) that the task did not justify. On an existing UI with a low or moderate budget the expected number is 0; state each unjustified slot.

**Process guidance check.** Answer in RESULTS.md: *Did you need `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` in the bundle, or was SKILL.md §2 / §7 enough?* (`"process_records_needed": true|false` in artifacts.json, with the reason.)

**Defects (step 7).** Count first-render and final defects by type as before, plus `"iterations"`. A defect the guidance explicitly warned about and you still shipped counts against you, not the skill; say so.

**Half of the task sentences carry no mode word** on purpose. Never rewrite the sentence.

**Routing (step 8)** uses the Phase 6 layer list: `scope` → `platform-evidence` → `mode` → `requirements` → `concerns` → `expected-concepts` → `criticality` → `candidate-retrieval` → `candidate-compatibility` → `bundle-selection` → `project-context` → `direction` → `implementation` → `verification`. One layer per miss, the earliest.

Rendering: HTML / web / kiosk / TV-web codebases render with Playwright (`npm i playwright@1.63.0` inside `<task>/render/`, Chromium is installed); TV-web at 1920×1080, kiosk at 1080×1920, web at 1280×800 and 390×844; Compose / SwiftUI / Flutter / WPF / WinUI / Avalonia: an HTML twin of the changed screen (state `render_mode: html-twin`) unless a capture harness exists. Never claim a render you did not look at.
