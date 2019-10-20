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

    date_from = dateutil.parser.parse(event['tgt_date_from'])
    date_to = dateutil.parser.parse(event['tgt_date_to'])
    
    dynamotable = dynamodb.Table(table_name)

    date_from = dateutil.parser.parse(event['tgt_date_from'])
    date_to = dateutil.parser.parse(event['tgt_date_to'])
    wkloop = date_from
    slip_list = []
    while str(wkloop) <= str(date_to) :
        wkres = dynamotable.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
        slip_list += wkres['Items']
        wkloop = wkloop + datetime.timedelta(days=1)

    return slip_list
