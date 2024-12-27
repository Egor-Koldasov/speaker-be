<script setup lang="ts">
import { reactive } from 'vue'
import { useSignUpByEmailCode } from '../../planning/Action/useSignUpByEmailCode'
import PublicPage from '../layout/PublicPage.vue'
import TextField from '../ui/TextField.vue'
import TextFieldGroup from '../ui/TextFieldGroup.vue'
// # Props, State
const form = reactive({
  authCode: '',
})
// # Hooks
const signUpByEmailCode = useSignUpByEmailCode()
// # Computed
// # Callbacks
const onSubmit = async (e: Event) => {
  e.preventDefault()
  signUpByEmailCode.memActionParams = {
    code: form.authCode,
  }
  await signUpByEmailCode.requestMainDb()
}
// # Watchers
</script>
<template>
  <PublicPage>
    <div class="ConfirmAuthCode">
      <form class="auth-form" @submit="onSubmit">
        <TextFieldGroup
          :field="{ type: 'text' }"
          label="Enter authentication code"
          v-model="form.authCode"
        />
        <button
          type="submit"
          :aria-busy="!!signUpByEmailCode.$state.waitingMainDbId"
        >
          Confirm
        </button>
      </form>
    </div>
  </PublicPage>
</template>
<style scoped lang="scss">
.ConfirmAuthCode {
  height: 1px;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 500px;

  .title {
    font-size: 2rem;
  }

  .auth-form {
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }
}
</style>
