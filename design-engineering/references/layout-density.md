# Layout, spacing, density, hierarchy

## Contents
- Spacing scale and grouping
- Density levels
- Layout topologies
- Grids and breakpoints
- Hierarchy
- States as layout
- Common defects and fixes

## Spacing scale and grouping

One scale per product: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 (px, dp, pt, epx as the platform dictates; TV multiplies by ~1.5–2). Rules:

- Inside-group spacing is smaller than between-group spacing by at least 1.5× (proximity is the grouping signal).
- One inset per container type (page, panel, card, list row) reused everywhere.
- Align left edges of text and controls across components; align icons to text baselines; equalise gaps in repeated structures.
- Never arbitrary values (13, 18, 22). "Spacing feels off" is nearly always a scale or grouping violation, not a colour problem.
- Windows: multiples of 4 epx (8 between related controls, 12 between groups, 16 to edges). Material: 4/8 dp grid. Apple: 8 pt rhythm with 16/20 margins.

## Density levels

| Level | Who | Base | Control height | Body | Table row |
|---|---|---|---|---|---|
| high | expert daily users on desktop/web with a pointer | 4 | 28–32 | 13–14 | 32–36 |
| medium | general users, touch + pointer | 8 | 40–48 | 16 | 44–52 |
| low | marketing, reading, TV, kiosk, brand-led | 8–16 | 48–56 (TV/kiosk ≥60) | 16–24 | n/a |

Density is bounded by input: touch cannot go high (targets), TV cannot go high (distance). Offer a density toggle (comfortable/compact) where audiences differ. Dense means more things visible at aligned sizes, not smaller text.

## Layout topologies

- single-column: phones, forms, reading, kiosks; width capped for measure; primary action reachable or sticky.
- form-stack: labelled fields in one column, titled sections, primary action at the end or in a sticky footer.
- master-detail: list pane + detail pane at ≥ ~900 px / 641 epx; collapses to list → detail with Back.
- table-first: toolbar + filters + table filling the viewport with internal scroll + optional side panel; virtualised.
- three-pane: tree/list/editor workbench at ≥1280 px; resizable, remembered, F6 cycling.
- dashboard-grid: 12 columns, modules sized by importance, reading order = importance, each module a region with states.
- grid-catalog: auto-fill columns from a minimum tile width, fixed aspect per catalog, filter bar reachable.
- feed: one column, dividers not cards, scroll restoration.
- editorial: measured column with asymmetric side content, sticky ToC on wide screens.
- rails (TV): rail titles, fixed focus pivot, focus memory, safe margins, lazy loading.
- immersive-hero-rails (TV): backdrop of focused item + rails; debounced crossfade; dual scrim.
- epg-grid (TV): 2-D virtualisation, sticky channel column and time header, now-line, focus by programme.
- canvas/player: full-bleed content with transient controls.

Choose by primary task (see design-reasoning.md). The direction tool proposes one; the codebase's existing topology wins for modifications.

## Grids and breakpoints

- Use the project's breakpoints (Tailwind `screens`, MUI, tokens) and prefer container queries for components.
- Windows: small <641, medium 641–1007, large ≥1008 epx; TVs count as small (effective pixels). Apple: size classes (compact/regular). Material: window size classes (compact <600, medium 600–839, expanded ≥840 dp).
- TV design frame: 960×540 dp (1080p at 2×); 12 columns of 52 dp with 20 dp gutters; safe margins 48/27 dp (up to 58/28); card counts per row at that width: 1×844, 2×412, 3×268, 4×196, 5×124 dp.
- Fluid content widths with min/max; no fixed-pixel containers.
- Desktop windows: minimum size defined; panes collapse in a documented order.

## Hierarchy

One focal element per screen (the thing the user came for): largest contrast in size/weight/position. Supporting information one step down; chrome (navigation, toolbars) two steps down and quieter than content. Dashboards: the focal point is the most important metric or the current anomaly, not the page title. Forms: the section the user is in. Media: the focused item.

Hierarchy comes from contrast between roles (size ≥1.25× jumps, weight, colour) not from decoration (borders, icons, backgrounds).

## States as layout

Empty, loading (skeleton with final dimensions), error (message + action, data preserved), partial (loaded parts shown, missing parts marked), long text (wrapping and clamping), zero and huge counts, first use. Each state occupies the same region as the content it replaces; on TV each state has a focusable element.

## Common defects and fixes

| Symptom | Cause | Fix |
|---|---|---|
| "looks busy" | no focal point; equal emphasis | demote all but one element; group with spacing |
| "looks unprofessional" | arbitrary spacing; misaligned edges; mixed radii | snap to scale; align; one radius per control class |
| "boxes in boxes" | cards used for grouping | headings + spacing + hairlines |
| "everything is huge" | display sizes used for headings; big KPI numbers | role scale; one display element |
| horizontal scroll on phones | fixed widths; tables | fluid widths; list rows |
| TV feels cramped | desktop density; no safe margins | rebuild at TV scale; 5% margins; rails |
| desktop feels like a phone app | 48 dp rows, huge padding, no menus | 4 epx grid, 32 epx controls, command bar + context menus |
