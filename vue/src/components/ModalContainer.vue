<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div id="ModalContainer"></div>
</template>
<style scoped lang="scss">
#ModalContainer {
  position: fixed;
  top: 0;
  left: 0;
  padding: 8px;
  width: 100vw;
  height: 100vh;
  z-index: 2;
  display: flex;
  align-items: flex-end;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
  overflow: hidden;
  flex-wrap: wrap;

  &:empty {
    padding: 0;
  }
}
</style>
