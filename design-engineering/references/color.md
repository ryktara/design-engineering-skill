# Colour: semantic roles, states, themes, validation

Colour is expressed as semantic roles that components consume; primitives (hue scales) sit underneath and are never referenced by components. Every theme (light, dark, high-contrast, each brand) redefines the semantic layer only.

## Contents
- Role model
- Deriving a palette without lookup tables
- Light and dark themes
- Interactive states
- Feedback and status colours
- Charts and categorical colour
- Platform notes
- Validation

## Role model

```
color.bg.canvas            page/window background
color.bg.surface           panels, list backgrounds
color.bg.elevated          menus, dialogs, dragged items
color.bg.selected          selected row/tab/item
color.text.primary         body and headings
color.text.secondary       supporting text
color.text.disabled        disabled labels (weaker, still readable)
color.text.on-action       label on primary action fills
color.text.link            links in prose (with underline)
color.action.primary       primary buttons, active controls
color.action.primary-hover / -pressed
color.action.destructive   delete/remove
color.border.default       hairlines (decorative, may be <3:1)
color.border.strong        control boundaries (≥3:1)
color.focus.ring           focus indicator (≥3:1 on canvas and surface)
color.feedback.success / warning / error / info (+ their subtle backgrounds)
color.chart.categorical[1..8], color.chart.sequential, color.chart.diverging
```

Component tokens (`button.primary.bg`) map to semantic roles when a component needs an override; they never carry raw hex either.

## Deriving a palette without lookup tables

1. Choose the colour strategy from the direction (neutral + accent; dark + accent; dominant brand; duotone; multicolour-semantic; monochrome; Material tonal). The strategy is a structural decision recorded in the fingerprint.
2. Neutrals: one tinted grey scale (a slight hue from the brand, never pure #808080 greys) with 9–11 steps; canvas/surface/elevated are three adjacent steps whose contrast steps are measurable (each ≥1.05:1 apart; borders that mark boundaries ≥3:1 against their surface).
3. Accent: the brand hue adjusted until `text.on-action` (white or near-black) reaches ≥4.5:1 on it; if the brand hue cannot reach 4.5:1 with either, it becomes an accent for large areas only and a darker/lighter variant is the action colour.
4. Feedback colours: error in the red family, success green, warning amber, info blue or the accent's neighbour; each distinct from the accent by hue family and from each other; each with a subtle background variant for banners.
5. Selection and focus: focus ring is usually the accent or a high-contrast complementary; selection background is a low-chroma tint of the accent with primary text still ≥4.5:1 on it.
6. Record the hue families (`tokens.py validate` prints them) and check that error ≠ accent family.

Avoid deriving every role by tinting everything with the brand hue; avoid indigo/violet/pink gradients as a default identity; avoid pure black canvases unless OLED black is deliberate (TV, media).

## Light and dark themes

Dark mode is a redesign of surfaces, not an inversion:

- Canvas is a dark tinted neutral (e.g. L* ≈ 8–12), surfaces step lighter with elevation (elevation = lighter, shadows become nearly useless).
- Text: primary ≈ 87–92% white, secondary ≈ 60–70%, disabled ≈ 38%; never pure white body text on pure black.
- Accents desaturate and lighten so they hold 4.5:1 for on-action text and 3:1 against the canvas.
- Borders lighten; images may get a slight dim; charts get a dark palette.
- Re-validate every pair in the dark set; state tokens are separate in each theme.

High-contrast themes (Windows) and "Increase Contrast" (Apple) must map cleanly: use system resources on native platforms rather than custom brushes.

## Interactive states

Every interactive role has rest / hover / pressed / focus / disabled / selected variants where the platform has them:

- Hover and pressed differ visibly from rest (≥ one neutral step or a measurable lightness delta) while keeping label contrast.
- Disabled is visibly weaker than secondary text but still readable (aim ≥3:1 even though exempt); no disabled control without an explanation nearby.
- Selected ≠ focused ≠ hovered; on TV the focused state carries the emphasis and selected is quieter.
- Destructive actions use the destructive role only for the action itself, not for the whole dialog.

## Feedback and status colours

- Always paired with text or an icon; never a coloured dot alone.
- One mapping across the product (the same green means the same thing in badges, charts, and banners).
- Status chips: text inside, ≤2 per item, background subtle variant with text at ≥4.5:1.
- Large saturated red/orange areas are discouraged on TV panels (bloom, banding) and in clinical/industrial UI where they must mean alarm.

## Charts and categorical colour

- One categorical palette of ≤8 colour-blind-safe colours (Okabe-Ito or a Tableau-like set tuned to the brand), plus sequential and diverging ramps with a neutral midpoint.
- Series also distinguished by line style, marker, or direct label; verify with a deuteranopia simulation.
- Keep chart colours out of the semantic action/status roles so a red line does not read as an error.
- Dark theme variant of the chart palette.

## Platform notes

- Web: CSS custom properties per theme on `:root` / `[data-theme]` / `prefers-color-scheme`; Tailwind v4 `@theme` maps tokens to utilities; shadcn's `--background/--foreground` pairs are semantic roles already.
- Android (Compose): Material 3 colour scheme from the brand seed; container/on-container pairs are the state-safe way to express roles; disable dynamic colour when brand lock is required; TV uses tv-material3 dark schemes.
- iOS/macOS: semantic system colours (`.label`, `.secondaryLabel`, `.systemBackground`) adapt to dark mode and contrast settings; brand colours as asset-catalog colour sets with light/dark variants.
- Windows (WinUI/WPF): theme resources (`TextFillColorPrimaryBrush`, `ControlFillColorDefaultBrush`, `AccentFillColorDefaultBrush`) give light/dark/high-contrast; override the accent via `ThemeResource` overrides, not per control.
- Flutter: `ColorScheme.fromSeed` + `ThemeData`, brightness-specific schemes; never hard-code `Colors.*` in widgets.

## Validation

```bash
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" init > tokens.json      # skeleton, then edit
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" validate tokens.json --platform web
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" contrast "#hex" "#hex"
```

The validator checks required roles, every text/background and control/background pair in every theme, state deltas, disabled weaker than secondary, feedback hue families, and TV-specific targets. Exit code 1 means the token set is not shippable. Map the validated roles to the project's theme mechanism; never leave hex values in components.
