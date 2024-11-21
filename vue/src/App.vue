<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import Toasts from './components/Toasts/Toasts.vue'
import Route from './components/Route.vue'
import ModalContainer from './components/ModalContainer.vue'

onMounted(() => {
  document.documentElement.setAttribute('data-theme', 'dark')
})
</script>

<template>
  <Toasts />
  <RouterView v-slot="{ Component, route }">
    <Route :route="route" :component="Component">
      <component :is="Component" />
    </Route>
  </RouterView>
  <ModalContainer />
</template>

<style scoped></style>

<style lang="scss">
@import './styles/global.scss';

pre {
  background-color: transparent;
  color: inherit;
  font-style: monospace;
}
html {
  font-size: 16px;
}
body {
  background-color: $mainBg;
  color: $textForDark;
  height: 100svh;
  opacity: 0;
  transform: scale(0.94);
  &.ready {
    opacity: 1;
    transform: scale(1);
    transition: 1s;

    * {
      transition: 0.4s;
    }
  }
}
* {
  gap: 4px;
}
#app {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.route {
  height: calc(100% - 24px);
  position: relative;
  overflow: hidden;
  & > * {
    position: absolute;
    inset: 0;
  }
}

// # Components
button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto;
  padding: 0 8px;
  &.small {
    padding: 0 4px;
    width: auto;
    @include font-s;
  }
}
article {
  margin: 0;
  padding: 8px;
}

h2 {
  color: inherit;
}
</style>
