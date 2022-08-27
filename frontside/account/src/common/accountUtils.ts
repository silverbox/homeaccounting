import masterdata, { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';

import { SlipView } from '@/common/interfaces';

export default class AccountUtils {
  getYYYYMMDDStr = (dateObj: Date): string => {
    const YYYY = dateObj.getFullYear()
    // 「月」を取得する
    const MM = dateObj.getMonth() + 1
    // 「日」を取得する
    const DD = dateObj.getDate()
    const yStr = String(YYYY)
    const mStr = (MM >= 10 ? '' : '0') + String(MM)
    const dStr = (DD >= 10 ? '' : '0') + String(DD)
    return yStr + mStr + dStr
  };
  getLocalDateStr = (yyyyMMddStr: string): string => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2))
    const dd = Number(yyyyMMddStr.substr(6, 2))
    // var dateObj = new Date(yy, mm, dd)
    return yy + ' / ' + mm + ' / ' + dd
  };
  getLocalDate = (yyyyMMddStr: string): Date => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2)) - 1
    const dd = Number(yyyyMMddStr.substr(6, 2))
    return new Date(yy, mm, dd)
  };
  cloneSlip = (orgSlipView: SlipView): SlipView => {
    const tgtDateObj = new Date(orgSlipView.tgt_date_obj.getTime());
    const slipView: SlipView = {
      tgt_date_obj: tgtDateObj,
      tgt_date_str: this.getLocalDateStr(this.getYYYYMMDDStr(tgtDateObj)),
      kind_nm: masterdata.getKindNm(orgSlipView.kind_cd),
      method_nm: masterdata.getMethodNm(orgSlipView.method_cd),
      value_fmt: Number(orgSlipView.value).toLocaleString(),
      kind_cd: orgSlipView.kind_cd,
      method_cd: orgSlipView.method_cd,
      uuid: orgSlipView.uuid,
      value: orgSlipView.value,
      memo: orgSlipView.memo
    }
    return slipView;
  };
  convertMapToSlipView = (orgSlipMap: {[key: string]: string }): SlipView => {
    const tgtDateObj = this.getLocalDate(orgSlipMap['tgt_date']);
    return {
      kind_cd: orgSlipMap['kind_cd'],
      method_cd: orgSlipMap['method_cd'],
      uuid: orgSlipMap['uuid'],
      value: Number(orgSlipMap['value']),
      memo: orgSlipMap['memo'],
      //
      tgt_date_obj: tgtDateObj,
      tgt_date_str: this.getLocalDateStr(this.getYYYYMMDDStr(tgtDateObj)),
      kind_nm: masterdata.getKindNm(orgSlipMap['kind_cd']),
      method_nm: masterdata.getMethodNm(orgSlipMap['method_cd']),
      value_fmt: Number(orgSlipMap['value']).toLocaleString()
    }
  };
}
export const accountUtils = new AccountUtils();
export const DEF_SLIP: SlipView = {
  tgt_date_obj: new Date(),
  tgt_date_str: accountUtils.getLocalDateStr(accountUtils.getYYYYMMDDStr(new Date())),
  kind_nm: masterdata.getKindNm(KIND_MST[0].kind_cd),
  method_nm: masterdata.getMethodNm(PAY_METHOD_MST[0].method_cd),
  value_fmt: '',
  kind_cd: KIND_MST[0].kind_cd,
  method_cd: PAY_METHOD_MST[0].method_cd,
  uuid: '',
  value: 0,
  memo: ''
};
