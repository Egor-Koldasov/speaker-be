<script setup lang="ts">
// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <main class="Page">
    <div class="settings-layout">
      <div class="page-box">
        <slot />
      </div>
    </div>
  </main>
</template>
<style scoped lang="scss">
@import '../../styles/vars/_settings.scss';
.Page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  overflow: hidden;

  &.settingsOpen {
    .page-box {
      width: calc(100% - $panelWidth * 2);
    }
  }
}
.settings-layout {
  position: absolute;
  width: calc(100% + $panelWidth);
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.page-box {
  width: calc(100% - $panelWidth);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 16px;
}
</style>
