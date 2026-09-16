# Astro

## Conventions to detect and respect
- Content-first, islands architecture: `.astro` components render static HTML; interactive islands in React/Vue/Svelte/Solid with `client:*` directives. Layouts in `src/layouts`, pages in `src/pages`, content collections.
- Styling: scoped `<style>`, Tailwind, or global CSS tokens; `astro:assets` `<Image>`/`<Picture>` for responsive images; `astro:transitions` (View Transitions) for navigation continuity.

## Implementation rules
- Keep pages static; add `client:visible`/`client:idle` islands only for real interactivity (menus, search, carousels with controls); no framework runtime for hover effects.
- Navigation: semantic `<nav>` with `aria-current`; mobile menu as a disclosure button (`aria-expanded`) with a small script, not CSS-only hacks.
- Fonts: self-host with `@font-face` (or the fonts integration), subset, preload the display face, `font-display: swap`.
- Images: `<Image>` with `width/height` (no CLS), `loading="eager"` + `fetchpriority="high"` for the LCP image.
- View Transitions: `transition:name` on shared elements; respect reduced motion (Astro honours it for its default animations).
- Forms: server endpoints or actions; visible labels and error messages rendered server-side.
- Theme: CSS variables with `prefers-color-scheme` and a `data-theme` override set by an inline script before paint.

## Verification
`astro dev` → browser pane/Playwright at the matrix; Lighthouse/CLS check if available; confirm no unintended client JS (`astro build` output size).
