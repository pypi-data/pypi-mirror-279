import datetime
import socket                               #导入socket模块
import threading
import json
import time
from mquant_api import *
from mquant_struct import *
from string_buffer import TcpStringBuffer
class TcpServer():
    """_summary_: tcpserver for m quant
    """
    def __init__(self, port) -> None:
        self.tcp_socket_init = False
        self.tcp_socket = None
        self.conn = None
        self.msg_new = None
        self.addr = None
        self.string_buffer = TcpStringBuffer()
        self.host = '127.0.0.1'                       #主机IP
        self.port = port                            #端口
        self.is_stopped = False
        self.msg_lock = threading.Lock()
        self.send_msg_lock = threading.Lock()

    # 创建TCP服务
    def create_tcp_server(self):
        if self.tcp_socket_init is False:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   #创建TCP/IP套接字
            self.tcp_socket.bind((self.host, self.port))        #绑定端口
            self.tcp_socket.listen(5)                           #设置最多连接数
            self.tcp_socket_init = True
        #阻塞模式
        print("等待TCP客户端连接") #建立客户端连接
        self.conn, self.addr = self.tcp_socket.accept()

    def tcp_proc(self):
        while not self.is_stopped:
            if self.tcp_socket_init is True:
                #获取客户端请求的数据,使用全局变量模式，供框架内其他函数使用
                msg_new = self.conn.recv(4096).decode()
                self.string_buffer.receive(msg_new)
        self.conn.close()

    def send_tcp_msg(self, msg):
        self.string_buffer.push(msg)
    #log.info("send_tcp_msg, msg_type:{} smg:{}".format(msg["msg_type"], msg))

    def msg_handler(self):
        while not self.is_stopped:
            if not self.string_buffer.is_recv_str_empty():
                for msg in self.string_buffer.get_recv():
                    self.handle_msg(msg)
            time.sleep(1)

    def send_msg_hander(self):
        while not self.is_stopped:
            if not self.string_buffer.is_send_str_empty():
                send_data = self.string_buffer.get_send()
                self.conn.sendall(send_data.encode())
                print(f'send tcp msg: {send_data}')
            time.sleep(1)

    def handle_msg(self, msg):
        msg_type = msg['msg_type']
        if msg_type == "req_order_insert":
            self.proc_split_order_algo_msg(msg)
        elif msg_type == "req_batch_order_insert":
            self.proc_split_order_algo_msg(msg, True)
        elif msg_type == "req_plain_order":
            self.req_plain_order(msg)
        elif msg_type == "req_limit_order":
            self.req_limit_order(msg)
        else:
            print("can not parse msg: {}".format(msg))
    
    def req_limit_order(self, msg):
        batch_no = str(msg['oid'])
        account_type = AccountType.margin
        if 'account_type' in msg['account_type']:
            if msg['account_type'] == 'normal':
                account_type = AccountType.normal
            elif msg['account_type'] == 'margin':
                account_type = AccountType.margin
        order_request = OrderRequest()
        side = msg['side']
        if side == 'buy':
            order_request.side = OrderSide.BUY
        elif side == 'sell':
            order_request.side = OrderSide.SELL
        else:
            log.error('参数错误，非法的订单方向：{}'.format(side))
            return
        order_request.symbol = msg['ticker']
        order_request.amount = int(msg['volume'])
        entrust_type = msg['entrust_type']
        if entrust_type == 6:
            order_request.entrust_type = EntrustType.creditFinancing
        elif entrust_type == 9:
            order_request.entrust_type = EntrustType.creditTransactions
        else:
            order_request.entrust_type = '0'
        limit_price = float(msg['price'])
        order_request.style = LimitOrderStyle(limit_price=limit_price)
        rsp = order_normal(order_request, account_type=account_type, batch_no=batch_no)
        if rsp is None:
            log.error("req plain order failed")
            return
        else:
            msg_dict = {
                "msg_type" : "on_rsp_plain_order_insert",
                "oid" : batch_no,
                "order_id" : rsp.order_id,
                "add_time" : rsp.add_time
            }

        self.send_tcp_msg(msg_dict)

    def req_plain_order(self, msg):
        batch_no = str(msg['oid'])
        order_request = OrderRequest()
        side = msg['side']
        if side == '1':
            order_request.side = OrderSide.BUY
        elif side == '2':
            order_request.side = OrderSide.SELL
        else:
            log.error('参数错误，非法的订单方向：{}'.format(side))
            return
        order_request.symbol = msg['ticker']
        order_request.amount = int(msg['volume'])
        limit_price = self.get_limit_price(msg['ticker'], side)
        order_request.style = MarketOrderStyle('a', limit_price=limit_price)
        rsp = order_normal(order_request, batch_no=batch_no)
        if rsp is None:
            log.error("req plain order failed")
            return
        else:
            msg_dict = {
                "msg_type" : "on_rsp_plain_order_insert",
                "oid" : batch_no,
                "order_id" : rsp.order_id,
                "add_time" : rsp.add_time
            }

        self.send_tcp_msg(msg_dict)
        
    def proc_split_t0_algo_msg(self, params):
        """
        处理T0算法创建消息
        """
        log.info('recv algo params {}'.format(params))

    def proc_split_order_algo_msg(self, params, batch=False):
        """
        处理算法创建消息
        """
        log.info('recv algo params {}'.format(params))
        fund_account = params['fund_account']
        split_algo_param = SplitOrderAlgoParam()
        algo_type = params['algo_type']
        if params['algo_type'] == 27:
            algo_type = AlgoType.KF_TWAPPLUS
        elif params['algo_type'] == 28:
            algo_type = AlgoType.KF_VWAPPLUS
        elif params['algo_type'] == 37:
            algo_type = AlgoType.FT_TWAPPLUS
        elif params['algo_type'] == 38:
            algo_type = AlgoType.FT_VWAPPLUS
        elif params['algo_type'] == 29:
            algo_type = AlgoType.smarT_I
        elif params['algo_type'] == 30:
            algo_type = AlgoType.smarT_Y
        try:
            split_algo_param.algo_type = algo_type 
        except Exception as e:
            err_msg = 'algo_type insert failed'
            log.error(f'{err_msg}')
            return

        try:
            split_algo_param.start_time = datetime.datetime.strptime(params['start_time'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            log.error('开始时间[{}]格式非法,请按照yyyy-MM-dd hh:mm:ss格式填写'.format(params['start_time']))
            return

        try:
            split_algo_param.end_time = datetime.datetime.strptime(params['end_time'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            log.error('结束时间[{}]格式非法,请按照yyyy-MM-dd hh:mm:ss格式填写'.format(params['end_time']))
            return

        side = str(params['side'])
        if side == '1':
            split_algo_param.order_side = OrderSide.BUY
        elif side == '2':
            split_algo_param.order_side = OrderSide.SELL
        else:
            split_algo_param.order_side = OrderSide.UNKNOWN
        entrust_type = params['entrust_type']
        if entrust_type == 6:
            split_algo_param.entrust_type = EntrustType.creditFinancing
        elif entrust_type == 9:
            split_algo_param.entrust_type = EntrustType.creditTransactions
        else:
            split_algo_param.entrust_type = EntrustType.entrust
        account_type = AccountType.margin
        if 'account_type' in params:
            if params['account_type'] == 'normal':
                account_type = AccountType.normal
            elif params['account_type'] == 'margin':
                account_type = AccountType.margin
        

        split_algo_param.remark = str(params['oid'])
        
        split_algo_param.limit_price = params['limit']
        if algo_type == AlgoType.KF_TWAPPLUS or algo_type == AlgoType.KF_VWAPPLUS:
            split_algo_param.up_limit = params['up_limit'] # 涨幅限制 涨幅限制，单位为%，范围[-1,20]，小数位数不限制。填-1或者为空时，相当于此参数不使用；
            split_algo_param.down_limit = params['down_limit']  # 跌幅限制 跌幅限制，单位为%，范围[-1,20]，小数位数不限制。填-1或者为空时，相当于此参数不使用；
            split_algo_param.limit_action = params['limit_action']  # 涨跌停是否继续交易 True:涨停可以卖、跌停可以买 False:涨停不卖、跌停不买
            split_algo_param.after_action = params['after_action']  # 过期后是否继续交易 True:到了结束时间，算法未完成全部交易，继续交易，直到闭市，不参与收盘集合竞价
        elif algo_type == AlgoType.FT_TWAPPLUS or algo_type == AlgoType.FT_VWAPPLUS:
            split_algo_param.limit_action = params['limit_action']
            split_algo_param.style = params['style']
        elif algo_type == AlgoType.smarT_I:
            split_algo_param.expiration_date = datetime.datetime.strptime(params['expire_date'], '%Y-%m-%d').date()
        elif algo_type == AlgoType.smarT_Y:
            split_algo_param.expiration_date = datetime.datetime.strptime(params['expire_date'], '%Y-%m-%d').date()
            split_algo_param.occupy_amount = params['occupy_amount']
        oid_list = []
        if batch is True:
            algo_info_params = params['param_list']
            for param in algo_info_params:
                symbol = param['stk_id']
                qty = int(param['volume'])
                s_oid = str(param['oid'])
                oid_list.append(s_oid)
                if algo_type == AlgoType.FT_TWAPPLUS or algo_type == AlgoType.FT_VWAPPLUS:
                    if side == '1':
                        order_item.side = OrderSide.BUY
                    elif side == '2':
                        order_item.side = OrderSide.SELL
                    else:
                        order_item.side = OrderSide.UNKNOWN
                order_item = AlgoOrderInfo()
                order_item.symbol = symbol
                order_item.amount = qty
                order_item.remark = s_oid
                order_item.buy_entrust_type = EntrustType.entrust  # 买入类型
                order_item.sell_entrust_type = EntrustType.entrust
                split_algo_param.order_list.append(order_item)
        else:
            symbol = params['ticker']
            qty = int(params['volume'])
            limit = str(params['limit'])

            order_item = AlgoOrderInfo()
            order_item.symbol = symbol
            order_item.amount = qty
            order_item.limit = limit
            split_algo_param.order_list.append(order_item)

        print('create algo instance')
        rsp = AlgoTradeHandler.start_split_order_algo_instance(account_type, split_algo_param)
        log.info('创建算法[{}]返回：{},{}'.format(algo_type, rsp.inst_id, rsp.err_info))
        rsp_msg = {}
        if rsp is None:
            log.error("创建算法[{}]失败'.format(algo_type)")
            rsp_msg = {
                "msg_type" : "on_rsp_order_insert",
                "status" : False,
                "inst_id" : '',
                "oid": str(params['oid']),
                "err_info" : ''
            }
        else:
            log.info('创建算法[{}]返回：{},{}'.format(algo_type, rsp.inst_id, rsp.err_info))
            rsp_msg = {
                "msg_type" : "on_rsp_order_insert",
                "status" : True,
                "inst_id" : rsp.inst_id,
                "oid": str(params['oid']),
                "err_info" : rsp.err_info
            }
            if batch is True:
                rsp_msg['param_list'] = params['param_list']
                rsp_msg['msg_type'] = "on_rsp_batch_order_insert"

        self.send_tcp_msg(rsp_msg)
    def get_limit_price(self, symbol, side):
        symbol_detail = get_symbol_detial(symbol)
        limit_price = 1.0
        if side == '1':
            limit_price = symbol_detail.HighLimitPrice
        elif side == '2':
            limit_price = symbol_detail.LowLimitPrice
        return limit_price
    def start(self):
        self.create_tcp_server()
        self.run()
    def run(self):
        ts = [
            threading.Thread(target=self.tcp_proc),
            threading.Thread(target=self.send_msg_hander),
            threading.Thread(target=self.msg_handler),
        ]
        for t in ts:
            t.setDaemon(True)
            t.start()
    def close(self):
        self.is_stopped = True
