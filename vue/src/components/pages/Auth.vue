<script setup lang="ts">
import Page from '../layout/Page.vue'
import PageHeader from '../layout/PageHeader.vue'
import TextField from '../ui/TextField.vue'
import TextFieldGroup from '../ui/TextFieldGroup.vue'
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <Page>
    <PageHeader />
    <div class="Auth">
      <div class="title">Authorize</div>
      <form class="auth-form">
        <TextFieldGroup
          :field="{ type: 'email' }"
          type="email"
          label="Email"
          placeholder="Username"
        />
        <TextFieldGroup
          :field="{ type: 'password' }"
          type="password"
          label="Password"
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  </Page>
</template>
<style scoped lang="scss">
.Auth {
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
