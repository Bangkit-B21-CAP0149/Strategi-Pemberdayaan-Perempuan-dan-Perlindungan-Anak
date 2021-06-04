import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior() {
    return { x: 0, y: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
      meta: {
        pageTitle: 'Home',
        breadcrumb: [
          {
            text: 'Home',
            active: true,
          },
        ],
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/dashboard/Analytics.vue'),
    },
    {
      path: '/mentions',
      name: 'mentions',
      component: () => import('@/views/mentions/Mentions.vue'),
      meta: {
        pageTitle: 'Mentions',
        breadcrumb: [
          {
            text: 'Mentions',
            active: true,
          },
        ],
      },
    },
    {
      path: '/vr_report',
      name: 'vr_report',
      component: () => import('@/views/VR/Report.vue'),
      meta: {
        pageTitle: 'Violence Report',
        breadcrumb: [
          {
            text: 'Violence Report',
            active: true,
          },
        ],
      },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: {
        layout: 'full',
      },
    },
    {
      path: '/error-404',
      name: 'error-404',
      component: () => import('@/views/error/Error404.vue'),
      meta: {
        layout: 'full',
      },
    },
    {
      path: '*',
      redirect: 'error-404',
    },
  ],
})

export default router
