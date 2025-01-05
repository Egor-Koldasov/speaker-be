<script setup lang="ts">
// # Props, State
const props = defineProps<{
  value: string | number
  selected?: boolean
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <option class="Option" :value="props.value"><slot /></option>
</template>
<style scoped lang="scss">
.Option {
}
</style>
