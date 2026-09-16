# Upstream Audit: nextlevelbuilder/ui-ux-pro-max-skill

Audited revision: `4aad058` (main, 2026-09-08). Upstream cloned read-only into a scratch directory; nothing was modified.
License: MIT (Copyright 2024 Next Level Builder). Full text in `LICENSE` at repo root. Reuse is permitted with notice retention; see `NOTICE-SOURCES.md`.

## 1. What it is

A skill pack whose central artifact is `ui-ux-pro-max`: a Python 3 stdlib CLI (`search.py`) that does BM25 retrieval over ~35 CSV files, plus a "design system" generator that stitches the top rows from five CSVs into a MASTER.md. Six sibling skills (`design`, `design-system`, `brand`, `slides`, `banner-design`, `ui-styling`) ship in the same plugin. Distribution is an npm CLI (`ui-ux-pro-max-cli init --ai <platform>`) that renders a template into one of 20 assistant formats.

Repository facts (measured):

| Metric | Value |
|---|---|
| Files (excluding .git) | 680 |
| Copies of `data/` + `scripts/` | 3 (`src/`, `cli/assets/`, `.claude/skills/ui-ux-pro-max/`) plus `gallery/data/styles.csv` |
| `src/ui-ux-pro-max/data` size | 1.5 MB, of which `google-fonts.csv` is 747 KB (49%) |
| `SKILL.md` size | 16.2 KB (~4k tokens) |
| `references/` | `quick-reference.md` 24.8 KB, `pro-rules.md` 11 KB |
| Python tests | 160 tests + 7936 subtests, all pass locally in 24 s |
| Retrieval eval fixture | 90 human-graded cases, 8 metrics, regression-gated |

## 2. Real control flow (derived from source, not README)

```
SKILL.md loaded (whole 16 KB, every activation)
  └─ Claude picks a mode from the "Query Contract" prose:
       --design-system | --domain <d> | --stack <s>
       └─ search.py
            ├─ design-system  → DesignSystemGenerator.generate()
            │     1. search(query,"product",1)      → Product Type = category
            │     2. ui-reasoning.csv row for category (Style_Priority, Pattern, moods, Decision_Rules JSON)
            │     3. apply_decision_rules(): substring conditions (if_mobile, if_trust_needed…) → style/constraint/pattern/mode actions
            │     4. five BM25 searches (style/color/landing/typography + product) with mood words appended
            │     5. _select_best_match(): reasoning Style_Priority overrides BM25
            │     6. colour mode resolved from style + query, palette filtered by luminance
            │     7. optional dials (variance/motion/density) → keyword bias / GSAP snippet / spacing table
            │     8. format ascii|markdown|MASTER.md (+ fixed "Pre-Delivery Checklist")
            ├─ domain search → core.search()
            │     1. exact style-identity match (Style ID/Category/Aliases)
            │     2. else detect_domain(): keyword-phrase counting over 12 hard-coded keyword lists, ties broken by fixed order, default "style"
            │     3. per-domain query rewrite (drop routing words, map synonyms)
            │     4. BM25 (k1=1.5,b=0.75) over concatenated search columns of one CSV
            │     5. abstain if top score < per-domain floor or token coverage < floor
            │     6. suggestions via difflib when empty
            └─ stack search → core.search_stack(): status filter (active/deprecated) + BM25 over one stack CSV
```

There is no project inspection step, no platform detection, no task-mode detection beyond the three CLI flags, and no compatibility check between retrieved rows. Claude is asked (in prose) to detect the stack from `package.json` etc. by itself.

## 3. Architecture findings

**Source of truth and mirroring.** `src/ui-ux-pro-max/` is canonical; `cli/scripts/sync-assets.mjs` copies it to two other locations and a CI job fails if they drift. The reason given in CLAUDE.md is Windows symlink breakage. Result: every data or script change touches three identical files, and the hand-authored `SKILL.md` diverges from the template-generated one (`templates/base/skill-content.md`) used for other platforms. This is duplicated truth with a sync tax.

**Platform abstraction.** 20 platform JSON templates, all rendering the same body with a different path prefix and file name. Only Claude gets `references/`. The abstraction serves distribution breadth, not behaviour.

**Skill structure.** One skill, one entry script, two references. `SKILL.md` is a CLI manual (flags, dials, persistence semantics, retry policy) more than a design workflow. About 40% of it documents `--persist`, `--force`, dials, and output formats.

