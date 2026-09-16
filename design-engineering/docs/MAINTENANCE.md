# Maintenance

## Layout

```
design-engineering/
├── SKILL.md                 router: classify → inspect → direction → load refs → implement → verify
├── references/              on-demand knowledge, one level deep from SKILL.md
├── platforms/               web, mobile, tv, desktop, kiosk (override generic habits)
├── stacks/                  one file per stack group; keys must match de_core.STACK_GROUPS
├── data/
│   ├── lexicon.json         signal phrases (modes, platforms, inputs, products, stacks, components, negatives, activation vocab)
│   ├── patterns.jsonl       direction-slot options with fingerprints (navigation, layout, density, surface, cards, typography, color, motion, focus, cta, imagery, icon, metadata)
│   ├── rules.jsonl          UX / accessibility / platform / performance rules (with provenance)
│   ├── components.jsonl     component reasoning with per-stack implementation notes
│   ├── charts.jsonl         chart forms by analytical question
│   ├── antipatterns.jsonl   justification-demanding devices and process failures
│   └── directions.jsonl     coherent named directions (full fingerprints)
├── scripts/                 de_core.py (engine), advise.py (CLI), tokens.py, fingerprint.py, inspect_project.py, validate_skill.py
├── evals/                   run_evals.py, benchmark_upstream.py, cases/*.json, fixtures/
└── docs/                    INSTALL, USAGE, MAINTENANCE
```

Single source of truth: this directory. No mirrors, no generated copies.

## Record schema (data/*.jsonl)

Required: `id` (kebab-case, unique), `kind` (pattern|rule|direction|component|chart|antipattern), `title`, `category`, `intent[]` (modes), `platform[]`, `input[]`, `product_fit[]`, `density`, `risk{a11y,perf}`, `use_when`, `avoid_when`, `compatible[]`, `incompatible[]` (ids must exist), `guidance` (20–900 chars, imperative, specific), `provenance` (platform-standard | accessibility-requirement | engineering-practice | heuristic | aesthetic | internal-preference | upstream-derived-concept), `source`, `version`, `keywords[]`.
Optional: `implementation{stack-group: note}` (keys must have a `stacks/<key>.md`), `fingerprint{axis: value}` (values from `fingerprint.py init`), `rank` (0–100, lower preferred on near-ties; default 50).

Provenance discipline: subjective taste is `aesthetic` or `internal-preference`, never `platform-standard`. Cite the standard in `source` for platform-standard and accessibility-requirement records.

## Adding knowledge

1. Append a line to the right `.jsonl`; give it precise `use_when`/`avoid_when` and keywords that users would actually say.
2. Tag platform/input/product/density honestly (`any` only when true); TV/desktop/mobile-specific records must carry the platform so filtering works.
3. Run `python scripts/validate_skill.py` (schema, cross-refs, duplicates, fingerprint values, stack files).
4. Add or extend an eval case in `evals/cases/` that would have failed without the record; run `python evals/run_evals.py`.
5. If the record is a pattern in a direction slot, give it a `fingerprint` and a `rank`.

## Adding a stack

1. Add the key to `STACK_GROUPS` in `scripts/de_core.py`.
2. Add phrases in `data/lexicon.json` → `stacks` and a platform mapping in `stack_platforms`.
3. Add dependency/manifest detection in `scripts/inspect_project.py` (`DEP_MAP`, `GRADLE_MAP`, `DOTNET_MAP`, or a manifest branch).
4. Write `stacks/<key>.md` (conventions to detect, implementation rules, verification) and link it from SKILL.md.
5. Add `implementation.<key>` notes to the components that matter; add a fixture under `evals/fixtures/` and a case in `evals/cases/project.json`.

## Adding a platform

Add to `PLATFORMS`, `implied_inputs`, lexicon `platforms`, a `platforms/<name>.md`, records tagged with it, a platform eval case, and (if needed) stricter `tokens.py` pairs.

## Updating standards

Rules carry `source` and `version`. When WCAG, a platform HIG, or a framework changes: update the record's guidance and `version`, note the date in `source` if useful, and adjust eval expectations only when the standard changed (record the reason in the case's `note`).

## Tuning retrieval

