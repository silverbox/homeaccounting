<template>
  <div class='container'>
    <bar-chart v-if='loaded' :chart-data='chartdata' :options='options'></bar-chart>
  </div>
</template>

<script>
import BarChart from '@/components/BarChart.js'
import * as palette from 'google-palette'

const LOAD_DATE_CNT = 7

export default {
  name: 'Graph',
  components: {
    BarChart
  },
  data: () => ({
    loaded: false,
    chartdata: null,
    options: null
  }),
  mounted () {
    this.loaded = false
    this.loadgraph()
  },
  methods: {
    loadgraph: function () {
      var that = this
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': that.apienv.key,
          'Authorization': 1
        },
        data: {}
      }
      that.loading = true
      const tgttodatestr = that.$myutils.getYYYYMMDDStr(new Date())

      const prmstr = 'tgt_date_to=' + tgttodatestr + '&tgt_date_count=' + LOAD_DATE_CNT
      console.log('loadgraph start:' + prmstr)
      that.$axios.get(that.apienv.baseendpoint + 'chart?' + prmstr, config).then(
        response => {
          that.options = response.data['options']
          const barcolors = palette('mpn65', response.data['chartdata']['datasets'].length).map((hex) => {
            return '#' + hex
          })
          response.data['chartdata']['datasets'].forEach(function (value, index) {
            value['backgroundColor'] = barcolors[index]
          })
          that.chartdata = response.data['chartdata']

          that.loaded = true
        }
      )
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>

</style>
