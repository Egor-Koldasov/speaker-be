import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/define-from-foreign',
    },
    {
      path: '/define-from-foreign',
      name: 'define-from-foreign',
      component: () => import('../components/pages/DefineFromForeign.vue'),
    },
    {
      path: '/define-to-foreign',
      name: 'define-to-foreign',
      component: () => import('../components/pages/DefineToForeigh.vue'),
    },
  ],
})

export default router
