<script lang="ts" generics="Row extends { id: string }">
  import type { Snippet } from 'svelte';

  export type Column<R> = {
    key: string;
    label: string;
    align?: 'left' | 'right';
    width?: string;
    render?: (row: R) => string;
  };

  let {
    columns,
    rows,
    onRowClick,
    cell,
    footer,
    empty = 'No records.'
  }: {
    columns: Column<Row>[];
    rows: Row[];
    onRowClick?: (row: Row) => void;
    cell?: Snippet<[Row, Column<Row>]>;
    footer?: Snippet<[Column<Row>[]]>;
    empty?: string;
  } = $props();

  function value(row: Row, col: Column<Row>) {
    if (col.render) return col.render(row);
    const v = (row as Record<string, unknown>)[col.key];
    return v == null ? '' : String(v);
  }
</script>

<div class="overflow-x-auto">
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr class="bg-neutral-50 border-b border-neutral-200">
        {#each columns as col (col.key)}
          <th
            scope="col"
            class="px-4 h-10 text-xs font-semibold uppercase tracking-wide text-neutral-500 whitespace-nowrap {col.align === 'right' ? 'text-right' : 'text-left'}"
            style={col.width ? `width:${col.width}` : undefined}
          >
            {col.label}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each rows as row (row.id)}
        <tr
          class="border-b border-neutral-200 last:border-b-0 {onRowClick ? 'cursor-pointer hover:bg-primary-50 focus-within:bg-primary-50' : ''}"
          onclick={() => onRowClick?.(row)}
          onkeydown={(e) => {
            if (onRowClick && (e.key === 'Enter' || e.key === ' ')) {
              e.preventDefault();
              onRowClick(row);
            }
          }}
          tabindex={onRowClick ? 0 : undefined}
          role={onRowClick ? 'button' : undefined}
        >
          {#each columns as col (col.key)}
            <td class="px-4 h-11 text-neutral-800 whitespace-nowrap {col.align === 'right' ? 'text-right tabular-nums' : 'text-left'}">
              {#if cell}
                {@render cell(row, col)}
              {:else}
                {value(row, col)}
              {/if}
            </td>
          {/each}
        </tr>
      {:else}
        <tr>
          <td colspan={columns.length} class="px-4 py-8 text-center text-neutral-500">{empty}</td>
        </tr>
      {/each}
    </tbody>
    {#if footer && rows.length}
      <tfoot class="border-t border-neutral-300 bg-neutral-50">
        {@render footer(columns)}
      </tfoot>
    {/if}
  </table>
</div>
