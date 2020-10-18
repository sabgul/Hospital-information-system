import Vue from 'vue'
import App from '@/App.vue'
import Vuesax from 'vuesax'
import { store } from '@/store/store';
import router from '@/router/router.js';

import 'vuesax/dist/vuesax.css' //Vuesax styles

Vue.config.productionTip = false

Vue.use(Vuesax, {
});

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
