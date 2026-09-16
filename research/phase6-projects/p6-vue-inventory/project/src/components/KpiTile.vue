<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    value: string
    hint?: string
    /** Emphasis for exception tiles; 'neutral' keeps the original look. */
    tone?: 'neutral' | 'warning' | 'danger'
    /** When set, the whole tile becomes a drill-down link. */
    to?: string
  }>(),
  { tone: 'neutral' },
)
</script>

<template>
  <component
    :is="to ? 'RouterLink' : 'div'"
    :to="to"
    :class="['kpi', 'panel', `tone-${tone}`, { 'kpi-link': to }]"
  >
    <p class="kpi-label">{{ label }}</p>
    <p class="kpi-value">{{ value }}</p>
    <p v-if="hint" class="kpi-hint">{{ hint }}</p>
  </component>
</template>

<style scoped>
.kpi {
  display: block;
  padding: var(--space-4);
  border-left: 3px solid transparent;
  color: var(--color-text);
}

.kpi-label {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.kpi-value {
  font-size: var(--text-2xl);
  font-weight: 600;
  margin-top: var(--space-1);
  font-variant-numeric: tabular-nums;
}

.kpi-hint {
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  margin-top: var(--space-1);
}

.tone-warning {
  border-left-color: var(--color-warning);
}

.tone-warning .kpi-value {
  color: var(--color-warning);
}

.tone-danger {
  border-left-color: var(--color-danger);
}

.tone-danger .kpi-value {
  color: var(--color-danger);
}

.kpi-link:hover {
  text-decoration: none;
  background: var(--color-surface-muted);
}

.kpi-link:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 1px;
}

.kpi-link .kpi-label {
  text-decoration: underline;
  text-decoration-color: var(--color-border-strong);
}
</style>
