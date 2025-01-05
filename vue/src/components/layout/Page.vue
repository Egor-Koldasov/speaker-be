<script setup lang="ts">
import { Transition, effect, ref, watch } from 'vue'
import { useLensQueryUser } from '../../planning/Lens/useLensQueryUser'
import { useRouter } from 'vue-router'
import { useSettingsPanel } from '../../uiStore/useSettingsPanel'
import SettingsPanel from './SettingsPanel/SettingsPanel.vue'
import PageHeader from './PageHeader.vue'

// # Props, State
const userLens = useLensQueryUser()
const isMounted = ref(false)

// # Hooks
const router = useRouter()

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
  <Transition :duration="isMounted ? undefined : 10">
    <main class="Page">
      <div class="page-box">
        <PageHeader />
        <div class="page-content">
          <slot />
        </div>
      </div>
    </main>
  </Transition>
</template>
<style scoped lang="scss">
@import '../../styles/vars/_settings.scss';
.Page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.v-enter-active,
.v-leave-active {
  .page-content {
    transition: transform 0.2s ease;
  }
}

.v-enter-from,
.v-leave-to {
  .page-content {
    transform: translateX(100%);
  }
}
.page-box {
  width: calc(100%);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.page-content {
  width: 100%;
  height: 100%;
  padding: 0.5rem;
}
</style>
