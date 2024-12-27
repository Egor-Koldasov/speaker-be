<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useLensUser } from '../../planning/Lens/useLensUser'
import { computed } from 'vue'

// # Props, State
// # Hooks
const userLens = useLensUser()
// # Computed
const userEmail = computed(() => userLens.$state.memData.user.email)
// # Callbacks
// # Watchers
</script>
<template>
  <main class="Page">
    <div class="settings-layout">
      <div class="page-box">
        <div class="header">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink v-if="!userEmail" to="/authorize" class="auth-btn"
            >Login</RouterLink
          >
          <RouterLink v-if="!!userEmail" to="/home" class="auth-btn"
            >Continue as {{ userEmail }}</RouterLink
          >
        </div>
        <div class="content-gap"></div>
        <div class="content"><slot /></div>
      </div>
    </div>
  </main>
</template>
<style scoped lang="scss">
@import '../../styles/vars/_settings.scss';
.Page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  overflow: hidden;

  &.settingsOpen {
    .page-box {
      width: calc(100% - $panelWidth * 2);
    }
  }
}
.settings-layout {
  position: absolute;
  width: calc(100% + $panelWidth);
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.page-box {
  width: calc(100% - $panelWidth);
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.content {
  padding: 0 16px;
  width: 100%;
  height: 100%;
  align-items: center;
  display: flex;
  flex-direction: column;
}
.header {
  display: flex;
  justify-content: flex-start;
  padding: 8px;
  border-bottom: 1px solid #333;
  width: 100%;
}
.auth-btn {
  /* flex-grow: 1; */
  /* max-width: 360px; */
  margin-left: auto;
  display: inline-block;
}
.content-gap {
  display: flex;
  flex-shrink: 1;
  flex-grow: 0;
  height: 30%;
}
</style>
