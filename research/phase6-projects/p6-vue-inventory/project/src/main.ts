import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import './styles/tokens.css'
import './styles/base.css'

const savedTheme = localStorage.getItem('stockroom.theme')
if (savedTheme === 'dark') {
  document.documentElement.setAttribute('data-theme', 'dark')
}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
