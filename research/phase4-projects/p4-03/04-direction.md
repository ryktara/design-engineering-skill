# Design direction: add keyboard shortcuts and a command bar to the existing stock adjustments page without changing its navigation or theme

**KNOWN:** platform: desktop (request: keyboard shortcut, keyboard shortcuts); input: keyboard (request: keyboard, shortcut, shortcuts); product: erp (project inspection (README)); stack: winui (project inspection); project_navigation: left-rail (repository: left-rail: 7 matches in MainWindow.xaml, MainWindow.xaml.cs, OrdersPage.xaml (shell/layout file); also menu-bar: 9 matches); project_components: winui3, community-toolkit (repository: winui3; community-toolkit)
**INFERRED:** input: pointer (implied by platform desktop); density: high (implied by product erp); mode: create (default (no mode cue)); project_theme: dual-theme (repository: dark theme configuration signals: 1; hex palette: 0 near-white, 0 near-black); project_surfaces: bordered-flat (repository: weak signal: shadow 0, border 1); project_spacing: 4 (repository: most used spacing values [16, 12, 8, 4, 2])
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (INFERRED); surfaces=bordered-flat (INFERRED); spacing=4 (INFERRED); components=winui3, community-toolkit (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (`nav-left-rail`) | preserved | request: keep the navigation |
| layout | Three-pane workbench (`layout-three-pane`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | new | density high (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Platform system font (`typography-system-native`) | new | no repository evidence for this slot |
| color | Preserve existing color: light-first (dual theme) (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Platform icon set (`icon-platform-native`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Resizable panes with remembered sizes, each pane a landmark/region with a heading, F6-style pane cycling on desktop, collapse order defined (inspector collapses first). Keyboard focus must be able to move between panes without tabbing through every control.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Use the platform set with its variable weight/fill axes rather than importing a web set; align icon weight to text weight; provide accessibility labels via the platform API.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Toolbar / command bar with selection-driven commands** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **No decorative imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.

## Guardrails (required concerns: component, structure, navigation, interaction, accessibility, data-display; uncovered: component)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- Hover reveals need a non-hover path: Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_
**states**
- Desktop: persist layout and selection state: Restore the workspace on launch (per user, per view), offer 'reset layout', keep undo history per document, and never lose selection on data refresh (re-select by key). _(covers: persisted workspace and selection)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "three-pane",
  "grid_behavior": "fixed",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "typography_character": "system-native",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "none",
  "icon_strategy": "system",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- layout: Master–detail (list + detail pane) (0.609), Dashboard grid of modules (0.491), Table-first working screen (0.456)
- cards: No card containers (dividers and spacing) (0.312), Flat tiles (0.302), List rows (0.284)
- typography: Neutral workhorse sans (0.339), Humanist sans for approachable products (0.167)
- cta: One primary action per screen (0.27), Contextual inline actions (0.211)
- imagery: Data graphics as the visual layer (0.31), Functional thumbnails (0.167)
- icon: Outline icon set, one weight (0.304), Custom glyph set (0.025)
- metadata: Inline badges and status chips (0.337), Moderate metadata with a hierarchy (0.25), Minimal metadata (0.131)

## Rejected for incompatibility
- typography: typography-geometric-sans — incompatible with density-high
- typography: typography-monospace-technical — product-specific (devtools) does not fit request product ['erp']; alternative within 25%
- motion: motion-crossfade — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
