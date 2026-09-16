# Nuxt (with or without Nuxt UI)

Everything in `stacks/vue.md` applies.

## Conventions to detect and respect
- `app.vue`, `layouts/`, `pages/` file routing, `components/` auto-import, `composables/`, `app.config.ts` (Nuxt UI theme), `nuxt.config.ts` modules (`@nuxt/ui`, `@nuxt/image`, `@nuxt/fonts`, `@nuxtjs/i18n`, `@nuxtjs/color-mode`).
- Nuxt UI: semantic colour aliases (`primary`, `neutral`, …) configured in `app.config.ts`; components are already accessible (Reka UI/Radix Vue based); extend via `ui` prop slots rather than overriding CSS.

## Implementation rules
- SSR by default; islands via `<ClientOnly>` or `.client.vue` only for browser-only widgets; avoid hydration mismatches (no random ids/dates in SSR markup).
- `@nuxt/image` `<NuxtImg>` with `sizes`, `preload` for LCP; `@nuxt/fonts` for self-hosted fonts with fallbacks.
- Colour mode: `useColorMode()`; tokens as CSS variables with light/dark; validate both sets.
- Loading/error: `<NuxtLoadingIndicator>`, `error.vue`, `useAsyncData` states rendered as skeletons at size.
- URL state: `useRoute().query` / `navigateTo` for filters and tabs; `definePageMeta` for layouts and transitions.

## Verification
`nuxt dev` → browser pane/Playwright across the matrix; check SSR/hydration warnings; dark/light modes; keyboard pass.
