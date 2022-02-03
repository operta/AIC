<template>
  <a-layout id="components-layout-demo-responsive">
    <navigation />
    <a-layout>
      <a-layout-content :style="{ margin: '24px 16px 0' }">
        <div
          :style="{ padding: '24px', background: '#fff', minHeight: '90vh' }"
        >
          <router-view />
        </div>
      </a-layout-content>
      <a-layout-footer style="textAlign: center">
        AIC Labaratory assignment W2020
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script lang="ts">
import Vue, { defineComponent, onMounted, ref, watch } from "vue";
import Navigation from "./components/Navigation.vue";
export default defineComponent({
  components: {
    Navigation,
  },
});
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
