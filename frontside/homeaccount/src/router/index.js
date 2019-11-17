import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from '@/components/HelloWorld'
import Input from '@/components/Input'
import List from '@/components/List'
import Graph from '@/components/Graph'

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
      component: Input
    },
    {
      path: '/list',
      name: 'List',
      component: List
    },
    {
      path: '/graph',
      name: 'Graph',
      component: Graph
    }
  ]
})
