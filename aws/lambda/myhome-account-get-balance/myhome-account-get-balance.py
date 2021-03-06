import json
import boto3
import logging
import datetime
import dateutil.parser

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def submit_balance(tgtDate, balancelist):
    balanncetable = dynamodb.Table('account_balance')
    logger.debug("submit_balance: " + tgtDate)
    with balanncetable.batch_writer() as batch:
        for wkbalance in balancelist:
            balanceItem = {
                "tgt_date" : tgtDate,
                "method_cd" : wkbalance['method_cd'],
                "value" : wkbalance['value']
            }
            batch.put_item(Item=balanceItem)

def lambda_handler(event, context):
    SAFECNT = 50
    table_name = 'account_balance'
    logger.info('Received event body: ' + json.dumps(event, indent=0))
    tgtDate = event['tgt_date']
    primary_key = {'tgt_date': tgtDate}
    dynamotable = dynamodb.Table(table_name)

    wkres = dynamotable.query(KeyConditionExpression=Key('tgt_date').eq(tgtDate))
    wkitems = wkres['Items']
    # org_len = len(wkitems)

    date_to = dateutil.parser.parse(event['tgt_date'])
    wkchk = 0
    wkloop = date_to
    emptyDateList = []
    while len(wkitems) == 0 and wkchk <= SAFECNT :
        emptyDateList.append(wkloop.strftime("%Y%m%d")) # add empty date info
        wkloop = wkloop + datetime.timedelta(days=-1)
        wkdatestr = wkloop.strftime("%Y%m%d")
        wkres = dynamotable.query(KeyConditionExpression=Key('tgt_date').eq(wkdatestr))
        wkitems = wkres['Items']
        wkchk += 1

    for emptyDate in emptyDateList:
        submit_balance(emptyDate, wkitems)

    return wkitems
