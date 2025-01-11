<script setup lang="ts">
import { useToasts } from '../../uiStore/useToasts'

const uisToasts = useToasts()
</script>
<template>
  <div class="toasts">
    <div
      class="toast"
      v-for="toast in uisToasts.toasts"
      :key="toast.id"
      role="status"
      :aria-label="toast.message"
    >
      {{ toast.message }}
    </div>
  </div>
</template>
<style scoped lang="scss">
@import '../../styles/colors';
.toasts {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  z-index: 2;
  gap: 4px;
  /* pointer-events: none; */
  padding: 0.2rem;
  .toast {
    background-color: $mainBg;
    border: 1px solid #4e0376;
    border-radius: 4px;
    padding: 4px 8px;
  }
}
</style>
