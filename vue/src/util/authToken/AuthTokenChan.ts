import { EventEmitter } from 'stream'

export const AuthTokenChan = new EventEmitter()

AuthTokenChan.addListener('authToken', (event) => {
  console.log('AuthTokenChan', event)
})
