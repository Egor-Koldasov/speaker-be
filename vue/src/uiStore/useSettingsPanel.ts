import { defineStore } from 'pinia'

export const useSettingsPanel = defineStore('settingsPanel', {
  state: () => ({
    open: false,
  }),
  actions: {
    onSettingsClick() {
      this.open = !this.open
    },
  },
})
