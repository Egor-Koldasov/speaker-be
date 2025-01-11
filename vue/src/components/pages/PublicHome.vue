<script setup lang="ts">
import { computed } from 'vue'
import { useLensQueryUser } from '../../planning/Lens/useLensQueryUser'
import PublicPage from '../layout/PublicPage.vue'

// # Props, State
// # Hooks
const userLens = useLensQueryUser()
// # Computed
const userEmail = computed(() => userLens.$state.memData.user.email)
// # Callbacks
// # Watchers
</script>
<template>
  <PublicPage>
    <div class="PublicHome">
      <div class="content">
        <h1 class="header">Nexa Memoria</h1>
        <div>
          <a target="_blank" href="https://google.com?q=Spaced+repetition"
            >Spaced repetition</a
          >
          tool to remember things forever
        </div>
        <div class="early-welcome">Welcome to early application</div>
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
  text-align: center;
  h1 {
    font-size: 2rem;
  }
  div {
    font-size: 1.5rem;
  }
}
.early-welcome.early-welcome {
  /* font-size: 1.2rem; */
  /* color: #ffffff50; */
}
</style>
