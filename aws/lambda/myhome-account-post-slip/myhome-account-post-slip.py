import json
import boto3
import logging

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug("Received event body: " + json.dumps(event, indent=0))

    bodyParam = json.loads(event['body'])
    slipItem = {
        "tgt_date" : bodyParam['tgt_date'],
        "kind_cd_seq" : bodyParam['kind_cd_seq'],
        "value" : bodyParam['value'],
        "memo" : bodyParam['memo']
    }

    table_name = 'account_slip'
    dynamotable = dynamodb.Table(table_name)

    res = dynamotable.put_item(Item=slipItem)
    print("put result response: " + json.dumps(res, indent=2))

    return {
        'statusCode': 200,
        'body': "{}",
        'headers': {},
        'isBase64Encoded': False
    }
