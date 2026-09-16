import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: () => import('./views/DashboardView.vue') },
    { path: '/products', name: 'products', component: () => import('./views/ProductsView.vue') },
    {
      path: '/products/:sku',
      name: 'product-detail',
      component: () => import('./views/ProductDetailView.vue'),
      props: true,
    },
    {
      path: '/adjustments',
      name: 'adjustments',
      component: () => import('./views/StockAdjustmentView.vue'),
    },
    { path: '/suppliers', name: 'suppliers', component: () => import('./views/SuppliersView.vue') },
    { path: '/settings', name: 'settings', component: () => import('./views/SettingsView.vue') },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

router.afterEach((to) => {
  const titles: Record<string, string> = {
    dashboard: 'Dashboard',
    products: 'Products',
    'product-detail': 'Product',
    adjustments: 'Stock adjustments',
    suppliers: 'Suppliers',
    settings: 'Settings',
  }
  document.title = `${titles[String(to.name)] ?? 'StockRoom'} · StockRoom`
})

export default router
