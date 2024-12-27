<script setup lang="ts">
import { RouterLink } from 'vue-router'

// # Props, State
// const props = defineProps<{
//   pageName: string
// }>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <nav class="PageNavigation">
    <ol class="nav-list">
      <!-- <li class="nav-item">
        <RouterLink to="/define-from-foreign">Page 1</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/define-to-foreign">Page 2</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/decks">Page 3</RouterLink>
      </li> -->
    </ol>
  </nav>
</template>
<style scoped lang="scss">
.PageNavigation {
  .nav-list {
    display: flex;
    gap: 1rem;
    padding: 0 1rem;
    .nav-item {
      padding: 0;
    }
  }
}
</style>
