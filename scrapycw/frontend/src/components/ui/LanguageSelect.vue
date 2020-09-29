<template>
  <div class="language-select">
    <Select v-model="lang" size="small" class="select-area" @on-change="changeLanguage">
      <Option v-for="(value, key) in languages" :value="key" :key="key">{{ value }}</Option>
    </Select>
  </div>
</template>

<script>
import { support as supportLanguages } from '@/i18n'

export default {
  name: 'LanguageSelect',
  data() {
    let vm = this;
    return {
      languages: supportLanguages,
      lang: vm.$store.state.lang
    }
  },
  methods: {
    changeLanguage() {
      let vm = this;
      vm.$store.commit("setLanguage", vm.lang);
    }
  }
}
</script>

<style scoped>
  .language-select {
    display: inline-block;
  }
  .language-select >>> .ivu-select-selection {
    background: inherit;
    border: 0;
    box-shadow: none;
  }
  .language-select >>> .ivu-select-selection .ivu-select-selected-value {
    padding: 0;
  }
  .select-area {
    width: 70px;
    color: inherit;
  }
</style>