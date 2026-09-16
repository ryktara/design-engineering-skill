# Benchmark: upstream ui-ux-pro-max vs design-engineering (method v2)

Generated 2026-09-16 from `research/benchmark-results.json` by `evals/benchmark_upstream.py --render`; do not edit numbers by hand.
Upstream revision `15de38f`; ours: 248 records, de_core `c99a09ea3056`, cases `660a3223567b`; Python 3.14.5.

Scoring: fraction of human-listed relevant terms present in returned guidance (higher better) and fraction of off-target terms present (lower better). Term lists were authored by the skill author; this measures topical fit, not final UI quality.
Timing: cold = subprocess per query incl. interpreter start, both systems identically; warm = in-process, records preloaded, ours only (search k=5 and guidance bundle); 7 repetitions, median and p95.

## Aggregate

| Metric | Upstream | Ours |
|---|---|---|
| mean relevant-term coverage | 0.200 | 0.922 |
| mean off-target-term coverage | 0.189 | 0.148 |
| empty results | 3 | 0 |
| cold latency median / p95 (ms) | 139 / 244 | 377 / 473 |
| warm latency median (ms) | n/a | 144 |
| mean required-facet coverage | n/a | 0.764 |

Guidance bundle (Phase 3 `advise.py guidance`, same terms and scoring; additive column, method unchanged):

| metric | ours (guidance bundle) |
|---|---|
| mean relevant-term coverage | 0.921 |
| mean off-target-term coverage | 0.102 |
| empty results | 0 |
| warm latency median (ms) | 286 |
| mean bundle size / concern coverage / bytes | 5.67 / 0.891 / 4005 |

## By category (relevant-term coverage)

| Category | n | Upstream | Ours |
|---|---|---|---|
| accessibility | 2 | 0.500 | 1.000 |
| anti-generic | 1 | 0.167 | 1.000 |
| brand | 1 | 0.000 | 1.000 |
| dense | 1 | 0.286 | 1.000 |
| desktop | 2 | 0.322 | 0.857 |
| ecommerce | 1 | 0.125 | 1.000 |
| erp | 1 | 0.000 | 1.000 |
| finance | 1 | 0.000 | 0.857 |
| kiosk | 1 | 0.000 | 1.000 |
| landing | 1 | 0.286 | 0.571 |
| media | 1 | 0.375 | 0.875 |
| mobile | 2 | 0.000 | 0.785 |
| saas | 1 | 0.286 | 1.000 |
| tv | 2 | 0.214 | 1.000 |

## Per query

