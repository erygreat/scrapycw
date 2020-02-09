<template>
    <div class="layout clear-float">
        <Menu mode="horizontal" theme="dark" active-name="1">
            <div class="layout-ceiling-logo">
                <!-- TODO 添加logo -->
            </div>
            <div class="layout-ceiling-nav">
                <MenuItem name="1">
                    <Icon type="logo-reddit" />
                    <router-link to="dashboard">{{ $t("Dashboard") }}</router-link>
                </MenuItem>
            </div>
            <div class="layout-ceiling-right">
                <router-link to="help">{{ $t("help")}}</router-link> | 
                <language-select></language-select>
            </div>
        </Menu>
    </div>
</template>

<script>
import LanguageSelect from "@/components/ui/LanguageSelect"
export default {
  components: { LanguageSelect },
}
</script>

<style scoped>
    .layout{
        background: #f5f7f9;
        position: relative;
    }
    .layout div,
    .layout a,
    .layout >>> a {
        color: #fbfbfb;
        text-decoration: none;
    }
    .layout-ceiling-logo {
        width: 20%;
        float: left;
        height: 100%;
    }
    .layout-ceiling-right {
        margin-right: 15px;
        float: right;

    }
</style>
