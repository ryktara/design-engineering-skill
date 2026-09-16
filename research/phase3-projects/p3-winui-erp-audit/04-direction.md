# Design direction: Warehouse clerks say our WinUI stock adjustments page is confusing and they keep missing rows; the screen reader reads the status column as just text

**KNOWN:** platform: desktop (project inspection); platform: tv (project inspection); input: remote (project inspection: DPAD/remote handling in source); product: erp (request: warehouse); stack: winui (request: winui); mode: accessibility (request: screen reader)
**INFERRED:** input: pointer (implied by platform desktop); input: keyboard (implied by platform desktop); density: medium (implied by product erp (capped for touch/remote platform)); mode: audit (problem statement (interaction): confusing, keep missing); environment: shared-device (a TV is normally a shared household device); environment: large-display (TV platform)

| Slot | Choice | Why |
|---|---|---|
| navigation | Tree + breadcrumb for deep hierarchies (`nav-breadcrumb-tree`) | platform desktop, input keyboard,pointer, product erp |
| layout | Horizontal rails (rows of content) (`layout-rails`) | platform tv, input remote (stated), product mismatch, density medium |
| density | Medium density (`density-medium`) | density medium (INFERRED) |
| surface | Bordered panes (`surface-bordered-panes`) | platform desktop, input keyboard,pointer, product erp |
| cards | List rows (`card-list-row`) | platform desktop, density medium |
| typography | Platform system font (`typography-system-native`) | platform desktop,tv |
| color | Dominant brand colour (`color-dominant-brand`) | platform tv, product mismatch |
| motion | Focus-driven motion (TV) (`motion-focus-scale`) | platform tv, input remote (stated) |
| focus | Visible focus ring (web/desktop) (`focus-ring-standard`) | platform desktop, input keyboard,pointer, mode accessibility |
| cta | Focus is the action (TV) (`cta-focus-selects`) | platform tv, input remote (stated) |
| imagery | No decorative imagery (`imagery-none`) | product erp |
| icon | Outline icon set, one weight (`icon-outline-system`) | platform desktop |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | platform desktop, product erp, density medium |

## Guidance per slot
- **navigation** — Tree in the left pane with full keyboard semantics (arrow keys expand/collapse, type-ahead), breadcrumb above the content that mirrors the tree path and is clickable at every level. Persist expansion state per session. Virtualise beyond ~500 nodes.
- **layout** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp).
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One neutral canvas, borders with ≥3:1 contrast where they define panes, headers as slightly darker/lighter strips, no rounded card containers inside panes. Focus rings and selection highlights carry the colour.
- **cards** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- **typography** — Use the platform text styles (Dynamic Type styles, Material type roles, Windows type ramp) so scaling, weights, and optical sizes are correct for free; add brand through colour, layout, and one display accent if needed.
- **color** — Brand colour on large surfaces with a verified on-colour text token; a secondary neutral for content areas; do not derive the whole palette by tinting everything with the brand hue. Interactive states need visible deltas on the brand surface.
- **motion** — Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- **focus** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element.
- **cta** — No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Icons only where they carry meaning (actions, states, object types); no icon beside every heading or list item; icon-only controls get an accessible name; sizes from tokens (16/20/24); never mix sets.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
- **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp).

## Guardrails (required concerns: accessibility, interaction, component, feedback, performance, data-display; uncovered: none)
**interaction**
- TV: overscan-safe margins: Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content.
- Desktop: keyboard is a first-class input: Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
**accessibility**
- Non-text contrast 3:1 for controls and focus: Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails.
- Announce dynamic status changes: Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable.
- Accessible names for every control and image: Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name).
**platform**
- Virtualise long lists and tables: Windowed rendering with stable row heights or measured heights, keyboard focus preserved when rows unmount (roving focus by key), aria-rowcount/aria-setsize so assistive tech knows the real size, scroll restoration on back navigation. Native: LazyColumn/List/FlatList/VirtualizingStackPanel already virtualise; keep keys stable.

## Fingerprint
```json
{
  "navigation_model": "breadcrumb-tree",
  "layout_topology": "rails",
  "grid_behavior": "horizontal-scroll",
  "content_density": "medium",
  "surface_strategy": "bordered",
  "card_geometry": "list-row",
  "corner_language": "sharp",
  "typography_character": "system-native",
  "color_strategy": "dominant-brand",
  "motion_character": "focus-scale",
  "focus_strategy": "ring",
  "cta_strategy": "focus-selects",
  "image_strategy": "none",
  "icon_strategy": "outline",
  "metadata_density": "inline-badges"
}
```

## Validation: VIOLATIONS
- tv/remote: focus strategy 'ring' is not a 10-foot focus treatment

## Alternatives considered
- navigation: TV side navigation (collapsible drawer) (0.341), Persistent left rail / sidebar (0.332), TV top tabs (0.301)
- layout: Table-first working screen (0.356), Master–detail (list + detail pane) (0.312), Dashboard grid of modules (0.302)
- surface: Imagery-backed surfaces (0.333), Flat surfaces with tonal layers (0.314), Translucent (glass) layers, justified (0.132)
- cards: Bordered cards (0.331), Landscape media cards (16:9) (0.227), Flat tiles (0.194)
- typography: Neutral workhorse sans (0.241), Grotesk display + quiet body (0.162), Condensed display for broadcast/media (0.155)
- color: Material tonal palette (Android) (0.255), Neutral canvas + one accent (0.241), Dark canvas + accent (dark-first) (0.201)
- motion: Functional minimal motion (0.188), Cinematic reveals (brand moments only) (0.109), Crossfade and shared-element continuity (0.075)
- focus: Scale + glow/border focus (TV) (0.377)
- cta: Toolbar / command bar with selection-driven commands (0.312), Contextual inline actions (0.267), One primary action per screen (0.264)
- imagery: Immersive backdrop (0.31), Poster art as primary recognition (0.246), Data graphics as the visual layer (0.215)
- icon: Platform icon set (0.267), Custom glyph set (0.147)
- metadata: Rich metadata (operational) (0.429), Focus-revealed metadata (TV) (0.4), Moderate metadata with a hierarchy (0.263)

## Rejected for incompatibility
- icon: icon-filled-system — incompatible with surface-bordered-panes

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
