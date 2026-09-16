# Vue 3

## Conventions to detect and respect
- SFC structure (`<script setup>`), Composition API, Pinia stores, Vue Router; component folders and naming; existing UI library (Vuetify, PrimeVue, Element Plus, Naive, Headless UI Vue, Radix Vue/shadcn-vue).
- Styling: scoped styles, CSS Modules, Tailwind, or library theming; tokens in CSS variables or the library's theme config.
- Icons: Iconify, the library's set, or an SVG sprite.

## Implementation rules
- Semantic markup; use the library's accessible primitives for menus/dialogs/tabs/comboboxes; otherwise Radix Vue or Headless UI Vue rather than hand-rolled ARIA.
- `<Transition>`/`<TransitionGroup>` with CSS classes for state changes; respect reduced motion via a composable; View Transitions API on navigation when appropriate.
- Forms: `v-model` with validation (VeeValidate/valibot/zod per project); link errors with `aria-describedby`; visible labels.
- Lists: `vue-virtual-scroller` or the library's virtual table beyond a few hundred rows; stable `:key`.
- Router: route params/query for tab/filter/selection state; `scrollBehavior` for restoration; `<KeepAlive>` for expensive views.
- Focus: `nextTick` + `ref.focus()` on dialog open; restore on close; `inert` for background.
- Theme: CSS variables on `:root`/`[data-theme]`; Vuetify/PrimeVue theme presets map to the same semantic roles.

## Verification
Vite dev server → browser pane/Playwright across the matrix; Tab pass; reduced-motion emulation; console warnings.