Ranking lives in `de_core.py`: field weights (`FIELD_WEIGHTS`), structured boosts in `_structured()` (platform 3, input 1.5, mode 2, product 2.5/0.75/−1, density ±1), the 0.55/0.45 lexical/structural mix, rank prior ±0.1, and the routing-token removal in `_lexical_tokens()`. Change one thing, run the full eval suite and the upstream benchmark, and keep the numbers in `research/BENCHMARK-RESULTS.md` honest.

## DesignRequirements contract (schema `design-requirements/v1`)

`de_core.build_requirements(query, project)` is the single classifier. It returns: `mode[]`, `platform[]`, `input[]`, `product[]`, `screen[]`, `stack[]`, `density`, `components[]`, `primary_jobs[]`, `constraints{preserve_existing_system, preserve_navigation, preserve_typography, no_new_dependencies, performance_sensitive, brand_system_present, input_only}`, `accessibility{keyboard, screen_reader, focus, touch_targets, reduced_motion, contrast}`, `negative_constraints[]`, `known[]`, `inferred[]`, `missing[]` (each entry carries a reason), `conflicts[]`, `source{request, project}`, `evidence{…}`, `activation{…}`. `validate_requirements()` is the schema check; `compact_requirements()` is the context-sized view the CLI prints.

Evidence priority (do not change without a case): explicit request statement > direct repository evidence (`inspect_project.py` output) > platform inference (stack → platform, platform → input, product → density capped on touch/remote) > default (`create`). A repository value that contradicts the request is recorded in `conflicts` and the request wins. Stack words never count as platform evidence. Web is never inferred from product words. `search()` and `direction()` take `requirements=`; pass the same object to both so retrieval and direction agree.

`python scripts/advise.py requirements "<request>" --project .design-inspect.json [--pretty] [--explain] [--full]`.

## Facets and result composition

Each record has derived facets (`de_core.record_facets`): kind/category → component | layout | navigation | visual | interaction | accessibility | performance | process | direction | anti-pattern | data-viz, plus `platform` when the record is platform-specific. `required_facets(req)` lists the concerns a result set must cover for the request's mode/platform/inputs (contextual, capped at k−1). `select_with_coverage` swaps an unmet facet's best candidate in for a redundant item only when it scores ≥ 0.5 × top and ≥ 0.75 × the item it replaces. Every search result reports `coverage.{required_facets, required_facets_satisfied, required_facets_unmet, facet_coverage, category_diversity, duplicate_pressure, swaps}`; evals can assert on them (`expect_facets`, `min_facet_coverage`, `max_duplicate_pressure`). Never add a query-specific rule; fix facet policy or data.

## Concern model and guidance bundle (Phase 3)

`CONCERNS` (16): structure, navigation, component, interaction, accessibility, content, data-display, adaptive, states, feedback, performance, privacy, environment, brand, motion, anti-pattern. A record's concerns come from `record_concerns()` (kind/category defaults in `_PATTERN_CONCERNS`, `_RULE_CONCERNS`, `_COMPONENT_CONCERNS`) or an explicit `concerns` field. `CONCEPTS` are canonical ids for recurring principles (`table.tabular_figures`, `interaction.focus_restore`, `tv.ten_foot_typography`…) declared in records' `concepts` and labelled for output by `CONCEPT_LABELS`; the validator warns about ids no record carries.

`derive_concerns(req)` is policy, not statistics (edit it only with a development case first):

1. task shape (mode; problem class visual/interaction/accessibility/general);
2. platform + input matrix (`INPUT_CONCEPTS`): web always requires keyboard navigation, hover independence and visible focus; desktop keyboard + focus; touch platforms minimum target; TV/remote D-pad reachability, focus restoration, visible focus, 10-foot type, safe margins; kiosk adds environment + privacy;
3. screen / subtype / component / data (forms → feedback + validation; data screens → data-display + tabular figures; player on remote → auto-hide + BACK; `SUBTYPE_CONCERNS`/`SUBTYPE_CONCEPTS` for epg, data-grid, wizard, sign-in, rails…; marketing pages → content + brand, states only recommended);
4. risk (high → confirmation; sensitive product on shared screen → privacy) and environment (`ENVIRONMENT_CONCEPTS`; KNOWN environment → required, inferred → recommended);
5. constraints (negatives → anti-pattern; performance-sensitive → performance).

