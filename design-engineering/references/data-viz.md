# Data visualisation

A chart answers a question. Choose the form from the analytical question and the data's shape; the knowledge base holds the per-form guidance (`advise.py search "<question>" --kind chart`).

## Contents
- From question to form
- Rules that prevent known mistakes
- Dashboards and real-time
- Accessibility of charts
- Colour
- Implementation notes

## From question to form

| Question | Form | Record |
|---|---|---|
| how does X change over time | line (1–6 series), area for single/cumulative, small multiples beyond 6 | `chart-trend-line`, `chart-small-multiples` |
| how do categories compare | bar (horizontal for long labels), sorted | `chart-compare-bar` |
| what share of the whole | stacked bar / waffle; donut only ≤4 parts | `chart-composition` |
| how is a variable distributed | histogram, box plot, strip for small n | `chart-distribution` |
| do two variables relate | scatter / bubble | `chart-relationship` |
| pattern across two categorical axes | heatmap / matrix | `chart-heatmap-matrix` |
| where do people drop off | funnel as step bars | `chart-flow-funnel` |
| how do quantities flow between states | Sankey | `chart-flow-sankey` |
| progress vs target | bullet graph / progress bar | `chart-progress-gauge` |
| where geographically | choropleth (rates) / symbol map (counts) | `chart-geo` |
| how certain is the forecast | bands and fans with a today marker | `chart-uncertainty` |
| what is happening now | rolling-window real-time chart | `chart-realtime` |
| one number | stat/KPI tile with comparison and sparkline | `comp-kpi-tile` |

Fewer than ~4 data points is a stat, not a chart. If the reader needs exact values, provide a table (optionally with conditional formatting) instead of or beside the chart.

## Rules that prevent known mistakes

- No pie charts with more than 4–5 slices; no 3D; no exploded slices; no donut without labels.
- Bar axes start at zero; line axes may not, but say so; no dual y-axes without a strong reason and clear labelling.
- Consistent time bucketing; missing data shown as gaps, not interpolated silently.
- Sorted categories unless order is meaningful; ≤15 categories per bar chart.
- No rainbow palettes for ordered data; diverging palettes have a meaningful neutral midpoint.
- No decorative animation; a single load transition at most; never animate on data refresh.
- Bubble area (not radius) encodes size; a size legend is present.
- Funnels as bars with counts and stage conversion, not trapezoids.
- Forecasts marked as forecasts with intervals; the boundary between actual and predicted is explicit.
- Legends replaced by direct labels where possible; otherwise a legend that is keyboard-reachable and toggles series.

## Dashboards and real-time

Modules sized by importance; the anomaly or key metric is the focal point; the same palette and mark style across all charts; shared time range control; fixed y-ranges with stepwise rescale for streams; thresholds drawn and labelled; alert states via colour + icon + text; "last updated" visible. Wall/TV displays: fewer panels, larger type, higher contrast, no hover-only values.

## Accessibility of charts

- Title states the question; unit and range visible; a text summary of the takeaway near the chart.
- Keyboard-reachable values (focusable marks, a data table toggle, or an accessible description per series); `role="img"` with `aria-label` summary on the web; Swift Charts audio graph and `accessibilityLabel/Value` per mark; Compose `contentDescription` summary.
- Colour never alone: line styles, markers, direct labels, patterns.
- Contrast ≥3:1 for marks against the background and adjacent marks where distinguishing them matters.
- Provide the data (table or export) for every chart.

## Colour

One categorical palette ≤8 (Okabe-Ito or a brand-tuned Tableau-like set), sequential and diverging ramps, dark-theme variants, kept out of the semantic action/status roles. Verify with a deuteranopia simulation.

## Implementation notes

Use the charting library already in the project; do not add one for a sparkline (inline SVG or CSS suffices). Lazy-load heavy chart bundles below the fold; render >2k points on canvas/WebGL; downsample time series; on native, prefer platform charts (Swift Charts) or the library the project already uses (Vico, MPAndroidChart, LiveCharts2, Syncfusion/DevExpress where licensed).
