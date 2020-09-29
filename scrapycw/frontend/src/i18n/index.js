import VueI18n from 'vue-i18n';
import Vue from "vue";
import messages from './message';
import support from "./support";
import language from "@/js/language"

let lang = language.getCurrentOrDefault();
Vue.use(VueI18n);

const i18n = new VueI18n({
    locale: lang,
    messages,
});

export { messages, support };
export default i18n;