# Sources, provenance, and licence notices

This workspace contains an original skill (`design-engineering/`) built after studying the open-source project **nextlevelbuilder/ui-ux-pro-max-skill** (MIT License, Copyright (c) 2024 Next Level Builder; revision `4aad058`, inspected 2026-09-08). The upstream project was treated as read-only input to an engineering investigation, not as a specification.

## Upstream licence and what it requires

MIT permits use, copying, modification, and redistribution provided the copyright notice and permission notice are included in copies or substantial portions of the Software. Full text: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE

## Directly reused components

None. No upstream file, dataset row, CSV, script, template, wording block, schema, or test fixture was copied into `design-engineering/`. All knowledge records, scripts, references, evals, and documentation were written new for this workspace. The upstream branding ("UI UX Pro Max", "uipro") is not used anywhere in the skill.

Because no substantial portion of the upstream Software is included, the MIT notice-retention condition is not triggered; the notice above is kept as a courtesy and for provenance.

## Concepts inspired by upstream (reimplemented independently)

- A zero-dependency Python CLI that the agent executes instead of loading knowledge into context.
- Explicit "no result is not a result" handling with suggested vocabulary when retrieval abstains.
- Per-record anti-pattern warnings (including AI-gradient defaults) and per-category "avoid when" guidance.
- A human-authored relevance fixture with regression gating (upstream's `relevance-cases.json` idea); ours is a different schema, different queries, different grader.
- Deprecation/alias thinking for identities (we use `rank` and `incompatible` relations instead of parent/alias columns).
- The companion `stack/` repository's idea that knowledge + taste + a browser feedback loop must be combined (we integrate verification into the skill itself).

Knowledge records that trace to this category carry `provenance: "upstream-derived-concept"` if any are added in future; at present none do, because every record was authored from primary standards or original synthesis.

## Rewritten / redesigned (no code lineage)

- Retrieval: field-weighted BM25 with structured platform/input/mode/product/density filtering and boosts, negative constraints, diversification, explanation, and a KNOWN/INFERRED/MISSING ledger (`scripts/de_core.py`). Upstream is single-field BM25 per CSV with keyword-list domain routing.
- Design generation: slot-based direction assembly with compatibility checking and fingerprints, instead of product-label → landing-pattern + palette + font.
- Knowledge model: JSONL records with intent/platform/input/product/density/risk/provenance/compatibility, instead of flat CSVs keyed by marketing product type.

## Completely new

`inspect_project.py` (repository inspection), `tokens.py` (WCAG contrast, semantic token validation, type scale), `fingerprint.py` (brand structure comparison), `validate_skill.py`, the eval suite and benchmark harness, all references, platform files (including TV, desktop, kiosk), stack files, and the direction/anti-generic/brand-differentiation architecture.

## Third-party standards referenced (not copied)

Guidance in the references and records paraphrases publicly documented standards and platform guidelines, cited in each record's `source`: W3C WCAG 2.2 and the ARIA Authoring Practices Guide; Android TV design guides (design principles, navigation on TV, layouts, focus system, color on TV, typography), Compose for TV documentation; Apple Human Interface Guidelines (iOS, macOS, tvOS); Material Design 3; Microsoft Windows app design (content layout and spacing, screen sizes and breakpoints, Fluent materials); ISA-101 HMI principles; Core Web Vitals documentation; Anthropic's skill authoring best practices and model prompting guidance; the Anthropic `frontend-design` skill's public description of AI default aesthetic clusters (used as calibration, not copied).

Font names mentioned are trademarks of their owners; no font files are bundled. Licences for any font must be verified at implementation time.

## Skill licence

`design-engineering/` is private work for the workspace owner. No licence is granted to third parties by this file.
