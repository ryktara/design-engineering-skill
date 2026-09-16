<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const router = useRouter()
const menuOpen = ref(false)

function submitSearch() {
  const q = ui.globalSearch.trim()
  if (!q) return
  router.push({ name: 'products', query: { q } })
}
</script>

<template>
  <header class="topbar">
    <RouterLink to="/" class="brand">
      <span class="brand-mark" aria-hidden="true"></span>
      StockRoom
    </RouterLink>

    <form class="search" @submit.prevent="submitSearch">
      <input
        v-model="ui.globalSearch"
        type="search"
        placeholder="Search SKU or product name"
        aria-label="Search products"
      />
    </form>

    <div class="user">
      <button type="button" class="user-button" @click="menuOpen = !menuOpen">
        <span class="avatar">MP</span>
        <span class="user-name">Meera Patel</span>
      </button>
      <div v-if="menuOpen" class="user-menu">
        <RouterLink to="/settings" @click="menuOpen = false">Settings</RouterLink>
        <button type="button" @click="menuOpen = false">Sign out</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  height: var(--topbar-height);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: var(--space-6);
  padding: 0 var(--space-4);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: 600;
  font-size: var(--text-lg);
  color: var(--color-text);
  width: calc(var(--sidenav-width) - var(--space-4));
}

.brand:hover {
  text-decoration: none;
}

.brand-mark {
  width: 22px;
  height: 22px;
  border-radius: var(--radius);
  background: var(--color-primary);
}

.search {
  flex: 1;
  max-width: 480px;
}

.search input {
  width: 100%;
}

.user {
  margin-left: auto;
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: none;
  border: 0;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius);
  cursor: pointer;
}

.user-button:hover {
  background: var(--color-surface-muted);
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: var(--text-xs);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.user-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  min-width: 160px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-popover);
  padding: var(--space-1) 0;
  z-index: 20;
}

.user-menu a,
.user-menu button {
  display: block;
  width: 100%;
  text-align: left;
  padding: var(--space-2) var(--space-3);
  background: none;
  border: 0;
  color: var(--color-text);
  cursor: pointer;
}

.user-menu a:hover,
.user-menu button:hover {
  background: var(--color-surface-muted);
  text-decoration: none;
}
</style>
