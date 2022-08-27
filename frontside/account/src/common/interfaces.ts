
export interface BalanceView {
  'method_nm': string;
  'value_fmt': string;
}

export interface SlipView {
  'uuid': string;
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
