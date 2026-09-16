<script setup lang="ts">
import { computed, ref } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import AppButton from '@/components/AppButton.vue'
import AppDialog from '@/components/AppDialog.vue'
import ReasonTag from '@/components/ReasonTag.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { formatDate, formatMoney } from '@/utils/format'

const props = defineProps<{ sku: string }>()

const inventory = useInventoryStore()

const product = computed(() => inventory.productBySku.get(props.sku))
const supplier = computed(() =>
  product.value ? inventory.supplierById.get(product.value.supplierId) : undefined,
)
const movements = computed(() => inventory.movementsFor(props.sku))

type Tab = 'overview' | 'movements' | 'supplier'
const tab = ref<Tab>('overview')
const tabs: Array<{ id: Tab; label: string }> = [
  { id: 'overview', label: 'Overview' },
  { id: 'movements', label: 'Movements' },
  { id: 'supplier', label: 'Supplier' },
]

const archiveOpen = ref(false)
function archive() {
  archiveOpen.value = false
}
</script>

<template>
  <div v-if="product" class="page">
    <div class="page-header">
      <div>
        <p class="muted"><RouterLink to="/products">Products</RouterLink> / {{ product.sku }}</p>
        <h1>{{ product.name }}</h1>
      </div>
      <div class="actions">
        <AppButton variant="secondary" @click="archiveOpen = true">Archive</AppButton>
        <RouterLink :to="{ name: 'adjustments', query: { sku: product.sku } }">
          <AppButton variant="primary">Adjust stock</AppButton>
        </RouterLink>
      </div>
    </div>

    <div class="tabs">
      <button
        v-for="t in tabs"
        :key="t.id"
        type="button"
        :class="['tab', { active: tab === t.id }]"
        @click="tab = t.id"
      >
        {{ t.label }}
      </button>
    </div>

    <section v-if="tab === 'overview'" class="panel">
      <dl class="facts">
        <div><dt>SKU</dt><dd class="mono">{{ product.sku }}</dd></div>
        <div><dt>Category</dt><dd>{{ product.category }}</dd></div>
        <div><dt>Bin location</dt><dd>{{ product.location }}</dd></div>
        <div>
          <dt>On hand</dt>
          <dd><StatusBadge :on-hand="product.onHand" :reorder-point="product.reorderPoint" /></dd>
        </div>
        <div><dt>Reorder point</dt><dd>{{ product.reorderPoint }}</dd></div>
        <div><dt>Unit cost</dt><dd>{{ formatMoney(product.unitCost) }}</dd></div>
        <div><dt>Stock value</dt><dd>{{ formatMoney(product.unitCost * product.onHand) }}</dd></div>
        <div><dt>Supplier</dt><dd>{{ supplier?.name }}</dd></div>
      </dl>
    </section>

    <section v-else-if="tab === 'movements'" class="panel">
      <table v-if="movements.length" class="movements">
        <thead>
          <tr>
            <th>Date</th>
            <th>Reference</th>
            <th>Reason</th>
            <th>Quantity</th>
            <th>User</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in movements" :key="m.id">
            <td>{{ formatDate(m.createdAt) }}</td>
            <td class="mono">{{ m.id }}</td>
            <td><ReasonTag :reason="m.reason" /></td>
            <td>{{ m.quantity > 0 ? '+' : '' }}{{ m.quantity }}</td>
            <td>{{ m.user }}</td>
            <td class="muted">{{ m.notes || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="panel-body muted">No movements recorded for this product.</p>
    </section>

    <section v-else class="panel">
      <dl v-if="supplier" class="facts">
        <div><dt>Supplier</dt><dd>{{ supplier.name }}</dd></div>
        <div><dt>Contact</dt><dd>{{ supplier.contact }}</dd></div>
        <div><dt>Email</dt><dd><a :href="`mailto:${supplier.email}`">{{ supplier.email }}</a></dd></div>
        <div><dt>City</dt><dd>{{ supplier.city }}</dd></div>
        <div><dt>Lead time</dt><dd>{{ supplier.leadTimeDays }} days</dd></div>
        <div>
          <dt>Other products</dt>
          <dd>{{ inventory.productsForSupplier(supplier.id).length - 1 }}</dd>
        </div>
      </dl>
    </section>

    <AppDialog :open="archiveOpen" title="Archive product" @close="archiveOpen = false">
      <p>
        Archiving <strong>{{ product.name }}</strong> hides it from the catalogue and reports.
        Existing movements are kept.
      </p>
      <template #footer>
        <AppButton variant="secondary" @click="archiveOpen = false">Cancel</AppButton>
        <AppButton variant="danger" @click="archive">Archive</AppButton>
      </template>
    </AppDialog>
  </div>

  <div v-else class="page">
    <h1>Product not found</h1>
    <p><RouterLink to="/products">Back to products</RouterLink></p>
  </div>
</template>

<style scoped>
.actions {
  display: flex;
  gap: var(--space-2);
}

.actions a:hover {
  text-decoration: none;
}

.tabs {
  display: flex;
  gap: var(--space-1);
  border-bottom: 1px solid var(--color-border);
}

.tab {
  background: none;
  border: 0;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-muted);
  cursor: pointer;
}

.tab.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
  font-weight: 500;
}

.facts {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4) var(--space-6);
  margin: 0;
  padding: var(--space-4);
}

.facts dt {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--color-text-muted);
}

.facts dd {
  margin: var(--space-1) 0 0;
}

.movements th,
.movements td {
  text-align: left;
  padding: var(--space-2) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.movements th {
  font-size: var(--text-xs);
  text-transform: uppercase;
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
}

.movements tbody tr:last-child td {
  border-bottom: 0;
}
</style>
