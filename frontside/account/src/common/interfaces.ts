export interface SlipRec {
  'tgt_date': Date;
  'kind_cd': string;
  'method_cd': string;
  'uuid': string;
  'value': number,
  'memo': string;
}

export interface BalanceView {
  'method_nm': string;
  'value_fmt': string;
}
