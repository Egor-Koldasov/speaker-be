<script setup lang="ts">
import { useLensUser } from '../../../planning/Lens/useLensUser'
import { useSettingsPanel } from '../../../uiStore/useSettingsPanel'

// # Props, State
// # Hooks
const settingsPanel = useSettingsPanel()
const userLens = useLensUser()

// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div class="SettingsPanel" :class="{ open: settingsPanel.open }">
    <h2>Settings</h2>
    {{ userLens.memData.user.email }}
  </div>
</template>
<style scoped lang="scss">
@import '../../../styles/_colors.scss';
@import '../../../styles/vars/_settings.scss';

.SettingsPanel {
  /* background-color: #110f01; */
  width: $panelWidth;
  height: 100%;
  transition: width padding 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  padding: 1rem;
  border-left: 1px solid $mainBgSub200;

  /* justify-content: center; */

  /* &.open {
    transform: translate();
  } */
}
</style>
