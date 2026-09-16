# Design direction: Add a team billing settings page with plan comparison, seat management table and invoice history to our Next.js SaaS admin

**KNOWN:** platform: web (project inspection); product: saas (request: saas, settings page); product: finance (request: invoice); stack: nextjs (request: next.js); stack: react (project inspection); stack: tailwind (project inspection); stack: shadcn (project inspection); screen: settings (request: settings); job: compare (request: comparison)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: create (default when no mode word is present)
**MISSING:** brand: no brand assets, guideline, or character description available

| Slot | Choice | Why |
|---|---|---|
| navigation | Persistent left rail / sidebar (`nav-left-rail`) | platform web, input keyboard,pointer,touch, mode create, product finance,saas, density high |
| layout | Table-first working screen (`layout-table-first`) | platform web, input keyboard,pointer, mode create, product finance,saas, screen mismatch, density high |
| density | High density (`density-high`) | density high (INFERRED) |
| surface | Bordered panes (`surface-bordered-panes`) | platform web, input keyboard,pointer, mode create, product finance,saas, density high |
| cards | Bordered cards (`card-bordered`) | platform web, input keyboard,pointer, mode create, product finance,saas |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | mode create, product finance,saas, density high |
| color | Dark canvas + accent (dark-first) (`color-dark-accent`) | platform web, mode create, product finance |
| motion | Functional minimal motion (`motion-functional-minimal`) | mode create |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | platform web, input keyboard,pointer, mode create |
| cta | Sticky action bar (`cta-sticky-bar`) | platform web, input pointer,touch, mode create, product finance,saas, screen mismatch |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | platform web, input keyboard,pointer, mode create, product finance,saas, density high |
| icon | Outline icon set, one weight (`icon-outline-system`) | platform web, mode create |
| metadata | Rich metadata (operational) (`metadata-rich`) | platform web, input keyboard,pointer, mode create, product finance,saas, density high |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- **layout** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- **color** — Canvas is a dark tinted neutral (not #000 unless OLED black is deliberate), surfaces step lighter with elevation, text primary ≈ 87–92% white not pure white, accent desaturated slightly for dark backgrounds, error/success re-tuned for dark contrast. On TV target ≥7:1 for body text and avoid saturated reds/oranges at large areas (bloom on cheap panels).
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Operational workbench** — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- **Data-entry grid (spreadsheet-like)** — Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.
- **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).

## Guardrails (required concerns: component, structure, states, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow).
**platform**
- Numeric tables: alignment, figures, units, precision: Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator.
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state.
**anti / patterns**
- Actions only on hover: Show on focus too, keep a visible affordance (overflow menu) for touch, and never on TV.

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "table-first",
  "grid_behavior": "virtualized",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "typography_character": "neutral-sans",
  "color_strategy": "dark-with-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- navigation: Tree + breadcrumb for deep hierarchies (0.398), Command palette as primary navigation accelerator (0.398), Top bar navigation (0.26)
- layout: Form stack with sections (0.435), Master–detail (list + detail pane) (0.33), Dashboard grid of modules (0.32)
- surface: Flat surfaces with tonal layers (0.278), Elevated cards as the primary container (0.256), Imagery-backed surfaces (0.193)
- cards: List rows (0.302), No card containers (dividers and spacing) (0.268), Flat tiles (0.248)
- typography: Serif editorial text (0.299), Geometric sans for product/tech brands (0.291), Monospace as identity for technical products (0.262)
- color: Neutral canvas + one accent (0.331), Multicolour by category (0.281), Dominant brand colour (0.183)
- motion: Spring-based physical motion (0.256), Expressive brand motion (0.226), Cinematic reveals (brand moments only) (0.163)
- focus: Underline / weight focus for text-first UI (0.2)
- cta: Toolbar / command bar with selection-driven commands (0.396), One primary action per screen (0.387), Contextual inline actions (0.247)
- imagery: No decorative imagery (0.367), Functional thumbnails (0.311), Illustration system (0.299)
- icon: Duotone icons as brand accent (0.153), Text-only, no icon system (0.153), Custom glyph set (0.043)
- metadata: Inline badges and status chips (0.355), Moderate metadata with a hierarchy (0.268), Minimal metadata (0.149)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
