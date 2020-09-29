<template>
  <div class="spider-management">
    <el-menu class="menu" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
      <el-submenu index="1">
        <template slot="title">
          <Icon type="logo-reddit" />
          <span slot="title"> {{ $t("Operating")}}</span>
        </template>
        <el-menu-item index="1-1">
          <router-link to="/spider-management/spiders">爬虫列表</router-link>
          <router-link to="/spider-management/jobs">任务列表</router-link>
        </el-menu-item>
      </el-submenu>
    </el-menu>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SpiderManagement',
}
</script>

<style scoped>
.spider-management {
  display: flex;
  height: 100%;
}
.menu {
  width: 200px;
  height: 100%;
}
</style>