import 'fake-indexeddb/auto'
import { vitest } from 'vitest'
import type { SwMessage } from '../../util/swChannel/isSwMessage'
import { uuidv7 } from '@kripod/uuidv7'

const mockSwListeners = {} as Record<string, (() => unknown)[]>

;(navigator.serviceWorker as any) = {
  ready: Promise.resolve({
    active: {
      postMessage: async (message: unknown) => {
        const messageReceiver = (await import('../../serviceWorker/messageReceiver'))
          .messageReceiver
        messageReceiver(message as SwMessage)
      },
      addEventListener: vitest.fn((name: string, listener: any) => {
        mockSwListeners[name] = listener
      }),
    },
    update: vitest.fn(),
    unregister: vitest.fn(),
  }),
  register: vitest.fn(() => import('../../serviceWorker/serviceWorker')),
}

vitest.mock('../../swClient/addUpdate.ts', async (getImp) => {
  const imp = (await getImp()) as any
  return {
    addUpdate: async (...args: any) => {
      imp.addUpdate(...args)
      return new Promise((resolve) => {
        setTimeout(resolve, 300)
      })
    },
  }
})
vitest.mock('../../swClient/requestSync.ts', async (getImp) => {
  const imp = (await getImp()) as any
  return {
    requestSync: async (...args: any) => {
      imp.requestSync(...args)
      return new Promise((resolve) => {
        setTimeout(resolve, 500)
      })
    },
  }
})
vitest.mock('../../swClient/authorize.ts', async (getImp) => {
  const imp = (await getImp()) as any
  return {
    authorize: async (...args: any) => {
      imp.authorize(...args)
      return new Promise((resolve) => {
        setTimeout(resolve, 500)
      })
    },
  }
})

type Listener = {
  id: string
  fn: (...args: any) => unknown
}
vitest.mock('../../util/swChannel/swChannel.ts', async () => {
  const listeners: Listener[] = []
  return {
    listenSwChannel: (cb: (...args: any) => unknown) => {
      listeners.push({ id: uuidv7(), fn: cb })
    },
    postFromSw: (...args: any) => {
      listeners.forEach((listener) => listener.fn(...args))
    },
  }
})

// afterAll(() => {
//   wsState.ws.close()
// })
