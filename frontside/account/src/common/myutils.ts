import myutils from '@/common/myutils';
import masterdata from '@/const/masterdata';
import { SlipRec, SlipView } from '@/common/interfaces';

export default {
  getYYYYMMDDStr: (dateObj: Date): string => {
    const YYYY = dateObj.getFullYear()
    // 「月」を取得する
    const MM = dateObj.getMonth() + 1
    // 「日」を取得する
    const DD = dateObj.getDate()
    const yStr = String(YYYY)
    const mStr = (MM >= 10 ? '' : '0') + String(MM)
    const dStr = (DD >= 10 ? '' : '0') + String(DD)
    return yStr + mStr + dStr
  },
  getLocalDateStr: (yyyyMMddStr: string): string => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2))
    const dd = Number(yyyyMMddStr.substr(6, 2))
    // var dateObj = new Date(yy, mm, dd)
    return yy + ' / ' + mm + ' / ' + dd
  },
  getLocalDate: (yyyyMMddStr: string): Date => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2)) - 1
    const dd = Number(yyyyMMddStr.substr(6, 2))
    return new Date(yy, mm, dd)
  },
  cloneSlip: (orgSlip: SlipRec): SlipRec => {
    return {
      tgt_date: new Date(orgSlip['tgt_date'].getTime()),
      kind_cd: orgSlip['kind_cd'],
      method_cd: orgSlip['method_cd'],
      uuid: orgSlip['uuid'],
      value: orgSlip['value'],
      memo: orgSlip['memo']
    }
  },
  getSlipView: (orgSlip: {[key: string]: any }): SlipView => {
    return {
      tgt_date: myutils.getLocalDate(orgSlip['tgt_date']),
      kind_cd: orgSlip['kind_cd'],
      method_cd: orgSlip['method_cd'],
      uuid: orgSlip['uuid'],
      value: orgSlip['value'],
      memo: orgSlip['memo'],
      //
      tgt_date_obj: myutils.getLocalDate(orgSlip['tgt_date']),
      tgt_date_str: myutils.getLocalDateStr(orgSlip['tgt_date']),
      kind_nm: masterdata.getKindNm(orgSlip['kind_cd']),
      method_nm: masterdata.getMethodNm(orgSlip['method_cd']),
      value_fmt: Number(orgSlip['value']).toLocaleString()
    }
  }
}
