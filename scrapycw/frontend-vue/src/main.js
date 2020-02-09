import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import "./css/reset.css";
import "./css/init.css";
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
import { Menu, Submenu, MenuItem, MenuItemGroup } from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ViewUI);

Vue.use(MenuItem)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItemGroup)

Vue.config.productionTip = false

new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount('#app')