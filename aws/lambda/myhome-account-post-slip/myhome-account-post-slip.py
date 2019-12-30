import json
import boto3
import logging
import datetime
import dateutil.parser
import uuid
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TBL_SLIP = 'account_slip'
TBL_BALANCE = 'account_balance'
SAFECNT = 50

ACCOUNT_DIR_CONSUME = '0'
ACCOUNT_DIR_INCOME = '1'
ACCOUNT_DIR_CHARGE = '2'
JST_OFFSET_HOURS = 9

def convert_dynamodata_to_map(dynamodatalist):
    retlist = []
    for dynamodata in dynamodatalist:
        onedata = {}
        wkitem = dynamodata['Item']
        for key in wkitem.keys():
            valobj = wkitem[key]
            for typkey in valobj.keys():
                if typkey == 'N':
                    onedata[key] = int(valobj[typkey])
                else:
                    onedata[key] = valobj[typkey]
        retlist.append(onedata)

    return retlist

def get_jst_from_utc(utcdate):
    return utcdate + datetime.timedelta(hours=JST_OFFSET_HOURS)
    
# ##
# # tgtDate: the YYYYMMDD format DateString recalc start. base balance will be 1 day before of the date.
# #
# def get_last_balance(tgtDate):
#     SAFECNT = 50
#     date_to = dateutil.parser.parse(tgtDate) + datetime.timedelta(days=-1)

#     balanncetable = dynamodb.Table('account_balance')
#     wkres = balanncetable.query(KeyConditionExpression=Key('tgt_date').eq(date_to.strftime("%Y%m%d")))
#     wkitems = wkres['Items']

#     wkchk = 0
#     wkloop = date_to
#     while len(wkitems) == 0 and wkchk <= SAFECNT :
#         wkloop = wkloop + datetime.timedelta(days=-1)
#         wkres = balanncetable.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
#         wkitems = wkres['Items']
#         SAFECNT += 1

#     balacemap = {}
#     for wk_balance in wkitems:
#         balacemap[wk_balance['method_cd']] = wk_balance['value']

#     logger.debug("get_last_balance: " + str(len(wkitems)) + ':' + wkloop.strftime("%Y%m%d"))
#     retitem = {}
#     retitem['balanceitemmap'] = balacemap
#     retitem['balancedate'] = wkloop
#     return retitem

# def update_balance(tgtDate, balancemap):
#     balanncetable = dynamodb.Table('account_balance')
#     wkDateStr = tgtDate.strftime("%Y%m%d")
#     logger.debug("update_balance: " + wkDateStr)
#     with balanncetable.batch_writer() as batch:
#         for wk_method_cd in balancemap.keys():
#             balanceItem = {
#                 "tgt_date" : wkDateStr,
#                 "method_cd" : wk_method_cd,
#                 "value" : balancemap[wk_method_cd]
#             }
#             batch.put_item(Item=balanceItem)

# ##
# # date_from: the YYYYMMDD format string recalc start. base balance will be 1 day before of the date.
# #
# def recalc_balance(date_from):
#     basebalance = get_last_balance(date_from)
#     new_date_from = basebalance['balancedate'] + datetime.timedelta(days=1)
#     balancemap = basebalance['balanceitemmap']
#     kindmstmap = get_kindmstmap()

#     sliptable = dynamodb.Table('account_slip')
#     dt_now = get_jst_from_utc(datetime.datetime.now())

#     wkloop = new_date_from
#     while str(wkloop) <= str(dt_now) :
#         wkres = sliptable.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
#         for slip in wkres['Items']:
#             wkkindseq = slip['kind_cd_seq'].split('_')
#             wkkindcd = wkkindseq[0]
#             wkmethodcd = slip['method_cd']
#             wkkindmst = kindmstmap[wkkindcd]
#             wkbalance = balancemap[wkmethodcd]
#             logger.info("recalc_balance: " + str(Decimal(slip['value'])))

#             if wkkindmst['account_dir'] == ACCOUNT_DIR_CHARGE:
#                 balancemap['cash'] -= Decimal(slip['value'])
#                 balancemap[wkmethodcd] += Decimal(slip['value'])
#             elif wkkindmst['account_dir'] == ACCOUNT_DIR_INCOME:
#                 balancemap[wkmethodcd] += Decimal(slip['value'])
#             else:
#                 balancemap[wkmethodcd] -= Decimal(slip['value'])
#         update_balance(wkloop, balancemap)
#         wkloop = wkloop + datetime.timedelta(days=1)

