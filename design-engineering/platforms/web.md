# Web (browser: pointer + keyboard + touch)

Load for websites, web apps, PWAs, and desktop-first web tools. The web must serve every input at once and every viewport.

## Contents
- Input model
- Structure and semantics
- Layout and responsiveness
- Navigation
- Components
- Performance
- Accessibility (WCAG 2.2 AA)
- Theming and tokens
- Checklist

## Input model

Pointer, keyboard, and touch simultaneously: hover is an enhancement (never the only path), focus-visible rings for keyboard users, targets ≥24 CSS px (44 for touch-heavy products), no drag-only interactions, `pointer`/`hover` media queries to adapt affordances, scroll wheel and touch scrolling both smooth.

## Structure and semantics

Semantic HTML first (`header/nav/main/aside/footer`, one `h1`, ordered headings, real buttons/links/tables/lists/forms), then style. ARIA only to fill gaps, following the ARIA Authoring Practices for composite widgets. URL reflects state (route, tab, filters, selected record) for deep links and Back.

## Layout and responsiveness

Fluid widths with min/max, CSS grid `auto-fill/minmax`, container queries for components, logical properties for RTL, project breakpoints (Tailwind `screens`, tokens), `scroll-padding` under sticky headers, `env(safe-area-inset-*)` on mobile web, reflow at 320 px, 200% zoom, no fixed-height text containers. Topologies: single column, editorial, form stack, catalog grid, feed, master-detail (≥ ~900 px), table-first, three-pane (≥1280), dashboard grid.

## Navigation

Top bar for ≤5 destinations (collapsing to a menu button), left rail for 6+ sections in authenticated tools, breadcrumb + tree for hierarchies, tabs for peer views (URL-synced), wizard for ordered steps, command palette as an accelerator. Mark the current page (`aria-current`), keep browser Back working, restore scroll on return.

## Components

Native elements where they exist (`<dialog>`, `<details>`, `<select>` when styling allows, `<input type=…>` with `autocomplete`); tested headless libraries (Radix, React Aria, Headless UI, or the project's) for menus, comboboxes, tabs, dialogs; data tables with `<table>` semantics or `role=grid` when interactive, virtualised beyond a few hundred rows; forms with visible labels and linked errors; toasts as live regions; carousels with pause/prev/next and no auto-rotation by default.

## Performance

CLS < 0.1 (reserved media space, font fallback metrics, skeletons at size), LCP < 2.5 s (preload hero/font, responsive images, no lazy LCP), INP responsive (avoid main-thread-heavy handlers), JS budget (CSS for hover/transitions, islands, individual icon imports, lazy charts/editors), `content-visibility` for long pages, modern image formats, ≤2 font families subset and preloaded.

## Accessibility (WCAG 2.2 AA)

Contrast 4.5:1 / 3:1 non-text; keyboard operability with roving tabindex in composites; focus visible and not obscured; targets 24 px; hover content dismissible/hoverable/persistent; dialogs manage focus; live regions for status; reduced motion; reflow and text spacing; consistent help; no redundant entry; accessible authentication. Run axe/Lighthouse if present; still do a keyboard and screen-reader pass.

## Theming and tokens

CSS custom properties per theme (`:root`, `[data-theme]`, `prefers-color-scheme`); Tailwind v4 `@theme` or v3 config maps tokens to utilities; shadcn's `--background/--foreground` pairs are semantic roles; never hex in components; validate with `tokens.py validate`.

## Checklist

- [ ] Semantic structure, landmarks, headings, URL state
- [ ] Hover never required; focus-visible rings; targets ≥24 px
- [ ] Responsive matrix from project breakpoints + 320 px reflow + 200% zoom verified
- [ ] Native/tested components for overlays, menus, comboboxes, tabs
- [ ] CLS/LCP guarded: reserved media, font loading, no lazy LCP
- [ ] Tokens via custom properties; light/dark validated
- [ ] axe or equivalent run; keyboard pass done; reduced motion honoured
