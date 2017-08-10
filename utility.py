from exchangeAPI.poloniex import Poloniex
from exchangeAPI.bitmex import Bitmex
from exchangeAPI.bitfinex import Bitfinex
from exchangeAPI.bittrex import Bittrex
from exchangeAPI.gdax import Gdax

template = {
    'poloniex' : [],
    'bittrex' : [],
    'gdax' : [],
    'bitfinex' : [],
    'bitmex' : []
}

template2 = {
    'poloniex' : Poloniex,
    'bittrex' : Bittrex,
    'gdax' : Gdax,
    'bitfinex' : Bitfinex,
    'bitmex' : Bitmex
}

def check_exchanges(list_):
    error = False
    for exch in list_:
        if exch not in template.keys():
            print ('There is no exchange named: ' + exch)
            error = True
    if error:
        print ('Invalid command. Please, try again.')
        return True
    return False

def check_cur_pair(pair, exchanges):
    error = False
    for exch in exchanges:
        res = template2[exch].check_pair(pair)
        if res[0] == False:
            error = True
        print (exch + ': ' + res[1])
    return error

def wtf():
    er_text = '.\n.\n.'
    print (er_text)
