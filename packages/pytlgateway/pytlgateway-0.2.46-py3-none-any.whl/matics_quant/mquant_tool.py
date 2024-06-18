import sys
import json
from datetime import datetime, timezone, timedelta
import traceback
import argparse

from ..mongo_client_gateway import MongoClientTradeGateway
from .constants import (FILES, GATEWAY_NAME)
from .utils import (decode_exchange_id)
import csv


class MquantTool(MongoClientTradeGateway):
    def __init__(self, config_filename, sync_pos,  end_time, clear_atx, reverse_trade, gateway_name):
        MongoClientTradeGateway.__init__(
            self, config_filename, end_time, gateway_name)
        self.update_trade_date = self.date
        self.sync_pos = sync_pos
        self.clear_atx = clear_atx
        self.reverse_trade = reverse_trade
        self.my_today = datetime.strftime(datetime.now(), "%Y-%m-%d")
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
        self.load_tool_setting(config_filename)

    def load_tool_setting(self, config_filename):
        try:
            #config_filename = os.path.join(config_path, 'atx_server_config.json')
            f = open(config_filename, encoding='gbk')
            setting = json.load(f)
            #self.recv_msg_dir = setting['recv_msg_path'].replace('/', '\\')
            self.recv_msg_path = setting['recv_msg_path']
            self.recv_msg_path = self.recv_msg_path.replace('/', '//')
            self.sync_position_open = setting['sync_position_open']
            self.sync_position_close = setting['sync_position_close']

        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(
                exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            print(f"load config failed! (exception){err}")
            exit(0)

    @MongoClientTradeGateway.error_handler
    def clear_atx_order(self):
        for acc in self.accounts_run:
            collection = self.order_info_db[acc]['atx_order']
            target_account_name = self.target_account_names[acc]
            targets_query = {'order_msg.accountName': target_account_name}
            targets = collection.find(targets_query)
            self.logger.info(f"now (target_account_name){target_account_name}")
            if targets.count() == 0:
                continue
            for order_tick in targets:
                local_ids = []
                instr_ids = []
                self.logger.info(f"goes in (order_tick){order_tick}")
                sid = order_tick['sid']
                query = {'sid': sid, 'order_msg.accountName': target_account_name}
                change = {
                    'local_ids': local_ids,
                    'instr_ids': instr_ids
                }
                new_data = {"$set": change}
                res = collection.update_many(
                    query, new_data, True)
                self.logger.info(
                    f"[update_atx_order] (res){res} (change){change}")
    @MongoClientTradeGateway.error_handler
    def reverse_trade_data(self):
        for acc in self.accounts_run:
            trade_acc = self.account_id[acc]
            trade_filename = self.recv_msg_path + '//' + self.my_today + '//' + FILES.TRADES + '_' + trade_acc + '.csv'
            with open(trade_filename, 'r', encoding='utf-8') as trade_file:
                csv_dict_reader = csv.DictReader(trade_file)
                for row in csv_dict_reader:
                    self.on_trade_msg(row, acc)
    @MongoClientTradeGateway.error_handler
    def on_trade_msg(self, msg, acc):
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
        oid = self.gen_order_id()
        acc = ''
        mid = ''
        order_dict = {}
        acc = self.account_id_to_acc[trade_acc]
        order_info_collection = self.order_info_db[acc]['cached_order']
        query = {'mudan_id' : mudan_id}
        order_info_target = order_info_collection.find_one(query)
        if not order_info_target is None:
            return

        _id = str(msg['trade_id'])

        ticker = str(msg['symbol']).split('.')[0]
        exchange = decode_exchange_id(str(msg['symbol']).split('.')[1])
        traded_vol = int(msg['amount'])
        traded_price = float(msg['price'])
        trade_amt = float(msg['business_balance'])
        order_type = msg['real_type']
        target_type = int(msg['side'])
        dbTime = datetime.now(timezone.utc)
        str_trade_time = msg['time']
        trade_time = datetime.strptime(str_trade_time, '%Y-%m-%d %H:%M:%S')
        utc_trade_time = trade_time - timedelta(hours=8)
        target_account_name = self.target_account_names[acc]
        log_account_name = target_account_name.split('@')[1]
        tg_name =  target_account_name.split('@')[0]

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
        replace_trade_query = { 'trade_ref': _id, 'accountName': log_account_name}
        db_res = trade_collection.replace_one(replace_trade_query, db_msg, True)
        self.logger.info(
            f'[rtn_trade] (db_res){db_res} (db_msg){db_msg} (traded_vol){traded_vol} (traded_price){traded_price}')
        #self.update_position(traded_vol, order_dict, mid, oid, target_type, trade_amt,exchange)

    def start(self):

        if self.sync_pos == True:
            self.date_change()
            _msg = "[gf_date_change] executed"
            self.send_to_user(logger=self.logger,
                              url_list=self.url_list, msg=_msg)
        if self.clear_atx == True:
            self.clear_atx_order()
            _msg = "[gf_clear_atx] executed"
            self.send_to_user(logger=self.logger,
                              url_list=self.url_list, msg=_msg)
        if self.reverse_trade == True:
            self.reverse_trade_data()
            _msg = "[reverse_trade] executed"
            self.send_to_user(logger=self.logger,
                              url_list=self.url_list, msg=_msg)

    @MongoClientTradeGateway.error_handler
    def date_change(self):
        dt = datetime.now()
        self.logger.info(f"(dt){dt.hour}")
        if dt.hour <= self.sync_position_open and self.sync_pos == True:
            self.logger.info("[date_change] date_change_open")
            self.update_position_date_open()
        elif dt.hour < self.sync_position_close and dt.hour > self.sync_position_open:
            self.logger.info("[date_change] date_not_change")
        elif dt.hour >= self.sync_position_close and self.sync_pos == True:
            self.logger.info("[date_change] date_change_close")
            self.update_position_date_close()
        else:
            self.logger.info("[date_change] date_not_change")
            return

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.') 

if __name__ == "__main__":

    description = "sync pos for emc_server"
    parser = argparse.ArgumentParser(description=description)

    _file_name = "C:\\Users\\Administrator\\Desktop\\emc_batandconfig\\emc_tool_setting.json"
    _date = datetime.now().strftime("%Y%m%d")
    parser.add_argument('-m', '--config_filename',
                        dest='config_filename', type=str, default=_file_name)
    parser.add_argument('-p', '--date_change',
                        dest='date_change', type=str2bool, default='T')
    parser.add_argument('-c', '--clear_atx', dest='clear_atx',
                        type=str2bool, default='F')
    parser.add_argument('-r', '--reverse_trade', dest='reverse_trade',
                        type=str2bool, default='F')
    end_time = "15:30"
    args = parser.parse_args()
    print(f"(args){args}")

    td = MquantTool(args.config_filename, args.date_change,
                 end_time, args.clear_atx, args.reverse_trade,GATEWAY_NAME)

    td.start()
