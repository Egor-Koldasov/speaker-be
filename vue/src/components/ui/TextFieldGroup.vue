<script setup lang="ts">
import TextField from './TextField.vue'

// # Props, State
const props = defineProps<{
  field: InstanceType<typeof TextField>['$props']
  label: string
}>()
const model = defineModel()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <label class="TextFieldGroup">
    <span>{{ props.label }}</span>
    <TextField v-bind="props.field" v-model="model" />
  </label>
</template>
<style scoped lang="scss">
.TextFieldGroup {
  display: flex;
  flex-direction: column;
  gap: 8px;

  label {
    font-size: 1rem;
  }
}
</style>
