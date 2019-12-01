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
    logger.info("Received event body: " + json.dumps(event, indent=0))

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
        date_from = date_to - datetime.timedelta(days=date_count - 1)
    elif (date_to is None) and date_count is not None:
        date_to = date_from + datetime.timedelta(days=date_count - 1)
    else:
        date_count = int( (date_to - date_from) / datetime.timedelta(days=1) ) + 1

    slip_table_name = 'account_slip'
    slip_table = dynamodb.Table(slip_table_name)

    datasetslist = []

    kindmst_table_name = 'account_kind_mst'
    kindmst_table = dynamodb.Table(kindmst_table_name)
    kindmstres = kindmst_table.scan()
    kindmstitems = kindmstres['Items']
    kindmstitems.sort(key=lambda x: x['display_order'])
    kindmstidxmap = {}
    kindmstcdmap = {}
    for kindmstitem in kindmstitems:
        if kindmstitem['account_dir'] != 0:
            continue
        wkdatasets = {}
        wkdatasets['kind_cd'] = kindmstitem['kind_cd']
        wkdatasets['label'] = kindmstitem['kind_nm']
        wkdatasets['data'] = [0] * (date_count + 1)
        wkdatasets['backgroundColor'] = '#000'
        wkkindcd = kindmstitem['kind_cd']

        kindmstidxmap[wkkindcd] = len(datasetslist)
        kindmstcdmap[wkkindcd] = kindmstitem
        datasetslist.append(wkdatasets)

    wkloop = date_from
    labels = []
    dateidx = 0
    cdchkmap = {}
    while str(wkloop) <= str(date_to) :
        wkloopstr = wkloop.strftime("%Y%m%d")
        wkres = slip_table.query(KeyConditionExpression=Key('tgt_date').eq(wkloopstr))

        labels.append(wkloopstr)
        for slip in wkres['Items']:
            wkkindseq = slip['kind_cd_seq'].split('_')
            wkslip = {}
            wkslip['tgt_date'] = slip['tgt_date']
            wkslip['kind_cd'] = wkkindseq[0]
            cdchkmap[wkkindseq[0]] = "true"

            wkkindmst = kindmstcdmap[wkslip['kind_cd']]
            wkkindidx = kindmstidxmap[wkslip['kind_cd']]
            wkdatasets = datasetslist[wkkindidx]
            wkdatasets['data'][dateidx] = wkdatasets['data'][dateidx] + float(slip['value'])

        wkloop = wkloop + datetime.timedelta(days=1)
        dateidx = dateidx + 1
        
    filtereddatasetlist = []
    for datasets in datasetslist:
        if datasets['kind_cd'] in cdchkmap.keys():
            filtereddatasetlist.append(datasets)

    chartdata = {}
    chartdata['labels'] = labels
    chartdata['datasets'] = filtereddatasetlist

    cahrtOptions = {
        'scales': {
            'xAxes': [{
                'stacked': 'true',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '日付'
                }
            }],
            'yAxes': [{
                'stacked': 'true',
                'scaleLabel': {
                    'display': 'true',
                    'labelString': '金額'
                },
                'ticks': {
                    'beginAtZero': 'true',
                    'stepSize': 500
                }
            }]
        }
    }

    chartstruct = {}
    chartstruct['options'] = cahrtOptions
    chartstruct['chartdata'] = chartdata
    return chartstruct

'''
    xSscaleLabel = {}
    xScaleLabel['display'] = true
    xScaleLabel['labelString'] = '日付'
    ySscaleLabel = {}
    yScaleLabel['display'] = true
    yScaleLabel['labelString'] = '日付'
    yTicks = {}
    yTicks['beginAtZero'] = true
    yTicks['stepSize'] = 500
    xAxes = {}
    yAxes = {}
    xAxes['stacked'] = true
    xAxes['scaleLabel'] = xScaleLabel
    yAxes['stacked'] = true
    yAxes['scaleLabel'] = ySscaleLabel
    yAxes['ticks'] = yTicks

    scales = {}
    scales['xAxes'] = xAxes
    scales['yAxes'] = yAxes
    options = {}
    options['scales'] = scales
'''