import './assets/main.css'

import { createApp, type Ref } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import isoWeek from 'dayjs/plugin/isoWeek'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import dayjs from 'dayjs'
import { idbInit } from './idb/idb'
import { useRouter, type Router } from 'vue-router'

dayjs.extend(isoWeek)
dayjs.extend(duration)
dayjs.extend(relativeTime)
dayjs.extend(customParseFormat)

idbInit()

declare module 'pinia' {
  export interface PiniaCustomProperties {
    router: Router
  }
}

const app = createApp(App)

const pinia = createPinia()
pinia.use(() => {
  const router = useRouter()
  return {
    router,
  }
})
app.use(pinia)
app.use(router)

app.mount('#app')
