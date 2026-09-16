<script setup lang="ts" generic="T extends Record<string, any>">
export interface Column<Row> {
  key: keyof Row & string
  label: string
  width?: string
  format?: (value: any, row: Row) => string
}

defineProps<{
  columns: Column<T>[]
  rows: T[]
  rowKey: keyof T & string
  emptyText?: string
}>()

const emit = defineEmits<{ (e: 'row-click', row: T): void }>()
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :style="{ width: col.width }">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="row in rows"
          :key="String(row[rowKey])"
          :class="{ clickable: true }"
          @click="emit('row-click', row)"
        >
          <td v-for="col in columns" :key="col.key">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ col.format ? col.format(row[col.key], row) : row[col.key] }}
            </slot>
          </td>
        </tr>
        <tr v-if="rows.length === 0">
          <td :colspan="columns.length" class="empty">{{ emptyText ?? 'No rows' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-wrap {
  overflow-x: auto;
}

.data-table th,
.data-table td {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.data-table th {
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
  white-space: nowrap;
}

.data-table tbody tr.clickable:hover {
  background: var(--color-surface-muted);
  cursor: pointer;
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.empty {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--space-8) var(--space-4);
}
</style>
