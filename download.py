import boto3
from database import Data
import json

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

data_name = _from[:10] + ' - ' + last[:10] + '.json'
tmp = 'tickers/' + data_name

with open(tmp, 'w') as outfile:
    json.dump(res_dict, outfile)

client = boto3.client('s3', region_name='eu-central-1')
bucket_name = 'exchangestat'
client.upload_file(tmp, bucket_name, data_name)


presigned_url = client.generate_presigned_url('get_object', Params = {'Bucket': 'exchangestat', 'Key': data_name})
print ('Your link for downloading: ')
print (presigned_url)

db.del_tickers()
