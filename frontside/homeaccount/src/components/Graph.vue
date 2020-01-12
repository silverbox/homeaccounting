<template>
  <div class='container'>
    <bar-chart v-if='loaded' :chart-data='chartdata' :options='options'></bar-chart>
    <line-chart v-if='loaded' :chart-data='balancechartdata' :options='balanceoptions'></line-chart>
  </div>
</template>

<script>
import BarChart from '@/components/BarChart.js'
import LineChart from '@/components/LineChart.js'
import * as palette from 'google-palette'

const LOAD_DATE_CNT = 7

const TOOLTIPOPTION = {
  callbacks: {
    label: function (tooltipItem, data) {
      var label = data.datasets[tooltipItem.datasetIndex].label || ''

      if (label) {
        label += ': '
      }
      label += tooltipItem.yLabel + ' ['
      label += data.datasets[tooltipItem.datasetIndex].detail[tooltipItem.index] + ']'
      // console.log(tooltipItem)
      // console.log(tooltipItem.datasetIndex + ':' + tooltipItem.index)
      return label
      // var retlist = []
      // retlist.push(label)
      // retlist.push(data.datasets[tooltipItem.datasetIndex].detail[tooltipItem.index])
      // console.log(data.datasets[tooltipItem.datasetIndex].detail[tooltipItem.index])
      // console.log(retlist)
      // return retlist
    }
  }
}

export default {
  name: 'Graph',
  components: {
    LineChart,
    BarChart
  },
  data: () => ({
    loaded: false,
    chartdata: null,
    options: null,
    balancechartdata: null,
    balanceoptions: null
  }),
  mounted () {
    this.loaded = false
    this.loadgraph()
  },
  methods: {
    loadgraph: function () {
      var that = this

      that.loading = true
      const tgttodatestr = that.$myutils.getYYYYMMDDStr(new Date())

      const prmstr = 'tgt_date_to=' + tgttodatestr + '&tgt_date_count=' + LOAD_DATE_CNT
      this.$cognito.callGetApi(that.$axios, that.apienv.baseendpoint + 'chart?' + prmstr).then(response => {
        console.log('loadgraph response:' + prmstr)
        that.options = response.data['options']
        that.options['tooltips'] = TOOLTIPOPTION
        const barcolors = palette('mpn65', response.data['chartdata']['datasets'].length).map((hex) => {
          return '#' + hex
        })
        response.data['chartdata']['datasets'].forEach(function (value, index) {
          value['backgroundColor'] = barcolors[index]
        })
        that.chartdata = response.data['chartdata']

        that.balanceoptions = response.data['balanceoptions']
        const linecolors = palette('mpn65', response.data['balancechartdata']['datasets'].length).map((hex) => {
          return '#' + hex
        })
        response.data['balancechartdata']['datasets'].forEach(function (value, index) {
          value['borderColor'] = linecolors[index]
          value['lineTension'] = 0
        })
        that.balancechartdata = response.data['balancechartdata']

        that.loaded = true
      }).catch(err => {
        that.$message({message: err, type: 'error'})
      })
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>

</style>
