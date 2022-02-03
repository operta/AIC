import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
  RouteRecordRaw,
} from "vue-router";
import PredictForm from "../views/PredictForm.vue";
import LossChartContainer from "../views/LossChartContainer.vue";
import DeviceViewer from "../views/DeviceViewer.vue";

const routerHistory = createWebHistory();

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Dashboard",
    component: DeviceViewer,
  },
  {
    path: "/forecast",
    name: "Forecast",
    component: PredictForm,
  },
  {
    path: "/losschart",
    name: "Loss Chart",
    component: LossChartContainer,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
