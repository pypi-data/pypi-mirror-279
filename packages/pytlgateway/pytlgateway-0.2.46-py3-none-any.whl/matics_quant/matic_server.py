# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import mmap,os
import datetime
import socket                               #导入socket模块
import threading
from trade_data_dump import TradeDataDownloader
from tcp_server import TcpServer

def initialize(context):
    fund_account_stock = context.get_fund_account_by_type(AccountType.normal)
    g.account_type_info = {}
    if fund_account_stock is not None and len(fund_account_stock) > 0:
        g.account_type_info[fund_account_stock] = AccountType.normal

    fund_account_margin = context.get_fund_account_by_type(AccountType.margin)
    if fund_account_margin is not None and len(fund_account_margin) > 0:
        g.account_type_info[fund_account_margin] = AccountType.margin

    g.max_symbol_cnt_per_algo_inst = 300
    g.download_trade_data = True

    if g.download_trade_data:
        g.trade_data_downloader = TradeDataDownloader()
        g.trade_data_downloader.set_context(context)
        g.trade_data_downloader.set_file_dir_path('C:/Users/SUST/Desktop/MQuantTradeData')
        g.trade_data_downloader.init_trade_files()

    tcp_server = TcpServer(int(context.run_params['port']))
    tcp_server.start()
    
def strategy_params():
    """
    category:事件回调
    brief:策略运行参数定义
    desc: 策略运行参数定义，可选实现。策略可自定义运行参数，启动策略时，会在启动弹框中显示策略自定义的参数，客户在界面修改参数值，修改后的参数会写入到context对象的run_params字段内，客户可在策略程序中通过context对象获取策略运行参数。目前支持int、float、string、list、table、bool类型的参数。

    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，由策略平台解析显示在界面上，支持编辑框、下拉列表、勾选框三种形式的参数，后续可根据需求进一步丰富
    :example:
        dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},                    #'desc'字段可填写，也可不填写，编辑框类型参数
       '委买价格':{'value':'17.50/27.5'},                                                        #编辑框类型参数
       '委卖价格':{'value':'18.50/28.0'},                                                        #编辑框类型参数
       '补单价格档位':{'value':['最新价','对手方一档','对手方二档','对手方3档','涨停价','跌停价']},  #下拉列表格式参数
       '使用持仓':{'value': True, 'desc':'买入篮子时是否使用持仓中已有的成分券额度'},                #bool类型参数
       '撤单时间间隔':{'value':10}                                                                #编辑框类型参数
       }
        return json.dumps(dict_params)
    """
    dict_params = {
        'ip': {'value':'127.0.0.1/139.224.119.84'},
        'port' : {'value' : [10500, 11000]}
    }
    return json.dumps(dict_params)

