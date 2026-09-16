# Design direction: Add a team members page with an invite flow, consistent with the rest of the settings area.

**KNOWN:** platform: web (project inspection); product: finance (project inspection (README)); product: saas (project inspection (README)); stack: nextjs (project inspection); stack: react (project inspection); stack: tailwind (project inspection); stack: shadcn (project inspection); project_navigation: left-rail (repository: left-rail: 1 matches in app-shell.tsx (shell/layout file)); project_theme: dual-theme (repository: dark theme configuration signals: 1; root/canvas backgrounds: 1 light, 0 dark); project_typography: custom (repository: font family Var (2 refs); monospace usage); project_components: tailwind, radix, shadcn-style cva, table:tanstack, shadcn (repository: tailwind; radix)
**INFERRED:** input: pointer (implied by platform web); input: keyboard (implied by platform web); input: touch (implied by platform web); density: high (implied by product finance); mode: create (build/create request on an existing surface); project_surfaces: bordered-flat (repository: borders in 8 files, shadow/elevation in 0); project_radius: small (repository: most common radius 0.5 (1×); others []); project_spacing: 8 (repository: most used spacing values [8, 16, 12, 4, 24]; tailwind spacing classes (92))
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=left-rail (KNOWN); theme=dual-theme (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=8 (INFERRED); typography=custom (KNOWN); components=tailwind, radix, shadcn-style cva, table:tanstack, shadcn (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'surface', 'typography', 'color'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: left-rail (KNOWN) (`nav-left-rail`) | preserved | repository evidence with change budget 'moderate' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | High density (`density-high`) | new | density high (INFERRED) |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: custom | preserved | request: keep the typography |
| color | Preserve existing color: light-first (dual theme) (`color-neutral-accent`) | preserved | request: keep the color |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | Sticky action bar (`cta-sticky-bar`) | new | no repository evidence for this slot |
| imagery | Functional thumbnails (`imagery-thumbnails`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Rich metadata (operational) (`metadata-rich`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 4 px base grid, 32 px row height in tables, 13–14 px body, 8–12 px gaps inside groups and 16–24 px between groups; density must be achieved by tightening spacing and sizes coherently, not by shrinking text below the platform floor. Offer a 'comfortable' density toggle where users differ.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — Keep the current typography; inspect and reuse it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — Fixed size per context, consistent crop (object-fit cover with a focal point), alt text that is empty when redundant with the adjacent text, lazy-loaded below the fold with intrinsic size set.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.

## Core guidance (components / layouts to build)
- **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current.
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.

## Guardrails (required concerns: structure, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Everything operable by keyboard, no traps: Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- Focus visible and not obscured: Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). _(covers: visible focus)_
**platform**
- Web: content-driven breakpoints and a test matrix: Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_

## Fingerprint
```json
{
  "navigation_model": "left-rail",
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "high",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "sticky-bar",
  "image_strategy": "thumbnails",
  "icon_strategy": "outline",
  "metadata_density": "rich"
}
```

## Validation: OK

## Alternatives considered
- layout: Master–detail (list + detail pane) (0.42), Table-first working screen (0.42), Dashboard grid of modules (0.41)
- cards: List rows (0.284), Flat tiles (0.276), No card containers (dividers and spacing) (0.25)
- motion: Spring-based physical motion (0.238), Expressive brand motion (0.208)
- focus: Underline / weight focus for text-first UI (0.182)
- cta: Toolbar / command bar with selection-driven commands (0.42), Contextual inline actions (0.337), One primary action per screen (0.33)
- imagery: Data graphics as the visual layer (0.4), No decorative imagery (0.349)
- icon: Duotone icons as brand accent (0.135), Text-only, no icon system (0.135), Custom glyph set (0.025)
- metadata: Inline badges and status chips (0.479), Moderate metadata with a hierarchy (0.25), Minimal metadata (0.131)

## Rejected for incompatibility
- motion: motion-crossfade — incompatible with density-high
- motion: motion-spring — incompatible with density-high
- motion: motion-expressive — incompatible with density-high,surface-bordered-panes
- motion: motion-cinematic — incompatible with density-high
- imagery: imagery-illustration — incompatible with density-high
- imagery: imagery-poster — incompatible with surface-bordered-panes
- imagery: imagery-immersive-backdrop — incompatible with surface-bordered-panes,density-high
- icon: icon-duotone — incompatible with density-high
- metadata: metadata-minimal — incompatible with density-high

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
