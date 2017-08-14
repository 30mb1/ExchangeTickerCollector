import boto3
from database import Data
import json
import sys

db = Data()
coursor = db.get_tickers()
res_dict = {}
first = True

for ticker in coursor:
    if first:
        _from = ticker['time']
        first = False
    time = ticker['time']
    last = time
    ticker.pop('time')
    ticker.pop('_id')
    res_dict[time] = ticker
if len(res_dict) == 0:
    print ('No data to download in database.')
    sys.exit(0)

data_name = _from[:10] + ' - ' + last[:10] + '.json'
tmp = 'tickers/' + data_name

with open(tmp, 'w') as outfile:
    json.dump(res_dict, outfile)

client = boto3.client('s3', region_name='us-east-2')
response = client.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]

bucket_name = 'exchange_data'
if bucket_name not in buckets:
    client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'
    })

client.upload_file(tmp, bucket_name, data_name)

presigned_url = client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': data_name})
print ('Your link for downloading: ')
print (presigned_url)

db.del_tickers()
