<template>
  <div class="inputform">
    <el-form ref="form" :model="slip" label-width="100px">
      <el-form-item label="日付">
        <el-date-picker v-model="slip.tgt_date" type="date" placeholder="Pick a day" />
      </el-form-item>
      <el-form-item label="種類">
        <el-select v-model="slip.kind_cd" placeholder="Select item kind">
          <el-option
            v-for="item in KIND_MST"
            :key="item.kind_cd"
            :label="item.kind_nm"
            :value="item.kind_cd">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="支払方法">
        <el-select v-model="slip.method_cd" placeholder="Select payment method">
          <el-option
            v-for="item in PAY_METHOD_MST"
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

<script lang='ts'>
import { defineComponent, computed, ref, onMounted } from 'vue';
import { SlipRec, BalanceView } from '@/common/interfaces';
import api from '@/common/api';

import masterdata, { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';
import myutils from '@/common/myutils';
console.log(masterdata.getKindNm('magazine'));
console.log(myutils.getYYYYMMDDStr(new Date()));

const slipDef: SlipRec = {
  tgt_date: new Date(),
  kind_cd: KIND_MST[0].kind_cd,
  method_cd: PAY_METHOD_MST[0].method_cd,
  uuid: '',
  value: 0,
  memo: ''
};

export default defineComponent({
  name: 'SlipInput',
  setup() {
    const balance = ref<number>(0);
    const submiting = ref<boolean>(false);
    const slip = ref<SlipRec>(slipDef);
    const balanceloading = ref<boolean>(false);
    const balancedate = ref<string>('');
    const balancelist = ref<BalanceView[]>([]);

    const onsubmit = () => {
      console.log('slip-data1:' + slip.value.method_cd + ':' + slip.value.uuid);
      submiting.value = true;

      const slipdata = {
        'tgt_date': slip.value.tgt_date,
        'kind_cd': slip.value.kind_cd,
        'method_cd': slip.value.method_cd,
        'uuid': slip.value.uuid,
        'value': slip.value,
        'memo': slip.value.memo ? slip.value.memo : ''
      };

      // var self = this
      // this.$cognito.callPostApi(this.$axios, this.apienv.baseendpoint + 'slip', slipdata).then(
      //   response => {
      //     console.log(response.data)
      //     self.$message({message: '登録しました', type: 'success'})
      //     self.initData()
      //     self.submiting = false
      //   }
      // ).catch(err => {
      //   self.$message({message: err, type: 'error'})
      //   self.submiting = false
      // })
      submiting.value = false;
    };
    const initData = async () => {
      // get balance data
      balanceloading.value = true;

      const tgtToDateStr = myutils.getYYYYMMDDStr(new Date());
      const balanceList = await api.getBalanceList(tgtToDateStr);
      // this.$cognito.callGetApi(that.$axios, that.apienv.baseendpoint + 'balance?' + prmstr).then(
      //   response => {
      //     that.finload(that, response)
      //     this.balanceloading = false
      //   }
      // ).catch(err => {
      //   that.$message({message: err, type: 'error'})
      //   this.balanceloading = false
      // })
      balanceloading.value = false;
    };
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const finload = (response: any) => {
      var wkDateStr = ''
      var wkBalanceList = []
      for (var resdata of response.data) {
        wkDateStr = myutils.getLocalDateStr(resdata['tgt_date'])
        const wkBalance: BalanceView = {
          method_nm: masterdata.getMethodNm(resdata['method_cd']),
          value_fmt: Number(resdata['value']).toLocaleString()
        }
        wkBalanceList.push(wkBalance)
      }
      balancedate.value = wkDateStr
      balancelist.value = wkBalanceList
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
      onsubmit,
      finload
    }
  }
});
</script>

<style scoped>
.inputform{
  padding : 20px;
}
.balancetable{
  padding : 5px 0px 0px 10px;
}
</style>
