# Design direction: accessibility audit and fix of the identify step of the pick-up kiosk: the date-of-birth keypad and name entry

**KNOWN:** platform: kiosk (request: kiosk); product: healthcare (project inspection (README)); product: government (project inspection (README)); stack: html-css (project inspection); mode: audit (explicit: audit; diagnose first); mode: accessibility (explicit: accessibility); project_navigation: hub-spoke (repository: hub-spoke: 24 matches in README.md, app.js, i18n.js (shell/layout file))
**INFERRED:** input: touch (implied by platform kiosk); mode: polish (change request about look/feel); environment: public (kiosk platform implies public use); project_surfaces: elevated (repository: weak signal: shadow 1, border 1); project_radius: medium (repository: most common radius 12 (1×); others [20.0, 32.0]); project_typography: humanist-sans (repository: font family Nunito (1 refs); weights 700, 800, 600, 500)
**CONFLICTS:** platform: request ['kiosk'] vs project web → request kept; repository platform recorded as context
**Project context:** navigation=hub-spoke (KNOWN); surfaces=elevated (INFERRED); radius=medium (INFERRED); typography=humanist-sans (INFERRED)
**Change budget:** low · preserved ['navigation', 'surface', 'typography'] · changed []

| Slot | Choice | Status | Why |
|---|---|---|---|
| navigation | Preserve existing navigation: hub-spoke (KNOWN) (`nav-hub-spoke`) | preserved | repository evidence with change budget 'low' |
| layout | Form stack with sections (`layout-form-stack`) | new | no repository evidence for this slot |
| density | Low density / spacious (`density-low`) | new | kiosk platform: low density unless stated |
| surface | Preserve existing surface: elevated (INFERRED) | preserved | repository evidence with change budget 'low' |
| cards | Flat tiles (`card-flat-tile`) | new | no repository evidence for this slot |
| typography | Preserve existing typography: humanist-sans (INFERRED) (`typography-humanist-sans`) | preserved | repository evidence with change budget 'low' |
| color | Neutral canvas + one accent (`color-neutral-accent`) | new | no repository evidence for this slot |
| motion | Functional minimal motion (`motion-functional-minimal`) | new | no repository evidence for this slot |
| focus | Touch-only focus handling (mobile) (`focus-none-touch-only`) | new | no repository evidence for this slot |
| cta | One primary action per screen (`cta-single-primary`) | new | no repository evidence for this slot |
| imagery | Illustration system (`imagery-illustration`) | new | no repository evidence for this slot |
| icon | Filled icons for distance and touch (`icon-filled-system`) | new | no repository evidence for this slot |
| metadata | Moderate metadata with a hierarchy (`metadata-moderate`) | new | no repository evidence for this slot |

## Guidance per slot
- **navigation** — One home screen of large, labelled entry points; each spoke is a linear flow with an obvious way back to the hub. Group entry points by user goal, not by internal system module. On kiosks, the hub also serves as the idle/attract screen and every spoke must time out back to it. (Existing system: do not replace it for this task.)
- **layout** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- **density** — Whitespace must come from a scale (e.g. 24/40/64/96), not arbitrary padding; keep line length in measure; big type is only justified for the one thing that should be read first. Spacious does not mean everything is huge. Kiosk: targets ≥ 64 px, body ≥ 20 px (platform floor overrides the generic numbers).
- **surface** — Keep the current surface; inspect and reuse it. (Existing system: do not replace it for this task.)
- **cards** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- **typography** — Open apertures and generous x-height (e.g. Source Sans 3, Nunito Sans, Open Sans, Fira Sans, Noto Sans for coverage). Pair with a slightly heavier weight for headings rather than a second family unless brand demands it. (Existing system: do not replace it for this task.)
- **color** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- **motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.
- **focus** — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
- **cta** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby.
- **imagery** — Define the style (line, flat, isometric) once, use it in ≤4 places (onboarding, empty, error, success), keep it meaningful (depicts the task), and mark decorative instances aria-hidden.
- **icon** — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
- **metadata** — Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.

## Core guidance (components / layouts to build)
- **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action.

## Guardrails (required concerns: accessibility, interaction, component, environment, privacy; uncovered: none)
**accessibility**
- Accessible names for every control and image: Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
**privacy / environment**
- Kiosk: public, hurried, standing users: Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- Privacy on shared and public screens: Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
**anti / patterns**
- Only the happy state was designed: Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_

## Fingerprint
```json
{
  "navigation_model": "hub-and-spoke",
  "layout_topology": "form-stack",
  "grid_behavior": "fluid",
  "content_density": "low",
  "card_geometry": "flat-tile",
  "corner_language": "small",
  "typography_character": "humanist-sans",
  "color_strategy": "neutral-plus-accent",
  "motion_character": "functional-minimal",
  "focus_strategy": "none-touch-only",
  "cta_strategy": "single-primary",
  "image_strategy": "illustration",
  "icon_strategy": "filled",
  "metadata_density": "moderate"
}
```

## Validation: OK

## Alternatives considered
- layout: Single column, one task (0.222)
- cards: No card containers (dividers and spacing) (0.214)
- color: Multicolour by category (0.191), Dominant brand colour (0.129)
- motion: Crossfade and shared-element continuity (0.075)
- imagery: No decorative imagery (0.241), Hero imagery on landing/brand pages (0.129), Functional thumbnails (0.095)
- icon: Custom glyph set (0.069)
- metadata: Minimal metadata (0.095)

Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional.
