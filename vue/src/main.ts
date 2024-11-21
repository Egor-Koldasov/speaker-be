import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import isoWeek from 'dayjs/plugin/isoWeek'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import dayjs from 'dayjs'
import { idbInit } from './idb/idb'

dayjs.extend(isoWeek)
dayjs.extend(duration)
dayjs.extend(relativeTime)
dayjs.extend(customParseFormat)

idbInit()

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
