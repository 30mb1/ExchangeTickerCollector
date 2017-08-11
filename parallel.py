from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from database import Data
from utility import template2
import time

def do_func(arg_list):
    exchange = template2[arg_list[0]]
    pairs = arg_list[1]
    if len(pairs) == 0:
        return 0
    pool = ThreadPool(len(pairs))
    ret = pool.map(exchange.get_quotation, pairs)
    return ret

def start_collecting():
    db = Data()
    while True:
        result_dict = {}
        _from = time.time()
        result_dict['time'] = time.strftime("%Y.%m.%d - %H:%M:%S")
        cur_setup = db.get_cur_setup()
        list_ = []
        for key, item in cur_setup.items():
            list_.append([key, item])
        pool = ThreadPool(5)
        ret = pool.map(do_func, list_)
        for jdx, item in enumerate(list_):
            tmp_dict = {}
            for idx, pair in enumerate(item[1]):
                tmp_dict[pair] = ret[jdx][idx]
            result_dict[item[0]] = tmp_dict

        #print (result_dict)
        db.insert_tick(result_dict)
        end_time = time.time() - _from
        if end_time < 1:
            time.sleep(1 - end_time)

def stop_collecting(process):
    process.terminate()
