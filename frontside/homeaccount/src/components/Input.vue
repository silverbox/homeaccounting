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
        <el-input v-model="slip.value" />
      </el-form-item>
      <el-form-item label="メモ">
        <el-input v-model="slip.memo" />
      </el-form-item>
      <el-form-item label="id">
        <el-input v-model="slip.uuid" :disabled="true" />
      </el-form-item>
    </el-form>
    <div class="dialog-footer">
      <el-button type="primary" @click="onsubmit">登録</el-button>
    </div>
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
      slip: {}
    }
  },
  mounted: function () {
    this.initData()
  },
  methods: {
    onsubmit: function () {
      console.log('slip-data1:' + this.slip.paymethod + ':' + this.slip.uuid)
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apienv.key,
          'Authorization': 1
        }
      }
      const slipdata = {
        'tgt_date': this.$myutils.getYYYYMMDDStr(this.slip.tgt_date),
        'kind_cd': this.slip.kind_cd,
        'method_cd': this.slip.paymethod,
        'uuid': this.slip.uuid,
        'value': this.slip.value,
        'memo': this.slip.memo ? this.slip.memo : ''
      }

      var self = this
      this.$axios.post(this.apienv.baseendpoint + 'slip', slipdata, config).then(
        response => {
          console.log(response.data)
          self.$message({message: '登録しました', type: 'success'})
          self.initData()
        }
      )
    },
    initData: function () {
      this.slip = {
        tgt_date: new Date(),
        kind_cd: this.$masterdata.kindmst[0].kind_cd,
        paymethod: this.$masterdata.paymethodmst[0].method_cd,
        value: 0,
        memo: '',
        uuid: ''
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.inputform{
  padding : 20px;
}
</style>
