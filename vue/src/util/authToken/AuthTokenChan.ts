import EventEmitter from 'eventemitter3'

export const AuthTokenChan = new EventEmitter()

AuthTokenChan.addListener('authToken', (event) => {
  console.log('AuthTokenChan', event)
})
