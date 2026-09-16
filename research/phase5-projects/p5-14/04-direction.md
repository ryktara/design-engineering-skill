# Design direction: Purchase-order lines: operators keep typing the quantity into the price column.

**KNOWN:** platform: desktop (project inspection); product: erp (request: purchase order); stack: wpf (project inspection); project_navigation: menu-bar (repository: menu-bar: 2 matches in App.xaml.cs, PurchaseOrderLinesView.xaml (shell/layout file)); project_theme: light-first (repository: root/canvas backgrounds: 4 light, 0 dark; hex palette: 11 near-white, 1 near-black); project_components: wpf (repository: wpf)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: audit (problem statement on existing UI); mode: refactor (fix follows the diagnosis); project_surfaces: bordered-flat (repository: borders in 3 files, shadow/elevation in 0); project_radius: small (repository: most common radius 2 (2×); others [1.0, 10.0]); project_spacing: 4 (repository: most used spacing values [16, 8, 2, 12, 9]); project_typography: monospace (repository: font family Cascadia Mono, Consolas (1 refs); weights semibold, bold)
**Project context:** navigation=menu-bar (KNOWN); theme=light-first (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); typography=monospace (INFERRED); components=wpf (KNOWN)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (KNOWN) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: monospace (INFERRED) (`typography-monospace-technical`) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Monospace for code, IDs, timestamps, and metrics (e.g. JetBrains Mono, IBM Plex Mono, Geist Mono, Commit Mono); a compact sans for prose and navigation. Never set paragraphs in monospace. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- **Rich metadata (operational)** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Guardrails (required concerns: accessibility, interaction, component, data-display; uncovered: none)
**interaction**
- Grids with row actions are one Tab stop: Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
**accessibility**
- Desktop status bar as the persistent feedback surface, with next-error navigation: One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_
- Native accessibility semantics (mobile/desktop): Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code. _(covers: semantic structure and roles, accessible names and labels)_
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "typography_character": "monospace-technical",
  "color_strategy": "neutral-plus-accent",
  "focus_strategy": "ring"
}
```

## Validation: OK

## Alternatives considered

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