def on_strategy_start(context):
    """
    category:事件回调
    category-desc:MQuant的事件处理引擎会将交易系统内的各种事件以回调函数的形式通知给策略脚本，策略脚本根据自身的业务逻辑在对应的回调函数中进行相应处理
    brief:策略启动回调
    desc:策略启动回调，可选实现。策略初始化结束后，会立即调用此回调函数，策略在此回调函数中可以进行交易，不可读取外部文件、网络等。

    策略正式启动回调
    :param context:
    :return:
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    #get_position_info(context)

def handle_tick(context, tick, msg_type):
    """
    category:事件回调
    brief:TICK行情回调
    desc:TICK行情回调，可选实现。调用subscribe订阅TICK行情后，在此函数中接收实时TICK行情推送。回测模式下，如果选择TICK级回测，回测行情也在此回调函数中接收处理。

    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :param msg_type 消息类型，暂不启用
    :return:
    :remark:可选实现
    """
    pass

def handle_data(context, kline_data):
    """
    category:事件回调
    brief:K线行情回调
    desc:K线行情回调，可选实现。调用subscribe订阅1分钟K线行情后，在此函数中接收实时的分钟K线行情推送。回测模式下，如果选择分钟K或者日K回测，回测行情也在此回调函数中接收处理。
    k线数据接收函数，包含实时分钟k，回测模式下的分钟k和日k
    :param context:
    :param kline_data:KLineDataPush类型，回测模式下分钟k和日k都通过该函数接收推送
    :return:
    :remark:可选实现
    """
    pass

def handle_order_record(context, order_record, msg_type):
    """
    category:事件回调
    brief:逐笔委托回调
    desc:逐笔委托回调，可选实现。调用subscribe订阅逐笔委托行情后，在此函数中接收实时的逐笔委托行情推送。回测模式不支持逐笔数据订阅。
    处理逐笔委托
    :param context: Context对象
    :param order_record: 逐笔委托数据，RecordOrder对象
    :param msg_type:
    :return:
    :remark:可选实现
    """
    pass

def handle_record_transaction(context, record_transaction, msg_type):
    """
    category:事件回调
    brief:逐笔成交回调
    desc:逐笔成交回调，可选实现。调用subscribe订阅逐笔成交行情后，在此函数中接收实时的逐笔成交行情推送。回测模式不支持逐笔数据订阅。
    处理逐笔成交
    :param context: Context对象
    :param record_transaction: 逐笔成交数据，RecordTransaction对象
    :param msg_type: 保留
    :return:
    :remark:可选实现
    """
    pass

def decode_ord_status(status):
    if status == OrderStatus.open:
        return 0
    elif status == OrderStatus.canceled:
        return 2
    elif status == OrderStatus.rejected:
        return 3
    elif status == OrderStatus.held:
        return 4

def transfer_order_side(side):
    if side == OrderSide.BUY:
        return 1
    elif side == OrderSide.SELL:
        return 2
    else:
        return -1

def deal_order_msg(ord):
    try:
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_order_update(ord)
    except:
        pass

def handle_order_report(context, ord, msg_type):
    """
    category:事件回调
    brief:订单回报函数
    desc:订单回报函数，可选实现。策略报单后，只要订单状态改变，都会进入订单回报函数，策略可以在此函数中判断订单状态并决定后续操作，只要当前策略报单的订单回报会通过此函数通知给策略。回测模式下，订单回报也在此函数中处理。
    订单回报处理函数
    :param ord:Order对象
    :param msg_type 消息类型，透传字段，调用查询接口时传入可获得协程并发
    :return:
    :remark:可选实现
    """
    # print(ord.__dict__)
    deal_order_msg(ord)


def handle_execution_report(context, execution, msg_type):
    """
    category:事件回调
    brief:成交回报函数
    desc:成交回报函数，可选实现。策略报单后，只要订单产生成交（可能分多笔成交），都会进入成交回报函数，策略可以在此函数中获取本次成交信息（成交价格、数量、金额等），只要当前策略报单的成交回报会通过此函数通知给策略。回测模式下，成交回报也在此函数中处理。
    成交回报
    :param context:
    :param execution:Trade对象
    :param msg_type:
    :return:
    """
    try:
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_execution_update(execution)
    except:
        pass

def on_fund_update(context, fund_info):
    """
    category:事件回调
    brief:资金推送
    desc:资金推送函数，可选实现。
    :param context:
    :param fund_info: FundUpdateInfo 类对象
    :return:
    """
    try:
        # print('recv fund update:', fund_info.__dict__)
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_fund_update(fund_info)
    except:
        pass

def get_position_info(context):
    msg_type = "on_position"
    fund_account = context.get_fund_account_by_type(AccountType.normal)
    account_type = g.account_type_info[fund_account]
    pos_list = get_positions_ex(account_type)
    if pos_list is not None:
        for pos in pos_list:
            pos_dict = {
                "msg_type" : msg_type,
                "fund_account" : fund_account,
                "symbol" : pos.security,
                "total_amount" : pos.total_amount,
                "closeable_amount" : pos.closeable_amount,
                "init_amount" : pos.init_amount,
                "hold_cost" : pos.hold_cost,
                "value" : pos.value
            }

            send_tcp_msg(pos_dict)

def on_position_update(context, pos_info):
    """
    category:事件回调
    brief:持仓推送
    desc:持仓推送函数，可选实现。
    :param context:
    :param pos_info: Position类对象
    :return:
    """
    try:
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_position_update(pos_info)
    except:
        pass

def handle_fund_flow(context, fund_flow):
    """
    category:事件回调
    brief:实时资金流向推送
    desc:实时资金流向推送函数，可选实现。
    :param context:
    :param fund_flow:资金流向数据，FundFlow类型
    :return:
    """
    pass

def on_strategy_params_change(params, path):
    """
    category:事件回调
    brief:参数修改回调
    desc:参数修改回调，可选实现。用户在策略执行监控界面的实例列表中，点击参数修改按钮修改实例参数时，参数信息会通过此回调通知给策略，支持修改策略启动参数值或者传入参数文件。

    监控界面修改策略实例参数回调
    :param params:参数，支持任意形式的文本参数
    :param path:如果传入的是参数文件，path为文件路径，否则path为空字符串
    :return:
    :remark:可选实现
    """
    pass

def on_rsp_user_params(context, json_params, wnd_title):
    """
    category:事件回调
    brief:请求用户参数异步响应
    desc:策略调用get_user_params在界面弹出一个参数框（异步模式），用户修改参数后，点击确定，修改后的参数将通过此回调函数回传给策略

    请求用户参数异步响应
    :param context:
    :param json_params:
    :param wnd_title:
    :return:
    :remark:可选实现
    """
    pass

def on_request_user_params_template(context, params):
    """
    category:事件回调
    brief:触发弹出用户参数设置窗口
    desc:用户在策略执行监控实例列表界面点击手工干预按钮，将会触发此回调函数，策略可以在此回调函数中获取用户参数，也可不实现
    :param context:
    :param params: 保留字段
    :return:
    :remark:可选实现
    """
    pass

def handle_etf_estimate_info(context, etf_estimate_info, msg_type):
    """
    实时ETF预估信息接收函数
    :param context:上下文
    :param etf_estimate_info: EtfEstimateInfo对象
    :param msg_type 保留字段
    :return:
    :remark:可选实现
    """
    pass

def market_open(context, trade_date):
    """
    category:事件回调
    brief:开盘信号
    desc:开盘信号，可选实现。回测模式下，回测周期内的每个交易日开始时，都会发送一个开盘信号给策略，策略在此回调函数中进行每日初始化操作。注意，仅回测模式有效。
    开盘信号，回测专用，在该回调中进行每日初始化操作，例如查询数据，处理静态数据等，日k回测在该回调函数中报单时，订单在当日撮合，在handle_data中报单时，订单在下一个交易日撮合
    :param context:
    :param trade_date:当前交易日
    :return:
    :remark:可选实现
    """
    pass

def market_close(context, trade_date):
    """
    category:事件回调
    brief:收盘信号
    desc:收盘信号，可选实现。回测模式下，回测周期内的每个交易日结束时，都会发送一个收盘信号给策略，策略在此回调函数中进行每日日终操作。注意，仅回测模式有效。
    收盘信号,回测专用
    :param context:
    :param trade_date: 交易日
    :return:
    :remark:可选实现
    """
    pass

def on_strategy_ready_stop(context):
    """
    category:事件回调
    brief:策略准备结束回调
    desc:策略准备结束回调，可选实现。停止策略时，会先调用此回调，调用结束后，再调用on_strategy_end回调。该回调中允许交易，不允许与外部系统交互，策略可选择在此回调函数中撤掉在途订单。
    :param context:
    :return:
    """
    pass

def on_strategy_end(context):
    """
    category:事件回调
    brief:策略结束回调
    desc:策略结束回调，可选实现。策略实例终止时，MQuant会调用此回调函数通知策略进行一些数据保存、环境清理等工作，待策略的处理工作结束后再结束策略进程。特别注意，如果直接关闭策略进程，可能导致此函数未执行完毕进程就已经关闭，建议通过策略执行监控界面或者通过stop_strategy API终止策略。
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    pass

def on_recv_order_reply(context, order_reply):
    """
    category:事件回调
    brief:报撤单异步响应
    desc:报撤单异步响应，可选实现。必须调用set_enable_order_reply(True)开启响应消息推送后，才可收到响应。set_enable_order_reply是全局开关，任何一个实例调用此接口设置后，其他实例都会受影响。
    :param context:
    :param order_reply: class OrderReply
    :return:
    """
    pass

def on_system_msg(context, error_code, error_msg):
    """
    category:事件回调
    brief:系统消息
    desc:系统消息,可选实现。
    :param context:
    :param error_code:
    :param error_msg:
    :return:
    """
    pass
