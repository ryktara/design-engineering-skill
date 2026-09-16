<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore, type Product } from '@/stores/inventory'
import DataTable, { type Column, type SortState } from '@/components/DataTable.vue'
import FilterBar, { type Filters } from '@/components/FilterBar.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { formatMoney } from '@/utils/format'

const inventory = useInventoryStore()
const route = useRoute()
const router = useRouter()

const filters = ref<Filters>({ category: '', supplierId: '', lowOnly: false })
const sort = ref<SortState>({ key: 'sku', direction: 'asc' })

const query = computed(() => String(route.query.q ?? '').toLowerCase())

const filtered = computed(() =>
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

function sortValue(row: Product, key: string) {
  if (key === 'supplierId') return inventory.supplierName(row.supplierId)
  return (row as Record<string, any>)[key]
}

const rows = computed(() => {
  const { key, direction } = sort.value
  const factor = direction === 'asc' ? 1 : -1
  return [...filtered.value].sort((a, b) => {
    const av = sortValue(a, key)
    const bv = sortValue(b, key)
    if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * factor
    return String(av).localeCompare(String(bv), undefined, { numeric: true }) * factor
  })
})

const activeFilters = computed(() => {
  const chips: Array<{ id: keyof Filters; label: string }> = []
  if (filters.value.category) chips.push({ id: 'category', label: filters.value.category })
  if (filters.value.supplierId)
    chips.push({ id: 'supplierId', label: inventory.supplierName(filters.value.supplierId) })
  if (filters.value.lowOnly) chips.push({ id: 'lowOnly', label: 'Low stock only' })
  if (query.value) chips.push({ id: 'category', label: `Search: ${route.query.q}` })
  return chips
})

const columns: Column<Product>[] = [
  { key: 'sku', label: 'SKU', width: '110px', sortable: true },
  { key: 'name', label: 'Product', sortable: true },
  { key: 'category', label: 'Category', width: '130px', sortable: true },
  {
    key: 'supplierId',
    label: 'Supplier',
    sortable: true,
    format: (id) => inventory.supplierName(id),
  },
  { key: 'location', label: 'Bin', width: '80px', sortable: true },
  { key: 'onHand', label: 'On hand', width: '110px', numeric: true, sortable: true },
  { key: 'reorderPoint', label: 'Reorder at', width: '110px', numeric: true, sortable: true },
  {
    key: 'unitCost',
    label: 'Unit cost',
    width: '110px',
    numeric: true,
    sortable: true,
    format: (v) => formatMoney(v),
  },
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
        <ul v-if="activeFilters.length" class="chips" aria-label="Active filters">
          <li v-for="chip in activeFilters" :key="chip.label" class="chip">{{ chip.label }}</li>
        </ul>
      </div>
      <DataTable
        :columns="columns"
        :rows="rows"
        row-key="sku"
        paginated
        rows-activatable
        :sort="sort"
        empty-text="No products match these filters. Clear a filter to see more."
        @update:sort="sort = $event"
        @row-click="openProduct"
      >
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

<style scoped>
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  list-style: none;
  margin: var(--space-3) 0 0;
  padding: 0;
}

.chip {
  padding: 2px var(--space-2);
  border-radius: var(--radius);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: var(--text-xs);
}
</style>
