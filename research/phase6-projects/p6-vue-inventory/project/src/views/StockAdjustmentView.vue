<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore, type AdjustmentReason } from '@/stores/inventory'
import AppButton from '@/components/AppButton.vue'
import AppDialog from '@/components/AppDialog.vue'
import ReasonTag from '@/components/ReasonTag.vue'
import { formatDate } from '@/utils/format'

const inventory = useInventoryStore()
const route = useRoute()
const router = useRouter()

const sku = ref(String(route.query.sku ?? ''))
const quantity = ref<number | null>(null)
const reason = ref<AdjustmentReason | ''>('')
const notes = ref('')
const error = ref('')
const saved = ref('')
const discardOpen = ref(false)
const keepEditingBtn = ref<{ $el: HTMLElement } | null>(null)
const discardTrigger = ref<{ $el: HTMLElement } | null>(null)
const skuField = ref<HTMLSelectElement | null>(null)

// Destructive confirmation opens on the safe action, and focus returns to the trigger.
watch(discardOpen, async (open) => {
  await nextTick()
  if (open) keepEditingBtn.value?.$el?.focus()
  else if (isDirty.value) discardTrigger.value?.$el?.focus()
  else skuField.value?.focus()
})

const reasons: Array<{ value: AdjustmentReason; label: string }> = [
  { value: 'received', label: 'Goods received' },
  { value: 'cycle-count', label: 'Cycle count correction' },
  { value: 'damaged', label: 'Damaged / written off' },
  { value: 'returned', label: 'Customer return' },
  { value: 'issued', label: 'Issued to works order' },
]

const selected = computed(() => inventory.productBySku.get(sku.value))

const isDirty = computed(
  () => sku.value !== '' || quantity.value !== null || reason.value !== '' || notes.value !== '',
)

function save() {
  error.value = ''
  if (!selected.value) {
    error.value = 'Choose a product.'
    return
  }
  if (quantity.value === null || quantity.value === 0) {
    error.value = 'Enter a non-zero quantity.'
    return
  }
  if (!reason.value) {
    error.value = 'Choose a reason.'
    return
  }
  inventory.addAdjustment({
    sku: sku.value,
    quantity: quantity.value,
    reason: reason.value,
    notes: notes.value.trim(),
  })
  saved.value = `Adjustment saved for ${sku.value}.`
  discard()
}

function requestDiscard() {
  if (!isDirty.value) return
  discardOpen.value = true
}

function confirmDiscard() {
  discardOpen.value = false
  discard()
}

function discard() {
  sku.value = ''
  quantity.value = null
  reason.value = ''
  notes.value = ''
  error.value = ''
  if (route.query.sku) router.replace({ name: 'adjustments' })
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1>Stock adjustments</h1>
    </div>

    <div class="layout">
      <form class="panel form" @submit.prevent="save">
        <div class="panel-header"><h2>New adjustment</h2></div>
        <div class="panel-body fields">
          <p v-if="saved" class="notice success">{{ saved }}</p>
          <p v-if="error" class="notice error">{{ error }}</p>

          <div>
            <label for="adj-sku">Product</label>
            <select id="adj-sku" ref="skuField" v-model="sku">
              <option value="">Select a product…</option>
              <option v-for="p in inventory.products" :key="p.sku" :value="p.sku">
                {{ p.sku }} — {{ p.name }}
              </option>
            </select>
            <p v-if="selected" class="hint">
              Currently {{ selected.onHand }} on hand · bin {{ selected.location }}
            </p>
          </div>

          <div class="row">
            <div>
              <label for="adj-qty">Quantity</label>
              <input id="adj-qty" v-model.number="quantity" type="number" step="1" />
              <p class="hint">Use a negative number to remove stock.</p>
            </div>
            <div>
              <label for="adj-reason">Reason</label>
              <select id="adj-reason" v-model="reason">
                <option value="">Select…</option>
                <option v-for="r in reasons" :key="r.value" :value="r.value">{{ r.label }}</option>
              </select>
            </div>
          </div>

          <div>
            <label for="adj-notes">Notes</label>
            <textarea id="adj-notes" v-model="notes" rows="3" placeholder="PO number, reference, etc."></textarea>
          </div>
        </div>
        <div class="form-footer">
          <AppButton variant="primary" type="submit">Save adjustment</AppButton>
          <AppButton ref="discardTrigger" variant="secondary" :disabled="!isDirty" @click="requestDiscard">Discard</AppButton>
        </div>
      </form>

      <AppDialog :open="discardOpen" title="Discard this adjustment?" @close="discardOpen = false">
        <p>The details you entered will be cleared. Nothing is written to stock.</p>
        <template #footer>
          <AppButton ref="keepEditingBtn" variant="secondary" @click="discardOpen = false">Keep editing</AppButton>
          <AppButton variant="danger" @click="confirmDiscard">Discard</AppButton>
        </template>
      </AppDialog>

      <section class="panel history">
        <div class="panel-header"><h2>History</h2></div>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>SKU</th>
              <th>Reason</th>
              <th>Qty</th>
              <th>User</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in inventory.recentAdjustments" :key="a.id">
              <td>{{ formatDate(a.createdAt) }}</td>
              <td><RouterLink :to="`/products/${a.sku}`" class="mono">{{ a.sku }}</RouterLink></td>
              <td><ReasonTag :reason="a.reason" /></td>
              <td>{{ a.quantity > 0 ? '+' : '' }}{{ a.quantity }}</td>
              <td>{{ a.user }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 420px minmax(0, 1fr);
  gap: var(--space-6);
  align-items: start;
}

.fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.fields select,
.fields input,
.fields textarea {
  width: 100%;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.hint {
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  margin-top: var(--space-1);
}

.form-footer {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--color-border);
}

.notice {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius);
  font-size: var(--text-sm);
}

.notice.success {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.notice.error {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}

.history th,
.history td {
  text-align: left;
  padding: var(--space-2) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.history th {
  font-size: var(--text-xs);
  text-transform: uppercase;
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
}

.history tbody tr:last-child td {
  border-bottom: 0;
}
</style>
