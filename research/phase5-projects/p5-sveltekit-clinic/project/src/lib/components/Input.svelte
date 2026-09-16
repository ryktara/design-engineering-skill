<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements';

  let {
    label,
    hint,
    error,
    id = `input-${Math.random().toString(36).slice(2, 8)}`,
    value = $bindable(''),
    class: className = '',
    ...rest
  }: HTMLInputAttributes & { label?: string; hint?: string; error?: string; id?: string } =
    $props();
</script>

<div class="flex flex-col gap-1 {className}">
  {#if label}
    <label for={id} class="text-sm font-medium text-neutral-700">{label}</label>
  {/if}
  <input
    {id}
    bind:value
    class="h-9 px-3 w-full rounded border bg-white text-sm text-neutral-800 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-neutral-50 disabled:text-neutral-500 {error
      ? 'border-danger-500'
      : 'border-neutral-300'}"
    aria-invalid={error ? 'true' : undefined}
    {...rest}
  />
  {#if error}
    <p class="text-xs text-danger-600">{error}</p>
  {:else if hint}
    <p class="text-xs text-neutral-500">{hint}</p>
  {/if}
</div>
