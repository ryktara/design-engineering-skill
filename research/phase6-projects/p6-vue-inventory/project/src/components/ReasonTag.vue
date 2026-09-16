<script setup lang="ts">
import type { AdjustmentReason } from '@/stores/inventory'

defineProps<{ reason: AdjustmentReason }>()

const labels: Record<AdjustmentReason, string> = {
  received: 'Received',
  'cycle-count': 'Cycle count',
  damaged: 'Damaged',
  returned: 'Returned',
  issued: 'Issued',
}
</script>

<template>
  <span class="tag">{{ labels[reason] }}</span>
</template>

<style scoped>
.tag {
  display: inline-block;
  padding: 1px var(--space-2);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  white-space: nowrap;
}
</style>
