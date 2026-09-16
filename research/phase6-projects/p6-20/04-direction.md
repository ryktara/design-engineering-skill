# Design direction: The stock adjustments grid shows 3,000 rows and scrolling is janky.

**KNOWN:** platform: desktop (project inspection); product: erp (project inspection (README)); product: finance (project inspection (README)); stack: winui (project inspection); project_navigation: left-rail (repository: left-rail: 3 matches in MainWindow.xaml, OrdersPage.xaml (shell/layout file); also menu-bar: 11 matches); project_components: winui3, community-toolkit (repository: winui3; community-toolkit)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: audit (interaction defect on existing UI); mode: refactor (fix follows the diagnosis); project_theme: dual-theme (repository: dark theme configuration signals: 1; hex palette: 0 near-white, 0 near-black); project_surfaces: bordered-flat (repository: borders in 2 files, shadow/elevation in 0); project_spacing: 4 (repository: most used spacing values [16, 8, 12, 4, 2])
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (INFERRED); surfaces=bordered-flat (INFERRED); spacing=4 (INFERRED); components=winui3, community-toolkit (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'moderate' |
| layout | Table-first working screen (`layout-table-first`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| color | Preserve existing color: light-first (dual theme) (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Preserve existing cta: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| imagery | Preserve existing imagery: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Preserve existing metadata: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- **Data-entry grid (spreadsheet-like)** — Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Grids with row actions are one Tab stop: Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
**accessibility**
- Exceptions first: surface what needs attention in lists and tables: Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
**platform**
- Editable grids: make the current column and its unit unmistakable: Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "table-first",
  "grid_behavior": "virtualized",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

## Alternatives considered
- layout: Dashboard grid of modules (0.528), Master–detail (list + detail pane) (0.384), Three-pane workbench (0.354)
- cards: Bordered cards (0.332), Flat tiles (0.218), No card containers (dividers and spacing) (0.217)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
