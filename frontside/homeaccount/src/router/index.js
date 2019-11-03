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

var API_URL_BASE = '/api/'
var API_KEY = ''
if (process.env.NODE_ENV !== 'production') {
  API_URL_BASE = 'https://fugafuga.execute-api.ap-northeast-1.amazonaws.com/dev/api/'
  API_KEY = 'hogehoge'
}
Vue.prototype.apienv = {baseurl: API_URL_BASE, key: API_KEY}

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
