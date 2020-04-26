<template>
  <div class="inputform">
    <el-form ref="form" :model="slip" label-width="100px">
      <el-form-item label="日付">
        <el-date-picker v-model="slip.tgt_date" type="date" placeholder="Pick a day" />
      </el-form-item>
      <el-form-item label="種類">
        <el-select v-model="slip.kind_cd" placeholder="Select item kind">
          <el-option
            v-for="item in kindmst"
            :key="item.kind_cd"
            :label="item.kind_nm"
            :value="item.kind_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="支払方法">
        <el-select v-model="slip.paymethod" placeholder="Select payment method">
          <el-option
            v-for="item in paymethodmst"
            :key="item.method_cd"
            :label="item.method_nm"
            :value="item.method_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="金額">
        <el-input v-model="slip.value" type="number"/>
      </el-form-item>
      <el-form-item label="メモ">
        <el-input v-model="slip.memo" />
      </el-form-item>
      <el-form-item label="id">
        <el-input v-model="slip.uuid" :disabled="true" />
      </el-form-item>
    </el-form>
    <div class="dialog-footer">
      <el-button type="primary" :loading="submiting" @click="onsubmit">登録</el-button>
    </div>
    <p v-loading="balanceloading" class="balancetable">
      <el-table
        :data="balancelist"
        style="width: 80%">
        <el-table-column
          prop="method_nm"
          label="種類"
          width="180"
          align="center">
        </el-table-column>
        <el-table-column
          prop="value_fmt"
          label="金額"
          width="100"
          align="center">
        </el-table-column>
      </el-table>
    </p>
  </div>
</template>

<script>

export default {
  name: 'Input',
  data () {
    return {
      balance: 0,
      kindmst: this.$masterdata.kindmst,
      paymethodmst: this.$masterdata.paymethodmst,
      submiting: false,
      slip: {},
      balanceloading: false,
      balancedate: undefined,
      balancelist: []
    }
  },
  mounted: function () {
    this.initData()
  },
  methods: {
    onsubmit: function () {
      console.log('slip-data1:' + this.slip.paymethod + ':' + this.slip.uuid)
      this.submiting = true

      const slipdata = {
        'tgt_date': this.$myutils.getYYYYMMDDStr(this.slip.tgt_date),
        'kind_cd': this.slip.kind_cd,
        'method_cd': this.slip.paymethod,
        'uuid': this.slip.uuid,
        'value': this.slip.value,
        'memo': this.slip.memo ? this.slip.memo : ''
      }

      var self = this
      this.$cognito.callPostApi(this.$axios, this.apienv.baseendpoint + 'slip', slipdata).then(
        response => {
          console.log(response.data)
          self.$message({message: '登録しました', type: 'success'})
          self.initData()
          self.submiting = false
        }
      ).catch(err => {
        self.$message({message: err, type: 'error'})
        self.submiting = false
      })
    },
    initData: function () {
      var that = this

      // init data
      that.slip = {
        tgt_date: new Date(),
        kind_cd: that.$masterdata.kindmst[0].kind_cd,
        paymethod: that.$masterdata.paymethodmst[0].method_cd,
        value: 0,
        memo: '',
        uuid: ''
      }

      // get balance data
      const tgttodatestr = that.$myutils.getYYYYMMDDStr(new Date())
      const prmstr = 'tgt_date=' + tgttodatestr
      this.balanceloading = true
      this.$cognito.callGetApi(that.$axios, that.apienv.baseendpoint + 'balance?' + prmstr).then(
        response => {
          that.finload(that, response)
          this.balanceloading = false
        }
      ).catch(err => {
        that.$message({message: err, type: 'error'})
        this.balanceloading = false
      })
    },
    finload: function (that, response) {
      var wkdatestr = ''
      var wkbalancelist = []
      for (var resdata of response.data) {
        wkdatestr = that.$myutils.getLocalDateStr(resdata['tgt_date'])
        var wkbalance = {}
        wkbalance['method_nm'] = that.$masterdata.getMethodNm(resdata['method_cd'])
        wkbalance['value_fmt'] = Number(resdata['value']).toLocaleString()
        wkbalancelist.push(wkbalance)
      }
      that.balancedate = wkdatestr
      that.balancelist = wkbalancelist
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.inputform{
  padding : 20px;
}
.balancetable{
  padding : 5px 0px 0px 10px;
}
</style>
