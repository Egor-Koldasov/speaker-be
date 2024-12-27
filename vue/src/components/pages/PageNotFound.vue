<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div class="PageNotFound">
    <div>Page Not Found</div>
    <div><a role="button" href="/">Go home</a></div>
  </div>
</template>
<style scoped lang="scss">
.PageNotFound {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 2rem;

  a {
    min-width: 240px;
  }
}
</style>
