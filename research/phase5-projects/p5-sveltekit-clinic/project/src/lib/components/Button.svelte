<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLButtonAttributes } from 'svelte/elements';

  type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';
  type Size = 'sm' | 'md';

  let {
    variant = 'secondary',
    size = 'md',
    children,
    class: className = '',
    ...rest
  }: HTMLButtonAttributes & { variant?: Variant; size?: Size; children: Snippet } = $props();

  const base =
    'inline-flex items-center justify-center gap-2 rounded font-medium border transition-colors ' +
    'focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-1 ' +
    'disabled:opacity-50 disabled:cursor-not-allowed';

  const variants: Record<Variant, string> = {
    primary: 'bg-primary-600 border-primary-600 text-white hover:bg-primary-700 hover:border-primary-700',
    secondary: 'bg-white border-neutral-300 text-neutral-800 hover:bg-neutral-50',
    ghost: 'bg-transparent border-transparent text-neutral-700 hover:bg-neutral-100',
    danger: 'bg-white border-danger-600 text-danger-700 hover:bg-danger-50'
  };

  const sizes: Record<Size, string> = {
    sm: 'h-8 px-3 text-sm',
    md: 'h-9 px-4 text-sm'
  };
</script>

<button type="button" class="{base} {variants[variant]} {sizes[size]} {className}" {...rest}>
  {@render children()}
</button>
