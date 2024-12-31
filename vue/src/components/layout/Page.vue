<script setup lang="ts">
import { effect, watch } from 'vue'
import { useLensQueryUser } from '../../planning/Lens/useLensQueryUser'
import { useRouter } from 'vue-router'
import { useSettingsPanel } from '../../uiStore/useSettingsPanel'
import SettingsPanel from './SettingsPanel/SettingsPanel.vue'
import PageHeader from './PageHeader.vue'

// # Props, State
const userLens = useLensQueryUser()
// # Hooks
const router = useRouter()
const settingsPanel = useSettingsPanel()

// # Computed
// # Callbacks
// # Watchers
effect(() => {
  console.log(
    'userLens.$state',
    userLens.$state.lastFetchedMainAt,
    userLens.$state.memData.user.id,
  )
  const authFailed =
    !!userLens.$state.lastFetchedMainAt && !userLens.$state.memData.user.id
  if (authFailed) {
    router.push('/')
  }
})
</script>
<template>
  <main class="Page" :class="{ settingsOpen: settingsPanel.open }">
    <div class="settings-layout">
      <div class="page-box">
        <PageHeader />
        <slot />
      </div>
      <SettingsPanel />
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
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
