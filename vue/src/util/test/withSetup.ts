import { createPinia } from 'pinia'
import { createApp } from 'vue'

export function withSetup<T>(composable: () => T) {
  let result: T
  const app = createApp({
    setup() {
      result = composable()
      // suppress missing template warning
      return () => {}
    },
  })
  app.use(createPinia())
  app.mount(document.createElement('div'))
  // return the result and the app instance
  // for testing provide/unmount
  return [result, app] as [T, typeof app]
}
