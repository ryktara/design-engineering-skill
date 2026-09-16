# New architecture: design-engineering

Decision record for the skill in `design-engineering/`. Each section states the decision, the alternatives considered, and why they were rejected.

## 1. Identity and scope

**Decision.** Name: `design-engineering` (command `/design-engineering`). Responsibility: understand product, users, environment, input modality, platform, constraints, and the existing implementation; derive a design direction; implement it in the project's conventions; verify by rendering. It is a design-engineering intelligence system, not a style catalogue.

**Rejected.** Keeping upstream's "searchable styles/palettes/fonts" identity: it optimises for catalogue counts and produces palette-and-pattern lookups that ignore platform and task. A sibling-skill pack (design, brand, slides…): out of scope for serious product work and a major activation-overlap risk.

## 2. Pipeline (real control flow)

```
request ─► classify (modes, platforms, inputs, products, screens, density, stacks, negatives; activation proxy)
        ─► inspect_project (stack, platform, tokens, fonts, components, breakpoints, a11y/focus mechanisms) ─► KNOWN hints
        ─► direction (slot-by-slot structural choices with compatibility checks, fingerprint, a11y constraints, anti-patterns, ledger)
        ─► load references/platform/stack files that apply (progressive disclosure)
        ─► implement in the project's component/token model
        ─► deterministic checks (tokens.py contrast/validate/scale; fingerprint.py compare)
        ─► render, capture, inspect, fix (verification loop)
        ─► report with KNOWN / INFERRED / MISSING
```

Every arrow is optional for small tasks; SKILL.md tells the model to scale effort.

## 3. Knowledge model

**Decision.** JSONL records (one JSON object per line) in six files by kind, one shared schema: `id, kind, title, category, intent[], platform[], input[], product_fit[], screen_fit[], density, risk{a11y,perf}, use_when, avoid_when, compatible[], incompatible[], guidance, implementation{stack: note}, fingerprint{axis: value}, rank, provenance, source, version, keywords[]`. 220 records at v1 (88 patterns, 58 rules, 25 components, 20 anti-patterns, 15 directions, 14 charts).

**Why JSONL.** Editable line by line, diffable, validated by a 40-line function, no server, no dependency, loads in milliseconds, relationships expressible as id references, provenance per record. Records carry the dimensions upstream's CSVs could not: platform, input modality, screen type, density, compatibility, risk, provenance.

**Rejected.** CSV (flat, per-file schemas, no nested implementation notes, no relations); SQLite/FTS5 (a binary artifact to regenerate, harder to review in PRs, no benefit at 220–2,000 records); YAML (slower, ambiguous scalars); Markdown-only knowledge (not filterable); a vector database (no evidence lexical+structured retrieval is the bottleneck; adds a model dependency and non-determinism; benchmark shows the structured axis, not semantics, was the missing piece).

## 4. Retrieval

**Decision.** Deterministic hybrid in `de_core.py`:

1. Signal extraction from a phrase lexicon (`data/lexicon.json`): modes, platforms, inputs (explicit or implied by platform), products, screens, density (explicit or implied by product, capped for touch/remote platforms), stacks (which imply platforms), components, negative constraints, activation vocabulary. Each signal is labelled KNOWN or INFERRED; MISSING is derived.
2. Field-weighted BM25 (title 3, keywords 2, category 1.5, use_when 1.5, guidance 1) with per-token weights: platform/stack words that are already structural signals get 0.25 weight so a single rare token cannot dominate; the lexical score is normalised by the top candidate and by the record's weighted query coverage.
3. Structured boosts/filters: platform (hard exclusion when disjoint; +3 match / +2 any), input (+1.5 / exclusion when the record demands an input the platform lacks), mode (+2 primary / +1 secondary), product fit (+2.5 / +0.75 any / −1 mismatch), screen fit (+1.5 / −1 mismatch), density (+1 / −1 opposite), negative constraints (exclusion of pattern/component/direction records that recommend the excluded device; the "none" alternative and anti-patterns stay).
4. Score = 0.55·lexical + 0.45·structural + editorial rank prior (±0.1). Diversification caps results per category. Confidence from score and coverage; abstention with suggestions from vocabulary nearest-neighbours.
5. Explanation: each result lists lexical/structural components and the matched signals; rejected candidates and the reason are exposed with `--explain`.

**Rejected.** Pure BM25 with keyword-list routing (upstream): no platform/mode/screen axis, so "Android TV kiosk" returns Neumorphism. Embeddings: non-deterministic, dependency, and the failures were structural not semantic. Hand-tuned per-domain score floors: replaced by coverage-based confidence that does not need re-tuning when data grows.

