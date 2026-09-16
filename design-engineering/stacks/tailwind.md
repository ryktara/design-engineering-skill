# Tailwind CSS (v3 config / v4 CSS-first)

## Conventions to detect and respect
- Version: v4 uses `@import "tailwindcss"` + `@theme { --color-*: … }` in CSS; v3 uses `tailwind.config.{js,ts}` with `theme.extend`. Detect before editing.
- Existing tokens: `theme.extend.colors`/`@theme` variables, `screens` breakpoints, font families, spacing/radius customisations; semantic aliases (`bg-background`, `text-foreground`, shadcn-style) if present.
- Utility conventions: `cn()`/`clsx`, `cva` variants, `@apply` usage (avoid adding more), plugin usage (`@tailwindcss/forms`, `typography`, `container-queries`).

## Implementation rules
- Add semantic tokens once (v4 `@theme`/CSS variables; v3 `extend.colors` mapping to CSS variables) and use `bg-surface`, `text-primary`-style utilities; never raw `bg-[#hex]` in components.
- Dark mode via the project's strategy (`class`/`data-theme`/media); define both sets of variables and validate with `tokens.py`.
- Breakpoints: use the configured `screens`; container queries via `@container` utilities for components.
- Focus: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[--color-focus-ring]` (or `ring-*` consistently); never `outline-none` without replacement.
- Motion: `transition-[transform,opacity]`, `motion-reduce:transition-none`/`motion-safe:` variants; avoid `transition-all`.
- Spacing: the default scale is 4 px based; keep to it; group spacing with `space-y-*`/`gap-*` from the scale.
- Typography: `font-*` families from tokens, `tabular-nums` for data, `text-balance` for headings, plugin `prose` for long content.
- Hover: `hover:` only inside `@media (hover: hover)` semantics (`[@media(hover:hover)]:hover:` or a custom variant) for touch-safe affordances.

## Verification
Build succeeds without unused arbitrary values; browser pane across `screens`; dark/light; focus pass.
