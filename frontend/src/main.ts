import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
// @ts-ignore
import VueApexCharts from 'vue3-apexcharts';

const app = createApp(App)
  .use(router)
  .use(store)
  .use(Antd)
  .use(VueApexCharts);

app.mount("#app");
