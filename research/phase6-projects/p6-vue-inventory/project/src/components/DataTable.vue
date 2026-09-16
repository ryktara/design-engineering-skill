<script setup lang="ts" generic="T extends Record<string, any>">
import { computed, ref, watch } from "vue";

export interface Column<Row> {
  key: keyof Row & string;
  label: string;
  width?: string;
  /** Right-align and use tabular figures. Set on quantity / money columns. */
  numeric?: boolean;
  /** Opt in to header sorting for this column. */
  sortable?: boolean;
  format?: (value: any, row: Row) => string;
}

export interface SortState {
  key: string;
  direction: "asc" | "desc";
}

const props = withDefaults(
  defineProps<{
    columns: Column<T>[];
    rows: T[];
    rowKey: keyof T & string;
    emptyText?: string;
    /** Show the page-size picker and pager below the table. */
    paginated?: boolean;
    pageSize?: number;
    sort?: SortState | null;
    /** Rows become keyboard-reachable (one Tab stop, arrows move, Enter opens). */
    rowsActivatable?: boolean;
  }>(),
  { paginated: false, pageSize: 50, sort: null, rowsActivatable: false },
);

const emit = defineEmits<{
  (e: "row-click", row: T): void;
  (e: "update:sort", sort: SortState): void;
}>();

const PAGE_SIZES = [25, 50, 100];

const page = ref(1);
const size = ref(props.pageSize);
const focusedIndex = ref(0);
const tbody = ref<HTMLElement | null>(null);
const wrap = ref<HTMLElement | null>(null);

const total = computed(() => props.rows.length);
const pageCount = computed(() =>
  Math.max(1, Math.ceil(total.value / size.value)),
);
const visibleRows = computed(() => {
  if (!props.paginated) return props.rows;
  const start = (page.value - 1) * size.value;
  return props.rows.slice(start, start + size.value);
});
const firstShown = computed(() =>
  total.value === 0 ? 0 : (page.value - 1) * size.value + 1,
);
const lastShown = computed(() =>
  Math.min(page.value * size.value, total.value),
);

// Filters or a new sort can shrink the set under the current page.
watch([total, size], () => {
  if (page.value > pageCount.value) page.value = pageCount.value;
});
watch(visibleRows, () => {
  if (focusedIndex.value > visibleRows.value.length - 1) focusedIndex.value = 0;
});

function ariaSort(col: Column<T>) {
  if (!col.sortable) return undefined;
  if (props.sort?.key !== col.key) return "none";
  return props.sort.direction === "asc" ? "ascending" : "descending";
}

function toggleSort(col: Column<T>) {
  if (!col.sortable) return;
  const direction =
    props.sort?.key === col.key && props.sort.direction === "asc"
      ? "desc"
      : "asc";
  emit("update:sort", { key: col.key, direction });
  page.value = 1;
  wrap.value?.scrollTo({ top: 0 });
}

function goTo(next: number) {
  page.value = Math.min(pageCount.value, Math.max(1, next));
  focusedIndex.value = 0;
  // A new page starts at row 1, so the scroll region must too.
  wrap.value?.scrollTo({ top: 0 });
}

function focusRow(index: number) {
  const target =
    tbody.value?.querySelectorAll<HTMLElement>("tr[data-row]")[index];
  if (target) {
    focusedIndex.value = index;
    target.focus();
  }
}

function onRowKeydown(event: KeyboardEvent, row: T, index: number) {
  switch (event.key) {
    case "ArrowDown":
      event.preventDefault();
      focusRow(Math.min(index + 1, visibleRows.value.length - 1));
      break;
    case "ArrowUp":
      event.preventDefault();
      focusRow(Math.max(index - 1, 0));
      break;
    case "Home":
      event.preventDefault();
      focusRow(0);
      break;
    case "End":
      event.preventDefault();
      focusRow(visibleRows.value.length - 1);
      break;
    case "Enter":
    case " ":
      event.preventDefault();
      emit("row-click", row);
      break;
  }
}
</script>