`select_bundle()` (deterministic greedy set cover): core = best component/direction/chart records with lexical evidence, then patterns, one per category, no incompatible pairs (3, or 2 for audit/review/accessibility); a rule scoring ≥ 0.9 × top with lexical evidence ≥ 0.5 is always a guardrail; then for each uncovered REQUIRED concern the candidate with the largest required-coverage gain (required concepts ×2 + required concerns) within 0.6 of that concern's best score, core kinds preferred for build concerns (component/structure/navigation/brand/data-display) and rules/anti-patterns otherwise; then uncovered required concept ids; then RECOMMENDED concerns/concepts. Budget: required coverage may grow the bundle to 8, recommended coverage only fills to 6, thin bundles are filled to 5 (`BUNDLE_MIN/SOFT/MAX`). The k experiment (`research/runs/phase3-k-experiment-dev.json`) is why: variable matched k=8 coverage at k=7 bytes.

Status: CONFIDENT = every required concern covered, ≥ 50 % of required concepts covered, platform not merely inferred; PARTIAL otherwise; AMBIGUOUS/ABSTAIN from the requirements contract. `direction()` consumes the bundle: guardrails are grouped (interaction, accessibility, platform, states, feedback, privacy/environment, anti-patterns) and an uncovered required interaction concern is a validation violation.

## Pipeline and failure diagnosis (Phase 4)

Every bug is assigned to the **earliest** incorrect layer of this pipeline, and fixed there:

```
user prompt → scope (de_semantic.classify_scope) → mode (task_intent + derive_modes; evidence exposed) → requirements (build_requirements)
→ concerns (derive_concerns) → expected concepts (derive_expected_concepts, concept-policy/v1) → candidate retrieval (candidates)
→ bundle selection (select_bundle, guidance-bundle/v2) → direction (direction; change budget + compatibility) → project adaptation (inspect_project design_context)
→ implementation → visual verification
```

Examples. "Users lose their place after closing the TV details screen" with no `interaction.focus_restore` in the bundle: scope ✓, mode ✓ (audit), platform ✓, concern ✓ (interaction), **concept missing** → fix `derive_expected_concepts` (a `details`/`resume` job demands `interaction.focus_restore`), not BM25 weights. "Polish this existing light-theme WPF screen" that receives a dark command-palette direction: requirements ✓, bundle ✓, **direction/project-context** → fix the inspector's theme/navigation detection or the preservation policy, never retrieval keywords.

Scope: `de_semantic._TECH` (per-domain phrases), `_UX_SYMPTOMS` (user-visible symptoms that keep a technical prompt in scope), `_UI_WORDS`; a trailing `*` allows suffixes. Mode: `_EXISTING / _PROBLEM / _CHANGE / _CREATE / _DIAGNOSE / _NO_CHANGE / _REDESIGN / _LOOKFEEL / _STRUCTURAL` cue lists, combined in `derive_modes`; explicit lexicon modes outrank inferred ones; `change_budget` is derived from the modes and intent. Concepts: `CONCEPT_META` (id → label, primary concern), `RELATIONS` (requires / related / conflicts), `INPUT_CONCEPTS`, `JOB_CONCEPTS`, `SUBTYPE_CONCEPTS`, `ENVIRONMENT_CONCEPTS`; states are demanded only with async/submission evidence (`ASYNC_WORDS`, never `STATIC_WORDS` pages). Bundle: utility = 2·new required concepts + new required concerns (+1 / +0.5 recommended) + 0.8·relevance − contamination (product/screen/category mismatch, low purity, preserved navigation/typography) − 0.25·tokens/300; anti-patterns lose ties to positive rules; contamination ≥ 0.5 excludes. Direction: `CONTEXT_SLOT_PATTERNS` maps detected context to slot patterns, `BUDGET_FREEDOM` / `BRAND_FREEDOM` say what each budget may change, `A11Y_OVERRIDE_SLOTS` what accessibility may force. Inspector: `NAV_SIGNALS`, theme configuration lists, radius/spacing/weight regexes; `NAV_WEIGHT` down-weights secondary structures (breadcrumb, wizard).

## Phase 5 layers: platform evidence, intent v2, aliases, concept trace

The pipeline gains an explicit **platform** layer between scope and mode:

```
scope -> platform (resolve_platform: typed, graded evidence; UNKNOWN over wrong) -> mode (task_intent v2: artifact_state / operations / problem_domain / change_scope / utterance) -> requirements -> concerns -> expected concepts (aliases first, then job / screen / environment tables) -> candidate retrieval -> bundle selection -> direction -> project adaptation
```

