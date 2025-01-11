<script setup lang="ts">
// # Props, State
const props = defineProps<{
  value: string
  onChange: (value: string) => void
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <select
    class="Select"
    :value="props.value"
    @change="
      (e) => props.onChange((e.currentTarget as HTMLSelectElement).value)
    "
  >
    <slot />
  </select>
</template>
<style scoped lang="scss">
.Select {
  width: 10rem;
  background-color: #301637;
  border-color: transparent;
  padding-left: 0;
  padding-right: 1.4rem;
  background-position: center right 0.2rem;
  &:hover {
    background-color: #3f1f4b;
  }
}
</style>
