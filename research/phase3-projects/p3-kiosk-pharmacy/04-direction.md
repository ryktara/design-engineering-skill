# Design direction: Pharmacy prescription pick-up kiosk flow: identify the patient, show ready prescriptions, confirm; public touch screen in the store

**KNOWN:** platform: kiosk (request: kiosk); input: touch (request: touch); product: ecommerce (request: store); product: healthcare (request: patient, pharmacy); job: high-risk-action (request: prescription)
**INFERRED:** mode: create (default when no mode word is present); environment: public (kiosk platform implies public use)
**MISSING:** brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence

| Slot | Choice | Why |
|---|---|---|
| navigation | Hub and spoke (`nav-hub-spoke`) | platform kiosk, input touch (stated), mode create, product healthcare |
| layout | Single column, one task (`layout-single-column`) | platform kiosk, mode create |
| density | Medium density (`density-medium`) | mode create |
| surface | Flat surfaces with tonal layers (`surface-flat-tonal`) | mode create |
| cards | No card containers (dividers and spacing) (`card-none`) | mode create |
| typography | Rounded friendly sans (`typography-rounded-friendly`) | platform kiosk, input touch (stated), mode create, product healthcare |
| color | Dominant brand colour (`color-dominant-brand`) | platform kiosk, mode create, product ecommerce |
| motion | Crossfade and shared-element continuity (`motion-crossfade`) | mode create, product ecommerce |
| focus | Touch-only focus handling (mobile) (`focus-none-touch-only`) | platform kiosk, input touch (stated), mode create |
| cta | One primary action per screen (`cta-single-primary`) | mode create |
| imagery | Hero imagery on landing/brand pages (`imagery-hero`) | platform kiosk, mode create, product ecommerce |
| icon | Filled icons for distance and touch (`icon-filled-system`) | platform kiosk, input touch (stated), mode create |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | mode create |

## Guidance per slot
- **navigation** — One home screen of large, labelled entry points; each spoke is a linear flow with an obvious way back to the hub. Group entry points by user goal, not by internal system module. On kiosks, the hub also serves as the idle/attract screen and every spoke must time out back to it.
- **layout** — Content width capped for reading (~60–75 characters per line), vertical rhythm from the spacing scale, primary action reachable without scrolling on the shortest supported viewport, or sticky at the bottom.
- **density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- **surface** — Define three tonal steps per theme with measured contrast (each step ≥1.1:1 apart and borders ≥3:1 where they mark boundaries). Shadows reserved for transient layers (menus, dialogs, drag). Reads professional at any density and avoids the 'everything is a floating card' look.
- **cards** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts.
- **typography** — Rounded terminals (e.g. Nunito, Quicksand for display only, Varela Round, M PLUS Rounded) with generous size; keep weights ≥500 for legibility; pair corner radius and icon style consistently with the type.
- **color** — Brand colour on large surfaces with a verified on-colour text token; a secondary neutral for content areas; do not derive the whole palette by tinting everything with the brand hue. Interactive states need visible deltas on the brand surface.
- **motion** — Shared element for one anchor (the image) plus a crossfade for the rest; 250–350 ms; reduced-motion swaps to an instant crossfade. Use platform APIs (View Transitions API, SharedTransitionLayout, matchedGeometryEffect) not manual clones.
- **focus** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — The hero is a thesis about the product: show the actual thing (product, interface, outcome). Reserve aspect box to avoid CLS, serve responsive sources, LCP image preloaded, text contrast guaranteed by placement or scrim, and no autoplay video without a static poster and reduced-motion respect.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Core guidance (components / layouts to build)
- **Public kiosk** — Attract screen → hub of large tiles → linear flows with one giant primary action, ≥60 px targets in the reach zone, ≥20 px text with high contrast for glare, brand colour on header and primary action, filled icons with labels, idle timeout with countdown, cancel always visible, audio/visual feedback. Identity via tile geometry, illustration, and the brand colour field.
- **Filled icons for distance and touch** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **Touch-only focus handling (mobile)** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.

## Guardrails (required concerns: structure, states, interaction, accessibility, environment, privacy, feedback; uncovered: none)
**accessibility**
- Users always know where they are and how to go back: Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there.
**states**
- Saving, saved, autosave, session expiry, and permission-denied states: Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry (restore the draft after re-authentication); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default.
**privacy / environment**
- Kiosk: public, hurried, standing users: Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step.

## Fingerprint
```json
{
  "navigation_model": "hub-and-spoke",
  "layout_topology": "single-column",
  "grid_behavior": "fluid",
  "content_density": "medium",
  "surface_strategy": "tonal-layers",
  "card_geometry": "none",
  "corner_language": "large",
  "typography_character": "rounded-friendly",
  "color_strategy": "dominant-brand",
  "motion_character": "crossfade",
  "focus_strategy": "none-touch-only",
  "cta_strategy": "single-primary",
  "image_strategy": "hero-imagery",
  "icon_strategy": "filled",
  "metadata_density": "moderate"
}
```

## Validation: OK

## Alternatives considered
- navigation: Linear wizard / stepper (0.337)
- layout: Form stack with sections (0.24)
- density: Low density / spacious (0.366)
- cards: Flat tiles (0.23)
- typography: Humanist sans for approachable products (0.452), Neutral workhorse sans (0.346), Geometric sans for product/tech brands (0.147)
- color: Neutral canvas + one accent (0.313), Multicolour by category (0.263)
- motion: Functional minimal motion (0.26)
- imagery: Illustration system (0.317), No decorative imagery (0.313), Functional thumbnails (0.293)
- icon: Custom glyph set (0.151)
- metadata: Minimal metadata (0.167)

Reconcile every slot with the existing codebase before implementing; existing conventions win over this direction unless the task is to change them. Guardrails are not optional.
