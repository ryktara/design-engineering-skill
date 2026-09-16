<script lang="ts">
  import type { HTMLSelectAttributes } from 'svelte/elements';

  export type Option = { value: string; label: string };

  let {
    label,
    options,
    placeholder,
    id = `select-${Math.random().toString(36).slice(2, 8)}`,
    value = $bindable(''),
    class: className = '',
    ...rest
  }: HTMLSelectAttributes & {
    label?: string;
    options: Option[];
    placeholder?: string;
    id?: string;
    value?: string;
  } = $props();
</script>

<div class="flex flex-col gap-1 {className}">
  {#if label}
    <label for={id} class="text-sm font-medium text-neutral-700">{label}</label>
  {/if}
  <select
    {id}
    bind:value
    class="h-9 px-3 pr-8 w-full rounded border border-neutral-300 bg-white text-sm text-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-neutral-50"
    {...rest}
  >
    {#if placeholder}
      <option value="">{placeholder}</option>
    {/if}
    {#each options as opt (opt.value)}
      <option value={opt.value}>{opt.label}</option>
    {/each}
  </select>
</div>
