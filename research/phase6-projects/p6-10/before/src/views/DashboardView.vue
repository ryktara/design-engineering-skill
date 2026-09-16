<script setup lang="ts">
import { computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import KpiTile from '@/components/KpiTile.vue'
import ReasonTag from '@/components/ReasonTag.vue'
import { formatInt, formatMoney, relativeDay } from '@/utils/format'

const inventory = useInventoryStore()

const recent = computed(() => inventory.recentAdjustments.slice(0, 8))
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1>Dashboard</h1>
      <p class="muted">Warehouse 2 · updated just now</p>
    </div>

    <div class="kpi-grid">
      <KpiTile label="Total SKUs" :value="formatInt(inventory.products.length)" />
      <KpiTile label="Stock value" :value="formatMoney(inventory.stockValue)" />
      <KpiTile label="Below reorder point" :value="formatInt(inventory.lowStock.length)" />
      <KpiTile label="Out of stock" :value="formatInt(inventory.outOfStock.length)" />
    </div>

    <section class="panel">
      <div class="panel-header">
        <h2>Recent adjustments</h2>
        <RouterLink to="/adjustments">New adjustment</RouterLink>
      </div>
      <ul class="recent">
        <li v-for="adj in recent" :key="adj.id" class="recent-row">
          <div class="recent-main">
            <RouterLink :to="`/products/${adj.sku}`" class="mono">{{ adj.sku }}</RouterLink>
            <span class="recent-name">{{ inventory.productBySku.get(adj.sku)?.name }}</span>
          </div>
          <ReasonTag :reason="adj.reason" />
          <span class="qty">{{ adj.quantity > 0 ? '+' : '' }}{{ adj.quantity }}</span>
          <span class="muted when">{{ relativeDay(adj.createdAt) }}</span>
        </li>
      </ul>
    </section>

    <section class="panel">
      <div class="panel-header">
        <h2>Needs reordering</h2>
        <RouterLink to="/products">View all products</RouterLink>
      </div>
      <ul class="recent">
        <li v-for="p in inventory.lowStock.slice(0, 6)" :key="p.sku" class="recent-row">
          <div class="recent-main">
            <RouterLink :to="`/products/${p.sku}`" class="mono">{{ p.sku }}</RouterLink>
            <span class="recent-name">{{ p.name }}</span>
          </div>
          <span class="muted">{{ inventory.supplierName(p.supplierId) }}</span>
          <span class="qty">{{ p.onHand }} / {{ p.reorderPoint }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4);
}

.recent {
  list-style: none;
  margin: 0;
  padding: 0;
}

.recent-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.recent-row:last-child {
  border-bottom: 0;
}

.recent-main {
  flex: 1;
  min-width: 0;
  display: flex;
  gap: var(--space-3);
  align-items: baseline;
}

.recent-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.qty {
  width: 72px;
}

.when {
  width: 96px;
  font-size: var(--text-sm);
}
</style>
