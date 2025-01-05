<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <label class="LabelBox"><slot /></label>
</template>
<style scoped lang="scss">
.LabelBox {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  color: inherit;
}
</style>