## 5. Direction assembly (decision engine)

**Decision.** Thirteen slots (navigation, layout, density, surface, cards, typography, colour, motion, focus, CTA, imagery, icon, metadata) filled by retrieval restricted to that slot's patterns, structural evidence allowed without lexical overlap, density taken directly from the signal, compatibility enforced against already-chosen slots (`incompatible` relations both ways), alternatives and rejections recorded. The chosen patterns' `fingerprint` fragments compose the direction's fingerprint. Accessibility rules and anti-patterns for the same signals are attached. Output includes the ledger and a note that the codebase wins.

**Rejected.** Upstream's product → reasoning row → landing pattern + palette + font: assumes every screen is a landing page; no slot for navigation, density, focus, or metadata; no compatibility model. LLM-only direction (no tool): loses determinism, traceability, and the fingerprint by-product.

## 6. Deterministic tools

- `inspect_project.py`: manifests (package.json, gradle, csproj, pubspec, xcodeproj, AndroidManifest, components.json, tailwind config) plus a bounded content sample (≤4,000 text files, ignoring node_modules/build/caches) for CSS architecture, custom properties, fonts, media queries, a11y attributes, focus/DPAD/TV-focus APIs. Output is compact JSON + a markdown summary with KNOWN/INFERRED.
- `tokens.py`: WCAG 2.x relative luminance and contrast; semantic token validation (required roles, 16 pair checks per theme, state deltas, disabled weaker than secondary, hue-family sanity, TV-specific targets); platform-aware type scale; skeleton generation.
- `fingerprint.py`: 15-axis enumerated fingerprint, weighted structural vs cosmetic similarity, verdicts DISTINCT / COSMETIC-ONLY / NEAR-DUPLICATE, actionable report.
- `validate_skill.py`: frontmatter limits, SKILL.md size, path existence, one-level references, record schema and cross-references, stack-file coverage, lexicon/schema alignment, eval-case references, fingerprint values.

**Rejected.** A dozen micro-scripts; a generic plugin framework; screenshot-to-fingerprint automation (would pretend vision is deterministic; instead the model fills the fingerprint from what it observes and the comparison is exact).

## 7. Progressive disclosure

SKILL.md ≈ 110 lines: classification table, inspection rule, direction/search commands, reference routing, implementation rules, verification, scope. Fifteen references, five platform files, eighteen stack files, all linked directly from SKILL.md (one level), each self-contained, with a Contents section when long. Knowledge is retrieved by script and never bulk-loaded.

**Rejected.** A priority table with anti-patterns and a 25 KB quick-reference in the entry point (upstream); CLI-flag documentation in SKILL.md (moved to `--help` and docs).

## 8. Activation

Description states what the skill does, where (web, mobile, desktop WinUI/WPF/Avalonia, Android TV/tvOS/IPTV, kiosk), when (create/redesign/audit/refactor/fix/brand/screenshot), and what it is not for (backend, database, infrastructure, non-visual bugs). No catalogue counts. The eval suite keeps a deterministic activation proxy aligned with the description's vocabulary; real routing is done by Claude from the description.

**Rejected.** `paths:` scoping (UI work touches files everywhere); `disable-model-invocation` (the point is automatic use); a `when_to_use` addendum (redundant with the description).

## 9. Evaluation

Nine suites, 109 cases at v1: activation (30), retrieval (20), platform differentiation (3 multi-platform cases), brand (4), accessibility (14), anti-generic (12), existing-project fixtures (5), greenfield direction (6), tool contracts (15). Plus a benchmark harness that runs the same 18 queries through upstream and ours with human-authored relevant/off-target term lists.

Philosophy: cases are never edited to pass; each adjustment carries a dated `note`. Two such notes exist (platform suite: distinct-top and overlap semantics), both documented.

## 10. Distribution

One directory, junction/symlink or copy into `~/.claude/skills/`. No npm CLI, no mirrors, no templates. Python 3 stdlib only.

**Rejected.** Multi-assistant templating and mirrored asset trees (upstream): triples maintenance and produced the SKILL.md/template divergence observed upstream. A plugin marketplace package: unnecessary for private use; the structure is plugin-compatible if ever needed.

## 11. Phase 2 additions (2026-09-08)

