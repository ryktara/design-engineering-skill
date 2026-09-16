# StockRoom

Internal warehouse inventory app for Warehouse 2. Tracks products, on-hand quantities against reorder points, supplier details and the stock adjustments made against each SKU. This repo is the front-end only; it currently runs against a deterministic in-memory dataset so it can be demoed and screenshot-tested without the API.

## Stack

- Vue 3 (`<script setup>`, TypeScript)
- Vite 5
- Pinia for state
- Vue Router 4 (history mode)
- Plain CSS with custom properties, no UI library

## Getting started

```sh
npm install
npm run dev        # http://localhost:5173
```

Production build:

```sh
npm run build      # outputs to dist/
npm run preview    # serves dist/ on :4173
```

## Screens

| Route              | View                    | Notes                                                      |
| ------------------ | ----------------------- | ---------------------------------------------------------- |
| `/`                | Dashboard               | KPI tiles, recent adjustments, items needing reorder       |
| `/products`        | Products                | Filter bar (category, supplier, low stock) + product table |
| `/products/:sku`   | Product detail          | Overview / Movements / Supplier tabs, archive dialog       |
| `/adjustments`     | Stock adjustments       | New adjustment form and full adjustment history            |
| `/suppliers`       | Suppliers               | Supplier table with product and low-stock counts           |
| `/settings`        | Settings                | Theme toggle, warehouse preferences                        |

## Project layout

```
src/
  components/   in-house UI pieces (AppButton, DataTable, FilterBar, KpiTile, AppDialog, StatusBadge, …)
  data/         seeded sample data (200 products, 12 suppliers, 30 adjustments)
  stores/       Pinia stores: inventory, ui
  styles/       tokens.css (design tokens) and base.css (reset + shared classes)
  views/        one file per route
  router.ts
```

## Design language

- **Shell:** 56 px top bar (product name, global search, user menu) and a 240 px left navigation. The content area scrolls independently.
- **Theme:** light by default, with a dark palette toggled from Settings via `data-theme="dark"` on `<html>`. Both palettes live in `src/styles/tokens.css`.
- **Colour:** primary indigo `#3F51B5`; neutral greys for surfaces and borders; green / amber / red for stock status.
- **Surfaces:** flat, bordered panels (`.panel`) with no drop shadows except popovers and dialogs.
- **Shape:** 6 px corner radius everywhere.
- **Spacing:** 4-pt scale (4 / 8 / 12 / 16 / 24 / 32) exposed as `--space-*`.
- **Type:** IBM Plex Sans loaded from Google Fonts with a system fallback stack; IBM Plex Mono for SKUs and references.
- **Components:** everything is in-house; there is no third-party component library.

## Conventions

- Views are thin; anything reused twice becomes a component.
- Formatting helpers live in `src/utils/format.ts`.
- Sample data is deterministic (seeded PRNG) so screenshots are reproducible.
