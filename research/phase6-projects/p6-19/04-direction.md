# Design direction: Add a status bar with the last sync time and any failed postings.

**KNOWN:** platform: desktop (project inspection); product: erp (request: posting); stack: wpf (project inspection); project_navigation: menu-bar (repository: menu-bar: 2 matches in App.xaml.cs, PurchaseOrderLinesView.xaml (shell/layout file)); project_theme: light-first (repository: root/canvas backgrounds: 4 light, 0 dark; hex palette: 11 near-white, 1 near-black); project_components: wpf (repository: wpf)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: high (implied by product erp); mode: create (build/create request); project_surfaces: bordered-flat (repository: borders in 5 files, shadow/elevation in 0); project_radius: small (repository: most common radius 2 (4×); others [1.0, 10.0]); project_spacing: 4 (repository: most used spacing values [16, 8, 6, 2, 12]); project_typography: humanist-sans (repository: font family Segoe UI Variable Text, Segoe UI (1 refs); monospace face Cascadia Mono, Consolas used for a code/number role)
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=menu-bar (KNOWN); theme=light-first (KNOWN); surfaces=bordered-flat (INFERRED); radius=small (INFERRED); spacing=4 (INFERRED); typography=humanist-sans (INFERRED); components=wpf (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'density', 'surface', 'typography', 'color', 'motion', 'focus', 'icon'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (KNOWN) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'moderate' |
| layout | Master–detail (list + detail pane) (`layout-master-detail`) | new | no repository evidence for this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | existing system with change budget 'moderate': density is not the task |
| surface | Preserve existing surface: bordered-flat (INFERRED) (`surface-bordered-panes`) | preserved | repository evidence with change budget 'moderate' |
| cards | Bordered cards (`card-bordered`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (INFERRED) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (KNOWN) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Preserve existing motion: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| focus | Preserve existing focus: as implemented Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state. | preserved | repository: explicit focus handling in source (keep and verify the existing focus treatment) |
| cta | Toolbar / command bar with selection-driven commands (`cta-toolbar-commands`) | new | no repository evidence for this slot |
| imagery | No decorative imagery (`imagery-none`) | new | no repository evidence for this slot |
| icon | Preserve existing icon: as implemented | preserved | existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there) |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour. (Existing system: do not replace it for this task.)
- **cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Primary commands as labelled buttons, overflow into a menu, disabled (not hidden) when no selection, keyboard accelerators shown in tooltips, and the count of selected items visible near the commands.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Rich metadata (operational)** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane.
- **Operational workbench** — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.

## Guardrails (required concerns: structure, states, interaction, accessibility, data-display; uncovered: none)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
**accessibility**
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
- Desktop status bar as the persistent feedback surface, with next-error navigation: One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_
- Exceptions first: surface what needs attention in lists and tables: Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "layout_topology": "master-detail",
  "grid_behavior": "fixed",
  "surface_strategy": "bordered",
  "card_geometry": "bordered",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent",
  "cta_strategy": "toolbar-commands",
  "image_strategy": "none",
  "metadata_density": "inline-badges"
}
```

## Validation: OK

## Alternatives considered
- layout: Table-first working screen (0.42), Dashboard grid of modules (0.41), Three-pane workbench (0.39)
- cards: List rows (0.284), No card containers (dividers and spacing) (0.25), Flat tiles (0.23)
- cta: One primary action per screen (0.27), Contextual inline actions (0.211)
- imagery: Functional thumbnails (0.167)
- metadata: Rich metadata (operational) (0.486), Moderate metadata with a hierarchy (0.288), Minimal metadata (0.131)

## Rejected for incompatibility
- imagery: imagery-data-graphics — product-specific (finance,saas,devtools,iot,healthcare) does not fit request product ['erp']; alternative within 25%

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