**Search architecture.** Verified in `core.py`: plain BM25 per CSV, no field weighting (all columns concatenated into one document), no phrase queries, regex used only for synonym normalisation, identity matching, and version-intent detection. Routing is keyword-list counting. Confidence is a per-domain absolute score floor (`_DOMAIN_SCORE_FLOORS`) tuned by hand ("values are intentionally conservative").

**Design generation.** Every design system output contains a *landing page pattern* (`Section Order`, `Primary CTA Placement`, `Conversion Optimization`) regardless of task. Running `"banking dashboard" --design-system` returned pattern "Trust & Authority + Conversion" with sections "Hero > Proof (logos, certs) > Solution overview > CTA" for what is an authenticated data application. The generator has no concept of screen type, platform, or input modality; `_detect_page_type` exists only for page-override files and is a substring list.

## 4. Retrieval findings (measured with the shipped CLI)

| Query | Auto-routed domain | Top 3 |
|---|---|---|
| design a banking dashboard | style | Data-Dense Dashboard, Bento Box Grid, **Brutalism** |
| audit the keyboard accessibility of an existing banking dashboard | ux | Skip Links, Keyboard Navigation, Focus Not Obscured (all `Platform: Web`) |
| create an Android TV banking kiosk UI | style | **Material 3 Expressive (Mobile)**, Zero Interface, **Neumorphism** |
| IPTV media browsing rails with remote control | style | *0 results, no suggestions* |
| WinUI desktop ERP data grid with keyboard shortcuts | ux | Keyboard Navigation (Web), Bulk Actions (Web), **Image Scaling (Web)** |

Observations:

- Routing distinguishes "design" from "audit" only because "accessibility" is in the `ux` keyword list; it does not represent task mode anywhere in the result.
- "TV", "kiosk", "remote", "DPAD" carry no signal: `grep -ri dpad data/` finds 2 occurrences (both inside `styles.csv` prose), `android tv` finds 0. There is no TV row in `ux-guidelines.csv` (Platform values: All 62, Web 47, Mobile 8, VisionOS 2).
- Stack CSVs are framework API guidelines (state hoisting, x:Bind, NavigationStack), not UI design guidance. `jetpack-compose.csv` has 52 rows, 2 on accessibility, 0 on focus/DPAD/TV.
- Result diversity is not managed; Brutalism appears third for "banking dashboard" purely on lexical overlap of "grid".
- Explainability: `--json` exposes `diagnostics` (score, margin, coverage) but nothing about *why* a row fits the product/platform.
- The relevance fixture (90 cases) is real and human-graded, and the regression gate is honest about being a floor, not a target (P@1 0.76, nDCG@3 0.84 on their own queries). This is the strongest engineering asset upstream has.

## 5. Knowledge model

Flat CSVs with per-file schemas. Relationships exist only as free text (`Best For`, `Do Not Use For`, `Anti_Patterns`) or as one join key (`Product Type` shared by `products.csv`, `colors.csv`, `ui-reasoning.csv`). There is no representation of:

- platform or input modality on styles, colours, typography, or landing patterns;
- density, hierarchy, or navigation model as first-class attributes;
- compatibility/incompatibility between patterns (only `Decision_Rules`, and 88% of activated conditions are `must_have`, `if_trust_needed`, `if_mobile`, `if_ux_focused`);
- provenance per row (`data-provenance.json` covers files, not rows; `ui-reasoning.csv` has `Reasoning` filled for 31/192 rows and `Confidence` for 31/192).

The product taxonomy (192 rows) is the spine, and it is a *marketing* taxonomy (SaaS, Micro SaaS, E-commerce Luxury…), which is why everything resolves to a landing-page pattern and a palette. The chain `product → users → environment → density → platform → navigation → layout → style → tokens → typography → components → motion → accessibility` is not expressible; only `product → style/palette/font/landing` is.

## 6. Skill activation

Description (447 chars): "UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, charts, and stack-specific UI implementation. Searchable local data: 79 searchable styles (50 active), 192 product palettes…"

- Broad by design ("designing, building, reviewing, or fixing interfaces"); acceptable, but 40% of the characters are catalog counts that carry no routing signal.
- Overlaps heavily with the sibling `design`, `design-system`, `ui-styling`, and `brand` skills in the same plugin, and on this machine with `frontend-design` (Anthropic), gstack `design-consultation`/`design-review`, and the `design:*` plugin. Nothing in the description says what it does *not* do or when a sibling is preferable.
- No TV, kiosk, remote, DPAD, or desktop-window vocabulary, so those prompts are unlikely to trigger it.

