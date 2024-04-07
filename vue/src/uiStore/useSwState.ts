import { defineStore } from 'pinia'
import { listenSwChannel } from '../util/swChannel/swChannel'
import { SwMessageName } from '../util/swChannel/SwMessageName'
import type { SwState } from '../types/SwState'
import { useToasts } from './useToasts'
import { watchEffect } from 'vue'
import { swClient } from '../swClient/swClient'
import { postToSw } from '../swClient/postToSw'

const useSwState_ = defineStore('swState', {
  state: () => ({
    swState: null as SwState | null,
    swClientState: null as null | ServiceWorkerState,
  }),
  actions: {
    async init() {
      const sw = await swClient()
      this.swClientState = sw.state
      sw.addEventListener('statechange', (event) => {
        this.swClientState = (event.target as null | { state: ServiceWorkerState })?.state ?? null
      })
      listenSwChannel((message) => {
        if (message.name !== SwMessageName.swState) return
        this.swState = message.swState as SwState
      })
      postToSw({ name: SwMessageName.getSwState })
    },
  },
})

export const useSwState = () => {
  const uisWs = useSwState_()
  uisWs.init()
  const uisToasts = useToasts()
  watchEffect(() => {
    uisToasts.addToast({ message: `ws readyState: ${uisWs.swState?.readyState}` })
  })
  return uisWs
}
