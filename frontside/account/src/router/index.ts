import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SlipInput from '@/views/SlipInput.vue'

// const requireAuth = (to, from, next) => {
//   cognito.isAuthenticated()
//     .then(function (session) {
//       // console.log('isAuthenticated:' + myutils.getIdToken())
//       next()
//     })
//     .catch(session => {
//       next({
//         path: '/login',
//         query: { redirect: to.fullPath }
//       })
//     })
// }

// const logout = (to, from, next) => {
//   cognito.logout()
//   next('/login')
// }

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/input',
    name: 'SlipInput',
    component: SlipInput,
    // beforeEnter: requireAuth
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
