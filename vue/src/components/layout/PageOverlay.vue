<script setup lang="ts">
import { computed } from 'vue'
import { OverlayLvl } from '../../types/OverlayLvl'

// # Props, State
const props = defineProps<{ lvl?: OverlayLvl }>()
// # Hooks
// # Computed
const lvl = computed(() => props.lvl ?? OverlayLvl.Z100)
// # Callbacks
// # Watchers
</script>
<template>
  <div class="PageOverlay">
    <slot />
  </div>
</template>
<style scoped lang="scss">
.PageOverlay {
  position: fixed;
  inset: 0;
  z-index: v-bind('lvl');
  background-color: #10040dcc;
}
</style>
