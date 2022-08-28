/* eslint-disable @typescript-eslint/no-explicit-any */
import { useAuthenticator } from '@aws-amplify/ui-vue';
import { CognitoUserSession } from 'amazon-cognito-identity-js';
import axios from 'axios';
import { BalanceView, SlipView } from '@/common/interfaces';
import masterdata from '@/const/masterdata';
import { accountUtils } from '@/common/accountUtils';

const API_BASE_URL = (process.env.VUE_APP_API_BASE_URL as string);

export default class ApiCalls {
  /**
   * inner common method
   */
  _getMergedConfig = (config: {[key:string]: any}, jwtToken: string): {[key:string]: any} => {
    const addHeaders = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`
    };
    const newHeaders = config['headers'] ? {
      ...config['headers'],
      ...addHeaders
    } : addHeaders;
    return {
      ...config,
      'headers': newHeaders
    };
  };
  _callGetApi = async (url: string, config: {[key:string]: any}, callback: any): Promise<any> => {
    const auth = useAuthenticator();
    auth.user.getSession(async (error: Error, session: CognitoUserSession) => {
      if (error != null) {
        throw error;
      }
      const mergedConfig = this._getMergedConfig(config, session.getIdToken().getJwtToken());
      const response = await axios.get(url, mergedConfig);
      return callback(response);
    });
  };
  _callPostApi = async (url: string, config: {[key:string]: any}, data: {[key:string]: any}, callback: any): Promise<any> => {
    const auth = useAuthenticator();
    auth.user.getSession(async (error: Error, session: CognitoUserSession) => {
      if (error != null) {
        throw error;
      }
      const mergedConfig = this._getMergedConfig(config, session.getIdToken().getJwtToken());
      const response = await axios.post(url, data, mergedConfig);
      return callback(response);
    });
  };

  /*
   * business method
   */

  getBalanceList = async (tgtDate: string): Promise<BalanceView[]> => {
    return new Promise(resolve => {
      const url = `${API_BASE_URL}/balance?tgt_date=${tgtDate}`;
      this._callGetApi(url, {}, (response: any) => {
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

  getSlipViewList = async (tgtToDateStr: string, tgtFromDateStr: string): Promise<SlipView[]> => {
    return new Promise(resolve => {
      const url = `${API_BASE_URL}/slip?tgt_date_to=${tgtToDateStr}&tgt_date_from=${tgtFromDateStr}`;
      this._callGetApi(url, {}, (response: any) => {
        const wkSlipList: SlipView[] = [];
        for (const resdata of response.data) {
          wkSlipList.push(accountUtils.convertMapToSlipView(resdata));
        }
        resolve(wkSlipList);
      });
    });
  };

  postSlip = async (slipData: {[key:string]: any}): Promise<boolean> => {
    return new Promise(resolve => {
      const url = `${API_BASE_URL}/slip`;
      this._callPostApi(url, {}, slipData, (response: any) => {
        resolve(response);
      });
    });
  };

  getChartDataResponse = async (tgtToDateStr: string, loadDateCount: number): Promise<any> => {
    return new Promise(resolve => {
      const url = `${API_BASE_URL}/chart?tgt_date_to=${tgtToDateStr}&tgt_date_count=${loadDateCount}`;
      this._callGetApi(url, {}, (response: any) => {
        resolve(response.data);
      });
    });
  };
}