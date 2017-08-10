from pymongo import MongoClient
from multiprocessing import Process, Pool
from exchangeAPI.poloniex import Poloniex
from exchangeAPI.bitmex import Bitmex
from exchangeAPI.bitfinex import Bitfinex
from exchangeAPI.bittrex import Bittrex
from exchangeAPI.gdax import Gdax
from database import Data
import utility
import time
import sys

database = MongoClient()['ExchangeStat']

def multifunc(func, args):
    p = Pool(len(args))
    print (p.map(func, args))
    sys.stdout.flush()



if __name__ == '__main__':
    print ('You are using exchange statistics collector.\nEnter command to start gathering information.\n'
           'Enter /help to get list of available commands.')
    db = Data()
    while True:
        command = input().strip()
        command = command.split(' ')
        if command[0] == '/help':
            print (help_message)
        if command[0] == '/add':
            exch_check_er = utility.check_exchanges(command[2:])
            if exch_check_er:
                utility.wtf()
                continue
            pair_er = utility.check_cur_pair(command[1], command[2:])
            if pair_er:
                utility.wtf()
                continue
            setup_dict = utility.template
            for exchange in command[2:]:
                setup_dict[exchange].append(command[1])
            db.setup(setup_dict)
            print ('OK. Collecting started. You can enter another command to remove some instrument or to add new.')
            utility.wtf()
        if command[0] == '/remove':
            exch_check_er = utility.check_exchanges(command[2:])
            if exch_check_er:
                utility.wtf()
                continue
            db.remove(command[1], command[2:])
            utility.wtf()

        if command[0] == '/info':
            cur_setup = db.get_cur_setup()
            for key, item in cur_setup.items():
                if key == '_id':
                    continue
                print (key, ':', item)
            utility.wtf()
