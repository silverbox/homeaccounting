import json
import boto3
import logging
import decimal
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
    table_name = 'account_kind_mst'

    dynamotable = dynamodb.Table(table_name)
    dbres = dynamotable.scan()
    items = dbres['Items']
    logger.info("Dynamo res body: " + json.dumps(items,cls=DecimalEncoder, indent=0))
    item = items[0]

    return {
        'statusCode': 200,
        'body': json.dumps(items,cls=DecimalEncoder, indent=0),
        'headers': {
            'my_header': 'dummy'
        },
        'isBase64Encoded': False
    }
