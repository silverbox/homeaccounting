import json
import boto3
import logging

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    table_name = 'account_balance'
    logger.info("Received event body: " + json.dumps(event, indent=0))
    tgtDate = event["tgt_date"]
    primary_key = {'tgt_date': tgtDate}
    dynamotable = dynamodb.Table(table_name)
    res = dynamotable.get_item(Key=primary_key)
    item = res['Item']

    return item

    #ret = {}
    #ret['value'] = str(item['value'])
    
#    return {
#        'statusCode': 200,
#        'body': json.dumps(ret, indent=0),
#        'headers': {
#            'my_header': 'dummy'
#        },
#        'isBase64Encoded': False
#    }

