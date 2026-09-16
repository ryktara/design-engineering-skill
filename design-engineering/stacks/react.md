# React (web, and web-on-TV)

## Conventions to detect and respect
- Component location and naming (`components/`, `src/components/`, feature folders); existing primitives (Button, Input, Dialog) and their variant APIs.
- Styling system: CSS Modules, Tailwind, styled-components/Emotion, vanilla-extract, or a UI library (MUI, Chakra, Mantine, Radix + shadcn). Use the one present; never add a second.
- Token layer: CSS custom properties, a `theme.ts`, or Tailwind config; add new values there.
- Routing: React Router / TanStack Router / Next.js; keep URL state for tabs, filters, selection.
- Icons: the installed set (Lucide, Phosphor, Heroicons, Tabler); import individual icons.
- Tests: RTL/Vitest/Jest, Playwright/Cypress; keep `data-testid` and roles stable.

## Implementation rules
- Semantic elements first; ARIA via tested headless primitives (Radix, React Aria, Headless UI) for menus, comboboxes, tabs, dialogs, tooltips; `<dialog>` where no library exists.
- Forms: controlled or react-hook-form per project; `aria-describedby`/`aria-invalid` for errors; `autoComplete` attributes.
- Tables: TanStack Table (headless) + TanStack Virtual for large sets; `<table>` semantics or `role=grid` with `aria-rowcount` when interactive.
- Lists: virtualise beyond a few hundred rows; stable keys; scroll restoration on back.
- Motion: CSS transitions first; View Transitions API for continuity; Motion/Framer only if present; `useReducedMotion`.
- Performance: avoid re-render storms (memoise list rows, hoist state), lazy-load heavy widgets, code-split routes, no barrel icon imports.
- Focus management: `useEffect` to move focus on route/dialog changes; `inert` for background; restore focus on close.

## Web-on-TV (React apps running on TV browsers/WebViews)
- Spatial navigation library (e.g. `@noriginmedia/norigin-spatial-navigation`, `@bam.tech/lrud`) with focus keys per rail; focus memory per row; `scrollIntoView({block:'nearest'})` with CSS `scroll-padding` for the pivot.
- CSS `:focus` styles with transform scale + outline; no `:hover` behaviour; disable text selection and scrollbars; BACK key mapped (`keyCode` 461/27/10009 per platform) to unwind.
- Font sizes in `rem` scaled for 1080p; performance budget for low-end WebViews (avoid `backdrop-filter`, heavy shadows).

## Verification
Dev server + Playwright/browser pane across the responsive matrix; Tab pass; `prefers-reduced-motion` emulation; axe if present. For TV builds, drive keyboard arrows in the browser and check focus visibility and memory.
