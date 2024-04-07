<script setup lang="ts">
import { reactive } from 'vue'

export type PopupMenuOption = {
  label: string
  value?: string
  onClick: () => unknown
}

// # Props, State
const props = defineProps<{
  options: PopupMenuOption[]
}>()
const state = reactive({
  open: false,
})
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div class="PopupMenu" @click="state.open = !state.open">
    <slot />
    <div class="menu-box" v-if="state.open">
      <div
        class="option"
        v-for="option in props.options"
        :key="option.value"
        @click="option.onClick"
      >
        {{ option.label }}
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
@import '../../styles/colors';
.PopupMenu {
  position: relative;
  display: inline-flex;
  height: auto;
  .menu-box {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translate(-50%, 4px);
    background-color: $mainBg;
    /* box-shadow: 0 0 16px -10px #ffffff; */
    min-width: 180px;
    display: flex;
    flex-direction: column;
    padding: 8px 4px;
    border-radius: 8px;
    border: 1px solid $inactive;
    z-index: 2;

    .option {
      padding: 0 8px;
      background-color: $inactive;
      border-radius: 8px;
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      font-size: 14px;

      &:hover {
        background-color: $primary;
      }
    }
  }
}
</style>