**Requirements contract.** `build_requirements(query, project)` produces one `design-requirements/v1` object: mode, platform, input, product, screen, stack, density, components, jobs, constraints (preserve_existing_system, preserve_navigation, preserve_typography, no_new_dependencies, performance_sensitive, brand_system_present, input_only), accessibility flags, negative constraints, and the KNOWN / INFERRED / MISSING ledger with reasons, plus recorded conflicts. Evidence priority: explicit request > repository evidence > platform inference > default. `search` and `direction` consume the object; nothing re-classifies. Rejected: an enterprise schema with per-field confidences (no downstream consumer), and inferring web from product words (would silently invent a platform).

**Facet-aware composition.** Records carry a derived facet (component, layout, navigation, visual, interaction, accessibility, performance, process, direction, anti-pattern, data-viz, plus platform when platform-specific). Required facets come from the requirements (mode, platform, stated inputs, components). Selection: normal ranking → per-category cap → for each unmet required facet, swap in its best candidate if it scores ≥ 0.5 × top and ≥ 0.75 × the redundant item it replaces → re-sort. Rejected: a keyboard bonus constant (another fragile weight), learning-to-rank (no training data), strict quotas (artificial diversity).

**Statuses and exit codes.** CONFIDENT / PARTIAL / AMBIGUOUS / ABSTAIN; `advise.py` exits 0/3/4/5, 2 invalid input, 1 tool failure. Confidence labels are documented as uncalibrated fit indicators (held-out showed no monotonic relation to concept recall).

**Direction invariants.** Contextual checks (TV needs a 10-foot focus treatment and no pointer navigation; kiosk touch-first and not dense; dense products not spacious; audits attach accessibility; brand emits a full fingerprint; preservation and negative constraints honoured; no incompatible pairs) reported as `validation.violations`.

**Evaluation architecture.** development / regression / heldout groups; frozen manifests with SHA-256 for held-out and activation sets; independent generation by a subagent that saw only the label taxonomy; token-level concept matching; canonical benchmark JSON (method v2) with cold/warm timings; `release_check.py`.

## 12. Phase 3 additions (2026-09-09): generalisation

**Why.** Held-out v1 showed the Phase 2 retrieval did not generalise (10/145 acceptable, concept recall 0.184): universal operability rules never entered create-mode results, problem statements defaulted to `create`, TV vocabulary mismatched, states beyond loading/empty/error and environmental context were unmodelled.

**Concern model.** Sixteen stable concerns; records address several (`record_concerns`); `derive_concerns(requirements)` produces REQUIRED / RECOMMENDED / OPTIONAL with reasons from a documented policy (task shape and problem class, platform + input matrix, screen/subtype/component/data, risk and environment, constraints). Canonical concept ids (`CONCEPTS`, 56) normalise vocabulary; records declare them and the output labels them (`covers: …`).

**Guidance bundle.** Candidate generation (lexical + structural, environment-gated, negatives excluded) is separated from final selection: a deterministic greedy set cover picks core (what to build) and guardrails (rules/anti-patterns), variable size 5–8 (required coverage may reach 8, recommended only fills to 6). Every response carries concern coverage, concept coverage, bundle size, diversity, redundancy. Rejected: fixed k (k=5 lost coverage, k=8 cost bytes for nothing), returning every universal rule (a checklist dump nobody reads), learned weights (no training data), embeddings (no evidence they beat the concern model on this corpus and they would cost determinism).

**Requirements contract v1 extensions (additive).** `screen_subtype[]`, `environment[]`, `jobs[]`, `problems[]`, `risk`. Problem statements → audit/polish/accessibility with `create` only when a build verb is present. Cautious platform inference (`platforms_inferred`: "Android", "SaaS", "portal", "laptop") yields INFERRED plus a MISSING "confirm" entry, never KNOWN.

**Knowledge.** Seven evidence-backed records (offline/sync states, persistence/session states, shared-device privacy, field use, TV sign-in, setup checklist, interruptive upsell); concepts/keywords/concerns added to ~80 existing records; no record copied from upstream.

**Evaluation.** `guidance` development suite from failure classes; regression cases from real Phase 3 failures; held-out v1 re-run as historical data (scored on the bundle, with the k=5 search recall kept as a reference column); blind held-out v2 with structured expectations and pre-registered thresholds; torture tests on real projects (`research/phase3-projects/`); `release_check.py --heldout-v1 --heldout-v2 --projects --real-activation`.

## 13. Phase 4 additions (2026-09-09): semantic coverage and codebase-compatible decisions

