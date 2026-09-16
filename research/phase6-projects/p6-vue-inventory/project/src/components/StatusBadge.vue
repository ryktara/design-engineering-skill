<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  onHand: number
  reorderPoint: number
}>()

const level = computed(() => {
  if (props.onHand === 0) return 'out'
  if (props.onHand <= props.reorderPoint) return 'low'
  return 'ok'
})
</script>

<template>
  <span :class="['badge', level]">{{ onHand }}</span>
</template>

<style scoped>
.badge {
  display: inline-block;
  padding: 2px var(--space-2);
  border-radius: var(--radius);
  font-size: var(--text-sm);
  font-weight: 500;
}

.ok {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.low {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.out {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}
</style>
