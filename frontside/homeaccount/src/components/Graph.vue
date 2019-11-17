<template>
  <div class="hello">
    <div class="sample">
      <h2>Basic Button</h2>
      <el-row>
        <el-button plain>Plain</el-button>
        <el-button type="primary" plain @click="reload">Reload</el-button>
        <el-button type="success" plain>Success</el-button>
        <el-button type="info" plain>Info</el-button>
        <el-button type="warning" plain>Warning</el-button>
        <el-button type="danger" plain>Danger</el-button>
      </el-row>
    </div>

    <div class="sample">
      <h2>Text Button</h2>
      <el-row>
        <el-date-picker v-model="tgtdate" type="date" placeholder="Pick a day" />
        <el-input v-model="balance" />
      </el-row>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Graph',
  data () {
    return {
      balance: 0,
      tgtdate: new Date()
    }
  },
  methods: {
    reload: function () {
      console.log(this.tgtdate)
      console.log(this.apienv.baseendpoint)
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apienv.key,
          'Authorization': 1
        },
        data: {}
      }

      this.$axios.get(this.apienv.baseendpoint + 'balance?tgt_date=20190831', config).then(
        response => {
          console.log(response.data)
          /* this.tableData3 = response.data; */
        }
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
