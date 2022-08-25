<template>
  <el-dialog title="入力" :visible.sync="slipDialogVisible" class="slipinputdlg" v-loading="saving">
    <el-form ref="form" :model="slip" label-width="80px">
      <el-form-item label="日付">
        <el-date-picker v-model="slip.tgt_date_obj" type="date" placeholder="Pick a day" />
      </el-form-item>
      <el-form-item label="種類">
        <el-select v-model="slip.kind_cd" placeholder="Select item kind">
          <el-option
            v-for="item in kindMst"
            :key="item.kind_cd"
            :label="item.kind_nm"
            :value="item.kind_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="支払方法">
        <el-select v-model="slip.method_cd" placeholder="Select payment method">
          <el-option
            v-for="item in payMethodMst"
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
      <el-button type="warning" :plain="true" @click="onDelSubmit">削除</el-button>
      <el-button type="danger" :plain="true" @click="slipDialogVisible = false">中止</el-button>
      <el-button type="primary" @click="onUpdSubmit">登録</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { defineComponent, computed, ref, onMounted, props, toRefs } from 'vue';
import masterdata, { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';
import { SlipRec, BalanceView } from '@/common/interfaces';
import myutils from '@/common/myutils';

const slipDef: SlipRec = {
  tgt_date: new Date(),
  kind_cd: KIND_MST[0].kind_cd,
  method_cd: PAY_METHOD_MST[0].method_cd,
  uuid: '',
  value: 0,
  memo: ''
};

export default defineComponent({
  name: 'SlipInputDlg',
  setup(props, context) {
    const api = new ApiCalls();
    const { callbackprm } = toRefs(props);
    const kindMst = KIND_MST;
    const payMethodMst = PAY_METHOD_MST;
    const slipDialogVisible = refs<boolean>(false);
    const balance = refs<number>(0);
    const saving = refs<boolean>(false);
    const slip = refs<SlipRec>(myutils.cloneSlip(slipDef));
    const slipOld = refs<SlipRec>(myutils.cloneSlip(slipDef));
    //
    const setSlipData = (slipdata: SlipRec) => {
      slip.value = myutils.cloneSlip(slipdata);
      slipOld.value = myutils.cloneSlip(slipdata);
    };
    const show = () => {
      slipDialogVisible.value = true;
    };
    const onDelSubmit = () => {
      onSubmitSub('del');
    };
    const onUpdSubmit = () => {
      onSubmitSub('upd');
    };
    const onSubmitSub = (mode) => {
      saving.value = true;

      const slipData = {
        'tgt_date': myutils.getYYYYMMDDStr(slip.value.tgt_date_obj),
        'kind_cd': slip.value.kind_cd,
        'method_cd': slip.value.method_cd,
        'uuid': slip.value.uuid,
        'value': slip.value.value,
        'memo': slip.value.memo ? slip.value.memo : '',
        'old_tgt_date': myutils.getYYYYMMDDStr(slipOld.value.tgt_date_obj),
        'old_kind_cd': slipOld.value.kind_cd,
        'old_uuid': slipOld.value.uuid,
        'old_method_cd': slipOld.value.method_cd,
        'old_value': slipOld.value.value
      }
      if (mode === 'del') {
        slipData['tgt_date'] = ''
        slipData['kind_cd'] = ''
        slipData['uuid'] = ''
      }

      await api.postSlip(slipData);
      slipDialogVisible.value = false;
      ElMessage({
        showClose: true,
        message: '登録しました',
        type: 'success',
      });
      saving.value = false;
      if (callback.value !== undefined) {
        callback.value(mode, slipData)
      }
    };

    return {
      balance,
      kindMst,
      payMethodMst,
      slipDialogVisible,
      saving,
      slip,
      slipOld,
      //
      setSlipData,
      show,
      onDelSubmit,
      onUpdSubmit,
    }
  },
  props: {
    parent: {
      type: Element,
      require: true
    },
    callback: {
      type: Function,
      require: false
    }
  },
  mounted: function () {
    // console.log('mounted:' + this.slip['uuid'])
    this.parent.appendChild(this.$el)
  },
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
@media (max-width:640px) {
  .slipinputdlg >>> .el-dialog {
    width: 280px;
  }
  .slipinputdlg >>> .el-date-editor.el-input, .el-date-editor.el-input__inner {
    width: 160px;
  }
}
</style>
