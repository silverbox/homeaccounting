import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import RedirectView from '@/views/RedirectView.vue'
import SlipInput from '@/views/SlipInput.vue'
import SlipList from '@/views/SlipList.vue'
import GraphView from '@/views/GraphView.vue'
import ToolsView from '@/views/ToolsView.vue'

import { useAuthenticator } from "@aws-amplify/ui-vue";
import { Amplify } from 'aws-amplify';
import awsconfig from '@/aws-exports';
const auth = useAuthenticator();
Amplify.configure(awsconfig);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const requireAuth = (to: any, from: any, next: any) => {
  if (auth.route === 'authenticated') {
    next();
  } else {
    next({
      path: '/',
      query: { redirect: to.fullPath }
    })
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'redirect',
    component: RedirectView
  },
  {
    path: '/input',
    name: 'SlipInput',
    component: SlipInput,
    beforeEnter: requireAuth
  },
  {
    path: '/list',
    name: 'SlipList',
    component: SlipList,
    beforeEnter: requireAuth
  },
  {
    path: '/graph',
    name: 'GraphView',
    component: GraphView,
    beforeEnter: requireAuth
  },
  {
    path: '/tools',
    name: 'ToolsView',
    component: ToolsView,
    beforeEnter: requireAuth
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AboutView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router
