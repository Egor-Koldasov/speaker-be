import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/:pathMatch(.*)*',
      name: 'page-not-found',
      component: () => import('../components/pages/PageNotFound.vue'),
    },
  ],
})

export default router
