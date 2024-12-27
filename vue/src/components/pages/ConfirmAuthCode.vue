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
          :field="{
            type: 'text',
            class: 'auth-code-field',
            autofocus: true,
            maxlength: 6,
          }"
          label="Enter authentication code"
          v-model="form.authCode"
        />
        <button
          type="submit"
          :aria-busy="!!signUpByEmailCode.$state.waitingMainDbId"
          :disabled="form.authCode.length !== 6"
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
  /* justify-content: center; */
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
    align-items: center;
    gap: 8px;
    width: 100%;
  }
  :deep(.TextFieldGroup) {
    width: 100%;
  }
  :deep(.auth-code-field) {
    font-size: 2rem;
    letter-spacing: 1rem;
    text-transform: uppercase;
    text-align: center;
  }
}
</style>
