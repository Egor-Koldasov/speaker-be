import { ActionName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'

export const useSignUpByEmailCode = defineUseAction({
  name: ActionName.SignUpByEmailCode,
  initParams: {
    code: '',
  },
})
