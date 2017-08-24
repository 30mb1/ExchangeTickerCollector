import boto3
from database import Data
import sys
from pandas.io.json import json_normalize

db = Data()
coursor = db.get_tickers()
res = []
first = True

for ticker in coursor:
    if first:
        _from = ticker['time']
        first = False
    last = ticker['time']
    ticker.pop('_id')
    res.append(ticker)
if len(res) == 0:
    print ('No data to download in database.')
    sys.exit(0)

data_name = _from[:10] + ' - ' + last[:10] + '.csv'
tmp = 'tickers/' + data_name

res = json_normalize(res)
res.to_csv(tmp)

client = boto3.client('s3', region_name='eu-central-1')
response = client.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]

bucket_name = 'ExchangeStatistics'
if bucket_name not in buckets:
    client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'eu-central-1'
    })

client.upload_file(tmp, bucket_name, data_name)

presigned_url = client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': data_name})
print ('Your link for downloading: ')
print (presigned_url)

db.del_tickers()