- **Platform** (`de_semantic.PLATFORM_EVIDENCE`): add phrases under the right type and strength; a DIRECT device phrase suppresses framework-only candidates; WEAK phrases may only ever produce a MISSING confirm entry. Cases: `evals/development/platform-evidence.json` (`expect_platforms`, `acceptable`, `forbid_platforms`, `expect_strength`, `expect_unknown`, `expect_inputs`). A repository platform confirms wording; "on phones" on a web project is a viewport (`_FORM_FACTOR_WORDS` in `de_core`).
- **Intent** (`task_intent`): `_EXISTING_CUES`, `_NEW_CUES`, `_DEFECT_PATTERNS`, `_QUESTION_PATTERNS`, `_OP_CUES`, `_DOMAIN_CUES`, `_SCOPE_CUES`; screen names that contain a verb ("Add Habit sheet") are rewritten before cue matching. Cases: `evals/development/mode-intent.json` (`expect_intent` with `_any` keys). Run `python evals/mode_confusion.py` after any change.
- **Aliases** (`ALIASES`): natural phrases map to one concept id each (the validator rejects a phrase mapped twice; when two concepts follow from one phrase, map the phrase to one and add a derivation rule in `derive_expected_concepts` for the other). `concept_for_phrase` is the evaluator's canonical lookup.
- **Concept trace**: `advise.py guidance "<task>" --explain` (Markdown) or `--json --explain` prints, per required concept, `covered` / `UNCOVERED` with the earliest wrong layer (`expected-concepts` never demanded, `candidate-retrieval` no carrier admitted, `bundle-selection` dropped by cap or utility, or a knowledge gap when no record carries the id). `python evals/concept_diagnostics.py` aggregates the same decomposition over the development guidance cases.
- **Scope with a repository**: a sentence with no technical vocabulary and no UI noun is in scope when a project inspection is supplied (the repository is the UI); decisive technical phrases (`_DECISIVE_TECH`, per domain) still abstain, and activation defers to a decisive abstention.
- **Real-project qualification**: `research/phase5-projects/PROTOCOL.md` (pre-registered `00-expectation.json` before any advise call, build hash at start and end, concept recall against the expectation, BAD categories, failure routing); `python evals/rescore_projects.py --label <candidate>` re-runs the skill steps for every task on the current build and scores them against the same expectations; `python evals/build_hash.py` prints the frozen-build hash. Never edit the skill while task agents run; a fix produces a new candidate hash and a rescoring.

## Phase 6 layers: criticality, bundle purity, situational platform evidence

- **Criticality** (`de_semantic.derive_expected_concepts`): `priority` 0–3 and `critical` on every required concept; narrow-task demotion; conditional platform generics. A missing critical concept is routed to *expected concepts* (alias or derivation rule) before anything else; a critical concept carried only by a composite is a *candidate compatibility* problem (add a focused rule only if no carrier exists and the failure repeats).
- **Bundle purity** (`de_core.task_evidence`, `coverage_quality`, `core_evidence_ok`, `select_bundle`): read `--explain` → `marginal` (why each record entered, its quality and contamination) and `omitted` / `not_surfaced` (why a record or a recommended concept did not). A generic guardrail in a bundle is a *bundle selection* defect: the fix is the admission rule, never a keyword on the record. A wrong-screen core record is a *candidate compatibility* defect: screen family, job affinity or a token trap.
- **Token traps** (`de_core._TOKEN_TRAPS`): a literal word that names a component or screen but means something else in context. Add a trap only for a demonstrated failure, with a context window, and keep the list small; the replacement token must not itself be a lexicon word.
- **Situational platform evidence** (`de_semantic.PLATFORM_EVIDENCE`, `EVIDENCE_FAMILY`, `_evidence_families`): WEAK phrases resolve only as a compound of two independent families. Check `python evals/platform_confusion.py` after any change: resolved-wrong must stay at 0 on the development sets; a lower unresolved count is the goal, never at the cost of a wrong platform.
- **Output layers**: CORE / CRITICAL GUARDRAILS / OPTIONAL NOTES. Bundles have no soft minimum (1–8). Do not add a minimum back: "no guidance" beats generic guidance.
- **Backups**: copy `scripts/de_core.py` and `scripts/de_semantic.py` to the session scratchpad before running any patch script; never open a file for writing before its content has been read into memory.

## Multi-layer fixes

