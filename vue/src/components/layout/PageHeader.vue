<script setup lang="ts">
import PageNavigation from './PageNavigation.vue'

// # Props, State
// # Hooks
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
    <!-- <button @click="onSpeak" :disabled="dataStore.textToSpeech.loading">
        Speak text
      </button> -->
    <slot />
  </header>
</template>
<style scoped lang="scss">
@import '../../styles/colors';

.PageHeader {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid #ffffff18;
  background-color: $mainBg;
  position: relative;
  z-index: 1;
}
</style>
