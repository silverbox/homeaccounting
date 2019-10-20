import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = 'account_slip'
    eventParam = event['queryStringParameters']
    print("Received event: " + json.dumps(eventParam, indent=2))
    primary_key = {'tgt_date': eventParam['tgt_date']}
    dynamotable = dynamodb.Table(table_name)
    res = dynamotable.get_item(Key=primary_key)
    item = res['Item']
    ret = {}
    ret['value'] = str(item['value'])

    return {
        'statusCode': 200,
        'body': json.dumps(ret, indent=0),
        'headers': {
            'my_header': 'dummy'
        },
        'isBase64Encoded': False
    }