| Query | Upstream domain / top | rel ↑ | off ↓ | Ours signals / top | rel ↑ | off ↓ | status |
|---|---|---|---|---|---|---|---|
| design a SaaS analytics dashboard | product: Analytics Dashboard, SaaS (General), Smart Home/IoT Dashboard | 0.29 | 0.50 | []/['create']: anti-generic-sidebar-dashboard, dir-analytical-console, layout-dashboard-grid | 1.00 | 0.50 | CONFIDENT |
| ERP purchase order entry screen with line items | style: — | 0.00 | 0.00 | []/['create']: comp-data-entry-grid, table-column-disambiguation, card-list-row | 1.00 | 0.25 | CONFIDENT |
| e-commerce product listing page with filters | landing: marketplace-directory, pricing-page-cta, ai-personalization-landing | 0.12 | 0.67 | []/['create']: layout-grid-catalog, comp-filters, dir-utility-commerce | 1.00 | 0.00 | CONFIDENT |
| transactions table for a banking app | product: Banking/Traditional Finance, Fintech/Crypto, Restaurant/Food Service | 0.00 | 0.67 | []/['create']: layout-table-first, comp-data-table, data-tables-numeric | 0.86 | 0.00 | CONFIDENT |
| IPTV home screen with live channels and VOD rails on Android TV | style: material-you-md3-mobile, inclusive-design, accessible-and-ethical | 0.38 | 0.40 | ['tv']/['create']: layout-rails, dir-cinematic-media-tv, layout-immersive-rails | 0.88 | 0.00 | CONFIDENT |
| EPG program guide grid for a set-top box | style: bento-box-grid, editorial-grid-magazine, minimalism-and-swiss-style | 0.14 | 0.50 | ['tv']/['create']: layout-epg-grid, comp-epg, dir-broadcast-guide-tv | 1.00 | 0.00 | CONFIDENT |
| video player controls for Apple TV with subtitles | style: liquid-glass, bento-box-grid, kinetic-typography | 0.29 | 0.67 | ['tv']/['create']: tv-player-controls, layout-split-player, comp-player-controls | 1.00 | 0.33 | CONFIDENT |
| iOS onboarding flow for a fitness app | product: Fitness/Gym App, Booking & Appointment App, Citizen Science Platform | 0.00 | 0.00 | ['mobile']/['create']: nav-wizard, imagery-illustration, comp-setup-checklist | 0.57 | 0.00 | CONFIDENT |
| Jetpack Compose order list with swipe actions | style: — | 0.00 | 0.00 | ['mobile']/['create']: comp-list-row-mobile, mobile-gestures-discoverable, card-list-row | 1.00 | 0.33 | CONFIDENT |
| WinUI 3 inventory management window with navigation and data grid | ux: Accessibility, Layout, Navigation | 0.14 | 0.00 | ['desktop']/['create']: comp-data-table, desktop-keyboard-first, desktop-status-bar-and-error-navigation | 0.71 | 0.00 | CONFIDENT |
| WPF chart of accounts tree with breadcrumb | chart: Root Cause Analysis, Hierarchical / Nested Data, Performance vs Target (Compact) | 0.50 | 0.00 | ['desktop']/['create']: nav-breadcrumb-tree, comp-tree-view, layout-dashboard-grid | 1.00 | 0.33 | CONFIDENT |
| landing page for a developer tool | landing: pricing-page-cta, ai-personalization-landing, pricing-focused-landing | 0.29 | 0.00 | ['web']/['create']: dir-developer-tool, typography-monospace-technical, layout-editorial | 0.57 | 0.00 | CONFIDENT |
| dense monitoring dashboard for network operations | style: data-dense-dashboard, spectrum-design-system, bento-box-grid | 0.29 | 0.00 | []/['create']: layout-dashboard-grid, dir-analytical-console, chart-realtime | 1.00 | 0.25 | CONFIDENT |
| keyboard accessibility audit of a web admin panel | ux: Accessibility, Accessibility, Accessibility | 0.67 | 0.00 | ['web']/['accessibility']: a11y-keyboard-operable, a11y-skip-link, nav-left-rail | 1.00 | 0.00 | CONFIDENT |
| check colour contrast of our dark theme | color: Digital Signage / Kiosk, Wallpaper & Theme App, Photography Studio | 0.33 | 0.00 | []/['accessibility']: color-dark-mode-rules, tv-dark-first, a11y-contrast-text | 1.00 | 0.00 | CONFIDENT |
| make our four white-label brands visually distinct beyond colour and logo | color: Photography Studio, Space Tech / Aerospace, Wiki / Encyclopedia | 0.00 | 0.00 | []/['brand']: anti-brand-cosmetic-only, color-dominant-brand, color-neutral-accent | 1.00 | 0.00 | CONFIDENT |
| self-service check-in kiosk for a hospital | style: — | 0.00 | 0.00 | ['kiosk']/['create']: dir-public-kiosk, kiosk-public-use, nav-hub-spoke | 1.00 | 0.33 | CONFIDENT |
| the dashboard looks generic with cards everywhere | style: data-dense-dashboard, bento-box-grid, dimensional-layering | 0.17 | 0.00 | []/['polish']: anti-generic-sidebar-dashboard, anti-card-everything, card-none | 1.00 | 0.33 | CONFIDENT |

## Where upstream scored higher

- none in this set

## Ties

- none
