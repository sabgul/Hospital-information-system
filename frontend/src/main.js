import Vue from 'vue'
import App from './App.vue'
import Vuesax from 'vuesax'
import { store } from './store/store';

import 'vuesax/dist/vuesax.css' //Vuesax styles

Vue.config.productionTip = false

Vue.use(Vuesax, {

});

new Vue({
  render: h => h(App),
  store,
}).$mount('#app')
