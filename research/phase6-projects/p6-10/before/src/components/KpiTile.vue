<script setup lang="ts">
defineProps<{
  label: string
  value: string
  hint?: string
}>()
</script>

<template>
  <div class="kpi panel">
    <p class="kpi-label">{{ label }}</p>
    <p class="kpi-value">{{ value }}</p>
    <p v-if="hint" class="kpi-hint">{{ hint }}</p>
  </div>
</template>

<style scoped>
.kpi {
  padding: var(--space-4);
}

.kpi-label {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.kpi-value {
  font-size: var(--text-2xl);
  font-weight: 600;
  margin-top: var(--space-1);
}

.kpi-hint {
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  margin-top: var(--space-1);
}
</style>