## 7. Context efficiency

Per activation: 16.2 KB SKILL.md (~4k tokens). Each search prints up to 3 rows with up to 21 columns each; a `--domain style` result is ~1.5–2.5 KB per row because `Implementation Checklist`, `Design System Variables`, and `AI Prompt Keywords` are emitted in full (`UNTRUNCATED_COLS`). `--design-system` prints ~3 KB ascii boxes. `quick-reference.md` (25 KB) is recommended "for a UI review/audit pass", so audits load ~45 KB before any project file is read.

Things that should be on demand but are inline: dials documentation, persistence semantics, output-format flags, the ten-row priority table with anti-patterns, and troubleshooting.

## 8. Generic-design risk (verified, not assumed)

- `products.csv` Primary Style Recommendation: "Glassmorphism" in 15/192 primary recommendations; "Vibrant & Block-based + Motion-Driven" 13; "Claymorphism + Vibrant" 9. Style is chosen *from the product label*, before any user, task, density, or platform signal.
- Every generated system includes a landing-page section order and CTA placement, even for dashboards, so the "hero + features + CTA" skeleton is structurally encouraged.
- The fixed Pre-Delivery Checklist hard-codes "Responsive: 375px, 768px, 1024px, 1440px" and "cursor-pointer on all clickable elements" into every MASTER.md, including native mobile and desktop outputs.
- Colour palettes are 192 near-identical Tailwind-derived sets (blue/indigo/emerald primaries dominate); `Card`/`Card Foreground` roles are mandatory in the schema, which assumes card-based composition.
- Positives: `Anti_Patterns` explicitly lists "AI purple/pink gradients" for many categories; styles carry `Do Not Use For`; `frontend-design` integration is documented in `stack/`.

Net: the architecture produces the generic SaaS landing skeleton with a palette swap by construction, because visual style is selected from a product label and page structure is always a marketing pattern.

## 9. Determinism split

Deterministic: BM25, domain routing, decision-rule application, luminance-based light/dark palette selection (`_relative_luminance` and `_contrast_ratio` exist in `design_system.py` but are used only to pick a palette, never to validate one), status filtering, persistence.
LLM-driven: everything about the actual design (hierarchy, layout, components, states, responsiveness, verification) plus stack detection.
Missing deterministic pieces: project inspection, contrast validation of proposed tokens, token schema validation, fingerprinting, any post-implementation check.

## 10. Engineering weaknesses (verified)

- Three mirrored trees + a CI sync check; `SKILL.md` hand-authored separately from the template used for every other platform.
- `validate_data.py` is 53 KB and is the largest script in the skill: schema drift is policed by code rather than prevented by structure.
- Hard-coded ranking constants (`_DOMAIN_SCORE_FLOORS`, `_STACK_THRESHOLD`, tie-break order, per-domain rewrite dictionaries) that must be re-tuned when data changes.
- `google-fonts.csv` (747 KB) is shipped to every install for a lookup that duplicates what the model already knows.
- Stack freshness tests pin framework versions (`react 19.2.x`, `nextjs 16.2`) that will rot.
- `_stack_query_requests_legacy` parses version intent with regexes; fragile but tested.
- Strong points: stdlib-only, snapshot-verified CSV reads, cached indexes, calibrated abstention with suggestions, honest regression gate, `Status`/`Parent Style ID` deprecation model.

## 11. What upstream does well (retained conceptually)

1. Zero-dependency Python tool executed by the agent instead of loaded into context.
2. Human-graded relevance fixture with explicit abstention measurement.
3. Explicit "0 results is not a match" instruction with suggestion terms.
4. Deprecation/alias model for identities.
5. Anti-pattern lists per category, including AI-gradient warnings.
6. The companion `stack/` repo's idea: knowledge + taste + browser feedback loop, with a multi-viewport audit script.

## 12. Root causes

1. Knowledge is organised by marketing product label, not by product/user/environment/modality, so every recommendation is a palette-and-pattern lookup.
2. Retrieval has no task-mode or platform axis; it only has "which CSV".
3. Nothing inspects the repository; stack detection is delegated to prose.
4. No post-implementation verification is part of the skill (the browser loop lives in a separate repo).
5. Distribution breadth (20 platforms, 3 mirrors, npm CLI) consumes most engineering effort.
