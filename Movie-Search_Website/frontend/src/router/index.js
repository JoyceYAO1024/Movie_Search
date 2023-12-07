import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: () => import('@/views/home/index.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/user/login/index.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/user/register/index.vue')
    },
    {
      path: '/search',
      name: 'Search',
      component: () => import('@/views/search/index.vue')
    },
    {
      path: '/search-detail',
      name: 'SearchDetail',
      component: () => import('@/views/search-detail/index.vue')
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: () => import('@/views/profile/index.vue')
    },
    {
      path: '/user',
      name: 'UserCenter',
      component: () => import('@/views/user/index.vue')
    }

  ]
})
