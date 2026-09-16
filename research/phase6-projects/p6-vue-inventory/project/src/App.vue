<script setup lang="ts">
import TopBar from '@/components/TopBar.vue'
import SideNav from '@/components/SideNav.vue'
</script>

<template>
  <div class="shell">
    <TopBar />
    <div class="shell-body">
      <SideNav />
      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.shell {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.shell-body {
  display: flex;
  flex: 1;
  min-height: 0;
}

.content {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  padding: var(--space-6);
}
</style>
