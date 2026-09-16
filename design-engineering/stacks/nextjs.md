# Next.js (App Router and Pages Router)

Everything in `stacks/react.md` applies; this adds framework-specific decisions.

## Conventions to detect and respect
- Router type (`app/` vs `pages/`), `layout.tsx` nesting, route groups; server vs client components (`"use client"` boundaries).
- Fonts via `next/font` (Google or local) with `variable` CSS custom properties; use the existing font setup and add `display: 'swap'` and `adjustFontFallback` behaviour by default.
- Images via `next/image` with `sizes`, `priority` for the LCP image, static `width/height` or `fill` with a sized container.
- `globals.css` with tokens (Tailwind v4 `@theme` or CSS variables); shadcn `components.json` if present.
- Metadata API for titles/descriptions; `next-intl`/`i18n` routing if present.

## Implementation rules
- Keep pages server-rendered; push interactivity into small client components (islands); no `"use client"` at the layout root for styling reasons.
- Use `loading.tsx`/Suspense for skeletons at final size; `error.tsx` for error states with retry; `not-found.tsx`.
- URL state via `searchParams` (or `nuqs`) for tabs, filters, pagination; `Link` prefetch for navigation; `router.back()` preserves scroll.
- View Transitions: `document.startViewTransition` in a client wrapper or the framework's experimental support for shared-element continuity.
- Streaming: avoid layout shift by reserving space for streamed sections.
- Middleware/edge only for locale/theme cookies; theme via `data-theme` on `<html>` set before hydration (inline script) to avoid flashes.

## Verification
`next dev` → browser pane/Playwright at the matrix; check hydration warnings in the console; Lighthouse for CLS/LCP if available; confirm the LCP image is `priority` and fonts are self-hosted through `next/font`.
