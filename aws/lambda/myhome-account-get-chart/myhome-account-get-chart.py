import json
import boto3
import decimal
import logging
import datetime
import dateutil.parser
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def get_methodmst():
    _paymethodmst = [
        {'method_cd': 'cash', 'method_nm': '現金', 'display_order': '0'},
        {'method_cd': 'suica', 'method_nm': 'SUICA', 'display_order': '1'},
        {'method_cd': 'nanaco', 'method_nm': 'nanaco', 'display_order': '2'}
    ]
    return _paymethodmst

def get_kindmst():
    wkitems = [
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
        {'kind_cd': 'charge', 'kind_nm': 'チャージ', 'matrix_cd': 'charge', 'account_dir': '2', 'memo': '', 'display_order': '20', 'prc_date': '2019/12/07'}
    ]

    return wkitems

def get_label_chartdata(date_from, date_to):
    labels = []
    wkloop = date_from
    while str(wkloop) <= str(date_to) :
        wkloopstr = wkloop.strftime("%Y%m%d")
        labels.append(wkloopstr)
        wkloop = wkloop + datetime.timedelta(days=1)

    return labels

def get_consume_chartdata(date_from, date_to, date_count):
    slip_table_name = 'account_slip'
    slip_table = dynamodb.Table(slip_table_name)

    datasetslist = []

    # kindmst_table_name = 'account_kind_mst'
    # kindmst_table = dynamodb.Table(kindmst_table_name)
    # kindmstres = kindmst_table.scan()
    kindmstitems = get_kindmst()
    kindmstitems.sort(key=lambda x: x['display_order'])
    kindmstidxmap = {}
    kindmstcdmap = {}
    for kindmstitem in kindmstitems:
        if kindmstitem['account_dir'] != '0':
            continue
        wkdatasets = {}
        wkdatasets['kind_cd'] = kindmstitem['kind_cd']
        wkdatasets['label'] = kindmstitem['kind_nm']
        wkdatasets['data'] = [0] * (date_count + 1)
        wkdatasets['detail'] = [[]] * (date_count + 1)
        wkdatasets['backgroundColor'] = '#000'
        wkkindcd = kindmstitem['kind_cd']

        kindmstidxmap[wkkindcd] = len(datasetslist)
        kindmstcdmap[wkkindcd] = kindmstitem
        datasetslist.append(wkdatasets)

    logger.info("get_consume_chartdata kindmstcdmap: " + json.dumps(kindmstcdmap, indent=0))

    wkloop = date_from
    dateidx = 0
    cdchkmap = {}
    while str(wkloop) <= str(date_to) :
        wkloopstr = wkloop.strftime("%Y%m%d")
        wkres = slip_table.query(KeyConditionExpression=Key('tgt_date').eq(wkloopstr))

        for slip in wkres['Items']:
            wkkindseq = slip['kind_cd_seq'].split('_')
            wkslip = {}
            wkslip['tgt_date'] = slip['tgt_date']
            wkslip['kind_cd'] = wkkindseq[0]
            if wkslip['kind_cd'] not in kindmstcdmap.keys():
                continue
            cdchkmap[wkkindseq[0]] = "true"

            wkkindmst = kindmstcdmap[wkslip['kind_cd']]
            wkkindidx = kindmstidxmap[wkslip['kind_cd']]
            wkdatasets = datasetslist[wkkindidx]
            wkdatasets['data'][dateidx] = wkdatasets['data'][dateidx] + float(slip['value'])

            wkdetail = str(slip['value'])
            if slip['memo'] != ' ':
                wkdetail += '(' + slip['memo'] + ')'

            if wkdatasets['detail'][dateidx] == None or len(wkdatasets['detail'][dateidx]) == 0:
                wkdatasets['detail'][dateidx] = []
            wkdatasets['detail'][dateidx].append(wkdetail)

        wkloop = wkloop + datetime.timedelta(days=1)
        dateidx = dateidx + 1
        
    filtereddatasetlist = []
    for datasets in datasetslist:
        if datasets['kind_cd'] in cdchkmap.keys():
            filtereddatasetlist.append(datasets)

    return filtereddatasetlist

