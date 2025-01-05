<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <button type="button" class="Button"><slot /></button>
</template>
<style scoped lang="scss">
.Button {
  &.secondary {
    background-color: #301637;
    color: inherit;
    &:hover {
      background-color: #3f1f4b;
    }
  }
  display: flex;
  align-items: center;
  border-color: transparent;
}
</style>
