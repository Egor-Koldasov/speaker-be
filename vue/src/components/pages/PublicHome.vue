<script setup lang="ts">
import { computed } from 'vue'
import { useLensUser } from '../../planning/Lens/useLensUser'

// # Props, State
// # Hooks
const userLens = useLensUser()
// # Computed
const userEmail = computed(() => userLens.$state.memData.user.email)
// # Callbacks
// # Watchers
</script>
<template>
  <div class="PublicHome">
    <div class="header">
      <a v-if="!userEmail" role="button" href="/authorize" class="auth-btn"
        >Authorize</a
      >
      <a v-if="!!userEmail" role="button" href="/home" class="auth-btn"
        >Continue as {{ userEmail }}</a
      >
    </div>
    <div class="content">
      <div>Welcome to early application</div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.PublicHome {
  width: 100%;
  height: 100%;
}
.content {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  text-align: center;
}
.header {
  display: flex;
  padding: 8px;
  border-bottom: 1px solid #333;
}
.auth-btn {
  flex-grow: 1;
  max-width: 360px;
  margin-left: auto;
}
</style>
