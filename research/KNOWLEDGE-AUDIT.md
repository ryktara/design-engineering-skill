# Knowledge-base quality audit (Phase 3, 2026-09-09)

Source data: `research/runs/phase3-knowledge-audit.json` (script output; 221 probe queries = development guidance/retrieval/accessibility/anti-generic/platform cases + held-out v1 queries, run through `guidance()`).

## Inventory

| Item | Count |
|---|---|
| records | 232 at freeze (pattern 88 · rule 63 · component 31 · antipattern 21 · direction 15 · chart 14); audit probes ran on the 227-record build, refreshed on the freeze |
| provenance | heuristic 95 · platform-standard 62 · accessibility-requirement 22 · aesthetic 21 · engineering-practice 14 · internal-preference 13 |
| records declaring concept ids | 87 (57 concept ids, every id carried by ≥ 1 record) |
| records with explicit `concerns` | 42 (the rest derive from kind/category) |
| records with stack implementation notes | 41 |
| platform-specific records | 152 |

## Findings and actions

1. **Never selected by the bundle across 221 probes (31 records).** Three groups:
   - direction-slot aesthetics patterns (`color-duotone`, `typography-humanist-sans`, `imagery-poster`, `metadata-rich`, `surface-bordered-panes`, `card-poster-landscape`, `motion-cinematic`, `cta-contextual-inline`, `icon-text-only`, `layout-editorial`…): expected — they are consumed by `direction()` slots, not by the bundle. Kept.
   - process rules (`impl-reuse-before-new`, `impl-safe-modification`, `verify-render-and-inspect`): carry no concern on purpose; SKILL.md already states them. Kept, excluded from bundles.
   - genuine long tail (`a11y-semantics-structure`, `a11y-text-scaling`, `anti-fashion-over-usability`, `anti-mobile-desktop-shrunk`, `chart-composition/-progress-gauge/-relationship/-uncertainty`, `desktop-density-spacing`, `desktop-fluent-materials`, `dir-learning-platform`, `dir-social-feed-mobile`, `mobile-perf-images-overdraw`, `web-hydration-js-budget`): correct records that no probe demanded. Kept; watch in held-out v2 (Phase 4). `a11y-text-scaling` and `a11y-semantics-structure` now carry concept ids (`a11y.text_scaling`, `a11y.semantics`) so accessibility-mode tasks can demand them.
2. **Over-selected (227-record probe):** `anti-no-states` (87/221) and `search-filter-feedback` (28/221). On the freeze the most-selected are `layout-states-empty-loading-error` (96), `grid-single-tab-stop` (61), `a11y-keyboard-operable` (44) — the positive states rule now wins the tie and the new grid rule is demanded by every desktop/web data task; the latter is worth watching for over-selection in Phase 4. The first is legitimate (states is required for most create tasks) but it beat the positive rule on ties; fixed by preferring rules over anti-patterns on ties. The second was off-target (a search-specific rule satisfying generic feedback/states concerns); fixed by narrowing its concerns to component+feedback and adding `screen_fit` search/list/dashboard.
3. **Near-duplicate titles (token Jaccard ≥ 0.5):** `comp-form`/`layout-form-stack`, `comp-sidebar-nav`/`nav-left-rail`, `comp-player-controls`/`tv-player-controls`, `comp-epg`/`layout-epg-grid`, `comp-wizard-stepper`/`nav-wizard`. Each pair is a component vs. a layout/navigation pattern or a rule; they cover different concerns and the bundle's per-category cap keeps them from crowding a result. No merge.
4. **Thin records:** `anti-hover-only-actions` guidance < 120 chars (acceptable for an anti-pattern); eleven direction-slot patterns have < 4 keywords (they are selected structurally by slot, not lexically). No change.
5. **New records (12)** each have a source, a development case, concept ids and concerns: from Phase 2 gap analysis `states-offline-and-sync`, `states-persistence-and-session`, `shared-device-privacy`, `mobile-field-use`, `comp-tv-sign-in`, `comp-setup-checklist`, `anti-interruptive-upsell`; from the torture tests `comp-product-detail-page`, `comp-checkout-one-page`, `comp-plan-comparison`, `comp-mini-player`, `grid-single-tab-stop`. Nothing copied from upstream.
6. **Vocabulary fixes on existing records** (keywords/concepts/concerns): ~80 records; the notable ones are the TV vocabulary gaps identified in Phase 2 (10-foot typography, pinned channel column, auto-hide timing, column priority) and problem-statement synonyms (cramped, inconsistent, logged out, loses answers, pop-up).

## Open gaps (not added; no evidence-backed case yet)

- Print stylesheets, email-client rendering, progressive enhancement as a rule, Siri Remote swipe semantics as a separate record, Windows Fluent materials depth (only one record), WinUI `AutomationProperties` specifics, adaptive `NavigationView` behaviour. Each appeared once in held-out v1 free-form concepts; they will be added when a real project or a repeated held-out v2 class demands them.
