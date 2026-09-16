<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    open = $bindable(false),
    title,
    children,
    footer
  }: { open?: boolean; title: string; children: Snippet; footer?: Snippet } = $props();

  function close() {
    open = false;
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') close();
  }
</script>

<svelte:window onkeydown={open ? onKeydown : undefined} />

{#if open}
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <button
      type="button"
      class="absolute inset-0 bg-neutral-900/40"
      aria-label="Close dialog"
      onclick={close}
    ></button>
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      class="relative w-full max-w-lg bg-white border border-neutral-200 rounded shadow-xl"
    >
      <header class="flex items-center justify-between px-5 h-12 border-b border-neutral-200">
        <h2 id="modal-title" class="text-base font-semibold text-neutral-800">{title}</h2>
        <button
          type="button"
          class="h-8 w-8 inline-flex items-center justify-center rounded text-neutral-500 hover:bg-neutral-100 hover:text-neutral-800"
          aria-label="Close"
          onclick={close}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M4 4l8 8M12 4l-8 8" stroke-linecap="round" />
          </svg>
        </button>
      </header>
      <div class="p-5">
        {@render children()}
      </div>
      {#if footer}
        <footer class="flex justify-end gap-2 px-5 h-14 items-center border-t border-neutral-200 bg-neutral-50 rounded-b">
          {@render footer()}
        </footer>
      {/if}
    </div>
  </div>
{/if}
