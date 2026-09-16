# Design direction: our React energy dashboard looks cramped and inconsistent, facility managers complain the numbers are hard to read and they don't know which button to press

**KNOWN:** platform: web (project inspection); stack: react (request: react); screen: dashboard (request: dashboard)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); mode: polish (problem statement (visual): looks cramped, cramped, inconsistent, hard to read); mode: audit (follows from visual problem statement)
**MISSING:** brand: no brand assets, guideline, or character description available

| Slot | Choice | Why |
|---|---|---|
| navigation | Persistent left rail / sidebar (`nav-left-rail`) | platform web, input keyboard,pointer,touch |
| layout | Dashboard grid of modules (`layout-dashboard-grid`) | platform web, input keyboard,pointer,touch, screen dashboard |
| density | Low density / spacious (`density-low`) | platform web |
| surface | Flat surfaces with tonal layers (`surface-flat-tonal`) | lexical |
| cards | No card containers (dividers and spacing) (`card-none`) | mode polish |
| typography | Serif editorial text (`typography-serif-editorial`) | platform web |
| color | Multicolour by category (`color-multicolour-semantic`) | lexical |
| motion | Functional minimal motion (`motion-functional-minimal`) | mode polish |
| focus | Underline / weight focus for text-first UI (`focus-underline`) | platform web, input keyboard,pointer |
| cta | Contextual inline actions (`cta-contextual-inline`) | platform web, screen dashboard |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | platform web, input keyboard,pointer |
| icon | Outline icon set, one weight (`icon-outline-system`) | platform web |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | lexical |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- **layout** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **density** — Whitespace must come from a scale (e.g. 24/40/64/96), not arbitrary padding; keep line length in measure; big type is only justified for the one thing that should be read first. Spacious does not mean everything is huge.
- **surface** — Define three tonal steps per theme with measured contrast (each step ≥1.1:1 apart and borders ≥3:1 where they mark boundaries). Shadows reserved for transient layers (menus, dialogs, drag). Reads professional at any density and avoids the 'everything is a floating card' look.
- **cards** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts.
- **typography** — A text serif with optical sizes (e.g. Source Serif 4, Literata, Newsreader, Fraunces for display, Spectral) at 17–19 px body with 1.5–1.6 line height; UI chrome (buttons, labels) stays in a sans to keep controls crisp.
- **color** — Category colours from a colour-blind-safe categorical palette, always paired with a label or icon, kept out of the action/status roles; neutrals for everything else so the categories stand out.
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — Text links: 2 px underline + background tint on focus (≥3:1); buttons/inputs still get the standard ring. Never remove the ring globally to protect the aesthetic.
- **cta** — Actions are visible (not hover-only), consistently placed per item type, and grouped: at most one emphasised per item. Hover-reveal is allowed only as an addition to a visible affordance and never on touch/TV.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Core guidance (components / layouts to build)
- **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default.
- **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
**accessibility**
- One clear focal point per screen: Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title.
**anti / patterns**
- Arbitrary spacing and misaligned edges: Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change.

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "dashboard-grid",
  "grid_behavior": "responsive-columns",
  "content_density": "low",
  "surface_strategy": "tonal-layers",
  "card_geometry": "none",
  "corner_language": "small",
  "typography_character": "serif-editorial",
  "color_strategy": "multicolour-semantic",
  "motion_character": "functional-minimal",
  "focus_strategy": "underline",
  "cta_strategy": "contextual-inline",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "moderate"
}
```

## Validation: OK

## Alternatives considered
- navigation: Tree + breadcrumb for deep hierarchies (0.344), Top bar navigation (0.294), Command palette as primary navigation accelerator (0.2)
- layout: Table-first working screen (0.276), Catalog grid (0.132), Master–detail (list + detail pane) (0.132)
- density: High density (0.24), Medium density (0.196)
- surface: Bordered panes (0.347), Imagery-backed surfaces (0.289), Elevated cards as the primary container (0.22)
- cards: List rows (0.23), Bordered cards (0.22), Landscape media cards (16:9) (0.203)
- typography: Monospace as identity for technical products (0.19), Rounded friendly sans (0.19), Grotesk display + quiet body (0.183)
- color: Duotone identity (0.238), Dark canvas + accent (dark-first) (0.203), Dominant brand colour (0.183)
- motion: Spring-based physical motion (0.22), Expressive brand motion (0.19), Cinematic reveals (brand moments only) (0.163)
- focus: Visible focus ring (web/desktop) (0.287)
- cta: Toolbar / command bar with selection-driven commands (0.335), One primary action per screen (0.253), Sticky action bar (0.092)
- imagery: Immersive backdrop (0.298), Poster art as primary recognition (0.203), Hero imagery on landing/brand pages (0.183)
- icon: Text-only, no icon system (0.283), Duotone icons as brand accent (0.153), Custom glyph set (0.079)
- metadata: Rich metadata (operational) (0.24), Inline badges and status chips (0.193), Minimal metadata (0.149)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
