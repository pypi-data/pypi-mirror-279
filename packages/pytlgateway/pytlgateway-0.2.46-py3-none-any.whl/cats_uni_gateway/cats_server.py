from datetime import datetime, timezone, timedelta
import os
import queue
import threading
import time
import json
import signal
import sys
import traceback
import argparse
import csv
import dbf
import shutil
import pathlib


from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient, ASCENDING, DESCENDING

from ..mongo_client_gateway import MongoClientTradeGateway
from ..utils import (get_exchange_from_ticker, check_today_index)
from .constants import (FILES, GATEWAY_NAME)
from .utils import (side_to_target_type, decode_exchange_id, decode_ordtype, decode_cats_status, decode_cats_side)
from ..logger import Logger

try:
    import thread
except ImportError:
    import _thread as thread

LL9 = 1000000000


class CatServer(MongoClientTradeGateway):
    def __init__(self, config_filename, endtime):
        MongoClientTradeGateway.__init__(self, config_filename, endtime, GATEWAY_NAME)

        self.insert_orders = {}
        self.oid_to_ref_list = {}
        self.sids = []
        self.oid_to_traded = {}
        self.oid_to_traded_money = {}
        self.sid_to_req = {}
        self.oid_to_req = {}
        self.oid_to_mid = {}
        self.oid_to_acc = {}
        self.db_id_to_oid = {}
        self.ref_to_oid = {}
        self.order_index = -1 #dbf文件当前index
        self.trade_index = -1
        self.pos_index = -1
        self.oid_to_local_ids = {}
        self.acct_type = {}
        self.client_id = {}
        self.oid_to_algoid = {}
        self.algoid_to_oid = {}
        self.algoid_to_order_record = {} #缓存 order
        self.mudanid_to_trade_record = {}
        self.algo_cache_lock = threading.RLock()
        self.order_cache_lock = threading.RLock()
        self.trade_index = -1
        self.order_index = -1
        self.algo_index = -1
        self.load_tg_setting(config_filename)
        self.init_dbf_tables()

    def monitor(self):
        self.thread_pool.submit(self.monitor_algo_order_insert)
        #self.thread_pool.submit(self.monitor_cancel_order_insert)
        self.thread_pool.submit(self.monitor_algo_order_update)
        self.thread_pool.submit(self.monitor_order_update)
        self.thread_pool.submit(self.monitor_trade_update)
        #self.thread_pool.submit(self.monitor_dbf_asset)
        self.thread_pool.submit(self.monitor_dbf_pos)
        self.thread_pool.submit(self.date_change)

    def load_tg_setting(self, config_filename):
        try:
            f = open(config_filename, encoding='gbk')
            setting = json.load(f)
            #self.insert_order_path = setting['insert_order_path'].replace('/', '\\')
            self.recv_msg_dir = setting['recv_msg_path'].replace('/', '\\')
            self.recv_msg_trade_dir = setting['recv_msg_path_trade'].replace('/', '\\')
            self.insert_order_path = setting['insert_order_path'].replace('/', '\\')
            for acc in self.accounts_run:
                config = self.config[acc]
                self.acct_type[acc] = config['acct_type']
                self.client_id[acc] = config['client_id']
        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            print(f"load config failed! (exception){err}")
            exit(0)
    @MongoClientTradeGateway.error_handler
    def init_dbf_tables(self):
        #not use
        pos_filename = self.recv_msg_dir + '\\' + FILES.POSITIONS  + '.dbf'
        self.position_order_table = dbf.Table(filename=pos_filename, codepage='utf8', on_disk=True)
        self.position_order_table.open(mode=dbf.READ_WRITE)
        self.logger.info(f"[init_dbf_tables open] (filename){pos_filename}")
        order_filename = self.recv_msg_trade_dir + '\\' + FILES.ORDERS + '.dbf'
        rtn_order_table = dbf.Table(filename=order_filename,codepage='utf8', on_disk=True)
        with rtn_order_table.open(mode=dbf.READ_WRITE):
            if len(rtn_order_table) <= 0:
                self.logger.warning(f'no record in {order_filename}')
            else:
                while rtn_order_table[self.order_index+1] is not rtn_order_table.last_record:
                    self.order_index += 1
                    record = rtn_order_table[self.order_index]
                    write_time = str(record.WRITE_TIME).strip(' ')[:-4]
                    if check_today_index(write_time):
                        break

        algo_order_filename = self.recv_msg_dir + '\\' + FILES.ALGO_ORDERS + '.dbf'
        rtn_algo_order_table = dbf.Table(filename=algo_order_filename,codepage='utf8', on_disk=True)
        with rtn_algo_order_table.open(mode=dbf.READ_WRITE):
            if len(rtn_algo_order_table) <= 0:
                self.logger.warning(f'no record in {algo_order_filename}')
            else:
                while rtn_algo_order_table[self.algo_index+1] is not rtn_algo_order_table.last_record:
                    self.algo_index += 1
                    record = rtn_algo_order_table[self.algo_index]
                    write_time = str(record.WRITE_TIME).split('@')[1].strip(' ')[:-4]
                    if check_today_index(write_time):
                        break

        trade_filename = self.recv_msg_trade_dir + '\\' + FILES.TRADES + '.dbf'
        rtn_trade_table = dbf.Table(filename=trade_filename,codepage='utf8', on_disk=True)
        with rtn_trade_table.open(mode=dbf.READ_WRITE):
            if len(rtn_trade_table) <= 0:
                self.logger.warning(f'no record in {trade_filename}')
            else:
                while rtn_trade_table[self.trade_index+1] is not rtn_trade_table.last_record:
                    self.trade_index += 1
                    record = rtn_trade_table[self.trade_index]
                    write_time = str(record.TIME).strip(' ')[:-4]
                    if check_today_index(write_time):
                        break

    @MongoClientTradeGateway.error_handler
    def str2bool(self, v: str):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    def strdeltautc(self, input_time_str):

        # 解析时间字符串为 datetime 对象
        input_time = datetime.strptime(input_time_str, "%H:%M:%S")
        # 减去 8 小时的时间间隔
        new_time = input_time - timedelta(hours=8)
        # 将结果转换为字符串
        new_time_str = new_time.strftime("%H:%M:%S")
        return new_time_str

    @MongoClientTradeGateway.error_handler
    def req_buy_order_insert(self, obj):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        temp_filename = self.insert_order_path + '\\InPut_temp\\' + '1_buy.' + formatted_time + '.csv'
        with open(temp_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            target_account_name = obj['accountName']
            acc = self.target_account_names_to_acc[target_account_name]
            account_id = self.account_id[acc].split('.')[0]
            acct_type = self.acct_type[acc]

            oid = str(self.gen_order_id())[4:] #cats limit 16
            mid = str(obj['mid'])
            vol = int(obj["volume"])
            price = 0.0
            if not obj.get('price') is None:
                price = float(obj['price'])
            financial_buy_s = obj["financingBuy"]
            side = '1'
            if financial_buy_s == True:
                side = 'A'
            else:
                side = '1'
            tradingstyle = 2
            if not obj.get('tradingstyle') is None:
                tradingstyle = int(obj['tradingstyle'])
            participate = 0.1
            if not obj.get('participate') is None:
                participate = float(obj['participate'] / 100)

            order_vol = f'{vol:d}'
            int_stock_code = int(obj['ticker'])
            stock_code = get_exchange_from_ticker(int_stock_code)
            algo_type = decode_ordtype(obj['executionPlan']['order_type'])
            begin_time  = str(obj['executionPlan']['start_time']).replace(':','')
            end_time = str(obj['executionPlan']['end_time']).replace(':','')
            ord_param = f'AlgoType={algo_type};beginTime={begin_time};endTime={end_time}'

            if algo_type in ['VWAP', 'TWAP']:
                ord_param += f';limitPrice={price};participateRate=0;tradingStyle={tradingstyle}'
            elif algo_type in ['VWAP3', 'TWAP3', 'SmartTWAP3', 'SmartVWAP3']:
                ord_param += f';limitPrice={price};participateRate=0;tradingStyle={tradingstyle}'
            elif algo_type in ['KF_POV_Core']:
                ord_param += f';maxRate={participate}'
            elif algo_type in ['VolumeInline3']:
                ord_param += f';participateRate={participate}'
            elif algo_type in ['SmartVolumeInline3']:
                ord_param += f';limitPrice=0;participateRate={participate};tradingStyle={tradingstyle};iWouldPrice=0;iWouldMax=0'
            #elif algo_type in ['KF_VWAP_Plus', 'KF_TWAP_Plus']:
            #s    ord_param += f';beginDate'

            insert_row = [oid, acct_type, account_id, stock_code, vol, side, "algo", ord_param]
            writer.writerow(insert_row)
            self.logger.info(f"[req_buy_order] insert_success (oid){oid} (mid){mid} (param){insert_row}")
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        final_filename = f"{self.insert_order_path}\\InPut\\1_buy.{formatted_time}.csv"
        shutil.move(temp_filename, final_filename)
        db_id = obj['_id']
        order_dict = {
            'oid' : oid,
            'mid' : mid,
            "db_id" : db_id,
            "ticker" : obj['ticker'],
            "side" : side,
            "volume" : order_vol,
            "accountName" : target_account_name,
            "order_type" : str(obj['executionPlan']["order_type"]),
            "start_time" : str(obj['executionPlan']["start_time"]),
            "end_time" : str(obj['executionPlan']["end_time"])
        }
        target_collection =  self.order_info_db[acc]['target']
        delete_query = {
                    '_id' : db_id
                }
        delete_res = target_collection.delete_one(delete_query)
        self.logger.info(f"[on_req_buy_order] delete (target){obj}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        local_id_list = []
        local_ref_list = []
        db_msg = {
                    "oid" : oid,
                    "mid" : mid,
                    "traded_vol" : 0,
                    "traded_amt" : 0,
                    "local_ids" : local_id_list,
                    "local_refs" : local_ref_list,
                    "order_msg": order_dict
                }
        query = {"oid": oid}
        res = atx_order_collection.replace_one(query, db_msg, True)
        self.logger.info(f"[on_req_order_insert] insert_cat_order_info (res){res} (msg){db_msg}")

        self.sids.append(mid)

        self.sid_to_req[mid] = order_dict
        self.oid_to_req[oid] = order_dict
        self.oid_to_mid[oid] = mid
        self.db_id_to_oid[db_id] = oid
        self.oid_to_acc[oid] = acc
        self.oid_to_traded[oid] = 0
        self.oid_to_traded_money[oid] = 0
        self.oid_to_local_ids[oid] = local_id_list
        self.oid_to_ref_list[oid] = local_ref_list

    @MongoClientTradeGateway.error_handler
    def req_sell_order_insert(self, obj):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        temp_filename = self.insert_order_path + '\\InPut_temp\\' + '1_sell.' + formatted_time + '.csv'
        with open(temp_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            target_account_name = obj['accountName']
            acc = self.target_account_names_to_acc[target_account_name]
            account_id = self.account_id[acc].split('.')[0]
            acct_type = self.acct_type[acc]

            oid = str(self.gen_order_id())[4:] #cats limit 16
            mid = str(obj['mid'])
            vol =  int(obj["volume"])
            price = 0.0
            if not obj.get('price') is None:
                price = float(obj['price'])

            side = '2'
            tradingstyle = 2
            if not obj.get('tradingstyle') is None:
                tradingstyle = int(obj['tradingstyle'])
            participate = 0.1
            if not obj.get('participate') is None:
                participate = float(obj['participate'] / 100)
            order_vol = f'{vol:d}'
            int_stock_code = int(obj['ticker'])
            stock_code = get_exchange_from_ticker(int_stock_code)
            algo_type = decode_ordtype(obj['executionPlan']['order_type'])
            begin_time  = str(obj['executionPlan']['start_time']).replace(':','')
            end_time = str(obj['executionPlan']['end_time']).replace(':','')
            ord_param = f'AlgoType={algo_type};beginTime={begin_time};endTime={end_time}'

            if algo_type in ['VWAP', 'TWAP']:
                ord_param += f';limitPrice={price};participateRate=0;tradingStyle={tradingstyle}'
            elif algo_type in ['VWAP3', 'TWAP3', 'SmartTWAP3', 'SmartVWAP3']:
                ord_param += f';limitPrice={price};participateRate=0;tradingStyle={tradingstyle}'
            elif algo_type in ['KF_POV_Core']:
                ord_param += f';maxRate={participate}'
            elif algo_type in ['VolumeInline3']:
                ord_param += f';participateRate={participate}'
            elif algo_type in ['SmartVolumeInline3']:
                ord_param += f';limitPrice=0;participateRate={participate};tradingStyle={tradingstyle};iWouldPrice=0;iWouldMax=0'

            insert_row = [oid, acct_type, account_id, stock_code, vol, side, "algo", ord_param]
            writer.writerow(insert_row)
            self.logger.info(f"[req_sell_order] insert_success (oid){oid} (mid){mid} (param){insert_row}")
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        final_filename = f"{self.insert_order_path}\\InPut\\1_sell.{formatted_time}.csv"
        shutil.move(temp_filename, final_filename)
        db_id = obj['_id']
        order_dict = {
            'oid' : oid,
            'mid' : mid,
            "db_id" : db_id,
            "ticker" : obj['ticker'],
            "side" : side,
            "volume" : vol,
            "accountName" : target_account_name,
            "order_type" : str(obj['executionPlan']["order_type"]),
            "start_time" : str(obj['executionPlan']["start_time"]),
            "end_time" : str(obj['executionPlan']["end_time"])
        }
        sell_target_collection =  self.order_info_db[acc]['sell_target']
        delete_query = {
                    '_id' : db_id
        }
        delete_res = sell_target_collection.delete_one(delete_query)
        self.logger.info(f"[on_req_sell_order] delete (target){obj}")
        atx_order_collection = self.order_info_db[acc]['atx_order']
        local_id_list = []
        local_ref_list = []
        db_msg = {
                    "oid" : oid,
                    "mid" : mid,
                    "traded_vol" : 0,
                    "traded_amt" : 0,
                    "local_ids" : local_id_list,
                    "local_refs" : local_ref_list,
                    "order_msg": order_dict
                }
        query = {"oid": oid}
        res = atx_order_collection.replace_one(query, db_msg, True)
        self.logger.info(f"[on_req_order_insert] insert_cat_order_info (res){res} (msg){db_msg}")

        self.sids.append(mid)
        self.sid_to_req[mid] = order_dict
        self.oid_to_req[oid] = order_dict
        self.oid_to_mid[oid] = mid
        self.db_id_to_oid[db_id] = oid
        self.oid_to_acc[oid] = acc
        self.oid_to_traded[oid] = 0
        self.oid_to_traded_money[oid] = 0
        self.oid_to_local_ids[oid] = local_id_list
        self.oid_to_ref_list[oid] = local_ref_list
    #使用的是执行统计输出，统计的是算法母单
    @MongoClientTradeGateway.error_handler
    def monitor_algo_order_update(self):
        while not self.is_stopped:
            print ("[monitor_algo_order_update]")
            self.logger.info('[monitor_algo_order_update] start')
            order_filename = self.recv_msg_dir + '\\' + FILES.ALGO_ORDERS + '.dbf'
            rtn_order_table = dbf.Table(filename=order_filename,codepage='utf8', on_disk=True)
            with rtn_order_table.open(mode=dbf.READ_WRITE):
                #algo_index = self.algo_index
                if self.algo_index == len(rtn_order_table) - 1 or len(rtn_order_table) == 0:
                    self.logger.info(f"[monitor_order_update] not_change (len){len(rtn_order_table)}")
                    self.logger.info('[monitor_algo_order_update] end')
                    time.sleep(self.order_scan_interval)
                    continue
                while rtn_order_table[self.algo_index+1] is not rtn_order_table.last_record:
                    self.algo_index += 1
                    record = rtn_order_table[self.algo_index]
                    self.update_algo_order(record)
                self.algo_index += 1
                self.update_algo_order(rtn_order_table.last_record)
            self.logger.info('[monitor_algo_order_update] end')
            time.sleep(self.order_scan_interval)
    @MongoClientTradeGateway.error_handler
    def update_algo_order(self,record):
        oid = str(record.ID).strip(' ')
        if oid == "":
            self.logger.warning(f"[update_algo_order] no_oid (record){record}")
            return
        acc = ""
        mid = ""
        order_dict = {}
        algo_id = str(record.INSTANCEID).strip(' ')
        #order_no 返回用
        self.algoid_to_oid[algo_id] = oid
        self.oid_to_algoid[oid] = algo_id
        if not oid in self.oid_to_acc: #shut_down or other problem
            acct_type = str(record.ACCT_TYPE).strip(' ')
            trade_acc = str(record.ACCT).strip(' ') + '.' + acct_type
            if trade_acc not in self.account_id_to_acc:
                self.logger.error(f"[update_algo_order] can't_parse_trade_acc {trade_acc}")
                return
            acc = self.account_id_to_acc[trade_acc]
            order_info_collection = self.order_info_db[acc]['atx_order'] 
            query = {'oid' : oid}
            order_info_target = order_info_collection.find_one(query)
            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                mid = order_info_target['mid']
                ref_list = order_info_target['local_refs']
                self.oid_to_traded_money[oid] = 0
                self.oid_to_traded[oid] = 0
                self.oid_to_mid[oid] = mid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref_list[oid] = ref_list
            else:
                self.logger.error(f"[update_algo_order] can't_find_oid (oid){oid}")
                return
        else:
            acc = self.oid_to_acc[oid]
            order_dict = self.oid_to_req[oid]
            mid = self.oid_to_mid[oid]
        atx_order_msg = {
                    "algo_id" : algo_id
                }
        query = {"oid": oid}
        self.update_atx_order(acc, query, atx_order_msg)
        ticker = record.Symbol.split('.')[0]
        exchange = decode_exchange_id(str(record.Symbol.split('.')[1]).strip(' '))
        volume = int(order_dict['volume'])
        price = float(str(record.FILLPRICE).strip(' '))

        tg_name = order_dict['accountName'].split('@')[0]
        account_name = order_dict['accountName'].split('@')[1]
        order_type = order_dict['order_type']
        start_time = order_dict['start_time']
        end_time = order_dict['end_time']

        target_type = side_to_target_type(str(order_dict['side']))
        filled_vol = int(str(record.QTY_FILLED).strip(' '))

        status = decode_cats_status(int(str(record.STATUS).strip(' ')), volume, filled_vol)
        replace_collection = self.tradelog_db[acc]['order']
        query = {'mid':mid, '_id': int(oid)}
        replace_target = replace_collection.find_one(query)
        if not replace_target is None:
            utc_update_time = replace_target['dbTime']
            order_msg = {
                    "_id": int(oid),
                    "tg_name": tg_name,  # 对应 account_info._id
                    "exchange": exchange, # 对应 tlclient.trader.constant 包 ExchangeID
                    "target_type": target_type,    # 'buy' | 'sell' | 'limit_sell'
                    "volume": volume,  # 订单的volume
                    "price": price,  # 实际成交均价
                    "order_type": order_type,  # algotype:200,目前没有其他的
                    "ticker": ticker,
                    "mid": mid,  # target中对应的 母单sid
                    "accountName": account_name,  # 对应 account_info.account_name
                    "algo_args": {  # 具体的算法参数
                        "order_type": order_type,  # 此柜台不使用下单时要求的算法
                        "start_time": start_time,
                        "end_time": end_time
                    },
                    "status": status,  # 'active' | 'filled' | 'canceled'
                    "filled_vol": filled_vol,  # 实际成交的 volume
                    "dbTime": utc_update_time,
            }

            res = replace_collection.replace_one(query, order_msg, True)
            self.logger.info(f"[update_algo_order]  replace {res.matched_count} documents (res):{res.upserted_id} (order_msg){order_msg}")
        else:
            str_update_time = str(str(record.WRITE_TIME).strip(' ').split('@')[1])[:-4] #去除毫秒部分
            update_time = datetime.strptime(str_update_time, "%Y-%m-%d %H:%M:%S")
            utc_update_time = update_time - timedelta(hours=8)
            #utc_update_time = replace_target['dbTime']
            order_msg = {
                    "_id": int(oid),
                    "exchange": exchange,
                    "target_type": target_type,    # 'buy' | 'sell' | 'limit_sell'
                    "volume": volume,  # 订单的volume
                    "price": price,  # 实际成交均价
                    "order_type": order_type,  # algotype:200,目前没有其他的
                    "ticker": ticker,
                    "mid": mid,  # target中对应的 母单sid
                    "accountName": account_name,  # 对应 account_info.account_name
                    "algo_args": {  # 具体的算法参数
                        "order_type": order_type,  # 此柜台不使用下单时要求的算法
                        "start_time": start_time,
                        "end_time": end_time
                    },
                    "status": status,  # 'active' | 'filled' | 'canceled'
                    "filled_vol": filled_vol,  # 实际成交的 volume
                    "dbTime": utc_update_time,
            }
            res = replace_collection.replace_one(query, order_msg, True)
            self.logger.info(f"[update_algo_order] (res){res} (order_msg){order_msg}")
        with self.algo_cache_lock:
            if algo_id in self.algoid_to_order_record:
                for record in self.algoid_to_order_record[algo_id]:
                    self.update_order(record)
                del self.algoid_to_order_record[algo_id]
    #使用的是执行统计输出，统计的是算法母单
    #0 已报 #2 filled 全成 #4 canceled #8 rejected
    @MongoClientTradeGateway.error_handler
    def monitor_order_update(self):
        while not self.is_stopped:
            print ("[monitor_order_update]")
            self.logger.info('[monitor_order_update] start')
            order_filename = self.recv_msg_trade_dir + '\\' + FILES.ORDERS + '.dbf'
            rtn_order_table = dbf.Table(filename=order_filename,codepage='utf8', on_disk=True)
            rtn_order_table.open(mode=dbf.READ_WRITE)
            #order_index = self.order_index
            if self.order_index == len(rtn_order_table) - 1 or len(rtn_order_table) == 0:
                self.logger.info(f"[monitor_order_update] not_change (len){len(rtn_order_table)}")
                self.logger.info('[monitor_order_update] end')
                time.sleep(self.order_scan_interval)
                continue

            while rtn_order_table[self.order_index+1] is not rtn_order_table.last_record:
                self.order_index += 1
                record = rtn_order_table[self.order_index]
                order_status = int(str(record.ORD_STATUS).strip(' '))
                if order_status in [5, 6]:
                    pass
                    #self.logger.warning(f"[monitor_order_update] order_rejected! (msg){str(record.ERR_MSG).strip(' ')}")        #self.logger.warn(f"[monitor_order_update] order_rejected!")
                elif order_status in [0, 1, 2, 3, 4]:
                    self.update_order(record)
                else:
                    self.logger.info("[monitor_order_update] order_not_finished_or_not_init")

            self.order_index += 1
            record = rtn_order_table[self.order_index]
            order_status = int(str(record.ORD_STATUS).strip(' '))
            if order_status in [5, 6]:
                self.logger.warning(f"[monitor_order_update] order_rejected! (msg){str(record.ERR_MSG).strip(' ')}")
            elif order_status in [0, 1, 2, 3, 4]:
                self.update_order(record)
            rtn_order_table.close()
            self.logger.info('[monitor_order_update] end')
            time.sleep(self.order_scan_interval)
    @MongoClientTradeGateway.error_handler
    def update_order(self,record):
        algo_id = str(record.CORR_ID).strip(' ')
        if algo_id not in self.algoid_to_oid:
            self.logger.warning(f'[update_order] can not match algo_id {algo_id}')
            with self.algo_cache_lock:
                if algo_id in self.algoid_to_order_record:
                    self.algoid_to_order_record[algo_id].append(record)
                else:
                    self.algoid_to_order_record[algo_id] = [record]
            return
        oid = self.algoid_to_oid[algo_id]
        acc = ""
        mid = ""
        order_dict = {}
        mudan_id = str(record.ORD_NO).strip(' ') #orderno 返回用
        if not oid in self.oid_to_acc: #shut_down or other problem
            acct_type = str(record.ACCT_TYPE).strip(' ')
            trade_acc = str(record.ACCT).strip(' ') + '.' + acct_type
            if trade_acc not in self.account_id_to_acc:
                self.logger.error(f"[update_order] can't_parse_trade_acc {trade_acc}")
                return
            acc = self.account_id_to_acc[trade_acc]
            order_info_collection = self.order_info_db[acc]['atx_order']
            query = {'oid' : oid}
            order_info_target = order_info_collection.find_one(query)
            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                mid = order_info_target['mid']
                ref_list = order_info_target['local_refs']
                self.oid_to_traded_money[oid] = 0
                self.oid_to_traded[oid] = 0
                self.oid_to_mid[oid] = mid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref_list[oid] = ref_list
                self.oid_to_algoid[oid] = algo_id
            else:
                self.logger.error(f"[update_order] can't_find_oid (oid){oid}")
                return
        else:
            acc = self.oid_to_acc[oid]
            order_dict = self.oid_to_req[oid]
            mid = self.oid_to_mid[oid]
        self.ref_to_oid[mudan_id] = oid
        if mudan_id not in self.oid_to_ref_list[oid]:
            self.oid_to_ref_list[oid].append(mudan_id)
            atx_query = {'oid' : oid}
            update_msg = {
                "local_refs" : self.oid_to_ref_list[oid]
            }
            self.update_atx_order(acc, atx_query, update_msg)
        with self.order_cache_lock:
            if mudan_id in self.mudanid_to_trade_record:
                for record in self.mudanid_to_trade_record[mudan_id]:
                    self.on_trade_msg(record)
                del self.mudanid_to_trade_record[mudan_id]

    @MongoClientTradeGateway.error_handler
    def monitor_algo_order_insert(self):
        while not self.is_stopped:
            print ("[monitor_algo_order_insert]")
            for acc in self.accounts_run:
                target_account_name = self.target_account_names[acc]
                buy_query = {"accountName": target_account_name}
                buy_targets = self.order_info_db[acc]["target"].find(buy_query)
                if buy_targets.count() == 0:
                    self.logger.warning(f"[monitor_buy_order] no_buy_target (acc){acc}")
                    continue
                for target in buy_targets:
                    if target['_id'] not in self.order_db_ids:
                        self.order_db_ids.append(target['_id'])
                        self.req_buy_order_insert(target)
                    else:
                        self.logger.warning(f"[monitor_algo_order_insert] _id_existed (_id){target['_id']}")
            for acc in self.accounts_run:
                target_account_name = self.target_account_names[acc]
                sell_query = {"accountName": target_account_name}
                sell_targets = self.order_info_db[acc]["sell_target"].find(sell_query)
                if sell_targets.count() == 0:
                    self.logger.warning(
                        f"[monitor_sell_order] no_sell_target (acc){acc}")
                    continue
                for sell_target in sell_targets:
                    if sell_target['_id'] not in self.sell_order_db_ids:
                        self.sell_order_db_ids.append(sell_target['_id'])
                        self.req_sell_order_insert(sell_target)
                    else:
                        self.logger.warning(f"[monitor_algo_order_insert] _id_existed (_id){sell_target['_id']}")
            time.sleep(self.scan_interval)
    #得到的数据 类似于子单的rtn_order
    @MongoClientTradeGateway.error_handler
    def monitor_trade_update(self):
        while not self.is_stopped:
            print("[monitor_trade_update]")
            self.logger.info("[monitor_trade_update] start")
            trade_filename = self.recv_msg_trade_dir + '\\' + FILES.TRADES + '.dbf'
            rtn_trade_table = dbf.Table(filename=trade_filename,codepage='utf8', on_disk=True)
            with rtn_trade_table.open(mode=dbf.READ_WRITE):
                #trade_index = self.trade_index
                if self.trade_index == len(rtn_trade_table)-1 or len(rtn_trade_table) == 0:
                    self.logger.info(f"[monitor_trade_update] not_change (len){len(rtn_trade_table)}")
                    self.logger.info("[monitor_trade_update] end")
                    time.sleep(self.trade_scan_interval)
                    continue
                else:
                    while rtn_trade_table[self.trade_index +1] is not rtn_trade_table.last_record:
                        self.trade_index += 1
                        record = rtn_trade_table[self.trade_index]
                        self.on_trade_msg(record)
                    self.trade_index += 1
                    record = rtn_trade_table[self.trade_index]
                    self.on_trade_msg(record)
            self.logger.info("[monitor_trade_update] end")
            time.sleep(self.trade_scan_interval)

    @MongoClientTradeGateway.error_handler
    def on_trade_msg(self, record):
        fill_qty = int(str(record.FILLQTY).strip(' '))
        fill_price = float(str(record.FILLPRICE).strip(' '))
        if fill_qty == 0 or fill_price == 0:
            self.logger.warning(f"[on_trade_msg] nothing_traded")
            return
        mudan_id = str(record.ORDERNO).strip(' ')
        if mudan_id == "":
            self.logger.warning(f"[on_trade_msg] no_mid (mudan_id){mudan_id}")
            return
        if mudan_id not in self.ref_to_oid:
            self.logger.warning(f"[on_trade_msg] no_oid (mudan_id){mudan_id}")
            with self.order_cache_lock:
                if mudan_id not in self.mudanid_to_trade_record:
                    self.mudanid_to_trade_record[mudan_id] = [record]
                else:
                    self.mudanid_to_trade_record[mudan_id].append(record)
            return
        oid = self.ref_to_oid[mudan_id]
        acc = ""
        mid = ""
        order_dict = {}
        if not oid in self.oid_to_acc: #shut_down or other problem
            acct_type = str(record.ACCTTYPE).strip(' ')
            trade_acc = str(record.ACCOUNT).strip(' ') + '.' + acct_type

            acc = self.account_id_to_acc[trade_acc]
            order_info_collection = self.order_info_db[acc]['atx_order']
            query = {'oid' : oid}
            order_info_target = order_info_collection.find_one(query)

            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                mid = order_info_target['mid']
                ref_list = order_info_target['local_refs']
                self.oid_to_local_ids[oid] = order_info_target['local_ids']
                self.oid_to_traded[oid] = 0
                self.oid_to_traded_money[oid] = 0
                self.oid_to_mid[oid] = mid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref_list[oid] = ref_list
            else:
                self.logger.error(f"[on_trade_msg] can't_find_oid (oid){oid}")
                return
        else:
            acc = self.oid_to_acc[oid]
            order_dict = self.oid_to_req[oid]
            mid = self.oid_to_mid[oid]
        _id = str(record.TRADENO).strip(' ')
        if _id in self.oid_to_local_ids[oid]:
            #self.logger.warning(f"[on_trade_msg] duplicate_trade_msg (record){record}")
            return
        else:
            self.oid_to_local_ids[oid].append(_id)#外部委托编号，出现在这个位置主要是凑数
        ticker = str(record.Symbol).split('.')[0]
        exchange = decode_exchange_id(str(record.Symbol).split('.')[1].strip(' '))
        traded_vol = fill_qty
        traded_price = fill_price
        trade_amt = float(traded_price * traded_vol)
        order_type = str(record.TRDTYPE).strip(' ')
        target_type = decode_cats_side(str(record.TRADSIDE).strip(' '))
        if target_type == 1 or target_type == 3:
            self.oid_to_traded_money[oid] += trade_amt
            self.oid_to_traded[oid] += traded_vol
        elif target_type == 2:
            self.oid_to_traded_money[oid] -= trade_amt
            self.oid_to_traded[oid] -= traded_vol
        entrust_vol = int(order_dict['volume'])
        entrust_price = 0 #没有
        dbTime = datetime.now(timezone.utc)
        str_trade_time = str(record.TIME).strip(' ')[:-4]
        trade_time = datetime.strptime(str_trade_time, "%Y-%m-%d %H:%M:%S")
        utc_trade_time = trade_time - timedelta(hours=8)
        target_account_name = order_dict['accountName']
        if target_account_name not in self.target_account_names_to_acc: #切换账号了，缓存无法使用
            return
        acc = self.target_account_names_to_acc[target_account_name]
        log_account_name = order_dict['accountName'].split('@')[1]
        tg_name =  order_dict['accountName'].split('@')[0]
        trade_collection = self.tradelog_db[acc]['tg_trade']
        replace_trade_query = { "trade_ref": _id, "oid" : int(oid)}
        trade_target = trade_collection.find_one(replace_trade_query)
        if not trade_target is None:
            dbTime = trade_target['dbTime']
        db_msg = {
                    "trade_ref": _id, # 用的是非凸的子单order_id 经测试之前用的trade_ref 经常为空
                    "oid": int(oid),
                    "tg_name": tg_name,
                    "exchange": exchange,
                    "ticker": ticker,
                    "traded_vol": traded_vol,
                    "traded_price": traded_price,
                    "order_type": order_type,
                    "side": target_type,  # 对应 tlclient.trader.constant 包 Side
                    "entrust_vol": entrust_vol,
                    "entrust_price": entrust_price,
                    "dbTime": dbTime,
                    "mid": mid,  # 对应订单中的 mid
                    "commission": 0,  # 没有
                    "trade_time": utc_trade_time,  # 具体交易时间
                    "accountName":  log_account_name,  # 对应 account_info.account_name
                }

        db_res = trade_collection.replace_one(replace_trade_query, db_msg, True)
        self.logger.info(
            f"[rtn_trade] (db_res){db_res} (db_msg){db_msg} (traded_vol){traded_vol} (traded_price){traded_price}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        atx_order_msg = {
                    "local_ids" : self.oid_to_local_ids[oid],
                }
        query = {"oid": oid}
        res = self.update_atx_order(acc, query, atx_order_msg)
        self.logger.info(f"[on_trade_msg] update_cat_order_info (res){res} (msg){atx_order_msg}")
    @MongoClientTradeGateway.error_handler
    def monitor_dbf_pos(self):
        print ("[monitor_dbf_pos]")
        while not self.is_stopped:
            order_filename = self.recv_msg_dir + '\\' + FILES.POSITIONS  + '.dbf'
            position_table = dbf.Table(filename=order_filename,codepage='utf8', on_disk=True)
            for acc in self.accounts_run:
                tg_position_collection = self.order_info_db[acc]['tg_equity_position']
                remove = tg_position_collection.delete_many({'account_name': self.log_account_names[acc], 'tg_name': self.target_account_names[acc]})
                self.logger.info(f"[monitor_dbf_pos] delete_old_position_info (remove){remove} ")
            with position_table.open(mode=dbf.READ_WRITE):
                pos_index = -1
                while position_table[pos_index+1] is not position_table.last_record:
                    pos_index += 1
                    record = position_table[pos_index]
                    self.update_dbf_position(record)

                pos_index += 1
                self.update_dbf_position(position_table.last_record)
            time.sleep(self.pos_interval)

    def update_dbf_position(self, record):
        a_type = str(record.A_TYPE).strip(' ')
        if a_type not in ['P']: #其他类型
            return

        acct_type = str(record.ACCT_TYPE).strip(' ')
        trade_acc = str(record.ACCT).strip(' ') + '.' + acct_type

        if trade_acc not in self.account_id_to_acc:
            self.logger.warning(f"[update_dbf_position] can't_parse_trade_acc {trade_acc}")
            return
        acc = self.account_id_to_acc[trade_acc]
        account_name = self.log_account_names[acc]
        tg_name = self.target_account_names[acc]
        ticker = record.S1.split('.')[0].strip(' ')
        exchange = decode_exchange_id(str(record.S1.split('.')[1]).strip(' '))
        td_pos = int(str(record.S2).strip(' '))
        yd_pos = int(str(record.S3).strip(' '))
        #new_id = tg_name + '@' + account_name + '@' + ticker
        pos_collection = self.order_info_db[acc]['tg_equity_position']
        query = {'tg_name':tg_name, 'account_name': account_name, "ticker": ticker}
        pos_msg = {
                "account_name": account_name,
                "tg_name": tg_name,
                "ticker": ticker,
                "exchange": exchange,
                "direction": "long", # long/short，没有short部分就只存long部分
                "avail_pos": yd_pos, # 昨仓
                "total_pos": td_pos, # 今仓，TODO 需要统计下不同券商盘中，对于卖出的position 是直接从 yd_pos 上减，还是在 td_pos 增加一个负的值。
                "cost": 0, #没有
                "type": "stock",
                "updated_at": datetime.utcnow()
              }
        res = pos_collection.replace_one(query, pos_msg, True)
        self.logger.info(f"[update_dbf_position] (res){res.modified_count} (order_msg){pos_msg}")
    def start(self):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        _msg = f"[atx_login] {self.log_name} start (time){datetime.now()}"
        self.send_to_user(logger=self.logger, url_list=self.url_list, msg=_msg)
        self.monitor()

    def close(self):
        self.position_order_table.close()
        return super().close()
    
    def join(self):
        while self.is_stopped == False:
            time.sleep(0.01)
            if self.is_stopped:
                self.logger.info(
                    "[close] main thread is stopped,active_orders message will lose")
                self.close()

if __name__ == "__main__":

    sys.stdout.reconfigure(encoding='utf-8')
    description = "cat_uni_server,get target from mongodb and serve cat"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e' , '--end_time', dest='end_time', default='15:30')
    _config_filename = "C:/Users/Administrator/Desktop/cat_uni_batandconfig/cat_uni_server_config.json"
    parser.add_argument('-p', '--config_filepath', dest= 'config_filepath', default= _config_filename)

    args = parser.parse_args()
    print (f"(args){args}")

    td = CatServer(args.config_filepath, args.end_time)
    td.start()

    td.join()