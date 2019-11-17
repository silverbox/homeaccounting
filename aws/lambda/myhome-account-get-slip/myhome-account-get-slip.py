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

def lambda_handler(event, context):
    table_name = 'account_slip'
    logger.info("Received event body: " + json.dumps(event, indent=0))

    date_from = None;
    date_to = None;
    date_count = None;
    if 'tgt_date_from' in event:
        date_from = dateutil.parser.parse(event['tgt_date_from'])
    if 'tgt_date_to' in event:
        date_to = dateutil.parser.parse(event['tgt_date_to'])
    if 'tgt_date_count' in event:
        date_count = int(event['tgt_date_count'])

    if (date_from is None) and date_count is not None:
        date_from = date_to - datetime.timedelta(days=date_count)
    elif (date_to is None) and date_count is not None:
        date_to = date_from + datetime.timedelta(days=date_count)

    dynamotable = dynamodb.Table(table_name)

    wkloop = date_to
    slip_list = []
    while str(wkloop) >= str(date_from) :
        wkres = dynamotable.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
        for slip in wkres['Items']:
            wkkindseq = slip['kind_cd_seq'].split('_')
            wkslip = {}
            wkslip['tgt_date'] = slip['tgt_date']
            wkslip['kind_cd'] = wkkindseq[0]
            wkslip['uuid'] = wkkindseq[1]
            wkslip['method_cd'] = slip['method_cd']
            wkslip['value'] = slip['value']
            wkslip['memo'] = slip['memo']
            slip_list.append(wkslip)

        wkloop = wkloop + datetime.timedelta(days=-1)

    return slip_list
