<script lang="ts">
  import type { Snippet } from 'svelte';

  export type Tab = { id: string; label: string };

  let {
    tabs,
    active = $bindable(tabs[0]?.id ?? ''),
    children
  }: { tabs: Tab[]; active?: string; children: Snippet<[string]> } = $props();
</script>

<div>
  <div role="tablist" class="flex gap-1 border-b border-neutral-200">
    {#each tabs as tab (tab.id)}
      <button
        type="button"
        role="tab"
        aria-selected={active === tab.id}
        class="h-10 px-3 -mb-px text-sm font-medium border-b-2 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-t {active === tab.id
          ? 'border-primary-600 text-primary-700'
          : 'border-transparent text-neutral-500 hover:text-neutral-800 hover:border-neutral-300'}"
        onclick={() => (active = tab.id)}
      >
        {tab.label}
      </button>
    {/each}
  </div>
  <div role="tabpanel" class="pt-4">
    {@render children(active)}
  </div>
</div>
