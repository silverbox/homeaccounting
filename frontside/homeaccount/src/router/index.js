import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import locale from 'element-ui/lib/locale/lang/ja'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'element-ui/lib/theme-chalk/display.css'

Vue.use(Router, { locale })
Vue.use(ElementUI, { locale })

Vue.prototype.$axios = axios

Vue.prototype.apienv = {baseendpoint: process.env.API_ENDPOINT_BASE, key: process.env.API_KEY}
console.log(process.env.NODE_ENV)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
