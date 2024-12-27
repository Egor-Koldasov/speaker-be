import { authTokenName } from './authTokenName'

export const getAuthToken = async (): Promise<string | null> => {
  const authToken = localStorage.getItem(authTokenName)
  if (!authToken || typeof authToken !== 'string') {
    return null
  }
  return authToken
}
