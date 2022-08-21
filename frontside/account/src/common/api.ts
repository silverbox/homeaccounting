import { useAuthenticator } from '@aws-amplify/ui-vue';
import { CognitoUserSession } from 'amazon-cognito-identity-js';
import axios from 'axios';
import { BalanceView } from '@/common/interfaces';
import masterdata from '@/const/masterdata';
// import myutils from '@/common/myutils';

const API_BASE_URL = (process.env.VUE_APP_API_BASE_URL as string);

export default class ApiCalls {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  callGetApi = async (url: string, config: {[key:string]: any}, callback: any): Promise<any> => {
    const auth = useAuthenticator();
    auth.user.getSession(async (error: Error, session: CognitoUserSession) => {
      if (error != null) {
        throw error;
      }
      const addHeaders = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.getIdToken().getJwtToken()}`
      };
      const newHeaders = config['headers'] ? {
        ...config['headers'],
        ...addHeaders
      } : addHeaders;
      const newConfig = {
        ...config,
        'headers': newHeaders
      };
      const response = await axios.get(url, newConfig);
      return callback(response);
    });
  };

  getBalanceList = async (tgtDate: string): Promise<BalanceView[]> => {
    return new Promise(resolve => {
      const url = `${API_BASE_URL}/balance?tgt_date=${tgtDate}`;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      this.callGetApi(url, { data: {}}, (response: any) => {
        const wkBalanceList: BalanceView[] = [];
        for (const resdata of response.data) {
          const wkBalance: BalanceView = {
            method_nm: masterdata.getMethodNm(resdata['method_cd']),
            value_fmt: Number(resdata['value']).toLocaleString()
          }
          wkBalanceList.push(wkBalance);
        }
        resolve(wkBalanceList);
      });
    });
  };
}