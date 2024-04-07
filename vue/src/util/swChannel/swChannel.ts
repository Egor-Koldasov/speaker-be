import { type SwMessage } from './isSwMessage'

const Bc = self ? self.BroadcastChannel : BroadcastChannel
const swChannel = new Bc('sw')

export const postFromSw = <T extends SwMessage>(message: T) => {
  console.log('postFromSw', message)
  swChannel.postMessage(message)
}

export const listenSwChannel = (callback: (message: SwMessage) => unknown) => {
  swChannel.addEventListener('message', (event) => {
    callback(event.data)
  })
}
