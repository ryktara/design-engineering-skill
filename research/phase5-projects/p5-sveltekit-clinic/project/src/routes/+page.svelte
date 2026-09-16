<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  onMount(() => {
    goto('/appointments', { replaceState: true });
  });
</script>

<p class="text-sm text-neutral-500">Redirecting to appointments…</p>
