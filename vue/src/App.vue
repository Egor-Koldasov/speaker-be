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
  overflow: hidden;
}
body {
  height: calc(100svh);
  background-color: $mainBg;
  position: relative;

  #static-loading {
    border: 16px solid #544659;
    position: absolute;
    inset: 0;
    animation: border-pulse 0.8s infinite alternate ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #544659;
    font-size: 2rem;
    #static-loading-graphic {
      border: 8px solid #544659;
      width: 64px;
      height: 64px;
      animation: square-circle-pulse 0.4s infinite alternate ease-in-out;
    }
  }

  #app {
    background-color: $mainBg;
    color: $textForDark;
    height: 100%;
    opacity: 0;
    /* transform: scale(0.1); */
  }
  &.ready {
    #app {
      opacity: 1;
      /* transform: scale(1); */
      transition: 0.2s ease;
    }
    * {
      transition: 0.2s ease;
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
  height: calc(100%);
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

@keyframes border-pulse {
  0% {
    border-color: #544659aa;
  }
  100% {
    border-color: #544659;
  }
}
@keyframes square-circle-pulse {
  0% {
    border-radius: 0;
    border-color: #544659aa;
  }
  100% {
    border-radius: 50%;
    border-color: #544659;
  }
}
</style>
