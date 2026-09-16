import { defineStore } from 'pinia'
import { ref } from 'vue'

export type Theme = 'light' | 'dark'

export const useUiStore = defineStore('ui', () => {
  const theme = ref<Theme>(
    document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light',
  )
  const globalSearch = ref('')

  function setTheme(next: Theme) {
    theme.value = next
    if (next === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark')
    } else {
      document.documentElement.removeAttribute('data-theme')
    }
    localStorage.setItem('stockroom.theme', next)
  }

  return { theme, globalSearch, setTheme }
})
