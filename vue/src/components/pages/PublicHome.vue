<script setup lang="ts">
import { computed } from 'vue'
import { useLensUser } from '../../planning/Lens/useLensUser'
import PublicPage from '../layout/PublicPage.vue'

// # Props, State
// # Hooks
const userLens = useLensUser()
// # Computed
const userEmail = computed(() => userLens.$state.memData.user.email)
// # Callbacks
// # Watchers
</script>
<template>
  <PublicPage>
    <div class="PublicHome">
      <div class="content">
        <div>Welcome to early application</div>
      </div>
    </div>
  </PublicPage>
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
  flex-direction: column;
  align-items: center;
  font-size: 2rem;
  text-align: center;
}
</style>
