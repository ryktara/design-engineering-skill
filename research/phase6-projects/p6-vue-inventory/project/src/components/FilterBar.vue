<script setup lang="ts">
import { ref, watch } from 'vue'
import { CATEGORIES } from '@/data/seed'
import { useInventoryStore } from '@/stores/inventory'

export interface Filters {
  category: string
  supplierId: string
  lowOnly: boolean
}

const emit = defineEmits<{ (e: 'change', filters: Filters): void }>()

const inventory = useInventoryStore()

const category = ref('')
const supplierId = ref('')
const lowOnly = ref(false)

watch([category, supplierId, lowOnly], () => {
  emit('change', { category: category.value, supplierId: supplierId.value, lowOnly: lowOnly.value })
})

function clear() {
  category.value = ''
  supplierId.value = ''
  lowOnly.value = false
}
</script>

<template>
  <div class="filter-bar">
    <div class="field">
      <label for="f-category">Category</label>
      <select id="f-category" v-model="category">
        <option value="">All categories</option>
        <option v-for="c in CATEGORIES" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>

    <div class="field">
      <label for="f-supplier">Supplier</label>
      <select id="f-supplier" v-model="supplierId">
        <option value="">All suppliers</option>
        <option v-for="s in inventory.suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
      </select>
    </div>

    <label class="check">
      <input v-model="lowOnly" type="checkbox" />
      Low stock only
    </label>

    <button type="button" class="link" @click="clear">Clear</button>
  </div>
</template>

<style scoped>
.filter-bar {
  display: flex;
  align-items: flex-end;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.field select {
  min-width: 180px;
}

.check {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  min-height: 34px;
  margin: 0;
  color: var(--color-text);
}

.check input {
  min-height: auto;
}

.link {
  background: none;
  border: 0;
  color: var(--color-primary);
  cursor: pointer;
  min-height: 34px;
  padding: 0 var(--space-2);
}
</style>
