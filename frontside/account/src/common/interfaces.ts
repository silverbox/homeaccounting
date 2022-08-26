import { KIND_MST, PAY_METHOD_MST } from '@/const/masterdata';

export interface SlipRec {
  'tgt_date': Date;
  'kind_cd': string;
  'method_cd': string;
  'uuid': string;
  'value': number;
  'memo': string;
}

export interface BalanceView {
  'method_nm': string;
  'value_fmt': string;
}

export interface SlipView {
  'uuid': string;
  'tgt_date': Date;
  'tgt_date_obj': Date;
  'tgt_date_str': string;
  'kind_cd': string;
  'kind_nm': string;
  'method_cd': string;
  'method_nm': string;
  'value': number;
  'value_fmt': string;
  'memo': string;
}

export const DEF_SLIP: SlipRec = {
  tgt_date: new Date(),
  kind_cd: KIND_MST[0].kind_cd,
  method_cd: PAY_METHOD_MST[0].method_cd,
  uuid: '',
  value: 0,
  memo: ''
};