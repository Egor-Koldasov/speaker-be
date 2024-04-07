<script setup lang="ts">
import { useToasts } from '../../uiStore/useToasts'

const uisToasts = useToasts()
</script>
<template>
  <div class="toasts">
    <div class="toast" v-for="toast in uisToasts.toasts" :key="toast.id">
      {{ toast.message }}
    </div>
  </div>
</template>
<style scoped lang="scss">
@import '../../styles/colors';
.toasts {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  z-index: 2;
  gap: 4px;
  pointer-events: none;
  .toast {
    background-color: $mainBg;
    border: 1px solid #4e0376;
    border-radius: 4px;
    padding: 4px 8px;
  }
}
</style>
