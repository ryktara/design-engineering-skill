# Design direction: Purchase order lines grid for our WPF ERP client; clerks enter 200 lines a day with the keyboard

**KNOWN:** platform: desktop (project inspection); input: keyboard (request: keyboard); product: erp (request: erp, purchase order); stack: wpf (request: wpf)
**INFERRED:** input: pointer (implied by platform desktop); density: high (implied by product erp); mode: create (default when no mode word is present)
**MISSING:** brand: no brand assets, guideline, or character description available

| Slot | Choice | Why |
|---|---|---|
| navigation | Command palette as primary navigation accelerator (`nav-command-palette`) | platform desktop, input keyboard (stated), mode create, product erp, density high |
| layout | Table-first working screen (`layout-table-first`) | platform desktop, input keyboard (stated), mode create, product erp, density high |
| density | High density (`density-high`) | density high (INFERRED) |
| surface | Bordered panes (`surface-bordered-panes`) | platform desktop, input keyboard (stated), mode create, product erp, density high |
| cards | List rows (`card-list-row`) | platform desktop, mode create |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | mode create, product erp, density high |
| color | Neutral canvas + one accent (`color-neutral-accent`) | mode create, product erp |
| motion | Functional minimal motion (`motion-functional-minimal`) | mode create |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | platform desktop, input keyboard (stated), mode create |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | platform desktop, input keyboard (stated), mode create, product erp, density high |
| imagery | No decorative imagery (`imagery-none`) | mode create, product erp, density high |
| icon | Outline icon set, one weight (`icon-outline-system`) | platform desktop, mode create |
| metadata | Rich metadata (operational) (`metadata-rich`) | platform desktop, input keyboard (stated), mode create, product erp, density high |

## Guidance per slot
- **navigation** — Global shortcut (Ctrl/Cmd+K), fuzzy search over commands and records, recent items first, arrow-key navigation with aria-activedescendant, Escape closes and restores focus. Every command in the palette must also exist somewhere visible.
- **layout** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- **Operational workbench** — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- **Many series or groups → small multiples** — Identical axes across panels (state if not), consistent ordering, panel titles as data labels, shared legend/colour meaning, grid sized so each panel keeps a readable aspect; lazy-render offscreen panels.

## Guardrails (required concerns: structure, states, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction.
**states**
- Search and filters: visible state and instant feedback: Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails.

## Fingerprint
```json
{
  "navigation_model": "command-palette",
  "layout_topology": "table-first",
  "grid_behavior": "virtualized",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "typography_character": "neutral-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "none",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- navigation: Persistent left rail / sidebar (0.476), Tree + breadcrumb for deep hierarchies (0.456), Desktop menu bar + toolbar commands (0.436)
- layout: Dashboard grid of modules (0.622), Three-pane workbench (0.542), Master–detail (list + detail pane) (0.52)
- surface: Flat surfaces with tonal layers (0.26), Translucent (glass) layers, justified (0.115)
- cards: Bordered cards (0.4), Flat tiles (0.358), No card containers (dividers and spacing) (0.25)
- typography: Platform system font (0.284), Monospace as identity for technical products (0.28), Humanist sans for approachable products (0.167)
- color: Dark canvas + accent (dark-first) (0.221), Monochrome with typographic hierarchy (0.145), Multicolour by category (0.137)
- motion: Crossfade and shared-element continuity (0.111)
- cta: One primary action per screen (0.27), Contextual inline actions (0.211)
- imagery: Functional thumbnails (0.333), Data graphics as the visual layer (0.31)
- icon: Platform icon set (0.294), Custom glyph set (0.191)
- metadata: Inline badges and status chips (0.337), Minimal metadata (0.297), Moderate metadata with a hierarchy (0.25)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
