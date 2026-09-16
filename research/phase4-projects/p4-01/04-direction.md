# Design direction: polish the billing settings page so plan cards, seat table and invoice history feel consistent with the rest of the admin, without changing navigation or theme

**KNOWN:** platform: web (project inspection); product: saas (request: settings page); product: finance (project inspection (README)); stack: nextjs (project inspection); stack: react (project inspection); stack: tailwind (project inspection); stack: shadcn (project inspection); screen: settings (request: settings); mode: polish (explicit: polish; look/feel words present); project_navigation: left-rail (repository: left-rail: 1 matches in app-shell.tsx (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 1; root/canvas backgrounds: 1 light, 0 dark); project_components: tailwind, radix, shadcn-style cva, table:tanstack, shadcn (repository: tailwind; radix)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: refactor (change request with structural words: navigation); project_radius: small (repository: most common radius 0.5 (1×); others []); project_spacing: 8 (repository: most used spacing values [16, 8, 4, 12, 24]; tailwind spacing classes (93)); project_typography: custom (repository: font family globals (1 refs); monospace usage)
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (KNOWN); radius=small (INFERRED); spacing=8 (INFERRED); typography=custom (INFERRED); components=tailwind, radix, shadcn-style cva, table:tanstack, shadcn (KNOWN)
**Change budget:** low · preserved ['navigation', 'density', 'typography', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (`nav-left-rail`) | preserved | request: keep the navigation |
| layout | Table-first working screen (`layout-table-first`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 8 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Bordered panes (`surface-bordered-panes`) | new | no repository evidence for this slot |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom (INFERRED) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (dual theme) (`color-neutral-accent`) | preserved | request: keep the color |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- **Bordered cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button).

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**accessibility**
- Spacing from one scale, grouping by proximity: A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
**states**
- Design empty, loading, error, and partial states: Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
**anti / patterns**
- Oversized display text and 'big number' KPIs everywhere: Reserve display sizes for one element per screen; app headings 20–28 px; KPI value 24–32 px with a readable label; hierarchy comes from contrast between roles, not from making everything large. TV is the exception with its own scale. _(covers: no oversized display text everywhere, visual hierarchy with one focal point)_

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
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- layout: Form stack with sections (0.337), Three-pane workbench (0.317), Master–detail (list + detail pane) (0.307)
- surface: Elevated cards as the primary container (0.35), Flat surfaces with tonal layers (0.276), Imagery-backed surfaces (0.159)
- cards: No card containers (dividers and spacing) (0.302), List rows (0.267), Flat tiles (0.262)
- motion: Crossfade and shared-element continuity (0.209), Spring-based physical motion (0.184)
- focus: Underline / weight focus for text-first UI (0.164)
- cta: One primary action per screen (0.366), Sticky action bar (0.252), Contextual inline actions (0.211)
- imagery: Poster art as primary recognition (0.386), Functional thumbnails (0.347), No decorative imagery (0.331)
- icon: Text-only, no icon system (0.211), Duotone icons as brand accent (0.147), Custom glyph set (0.043)
- metadata: Moderate metadata with a hierarchy (0.352), Inline badges and status chips (0.345), Minimal metadata (0.187)

## Rejected for incompatibility
- surface: surface-elevated-cards — incompatible with layout-table-first
- surface: surface-imagery-backed — incompatible with layout-table-first
- surface: surface-glass — incompatible with layout-table-first
- cards: card-poster-landscape — incompatible with layout-table-first
- cards: card-poster-portrait — incompatible with layout-table-first
- motion: motion-expressive — incompatible with surface-bordered-panes
- motion: motion-crossfade — incompatible with layout-table-first
- motion: motion-cinematic — incompatible with layout-table-first
- focus: focus-underline — incompatible with layout-table-first
- imagery: imagery-poster — incompatible with layout-table-first,surface-bordered-panes
- imagery: imagery-illustration — incompatible with layout-table-first
- imagery: imagery-immersive-backdrop — incompatible with surface-bordered-panes,layout-table-first
- metadata: metadata-minimal — incompatible with layout-table-first

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
