import Vue from 'vue'
import App from '@/App.vue'
import { store } from '@/store/store';
import router from '@/router/router.js';
import Vuesax from 'vuesax';
import 'vuesax/dist/vuesax.css'; // Vuesax styles
import '@/assets/css/global.css';

Vue.config.productionTip = false;
Vue.prototype.window = window;

Vue.use(Vuesax, {
});

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
