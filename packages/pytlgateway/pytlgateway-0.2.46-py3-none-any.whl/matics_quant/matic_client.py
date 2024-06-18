# encoding: utf-8
import sys
import json
import argparse
import  datetime
import socket                             #导入socket模块
import signal
import threading
import time
import csv
from datetime import date,datetime, timezone, timedelta
from ..mongo_client_gateway import MongoClientTradeGateway
from .constants import (GATEWAY_NAME, FILES)
from .utils import (decode_algo_type, date_to_str, decode_exchange_id, transfer_order_side, decode_mquant_status, side_to_target_type, check_split, decode_exchange_id, encode_exchange_id)
from .string_buffer import TcpStringBuffer

class MquantServer(MongoClientTradeGateway):
    def __init__(self, config_filename, end_time):
        MongoClientTradeGateway.__init__(self, config_filename, end_time, GATEWAY_NAME)
        self.tcp_socket_init = False
        self.tcp_socket = None
        self.conn = None
        self.load_tg_setting(config_filename)
        self.insert_orders = {}
        self.oid_to_ref = {}
        self.oid_to_traded_vol = {}
        self.oid_to_traded_amt = {}
        self.mid_to_req = {}
        self.oid_to_req = {}
        self.oid_to_mid = {}
        self.oid_to_acc = {}
        self.db_id_to_oid = {}
        self.ref_to_oid = {}
        self.oid_to_local_ids = {}
        self.tcp_string_buffer = TcpStringBuffer()
        self.tcp_msg_lock = threading.Lock()
        self.order_msg_lock = threading.Lock()
        self.my_today = datetime.strftime(datetime.now(), "%Y-%m-%d")


    # 创建TCP连接
    def create_tcp_client(self):
        if self.tcp_socket_init is False:
            self.tcp_socket = socket.socket()                        #创建套接字
            self.tcp_socket.connect((self.tcp_host,self.tcp_port))   #主动初始化TCP服务器连接
            self.tcp_socket_init = True

    #发送TCP数据
    @MongoClientTradeGateway.error_handler
    def tcp_send(self, data):
        if self.tcp_socket_init is True:
            self.tcp_string_buffer.push(data)

    @MongoClientTradeGateway.error_handler
    def tcp_recv(self):
        while not self.is_stopped:
            if self.tcp_socket_init is True:
                try:
                    #接受对方发送过来的数据，最大接受4096字节
                    recv_data = self.tcp_socket.recv(4096).decode()          #接收数据
                    self.tcp_string_buffer.receive(recv_data)
                    self.logger.info(f'recv msg: {recv_data}')
                except json.JSONDecodeError as e:
                    self.logger.error(f'recv failed {recv_data} error:{e}')
                except ConnectionAbortedError as e:
                    self.logger.error(f'connection broken error: {e}')
    @MongoClientTradeGateway.error_handler
    def handle_msg(self):
        while not self.is_stopped:
            if not self.tcp_string_buffer.is_recv_str_empty():
                msg_list = self.tcp_string_buffer.get_recv()
                for msg in msg_list:
                    self.on_message(msg)
            time.sleep(1)
    @MongoClientTradeGateway.error_handler
    def handle_send_msg(self):
        while not self.is_stopped:
            if not self.tcp_string_buffer.is_send_str_empty():
                send_data = self.tcp_string_buffer.get_send()
                self.tcp_socket.sendall(send_data.encode())
    # tcp_socket.close()    #关闭套接字
    def load_tg_setting(self, config_filename):
        f = open(config_filename, encoding='gbk')
        setting = json.load(f)
        self.recv_msg_path = setting['recv_msg_path']
        self.recv_msg_path = self.recv_msg_path.replace('/', '//')
        self.tcp_host = setting['tcp_host']
        self.tcp_port = setting['tcp_port']
        self.account_type = {}
        for acc in self.accounts_run:
            self.account_type[acc] = setting['accounts'][acc]['account_type']

    @MongoClientTradeGateway.error_handler
    def monitor_algo_limit_order_insert(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                target_account_name = self.target_account_names[acc]
                buy_query = {'accountName': target_account_name}
                targets_collection = self.order_info_db[acc]['limit_stop']
                targets = targets_collection.find(buy_query)
                if targets.count() == 0:
                    self.logger.warning(f'[monitor_algo_order_insert] no_buy_target (acc){acc}')
                    continue
                for target in targets:
                    if target['_id'] not in self.order_db_ids:
                        self.order_db_ids.append(target['_id'])
                        self.req_limit_order_insert(target)
                    else:
                        self.logger.warning(f'[monitor_algo_order_insert] _id_existed (_id){target["_id"]}')
    @MongoClientTradeGateway.error_handler
    def req_limit_order_insert(self, obj):
        target_account_name = obj['accountName']
        acc = self.target_account_names_to_acc[target_account_name]
        ticker = str(obj['ticker']) + encode_exchange_id(obj['ticker'])
        account_id = self.account_id[acc]
        mid = str(obj['mid'])
        vol = int(obj['volume'])
        symbol_type = 0
        price = 0.0
        if 'price' in obj:
            price = float(obj['price'])
        entrust_type = 9
        if not obj.get('financingBuy') is None :
            financial_buy_s = obj["financingBuy"]
            if financial_buy_s == True:
                entrust_type = 6
            else:
                entrust_type = 9
        account_type = self.account_type[acc]
        volume_list = check_split(vol, price, symbol_type)
        for order_vol in volume_list:
            oid = str(self.gen_order_id())
            side = obj['direction']

            msg_type = 'req_limit_order'
            output_dict = {
                'msg_type' : msg_type,
                'oid' : oid,
                'price' : price,
                'entrust_type': entrust_type,
                "account_type": account_type,
                'fund_account' : account_id,
                'side' : str(side),
                'ticker': ticker,
                'volume' : order_vol
            }
            self.tcp_send(output_dict)
            db_id = obj['_id']
            order_dict = {
                'oid' : oid,
                'mid' : mid,
                'db_id' : db_id,
                'ticker' : ticker,
                'side' : side,
                'volume' : order_vol,
                'account_name' : target_account_name,
                'order_type' : 'limit',
                'start_time' : '0',
                'end_time' : '0' #凑数
            }

            self.logger.info(f'[req_plain_order_insert] insert_success (oid){oid} (mid){mid} (param){output_dict}')
        local_id_list = []
        with self.order_msg_lock:
            self.mid_to_req[mid] = order_dict
            self.oid_to_req[oid] = order_dict
            self.oid_to_mid[oid] = mid
            self.db_id_to_oid[db_id] = oid
            self.oid_to_acc[oid] = acc
            self.oid_to_traded_vol[oid] = 0
            self.oid_to_traded_amt[oid] = 0
            self.oid_to_local_ids[oid] = local_id_list
        target_collection =  self.order_info_db[acc]['limit_stop']
        query = {
                    '_id' : db_id
                }
        delete_res = target_collection.delete_one(query)
        self.logger.info(f'[on_req_order] used (target){obj}')

    @MongoClientTradeGateway.error_handler
    def monitor_algo_order_insert(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                target_account_name = self.target_account_names[acc]
                buy_query = {'accountName': target_account_name}
                targets_collection = self.order_info_db[acc]['target']
                targets = targets_collection.find(buy_query)
                if targets.count() == 0:
                    self.logger.warning(f'[monitor_algo_order_insert] no_buy_target (acc){acc}')
                    continue
                for target in targets:
                    if target['_id'] not in self.order_db_ids:
                        self.order_db_ids.append(target['_id'])
                        self.req_order_insert(target, True)
                    else:
                        self.logger.warning(f'[monitor_algo_order_insert] _id_existed (_id){target["_id"]}')
            for acc in self.accounts_run:
                target_account_name = self.target_account_names[acc]
                buy_query = {'accountName': target_account_name}
                targets_collection = self.order_info_db[acc]['sell_target']
                targets = targets_collection.find(buy_query)
                if targets.count() == 0:
                    self.logger.warning(f'[monitor_algo_order_insert] no_sell_target (acc){acc}')
                    continue
                for target in targets:
                    if target['_id'] not in self.order_db_ids:
                        self.order_db_ids.append(target['_id'])
                        self.req_order_insert(target, False)
                    else:
                        self.logger.warning(f'[monitor_algo_order_insert] _id_existed (_id){target["_id"]}')

            time.sleep(self.scan_interval)

    @MongoClientTradeGateway.error_handler
    def req_plain_order_insert(self, obj):
        target_account_name = obj['accountName']
        acc = self.target_account_names_to_acc[target_account_name]
        account_id = self.account_id[acc]
        mid = str(obj['mid'])
        vol = int(obj['volume'])
        ticker = str(obj['ticker']) + encode_exchange_id(obj['ticker'])
        account_type = self.account_type[acc]
        symbol_type = 0
        price = 0.0
        if 'price' in obj:
            price = float(obj['price'])
        volume_list = check_split(vol, price, symbol_type)
        for order_vol in volume_list:
            oid = str(self.gen_order_id())
            side = obj['direction']

            msg_type = 'req_plain_order'
            output_dict = {
                'msg_type' : msg_type,
                'oid' : oid,
                'price' : price,
                'fund_account' : account_id,
                'side' : str(side),
                'account_type': account_type,
                'ticker': ticker,
                'volume' : order_vol,

            }
            self.tcp_send(output_dict)
            db_id = obj['_id']
            order_dict = {
                'oid' : oid,
                'mid' : mid,
                'db_id' : db_id,
                'ticker' : ticker,
                'side' : side,
                'volume' : order_vol,
                'account_name' : target_account_name,
                'order_type' : str(obj['order_type']),
                'start_time' : str(obj['start_time']),
                'end_time' : str(obj['end_time'])
            }

            self.logger.info(f'[req_plain_order_insert] insert_success (oid){oid} (mid){mid} (param){output_dict}')
        local_id_list = []
        with self.order_msg_lock:
            self.mid_to_req[mid] = order_dict
            self.oid_to_req[oid] = order_dict
            self.oid_to_mid[oid] = mid
            self.db_id_to_oid[db_id] = oid
            self.oid_to_acc[oid] = acc
            self.oid_to_traded_vol[oid] = 0
            self.oid_to_traded_amt[oid] = 0
            self.oid_to_local_ids[oid] = local_id_list
        target_collection =  self.order_info_db[acc]['limit_stop']
        query = {
                    '_id' : db_id
                }
        delete_res = target_collection.delete_one(query)
        self.logger.info(f'[on_req_order] used (target){obj}')

    @MongoClientTradeGateway.error_handler
    def req_batch_order_insert(self, obj, side):
        msg_type = 'req_batch_order_insert'
        target_account_name = obj['accountName']
        acc = self.target_account_names_to_acc[target_account_name]
        account_id = self.account_id[acc]
        mid = str(obj['mid'])
        batch_oid = str(self.gen_order_id())
        algo_type = decode_algo_type(obj['order_type'])
        str_date = date_to_str(int(self.date))
        start_time  = str_date + str(obj['start_time'])
        end_time = str_date + str(obj['end_time'])
        limit_action = 1  #涨跌停后交易
        if not obj.get('LimAction') is None :
            if obj.get('LimAction'):
                limit_action = 0
        after_action = 0    #时间结束后不交易
        if not obj.get('AftAction') is None :
            if obj.get('AftAction'):
                after_action = 1
        up_limit = -1 #涨幅限制
        if not obj.get('up_limit') is None:
            up_limit = obj['up_limit']
        down_limit = -1 #涨幅限制
        if not obj.get('down_limit') is None:
            down_limit = obj['down_limit']
        limit = 0 #限价
        if not obj.get('limit') is None:
            limit = obj['limit']
        expire_date =  datetime.strftime(datetime.today(), '%Y-%m-%d')
        if not obj.get('expire_date') is None:
            expire_date = obj['expire_date']
        occupy_amount = 0.0
        if not obj.get('occupy_amount') is None:
            occupy_amount = obj['occupy_amount']
        param_list = []
        db_id = obj['_id']
        for param in obj['param_list']:
            oid = str(self.gen_order_id())
            stk_id = param['stk_id']
            volume = param['volume']
            algo_order_info = {
                'oid' : oid,
                'stk_id' : stk_id,
                'volume' : volume
            }
            param_list.append(algo_order_info)
            order_dict = {
                'oid' : oid,
                'mid' : mid,
                'db_id' : db_id,
                'ticker' : param['stk_id'],
                'side' : side,
                'volume' : volume,
                'account_name' : target_account_name,
                'order_type' : str(obj['order_type']),
                'start_time' : str(obj['start_time']),
                'end_time' : str(obj['end_time'])
            }
            local_id_list = []
            with self.order_msg_lock:
                #self.mid_to_req[mid] = order_dict
                self.oid_to_req[oid] = order_dict
                self.oid_to_mid[oid] = mid
                self.db_id_to_oid[db_id] = oid
                self.oid_to_acc[oid] = acc
                self.oid_to_traded_vol[oid] = 0
                self.oid_to_traded_amt[oid] = 0
                self.oid_to_local_ids[oid] = local_id_list
        output_dict = {
                'msg_type' : msg_type,
                'oid' : batch_oid,
                'algo_type' : algo_type,
                'fund_account' : account_id,
                'side' : str(side),
                'start_time' : start_time,
                'end_time' : end_time,
                'up_limit': up_limit,
                'down_limit': down_limit,
                'param_list' : param_list,
                'limit' : limit,
                'limit_action': limit_action,
                'after_action': after_action,
                'expire_date': expire_date,
                'occupy_amount': occupy_amount
            }
        self.tcp_send(output_dict)
        self.logger.info(f'[req_batch_order_insert] insert_success (mid){mid} (param){output_dict}')
        target_collection =  self.order_info_db[acc]['target']
        query = {
                    '_id' : db_id
                }
        delete_res = target_collection.delete_one(query)
        self.logger.info(f'[on_req_order_insert] used (target){obj}')

    @MongoClientTradeGateway.error_handler
    def req_order_insert(self, obj, IsBuy):
        target_account_name = obj['accountName']
        acc = self.target_account_names_to_acc[target_account_name]
        account_id = self.account_id[acc]
        account_type = self.account_type[acc]
        side = 1
        if not IsBuy:
            side = 2
        order_type = obj['executionPlan']['order_type']
        if order_type == 'smart_yr':
            self.req_batch_order_insert(obj, side)
            return
        entrust_type = 0
        if account_type == 'margin':
            if not obj.get('financingBuy') is None :
                financial_buy_s = obj["financingBuy"]
                if financial_buy_s == True:
                    entrust_type = 6
                else:
                    entrust_type = 9
            else:
                entrust_type = 9

        symbol_type = 0
        #price = float(obj['last_price'])
        mid = str(obj['mid'])
        vol = int(obj['volume'])
        algo_type = decode_algo_type(obj['executionPlan']['order_type'])
        str_date = date_to_str(int(self.date))
        start_time  = str_date + str(obj['executionPlan']['start_time'])
        end_time = str_date + str(obj['executionPlan']['end_time'])
        ticker = str(obj['ticker']) + encode_exchange_id(obj['ticker'])
        limit_action = 1  #涨跌停后交易
        if not obj.get('LimAction') is None :
            if obj.get('LimAction'):
                limit_action = 0
        after_action = 0    #时间结束后不交易
        if not obj.get('AftAction') is None :
            if obj.get('AftAction'):
                after_action = 1
        up_limit = -1 #涨幅限制
        if not obj.get('up_limit') is None:
            up_limit = obj['up_limit']
        down_limit = -1 #涨幅限制
        if not obj.get('down_limit') is None:
            down_limit = obj['down_limit']
        expire_date =  datetime.strftime(datetime.today(), '%Y-%m-%d')
        if not obj.get('expire_date') is None:
            expire_date = obj['expire_date']
        occupy_amount = 0.0
        if not obj.get('occupy_amount') is None:
            occupy_amount = obj['occupy_amount']
        price = 0.0
        if not obj.get('price') is None:
            price = float(obj['price'])
        style = 2
        if not obj.get('style') is None:
            style = int(obj['style'])
        #volume_list = check_split(vol, price, symbol_type)
        
        oid = str(self.gen_order_id())
        msg_type = 'req_order_insert'
        output_dict = {
            'msg_type' : msg_type,
            'oid' : oid,
            'algo_type' : algo_type,
            'fund_account' : account_id,
            'price' : price,
            'side' : str(side),
            'ticker': ticker,
            'volume' : vol,
            'start_time' : start_time,
            'end_time' : end_time,
            'up_limit': up_limit,
            'down_limit': down_limit,
            'limit' : price,
            'limit_action': limit_action,
            'after_action': after_action,
            'expire_date': expire_date,
            'occupy_amount': occupy_amount,
            'entrust_type': entrust_type,
            'account_type': account_type,
            'style': style
        }
        self.tcp_send(output_dict)
        db_id = obj['_id']
        order_dict = {
            'oid' : oid,
            'mid' : mid,
            'db_id' : db_id,
            'ticker' : ticker,
            'side' : side,
            'volume' : vol,
            'account_name' : target_account_name,
            'order_type' : order_type,
            'start_time' : str(obj['executionPlan']['start_time']),
            'end_time' : str(obj['executionPlan']['end_time'])
        }
        local_id_list = []
        with self.order_msg_lock:
            self.mid_to_req[mid] = order_dict
            self.oid_to_req[oid] = order_dict
            self.oid_to_mid[oid] = mid
            self.db_id_to_oid[db_id] = oid
            self.oid_to_acc[oid] = acc
            self.oid_to_traded_vol[oid] = 0
            self.oid_to_traded_amt[oid] = 0
            self.oid_to_local_ids[oid] = local_id_list
        self.logger.info(f'[req_order_insert] insert_success (oid){oid} (mid){mid} (param){output_dict}')
        target_collection =  self.order_info_db[acc]['target']
        if not IsBuy:
            target_collection =  self.order_info_db[acc]['sell_target']
        query = {
                    '_id' : db_id
                }
        delete_res = target_collection.delete_one(query)
        self.logger.info(f'[on_req_order_insert] used (target){obj}')

    @MongoClientTradeGateway.error_handler
    def on_message(self, msg):
        """ _summary_ : 根据信息内容，判断 on_order_msg/on_trade_msg/.../ 所有回报都在这个函数
            Args:
                msg (_type_): dict
        """
        if not 'msg_type' in msg:
            self.logger.error(f'msg_type not exist msg:{msg}')
        else:
            msg_type = msg['msg_type']
            if msg_type == 'on_rsp_order_insert':
                self.on_rsp_order_insert(msg)
            elif msg_type == 'on_rsp_plain_order_insert':
                self.on_rsp_plain_order_insert(msg)
            elif msg_type == 'on_rtn_trade':
                self.on_trade_msg(msg)
            elif msg_type == "on_rtn_order":
                if msg['status'] in [0 ,2, 4]:
                    self.update_order(msg)
                elif msg['status'] == 3:
                    self.logger.warning(f'order rejected: msg{msg}')
            elif msg_type == 'on_position':
                self.on_rtn_position(msg)
            elif msg_type == 'on_fund':
                self.on_rtn_fund(msg)
            else:
                self.logger.error(f'can not parse msg: {msg}')

    @MongoClientTradeGateway.error_handler
    def on_rsp_order_insert(self, msg):
        is_success = msg['status']
        err_info = msg['err_info']
        oid = msg['oid']
        inst_id = msg['inst_id'] #实例ID
        if not is_success:
            acc = self.oid_to_acc[oid]
            mid = self.oid_to_mid[oid]
            order_dict = self.oid_to_req[oid]
            warning_msg = f'[on_rsp_order_insert] create_instance failed oid : {oid}'
            self.logger.warning(warning_msg)
            self.send_error_to_user(self.logger, self.error_url_list, warning_msg)
        if len(inst_id) == 0:
            acc = self.oid_to_acc[oid]
            mid = self.oid_to_mid[oid]
            order_dict = self.oid_to_req[oid]
            warning_msg = f'[on_rsp_order_insert] req insert failed oid : {oid}, error_info:{err_info} order_msg:{order_dict}'
            self.logger.warning(warning_msg)
            self.send_error_to_user(self.logger, self.error_url_list, warning_msg)

        self.oid_to_ref[oid] = inst_id
        self.ref_to_oid[inst_id] = oid
        self.logger.info(f'[on_rsp_order_insert] insert success oid:{oid}')
        acc = self.oid_to_acc[oid]
        mid = self.oid_to_mid[oid]
        order_dict = self.oid_to_req[oid]
        cached_order_collection = self.order_info_db[acc]['cached_order']
        local_id_list = []
        db_msg = {
                    'oid' : oid,
                    'mid' : mid,
                    'mudan_id' : inst_id,
                    "insert_time": datetime.utcnow(),
                    'traded_vol' : 0,
                    'traded_amt' : 0,
                    'local_ids' : local_id_list,
                    'order_msg': order_dict
        }
        query = {'oid': oid}
        res = cached_order_collection.replace_one(query, db_msg, True)
        self.logger.info(f'[on_rsp_order_insert] update_cached_order_info (res){res} (msg){db_msg}')

    @MongoClientTradeGateway.error_handler
    def on_rsp_plain_order_insert(self, msg):
        oid = msg['oid']
        order_id = msg['order_id'] #实例ID

        self.oid_to_ref[oid] = order_id
        self.ref_to_oid[order_id] = oid
        self.logger.info(f'[on_rsp_order_insert] insert success oid:{oid}')
        acc = self.oid_to_acc[oid]
        mid = self.oid_to_mid[oid]
        order_dict = self.oid_to_req[oid]
        cached_order_collection = self.order_info_db[acc]['cached_order']
        local_id_list = []
        db_msg = {
                    'oid' : oid,
                    'mid' : mid,
                    'mudan_id' : order_id,
                    "insert_time": datetime.utcnow(),
                    'traded_vol' : 0,
                    'traded_amt' : 0,
                    'local_ids' : local_id_list,
                    'order_msg': order_dict
        }
        query = {'oid': oid}
        res = cached_order_collection.replace_one(query, db_msg, True)
        self.logger.info(f'[on_rsp_order_insert] update_cached_order_info (res){res} (msg){db_msg}')

    @MongoClientTradeGateway.error_handler
    def monitor_trade_update(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                trade_filename = self.recv_msg_path + '//' + self.my_today + '//' + FILES.TRADES + '_' + trade_acc + '.csv'
                with open(trade_filename, 'r', encoding='utf-8') as trade_file:
                    csv_dict_reader = csv.DictReader(trade_file)
                    for row in csv_dict_reader:
                        self.on_trade_msg(row)
            time.sleep(self.trade_scan_interval)

    @MongoClientTradeGateway.error_handler
    def on_trade_msg(self, msg):
        if msg['amount'] == 0 or msg['price'] == 0:
            self.logger.warning(f'[on_trade_msg] nothing_traded (record){msg}')
            return
        trade_acc = msg['fund_account']
        mudan_id = msg['algo_inst_id']
        if mudan_id is None or len(mudan_id) == 0:
            if 'order_id' not in msg or len(msg['order_id']) == 0:
                self.logger.warning(f"[on_trade_msg] can not get mudan_id, msg:{msg}")
                return
            mudan_id = msg['order_id']
        oid = ''
        acc = ''
        mid = ''
        order_dict = {}
        with self.order_msg_lock:
            if mudan_id not in self.ref_to_oid or oid not in self.oid_to_acc:
                acc = self.account_id_to_acc[trade_acc]
                order_info_collection = self.order_info_db[acc]['cached_order']
                query = {'mudan_id' : mudan_id}
                order_info_target = order_info_collection.find_one(query)
                if not order_info_target is None:
                    order_dict = order_info_target['order_msg']
                    mid = order_info_target['mid']
                    oid = order_info_target['oid']
                    self.oid_to_local_ids[oid] = order_info_target['local_ids']
                    self.oid_to_traded_vol[oid] = 0
                    self.oid_to_traded_amt[oid] = 0
                    self.oid_to_mid[oid] = mid
                    self.oid_to_req[oid] = order_dict
                    self.oid_to_ref[oid] = mudan_id
                    self.ref_to_oid[mudan_id] = oid
                else:
                    self.logger.warning(f"[on_trade_msg] can not get oid, msg:{msg}, mudan_id:{mudan_id}")
                    return
            else:
                oid = self.ref_to_oid[mudan_id]
                acc = self.oid_to_acc[oid]
                order_dict = self.oid_to_req[oid]
                mid = self.oid_to_mid[oid]
        acc = self.account_id_to_acc[trade_acc]
        order_info_collection = self.order_info_db[acc]['cached_order']
        query = {'oid' : oid}
        order_info_target = order_info_collection.find_one(query)

        _id = str(msg['trade_id'])
        if _id in self.oid_to_local_ids[oid]:
            self.logger.warning(f'[on_trade_msg] duplicate_trade_msg (record){msg}')
            return
        else:
            self.oid_to_local_ids[oid].append(_id)#外部委托编号
        ticker = str(msg['symbol']).split('.')[0]
        exchange = decode_exchange_id(str(msg['symbol']).split('.')[1])
        traded_vol = int(msg['amount'])
        traded_price = float(msg['price'])
        trade_amt = float(msg['business_balance'])
        order_type = msg['real_type']
        target_type = int(msg['side'])
        if target_type in [1, 3]:
            self.oid_to_traded_amt[oid] += trade_amt
            self.oid_to_traded_vol[oid] += traded_vol
        elif target_type == 2:
            self.oid_to_traded_amt[oid] -= trade_amt
            self.oid_to_traded_vol[oid] -= traded_vol
        dbTime = datetime.now(timezone.utc)
        str_trade_time = msg['time']
        trade_time = datetime.strptime(str_trade_time, '%Y-%m-%d %H:%M:%S')
        utc_trade_time = trade_time - timedelta(hours=8)
        target_account_name = order_dict['account_name']
        acc = self.target_account_names_to_acc[target_account_name]
        log_account_name = order_dict['account_name'].split('@')[1]
        tg_name =  order_dict['account_name'].split('@')[0]

        db_msg = {
            'trade_ref': _id,
            'oid': int(oid),
            'tg_name': tg_name,
            'ticker': ticker,
            "exchange": exchange,
            'traded_vol': traded_vol,
            'traded_price': traded_price,
            'order_type': order_type, #算法类型
            'side': target_type,
            'entrust_vol': 0,
            'entrust_price': 0,
            'dbTime': dbTime,
            'mid': mid,  # 对应订单中的 mid
            "commission" : 0,
            'trade_time': utc_trade_time,  # 具体交易时间
            'accountName':  log_account_name
        }
        trade_collection = self.tradelog_db[acc]['tg_trade']
        replace_trade_query = { 'trade_ref': _id, 'oid' : int(oid), 'mid': mid, 'accountName': log_account_name}
        db_res = trade_collection.replace_one(replace_trade_query, db_msg, True)
        self.logger.info(
            f'[rtn_trade] (db_res){db_res} (db_msg){db_msg} (traded_vol){traded_vol} (traded_price){traded_price}')
        #self.update_position(traded_vol, order_dict, mid, oid, target_type, trade_amt,exchange)

        cached_order_collection = self.order_info_db[acc]['cached_order']
        cached_order_msg = {
                    'local_ids' : self.oid_to_local_ids[oid],
                }
        update_cached_order_msg = {'$set': cached_order_msg}
        query = {'oid': oid}
        res = cached_order_collection.update_one(query, update_cached_order_msg)
        self.logger.info(f'[on_trade_msg] update_cached_order_info (res){res} (msg){update_cached_order_msg}')

    def monitor_order_update(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                order_filename = self.recv_msg_path + '//' + self.my_today + '//' + FILES.ORDERS + '_' + trade_acc + '.csv'
                with open(order_filename, 'r', encoding='utf-8') as order_file:
                    csv_dict_reader = csv.DictReader(order_file)
                    for row in csv_dict_reader:
                        status = int(row['status'])
                        if status in [2 ,4]:
                            self.update_order(row)
            time.sleep(self.order_scan_interval)

    @MongoClientTradeGateway.error_handler
    def update_order(self, msg):
        oid = ''
        acc = ''
        mid = ''
        order_dict = {}
        mudan_id = msg['algo_inst_id']
        if mudan_id is None or len(mudan_id) == 0:
            if 'order_id' not in msg or len(msg['order_id']) == 0:
                self.logger.warning(f"[update_order] can not get mudan_id, msg:{msg}")
                return
            mudan_id = msg['order_id']
        trade_acc = msg['fund_account']
        acc = self.account_id_to_acc[trade_acc]
        order_info_collection = self.order_info_db[acc]['cached_order']
        with self.order_msg_lock:
            if  mudan_id not in self.ref_to_oid or oid not in self.oid_to_acc: #shut_down or other problem
                if trade_acc not in self.account_id_to_acc:
                    self.logger.error(f'[update_order] can not_parse_trade_acc {trade_acc}')
                    return
                query = {'mudan_id' : mudan_id}
                order_info_target = order_info_collection.find_one(query)
                if not order_info_target is None:
                    order_dict = order_info_target['order_msg']
                    oid = order_info_target['oid']
                    mid = order_info_target['mid']
                    self.oid_to_local_ids[oid] = order_info_target['local_ids']
                    self.oid_to_traded_amt[oid] = 0
                    self.oid_to_traded_vol[oid] = 0
                    self.oid_to_mid[oid] = mid
                    self.oid_to_req[oid] = order_dict
                    self.oid_to_ref[oid] = mudan_id
                    self.ref_to_oid[mudan_id] = oid
                else:
                    self.logger.warning(f'[update_order] can not_find_oid (mudan_id){mudan_id}')
                    return
            else:
                oid = self.ref_to_oid[mudan_id]
                acc = self.oid_to_acc[oid]
                order_dict = self.oid_to_req[oid]
                mid = self.oid_to_mid[oid]
        local_id = msg['order_id']
        if local_id in self.oid_to_local_ids[oid]:
            self.logger.warning(f'[update_order] duplicate_order_msg (record){msg}')
            return
        else:
            self.oid_to_local_ids[oid].append(local_id)
        ticker = msg['symbol'].split('.')[0]
        exchange = decode_exchange_id(str(msg['symbol'].split('.')[1]))
        volume = order_dict['volume']
        price = float(msg['price'])

        tg_name = order_dict['account_name'].split('@')[0]
        account_name = order_dict['account_name'].split('@')[1]
        order_type = order_dict['order_type']
        start_time = order_dict['start_time']
        end_time = order_dict['end_time']

        target_type = side_to_target_type(order_dict['side'])
        filled_vol = int(msg['filled'])
        status = decode_mquant_status(int(msg['status']))

        replace_collection = self.tradelog_db[acc]['order']
        query = {'mid':mid, '_id': int(oid)}
        replace_target = replace_collection.find_one(query)
        if not replace_target is None:
            utc_update_time = replace_target['dbTime']
            _filled_vol = filled_vol + replace_target['filled_vol']
            filled_vol = min(_filled_vol, volume)
            order_msg = {
                '_id': int(oid),
                'tg_name': tg_name,  # 对应 account_info._ids
                "exchange": exchange,
                'target_type': target_type,    # 'buy' | 'sell' | 'limit_sell'
                'volume': volume,  # 订单的volume
                'price': price,  # 实际成交均价
                'order_type': order_type,
                'ticker': ticker,
                'mid': mid,  # target中对应的 母单mid
                'accountName': account_name,
                'algo_args': {  # 具体的算法参数
                    'order_type': order_type,  # 此柜台不使用下单时要求的算法
                    'start_time': start_time,
                    'end_time': end_time
                },
                'status': status,  # 'active' | 'filled' | 'canceled'
                'filled_vol': filled_vol,  # 实际成交的 volume
                'dbTime': utc_update_time,
            }

            res = replace_collection.replace_one(query, order_msg, True)
            self.logger.info(f'[rtn_order] (res){res} (order_msg){order_msg}')
        else:
            str_update_time = str((msg['add_time']))
            update_time = datetime.strptime(str_update_time, '%Y-%m-%d %H:%M:%S')
            utc_update_time = update_time - timedelta(hours=8)
            order_msg = {
                '_id': int(oid),
                'tg_name': tg_name,  # 对应 account_info._id
                'target_type': target_type,    # 'buy' | 'sell' | 'limit_sell'
                "exchange": exchange,
                'volume': volume,  # 订单的volume
                'price': price,  # 实际成交均价
                'order_type': order_type,
                'ticker': ticker,
                'mid': mid,  # target中对应的 母单mid
                'accountName': account_name,  # 对应 account_info.account_name
                'algo_args': {  # 具体的算法参数
                    'order_type': order_type,
                    'start_time': start_time,
                    'end_time': end_time
                },
                'status': status,  # 'active' | 'filled' | 'canceled'
                'filled_vol': filled_vol,  # 实际成交的 volume
                'dbTime': utc_update_time,
            }

            res = replace_collection.replace_one(query, order_msg, True)
            self.logger.info(f'[rtn_order] (res){res} (order_msg){order_msg}')
        cached_order_collection = self.order_info_db[acc]['cached_order']
        cached_order_msg = {
                    'local_ids' : self.oid_to_local_ids[oid],
                }
        update_cached_order_msg = {'$set': cached_order_msg}
        query = {'oid': oid}
        res = cached_order_collection.update_one(query, update_cached_order_msg)
        self.logger.info(f'[update_order] update_cached_order_info (res){res} (msg){update_cached_order_msg}')

    @MongoClientTradeGateway.error_handler
    def monitor_position_update(self):
        while not self.is_stopped:
            print("[monitor_position_update]")
            for acc in self.accounts_run:
                pos_msg_list = []
                trade_acc = self.account_id[acc]
                tg_name = self.target_account_names[acc]
                pos_collection = self.order_info_db[acc]['tg_equity_position']
                delete_filter = {
                    "tg_name" : tg_name
                }
                delete_res = pos_collection.delete_many(delete_filter)
                self.logger.info(f"delete {delete_res.deleted_count} documents in {tg_name}")
                pos_filename = self.recv_msg_path + '//' + self.my_today + '//' + FILES.POSITIONS + '_' + trade_acc + '.csv'
                try:
                    with open(pos_filename, 'r', encoding='utf-8') as pos_file:
                        csv_dict_reader = csv.DictReader(pos_file)
                        for row in csv_dict_reader:
                            pos_msg = self.on_rtn_position(row)
                            pos_msg_list.append(pos_msg)
                    if len(pos_msg_list) > 0:
                        try:
                            res = pos_collection.insert_many(pos_msg_list)
                        except Exception as e:
                            self.logger.error(f'insert error: {e}')
                            time.sleep(1)
                            continue
                        self.logger.info(f'[on_rtn_position] position_updated length:{len(res.inserted_ids)}')
                except Exception as e:
                    self.logger.error(f'[on_rtn_position] insert error: {e}')
                    time.sleep(1)
                    continue

            time.sleep(self.pos_interval)
    @MongoClientTradeGateway.error_handler
    def on_rtn_position(self, msg):

        trade_acc = msg['fund_account']
        if trade_acc not in self.account_id_to_acc:
            self.logger.warning(f'[on_rtn_position] can not_parse_trade_acc {trade_acc}')
            return
        acc = self.account_id_to_acc[trade_acc]
        account_name = self.log_account_names[acc]
        tg_name = self.target_account_names[acc]
        ticker = str(msg['symbol']).split('.')[0]
        exchange = decode_exchange_id(str(msg['symbol']).split('.')[1])
        td_pos = float(msg['total_amount'])
        yd_pos = float(msg['closeable_amount'])
        market_value = float(msg['value'])
        holding_cost = float(msg['holding_cost'])
        pos_msg = {
            "account_name": account_name,
            'tg_name': tg_name,
            'ticker': ticker,
            "exchange": exchange,
            "direction": "long",
            'avail_pos': yd_pos, # 昨仓
            'total_pos': td_pos, # 今仓
            "type": "stock",
            'updated_at': datetime.utcnow()
        }
        return pos_msg

    @MongoClientTradeGateway.error_handler
    def monitor_fund_update(self):
        while not self.is_stopped:
            print("[monitor_fund_update]")
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                asset_filename = self.recv_msg_path + '//' + self.my_today + '//' + FILES.ASSETS + '_' + trade_acc + '.csv'
                with open(asset_filename, 'r', encoding='utf-8') as asset_file:
                    csv_dict_reader = csv.DictReader(asset_file)
                    for row in csv_dict_reader:
                        self.on_rtn_fund(row)
            time.sleep(self.acc_interval)
    def on_rtn_fund(self, msg):
        trade_acc = msg['fund_account']
        available_cash = float(msg['available_cash'])
        market_amt = float(msg['market_value'])
        acc = self.account_id_to_acc[trade_acc]
        tg_name = self.tgnames[acc]
        account_name = self.log_account_names[acc]
        asset_collection = self.order_info_db[acc]['EquityAccount']
        query = {'tg_name':tg_name, 'account_name': account_name}
        id_query = {'_id': tg_name}
        target = asset_collection.find_one(id_query)
        if target is None:
            asset_msg = {
                "_id" : tg_name,
                #"tg_name" : tg_name, # 对应之前的 TG 名称
                'accountName': account_name,  # 产品名称
                #"fund_account" : trade_acc,
                'avail_amt': available_cash,  # 可用资金（可现金买入的资金）
                'balance': available_cash + market_amt, # 净资产.  最好是由券商那边提供，通常普通账户是 可用资金(包含预扣费用) + 市值；信用账户是总资金 - 总负债
                'holding': market_amt, # 市值,
                'updated_at': datetime.utcnow()
            }
            res = asset_collection.insert_one(asset_msg)
            self.logger.info(f'[update_dbf_asset] (res){res} (order_msg){asset_msg}')
        else:
            up_asset_msg = {
                #"tg_name" : tg_name, # 对应之前的 TG 名称
                'accountName': account_name,  # 产品名称
                #"fund_account" : trade_acc,
                'avail_amt': available_cash,  # 可用资金（可现金买入的资金）
                'balance': available_cash + market_amt, # 净资产.  最好是由券商那边提供，通常普通账户是 可用资金(包含预扣费用) + 市值；信用账户是总资金 - 总负债
                'holding': market_amt, # 市值,
                'updated_at': datetime.utcnow()
            }
            res = asset_collection.update_one(id_query, {'$set': up_asset_msg}, True)
            self.logger.info(f'[update_dbf_asset] (res){res} (order_msg){up_asset_msg}')

    def monitor(self):
        ts = [
            threading.Thread(target=self.monitor_algo_order_insert),
            threading.Thread(target=self.tcp_recv),
            threading.Thread(target=self.handle_send_msg),
            threading.Thread(target=self.handle_msg),
            #threading.Thread(target=self.monitor_fund_update),
            threading.Thread(target=self.monitor_position_update),
            threading.Thread(target=self.monitor_trade_update),
            threading.Thread(target=self.monitor_order_update),
            threading.Thread(target=self.monitor_algo_limit_order_insert),
            threading.Thread(target=self.date_change)
        ]
        for t in ts:
            t.setDaemon(True)
            t.start()
        #self.thread_pool.submit(self.monitor_dbf_pos)

    @MongoClientTradeGateway.error_handler
    def start(self):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        _msg = f'[login] {GATEWAY_NAME}_server_start (time){datetime.now()}'
        self.send_to_user(logger=self.logger, url_list=self.url_list, msg=_msg)
        self.create_tcp_client()
        #self.update_holding_pos("pre_holding_pos")
        self.monitor()

    def close(self):
        self.tcp_socket_init = False
        self.tcp_socket.close()
        return super().close()

    def join(self):
        while self.is_stopped == False:
            time.sleep(0.01)
            if self.is_stopped:
                self.logger.info(
                    '[close] main thread is stopped,active_orders message will lose')
                self.close()

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    description = 'mquant_server,get target from mongodb and serve mquant api'  
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-e' , '--end_time', dest='end_time', default='15:30')
    _config_filename = 'C:/Users/Administrator/Desktop/mquant_batandconfig/mquant_server_config.json'
    parser.add_argument('-p', '--config_filepath', dest= 'config_filepath', default= _config_filename)

    args = parser.parse_args()
    print (f'(args){args}')

    td = MquantServer(args.config_filepath, args.end_time)
    td.start()

    td.join()