def get_kindmstmap():
    # table_name = 'account_kind_mst'
    # dynamotable = dynamodb.Table(table_name)
    # dbres = dynamotable.scan()
    # wkitems = dbres['Items']
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
    kindmstmap = {}
    for wk_kindmst in wkitems:
        kindmstmap[wk_kindmst['kind_cd']] = wk_kindmst

    return kindmstmap

def get_memostr(bodyParam):
    memostr = bodyParam['memo']
    if memostr is None or memostr == "":
        memostr = " "
    return memostr

def get_insitemobj(bodyParam):
    return {
        "tgt_date": { "S": bodyParam['tgt_date'] },
        "kind_cd_seq": { "S": bodyParam['kind_cd'] + "_" + str(uuid.uuid4()) },
        "method_cd": { "S": bodyParam['method_cd'] },
        "value": { "N": str(bodyParam['value']) },
        "memo" : { "S": get_memostr(bodyParam) }
    }

def get_delupdkeyobj(bodyParam):
    oldtgtdate = bodyParam['old_tgt_date']
    oldkindseq = bodyParam['old_kind_cd'] + "_" + bodyParam['old_uuid']
    return {
        "tgt_date": { "S": oldtgtdate },
        "kind_cd_seq": { "S": oldkindseq }
    }

def get_attrnameobj():
    return {
        '#tgt_date' : 'tgt_date',
        '#kind_cd_seq' : 'kind_cd_seq',
        '#value' : 'value'
    }

def get_ins_tr_slipitems(bodyParam):
    retlist = []
    insitem = {
        'Put': {
            'TableName': TBL_SLIP,
            'Item': get_insitemobj(bodyParam),
            'ConditionExpression': 'attribute_not_exists(tgt_date) and attribute_not_exists(kind_cd_seq)'
        }
    }
    retlist.append(insitem)
    return retlist

def get_del_tr_slipitems(bodyParam):
    oldtgtdate = bodyParam['old_tgt_date']
    oldkindseq = bodyParam['old_kind_cd'] + "_" + bodyParam['old_uuid']
    oldval = bodyParam['old_value']
    retlist = []
    delitem = {
        'Delete': {
            'TableName': TBL_SLIP,
            'Key': get_delupdkeyobj(bodyParam),
            'ConditionExpression': '#tgt_date = :tgt and #kind_cd_seq = :kindseq and #value = :befval',
            'ExpressionAttributeNames' : get_attrnameobj(),
            'ExpressionAttributeValues': {
                ':tgt': {'S': oldtgtdate},
                ':kindseq': {'S': oldkindseq },
                ':befval': {'N': str(oldval) }
            }
        }
    }
    retlist.append(delitem)
    return retlist

def get_upd_tr_slipitems(bodyParam):
    retlist = []
    oldtgtdate = bodyParam['old_tgt_date']
    oldkindseq = bodyParam['old_kind_cd'] + "_" + bodyParam['old_uuid']
    oldval = bodyParam['old_value']
    newval = bodyParam['value']
    if bodyParam['tgt_date'] != oldtgtdate or bodyParam['kind_cd'] != bodyParam['old_kind_cd'] or bodyParam['old_uuid'] != bodyParam['uuid']:
        insitem = {
            'Put': {
                'TableName': TBL_SLIP,
                'Item': get_insitemobj(bodyParam),
                'ConditionExpression': 'attribute_not_exists(tgt_date) and attribute_not_exists(kind_cd_seq)'
            }
        }
        delitem = {
            'Delete': {
                'TableName': TBL_SLIP,
                'Key': get_delupdkeyobj(bodyParam),
                'ConditionExpression': '#tgt_date = :tgt and #kind_cd_seq = :kindseq and #value = :befval',
                'ExpressionAttributeNames' : get_attrnameobj(),
                'ExpressionAttributeValues': {
                    ':tgt': {'S': oldtgtdate},
                    ':kindseq': {'S': oldkindseq },
                    ':befval': {'N': str(oldval) }
                }
            }
        }
        retlist.append(insitem)
        retlist.append(delitem)
    else:
        wkattrname = get_attrnameobj()
        wkattrname['#method_cd'] = 'method_cd'
        wkattrname['#memo'] = 'memo'
        upditem = {
            'Update': {
                'TableName': TBL_SLIP,
                'Key': get_delupdkeyobj(bodyParam),
                'ConditionExpression': '#tgt_date = :tgt and #kind_cd_seq = :kindseq and #value = :befval',
                'UpdateExpression': 'SET #value = :aftval, #method_cd = :method_cd, #memo = :memo',
                'ExpressionAttributeNames' : wkattrname,
                'ExpressionAttributeValues': {
                    ':tgt': {'S': oldtgtdate},
                    ':kindseq': {'S': oldkindseq},
                    ':befval': {'N': str(oldval) },
                    ':aftval' : {'N': str(newval) },
                    ':method_cd': {'S': bodyParam['method_cd']},
                    ':memo': {'S': get_memostr(bodyParam)}
                }
            }
        }
        retlist.append(upditem)

    return retlist

