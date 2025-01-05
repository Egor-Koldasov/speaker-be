<script setup lang="ts">
// # Props, State
const props = defineProps<{
  placeholder?: string
  class?: string
  autofocus?: boolean
  maxlength?: number
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <textarea class="TextArea" rows="2" v-bind="props"></textarea>
</template>
<style scoped lang="scss">
@import '../../styles/_colors.scss';

.TextArea {
  resize: none;
  background-color: $inputBg1;
  border-color: transparent;
  &::placeholder {
    color: #ffffff50;
    font-style: italic;
  }
}
</style>
