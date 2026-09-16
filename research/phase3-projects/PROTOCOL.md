# Phase 3 torture-test protocol (one directory per case)

Purpose: exercise the `design-engineering` skill end to end on a realistic project and record where it helps, where it misses, and what defects the first render had that a second pass fixed. The skill is under test; **do not modify anything under `design-engineering/`** (scripts, data, evals, docs). Report gaps instead.

Skill root: `D:\indigo pro\MYownSkills\design-engineering` (Python 3, stdlib only). Case root: `D:\indigo pro\MYownSkills\research\phase3-projects\<case-id>\`.

## Steps (all commands from the skill root unless noted)

1. **Project** — create or reuse the project under `<case>/project/`. Real code in the named stack. Keep it small (one to three screens) but honest: real components, real data shapes, real states.
2. **Inspect** — `python scripts/inspect_project.py <case>/project --json > <case>/01-inspect.json`. Note what it detected (KNOWN/INFERRED) and what it missed.
3. **Requirements** — `python scripts/advise.py requirements "<the task sentence>" --project <case>/01-inspect.json --pretty --explain > <case>/02-requirements.json` (exit codes 0/3/4/5 are statuses, not failures). Judge every KNOWN/INFERRED/MISSING entry: right, wrong, or missing.
4. **Guidance** — `python scripts/advise.py guidance "<task>" --project <case>/01-inspect.json --explain > <case>/03-guidance.md` and the same with `--json > <case>/03-guidance.json`. For each core/guardrail record say: relevant / partially / off-target. List guidance you needed that was absent (knowledge gap) or present in the base but not selected (ranking miss; check with `python scripts/advise.py search "<task>" -k 12 --explain`).
5. **Direction** — `python scripts/advise.py direction "<task>" --project <case>/01-inspect.json --explain --out <case>/04-direction.json > <case>/04-direction.md`. Check the validation block and whether the slots fit the platform.
6. **Implement** — build the screen(s) following the guidance and direction. Reuse the project's existing conventions when they exist.
7. **Render** — web/TV/kiosk/mobile HTML: screenshot with Playwright (`npm init -y; npm i playwright@1.63.0` inside `<case>/render/`, Chromium is already installed) at the platform's viewport (web 1440×900 and 390×844; TV 1920×1080; kiosk 1080×1920 portrait; mobile 390×844). Native stacks (Compose, SwiftUI, WinUI/WPF/Avalonia, Flutter): build if the toolchain is present (`dotnet` 10 SDK is available; no gradle wrapper, no Xcode, no Flutter), otherwise do a static review of the code and render an HTML twin of the screen at the platform viewport so the visual can still be inspected. Say clearly which one you did.
8. **Inspect the render** — open the PNG (Read tool) and list defects: overlap, clipping, contrast, hierarchy, density wrong for the platform, missing states, generic look, focus not visible, targets too small, safe-area violations, etc. Record these as **first-render defects**.
9. **Interaction test** — Playwright script: keyboard Tab/Arrow traversal (web/desktop), D-pad simulation with arrow keys and Enter/Backspace/Escape for TV, touch-target measurement (`getBoundingClientRect` ≥ 48 px) for mobile/kiosk, focus-visible check (computed outline/box-shadow on focused element), reduced-motion media query respected. Write results to `<case>/05-interaction.json`.
10. **Fix and re-render** — fix the defects, re-screenshot, re-run the interaction test. Record **final defects** (what remains).
11. **Tokens (optional)** — if you defined tokens, `python scripts/tokens.py validate <tokens.json> --platform <web|mobile|desktop|tv|kiosk>` and record the result.

## Deliverables in `<case>/`

- `RESULTS.md` with sections: Task · Stack/platform · Inspection verdict · Requirements verdict (per field) · Guidance verdict (per record: relevant/partial/off-target; gaps; ranking misses) · Direction verdict (slots, validation) · First-render defects (numbered) · Final defects · Iterations (count and what each changed) · Interaction test summary · Time spent (rough) · **Failure taxonomy tags** from this list: `requirements-miss`, `vocabulary-gap`, `ranking-miss`, `knowledge-gap`, `direction-invariant`, `render-defect-fixed`, `render-defect-remaining`, `tooling-limit`, `skill-helped`.
- `artifacts.json`: `{ "case": "<id>", "platform": ..., "stack": ..., "rendered": true|false, "render_mode": "native|html|html-twin|static-review", "screenshots": [...], "first_render_defects": n, "final_defects": n, "iterations": n, "guidance_relevant": n, "guidance_partial": n, "guidance_offtarget": n, "knowledge_gaps": [...], "ranking_misses": [...], "requirements_errors": [...], "tags": [...] }`.
- Screenshots `render/first-*.png`, `render/final-*.png`.

Be factual. A skill that gave you nothing useful is a valid result; write that down. Do not pad the verdicts.