def get_balance_transaction_items(recalctgt, bodyParam, kindmstmap):
    target_methodlist = []
    has_cash = False
    if bodyParam['method_cd'] != '':
        target_methodlist.append(bodyParam['method_cd'])
        if bodyParam['method_cd'] == 'cash':
            has_cash = True
    if 'old_method_cd' in bodyParam and bodyParam['old_method_cd'] != '' and bodyParam['method_cd'] != bodyParam['old_method_cd']:
        target_methodlist.append(bodyParam['old_method_cd'])
        if bodyParam['old_method_cd'] == 'cash':
            has_cash = True
    
    if not has_cash:
        if bodyParam['kind_cd'] != '':
            wkkindmst = kindmstmap[bodyParam['kind_cd']]
            if wkkindmst['account_dir'] == ACCOUNT_DIR_CHARGE: 
                target_methodlist.append('cash')
        elif 'old_kind_cd' in bodyParam and bodyParam['old_kind_cd'] != '':
            wkkindmst = kindmstmap[bodyParam['old_kind_cd']]
            if wkkindmst['account_dir'] == ACCOUNT_DIR_CHARGE: 
                target_methodlist.append('cash')

    dt_now = get_jst_from_utc(datetime.datetime.now())
    date_from = dateutil.parser.parse(recalctgt)
    wkchk = 0
    wkloop = dt_now
    wkloopstr = wkloop.strftime("%Y%m%d")
    target_datelist = []
    while recalctgt <= wkloopstr and wkchk <= SAFECNT :
        logger.info("get_balance_transaction_items3:" + recalctgt + ':' + wkloopstr)
        target_datelist.append(wkloopstr)
        wkloop = wkloop + datetime.timedelta(days=-1)
        wkloopstr = wkloop.strftime("%Y%m%d")
        wkchk += 1

    logger.info("get_balance_transaction_items4:" + str(len(target_methodlist)))

    ret_tritemlist = []
    for tgtdate in target_datelist:
        for tgtmethod in target_methodlist:
            tr_getitem = {
                'Get': {
                    'TableName': TBL_BALANCE,
                    'Key': {
                        "tgt_date": {"S": tgtdate},
                        "method_cd": {"S": tgtmethod}
                    }
                }
            }
            ret_tritemlist.append(tr_getitem)

    return ret_tritemlist

