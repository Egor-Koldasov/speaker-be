import { ActionName } from 'speaker-json-schema'
import { defineUseAction } from '../DefineUseAction'
import { setAuthToken } from '../../util/authToken/setAuthToken'

export const useSignUpByEmailCode = defineUseAction({
  name: ActionName.SignUpByEmailCode,
  initParams: {
    code: '',
  },
  async onSuccess(response, store) {
    await setAuthToken(response.data.actionParams.sessionToken)
    store.router.push('/home')
  },
})
