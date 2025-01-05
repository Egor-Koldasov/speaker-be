import { defineStore } from 'pinia'

export const useCardConfigSelector = defineStore('cardConfigSelector', {
  state() {
    return {
      selectedCardConfigId: '',
    }
  },
})
