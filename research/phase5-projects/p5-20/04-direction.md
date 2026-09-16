# Design direction: Stats screen in dark mode: the bars are barely visible.

**KNOWN:** platform: mobile (project inspection); product: ecommerce (project inspection (README)); stack: swiftui (project inspection); project_navigation: bottom-tabs (repository: bottom-tabs: 7 matches in README.md, RootTabView.swift, StreaksApp.swift (shell/layout file))
**INFERRED:** input: touch (implied by platform mobile); mode: polish (visual defect on existing UI); mode: audit (diagnose first); project_theme: dual-theme (repository: dark theme configuration signals: 2; hex palette: 0 near-white, 0 near-black); project_surfaces: elevated (repository: shadow/elevation in 4 files, borders in 0); project_radius: medium (repository: most common radius 8 (1×); others []); project_spacing: 4 (repository: most used spacing values [2, 4, 12, 16]); project_typography: humanist-sans (repository: font family Nunito (1 refs); encoded type scale in 3 files)
**MISSING:** brand: no brand assets, guideline, or character description available
**Project context:** navigation=bottom-tabs (KNOWN); theme=dual-theme (INFERRED); surfaces=elevated (INFERRED); radius=medium (INFERRED); spacing=4 (INFERRED); typography=humanist-sans (INFERRED)
**Change budget:** low · preserved ['navigation', 'layout', 'density', 'surface', 'cards', 'typography', 'color', 'motion', 'focus', 'cta', 'imagery', 'icon', 'metadata'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: bottom-tabs (KNOWN) (`nav-bottom-tabs`) | preserved | repository evidence with change budget 'low' |
| layout | Preserve existing layout: as implemented | preserved | change budget 'low': the task does not concern this slot |
| density | Preserve existing density: spacing base 4 (INFERRED) | preserved | repository spacing rhythm with change budget 'low' |
| surface | Preserve existing surface: elevated (INFERRED) (`surface-elevated-cards`) | preserved | repository evidence with change budget 'low' |
| cards | Preserve existing cards: as implemented | preserved | change budget 'low': the task does not concern this slot |
| typography | Preserve existing typography: humanist-sans (INFERRED) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'low' |
| color | Preserve existing color: light-first (dual theme) (INFERRED) (`color-neutral-accent`) | preserved | repository evidence with change budget 'low' |
| motion | Preserve existing motion: as implemented | preserved | change budget 'low': the task does not concern this slot |
| focus | Preserve existing focus: as implemented | preserved | change budget 'low': the task does not concern this slot |
| cta | Preserve existing cta: as implemented | preserved | change budget 'low': the task does not concern this slot |
| imagery | Preserve existing imagery: as implemented | preserved | change budget 'low': the task does not concern this slot |
| icon | Preserve existing icon: as implemented | preserved | change budget 'low': the task does not concern this slot |
| metadata | Preserve existing metadata: as implemented | preserved | change budget 'low': the task does not concern this slot |

## Guidance per slot
- **navigation** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination. (Existing system: do not replace it for this task.)
- **layout** — Keep the current layout; inspect and reuse it. (Existing system: do not replace it for this task.)
- **density** — Keep the current density; inspect and reuse it. (Existing system: do not replace it for this task.)
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers. (Existing system: do not replace it for this task.)
- **cards** — Keep the current cards; inspect and reuse it. (Existing system: do not replace it for this task.)
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py. (Existing system: do not replace it for this task.)
- **motion** — Keep the current motion; inspect and reuse it. (Existing system: do not replace it for this task.)
- **focus** — Keep the current focus; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cta** — Keep the current cta; inspect and reuse it. (Existing system: do not replace it for this task.)
- **imagery** — Keep the current imagery; inspect and reuse it. (Existing system: do not replace it for this task.)
- **icon** — Keep the current icon; inspect and reuse it. (Existing system: do not replace it for this task.)
- **metadata** — Keep the current metadata; inspect and reuse it. (Existing system: do not replace it for this task.)

## Core guidance (components / layouts to build)
- **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **Bottom tab bar** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination.

## Guardrails (required concerns: structure, anti-pattern, interaction, accessibility; uncovered: none)
**interaction**
- Target size by platform: Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
**accessibility**
- Dark mode is a redesign of surfaces, not an inversion: Elevation = lighter surface (not darker shadow); desaturate accents; text 87/60/38% white steps for primary/secondary/disabled; borders lighten; images may need a slight dim; charts get a dark palette; re-validate every contrast pair. _(covers: dark mode as a surface redesign, not inversion)_
- Measure, rhythm, and hierarchy by contrast of size and weight: 45–75 characters per line for prose; vertical spacing from the spacing scale tied to line height; hierarchy from clear jumps (≥1.25×) in size or weight, not from five near-identical sizes; headings closer to the content below than to the content above. _(covers: readable line length, visual hierarchy with one focal point)_
- Spacing from one scale, grouping by proximity: A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- Reuse → extend → compose → new (in that order): Inspect the repository first (inspect_project.py): existing components, tokens, fonts, breakpoints, and conventions win. Reuse the existing component; if it lacks a variant, extend it through its API; if the composition is new, compose existing primitives; only create a new primitive when the gap is real, and put it where the others live. _(covers: reuse → extend → compose → new)_
**anti / patterns**
- Dark mode by inversion: Redesign surfaces (elevation = lighter), desaturate accents, use 87/60/38% white text steps, re-validate every pair, define dark chart palettes. See the dark mode rule. _(covers: dark mode as a surface redesign, not inversion)_

## Fingerprint
```json
{
  "navigation_model": "bottom-tabs",
  "surface_strategy": "elevated",
  "card_geometry": "elevated",
  "corner_language": "medium",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent"
}
```

## Validation: OK

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
