<template>
  <div class="inputform">
    <el-form class="input-form" ref="form" :model="slip" label-width="100px">
      <el-form-item class="input-field" label="日付">
        <el-date-picker v-model="slip.tgt_date_obj" type="date" placeholder="Pick a day" />
      </el-form-item>
      <el-form-item class="input-field" label="種類">
        <el-select v-model="slip.kind_cd" placeholder="Select item kind">
          <el-option
            v-for="item in KIND_MST"
            :key="item.kind_cd"
            :label="item.kind_nm"
            :value="item.kind_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item class="input-field" label="支払方法">
        <el-select v-model="slip.method_cd" placeholder="Select payment method">
          <el-option
            v-for="item in PAY_METHOD_MST"
            :key="item.method_cd"
            :label="item.method_nm"
            :value="item.method_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item class="input-field" label="金額">
        <el-input v-model="slip.value" type="number"/>
      </el-form-item>
      <el-form-item class="input-field" label="メモ">
        <el-input v-model="slip.memo" />
      </el-form-item>
      <el-form-item class="input-field" label="id">
        <el-input v-model="slip.uuid" :disabled="true" />
      </el-form-item>
    </el-form>
    <div class="dialog-footer">
      <el-button type="primary" :loading="submiting" @click="onsubmit">登録</el-button>
    </div>
    <p v-loading="balanceloading" class="balancetable">
      <el-table
        :data="balancelist"
        style="display: block; width: 240px; margin: auto;">
        <el-table-column
          prop="method_nm"
          label="種類"
          width="120"
          align="center">
        </el-table-column>
        <el-table-column
          prop="value_fmt"
          label="金額"
          width="120"
          align="center">
        </el-table-column>
      </el-table>
    </p>
  </div>
</template>

<script lang='ts'>
import { defineComponent, computed, ref, onMounted } from 'vue';
import { SlipView, BalanceView } from '@/common/interfaces';
import { ElMessage } from 'element-plus'

import masterdata, { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';
import ApiCalls from '@/common/api';
import { accountUtils, DEF_SLIP } from '@/common/accountUtils';

export default defineComponent({
  name: 'SlipInput',
  setup() {
    const api = new ApiCalls();

    const balance = ref<number>(0);
    const submiting = ref<boolean>(false);
    const slip = ref<SlipView>(accountUtils.cloneSlip(DEF_SLIP));
    const balanceloading = ref<boolean>(false);
    const balancedate = ref<string>('');
    const balancelist = ref<BalanceView[]>([]);

    const onsubmit = async () => {
      submiting.value = true;

      const slipData = {
        'tgt_date': accountUtils.getYYYYMMDDStr(slip.value.tgt_date_obj),
        'kind_cd': slip.value.kind_cd,
        'method_cd': slip.value.method_cd,
        'uuid': slip.value.uuid,
        'value': slip.value.value,
        'memo': slip.value.memo ? slip.value.memo : ''
      };

      try {
        await api.postSlip(slipData);
        initData();
        ElMessage({
          showClose: true,
          message: '登録しました',
          type: 'success',
        });
      } catch (error: any) {
        ElMessage({
          showClose: true,
          message: '登録に失敗しました',
          type: 'error',
        });
      } finally {
        submiting.value = false;
      }
    };
    const initData = async () => {
      // get balance data
      balanceloading.value = true;

      const tgtToDateStr = accountUtils.getYYYYMMDDStr(new Date());
      const balanceList = await api.getBalanceList(tgtToDateStr);
      balancedate.value = accountUtils.getLocalDateStr(tgtToDateStr);
      balancelist.value = balanceList;
      balanceloading.value = false;

      slip.value = accountUtils.cloneSlip(DEF_SLIP);
    };

    onMounted(() => {
      initData();
    });
    return {
      KIND_MST,
      PAY_METHOD_MST,
      //
      balance,
      submiting,
      slip,
      balanceloading,
      balancedate,
      balancelist,
      //
      onsubmit
    }
  }
});
</script>

<style scoped>
.inputform {
  padding : 20px;
}
.balancetable {
  padding : 5px 0px 0px 10px;
}
.input-form {
  margin: auto;
  width: 380px;
}
.input-field {
  width: 300px;
}
</style>
