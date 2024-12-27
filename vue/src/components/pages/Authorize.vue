<script setup lang="ts">
import { reactive } from 'vue'
import { useSignUpByEmail } from '../../planning/Action/useSignUpByEmail'
import PublicPage from '../layout/PublicPage.vue'
import TextFieldGroup from '../ui/TextFieldGroup.vue'
// # Props, State
const form = reactive({
  email: '',
})
// # Hooks
const signUpByEmail = useSignUpByEmail()
// # Computed
// # Callbacks
const onSubmit = async (e: Event) => {
  e.preventDefault()
  signUpByEmail.memActionParams = {
    email: form.email,
  }
  await signUpByEmail.requestMainDb()
}
// # Watchers
</script>
<template>
  <PublicPage>
    <div class="Authorize">
      <div class="title">Authorize {{ form.email }}</div>
      <form class="auth-form" @submit="onSubmit">
        <TextFieldGroup
          :field="{ type: 'email' }"
          type="email"
          label="Email"
          placeholder="Email"
          v-model="form.email"
        />
        <button
          type="submit"
          :aria-busy="!!signUpByEmail.$state.waitingMainDbId"
        >
          Login
        </button>
      </form>
    </div>
  </PublicPage>
</template>
<style scoped lang="scss">
.Authorize {
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