**Why.** Blind held-out v2 (Phase 3) met 3 of 8 thresholds: concept recall 0.21, mode 61 %, abstention 70 %, concern-policy agreement 0.60; the torture tests showed directions that ignored the existing navigation and theme.

**Scope model** (`de_semantic.classify_scope`): deterministic domain classification (UI_DESIGN / UI_INTERACTION / UI_ACCESSIBILITY / UI_IMPLEMENTATION / FRONTEND_RUNTIME / BACKEND / DATA / INFRASTRUCTURE / BUILD_TOOLING / UNKNOWN); a technical prompt is out of scope unless it carries a user-visible symptom; out-of-scope returns a reason and the nearest supported UI task. Activation (the frozen proxy) and internal scope are different decisions.

**Task-intent model** (`task_intent`, `derive_modes`, `change_budget`): existing-vs-new, problem-vs-request, facet (visual / interaction / accessibility), diagnose-vs-modify, redesign, preservation targets; cues only count in combination; explicit lexicon modes outrank inferred ones; primary + secondary modes with evidence strings; contradictory instructions become a recorded conflict (AMBIGUOUS). Change budget: low / moderate / high / greenfield.

**Concept ontology** (concept-policy/v1): 109 concept ids in 23 namespaces, each one reusable design requirement; `RELATIONS` (requires with cycle check, related, conflicts); 145 records labelled, slot patterns and directions intentionally not. `derive_expected_concepts(requirements, concerns)` turns concerns into concrete REQUIRED / RECOMMENDED / OPTIONAL concept ids with reasons, conditional on platform, input, screen, subtype, component, job, problem, risk, environment and mode (states only with async/submission evidence; charts only with data evidence; media/onboarding/dashboard jobs).

**Guidance bundle v2** (`guidance-bundle/v2`): greedy set cover whose utility counts new required concepts (×2), required concerns, recommended coverage, relevance, minus contamination (product/screen/category mismatch, low record purity, preserved navigation or typography), minus token cost; anti-patterns lose ties to positive rules; a rule that is the most relevant record for the wording stays a guardrail; metrics add `concept_coverage_ratio`, `bundle_tokens`, `coverage_per_1k_tokens`, `mean_purity`, `contaminated`. Rejected: an optimizer package, embeddings (no controlled evidence yet), returning every universal rule.

**Codebase-aware direction.** `inspect_project.py` emits `design_context` (design-context/v1): navigation topology, theme polarity (with dual-theme default), surface strategy, radius, spacing base, typography family/features, component library, each KNOWN / INFERRED / UNKNOWN with evidence and never claiming visual understanding. Requirements carry it as repository evidence (`project_context`, ledger entries `project_*`), below explicit request and above platform inference. `direction()` maps context to slot patterns, applies the change budget (`BUDGET_FREEDOM`, brand keeps navigation and workflow, accessibility/platform may override under a low budget) and emits a per-slot compatibility table (preserved / changed / new, reason) plus preservation metrics; unjustified structural change is a validation violation.

**Evaluation.** Development suites `scope`, `mode`, `context` (real Phase 3 projects as fixtures) written before implementation; 15 real-project tasks over 9 applications (11 modifying existing UI) with design-context correctness, preservation metrics and defect types; held-out v3 (≥ 300 blind cases, structured concept expectations, thresholds and stability labels pre-registered in `evals/heldout-v3/THRESHOLDS.md`, generator / expectation reviewer / bundle-quality reviewer separated); v1 and v2 re-run once as historical, non-blind data.

## 14. Phase 5 additions (2026-09-09): platform evidence, task semantics, concept generalisation, native context

**Why.** Blind held-out v3 met 6 of 9 thresholds; the misses were mostly *no platform detected* rather than wrong platform, `create` where a change mode was expected, and required concepts never demanded. Phase 5 changed only the four layers responsible and froze everything else (scope architecture, concern model, requirements contract, bundle architecture, set-cover strategy, change budget, preservation model, tokens, benchmark and release infrastructure).

**Platform semantic resolution** (`de_semantic.PLATFORM_EVIDENCE`, `resolve_platform`): every platform phrase is typed (explicit, stack, form-factor, modality, OS, environment, repository, product) and graded DIRECT / STRONG_INFERENCE / WEAK_INFERENCE; candidates are resolved with device-class precedence (a named device beats a framework; a TV or kiosk beats a phone mention unless the phone is the subject), negations and "not a browser" rewrites; WEAK evidence alone yields UNKNOWN plus a MISSING confirm entry, never a wrong platform. Requirements expose `platform_evidence` (candidates, strengths, weak_only, unknown). Repository platforms confirm wording (no confirm entry when the repository already states it); "on phones" against a web project is a viewport (web + responsive), not a platform switch.