<template>
  <div class="table-block">
    <div ref="wrap" :class="['table-wrap', { scrollable: paginated }]">
      <table class="data-table">
        <thead>
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              :style="{ width: col.width }"
              :class="{ numeric: col.numeric }"
              :aria-sort="ariaSort(col)"
              scope="col"
            >
              <button
                v-if="col.sortable"
                type="button"
                class="sort"
                @click="toggleSort(col)"
              >
                {{ col.label }}
                <span class="sort-mark" aria-hidden="true">{{
                  sort?.key === col.key
                    ? sort.direction === "asc"
                      ? "▲"
                      : "▼"
                    : "↕"
                }}</span>
              </button>
              <template v-else>{{ col.label }}</template>
            </th>
          </tr>
        </thead>
        <tbody ref="tbody">
          <tr
            v-for="(row, index) in visibleRows"
            :key="String(row[rowKey])"
            :class="{ clickable: true }"
            :data-row="rowsActivatable ? '' : undefined"
            :tabindex="
              rowsActivatable ? (index === focusedIndex ? 0 : -1) : undefined
            "
            @click="emit('row-click', row)"
            @focus="focusedIndex = index"
            @keydown="rowsActivatable && onRowKeydown($event, row, index)"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              :class="{ numeric: col.numeric }"
            >
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ col.format ? col.format(row[col.key], row) : row[col.key] }}
              </slot>
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="columns.length" class="empty">
              {{ emptyText ?? "No rows" }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="paginated && total > 0" class="pager">
      <p class="range" aria-live="polite">
        Showing {{ firstShown }}–{{ lastShown }} of {{ total }}
      </p>
      <div class="pager-controls">
        <label class="rows-label" for="rows-per-page">Rows</label>
        <select id="rows-per-page" v-model.number="size" @change="goTo(1)">
          <option v-for="n in PAGE_SIZES" :key="n" :value="n">{{ n }}</option>
        </select>
        <button type="button" :disabled="page === 1" @click="goTo(page - 1)">
          Previous
        </button>
        <span class="page-count">Page {{ page }} of {{ pageCount }}</span>
        <button
          type="button"
          :disabled="page === pageCount"
          @click="goTo(page + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-wrap {
  overflow-x: auto;
}

/* A scroll region of its own so the sticky header and the pager stay in view. */
.table-wrap.scrollable {
  overflow: auto;
  max-height: min(60vh, 620px);
}

.data-table th,
.data-table td {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.data-table th {
  position: sticky;
  top: 0;
  z-index: 1;
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
  white-space: nowrap;
}

.data-table th.numeric,
.data-table td.numeric {
  text-align: right;
  font-variant-numeric: tabular-nums lining-nums;
}

.sort {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  color: inherit;
  text-transform: inherit;
  letter-spacing: inherit;
  cursor: pointer;
}

th.numeric .sort {
  flex-direction: row-reverse;
}

.sort:hover {
  color: var(--color-text);
}

.sort:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.sort-mark {
  color: var(--color-text-faint);
  font-size: 9px;
}

.data-table tbody tr.clickable:hover {
  background: var(--color-surface-muted);
  cursor: pointer;
}

.data-table tbody tr:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: -2px;
  background: var(--color-surface-muted);
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.empty {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--space-8) var(--space-4);
}

.pager {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: var(--text-sm);
}

.pager-controls {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.rows-label {
  margin: 0;
}

.pager-controls select {
  min-height: 30px;
  padding: 2px var(--space-2);
}

.pager-controls button {
  min-height: 30px;
  padding: 0 var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius);
  cursor: pointer;
}

.pager-controls button:hover:not(:disabled) {
  background: var(--color-surface-muted);
}

.pager-controls button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.pager-controls button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.page-count {
  white-space: nowrap;
}
</style>
