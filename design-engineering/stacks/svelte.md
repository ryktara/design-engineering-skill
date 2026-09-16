# Svelte 5 / SvelteKit

## Conventions to detect and respect
- SvelteKit routing (`src/routes/+page.svelte`, `+layout.svelte`, load functions), `$lib/components`, runes (`$state`, `$derived`) vs stores; existing UI kit (Skeleton, shadcn-svelte/Bits UI, Melt UI, Flowbite Svelte).
- Styling: scoped component styles, Tailwind, or the kit's theme; tokens as CSS variables in `app.css`.

## Implementation rules
- Semantic markup; Bits UI/Melt UI for accessible menus/dialogs/tabs/comboboxes rather than custom ARIA.
- Transitions: `transition:`/`animate:` directives with CSS-based fades/slides; gate with `prefers-reduced-motion` (`window.matchMedia`) and use the `|global` modifier sparingly.
- Forms: progressive enhancement with form actions and `use:enhance`; server validation errors rendered next to fields with `aria-describedby`.
- Lists: virtualisation (`svelte-virtual-list`/`@tanstack/svelte-virtual`) beyond a few hundred rows; keyed `{#each}`.
- Routing state: `$page.url.searchParams` for filters/tabs; `goto` with `keepFocus`/`noScroll` as appropriate; snapshot API for scroll/form restoration.
- Focus: `bind:this` + `focus()` after `tick()`; `inert` on background; restore on close.
- Images: `@sveltejs/enhanced-img` for responsive sources; reserve space.

## Verification
Vite dev server → browser pane/Playwright at the matrix; Tab pass; reduced-motion; SSR hydration warnings.
