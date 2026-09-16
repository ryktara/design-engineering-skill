<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'danger'
    type?: 'button' | 'submit'
    disabled?: boolean
  }>(),
  { variant: 'secondary', type: 'button', disabled: false },
)
</script>

<template>
  <button :type="type" :class="['btn', `btn-${variant}`]" :disabled="disabled">
    <slot />
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  min-height: 34px;
  padding: 0 var(--space-4);
  border-radius: var(--radius);
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-on-primary);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: var(--color-surface);
  border-color: var(--color-border-strong);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-surface-muted);
}

.btn-danger {
  background: var(--color-primary);
  color: var(--color-on-primary);
}

.btn-danger:hover:not(:disabled) {
  background: var(--color-primary-hover);
}
</style>
