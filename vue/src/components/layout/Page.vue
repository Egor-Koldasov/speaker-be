<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <main class="Page">
    <slot />
  </main>
</template>
<style scoped lang="scss">
.Page {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
