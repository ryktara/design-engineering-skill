<script setup lang="ts">
import { ref } from 'vue'
import { useUiStore } from '@/stores/ui'
import AppButton from '@/components/AppButton.vue'

const ui = useUiStore()

const warehouseName = ref('Warehouse 2')
const currency = ref('GBP')
const lowStockEmail = ref(true)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1>Settings</h1>
    </div>

    <section class="panel">
      <div class="panel-header"><h2>Appearance</h2></div>
      <div class="panel-body">
        <label>Theme</label>
        <div class="theme-toggle">
          <button
            type="button"
            :class="['seg', { active: ui.theme === 'light' }]"
            @click="ui.setTheme('light')"
          >
            Light
          </button>
          <button
            type="button"
            :class="['seg', { active: ui.theme === 'dark' }]"
            @click="ui.setTheme('dark')"
          >
            Dark
          </button>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-header"><h2>Warehouse</h2></div>
      <div class="panel-body fields">
        <div>
          <label for="s-name">Warehouse name</label>
          <input id="s-name" v-model="warehouseName" type="text" />
        </div>
        <div>
          <label for="s-currency">Currency</label>
          <select id="s-currency" v-model="currency">
            <option value="GBP">GBP (£)</option>
            <option value="EUR">EUR (€)</option>
            <option value="USD">USD ($)</option>
          </select>
        </div>
        <label class="check">
          <input v-model="lowStockEmail" type="checkbox" />
          Email me a daily low-stock summary
        </label>
      </div>
      <div class="footer">
        <AppButton variant="primary">Save changes</AppButton>
      </div>
    </section>
  </div>
</template>

<style scoped>
.theme-toggle {
  display: inline-flex;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius);
  overflow: hidden;
}

.seg {
  background: var(--color-surface);
  border: 0;
  padding: 6px var(--space-4);
  cursor: pointer;
}

.seg + .seg {
  border-left: 1px solid var(--color-border-strong);
}

.seg.active {
  background: var(--color-primary);
  color: var(--color-on-primary);
}

.fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-width: 420px;
}

.fields input,
.fields select {
  width: 100%;
}

.check {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text);
}

.check input {
  width: auto;
  min-height: auto;
}

.footer {
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--color-border);
}
</style>
