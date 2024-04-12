<script setup lang="ts">
// # Props, State
const props = defineProps<{
  onClose: () => unknown
  title?: string
  class?: string
}>()
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <Teleport to="#ModalContainer">
    <div class="modal-root" :class="props.class">
      <div class="overlay" />
      <div class="modal">
        <div class="modal-header">
          <div class="close" @click="props.onClose">X</div>
          <div class="title">{{ props.title }}</div>
        </div>
        <div class="modal-content">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>
<style scoped lang="scss">
@import '../styles/colors';

.modal {
  min-width: 300px;
  /* border: 1px dotted $modalMoveNode; */
  border-radius: 8px;
  background-color: $mainBg;
  z-index: 2;
  box-shadow: 0 0 33px -23px #ffffff;
  pointer-events: auto;

  .modal-header {
    position: relative;
    color: #848261;
    display: flex;
    padding: 4px;
    background: linear-gradient(
      -90deg,
      rgb(13, 1, 17) 0%,
      rgb(0 47 57) 40%,
      rgb(0 63 8) 55%,
      rgb(124 116 0) 70%,
      rgb(202 72 10) 85%,
      rgb(233, 30, 99) 100%
    );
    border-radius: 12px;
    align-items: center;
    .title {
      position: absolute;
      left: 50%;
      transform: translate(-50%, 0);
      padding-left: 16px;
      font-size: 16px;
      font-weight: 600;
    }

    .close {
      padding: 4px;
      cursor: pointer;
      height: 16px;
      font-size: 12px;
      background-color: $inactive;
      border-radius: 50%;
      width: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
      &:hover {
        background-color: $primary;
      }
    }
  }
  .modal-content {
    padding: 8px;
  }
}
</style>
