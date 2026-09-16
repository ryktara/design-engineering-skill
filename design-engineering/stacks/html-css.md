# Plain HTML/CSS (and web components)

## Conventions to detect and respect
- Existing CSS architecture (BEM, utility classes, layers, custom properties), build (none/PostCSS/Sass), JS approach (vanilla modules, web components, htmx/Alpine), icon approach (SVG sprite/inline).

## Implementation rules
- Semantic HTML: landmarks, headings, `<button>`/`<a>`/`<table>`/`<dialog>`/`<details>`/`<fieldset>`; native form controls with `autocomplete`; `<label for>`.
- Tokens as custom properties in `:root` and theme scopes; layers (`@layer reset, tokens, base, components, utilities`) to control specificity; logical properties; `clamp()` for fluid display type only.
- Layout: grid/flex with `auto-fill/minmax`, container queries, `aspect-ratio`, `scroll-padding`, `env(safe-area-inset-*)`.
- Interaction: `:focus-visible` rings, `@media (hover: hover)` for hover-only enhancements, `prefers-reduced-motion` guards, `popover`/`<dialog>` for overlays, small progressive-enhancement scripts for menus and tabs following the ARIA Authoring Practices.
- Performance: no framework for static pages; images with `width/height`, `srcset/sizes`, `loading=lazy` below the fold; fonts self-hosted, subset, preloaded; CSS transitions on transform/opacity.
- Web components: shadow DOM styles consume the same custom properties; delegate focus (`delegatesFocus`), expose ARIA via ElementInternals.

## Verification
Static server → browser pane/Playwright at the matrix; validate HTML; axe if available; Tab pass; reduced motion.
