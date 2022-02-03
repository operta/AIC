<template>
  <a-form layout="inline">
    <a-form-item label="Automatically refresh">
      <a-switch v-model:checked="autoUpdate" />
    </a-form-item>
    <a-form-item>
      <a-button type="primary" @click="getDeviceStatus">
        Refresh
      </a-button>
    </a-form-item>
  </a-form>
  <a-row v-for="(row, index) in devicesRowed" :key="index">
    <a-col v-for="(device, i) in row" :key="i" span="8">
      <div class="">
        <device-view :device="device"> </device-view></div
    ></a-col>
  </a-row>
</template>

<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
  onBeforeUnmount,
  onUnmounted,
  reactive,
  ref,
} from "vue";
import { DeviceStatus } from "../models/DeviceStatus";
import { SERVER_NAME } from "../utils/ServerName";
import DeviceView from "../components/DeviceView.vue";
import { message } from "ant-design-vue";
import axios from "axios";

export default defineComponent({
  name: "DeviceViewer",
  components: { DeviceView },
  setup() {
    const serverName = SERVER_NAME;
    const errorMessage = ref("");
    const autoUpdate = ref(true);
    const state = reactive({
      devicesStatus: [] as DeviceStatus[],
    });
    // let devicesStatus: DeviceStatus[] = [];

    async function getDeviceStatus(): Promise<DeviceStatus[]> {
      return new Promise((resolve, reject) => {
        axios
          .get<DeviceStatus[]>(`${serverName}/api/status`, {
            timeout: 3000,
            timeoutErrorMessage: `Request timed out. Hostname: "${serverName}. Timeout: "3000ms"`
          })
          .then((response) => {
            message.success("Data successfully fetched", 1);
            state.devicesStatus = Object.values(response.data);
            resolve(Object.values(response.data));
          })
          .catch((error) => {
            message.error({
              content: "Unable to fetch data",
              duration: 2,
            });
            reject(error.message);
          });
      });
    }

    function callGetDeviceStatus(): void {
      if (autoUpdate.value) {
        getDeviceStatus();
      }
    }

    onUnmounted(() => {
      autoUpdate.value = false;
    });
    onMounted(() => {
      autoUpdate.value = true;
    });
    setInterval(() => callGetDeviceStatus(), 3000);

    getDeviceStatus().then((result) => {
      state.devicesStatus = result;
    });
    const devicesRowed = computed((): DeviceStatus[][] => {
      const devices = state.devicesStatus;
      const size = 3;
      const result = [];
      for (let i = 0; i < devices.length; i += size) {
        const chunk = devices.slice(i, i + size);
        result.push(chunk);
      }
      return result;
    });
    return { state, errorMessage, autoUpdate, devicesRowed, getDeviceStatus };
  },
});
</script>
