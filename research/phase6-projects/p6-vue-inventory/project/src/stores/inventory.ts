import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import {
  adjustments as seedAdjustments,
  products as seedProducts,
  suppliers as seedSuppliers,
  type Adjustment,
  type AdjustmentReason,
  type Product,
  type Supplier,
} from '@/data/seed'

export type { Adjustment, AdjustmentReason, Product, Supplier }

export const useInventoryStore = defineStore('inventory', () => {
  const products = ref<Product[]>(seedProducts.map((p) => ({ ...p })))
  const suppliers = ref<Supplier[]>(seedSuppliers)
  const adjustments = ref<Adjustment[]>(seedAdjustments.map((a) => ({ ...a })))

  const productBySku = computed(() => {
    const map = new Map<string, Product>()
    for (const p of products.value) map.set(p.sku, p)
    return map
  })

  const supplierById = computed(() => {
    const map = new Map<string, Supplier>()
    for (const s of suppliers.value) map.set(s.id, s)
    return map
  })

  const lowStock = computed(() => products.value.filter((p) => p.onHand <= p.reorderPoint))

  const outOfStock = computed(() => products.value.filter((p) => p.onHand === 0))

  const stockValue = computed(() =>
    products.value.reduce((sum, p) => sum + p.onHand * p.unitCost, 0),
  )

  const recentAdjustments = computed(() =>
    [...adjustments.value].sort((a, b) => b.createdAt.localeCompare(a.createdAt)),
  )

  function movementsFor(sku: string) {
    return recentAdjustments.value.filter((a) => a.sku === sku)
  }

  function supplierName(id: string) {
    return supplierById.value.get(id)?.name ?? '—'
  }

  function productsForSupplier(id: string) {
    return products.value.filter((p) => p.supplierId === id)
  }

  function addAdjustment(input: {
    sku: string
    quantity: number
    reason: AdjustmentReason
    notes: string
  }) {
    const product = productBySku.value.get(input.sku)
    if (!product) throw new Error(`Unknown SKU ${input.sku}`)
    product.onHand = Math.max(0, product.onHand + input.quantity)
    const nextNumber = adjustments.value.length + 3121
    adjustments.value.unshift({
      id: `ADJ-${String(nextNumber).padStart(5, '0')}`,
      sku: input.sku,
      quantity: input.quantity,
      reason: input.reason,
      notes: input.notes,
      user: 'you',
      createdAt: new Date().toISOString(),
    })
  }

  return {
    products,
    suppliers,
    adjustments,
    productBySku,
    supplierById,
    lowStock,
    outOfStock,
    stockValue,
    recentAdjustments,
    movementsFor,
    supplierName,
    productsForSupplier,
    addAdjustment,
  }
})
