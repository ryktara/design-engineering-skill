# Design direction: Flutter field inspection app for utility technicians working outdoors with gloves and patchy connectivity: checklist, defect report form, offline sync

**KNOWN:** platform: mobile (project inspection); product: erp (project inspection (README)); stack: flutter (request: flutter); screen: form (request: form); environment: outdoor (request: outdoor, outdoors); environment: low-bandwidth (request: offline); environment: gloves (request: gloves)
**INFERRED:** input: touch (implied by platform mobile); density: medium (implied by product erp (capped for touch/remote platform)); mode: create (default when no mode word is present)
**MISSING:** brand: no brand assets, guideline, or character description available

| Slot | Choice | Why |
|---|---|---|
| navigation | Bottom tab bar (`nav-bottom-tabs`) | platform mobile, input touch, mode create, density medium |
| layout | Form stack with sections (`layout-form-stack`) | mode create, screen form, density medium |
| density | Medium density (`density-medium`) | density medium (INFERRED) |
| surface | Elevated cards as the primary container (`surface-elevated-cards`) | platform mobile, input touch, mode create, product mismatch, density medium |
| cards | Landscape media cards (16:9) (`card-poster-landscape`) | platform mobile, mode create, product mismatch, density medium |
| typography | Neutral workhorse sans (`typography-neutral-sans`) | mode create, product erp |
| color | Neutral canvas + one accent (`color-neutral-accent`) | mode create, product erp |
| motion | Spring-based physical motion (`motion-spring`) | platform mobile, input touch, mode create, product mismatch, density medium |
| focus | Touch-only focus handling (mobile) (`focus-none-touch-only`) | platform mobile, input touch, mode create |
| cta | Sticky action bar (`cta-sticky-bar`) | platform mobile, input touch, mode create, product mismatch, screen form, density medium |
| imagery | No decorative imagery (`imagery-none`) | mode create, product erp |
| icon | Filled icons for distance and touch (`icon-filled-system`) | platform mobile, input touch, mode create |
| metadata | Inline badges and status chips (`metadata-inline-badges`) | platform mobile, mode create, product erp, density medium |

## Guidance per slot
- **navigation** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination.
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — One elevation level for resting cards, one for pressed/dragged; the whole card is the target with a single accessible name; never nest a card inside a card; cards in a grid share aspect ratio and padding. If more than ~30% of a screen is card borders, switch to dividers.
- **cards** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- **typography** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- **motion** — Use the platform spring APIs (SwiftUI .spring, Compose spring(), Motion/Framer spring on web) with one or two named presets (snappy, gentle); interruptible and gesture-tracking; never chain springs on page load.
- **focus** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
- **cta** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it.
- **imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.

## Core guidance (components / layouts to build)
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.

## Guardrails (required concerns: component, structure, states, interaction, accessibility, feedback, data-display, environment; uncovered: none)
**interaction**
- Mobile: density is bounded by touch: Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things.
**accessibility**
- One type scale with named roles: Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles.
**privacy / environment**
- Offline, sync, and connectivity states: Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- Field use: sunlight readability and glanceable status: Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding).
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks.

## Fingerprint
```json
{
  "navigation_model": "bottom-tabs",
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "medium",
  "surface_strategy": "elevated",
  "card_geometry": "poster-landscape",
  "corner_language": "small",
  "typography_character": "neutral-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "spring",
  "focus_strategy": "none-touch-only",
  "cta_strategy": "sticky-bar",
  "image_strategy": "none",
  "icon_strategy": "filled",
  "metadata_density": "inline-badges"
}
```

## Validation: OK

## Alternatives considered
- navigation: Linear wizard / stepper (0.333), Hub and spoke (0.256)
- layout: Single column, one task (0.396), Catalog grid (0.204), Vertical feed (0.194)
- surface: Flat surfaces with tonal layers (0.278), Imagery-backed surfaces (0.229), Translucent (glass) layers, justified (0.169)
- cards: Flat tiles (0.284), No card containers (dividers and spacing) (0.268)
- typography: Humanist sans for approachable products (0.363), Platform system font (0.302), Rounded friendly sans (0.262)
- color: Material tonal palette (Android) (0.309), Dark canvas + accent (dark-first) (0.239), Dominant brand colour (0.219)
- motion: Functional minimal motion (0.278), Expressive brand motion (0.262), Cinematic reveals (brand moments only) (0.199)
- cta: One primary action per screen (0.383), Contextual inline actions (0.241), Floating action button (Material) (0.154)
- imagery: Poster art as primary recognition (0.275), Functional thumbnails (0.221), Hero imagery on landing/brand pages (0.219)
- icon: Platform icon set (0.312), Duotone icons as brand accent (0.189), Custom glyph set (0.043)
- metadata: Moderate metadata with a hierarchy (0.304), Minimal metadata (0.185)

## Rejected for incompatibility
- cards: card-list-row — incompatible with surface-elevated-cards
- cards: card-flat-tile — incompatible with surface-elevated-cards

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