Most real failures need more than one layer. Order: (1) regression case; (2) lexicon (vocabulary: modes, problems, platforms_inferred, environment, jobs, screen_subtypes, negatives) — prefer this for wording gaps; (3) record `keywords`/`concepts`/`concerns` (a record exists but is not found or not credited); (4) new record only with a development case and a source; (5) `derive_concerns` policy (a concern should have been demanded); (6) `select_bundle` (right candidates, wrong composition); (7) scoring constants last. After each layer: `run_evals.py` + `validate_skill.py`. Never read held-out cases to decide a fix; use aggregate failure classes only, and record that in the phase results.

## Eval groups and discipline

`evals/development/` (tuning allowed; `guidance.json` asserts concerns/concept ids, never wording), `evals/regression/` (real defects; every case needs a `note`; never removed while valid), `evals/heldout/` (v1, frozen, no longer blind after Phase 3 analysis: historical comparison only), `evals/heldout-v2/` (blind in Phase 3; inspected at class level since: historical), `evals/heldout-v3/` (blind; structured expectations with concept ids, expected scope/modes/platform, forbidden concepts, required preservation; thresholds and stability labels in `THRESHOLDS.md` written before generation; `MANIFEST.json` records the thresholds hash; plus an independent bundle-quality review via `evals/dump_bundles.py`). Development suites `scope.json`, `mode.json`, `context.json` (real Phase 3 projects as fixtures) cover the Phase 4 layers. `evals/activation/` holds the frozen 180-prompt set; `activation_metrics.py` computes precision/recall/FPR/FNR (proxy, and `--real` when the CLI is authenticated).

Fix order for any observed failure:

```
real failure observed
↓ add a regression case that fails today (note: date, source, symptom)
↓ classify the cause: lexicon | knowledge | scoring | facet coverage | compatibility | project inspection | skill routing
↓ smallest architectural fix (no query-specific hacks, no new global constant without a documented reason)
↓ run development + regression (python evals/run_evals.py) and validate_skill.py
↓ do NOT re-run held-out to check the fix; held-out is measured once per release (release_check.py --heldout) and results archived in research/runs/
```

Statuses: CONFIDENT / PARTIAL / AMBIGUOUS / ABSTAIN drive CLI exit codes (0/3/4/5). `confidence` (high/medium/low/none) is an uncalibrated fit indicator; do not present it as a probability.

Benchmark: `python evals/benchmark_upstream.py --upstream <clone>` writes `research/benchmark-results.json` (method v2) and renders `BENCHMARK-RESULTS.md`; never type benchmark numbers by hand; `validate_skill.py` fails when Markdown drifts from the JSON. Increment `METHOD` when scoring rules change.

Release: `python evals/release_check.py [--heldout-v1] [--heldout-v2] [--heldout-v3 [--human-review verdicts.json]] [--projects] [--real-activation]` (`--heldout-v3` prints the pre-registered threshold verdict and the label inputs; `--projects` aggregates both `research/phase3-projects/*/artifacts.json` and `research/phase4-projects/*/artifacts.json`). Historical sets (v1, v2) are reported as non-blind.

## Eval philosophy

Never edit a case to make the implementation pass. A failure is a defect, a wrong case (fix it and write why in `note`), or an ambiguity (document it). Keep regression cases for every defect found. Activation cases test the deterministic proxy; Claude's real routing depends on the SKILL.md description, so keep the description's vocabulary and `lexicon.json` aligned when you change either. `evals/probe_activation_with_claude.py` asks a real model the same questions; it needs the `claude` CLI logged in for non-interactive use (`claude -p` prints "Not logged in" otherwise) and aborts rather than scoring silently when the CLI does not answer YES/NO.

## Upgrading for new Claude versions

Re-read the current skill authoring guidance (frontmatter limits: name ≤64 chars kebab-case, description ≤1024 chars third person, SKILL.md body <500 lines; Claude Code listing cap 1536 chars description+when_to_use) and the model prompting page. Remove cargo-cult instructions (no forced step-by-step narration, no "CRITICAL/MUST" shouting, no redundant self-check loops); keep instructions explicit, one level of references, deterministic scripts for deterministic work. `validate_skill.py` enforces the structural limits.

## Release checklist

`validate_skill.py` OK → `run_evals.py` all OK → `benchmark_upstream.py` re-run if retrieval changed → update `research/*` numbers → bump `version` fields on changed records.
