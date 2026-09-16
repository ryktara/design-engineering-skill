<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    title,
    actions,
    children,
    padded = true,
    class: className = ''
  }: { title?: string; actions?: Snippet; children: Snippet; padded?: boolean; class?: string } =
    $props();
</script>

<section class="bg-white border border-neutral-200 rounded {className}">
  {#if title || actions}
    <header class="flex items-center justify-between px-4 h-12 border-b border-neutral-200">
      {#if title}
        <h2 class="text-sm font-semibold text-neutral-800">{title}</h2>
      {/if}
      {#if actions}
        <div class="flex items-center gap-2">{@render actions()}</div>
      {/if}
    </header>
  {/if}
  <div class={padded ? 'p-4' : ''}>
    {@render children()}
  </div>
</section>
