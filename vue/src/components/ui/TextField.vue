<script setup lang="ts">
// # Props, State
const props = defineProps<{
  placeholder?: string
  type?: 'text' | 'email' | 'password'
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <input
    class="TextField"
    :type="props.type ?? 'text'"
    :placeholder="props.placeholder"
  />
</template>
<style scoped lang="scss">
@import '../../styles/_colors.scss';
.TextField.TextField.TextField.TextField {
  background-color: $inputBg1;
  border: none;
  &:-webkit-autofill {
    background-color: $inputBg1;
    -webkit-box-shadow: 0 0 0 50px $inputBg1AutoFill inset; /* Change the color to your own background color */
  }
}
</style>
