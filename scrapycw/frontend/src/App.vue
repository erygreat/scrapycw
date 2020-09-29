<template>
  <div id="app">
    <layout-header></layout-header>
    <router-view/>  
  </div>
</template>

<script>
import LayoutHeader from "@/components/LayoutHeader"
export default {
  name: "App",
  components: { LayoutHeader },
}
</script>

<style scoped> 
#app {
  height: 100%;
  overflow-y: hidden;
}
</style>