# Design direction: add a column-defaults settings dialog to the purchase order lines window so clerks can choose default warehouse and hidden columns

**KNOWN:** platform: desktop (request: window); product: erp (request: warehouse, purchase order); stack: wpf (project inspection); screen: settings (request: settings); project_components: wpf (repository: wpf)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: create (default (no mode cue)); project_navigation: menu-bar (repository: menu-bar: 1 matches in PurchaseOrderLinesView.xaml); project_theme: light-first (repository: hex palette: 11 near-white, 1 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 2 (2×); others [1.0, 10.0]); project_spacing: 4 (repository: most used spacing values [16, 4, 12, 10, 6])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=menu-bar (INFERRED); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); components=wpf (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (INFERRED) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'moderate' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | new | density high (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Platform system font (`typography-system-native`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Platform icon set (`icon-platform-native`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Use the platform set with its variable weight/fill axes rather than importing a web set; align icon weight to text weight; provide accessibility labels via the platform API.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).
- **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action.
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Grids with row actions are one Tab stop: Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions)_
- Dialog focus management: On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. _(covers: dialog focus management, focus restoration)_
**platform**
- Numeric tables: alignment, figures, units, precision: Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator. _(covers: tabular figures and numeric alignment)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "typography_character": "system-native",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "single-primary",
  "image_strategy": "none",
  "icon_strategy": "system",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- layout: Table-first working screen (0.409), Dashboard grid of modules (0.355), Master–detail (list + detail pane) (0.35)
- cards: List rows (0.348), No card containers (dividers and spacing) (0.268), Flat tiles (0.248)
- typography: Neutral workhorse sans (0.357), Monospace as identity for technical products (0.262), Geometric sans for product/tech brands (0.242)
- motion: Crossfade and shared-element continuity (0.129)
- cta: Toolbar / command bar with selection-driven commands (0.368), Contextual inline actions (0.121)
- imagery: Data graphics as the visual layer (0.292), Functional thumbnails (0.185)
- icon: Outline icon set, one weight (0.322), Custom glyph set (0.043)
- metadata: Inline badges and status chips (0.355), Minimal metadata (0.33), Moderate metadata with a hierarchy (0.268)

## Rejected for incompatibility
- typography: typography-geometric-sans — incompatible with density-high
- motion: motion-crossfade — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