**Task/mode semantics v2** (`task_intent`): `artifact_state` new / existing / unknown, `operations` (create, inspect, diagnose, modify, polish, restructure, redesign, compare, review, validate), `problem_domain`, `change_scope` local / screen / flow / system, `utterance` observation / request / question; present-tense observations and determiner-led sentences about a screen are existing UI; spec-shaped noun phrases ("an online store for ...") are new; explicit verbs keep the highest priority; a proper noun such as "the Add Habit sheet" is not a create verb. `derive_modes` maps existing-plus-defect by lead domain (layout: audit + refactor; visual: polish + audit; accessibility: accessibility + audit; responsive: responsive + audit). Multi-mode credit and a confusion matrix (`evals/mode_confusion.py`) are part of the evaluation.

**Expected-concept generalisation**: an alias layer (`ALIASES`, `normalize_phrase`, `alias_concepts`; each alias maps to exactly one concept, validated) turns natural wording into concept ids before any lexicon match; job / screen-subtype / environment / risk tables and derivation rules (modal words demand dialog focus, exceptions-first demands colour-not-only and glanceable status, a spinner demands progress feedback and live status, gestures demand a keyboard alternative); saturation keeps the top 8 required concepts by priority phase (named in the request, then job / screen / environment, then mode / states, then platform generics); `--explain` emits a `concept_trace` (JSON and Markdown) naming, per required concept, the candidate records, the selected carrier, and the earliest wrong layer when uncovered. Five concept ids were added (114 total); no ontology explosion.

**Native design-context extraction** (`inspect_project.py`): typography, surfaces, radius and spacing on SwiftUI / Compose / WinUI / WPF / Avalonia / Flutter and on Svelte / Vue templates (resource dictionaries, `CornerRadius`, `Thickness`, `x:Double` spacing keys, font lists, `Font.system`, Tailwind border / rounded / tabular-nums classes); a monospace face used for codes never defines the UI family; README-declared kiosks make web the substrate rather than the platform; README environment hints (outdoor, gloves, public) enter requirements; product hints are word-bounded (a `stores.ts` file no longer makes a clinic an e-commerce product). Precision fixtures with misleading identifiers (`ListView`, `NavigationView`, `isTVEnabled`, `darkText`, `MobileSettings`) guard the detectors.

**Direction on existing systems.** With a low or moderate change budget on an existing system, slots the task does not mention stay "as implemented" (only a genuinely new screen may pick layout, cards, CTA, metadata or imagery freely); a repository that already handles focus keeps its focus treatment (an accessibility task verifies it instead of replacing it); media-only patterns never fill a slot without a media signal; density is preserved unless requested.

**Evaluation.** Phase 5 development cases were written before implementation for platform evidence (87), task intent (122, 96 without explicit verbs), guidance and context; a real-project qualification round of 22 tasks over 12 codebases ran on a frozen build (hash recorded per task) with pre-registered per-task expectations, real concept recall, BAD-guidance categories and failure routing by earliest wrong layer; its findings produced 63 further cases (`evals/development/p5r-*.json`) and a second frozen candidate; held-out v4 (434 blind cases, three separated roles, two model families) was generated after the freeze and run exactly once. Results: `research/PHASE5-RESULTS.md`.

## 15. Phase 6 additions (2026-09-10): stability hardening (surgical)

**Why.** Blind held-out v4 (Phase 5) showed three aggregate defect classes in the human review — generic concern-filling guardrails, wrong-screen / wrong-product core records, missing critical concepts — and a 44 % platform-UNKNOWN rate. Phase 6 changed only the layers responsible (expected-concept criticality, bundle selection, contamination, situational platform evidence) and left the scope model, requirements contract, concern model and record schema untouched. No v4 case was opened; only the aggregate classes drove the work.

