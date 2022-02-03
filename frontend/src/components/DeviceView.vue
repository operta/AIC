<template>
  <a-card :title="`Device #${device.ID}`" hoverable bordered>
    <template #extra>
      <a-tag :color="device.available ? 'success' : 'error'">
        <template #icon>
          <wifi-outlined v-if="device.available" />
          <exclamation-circle-outlined v-else />
        </template>
        {{ device.available ? "Available" : "Unavailable" }}
      </a-tag></template
    >
    <a-tag :color="device.state === 'WORKING' ? 'processing' : 'warning'">
      <template #icon>
        <setting-outlined v-if="device.state === 'WORKING'" :spin="true" />
        <sync-outlined v-else-if="device.state === 'CHARGING'" :spin="true" />
      </template>
      {{ device.state }}
    </a-tag>

    <div>
      Battery
      <a-progress
        :percent="parseInt(device.battery)"
        size="small"
        :status="device.state === 'CHARGING' ? 'active' : 'normal'"
        :format="() => `${device.battery}%`"
      />
    </div>
    <div class="text item">Last update: {{ device.last_update }}</div>
    <div class="text item">Host: {{ device.host }}</div>
    <div class="text item">Port: {{ device.port }}</div>
  </a-card>
</template>

<script lang="ts">
import { DeviceStatus } from "@/models/DeviceStatus";
import { defineComponent, ref } from "vue";
import {
  ExclamationCircleOutlined,
  WifiOutlined,
  SettingOutlined,
  SyncOutlined,
} from "@ant-design/icons-vue";
export default defineComponent({
  components: {
    ExclamationCircleOutlined,
    WifiOutlined,
    SyncOutlined,
    SettingOutlined,
  },
  props: {
    device: {
      type: Object as () => DeviceStatus,
      required: true
    }
  },

  setup() {
    const error = ref(null);
    function getChargeIndicator(state: string, charge: number): string {
      if (state === "CHARGING") {
        return "active";
      }
      return charge > 50 ? "normal" : "error";
    }
    return { error, getChargeIndicator };
  },
});
</script>
<style></style>
