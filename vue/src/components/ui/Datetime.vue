<script setup lang="ts">
import dayjs from 'dayjs'
import { reactive, watchEffect } from 'vue'
const props = defineProps<{
  onChange: (time: Date) => unknown
  value: Date
}>()

// # Props, State
const state = reactive({
  date: '',
  time: '',
})
// # Hooks
// # Computed
watchEffect(() => {
  if (!state.date || !state.time) return
  const date = dayjs(`${state.date}T${state.time}`).toDate()
  props.onChange(date)
})
watchEffect(() => {
  const date = dayjs(props.value)
  state.date = date.format('YYYY-MM-DD')
  state.time = date.format('HH:mm')
})
</script>
<template>
  <div class="datetime">
    <input type="date" v-model="state.date" class="date" />
    <input type="time" v-model="state.time" class="time" />
  </div>
</template>
<style scoped lang="scss">
.datetime {
  display: flex;
  gap: 4px;
  width: auto;
  input {
    padding: 4px;
    height: auto;
    width: auto;
  }
  .date {
    width: 125px;
  }
  .time {
    width: 82px;
  }
}
</style>
