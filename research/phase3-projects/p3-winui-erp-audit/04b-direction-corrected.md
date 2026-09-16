# Design direction: Warehouse clerks say our WinUI stock adjustments page is confusing and they keep missing rows; the screen reader reads the status column as just text

**KNOWN:** platform: desktop (project inspection); product: erp (request: warehouse); stack: winui (request: winui); mode: accessibility (request: screen reader)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: audit (problem statement (interaction): confusing, keep missing)

| Slot | Choice | Why |
|---|---|---|
| navigation | Tree + breadcrumb for deep hierarchies (`nav-breadcrumb-tree`) | platform desktop, input keyboard,pointer, product erp, density high |
| layout | Table-first working screen (`layout-table-first`) | platform desktop, input keyboard,pointer, product erp, density high |
| density | High density (`density-high`) | density high (INFERRED) |
| surface | Bordered panes (`surface-bordered-panes`) | platform desktop, input keyboard,pointer, product erp, density high |
| cards | List rows (`card-list-row`) | platform desktop |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | product erp, density high |
| color | Neutral canvas + one accent (`color-neutral-accent`) | product erp |
| motion | Functional minimal motion (`motion-functional-minimal`) | lexical |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | platform desktop, input keyboard,pointer, mode accessibility |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | platform desktop, input keyboard,pointer, product erp, density high |
| imagery | No decorative imagery (`imagery-none`) | product erp, density high |
| icon | Outline icon set, one weight (`icon-outline-system`) | platform desktop |
| metadata | Rich metadata (operational) (`metadata-rich`) | platform desktop, input keyboard,pointer, product erp, density high |

## Guidance per slot
- **navigation** — Tree in the left pane with full keyboard semantics (arrow keys expand/collapse, type-ahead), breadcrumb above the content that mirrors the tree path and is clickable at every level. Persist expansion state per session. Virtualise beyond ~500 nodes.
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
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.

## Guardrails (required concerns: accessibility, interaction, component, feedback, data-display; uncovered: none)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
**accessibility**
- Non-text contrast 3:1 for controls and focus: Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails.
- Accessible names for every control and image: Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name).
**states**
- Saving, saved, autosave, session expiry, and permission-denied states: Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry (restore the draft after re-authentication); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default.

## Fingerprint
```json
{
  "navigation_model": "breadcrumb-tree",
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
- navigation: Persistent left rail / sidebar (0.368), Desktop menu bar + toolbar commands (0.328), Command palette as primary navigation accelerator (0.308)
- layout: Master–detail (list + detail pane) (0.348), Dashboard grid of modules (0.338), Three-pane workbench (0.318)
- surface: Flat surfaces with tonal layers (0.314), Translucent (glass) layers, justified (0.096)
- cards: Bordered cards (0.295), No card containers (dividers and spacing) (0.18), Flat tiles (0.158)
- typography: Platform system font (0.248), Monospace as identity for technical products (0.172), Humanist sans for approachable products (0.095)
- color: Dark canvas + accent (dark-first) (0.201), Multicolour by category (0.135), Monochrome with typographic hierarchy (0.073)
- motion: Crossfade and shared-element continuity (0.039)
- cta: One primary action per screen (0.264), Contextual inline actions (0.231)
- imagery: Data graphics as the visual layer (0.251), Functional thumbnails (0.147)
- icon: Platform icon set (0.267), Custom glyph set (0.147)
- metadata: Inline badges and status chips (0.459), Moderate metadata with a hierarchy (0.227), Minimal metadata (0.059)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
