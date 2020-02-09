import support from "@/i18n/support";
import config from "@/config";

export default {
    /**
     * 获取当前浏览器语言
     */
    getBrowser: () => navigator.language || navigator.userLanguage,
    /**
     * 获取当前语言，检查 localStorage 中是否有设置语言
     */
    getByLocalStorage: () => localStorage.getItem("lang"),
    /**
     * 保存当前语言，将语言代码写入到 localStorage 中
     */
    setToLocalStorage: lang => localStorage.setItem("lang", lang),
    /**
     * 检查当前模块是否支持当前语言
     */
    support: lang => lang in support,
    /**
     * 获取当前可用语言，如果当前模块支持当前语言，则返回当前语言，如果不支持当前语言，则返回默认语言
     */
    getCurrentOrDefault() {
        let _this = this;
        let lang = _this.getByLocalStorage() || _this.getBrowser();
        if (_this.support(lang)) {
            return lang;
        }
        lang = lang.substr(0, 2);
        return _this.support(lang) ? lang : config.defaultLanguage
    }
}