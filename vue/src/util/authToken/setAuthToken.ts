import { AuthTokenChan } from './AuthTokenChan'
import { authTokenName } from './authTokenName'

export const setAuthToken = async (token: string) => {
  localStorage.setItem(authTokenName, token)
  AuthTokenChan.emit('authToken', token)
}
