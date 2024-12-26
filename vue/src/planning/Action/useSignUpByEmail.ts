import { ActionName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'

export const useSignUpByEmail = defineUseAction({
  name: ActionName.SignUpByEmail,
  initParams: {
    email: '',
  },
})