def get_balance_chartdata(date_from, date_to, date_count):
    balance_table_name = 'account_balance'
    balance_table = dynamodb.Table(balance_table_name)

    datasetslist = []

    methodmstitems = get_methodmst()
    methodmstitems.sort(key=lambda x: x['display_order'])
    methodmstidxmap = {}
    methodmstcdmap = {}
    for methodmstitem in methodmstitems:
        wkdatasets = {}
        wkdatasets['method_cd'] = methodmstitem['method_cd']
        wkdatasets['label'] = methodmstitem['method_nm']
        wkdatasets['data'] = [0] * (date_count + 1)
        wkdatasets['borderColor'] = '#000'
        wkmethodcd = methodmstitem['method_cd']

        methodmstidxmap[wkmethodcd] = len(datasetslist)
        methodmstcdmap[wkmethodcd] = methodmstitem
        datasetslist.append(wkdatasets)

    wkloop = date_from
    dateidx = 0
    cdchkmap = {}
    while str(wkloop) <= str(date_to) :
        wkloopstr = wkloop.strftime("%Y%m%d")
        wkres = balance_table.query(KeyConditionExpression=Key('tgt_date').eq(wkloopstr))

        for balance in wkres['Items']:
            wkbalance = {}
            wkbalance['tgt_date'] = balance['tgt_date']
            wkbalance['method_cd'] = balance['method_cd']

            wkmethodmst = methodmstcdmap[wkbalance['method_cd']]
            wkmethodidx = methodmstidxmap[wkbalance['method_cd']]
            wkdatasets = datasetslist[wkmethodidx]
            wkdatasets['data'][dateidx] = wkdatasets['data'][dateidx] + float(balance['value'])

        wkloop = wkloop + datetime.timedelta(days=1)
        dateidx = dateidx + 1

    return datasetslist

def lambda_handler(event, context):
    logger.info("Received event body: " + json.dumps(event, indent=0))

    date_from = None;
    date_to = None;
    date_count = None;
    if 'tgt_date_from' in event and event['tgt_date_from'] != '':
        date_from = dateutil.parser.parse(event['tgt_date_from'])
    if 'tgt_date_to' in event and event['tgt_date_to'] != '':
        date_to = dateutil.parser.parse(event['tgt_date_to'])
    if 'tgt_date_count' in event and event['tgt_date_count'] != '':
        date_count = int(event['tgt_date_count'])

    if (date_from is None) and date_count is not None:
        date_from = date_to - datetime.timedelta(days=date_count - 1)
    elif (date_to is None) and date_count is not None:
        date_to = date_from + datetime.timedelta(days=date_count - 1)
    else:
        date_count = int( (date_to - date_from) / datetime.timedelta(days=1) ) + 1

    chartdata = {}
    chartdata['labels'] = get_label_chartdata(date_from, date_to)
    chartdata['datasets'] = get_consume_chartdata(date_from, date_to, date_count)

    balancechartdata = {}
    balancechartdata['labels'] = get_label_chartdata(date_from, date_to)
    balancechartdata['datasets'] = get_balance_chartdata(date_from, date_to, date_count)
    logger.info("barance_items body: " + json.dumps(balancechartdata, indent=0))

    cahrtOptions = {
        'scales': {
            'xAxes': [{
                'stacked': 'true',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '日付'
                }
            }],
            'yAxes': [{
                'stacked': 'true',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '金額'
                },
                'ticks': {
                    'beginAtZero': 'true',
                    'stepSize': 500
                }
            }]
        }
    }

    balranceCahrtOptions = {
        'scales': {
            'xAxes': [{
                # 'stacked': 'false',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '日付'
                }
            }],
            'yAxes': [{
                # 'stacked': 'false',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '金額'
                },
                'ticks': {
                    'beginAtZero': 'true',
                    'stepSize': 5000
                }
            }]
        }
    }

    chartstruct = {}
    chartstruct['options'] = cahrtOptions
    chartstruct['chartdata'] = chartdata
    chartstruct['balanceoptions'] = balranceCahrtOptions
    chartstruct['balancechartdata'] = balancechartdata
    return chartstruct
