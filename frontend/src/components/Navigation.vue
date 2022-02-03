<template>
  <a-layout-sider breakpoint="lg" collapsed-width="0">
    <div class="logo">AIC Lab</div>
    <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
      <a-menu-item v-for="route in routes" :key="route.path">
        <router-link class="nav-text" :to="route.path">
          {{ route.name }}
        </router-link>
      </a-menu-item>
    </a-menu>
  </a-layout-sider>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import router from "../router/index";

export default defineComponent({
  name: "Navigation",
  setup() {
    const activeLink = ref("");
    const route = useRoute();
    const routes = router.getRoutes().map((route) => {
      return { name: route.name, path: route.path };
    });
    const selectedKeys = ref([router.currentRoute.value.path]);

    watch(
      () => route.path,
      () => {
        activeLink.value = route.path;
      }
    );
    onMounted(() => {
      activeLink.value = router.currentRoute.value.path;
    });
    return { activeLink, route, selectedKeys, routes };
  },
});
</script>

<style>
#components-layout-demo-responsive .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}
</style>
