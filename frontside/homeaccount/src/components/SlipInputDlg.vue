<template>
  <el-dialog title="入力" :visible.sync="slipDialogVisible">
    <el-form ref="form" :model="slip" label-width="60px">
      <el-form-item label="日付">
        <el-date-picker v-model="slip.tgt_date_obj" type="date" placeholder="Pick a day" />
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
        <el-select v-model="slip.method_cd" placeholder="Select payment method">
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
      <el-button type="warning" :plain="true" @click="ondelsubmit">削除</el-button>
      <el-button type="danger" :plain="true" @click="slipDialogVisible = false">中止</el-button>
      <el-button type="primary" @click="onupdsubmit">登録</el-button>
    </div>
  </el-dialog>
</template>

<script>

export default {
  name: 'SlipInputDlg',
  props: {
    parent: {
      type: Element,
      require: true
    },
    myutilsprm: {
      type: Object,
      require: true
    },
    masterdateprm: {
      type: Object,
      require: true
    },
    callbackprm: {
      type: Function,
      require: false
    }
  },
  data () {
    return {
      balance: 0,
      kindmst: this.masterdateprm.kindmst,
      paymethodmst: this.masterdateprm.paymethodmst,
      slipDialogVisible: false,
      slip: {
        tgt_date_obj: new Date(),
        kind_cd: '',
        method_cd: '',
        value: 0,
        memo: '',
        uuid: '',
        old_tgt_date: '',
        old_kind_cd: '',
        old_uuid: ''
      }
    }
  },
  mounted: function () {
    console.log('mounted:' + this.slip['uuid'])
    this.parent.appendChild(this.$el)
  },
  updated: function () {
    // console.log('updated:' + this.slip['uuid'])
  },
  methods: {
    setSlipData: function (slipdata) {
      this.slip = slipdata
      // this.slip.tgt_date_obj = this.myutilsprm.getLocalDate(this.slip.tgt_date)
      // this.slip.method_cd = this.slip.method_cd
      this.slip.old_tgt_date = this.slip.tgt_date
      this.slip.old_kind_cd = this.slip.kind_cd
      this.slip.old_uuid = this.slip.uuid
    },
    show: function () {
      console.log('show:' + this.slip.old_kind_cd + ':' + this.slip.old_tgt_date)
      this.slipDialogVisible = true
    },
    ondelsubmit: function () {
      this.onsubmitsub('del')
    },
    onupdsubmit: function () {
      this.onsubmitsub('upd')
    },
    onsubmitsub: function (mode) {
      console.log('slip-data1:' + this.slip.method_cd + ':' + this.slip.uuid)
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apienv.key,
          'Authorization': 1
        }
      }
      const slipdata = {
        'tgt_date': this.myutilsprm.getYYYYMMDDStr(this.slip.tgt_date_obj),
        'kind_cd': this.slip.kind_cd,
        'method_cd': this.slip.method_cd,
        'uuid': this.slip.uuid,
        'value': this.slip.value,
        'memo': this.slip.memo ? this.slip.memo : '',
        'old_tgt_date': this.slip.old_tgt_date,
        'old_kind_cd': this.slip.old_kind_cd,
        'old_uuid': this.slip.old_uuid
      }
      if (mode === 'del') {
        slipdata['tgt_date'] = ''
        slipdata['kind_cd'] = ''
        slipdata['uuid'] = ''
      }

      var self = this
      this.$axios.post(this.apienv.baseendpoint + 'slip', slipdata, config).then(
        response => {
          self.slipDialogVisible = false
          self.$message({message: '登録しました', type: 'success'})
          if (self.callbackprm !== undefined) {
            self.callbackprm(mode, slipdata)
          }
        }
      )
    }
  },
  destroyed: function () {
    console.log('destroyed:' + this.slip['uuid'])
    // this.$el.remove()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.inputform{
  padding : 20px;
}
.dialog-footer {
    text-align: right;
}
</style>
