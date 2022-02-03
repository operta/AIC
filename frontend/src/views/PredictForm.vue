<template>
  <a-row :gutter="20">
    <a-col :span="8"
      ><div class="grid-content bg-purple">
        <a-form :wrapper-col="state.wrapperCol" :label-col="state.labelCol">
          <a-form-item has-feedback label="CO" name="co">
            <a-input-number
              v-model:value="state.form.co"
              :precision="5"
              step="0.1"
            />
          </a-form-item>
          <a-form-item has-feedback label="NO2" name="no2">
            <a-input-number
              v-model:value="state.form.no2"
              :precision="5"
              step="0.1"
            />
          </a-form-item>
          <a-form-item has-feedback label="O3" name="o3">
            <a-input-number
              v-model:value="state.form.o3"
              :precision="5"
              step="0.1"
            />
          </a-form-item>
          <a-form-item has-feedback label="PM2" name="pm2_5">
            <a-input-number
              v-model:value="state.form.pm2_5"
              :precision="5"
              step="0.1"
            />
          </a-form-item>
          <a-form-item has-feedback label="PM10" name="no2">
            <a-input-number
              v-model:value="state.form.pm10"
              :precision="5"
              step="0.1"
            />
          </a-form-item>
          <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
            <a-button type="primary" @click="postForm">
              Send request
            </a-button>
          </a-form-item>
        </a-form>
      </div></a-col
    >
    <a-col :span="16">
      <a-button type="primary" @click="getCurrentJobs">Refresh</a-button>
      <a-table
        :columns="state.columns"
        :data-source="currentJobs"
        :pagination="pagination"
        :loading="false"
      >
        <template #datetime="{ text }">
          {{ formatDate(text) }}
        </template>
      </a-table>
    </a-col>
  </a-row>
</template>
<script lang="ts">
import { DataModel } from "../models/DataModel";
import { SERVER_NAME } from "../utils/ServerName";
import axios from "axios";
import { computed, defineComponent, onMounted, reactive, ref } from "vue";
import moment from "moment";
import { message } from "ant-design-vue";
export default defineComponent({
  setup() {
    const serverName = SERVER_NAME;
    const error = ref(null);
    const state = reactive({
      form: {
        date: 0,
        co: 0.01,
        no2: 0.01,
        o3: 0.01,
        pm2_5: 0.01,
        pm10: 0.01,
      },
      columns: [
        {
          title: "Date/time",
          dataIndex: "datetime",
          key: "1",
          slots: { customRender: "datetime" },
        },
        { title: "CO", dataIndex: "co", key: "2" },
        { title: "NO2", dataIndex: "no2", key: "3" },
        { title: "O3", dataIndex: "o3", key: "3" },
        { title: "PM2", dataIndex: "pm2_5", key: "4" },

        { title: "PM10", dataIndex: "pm10", key: "5" },
        { title: "SO2 (result)", dataIndex: "result", key: "6" },
      ],
      labelCol: { span: 6 },
      wrapperCol: { span: 12 },
    });

    const jobs = ref([] as DataModel[]);

    function formatDate(datetimeUnix: number): string {
      return new Date(datetimeUnix * 1000).toLocaleString();
    }
    const currentJobs = computed((): DataModel[] => {
      return jobs.value.reverse();
    });
    async function getCurrentJobs(): Promise<DataModel[]> {
      return new Promise((resolve, reject) => {
        axios
          .get<DataModel[]>(`${serverName}/api/jobs`, {
            timeout: 3000,
            timeoutErrorMessage: `Request timed out. Hostname: "${serverName}. Timeout: "3000ms"`,
          })
          .then((response) => {
            jobs.value = response.data;
            resolve(response.data);
            message.success("Jobs list fetched successfully", 1);
          })
          .catch((error) => {
            message.error(`Failure to fetch jobs list: ${error}`, 3);

            reject(error);
          });
      });
    }
    onMounted(() => {
      getCurrentJobs();
    });

    function onOk(newTimestamp: moment.Moment) {
      state.form.date = newTimestamp.unix();
    }
    function postForm() {
      const formData = {
        datetime: Math.round(new Date().getTime() / 1000),
        co: state.form.co,
        no2: state.form.no2,
        o3: state.form.o3,
        pm2_5: state.form.pm2_5,
        pm10: state.form.pm10,
        completed: false,
      } as DataModel;
      axios
        .post(`${serverName}/api/predict`, formData)
        .then((response) => {
          message.success("Data sent successfully", 2);

          jobs.value.push(formData);
        })
        .catch((error) => {
          message.error(`Failure when sending the data: ${error}`, 3);
        });
    }
    return {
      state,
      error,
      postForm,
      getCurrentJobs,
      formatDate,
      moment,
      onOk,
      currentJobs,
    };
  },
});
</script>
<style></style>
