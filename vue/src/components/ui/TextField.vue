<script setup lang="ts">
import { computed, effect, useTemplateRef } from 'vue'

// # Props, State
const props = defineProps<{
  placeholder?: string
  type?: 'text' | 'email' | 'password'
  class?: string
  autofocus?: boolean
  maxlength?: number
}>()
const model = defineModel()
const templateRef = useTemplateRef<HTMLInputElement>('TextField')

// # Hooks
// # Computed
const overflowing = computed(() => {
  if (!templateRef.value || !model.value) return
  const overflowing_ =
    templateRef.value.scrollWidth > templateRef.value.clientWidth
  return overflowing_
})
// # Callbacks
// # Watchers
</script>
<template>
  <input
    class="TextField"
    :class="[props.class, { overflowing: overflowing }]"
    :type="props.type ?? 'text'"
    :placeholder="props.placeholder"
    :autofocus="props.autofocus"
    :maxlength="props.maxlength"
    v-model="model"
    ref="TextField"
  />
</template>
<style scoped lang="scss">
@import '../../styles/_colors.scss';
.TextField.TextField.TextField.TextField {
  width: 10rem;
  margin: 0;
  padding: 0 0.3rem;
  height: auto;
  background-color: $inputBg1;
  border: none;
  position: relative;
  &:-webkit-autofill {
    background-color: $inputBg1;
    -webkit-box-shadow: 0 0 0 50px $inputBg1AutoFill inset; /* Change the color to your own background color */
  }
  &.overflowing {
    border-right: 3px solid #563741;
  }
}
</style>
