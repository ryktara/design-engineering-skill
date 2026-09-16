<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore, type Product } from '@/stores/inventory'
import DataTable, { type Column } from '@/components/DataTable.vue'
import FilterBar, { type Filters } from '@/components/FilterBar.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { formatMoney } from '@/utils/format'

const inventory = useInventoryStore()
const route = useRoute()
const router = useRouter()

const filters = ref<Filters>({ category: '', supplierId: '', lowOnly: false })

const query = computed(() => String(route.query.q ?? '').toLowerCase())

const rows = computed(() =>
  inventory.products.filter((p) => {
    if (filters.value.category && p.category !== filters.value.category) return false
    if (filters.value.supplierId && p.supplierId !== filters.value.supplierId) return false
    if (filters.value.lowOnly && p.onHand > p.reorderPoint) return false
    if (query.value) {
      const hay = `${p.sku} ${p.name}`.toLowerCase()
      if (!hay.includes(query.value)) return false
    }
    return true
  }),
)

const columns: Column<Product>[] = [
  { key: 'sku', label: 'SKU', width: '110px' },
  { key: 'name', label: 'Product' },
  { key: 'category', label: 'Category', width: '130px' },
  { key: 'supplierId', label: 'Supplier', format: (id) => inventory.supplierName(id) },
  { key: 'location', label: 'Bin', width: '80px' },
  { key: 'onHand', label: 'On hand', width: '100px' },
  { key: 'reorderPoint', label: 'Reorder at', width: '100px' },
  { key: 'unitCost', label: 'Unit cost', width: '110px', format: (v) => formatMoney(v) },
]

function openProduct(row: Product) {
  router.push({ name: 'product-detail', params: { sku: row.sku } })
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>Products</h1>
        <p class="muted">{{ rows.length }} of {{ inventory.products.length }} products</p>
      </div>
      <RouterLink to="/adjustments">New adjustment</RouterLink>
    </div>

    <div class="panel">
      <div class="panel-body">
        <FilterBar @change="filters = $event" />
      </div>
      <DataTable :columns="columns" :rows="rows" row-key="sku" @row-click="openProduct">
        <template #cell-sku="{ value }">
          <span class="mono">{{ value }}</span>
        </template>
        <template #cell-onHand="{ row }">
          <StatusBadge :on-hand="row.onHand" :reorder-point="row.reorderPoint" />
        </template>
      </DataTable>
    </div>
  </div>
</template>
