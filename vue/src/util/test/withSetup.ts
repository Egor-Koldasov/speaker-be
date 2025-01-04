import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { type Router } from 'vue-router'

export function withSetup<T>(composable: () => T) {
  let result: T | null = null
  const app = createApp({
    setup() {
      result = composable()
      // suppress missing template warning
      return () => {}
    },
  })
  const pinia = createPinia()
  pinia.use(() => {
    const mockRouter = {} as Router
    mockRouter.push = (() => {}) as any
    return {
      router: mockRouter,
    }
  })
  app.use(pinia)
  app.mount(document.createElement('div'))
  if (!result) {
    throw new Error('The setup function must return the composable')
  }
  // return the result and the app instance
  // for testing provide/unmount
  return { result: result as T, app }
}
