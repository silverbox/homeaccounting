interface KindMstRec {
  kind_cd: string;
  kind_nm: string;
  matrix_cd: string;
  account_dir: string;
  memo: string;
  display_order: string;
  prc_date: string;
}

export const KIND_MST: KindMstRec[] = [
  {'kind_cd': 'food01', 'kind_nm': '通常食費', 'matrix_cd': 'food01', 'account_dir': '0', 'memo': '日常の食費。外食は含まず', 'display_order': '1', 'prc_date': '2005/05/24'},
  {'kind_cd': 'food02', 'kind_nm': '特別食費', 'matrix_cd': 'food02', 'account_dir': '0', 'memo': '外食などの贅沢食事', 'display_order': '2', 'prc_date': '2005/05/24'},
  {'kind_cd': 'magazine', 'kind_nm': '雑誌', 'matrix_cd': 'text', 'account_dir': '0', 'memo': '', 'display_order': '3', 'prc_date': '2005/05/24'},
  {'kind_cd': 'book', 'kind_nm': '書籍', 'matrix_cd': 'text', 'account_dir': '0', 'memo': '', 'display_order': '4', 'prc_date': '2005/05/24'},
  {'kind_cd': 'newspaper', 'kind_nm': '新聞代', 'matrix_cd': 'text', 'account_dir': '0', 'memo': '', 'display_order': '5', 'prc_date': '2005/06/30'},
  {'kind_cd': 'living', 'kind_nm': '生活費', 'matrix_cd': 'life', 'account_dir': '0', 'memo': '', 'display_order': '6', 'prc_date': '2005/05/24'},
  {'kind_cd': 'medical', 'kind_nm': '医療関係', 'matrix_cd': 'life', 'account_dir': '0', 'memo': '', 'display_order': '7', 'prc_date': '2005/07/02'},
  {'kind_cd': 'baby', 'kind_nm': '子供関係', 'matrix_cd': 'life', 'account_dir': '0', 'memo': '赤ちゃん用品など', 'display_order': '8', 'prc_date': '2005/06/26'},
  {'kind_cd': 'car', 'kind_nm': '車', 'matrix_cd': 'special', 'account_dir': '0', 'memo': '車関係出費', 'display_order': '9', 'prc_date': '2005/06/12'},
  {'kind_cd': 'aikido', 'kind_nm': '合気道', 'matrix_cd': 'enjoing', 'account_dir': '0', 'memo': '合気道関係出費', 'display_order': '10', 'prc_date': '2005/06/12'},
  {'kind_cd': 'hobby', 'kind_nm': '趣味', 'matrix_cd': 'enjoing', 'account_dir': '0', 'memo': '', 'display_order': '11', 'prc_date': '2005/05/24'},
  {'kind_cd': 'dating', 'kind_nm': 'デート', 'matrix_cd': 'enjoing', 'account_dir': '0', 'memo': '', 'display_order': '12', 'prc_date': '2005/05/24'},
  {'kind_cd': 'social', 'kind_nm': '交際費', 'matrix_cd': 'social', 'account_dir': '0', 'memo': '', 'display_order': '13', 'prc_date': '2005/05/24'},
  {'kind_cd': 'etc', 'kind_nm': 'その他', 'matrix_cd': 'etc', 'account_dir': '0', 'memo': '', 'display_order': '14', 'prc_date': '2005/05/24'},
  {'kind_cd': 'special', 'kind_nm': '特別出費', 'matrix_cd': 'special', 'account_dir': '0', 'memo': '', 'display_order': '15', 'prc_date': '2005/05/24'},
  {'kind_cd': 'tax', 'kind_nm': '税金', 'matrix_cd': 'special', 'account_dir': '0', 'memo': '各種税金。特別出費か。', 'display_order': '16', 'prc_date': '2005/05/24'},
  {'kind_cd': 'gift', 'kind_nm': 'お祝い金', 'matrix_cd': 'income', 'account_dir': '1', 'memo': '親からもらったものなど', 'display_order': '17', 'prc_date': '2005/06/26'},
  {'kind_cd': 'sell', 'kind_nm': '物品売却', 'matrix_cd': 'income', 'account_dir': '1', 'memo': 'オークションその他', 'display_order': '18', 'prc_date': '2005/05/24'},
  {'kind_cd': 'withdrow', 'kind_nm': '銀行引出', 'matrix_cd': 'income', 'account_dir': '1', 'memo': '', 'display_order': '19', 'prc_date': '2005/05/24'},
  {'kind_cd': 'charge', 'kind_nm': '現金チャージ', 'matrix_cd': 'charge', 'account_dir': '2', 'memo': '', 'display_order': '20', 'prc_date': '2019/12/07'},
  {'kind_cd': 'bankcharge', 'kind_nm': '非現金チャージ', 'matrix_cd': 'charge', 'account_dir': '3', 'memo': '', 'display_order': '21', 'prc_date': '2019/12/07'}
];

const _kindmap: {[key:string] : KindMstRec} = {};
for (const kind of KIND_MST) {
  _kindmap[kind.kind_cd] = kind
}

interface MethodMstRec {
  method_cd: string;
  method_nm: string;
}

export const PAY_METHOD_MST: MethodMstRec[] = [
  {'method_cd': 'cash', 'method_nm': '現金'},
  {'method_cd': 'suica', 'method_nm': 'SUICA'},
  {'method_cd': 'nanaco', 'method_nm': 'nanaco'},
  {'method_cd': 'paypay', 'method_nm': 'PayPay'}
];

const _methodmap: {[key:string] : MethodMstRec} = {};
for (const method of PAY_METHOD_MST) {
  _methodmap[method.method_cd] = method
}

const masterdata = {
  getKindNm: (kindCd: string): string => {
    return _kindmap[kindCd].kind_nm;
  },
  getMethodNm: (methodCd: string): string => {
    return _methodmap[methodCd].method_nm;
  }
};
export default masterdata;
