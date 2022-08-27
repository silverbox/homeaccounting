<template>
  <div class="listviewform">
    <div>
      <span>Target date</span>
      <el-date-picker v-model="tgtdate" type="date" @change="reload" placeholder="Pick a day" />
    </div>
    <div class="infinite-list-wrapper" style="overflow:auto">
      <div
        class="listview"
        v-infinite-scroll="loadMore"
        infinite-scroll-disabled="disabled">
        <div class="slip-header">
          <div class="slip-val-elem slip-w-mid ">日付</div>
          <div class="slip-val-elem slip-w-mid ">種類</div>
          <div class="slip-val-elem slip-w-mid ">支払方法</div>
          <div class="slip-val-elem slip-w-num-h ">金額</div>
          <div class="slip-val-elem ">メモ</div>
        </div>
        <div v-for="(item, index) in slipViewList" class="slip-item" :key="index" @click="slipedit(item.uuid)">
          <div class="slip-val-elem slip-w-mid ">{{ item.tgt_date_str }}</div>
          <div class="slip-val-elem slip-w-mid ">{{ item.kind_nm }}</div>
          <div class="slip-val-elem slip-w-mid ">{{ item.method_nm }}</div>
          <div class="slip-val-elem slip-w-num ">{{ item.value_fmt }}</div>
          <div class="slip-val-elem ">{{ item.memo }}</div>
        </div>
      </div>
      <p v-if="loading" v-loading="loading">
        <span>Loading {{ loaddatecnt }} days before from </span>
        <el-date-picker v-model="wkdate" type="date" :readonly="true" />
      </p>
      <p v-if="noMore">Limit over(100 records or 33 days)</p>
    </div>
  </div>
  <SlipInputDlg
    v-bind:dialogVisible="dialogVisible"
    v-bind:slipdata="dialogSlip"
    v-on:slipSubmit="onSlipSubmit"
    v-on:cancelDialog="onSlipCancel"
  ></SlipInputDlg>
</template>

<script lang='ts'>
import { defineComponent, computed, ref, getCurrentInstance } from 'vue';
import { SlipView, BalanceView } from '@/common/interfaces';
import SlipInputDlg from '@/components/SlipInputDlg.vue';
import { accountUtils, DEF_SLIP } from '@/common/accountUtils';
import masterdata, { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';
import ApiCalls from '@/common/api';

const LOAD_DATE_CNT = 3
const LOAD_LIMIT_DATE = 31
const LOAD_LIMIT_REC = 100

export default {
  name: 'SlipList',
  setup(props: any, context: any) {
    const instance = getCurrentInstance();
    const api = new ApiCalls();
    //
    const tgtdate = ref<Date>(new Date());
    const slipViewList = ref<SlipView[]>([]);
    const loading = ref<boolean>(false);
    const loaddatecnt = ref<number>(LOAD_DATE_CNT);
    const loadeddatecnt = ref<number>(0);
    const dlgeditidx = ref<number>(-1);
    const wkdate = ref<Date>(new Date());
    //
    const dialogSlip = ref<SlipView>(DEF_SLIP);
    const dialogVisible = ref<boolean>(false);

    const count = computed(() => {
      return slipViewList.value.length;
    });
    const noMore = computed(() => {
      return slipViewList.value.length >= LOAD_LIMIT_REC || loadeddatecnt.value >= LOAD_LIMIT_DATE;
    });
    const disabled = computed(() => {
      return loading.value || noMore.value;
    });

    const slipedit = (uuid: string) => {
      for (const slipView of slipViewList.value) {
        if (slipView.uuid == uuid) {
          dialogSlip.value = slipView;
          dialogVisible.value = true;
          return;
        }
      }
    };
    const onSlipSubmit = (mode: string, newSlipData: {[key: string]: any}) => {
      if (mode === 'upd') {
        slipViewList.value.forEach((slipView, index) => {
          if (slipView.uuid == newSlipData.uuid) {
            slipViewList.value[index] = accountUtils.convertMapToSlipView(newSlipData);
            return;
          }
        });
        if (instance != null && instance.proxy != null) instance.proxy.$forceUpdate();
      } else {
        slipViewList.value.splice(dlgeditidx.value, 1);
      }
      dialogVisible.value = false;
    };
    const onSlipCancel = () => {
      dialogVisible.value = false;
    };
    const loadMore = () => {
      if (!loading.value) {
        loadsub();
      }
    };
    const loadsub = async () => {
      loading.value = true;
      const tgtToDateStr = accountUtils.getYYYYMMDDStr(wkdate.value);
      wkdate.value.setDate(wkdate.value.getDate() + 1 - LOAD_DATE_CNT);
      const tgtFromDateStr = accountUtils.getYYYYMMDDStr(wkdate.value);

      const newSlipViewList = await api.getSlipViewList(tgtToDateStr, tgtFromDateStr);
      Array.prototype.push.apply(slipViewList.value, newSlipViewList);
      wkdate.value.setDate(wkdate.value.getDate() - 1);
      loading.value = false;
      loadeddatecnt.value += loaddatecnt.value;
    };
    const reload = () => {
      if (!loading.value) {
        loading.value = true;
        wkdate.value = new Date(tgtdate.value);
        slipViewList.value = [];
        loadeddatecnt.value = 0;
        loading.value = false;
        loadMore();
      }
    };

    return {
      tgtdate,
      slipViewList,
      loading,
      loaddatecnt,
      loadeddatecnt,
      dlgeditidx,
      wkdate,
      dialogSlip,
      dialogVisible,
      //
      count,
      noMore,
      disabled,
      //
      onSlipSubmit,
      onSlipCancel,
      slipedit,
      loadMore,
      reload
    }
  },
  components: {
    SlipInputDlg
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .listview .slip-item {
    align-items: center;
    margin: 10px;
    text-align: left;
    border-bottom: solid 1px #E0E0E0;
  }
  .listview .slip-header {
    align-items: center;
    margin: 10px;
    text-align: left;
    margin-bottom: 3px;
    font-weight: bold;
    font-color: #1f1f1f;
    border-bottom: solid 1px #202020;
  }
  .listviewform{
    padding : 20px;
  }

  .slip-w-icon {
    width: 40px;
    text-align: center;
  }
  .slip-w-mid {
    width: 120px;
    text-align: center;
  }
  .slip-w-num {
    width: 80px;
    text-align: right;
  }
  .slip-w-num-h {
    width: 80px;
    text-align: center;
  }
  .slip-val-elem {
    display: inline-block;
    vertical-align: top;
    height: 20px;
    margin: 5px;
  }
</style>
