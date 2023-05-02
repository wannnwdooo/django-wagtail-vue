import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/blog',
      name: 'blog',
      component: () => import('../views/BlogPage.vue'),
      children: [
        {
          path: ':article',
          component: () => import('../components/views/blog/ArticlePage.vue'),
          props: true
        }
      ]
    }
  ]
})

export default router
