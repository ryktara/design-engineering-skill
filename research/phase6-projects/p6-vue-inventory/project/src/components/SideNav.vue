<script setup lang="ts">
const links = [
  { to: '/', label: 'Dashboard', exact: true },
  { to: '/products', label: 'Products' },
  { to: '/adjustments', label: 'Stock adjustments' },
  { to: '/suppliers', label: 'Suppliers' },
  { to: '/settings', label: 'Settings' },
]
</script>

<template>
  <nav class="sidenav" aria-label="Main">
    <ul>
      <li v-for="link in links" :key="link.to">
        <RouterLink :to="link.to" :class="{ exact: link.exact }" active-class="active">
          {{ link.label }}
        </RouterLink>
      </li>
    </ul>
    <p class="version">v0.4.2 · Warehouse 2</p>
  </nav>
</template>

<style scoped>
.sidenav {
  width: var(--sidenav-width);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  padding: var(--space-3) 0;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

a {
  display: block;
  padding: var(--space-2) var(--space-4);
  color: var(--color-text);
  border-left: 3px solid transparent;
}

a:hover {
  background: var(--color-surface-muted);
  text-decoration: none;
}

a.active:not(.exact),
a.exact.router-link-exact-active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-left-color: var(--color-primary);
  font-weight: 500;
}

.version {
  margin-top: auto;
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-xs);
  color: var(--color-text-faint);
}
</style>
