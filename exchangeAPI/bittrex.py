import requests
import json

class Bittrex(object):

    def retry(func):
        def wrapper(*args, **kwargs):
            for i in range(3):
                try:
                    res = func(*args)
                    if res:
                        return [res, 'OK']
                    else:
                        return [res, 'This instrument is not available on this exchange.']
                except:
                    continue
            return [False, 'Bittrex: problems with network.']
        return wrapper

    @staticmethod
    @retry
    def check_pair(pair):
        pair = pair.replace('USD', 'USDT')
        pair = pair.replace('_', '-')
        ret = requests.get('https://bittrex.com/api/v1.1/public/getmarkets', timeout=2)
        ret = ret.json()['result']
        for cur_pair in ret:
            if pair == cur_pair['MarketName']:
                return True
        return False

    @staticmethod
    def get_quotation(pair):
        pair = pair.replace('USD', 'USDT')
        pair = pair.replace('_', '-')
        try:
            ret = requests.get('https://bittrex.com/api/v1.1/public/getticker?market=' + pair, timeout=0.8)
            if ret.status_code != 200:
                return 0
            ret = ret.json()['result']
            return [ret['Bid'], ret['Ask']]
        except:
            return 0
