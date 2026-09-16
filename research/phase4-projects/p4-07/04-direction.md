# Design direction: polish this existing light-theme WPF purchase-order screen: inconsistent spacing in the toolbar and status bar, and validation errors are hard to read

**KNOWN:** platform: desktop (project inspection); product: erp (request: purchase order); stack: wpf (request: wpf); mode: polish (explicit: polish; visual problem on existing UI); project_components: wpf (repository: wpf)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: audit (diagnose first); project_navigation: menu-bar (repository: menu-bar: 1 matches in PurchaseOrderLinesView.xaml); project_theme: light-first (repository: hex palette: 11 near-white, 1 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_radius: small (repository: most common radius 2 (2×); others [1.0, 10.0]); project_spacing: 4 (repository: most used spacing values [16, 4, 12, 10, 6])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=menu-bar (INFERRED); theme=light-first (INFERRED); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); components=wpf (KNOWN)
**Change budget:** low · preserved ['navigation', 'density', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (INFERRED) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'low' |
| layout | Dashboard grid of modules (`layout-dashboard-grid`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'low' |
| cards | No card containers (dividers and spacing) (`card-none`) | new | no repository evidence for this slot |
| typography | Platform system font (`typography-system-native`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Toolbar / command bar with selection-driven commands** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **Desktop menu bar + toolbar commands** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live.
- **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility, feedback, data-display; uncovered: accessibility)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
**accessibility**
- Measure, rhythm, and hierarchy by contrast of size and weight: 45–75 characters per line for prose; vertical spacing from the spacing scale tied to line height; hierarchy from clear jumps (≥1.25×) in size or weight, not from five near-identical sizes; headings closer to the content below than to the content above. _(covers: readable line length, visual hierarchy with one focal point)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
**anti / patterns**
- Arbitrary spacing and misaligned edges: Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "layout_topology": "dashboard-grid",
  "grid_behavior": "responsive-columns",
  "surface_strategy": "bordered",
  "card_geometry": "none",
  "corner_language": "sharp",
  "typography_character": "system-native",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "inline-badges"
}
```

## Validation: OK

## Alternatives considered
- layout: Table-first working screen (0.47), Master–detail (list + detail pane) (0.375), Form stack with sections (0.351)
- cards: Bordered cards (0.34), List rows (0.212), Flat tiles (0.193)
- typography: Neutral workhorse sans (0.267), Monospace as identity for technical products (0.172), Humanist sans for approachable products (0.095)
- motion: Crossfade and shared-element continuity (0.039)
- cta: One primary action per screen (0.246), Contextual inline actions (0.15)
- imagery: No decorative imagery (0.277), Functional thumbnails (0.095)
- icon: Platform icon set (0.222), Custom glyph set (0.025)
- metadata: Rich metadata (operational) (0.384), Moderate metadata with a hierarchy (0.205), Minimal metadata (0.059)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