def get_upd_tr_balanceitems(bodyParam, balance_datalist, kindmstmap):
    ret_tritemlist = []
    for balance_data in balance_datalist:
        bl_tgtdate = balance_data['tgt_date']
        bl_method = balance_data['method_cd']
        bl_value = balance_data['value']
        wk_bl_value = bl_value

        #if prm_tgt_date == prm_old_tgt_date and new_dir == old_dir and prm_method_cd == prm_old_method_cd and prm_value == prm_old_value:
        #    continue

        if bodyParam['tgt_date'] != '':
            prm_tgt_date = bodyParam['tgt_date']
            prm_kind_cd = bodyParam['kind_cd']
            prm_method_cd = bodyParam['method_cd']
            prm_value = bodyParam['value']
            new_kindmst = kindmstmap[prm_kind_cd]
            new_dir = new_kindmst['account_dir']

            if prm_tgt_date <= bl_tgtdate:
                # special operation for charge
                if new_dir == ACCOUNT_DIR_CHARGE and bl_method == 'cash' and bl_method != prm_method_cd:
                    wk_bl_value -= Decimal(prm_value)

                if bl_method == prm_method_cd:
                    if new_dir == ACCOUNT_DIR_CHARGE:
                        wk_bl_value += Decimal(prm_value)
                    elif new_dir == ACCOUNT_DIR_INCOME:
                        wk_bl_value += Decimal(prm_value)
                    else:
                        wk_bl_value -= Decimal(prm_value)

        if 'old_tgt_date' in bodyParam and bodyParam['old_tgt_date'] != '':
            prm_old_tgt_date = bodyParam['old_tgt_date']
            prm_old_kind_cd = bodyParam['old_kind_cd']
            prm_old_method_cd = bodyParam['old_method_cd']
            prm_old_value = bodyParam['old_value']
            old_kindmst = kindmstmap[prm_old_kind_cd]
            old_dir = old_kindmst['account_dir']

            if prm_old_tgt_date <= bl_tgtdate:
                # special operation for charge
                if old_dir == ACCOUNT_DIR_CHARGE and bl_method == 'cash' and bl_method != prm_old_method_cd:
                    wk_bl_value += Decimal(prm_old_value)

                if bl_method == prm_old_method_cd:
                    if old_dir == ACCOUNT_DIR_CHARGE:
                        wk_bl_value -= Decimal(prm_old_value)
                    elif old_dir == ACCOUNT_DIR_INCOME:
                        wk_bl_value -= Decimal(prm_old_value)
                    else:
                        wk_bl_value += Decimal(prm_old_value)

        if bl_value != wk_bl_value:
            bl_tritem = {
                'Update': {
                    'TableName': TBL_BALANCE,
                    'Key': {
                        "tgt_date": { "S": bl_tgtdate },
                        "method_cd": { "S": bl_method }
                    },
                    'ConditionExpression': '#tgt_date = :tgt and #method_cd = :method_cd and #value = :befval',
                    'UpdateExpression': 'SET #value = :aftval',
                    'ExpressionAttributeNames' : {
                        '#tgt_date' : 'tgt_date',
                        '#method_cd' : 'method_cd',
                        '#value' : 'value'
                    },
                    'ExpressionAttributeValues': {
                        ':tgt': {'S': bl_tgtdate},
                        ':method_cd': {'S': bl_method},
                        ':befval': {'N': str(bl_value) },
                        ':aftval' : {'N': str(wk_bl_value) }
                    }
                }
            }
            ret_tritemlist.append(bl_tritem)

    return ret_tritemlist

def lambda_handler(event, context):
    MODE_INS = 'ins'
    MODE_UPD = 'upd'
    MODE_DEL = 'del'

    #bodyParam = event['body']  # for lamda test directly
    bodyParam = json.loads(event['body'])
    logger.debug("Received event body: " + json.dumps(bodyParam, indent=0))
    uuidstr = bodyParam['uuid']
    if bodyParam['uuid'] == '':
        uuidstr = str(uuid.uuid4())

    table_name = 'account_slip'
    dynamotable = dynamodb.Table(table_name)

    mode = ''
    recalctgt = bodyParam['tgt_date']
    tran_items = []
    if bodyParam['tgt_date'] == '':
        mode = MODE_DEL
        recalctgt = bodyParam['old_tgt_date']
        tran_items.extend(get_del_tr_slipitems(bodyParam))
    elif 'old_tgt_date' in bodyParam:
        mode = MODE_UPD
        if bodyParam['old_tgt_date'] < recalctgt:
            recalctgt = bodyParam['old_tgt_date']
        tran_items.extend(get_upd_tr_slipitems(bodyParam))
    else:
        mode = MODE_INS
        tran_items.extend(get_ins_tr_slipitems(bodyParam))

    logger.info("tran_items size-slip: " + str(len(tran_items)))

    kindmstmap = get_kindmstmap()
    balance_get_response = client.transact_get_items(
        TransactItems = get_balance_transaction_items(recalctgt, bodyParam, kindmstmap)
    )
    balance_datalist = convert_dynamodata_to_map(balance_get_response['Responses'])

    tran_items.extend(get_upd_tr_balanceitems(bodyParam, balance_datalist, kindmstmap))
    logger.info("tran_items size-total: " + str(len(tran_items)))
    logger.info("tran_items body: " + json.dumps(tran_items, indent=0))

    response = client.transact_write_items(
        ReturnConsumedCapacity='INDEXES',
        TransactItems=tran_items
    )

    return {
        'statusCode': 200,
        'body': "{}",
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods' : 'GET,OPTIONS,POST',
            'Access-Control-Allow-Origin' : 'http://localhost:8080'
        },
        'isBase64Encoded': False
    }
