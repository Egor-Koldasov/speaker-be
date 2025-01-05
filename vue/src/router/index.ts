import { createRouter, createWebHistory, type RouterOptions } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'public-home',
    component: () => import('../components/pages/PublicHome.vue'),
  },
  {
    path: '/home',
    name: 'app-home',
    component: () => import('../components/pages/AppHome.vue'),
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('../components/pages/User.vue'),
  },
  {
    path: '/authorize',
    name: 'authorize',
    component: () => import('../components/pages/Authorize.vue'),
  },
  {
    path: '/confirm-auth-code',
    name: 'confirm-auth-code',
    component: () => import('../components/pages/ConfirmAuthCode.vue'),
  },
  {
    path: '/card-builder',
    name: 'card-builder',
    component: () => import('../components/pages/CardCreator.vue'),
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../components/pages/Settings.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'page-not-found',
    component: () => import('../components/pages/PageNotFound.vue'),
  },
] as const satisfies RouterOptions['routes']

type Routes = typeof routes
export type RouteName = Routes[number]['name']

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
