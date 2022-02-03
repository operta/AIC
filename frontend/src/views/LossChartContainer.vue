<template>
  <div class="container">
    <div>
      <apexchart type="line" height="500" :options="state.chartOptions" :series="state.series"></apexchart>
    </div>
  </div>
</template>

<script>
import { SERVER_NAME } from "../utils/ServerName";
import {
  computed,
  defineComponent,
  onMounted,
  onBeforeUnmount,
  onUnmounted,
  reactive,
  ref,
} from "vue";

export default defineComponent({
    name: 'LossChartContainer',
    setup() {
        const state = reactive({
            update: true,
            series: [{
                data: []
            }],
            chartOptions: {
                chart: {
                    id: 'realtime',
                    height: 350,
                    type: 'line',
                    zoom: {
                        enabled: false
                    }
                },
                animations: {
                    enabled: false,
                    easing: 'linear',
                    dynamicAnimation: {
                        speed: 1000
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'straight'
                },
                title: {
                    text: 'Losses over training rounds',
                    align: 'left'
                },
                grid: {
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                xaxis: {
                    type: "numeric"
                }
            }
        })
        function updateData() {
            if(state.update) {
                try {
                    fetch(SERVER_NAME + "/api/losses").then((response) =>{
                        response.json().then((losses) => {
                            state.series = [{
                                data: losses.loss
                            }]
                        })
                    });
                } catch (e) {
                    console.error(e)
                }
            }
        }
        updateData();
        setInterval(() => updateData(), 3000);
        onUnmounted(() => {
            state.update = false;
        });
        onMounted(() => {
            state.update = true;
        });
        return { updateData, state }
    },
    // data() {
    //     return {
    //         loaded: false,
    //         series: [{
    //             data: []
    //         }],
    //         chartOptions: {
    //             chart: {
    //                 id: 'realtime',
    //                 height: 350,
    //                 type: 'line',
    //                 zoom: {
    //                     enabled: false
    //                 }
    //             },
    //             animations: {
    //                 enabled: false,
    //                 easing: 'linear',
    //                 dynamicAnimation: {
    //                     speed: 1000
    //                 }
    //             },
    //             dataLabels: {
    //                 enabled: false
    //             },
    //             stroke: {
    //                 curve: 'straight'
    //             },
    //             title: {
    //                 text: 'Losses over training rounds',
    //                 align: 'left'
    //             },
    //             grid: {
    //                 row: {
    //                     colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
    //                     opacity: 0.5
    //                 },
    //             },
    //             xaxis: {
    //                 type: "numeric"
    //             }
    //         }
    //     }
    // },
    // methods: {
    //     updateData: function () {
    //         this.loaded = false
    //         try {
    //             fetch(SERVER_NAME + "/api/losses").then((response) =>{
    //                 response.json().then((losses) => {
    //                     this.series = [{
    //                         data: losses.loss
    //                     }]
    //                     this.loaded = true
    //                 })
    //             });
    //         } catch (e) {
    //             console.error(e)
    //         }

    //     }
    // },
    // mounted () {
    //     this.updateData();
    //     // setInterval(() => {this.updateData()}, 3000)
    // }
})
</script>