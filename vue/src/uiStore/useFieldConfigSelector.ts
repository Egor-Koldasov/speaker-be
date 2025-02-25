import { defineStore } from 'pinia'

export const useFieldConfigSelector = defineStore('fieldConfigSelector', {
  state() {
    return {
      selectedFieldConfigId: '',
    }
  },
})
