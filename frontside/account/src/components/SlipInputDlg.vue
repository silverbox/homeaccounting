<template>
  <div class="slipinputdlg">
  <el-dialog title="入力" v-model="dialogShow" center>
    <el-form ref="form" v-model="slip" label-width="80px">
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
      <el-button type="danger" :plain="true" @click="dialogShow = false">中止</el-button>
      <el-button type="primary" @click="onUpdSubmit">登録</el-button>
    </div>
  </el-dialog>
  </div>
</template>

<script>
import { defineComponent, computed, ref, watch, toRefs } from 'vue';
import { ElMessage } from 'element-plus'

import { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';
import { SlipView } from '@/common/interfaces';
import { accountUtils } from '@/common/accountUtils';
import ApiCalls from '@/common/api';

export default defineComponent({
  name: 'SlipInputDlg',
  setup(props, context) {
    const api = new ApiCalls();
    //
    const { slipdata, dialogVisible } = toRefs(props);
    const dialogShow = computed({
      get: () => dialogVisible.value,
      set: val => {if (!val) {context.emit('cancelDialog')}}
    });

    const kindMst = KIND_MST;
    const payMethodMst = PAY_METHOD_MST;
    const balance = ref(0);
    const saving = ref(false);
    const slip = ref(accountUtils.cloneSlip(slipdata.value));
    const slipOld = ref(accountUtils.cloneSlip(slipdata.value));
    //
    const onDelSubmit = () => {
      onSubmitSub('del');
    };
    const onUpdSubmit = () => {
      onSubmitSub('upd');
    };
    const onSubmitSub = async (mode) => {
      const slipData = {
        'tgt_date': accountUtils.getYYYYMMDDStr(slip.value.tgt_date_obj),
        'kind_cd': slip.value.kind_cd,
        'method_cd': slip.value.method_cd,
        'uuid': slip.value.uuid,
        'value': slip.value.value,
        'memo': slip.value.memo ? slip.value.memo : '',
        'old_tgt_date': accountUtils.getYYYYMMDDStr(slipOld.value.tgt_date_obj),
        'old_kind_cd': slipOld.value.kind_cd,
        'old_uuid': slipOld.value.uuid,
        'old_method_cd': slipOld.value.method_cd,
        'old_value': slipOld.value.value
      };
      if (mode === 'del') {
        slipData['tgt_date'] = '';
        slipData['kind_cd'] = '';
        slipData['uuid'] = '';
      }

      await api.postSlip(slipData);
      ElMessage({
        showClose: true,
        message: '登録しました',
        type: 'success',
      });
      context.emit("slipSubmit", mode, slipData);
    };
    watch(slipdata, () => {
      slip.value = accountUtils.cloneSlip(slipdata.value);
      slipOld.value = accountUtils.cloneSlip(slipdata.value);
    });
    return {
      dialogShow,
      balance,
      kindMst,
      payMethodMst,
      saving,
      slip,
      slipOld,
      //
      onDelSubmit,
      onUpdSubmit,
    }
  },
  emits: [
    'slipSubmit',
    'cancelDialog'
  ],
  props: {
    dialogVisible: {
      type: Boolean,
      require: true
    },
    slipdata: {
      type: SlipView,
      require: true
    }
  },
});
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
