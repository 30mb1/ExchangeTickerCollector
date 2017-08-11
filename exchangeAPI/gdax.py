import requests
import json

class Gdax(object):

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
            return [False, 'Gdax: problems with network.']
        return wrapper

    @staticmethod
    @retry
    def check_pair(pair):
        pair = pair[pair.find('_') + 1:] + '-' + pair[:pair.find('_')]
        ret = requests.get('https://api.gdax.com/products', timeout=2)
        ret = ret.json()
        for cur_pair in ret:
            if  pair == cur_pair["id"]:
                return True
        return False

    @staticmethod
    def get_quotation(pair):
        pair = pair[pair.find('_') + 1:] + '-' + pair[:pair.find('_')]
        try:
            ret = requests.get('https://api.gdax.com/products/' + pair + '/book', timeout=0.9)
            if ret.status_code != 200:
                return 0
            ret = ret.json()
            return [float(ret["bids"][0][0]), float(ret["asks"][0][0])]
        except:
            return 0
