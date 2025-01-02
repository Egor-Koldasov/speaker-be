import { createPinia } from 'pinia'
import { createApp } from 'vue'

export function withSetup<T>(composable: () => T) {
  let result: T | null = null
  const app = createApp({
    setup() {
      result = composable()
      // suppress missing template warning
      return () => {}
    },
  })
  app.use(createPinia())
  app.mount(document.createElement('div'))
  if (!result) {
    throw new Error('The setup function must return the composable')
  }
  // return the result and the app instance
  // for testing provide/unmount
  return { result: result as T, app }
}
