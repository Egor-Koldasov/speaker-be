import { uuidv7 } from '@kripod/uuidv7'
import { defineStore } from 'pinia'

export type Toast = {
  id: string
  message: string
}
export type ToastById = Record<string, Toast>

export const useToasts = defineStore('toasts', {
  state: () => ({
    toasts: {} as ToastById
  }),
  actions: {
    addToast(props: { message: string }) {
      const id = uuidv7()
      this.toasts[id] = { id, message: props.message }
      setTimeout(() => {
        delete this.toasts[id]
      }, 5000)
    }
  }
})
