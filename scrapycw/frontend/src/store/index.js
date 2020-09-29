import Vue from 'vue'
import Vuex from 'vuex'
import languageUtil from "@/js/language"
import i18n from "@/i18n"

Vue.use(Vuex)

export default new Vuex.Store({
    strict: process.env.NODE_ENV !== 'production', // 非生产环境下启用严格模式
    state: {
        lang: i18n.locale
    },
    mutations: {
        setLanguage(state, lang) {
            state.lang = lang;
            languageUtil.setToLocalStorage(lang);
            i18n.locale = lang;
        },
    },
    actions: {},
    modules: {}
})