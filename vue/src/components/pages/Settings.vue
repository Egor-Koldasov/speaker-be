<script setup lang="ts">
import { useLensQueryUser } from '../../planning/Lens/useLensQueryUser'
import Page from '../layout/Page.vue'

// # Props, State
// # Hooks
const userLens = useLensQueryUser()

// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <Page>
    <div class="Settings">
      <h2>Settings</h2>
      {{ userLens.memData.user.email }}
    </div>
  </Page>
</template>
<style scoped lang="scss">
@import '../../styles/_colors.scss';
@import '../../styles/vars/_settings.scss';

.Settings {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  padding: 1rem;
}
</style>
