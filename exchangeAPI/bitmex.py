import requests
import json

class Bitmex(object):

    allowed_pairs = {
        'USD_BTC' : 'XBT',
        'YEN_BTC' : 'XBJ',
        'BTC_DASH' : 'DASH',
        'BTC_ETH' : 'ETH',
        'BTC_ETC' : 'ETC',
        'BTC_LTC' : 'LTC',
        'BTC_QTUM' : 'QTUM',
        'BTC_XMR' : 'XMR',
        'BTC_XRP' : 'XRP',
        'BTC_XTZ' : 'XTZ',
        'BTX_ZEC' : 'ZEC'
    }

    @staticmethod
    def check_pair(pair):
        if pair in Bitmex.allowed_pairs.keys():
            return [True, 'OK']
        return [False, 'This instrument is not available on this exchange.']

    @staticmethod
    def get_quotation(pair):
        try:
            ret = requests.get('https://www.bitmex.com/api/v1/quote?symbol=' + Bitmex.allowed_pairs[pair] + '&count=1&reverse=true', timeout=0.8)
            if ret.status_code != 200:
                return 0
            ret = ret.json()[0]
            return [ret['bidPrice'], ret['askPrice']]
        except:
            return 0
