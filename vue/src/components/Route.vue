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
    <Transition>
      <slot :ref="slotRef" />
    </Transition>
  </div>
</template>
<style scoped lang="scss">
// # Route transitions
.route {
}
</style>
