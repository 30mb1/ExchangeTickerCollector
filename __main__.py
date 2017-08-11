from pymongo import MongoClient
from exchangeAPI.poloniex import Poloniex
from exchangeAPI.bitmex import Bitmex
from exchangeAPI.bitfinex import Bitfinex
from exchangeAPI.bittrex import Bittrex
from exchangeAPI.gdax import Gdax
from multiprocessing import Process
from database import Data
import parallel
import utility
import sys
import time
import copy

proc = []

def command_handler(command):
    command = command.split(' ')
    if command[0] == '/help':
        print (help_message)
        return

    if command[0] == '/add':
        exch_check_er = utility.check_exchanges(command[2:])
        if exch_check_er:
            utility.wtf()
            return
        pair_er = utility.check_cur_pair(command[1], command[2:])
        if pair_er:
            utility.wtf()
            return
        setup_dict = copy.deepcopy(utility.template)
        if len(command[2:]) == 0:
            print ('Enter exchanges.')
            utility.wtf()
            return
        for exchange in command[2:]:
            setup_dict[exchange].append(command[1])
        db = Data()
        db.setup(setup_dict)
        print ('OK, instrument added to collector. Use /on to start gathering information.')
        utility.wtf()
        return

    if command[0] == '/remove':
        exch_check_er = utility.check_exchanges(command[2:])
        if exch_check_er:
            utility.wtf()
            return
        db = Data()
        db.remove(command[1], command[2:])
        utility.wtf()
        return

    if command[0] == '/info':
        db = Data()
        cur_setup = db.get_cur_setup()
        for key, item in cur_setup.items():
            print (key, ':', item)
        utility.wtf()
        return

    global proc
    if command[0] == '/off':
        if len(proc) != 0:
            parallel.stop_collecting(proc[0])
            print ('Collecting stopped.')
            proc = []
        utility.wtf()
        return

    if command[0] == '/on':
        proc.append(Process(target=parallel.start_collecting, args=()))
        proc[0].start()
        print ('Collecting started.')
        utility.wtf()
        return

    raise BaseException

if __name__ == '__main__':
    print ('You are using exchange statistics collector.\nEnter command to start gathering information.\n'
           'Enter /help to get list of available commands.')
    while True:
        try:
            command = input().strip()
            command_handler(command)
        except KeyboardInterrupt:
            print ('Turning bot off...')
            db = Data()
            db.clean()
            if len(proc) != 0:
                parallel.stop_collecting(proc[0])
            sys.exit(0)
        except:
            print ('Unrecognized command. Please, try again.')
            utility.wtf()
