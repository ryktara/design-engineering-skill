# Typography: roles, scale, character, loading

Typography is decided after structure and density, and it is chosen for readability, language coverage, numerals, platform rendering, and brand character, in that order.

## Contents
- Type roles
- Building the scale
- Platform floors and units
- Choosing character
- Numerals and data
- Language coverage and loading
- Hierarchy and rhythm
- Mapping to frameworks

## Type roles

Define these roles once; components reference roles, never sizes:

| Role | Use | Notes |
|---|---|---|
| display | the single largest statement on a screen (hero, TV featured title) | ≤1 per screen; tight tracking; may use the display face |
| heading | screen/section titles | line height 1.15–1.25 |
| title | card/list/dialog titles | medium weight, compact |
| body-large | lead paragraphs, TV synopsis | |
| body | default reading and control text | web/mobile 16 px, desktop 14 px, TV 24 sp |
| label | buttons, tabs, form labels, table headers | often medium weight, slight tracking |
| caption | metadata, helper text | never below the platform floor |
| numeric | KPIs, tables, timers, prices | tabular lining figures (`font-variant-numeric: tabular-nums`), fixed decimals |

Weights: two or three (regular, medium/semibold, bold) per family; more is rarely needed.

## Building the scale

`tokens.py scale --platform <p> [--base N] [--ratio R]` generates a role scale that respects platform floors. Ratios: 1.2–1.25 for dense tools and mobile, 1.25–1.333 for content and marketing, 1.25 with a large base for TV. Round to whole pixels (even numbers on TV). Keep ≤7 sizes; hierarchy comes from clear jumps (≥1.25×) and weight, not from many near-identical sizes.

## Platform floors and units

| Platform | Body | Floor | Unit | Scaling mechanism |
|---|---|---|---|---|
| Web | 16 px | 12 px | rem | browser zoom 200%, text-spacing overrides |
| iOS | 17 pt (body) | 11–12 pt | Dynamic Type styles | user text size up to AX5 |
| Android | 16 sp | 12 sp | sp | font scale up to 200% |
| Windows | 14 epx | 12 epx | epx | text scaling 100–225% |
| macOS | 13 pt | 11 pt | pt | Accessibility text size |
| TV | 24 sp / 29 pt | 20 sp | sp / pt at 1080p frame | limited; design large |
| Kiosk | 20 px | 16 px | px at panel scale | none; design large |

Never lock text sizes; containers grow with text; truncation must reveal the full value on focus/hover or in a detail view.

## Choosing character

Order of preference for functional products: the platform system font (SF, Roboto/Google Sans, Segoe UI Variable) → the font the codebase already uses → a neutral workhorse with tabular figures (IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible). For brand-led surfaces, pick a display face for the brief and keep a quiet text face; verify the pairing on the real background and at the real sizes.

Characters and when they fit:

- neutral sans: dense tools, data, forms; disappears behind content.
- system native: native apps; free Dynamic Type/scaling and correct rendering.
- humanist sans: public services, health, education, long forms, multilingual.
- geometric sans: product/tech marketing and consumer apps; check numerals and x-height; avoid the saturated defaults (Inter, Space Grotesk, Poppins) when identity matters.
- grotesk display + quiet body: brand-led web/TV surfaces (e.g. Bricolage Grotesque, Instrument Sans, Familjen Grotesk, Schibsted Grotesk; Unbounded for very bold).
- serif editorial: long reading and authority (Source Serif 4, Literata, Newsreader, Spectral); UI chrome stays sans; not on TV.
- serif display: luxury/fashion headlines only; avoid the cream+serif+terracotta default cluster unless the brand owns it.
- condensed display: broadcast, sports, EPG titles (Barlow Condensed, Oswald, Roboto Condensed, Archivo Narrow) at heavy weights, never for body.
- monospace accent: developer tools, IDs, timestamps, metrics (JetBrains Mono, IBM Plex Mono, Geist Mono, Commit Mono); never paragraphs.
- rounded friendly: children, wellness, playful consumer, kiosks (Nunito, Varela Round, M PLUS Rounded); weights ≥500.

Check before committing: x-height and aperture at the body size, tabular figures, weights available, italics if needed, script coverage, licence, rendering on the target platform (hinting matters on Windows; thin weights fail on TV).

## Numerals and data

Tables, KPIs, prices, timers, and EPG times use tabular lining figures at a consistent precision; right-align numbers; units in headers; negative values with a sign (and parentheses in finance if house style); thousands separators by locale. If the chosen family lacks tabular figures, use a second family for the numeric role only.

## Language coverage and loading

- Verify glyph coverage for every script the product ships (Latin extended, Cyrillic, Greek, Arabic, Hebrew, Devanagari, CJK); fall back per script with `unicode-range` or platform font fallback; allow 30–50% text expansion in layouts.
- Web: self-host, subset, variable font when it saves bytes, ≤2 families, preload the above-the-fold face, `font-display: swap` with `size-adjust`/metric-compatible fallback to avoid layout shift; measure the font bytes.
- Native: bundle only the weights used; on Android register the family in `FontFamily`, on iOS in Info.plist, on Windows as app resources; system fonts cost nothing.
- TV: heavy enough weights to survive scaling and compression; avoid thin and light; test on a real panel at 3 m.

## Hierarchy and rhythm

- 45–75 characters per line for prose; dense tables are exempt.
- Line height: display 1.1, headings 1.2, body 1.4–1.6, labels 1.4.
- Vertical spacing from the spacing scale, tied to line height; headings closer to the content below than above.
- Sentence case for UI text unless the brand defines otherwise; consistent casing across the product.
- Truncation: single-line with ellipsis only where the full text is reachable; two-line clamp for titles on cards.

## Mapping to frameworks

- CSS: `--font-display`, `--font-body`, `--font-mono`, role classes or utilities (`.text-body`, Tailwind `@theme` font sizes with line heights).
- Compose: `MaterialTheme.typography` roles (displayLarge … labelSmall) or tv-material3 typography for TV; define `Typography(...)` once.
- SwiftUI: `.font(.title2)` etc.; custom fonts via `Font.custom(_, size:, relativeTo:)` so Dynamic Type still scales.
- WinUI/WPF: text styles from the type ramp (`TitleTextBlockStyle`, `BodyTextBlockStyle`) or a `Style` per role; Segoe UI Variable with optical size axis.
- Flutter: `TextTheme` roles; `Theme.of(context).textTheme.bodyMedium`.
- React Native: a typography module exporting role styles; `allowFontScaling` left on.
