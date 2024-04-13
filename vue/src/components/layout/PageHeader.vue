<script setup lang="ts">
import PageNavigation from './PageNavigation.vue'

// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <header class="PageHeader">
    <PageNavigation />
    <slot />
  </header>
</template>
<style scoped lang="scss">
.PageHeader {
  margin-bottom: auto;
  width: 100%;
  display: flex;
  padding: 0.5rem;
}
</style>
