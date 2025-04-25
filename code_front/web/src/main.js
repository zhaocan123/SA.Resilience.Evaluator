import Vue from 'vue'
import axios from 'axios'
import store from './utils/store'

import App from './App'
import { router } from './router'
import ElementUI from 'element-ui'
import * as echarts from 'echarts'
import 'jquery'
import 'bootstrap'
import 'element-ui/lib/theme-chalk/index.css'
import MathJax from '@/utils/MathJax.js'
import Print from '@/utils/print'


Vue.use(ElementUI)
Vue.use(Print)
Vue.http = Vue.prototype.$http = axios


Vue.prototype.MathJax = MathJax
Vue.config.productionTip = false

Vue.prototype.$echarts = echarts

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
