from pymongo import MongoClient
from utility import template

class Data(object):
    def __init__(self):
        self.database = MongoClient()['ExchangeStat']

    def setup(self, setup_dict):
        cur_setup = self.database['setup'].find_one()
        if cur_setup != None:
            for key in setup_dict.keys():
                if len(setup_dict[key]) != 0:
                    if setup_dict[key][0] not in cur_setup[key]:
                        cur_setup[key].extend(setup_dict[key])
            self.database['setup'].update_one(
                {},
                {
                    '$set' : cur_setup
                }
            )
        else:
            self.database['setup'].insert_one(
                setup_dict
            )

    def get_cur_setup(self):
        cur_setup = self.database['setup'].find_one()
        if cur_setup == None:
            return template
        else:
            cur_setup.pop('_id')
            return cur_setup

    def remove(self, pair, exchanges):
        cur_setup = self.database['setup'].find_one()
        if cur_setup == None:
            return
        else:
            for cur in exchanges:
                try:
                    cur_setup[cur].remove(pair)
                except:
                    pass
            self.database['setup'].update_one(
                {},
                {
                    '$set' : cur_setup
                }
            )

    def insert_tick(self, tick):
        self.database['tickers'].insert_one(
            tick
        )

    def clean(self):
        cur_setup = self.database['setup'].find_one()
        if cur_setup != None:
            self.database['setup'].delete_one(
                cur_setup
            )
