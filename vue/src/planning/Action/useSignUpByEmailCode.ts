import { ActionName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'
import { setAuthToken } from '../../util/authToken/setAuthToken'

export const useSignUpByEmailCode = defineUseAction({
  name: ActionName.SignUpByEmailCode,
  initParams: {
    code: '',
  },
  onSuccess(response) {
    setAuthToken(response.data.actionParams.sessionToken)
  },
})
