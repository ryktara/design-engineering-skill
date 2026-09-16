# Phase 4 concept coverage audit (2026-09-09)

Data: `research/runs/phase4-concept-audit-raw.json` (every record before Phase 4: id, kind, category, concerns, concepts, platform, input, screen, product, risk, environment) and `research/runs/phase4-concept-audit.json` (after; adds tokens, before/after concept lists, orphan and breadth checks). The ontology itself is `scripts/de_semantic.py` (`CONCEPT_META`, `RELATIONS`, concept-policy/v1).

## Question asked

Are the design concepts reviewers expect missing from the knowledge base, or merely not structurally represented? Phase 3 held-out analysis said: mostly not represented (464 of 632 misses had the principle somewhere in the base). This audit went record by record.

## Numbers

| Item | Before | After |
|---|---|---|
| concept ids | 57 | 109 (namespaces: a11y, interaction, navigation, layout, state, form, table, data, adaptive, touch, tv, desktop, privacy, env, perf, content, brand, motion, onboarding, media, anti, process, feedback) |
| records declaring concept ids | 87 / 232 | 145 / 234 |
| records intentionally unlabelled | — | 89: the 15 `dir-*` direction records and 74 slot patterns (`nav-*`, `layout-*`, `density-*`, `surface-*`, `typography-*`, `color-*`, `motion-*`, `focus-*`, `cta-*`, `imagery-*`, `icon-*`, `metadata-*`, `card-*`). They are chosen by `direction()` per slot and by fingerprint, not by concept demand; labelling them would make aesthetic choices look like requirements. Six slot patterns that do carry a reusable principle are labelled (`nav-bottom-tabs`, `nav-wizard`, `nav-breadcrumb-tree`, `nav-command-palette`, `cta-toolbar-commands`, `layout-immersive-rails`, `cta-single-primary`, `card-none`). |
| orphan concepts (no record) | 0 | 0 (validator warns) |
| relations | 0 | 22 entries: 15 `requires` edges, `related`, 1 `conflicts`; no cycles (validator checks) |
| records with ≥ 4 concepts (watch for breadth) | 4 | 10 (`chart-realtime`, `comp-data-table` 5, `comp-form`, `comp-chart-container`, `comp-epg`, `comp-product-detail-page`, `comp-checkout-one-page` 5, `comp-plan-comparison` 5, `comp-mini-player`, `media-resume-and-details` 6) |

## Findings by class

1. **Reusable guidance with no concept id (58 records fixed).** All 14 chart records expressed "choose the form from the question" and "table alternative" only in prose → `data.chart_by_question`, `data.accessible_chart_alternative`, plus the specific idea (`data.kpi_comparison`, `data.realtime_window`, `data.exception_first`). Twelve components (menu, tabs, tree, drawer, command palette, sidebar, search, filters, pagination, media card, settings, hero) each carried one distinct interaction or structure principle → one id each. Process and platform rules (reuse-first, safe modification, render-verify, Fluent materials, desktop spacing/persistence, JS budget, font loading, token layers, dark-mode redesign) → `process.*`, `desktop.*`, `perf.js_budget`, `brand.*`. Anti-patterns → `anti.*` ids so exclusions and audits can demand them.
2. **Concepts only in prose, synonyms.** "10-foot", "readable at distance", "distance typography" → `tv.ten_foot_typography` (already); "last updated", "refresh", "live status" → `data.refresh_timestamp` / `data.realtime_window`; "which button", "primary action", "one CTA" → `layout.one_primary_action`; "continue watching", "resume", "where they left off" → `media.resume_playback`; "coach marks", "first-run tips", "tooltip tour" → `onboarding.feature_education`; "permission prompt", "priming" → `onboarding.permission_priming`. Query-side synonyms live in the lexicon (jobs, subtypes); record-side in `keywords` + `concepts`.
3. **Several distinct concepts expressed ambiguously (kept, with purity handling).** `comp-data-table` (5 concepts), `comp-checkout-one-page`, `comp-plan-comparison`, `media-resume-and-details` are legitimately composite components; instead of splitting them, the bundle selector computes `record_purity` (task-relevant concepts / concepts expressed) and applies a contamination penalty when a composite record would enter for one concept while its context (product, screen, category evidence) does not match. Evidence for a split was required (repeated real or blind failures) and none appeared; splitting is deferred.
4. **Duplicates.** `comp-player-controls` vs `tv-player-controls` (component vs rule; both keep `tv.player_autohide`), `comp-epg` vs `layout-epg-grid`, `comp-form` vs `layout-form-stack`: different kinds, same principle; the per-category core cap and concept-redundancy rule keep one in a bundle. No merge.
5. **Over-broad selection watch-list (Phase 3).** `grid-single-tab-stop` and `layout-states-empty-loading-error`: Phase 4 gates both by evidence rather than removing them — table-category records need grid/table evidence in the request (category contamination), and `state.loading_empty_error` is demanded only when the screen has asynchronous or submitted data (screen/component/job/word evidence), never for static pages. Development cases `g-grid-rule-not-for-*` and `g-states-not-universal-static` pin this.
6. **Mislabel caught during development.** `onboarding-first-run` initially carried `layout.one_primary_action` ("never cover the primary action") and displaced `cta-single-primary` on a "which button" task; relabelled. This is the failure the purity metric is meant to catch.

## Concept ontology principles (kept deliberately small)

One id = one reusable design requirement that several queries can need. No screen-specific ids. Relationships only where they change derivation (`table.inline_edit` requires keyboard navigation, visible focus and validation; `data.drilldown` requires orientation-and-back; `tv.no_touch_hover` conflicts with touch gesture concepts). The validator checks id validity, relation targets, `requires` cycles, orphans and concept→concern consistency for rules/components.
