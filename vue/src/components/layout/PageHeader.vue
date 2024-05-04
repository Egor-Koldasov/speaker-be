<script setup lang="ts">
import { watch } from 'vue'
import PageNavigation from './PageNavigation.vue'
import { useMessageStore } from '../../dataStore/messageStore'
import { playAudioBase64 } from '../../util/playAudioBase64'
import { useToasts } from '../../uiStore/useToasts'

// # Props, State
// # Hooks
const dataStore = useMessageStore()
const toasts = useToasts()
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
  }
}
</style>
