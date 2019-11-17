import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event['body'], indent=2))
    print("Received event: " + event['body'])
    bodyParam = json.loads(event['body'])
    balanceItem = {
        "tgt_date" : bodyParam['tgt_date'],
        "value" : bodyParam['value'],
        "memo" : bodyParam['memo']
    }

    table_name = 'account_balance'
    dynamotable = dynamodb.Table(table_name)

    res = dynamotable.put_item(Item=balanceItem)
    print("put result response: " + json.dumps(res, indent=2))

    #item = res['Item']
    ret = {}
    ret['value'] = str("")

    return {
        'statusCode': 200,
        'body': json.dumps(ret, indent=0),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods' : 'GET,OPTIONS,POST',
            'Access-Control-Allow-Origin' : 'http://localhost:8080'
        },
        'isBase64Encoded': False
    }
