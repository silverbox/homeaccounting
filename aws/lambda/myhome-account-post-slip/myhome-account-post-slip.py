import json
import boto3
import logging
import uuid

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    bodyParam = json.loads(event['body'])
    logger.debug("Received event body: " + json.dumps(bodyParam, indent=0))
    uuidstr = bodyParam['uuid']
    if bodyParam['uuid'] == '':
        uuidstr = str(uuid.uuid4())

    table_name = 'account_slip'
    dynamotable = dynamodb.Table(table_name)

    if bodyParam['tgt_date'] != '':
        memostr = bodyParam['memo']
        if memostr is None or memostr == "":
            memostr = " "
        slipItem = {
            "tgt_date" : bodyParam['tgt_date'],
            "kind_cd_seq" : bodyParam['kind_cd'] + "_" + uuidstr,
            "method_cd" : bodyParam['method_cd'],
            "value" : bodyParam['value'],
            "memo" : memostr
        }
        res = dynamotable.put_item(Item=slipItem)
        print("put result response: " + json.dumps(res, indent=2))

    if 'old_tgt_date' in bodyParam:
        if bodyParam['tgt_date'] != bodyParam['old_tgt_date'] or bodyParam['kind_cd'] != bodyParam['old_kind_cd'] or bodyParam['old_uuid'] != bodyParam['uuid']:
            delSlipItem = {
                "tgt_date" : bodyParam['old_tgt_date'],
                "kind_cd_seq" : bodyParam['old_kind_cd'] + "_" + bodyParam['old_uuid']
            }
            resdel = dynamotable.delete_item(Key=delSlipItem)
            print("del result response: " + json.dumps(resdel, indent=2))

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
