import json
import boto3
import decimal
import logging
import datetime
import dateutil.parser
import os
#import base64
import tempfile
import zipfile
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
    logger.info("Received event body: " + json.dumps(event, cls=DecimalEncoder, indent=0))

    #token = event['token'];
    #sections = token.split('.');
    #payload = json.loads(base64.b64decode(sections[1]).decode())
    #logger.info("payload body: " + json.dumps(payload, indent=0))

    date_from = None;
    date_to = None;
    date_count = None;
    if 'tgt_date_from' in event and event['tgt_date_from'] != '':
        date_from = dateutil.parser.parse(event['tgt_date_from'])
    if 'tgt_date_to' in event and event['tgt_date_to'] != '':
        date_to = dateutil.parser.parse(event['tgt_date_to'])
    if 'tgt_date_count' in event and event['tgt_date_count'] != '':
        date_count = int(event['tgt_date_count'])

    if (date_from is None) and date_count is not None:
        date_from = date_to - datetime.timedelta(days=date_count)
    elif (date_to is None) and date_count is not None:
        date_to = date_from + datetime.timedelta(days=date_count)

    file_suffix = '_{0}_{1}'.format(date_from.strftime("%Y%m%d"), date_to.strftime("%Y%m%d"))

    slip_table_name = 'account_slip'
    slip_table = dynamodb.Table(slip_table_name)
    slip_file_name = 'slip' + file_suffix + '.tcv'
    fmt_slip = '{0}\t{1}\t{2}\t{3}\t{4}\n'
    balance_table_name = 'account_balance'
    balance_table = dynamodb.Table(balance_table_name)
    balance_file_name = 'balance' + file_suffix + '.tcv'
    fmt_balance = '{0}\t{1}\t{2}\n'
    packed_file_name = 'packed' + file_suffix + '.zip'

    tmpdir = tempfile.TemporaryDirectory()
    try:
        packed_full_name = os.path.join(tmpdir.name, packed_file_name)
        slip_full_name = os.path.join(tmpdir.name, slip_file_name)
        balance_full_name = os.path.join(tmpdir.name, balance_file_name)

        logger.info("slip_full_name: " + slip_full_name)
        logger.info("balance_full_name: " + balance_full_name)
        slip_file = open(slip_full_name, 'w')
        balance_file = open(balance_full_name, 'w')
        try:
            wkloop = date_from
            while str(wkloop) <= str(date_to) :
                wkslipres = slip_table.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
                wkbalanceres = balance_table.query(KeyConditionExpression=Key('tgt_date').eq(wkloop.strftime("%Y%m%d")))
                for slip in wkslipres['Items']:
                    wkslipstr = fmt_slip.format(slip['tgt_date'], slip['kind_cd_seq'], slip['method_cd'], slip['value'], slip['memo'])
                    # logger.info("wkslipstr: " + wkslipstr)
                    slip_file.write(wkslipstr)
                for balance in wkbalanceres['Items']:
                    wkbalancestr = fmt_balance.format(balance['tgt_date'], balance['method_cd'], balance['value'])
                    # logger.info("wkbalancestr: " + wkbalancestr)
                    balance_file.write(wkbalancestr)

                wkloop = wkloop + datetime.timedelta(days=1)
        finally:
            slip_file.close()
            balance_file.close()

        with zipfile.ZipFile(packed_full_name, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            new_zip.write(slip_full_name, arcname=slip_file_name)
            new_zip.write(balance_full_name, arcname=balance_file_name)

        s3 = boto3.resource('s3')
        bucket = s3.Bucket('myapp-userdata')
        bucket.upload_file(packed_full_name, 'cognito/myhome-account/' + event['identityid'] + '/' + packed_file_name)
    finally:
        tmpdir.cleanup()

    return packed_file_name
