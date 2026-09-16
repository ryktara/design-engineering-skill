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
