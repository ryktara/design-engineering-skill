<script lang="ts">
  import type { Snippet } from 'svelte';

  /**
   * Empty state for lists and tables: says what this is, why it is empty and
   * offers one next step. Place it inside the container the data would have
   * filled (a Card) so the region does not collapse.
   */
  let {
    title,
    description,
    actions,
    class: className = ''
  }: { title: string; description?: string; actions?: Snippet; class?: string } = $props();
</script>

<div class="flex flex-col items-center text-center px-4 py-10 sm:px-6 sm:py-12 {className}" data-empty-state>
  <span class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-neutral-100 text-neutral-500" aria-hidden="true">
    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="7" cy="7" r="4.5" /><path d="M10.5 10.5L14 14" />
    </svg>
  </span>
  <p class="mt-3 text-sm font-semibold text-neutral-800">{title}</p>
  {#if description}
    <p class="mt-1 max-w-md text-sm text-neutral-500">{description}</p>
  {/if}
  {#if actions}
    <div class="mt-4 flex flex-wrap items-center justify-center gap-2">{@render actions()}</div>
  {/if}
</div>
