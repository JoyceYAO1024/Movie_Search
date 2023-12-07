import Vue from 'vue'
import App from './App.vue'
import router from './router'

import 'normalize.css' // reset style
import '@/styles/index.scss'
import ElementUI from 'element-ui' // use element-ui lib
import 'element-ui/lib/theme-chalk/index.css' // use element-ui lib style
import '@/styles/theme/index.css' // change element-ui lib style primary color
import '@/styles/icon/iconfont.css' // use icon font

Vue.config.productionTip = false
Vue.use(ElementUI, {
  // size: 'small'
})
new Vue({
  render: h => h(App),
  router
}).$mount('#app')
