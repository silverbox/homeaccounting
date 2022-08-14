import axios from 'axios';
import { BalanceView } from '@/common/interfaces';
import masterdata from '@/const/masterdata';
// import myutils from '@/common/myutils';

const API_BASE_URL = (process.env.VUE_APP_API_BASE_URL as string);

export default {
  getBalanceList: async (tgtDate: string): Promise<BalanceView[]> => {
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'dummy' // session.getIdToken().getJwtToken()
      },
      data: {}
    }
    console.log(`${API_BASE_URL}/balance?tgt_date=${tgtDate}`);
    return await axios.get(`${API_BASE_URL}/balance?tgt_date=${tgtDate}`, config).then(
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (response: any) => {
        const wkBalanceList: BalanceView[] = [];
        for (const resdata of response.data) {
          const wkBalance: BalanceView = {
            method_nm: masterdata.getMethodNm(resdata['method_cd']),
            value_fmt: Number(resdata['value']).toLocaleString()
          }
          wkBalanceList.push(wkBalance);
        }
        return wkBalanceList;
      },
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (error: any) => {
        throw error;
      }
    );
  }
}