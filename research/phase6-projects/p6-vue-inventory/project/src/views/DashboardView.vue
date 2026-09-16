<script setup lang="ts">
import { computed } from 'vue'
import { useInventoryStore, type Product } from '@/stores/inventory'
import KpiTile from '@/components/KpiTile.vue'
import ReasonTag from '@/components/ReasonTag.vue'
import { formatInt, formatMoney, relativeDay } from '@/utils/format'

const inventory = useInventoryStore()

const recent = computed(() => inventory.recentAdjustments.slice(0, 8))

type Urgency = 'out' | 'critical' | 'low'

interface ReorderRow {
  product: Product
  urgency: Urgency
  shortfall: number
  suggested: number
  leadTimeDays: number
  supplier: string
}

const URGENCY_LABEL: Record<Urgency, string> = {
  out: 'Out of stock',
  critical: 'Critical',
  low: 'Below reorder point',
}

const URGENCY_ICON: Record<Urgency, string> = {
  out: '●',
  critical: '▲',
  low: '△',
}

const RANK: Record<Urgency, number> = { out: 0, critical: 1, low: 2 }

/** Items at or below their reorder point, worst first. */
const reorderRows = computed<ReorderRow[]>(() =>
  inventory.lowStock
    .map((product) => {
      const urgency: Urgency =
        product.onHand === 0
          ? 'out'
          : product.onHand <= product.reorderPoint / 2
            ? 'critical'
            : 'low'
      const supplier = inventory.supplierById.get(product.supplierId)
      return {
        product,
        urgency,
        shortfall: Math.max(0, product.reorderPoint - product.onHand),
        // Order back up to twice the reorder point.
        suggested: product.reorderPoint * 2 - product.onHand,
        leadTimeDays: supplier?.leadTimeDays ?? 0,
        supplier: inventory.supplierName(product.supplierId),
      }
    })
    .sort(
      (a, b) =>
        RANK[a.urgency] - RANK[b.urgency] ||
        b.leadTimeDays - a.leadTimeDays ||
        b.shortfall - a.shortfall,
    ),
)

const topReorder = computed(() => reorderRows.value.slice(0, 8))
const outOfStockCount = computed(() => inventory.outOfStock.length)
const criticalCount = computed(
  () => reorderRows.value.filter((r) => r.urgency !== 'low').length,
)
const suggestedCost = computed(() =>
  reorderRows.value.reduce((sum, r) => sum + r.suggested * r.product.unitCost, 0),
)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1>Dashboard</h1>
      <p class="muted">Warehouse 2 · updated just now</p>
    </div>

    <div class="kpi-grid">
      <KpiTile
        label="Needs reordering today"
        :value="formatInt(reorderRows.length)"
        :hint="`${formatInt(outOfStockCount)} out of stock · ${formatInt(criticalCount)} urgent`"
        :tone="outOfStockCount > 0 ? 'danger' : 'warning'"
        to="/products"
      />
      <KpiTile
        label="Suggested order value"
        :value="formatMoney(suggestedCost)"
        hint="To bring every flagged item back to 2× its reorder point"
      />
      <KpiTile
        label="Total SKUs"
        :value="formatInt(inventory.products.length)"
        :hint="`${formatInt(inventory.products.length - reorderRows.length)} at healthy stock`"
      />
      <KpiTile label="Stock value" :value="formatMoney(inventory.stockValue)" />
    </div>

    <section class="panel" aria-labelledby="reorder-heading">
      <div class="panel-header">
        <div class="panel-title">
          <h2 id="reorder-heading">
            Needs reordering today
            <span class="count">{{ formatInt(reorderRows.length) }}</span>
          </h2>
          <p class="rule muted">On hand at or below the reorder point · longest lead time first</p>
        </div>
        <RouterLink to="/products">View all products</RouterLink>
      </div>
      <div v-if="topReorder.length" class="recent-row reorder-row col-head muted" aria-hidden="true">
        <span class="urgency">Status</span>
        <span class="recent-main">Item</span>
        <span class="supplier">Supplier · lead time</span>
        <span class="qty num">On hand / point</span>
        <span class="order num">Suggested</span>
      </div>
      <ul v-if="topReorder.length" class="recent">
        <li v-for="row in topReorder" :key="row.product.sku" class="recent-row reorder-row">
          <span :class="['urgency', row.urgency]">
            <span aria-hidden="true">{{ URGENCY_ICON[row.urgency] }}</span>
            {{ URGENCY_LABEL[row.urgency] }}
          </span>
          <div class="recent-main">
            <RouterLink :to="`/products/${row.product.sku}`" class="mono">{{
              row.product.sku
            }}</RouterLink>
            <span class="recent-name">{{ row.product.name }}</span>
          </div>
          <span class="supplier muted"
            >{{ row.supplier }} · {{ row.leadTimeDays }}d lead</span
          >
          <span class="qty num">
            {{ row.product.onHand }} / {{ row.product.reorderPoint }}
            <span class="visually-hidden">on hand of reorder point</span>
          </span>
          <span class="order num"
            >order {{ formatInt(row.suggested) }}
            <span class="visually-hidden">units suggested</span></span
          >
        </li>
      </ul>
      <p v-else class="panel-body muted">
        Nothing to reorder today — every SKU is above its reorder point.
      </p>
      <p v-if="reorderRows.length > topReorder.length" class="panel-body more muted">
        {{ formatInt(reorderRows.length - topReorder.length) }} more items below their reorder
        point.
        <RouterLink to="/products">See the full list</RouterLink>
      </p>
    </section>

    <section class="panel" aria-labelledby="recent-heading">
      <div class="panel-header">
        <h2 id="recent-heading">Recent adjustments</h2>
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

.panel-title {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.count {
  display: inline-block;
  margin-left: var(--space-2);
  padding: 0 var(--space-2);
  border-radius: var(--radius);
  background: var(--color-surface-muted);
  border: 1px solid var(--color-border-strong);
  font-size: var(--text-sm);
  font-variant-numeric: tabular-nums;
}

.rule {
  font-size: var(--text-xs);
}

.reorder-row .qty,
.order {
  font-variant-numeric: tabular-nums;
}

.num {
  text-align: right;
}

.order {
  width: 96px;
  font-size: var(--text-sm);
}

.supplier {
  width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: var(--text-sm);
}

.urgency {
  width: 150px;
  flex-shrink: 0;
  font-size: var(--text-sm);
  font-weight: 500;
}

.urgency.out {
  color: var(--color-danger);
}

.urgency.critical {
  color: var(--color-warning);
}

.urgency.low {
  color: var(--color-text-muted);
}

.col-head {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  background: var(--color-surface-muted);
  padding-top: var(--space-1);
  padding-bottom: var(--space-1);
}

.col-head .qty,
.col-head .order {
  font-size: var(--text-xs);
}

.more {
  border-top: 1px solid var(--color-border);
  font-size: var(--text-sm);
}

@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .supplier {
    display: none;
  }
}

@media (max-width: 600px) {
  .kpi-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .col-head {
    display: none;
  }

  .reorder-row {
    flex-wrap: wrap;
    gap: var(--space-2);
  }

  .urgency {
    width: auto;
  }

  .recent-main {
    flex-basis: 100%;
  }
}
</style>
