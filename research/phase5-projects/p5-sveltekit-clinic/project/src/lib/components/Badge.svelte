<script lang="ts">
  import type { Snippet } from 'svelte';

  type Tone = 'neutral' | 'primary' | 'success' | 'warning' | 'danger';

  let { tone = 'neutral', children }: { tone?: Tone; children: Snippet } = $props();

  const tones: Record<Tone, string> = {
    neutral: 'bg-neutral-100 text-neutral-700 border-neutral-200',
    primary: 'bg-primary-50 text-primary-700 border-primary-200',
    success: 'bg-success-50 text-success-700 border-success-100',
    warning: 'bg-warning-50 text-warning-700 border-warning-100',
    danger: 'bg-danger-50 text-danger-700 border-danger-100'
  };
</script>

<span
  class="inline-flex items-center h-5 px-2 rounded-sm border text-xs font-medium whitespace-nowrap {tones[tone]}"
>
  {@render children()}
</span>
