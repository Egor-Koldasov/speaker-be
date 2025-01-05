<script setup lang="ts">
// # Props, State
const props = defineProps<{
  alwaysWrap?: boolean
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <label class="LabelBox" :class="{ alwaysWrap }"><slot /></label>
</template>
<style scoped lang="scss">
.LabelBox {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  color: inherit;
  &.alwaysWrap {
    :deep(.LabelText),
    input {
      width: 100%;
    }
  }
}
</style>
