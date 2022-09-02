import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SlipInput from '@/views/SlipInput.vue'
import SlipList from '@/views/SlipList.vue'
import GraphView from '@/views/GraphView.vue'
import ToolsView from '@/views/ToolsView.vue'

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
    path: '/list',
    name: 'SlipList',
    component: SlipList,
  },
  {
    path: '/graph',
    name: 'GraphView',
    component: GraphView,
  },
  {
    path: '/tools',
    name: 'ToolsView',
    component: ToolsView,
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