**Bundle purity (guidance-bundle/v3, `select_bundle`).** Every candidate gets `task_evidence` flags (strong / weak wording, screen, subtype, component, job, explicit product, platform, problem, explicit demand of a critical concept, repository) and every concept it would cover gets a `coverage_quality`: DIRECT (focused record with task fit for a critical concept), SPECIFIC (task fit), GENERIC (concept only), INCIDENTAL (side note of unrelated guidance). Core records need positive task evidence (a screen-specific composite needs screen evidence; a visual pattern on a local change needs an explicit demand; a direction needs product-and-screen/job evidence or a build task with a stated product family). Selection order is critical required concepts → core → most relevant rules → other required concepts (GENERIC admitted only with wording, a problem statement, high risk or a focused low-priority carrier) → specialist rules where a critical concept is carried only by a composite → recommended (DIRECT / SPECIFIC with task fit only). There is no soft minimum: bundles are 1–8 records, an explicit stop condition (marginal utility ≤ 0.5) ends each phase, `marginal` per record (new critical / required / recommended concepts, specificity, evidence, quality, contamination, tokens) is exposed under `--explain`, and `not_surfaced` lists recommended concepts that had no sufficiently specific carrier. Coverage is a diagnostic, not an objective.

**Wrong-screen / wrong-product guards.** Screen families (discover / inspect / commit / configure / consume / monitor) make a hard mismatch (checkout record on a search task) a 0.7 contamination; job–category affinity; a chart needs numeric wording before a compare job admits it; platform-only records without platform evidence are penalised; product mismatch is waived only for focused explicit carriers of a critical concept, never for composites; literal token traps (`neutralize_token_traps`: the Tab key, a landscape orientation, a cookie / loading overlay, a remote office, a terminal building, a poster-sized print, a member profile, a payment card, "compare two files") are neutralised in a small deterministic list with context windows before retrieval, alias matching and product detection.

**Critical concepts first.** Required concepts carry `priority` (0 named in the request, 1 screen / job baseline, 2 derived, 3 platform generic) and `critical` (priority ≤ 1). Criticality is conditional: platform generics are recommendations on static or non-interactive tasks; a narrow task (one named principle, modify-type operations, no stated job, no end-to-end wording) keeps only the named concept required and demotes the rest to recommendations (TV / kiosk baselines and states around submit / save / upload excepted); an accessibility review demands keyboard operability and, on touch platforms, target size. The concept trace reports `critical`, `concept_priority` and the `carrier_quality` of the selected record; the markdown output has three layers — CORE, CRITICAL GUARDRAILS, OPTIONAL NOTES (omitted when empty).

**Situational platform inference.** Evidence phrases are grouped into families (environment, input, viewing distance, form factor, runtime, OS, repository, product); two WEAK clues from independent families with no competing strong platform resolve as a compound STRONG_INFERENCE (a clue counts once even when several synonyms match; weak rivals block); ambiguous wording ("large display", "remote office dashboard", "phones and laptops") stays UNKNOWN or falls to web. `evals/platform_confusion.py` prints the expected × resolved matrix (resolved-correct / unresolved / resolved-wrong and the resolution rate).

**Evaluation.** 150 situational platform cases and 159 purity cases (pairwise wording, screen pairs, platform pairs, small bundles without filler) were written before the code; guidance cases that asserted concern *coverage* were relaxed with dated notes because coverage is now diagnostic. One record was added (`mobile-orientation-size-classes`, no carrier existed for orientation / size classes); the process rules (`impl-reuse-before-new`, `impl-safe-modification`, `verify-render-and-inspect`) were audited against SKILL.md §2 / §7 and left in place: they enter 2 of 281 development bundles and only with repository evidence.

**Outcome.** Candidate c4 was judged by an implemented project round (32 tasks / 16 codebases, round failed 4 of 9 criteria) and by blind held-out v5 (525 cases, 5 of 11 thresholds; wrong-screen and platform bars met, critical recall, human quality and scope-as-scored failed, 78 empty bundles counted as abstentions). Verdict: personal-production-ready, unchanged; phase-chasing stops (`research/PHASE6-RESULTS.md`).

**Disclosure.** During Phase 6 a patch script truncated `scripts/de_core.py`; it was rebuilt from the Phase 4 backup plus every recorded Phase 5 / 6 patch and re-validated (all suites), but the Phase 5 candidate hash `50966e8e…` can no longer be reproduced byte-for-byte. Scripts are now backed up to the session scratchpad before every patch.

## 16. Known trade-offs

- Lexicon-based classification is precise but only as broad as its phrase lists; new vocabulary requires editing `lexicon.json` (validated, tested).
- Structured boosts are hand-set constants; they are documented and covered by evals and the benchmark, but they are still constants.
- Fingerprints describe structure, not pixels; the model must fill them honestly for existing screens.
- The knowledge base is intentionally small (227 records); coverage gaps are handled by abstention, `uncovered_required_concerns`, and the references, not by guessing.
- Concern derivation is hand-written policy; it is explainable and testable but it will be wrong for tasks nobody anticipated. Held-out v2 measures how often.
