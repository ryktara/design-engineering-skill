# Design direction: The dispatch job form lets you lose an unsaved job by clicking another one.

**KNOWN:** platform: desktop (project inspection); stack: avalonia (project inspection); screen: form (request: form); project_navigation: menu-bar (repository: menu-bar: 1 matches in MainWindow.axaml (shell/layout file); also left-rail: 1 matches); project_typography: geometric-sans (repository: font family Segoe UI, avares://Avalonia.Fonts.Inter/Assets#Inter (2 refs); weights semibold); project_components: avalonia (repository: avalonia)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); mode: audit (interaction defect on existing UI); mode: refactor (fix follows the diagnosis); project_theme: light-first (repository: hex palette: 9 near-white, 0 near-black); project_spacing: 4 (repository: most used spacing values [4])
**Project context:** navigation=menu-bar (KNOWN); theme=light-first (INFERRED); spacing=4 (INFERRED); typography=geometric-sans (KNOWN); components=avalonia (KNOWN)
**Change budget:** moderate · preserved ['navigation', 'typography', 'color'] · changed ['density']

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: menu-bar (KNOWN) (`nav-menu-bar-desktop`) | preserved | repository evidence with change budget 'moderate' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | Medium density (`density-medium`) | changed | existing 4 (INFERRED) → density-medium: allowed by change budget 'moderate' |
| surface | Bordered panes (`surface-bordered-panes`) | new | no repository evidence for this slot |
| cards | List rows (`card-list-row`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: geometric-sans (KNOWN) (`typography-geometric-sans`) | preserved | repository evidence with change budget 'moderate' |
| color | Preserve existing color: light-first (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'moderate' |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Data graphics as the visual layer (`imagery-data-graphics`) | new | no repository evidence for this slot |
| icon | Outline icon set, one weight (`icon-outline-system`) | new | no repository evidence for this slot |
| metadata | Minimal metadata (`metadata-minimal`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Title plus at most one secondary line; everything else on the detail screen. On TV, reveal one more line on focus rather than showing it always.

## Core guidance (components / layouts to build)
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.

## Guardrails (required concerns: accessibility, interaction, component, feedback; uncovered: none)
**interaction**
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- Hover reveals need a non-hover path: Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_
**accessibility**
- Form labels, errors, and recovery: Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- Desktop status bar as the persistent feedback surface, with next-error navigation: One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_

## Fingerprint
```json
{
  "navigation_model": "menu-bar",
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "medium",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "typography_character": "geometric-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "ring",
  "cta_strategy": "single-primary",
  "image_strategy": "data-graphics",
  "icon_strategy": "outline",
  "metadata_density": "minimal"
}
```

## Validation: OK

## Alternatives considered
- layout: Master–detail (list + detail pane) (0.188), Table-first working screen (0.168), Dashboard grid of modules (0.158)
- surface: Translucent (glass) layers, justified (0.258), Flat surfaces with tonal layers (0.242)
- cards: Bordered cards (0.434), Flat tiles (0.395), No card containers (dividers and spacing) (0.232)
- motion: Crossfade and shared-element continuity (0.192)
- cta: Toolbar / command bar with selection-driven commands (0.168), Contextual inline actions (0.129)
- imagery: No decorative imagery (0.205), Functional thumbnails (0.185)
- icon: Platform icon set (0.276), Custom glyph set (0.079)
- metadata: Rich metadata (operational) (0.276), Moderate metadata with a hierarchy (0.232), Inline badges and status chips (0.229)

## Rejected for incompatibility
- density: density-high — product-specific (erp,finance,devtools,saas,healthcare) does not fit request product unknown; alternative within 25%

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
