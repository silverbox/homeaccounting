<template>
  <div class='container'>
    <BarChart v-if='loaded' :chartData='chartData' :chartOptions='chartOptions'></BarChart>
    <LineChart v-if='loaded' :chartData='balanceChartData' :chartOptions='balanceOptions'></LineChart>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue';

import BarChart from '@/components/BarChart';
import LineChart from '@/components/LineChart';
import * as palette from 'google-palette';
import { accountUtils, DEF_SLIP } from '@/common/accountUtils';
import ApiCalls from '@/common/api';

const LOAD_DATE_CNT = 7;

const TOOLTIPOPTION = {
  callbacks: {
    label: function (tooltipItem, data) {
      var label = tooltipItem.dataset.label;
      const infoAry = tooltipItem.dataset.detail[tooltipItem.dataIndex];
      if (label) {
        label += `: ${tooltipItem.dataset.data[tooltipItem.dataIndex]}`;
        if (infoAry && infoAry.join('').length > 0) {
          label += '[' + tooltipItem.dataset.detail[tooltipItem.dataIndex].join(', ') + ']';
        }
      }
      return label;
    }
  }
}

export default defineComponent({
  name: 'GraphView',
  components: {
    LineChart,
    BarChart
  },
  setup() {
    const api = new ApiCalls();

    const loaded = ref(false);
    const chartData = ref({});
    const chartOptions = ref({});
    const balanceChartData = ref({});
    const balanceOptions = ref({});

    const loadgraph = async () => {
      const tgtToDateStr = accountUtils.getYYYYMMDDStr(new Date());

      const graphDataResponse = await api.getChartDataResponse(tgtToDateStr, LOAD_DATE_CNT);

      chartOptions.value = {
        'plugins': {
          'title': {
            display: true,
            text: '消費額'
          },
          'tooltip': TOOLTIPOPTION
        },
        'scales': {
          'x': {
            'stacked': 'true',
            'title': {
              'display': 'true',
              'text': '日付'
            }
          },
          'y': {
            'stacked': 'true',
            'title': {
              'display': 'true',
              'text': '金額'
            },
            'ticks': {
              'stepSize': 500
            },
            'beginAtZero': 'true'
          }
        }
      };

      // chartOptions.value = {}; //graphDataResponse['options'];
      // chartOptions.value['plugins'] = { 'tooltip': TOOLTIPOPTION };
      const barColors = palette('mpn65', graphDataResponse['chartdata']['datasets'].length).map((hex) => {
        return '#' + hex;
      });
      graphDataResponse['chartdata']['datasets'].forEach(function (datasets, index) {
        datasets['backgroundColor'] = barColors[index]
      });
      chartData.value = graphDataResponse['chartdata'];

      balanceOptions.value = {
        'plugins': {
          'title': {
            display: true,
            text: '残高推移'
          }
        },
        'scales': {
          'x': {
            'stacked': 'true',
            'title': {
              'display': 'true',
              'text': '日付'
            }
          },
          'y': {
            'title': {
              'display': 'true',
              'text': '金額'
            },
            'ticks': {
              'stepSize': 5000
            },
            'beginAtZero': 'true'
          }
        }
      };
      // balanceOptions.value = graphDataResponse['balanceoptions'];
      const lineColors = palette('mpn65', graphDataResponse['balancechartdata']['datasets'].length).map((hex) => {
        return '#' + hex
      });
      graphDataResponse['balancechartdata']['datasets'].forEach(function (datasets, index) {
        datasets['borderColor'] = lineColors[index]
        datasets['lineTension'] = 0
      });
      balanceChartData.value = graphDataResponse['balancechartdata'];

      loaded.value = true;
    };

    onMounted(() => {
      loaded.value = false;
      loadgraph();
    });
    return {
      loaded,
      chartData,
      chartOptions,
      balanceChartData,
      balanceOptions
    }
  }
});
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>

</style>
