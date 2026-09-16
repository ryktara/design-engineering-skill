# Component reasoning

The knowledge base holds one record per component with platform-specific implementation notes: `advise.py search "<component> <platform>" --kind component` or `advise.py show comp-<name>`. This file is the map and the cross-component rules; a financial table and a movie rail must not share generic advice.

## Contents
- Choosing the component from the task
- Cross-component rules
- Platform substitutions
- Record index

## Choosing the component from the task

| Task | Component | Not this |
|---|---|---|
| work a set of homogeneous records with attributes | data table / grid (`comp-data-table`) | card grid, list of cards |
| batch entry of many similar rows | data-entry grid (`comp-data-entry-grid`) | form per row |
| enter or edit one record | form (`comp-form`) | modal with 20 fields |
| confirm or decide one thing | dialog (`comp-dialog`) | toast with buttons |
| inspect/edit beside the main content | drawer / side panel (`comp-drawer-panel`) | second modal |
| overflow or object actions | menu (`comp-menu`) | row of icon buttons on hover |
| peer views of one object | tabs (`comp-tabs`) | wizard |
| ordered steps | wizard / stepper (`comp-wizard-stepper`) | tabs |
| 6+ sections, frequent switching | sidebar / rail (`comp-sidebar-nav`) | top bar |
| many commands, keyboard users | command palette (`comp-command-palette`) | deep menus only |
| find within a large set | search (`comp-search`) + filters (`comp-filters`) | endless scrolling |
| long lists | pagination / load more (`comp-pagination`) | infinite scroll under a footer |
| show a measure over time/categories | chart container (`comp-chart-container`) + data-viz.md | decorative chart |
| headline metric | KPI tile (`comp-kpi-tile`) | four identical gradient cards |
| artwork-recognised items | media card (`comp-media-card`) | text list |
| categorised browsing on TV | TV rail (`comp-tv-rail`) | grid of everything |
| live TV schedule | EPG (`comp-epg`) | list of channels |
| playback | player controls (`comp-player-controls`) | custom controls without keys |
| phone lists | list row with swipe (`comp-list-row-mobile`) | table |
| preferences | settings screen (`comp-settings-screen`) | form with a Save button for every toggle |
| nothing to show | empty state (`comp-empty-state`) | blank area |
| transient confirmation | toast/snackbar/banner (`comp-toast-notification`) | modal |
| hierarchies | tree view (`comp-tree-view`) | nested accordions |
| landing first screen | hero (`comp-hero-section`) | template hero |

## Cross-component rules

- Every component has all its states designed: rest, hover (pointer), focus (keyboard/DPAD), pressed, selected, disabled, loading, error, empty, overflow/long text.
- One accessible name per interactive element; composite widgets follow the ARIA Authoring Practices keyboard model or the platform equivalent.
- Row/card actions: visible affordance (overflow menu) always; hover reveal is an addition; never on touch/TV.
- Tables and grids: sticky header, numeric alignment with tabular figures, sort indicators, selection count, bulk actions in the toolbar, virtualisation, persisted column state.
- Lists on phones: ≥48 dp rows, whole row tappable, swipe actions mirrored by a menu, section headers, scroll restoration.
- Overlays: focus in/out management, Escape/BACK closes, one at a time, sized to content, scroll inside the body.
- Rails/carousels: fixed pivot, focus memory, one aspect per rail, lazy images with placeholders, safe margins, no wrap-around.
- Forms: labels above, inline errors linked to fields, summary on submit, autofill, sticky primary when long.
- Charts: title = question, units, direct labels, keyboard-reachable values, table alternative, no refresh animation.
- Player: transport keys work without the overlay, overlay hides on inactivity except while focused, captions selectable, live indicator.

## Platform substitutions

| Web | Mobile | TV | Desktop |
|---|---|---|---|
| dialog | bottom sheet / full-screen | full-screen or side sheet with default focus | ContentDialog / owned window |
| dropdown menu | bottom sheet menu / platform menu | row of buttons or side sheet (no menus) | MenuFlyout / ContextMenu |
| sidebar rail | bottom tabs (+ drawer) | side navigation drawer or top tabs | NavigationView / left list |
| data table | list rows + detail | rail/grid of cards or EPG | DataGrid |
| tooltip | long-press hint / help text | focus-revealed detail strip | ToolTip with shortcut |
| hover actions | visible overflow | focus-select + menu key | context menu + toolbar |
| pagination | load more | rail lazy append | virtualised grid + paging |

## Record index

Components: `comp-data-table`, `comp-data-entry-grid`, `comp-form`, `comp-dialog`, `comp-drawer-panel`, `comp-menu`, `comp-tabs`, `comp-sidebar-nav`, `comp-command-palette`, `comp-search`, `comp-filters`, `comp-pagination`, `comp-chart-container`, `comp-kpi-tile`, `comp-media-card`, `comp-player-controls`, `comp-tv-rail`, `comp-epg`, `comp-list-row-mobile`, `comp-settings-screen`, `comp-empty-state`, `comp-toast-notification`, `comp-wizard-stepper`, `comp-tree-view`, `comp-hero-section`. Each record carries `implementation` notes keyed by stack group; the stack file adds the framework conventions.
