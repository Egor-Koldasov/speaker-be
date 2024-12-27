<script setup lang="ts">
import { useSettingsPanel } from '../../uiStore/useSettingsPanel'
import { useToasts } from '../../uiStore/useToasts'
import PageNavigation from './PageNavigation.vue'

// # Props, State
// # Hooks
const toasts = useToasts()
const settingsPanel = useSettingsPanel()
// # Computed
// # Callbacks
// const onSpeak = () => {
//   const text = window.getSelection()?.toString()
//   if (!text) {
//     toasts.addToast({
//       message: 'Select the text before pressing the button',
//     })
//     return
//   }
//   dataStore.sendMessage({
//     name: 'textToSpeech',
//     data: { text },
//   })
// }
// # Watchers
// watch(
//   () => dataStore.textToSpeech.data?.audio,
//   () => {
//     if (dataStore.textToSpeech.data?.audio) {
//       playAudioBase64(dataStore.textToSpeech.data?.audio)
//     }
//   },
// )
</script>
<template>
  <header class="PageHeader">
    <PageNavigation />
    <div class="button-bar">
      <!-- <button @click="onSpeak" :disabled="dataStore.textToSpeech.loading">
        Speak text
      </button> -->
      <slot />
      <button class="settings-button" @click="settingsPanel.onSettingsClick">
        <img
          src="@/assets/icons/Settings.png"
          alt="Settings"
          class="settings-img"
        />
      </button>
    </div>
  </header>
</template>
<style scoped lang="scss">
.PageHeader {
  margin-bottom: auto;
  width: 100%;
  display: flex;
  align-items: center;

  padding: 0.5rem;
  .button-bar {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
}
.settings-button {
  padding: 0;
  background-color: #433448;
  &:hover {
    .settings-img {
      transform: rotate(720deg);
    }
  }
}
.settings-img {
  width: 2rem;
  height: 2rem;
  transition: transform 0.1s;
}
</style>
