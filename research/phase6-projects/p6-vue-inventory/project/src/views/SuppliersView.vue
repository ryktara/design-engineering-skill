<script setup lang="ts">
import { computed } from 'vue'
import { useInventoryStore, type Supplier } from '@/stores/inventory'
import DataTable, { type Column } from '@/components/DataTable.vue'

const inventory = useInventoryStore()

interface SupplierRow extends Supplier {
  productCount: number
  lowCount: number
}

const rows = computed<SupplierRow[]>(() =>
  inventory.suppliers.map((s) => {
    const items = inventory.productsForSupplier(s.id)
    return {
      ...s,
      productCount: items.length,
      lowCount: items.filter((p) => p.onHand <= p.reorderPoint).length,
    }
  }),
)

const columns: Column<SupplierRow>[] = [
  { key: 'id', label: 'ID', width: '100px' },
  { key: 'name', label: 'Supplier' },
  { key: 'contact', label: 'Contact' },
  { key: 'email', label: 'Email' },
  { key: 'city', label: 'City', width: '120px' },
  { key: 'leadTimeDays', label: 'Lead time', width: '100px', format: (v) => `${v} d` },
  { key: 'productCount', label: 'Products', width: '90px' },
  { key: 'lowCount', label: 'Low stock', width: '90px' },
]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1>Suppliers</h1>
      <p class="muted">{{ rows.length }} active suppliers</p>
    </div>

    <div class="panel">
      <DataTable :columns="columns" :rows="rows" row-key="id">
        <template #cell-id="{ value }">
          <span class="mono">{{ value }}</span>
        </template>
        <template #cell-email="{ value }">
          <a :href="`mailto:${value}`">{{ value }}</a>
        </template>
      </DataTable>
    </div>
  </div>
</template>
