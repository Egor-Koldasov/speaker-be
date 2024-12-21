<script setup lang="ts">
import { onMounted, ref, type VNode } from 'vue'
import type { RouteLocationNormalizedLoaded } from 'vue-router'
import { timeout } from '../util/timeout'

// # Props, State
const props = defineProps<{
  route: RouteLocationNormalizedLoaded
  component: VNode
}>()
const isMounted = ref(false)

const slotRef = ref<HTMLElement | null>(null)
// # Hooks
// # Computed
onMounted(async () => {
  await timeout(500).promise
  requestAnimationFrame(() => {
    document.body.classList.add('ready')
  })
})
</script>
<template>
  <div class="route">
    <Transition :duration="isMounted ? undefined : 1">
      <slot :ref="slotRef" />
    </Transition>
  </div>
</template>
<style scoped lang="scss">
// # Route transitions
.route {
  & > * {
    transition: all 0.4s;
    /* &.v-enter-active.v-enter-active,
    &.v-leave-active.v-leave-active {
      transition: all 0.4s ease;
    } */

    &.v-leave-to.v-leave-to {
      opacity: 0;
      transform: translate(0, 100%);
    }
    &.v-enter-from.v-enter-from {
      opacity: 0;
      transform: translate(0, -100%);
    }
    &.v-enter-to.v-enter-to {
      opacity: 1;
      transform: translate(0, 0);
    }
  }
}
</style>
