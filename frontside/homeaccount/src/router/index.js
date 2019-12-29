import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from '@/components/HelloWorld'
import Input from '@/components/Input'
import List from '@/components/List'
import Graph from '@/components/Graph'
import Table from '@/components/Table'
import cognito from '@/cognito'
import Login from '@/components/Login'
import Signup from '@/components/Signup'
import Confirm from '@/components/Confirm'

import axios from 'axios'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/ja'
import 'element-ui/lib/theme-chalk/index.css'
// import 'element-ui/lib/theme-chalk/display.css'

import masterdata from '@/const/masterdata'
import myutils from '@/common/myutils'

Vue.use(Router, { locale })
Vue.use(ElementUI, { locale })

Vue.prototype.$axios = axios

Vue.prototype.apienv = {baseendpoint: process.env.API_ENDPOINT_BASE, key: process.env.API_KEY}
Vue.prototype.$masterdata = masterdata
Vue.prototype.$myutils = myutils

const requireAuth = (to, from, next) => {
  cognito.isAuthenticated()
    .then(function (session) {
      // console.log('isAuthenticated:' + session.getAccessToken().getJwtToken())
      next()
    })
    .catch(session => {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    })
}

const logout = (to, from, next) => {
  cognito.logout()
  next('/login')
}

console.log(process.env.NODE_ENV)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/input',
      name: 'Input',
      component: Input,
      beforeEnter: requireAuth
    },
    {
      path: '/list',
      name: 'List',
      component: List,
      beforeEnter: requireAuth
    },
    {
      path: '/graph',
      name: 'Graph',
      component: Graph,
      beforeEnter: requireAuth
    },
    {
      path: '/table',
      name: 'Table',
      component: Table
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/singup',
      name: 'Signup',
      component: Signup
    },
    {
      path: '/confirm',
      name: 'Confirm',
      component: Confirm
    },
    { path: '/logout',
      beforeEnter: logout
    }
  ]
})
