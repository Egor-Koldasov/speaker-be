<script setup lang="ts">
import TextField from './TextField.vue'

// # Props, State
const props = defineProps<{
  field: InstanceType<typeof TextField>['$props']
  label: string
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div class="TextFieldGroup">
    <label>{{ props.label }}</label>
    <TextField v-bind="props.field" />
  </div>
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
