import requests
import json

class Bitfinex(object):

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
            return [False, 'Bitfinex: problems with network.']
        return wrapper

    @staticmethod
    @retry
    def check_pair(pair):
        pair = pair[pair.find('_') + 1:] + pair[:pair.find('_')]
        pair = pair.lower()
        ret = requests.get('https://api.bitfinex.com/v1/symbols', timeout=2)
        if pair not in ret.json():
            return False
        return True

    def get_quotation(pair):
        pair = pair[pair.find('_') + 1:] + pair[:pair.find('_')]
        try:
            ret = requests.get('https://api.bitfinex.com/v1/pubticker/' + pair, timeout=0.9)
            if ret.status_code != 200:
                return 0
            ret = ret.json()
            return [float(ret['bid']), float(ret['ask'])]
        except:
            return 0
