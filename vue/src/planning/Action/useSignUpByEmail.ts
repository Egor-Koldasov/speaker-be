import { ActionName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'
import { useRouter } from 'vue-router'

export const useSignUpByEmail = defineUseAction({
  name: ActionName.SignUpByEmail,
  initParams: {
    email: '',
  },
  onSuccess(response, store) {
    store.router.push('/confirm-auth-code')
  },
})
