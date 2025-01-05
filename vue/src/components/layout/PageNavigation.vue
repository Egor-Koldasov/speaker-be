<script setup lang="ts">
import { computed, reactive } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageOverlay from './PageOverlay.vue'
import { OverlayLvl } from '../../types/OverlayLvl'
import type { RouteName } from '../../router'

// # Props, State
// const props = defineProps<{
//   pageName: string
// }>()
const state = reactive({
  navOpen: false,
})
const settingsZIndex = OverlayLvl.Z100
// # Hooks
const route = useRoute()
const routeName: RouteName = route.name as RouteName
// # Computed
type NavItemConfig = {
  activeRoutes: RouteName[]
  to: string
  textShown: string
}
const navConfig = computed((): NavItemConfig[] => [
  {
    activeRoutes: ['app-home'],
    to: '/home',
    textShown: 'Home',
  },
  {
    activeRoutes: ['card-builder'],
    to: '/card-builder',
    textShown: 'Card creator',
  },
  {
    activeRoutes: ['settings'],
    to: '/settings',
    textShown: 'Settings',
  },
])
const navItemConfigActive = computed(() => {
  return navConfig.value.find((itemConfig) =>
    itemConfig.activeRoutes.includes(routeName),
  )
})

// # Callbacks
// # Watchers
</script>
<template>
  <PageOverlay v-if="state.navOpen">
    <div class="title">Where do you want to go?</div>
    <div class="top-gap"></div>
    <nav class="PageNavigation">
      <ol class="nav-list">
        <li
          class="nav-item"
          :class="{ active: navItemConfigActive?.to === itemConfig.to }"
          v-for="itemConfig in navConfig"
          :key="itemConfig.to"
          @click="state.navOpen = false"
        >
          <RouterLink :to="itemConfig.to">{{
            itemConfig.textShown
          }}</RouterLink>
        </li>
        <!-- 
      <li class="nav-item">
        <RouterLink to="/define-to-foreign">Page 2</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/decks">Page 3</RouterLink>
      </li> -->
      </ol>
    </nav>
  </PageOverlay>
  <div class="page-name" v-if="navItemConfigActive">
    {{ navItemConfigActive.textShown }}
  </div>
  <button
    class="settings-button"
    :class="{ open: state.navOpen }"
    @click="state.navOpen = !state.navOpen"
  >
    <!-- <img
      src="@/assets/icons/Settings.png"
      alt="Page Navigation"
      class="settings-img"
    /> -->
    <!-- menu-icon.svg -->
    <svg
      alt="Page Navigation"
      class="settings-img"
      xmlns="http://www.w3.org/2000/svg"
      id="Outline"
      viewBox="0 0 24 24"
      width="512"
      height="512"
    >
      <path d="M7,6H23a1,1,0,0,0,0-2H7A1,1,0,0,0,7,6Z" />
      <path d="M23,11H7a1,1,0,0,0,0,2H23a1,1,0,0,0,0-2Z" />
      <path d="M23,18H7a1,1,0,0,0,0,2H23a1,1,0,0,0,0-2Z" />
      <circle cx="2" cy="5" r="2" />
      <circle cx="2" cy="12" r="2" />
      <circle cx="2" cy="19" r="2" />
    </svg>
  </button>
</template>
<style scoped lang="scss">
.title {
  padding-left: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.top-gap {
  flex-shrink: 1;
  flex-grow: 0;
  width: 100%;
  height: 3rem;
}
.PageNavigation {
  width: 100%;
  display: flex;
  justify-content: center;
  .nav-list {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-top: 3rem;
    gap: 1rem;
    font-size: 1.5rem;
    width: 100%;
    .nav-item {
      padding: 0.5rem 1rem;
      width: 100%;
      &.active {
        font-weight: bold;
        background-color: #29072c;
      }
    }
  }
}
.settings-button {
  padding: 0;
  background-color: transparent;
  position: relative;
  z-index: v-bind('settingsZIndex');
  margin-left: auto;
  &.open {
    .settings-img {
      path,
      circle {
        fill: #d2c1d4;
      }
    }
  }
  &:hover {
    .settings-img {
      /* transform: rotate(720deg); */
    }
  }
}
.settings-img {
  width: 1.5rem;
  height: 1.5rem;
  /* transition: transform 0.1s; */

  path,
  circle {
    fill: #ffffff33;
  }
}
</style>
