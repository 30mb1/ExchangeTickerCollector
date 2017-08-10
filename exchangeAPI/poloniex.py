import requests
import json

class Poloniex(object):
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
            return [False, 'Poloniex: problems with network.']
        return wrapper

    @staticmethod
    @retry
    def check_pair(pair):
        pair = pair.replace('USD', 'USDT')
        ret = requests.get('https://poloniex.com/public?command=returnTicker', timeout=2)
        if pair not in ret.json().keys():
            return False
        return True

    @staticmethod
    def get_quotation(pair):
        pair = pair.replace('USD', 'USDT')
        try:
            ret = requests.get('https://poloniex.com/public?command=returnTicker', timeout=0.9)
            if ret.status_code != 200:
                return 0
            ret = ret.json()[pair]
            return [ret['highestBid'], ret['lowestAsk']]
        except:
            return 0
