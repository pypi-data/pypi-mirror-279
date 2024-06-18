import math
def decode_algo_type(order_type:str):
    algo_type = -1
    mapping = {
        'kf_twap_plus': 27,
        'kf_vwap_plus': 28,
        'smart_kf' : 29, #T0策略，smarT_I,该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_卡方
        'smart_yr' : 30,
        'ft_twap_plus': 37,
        'ft_vwap_plus': 38
    }
    algo_type = mapping.get(order_type, -1)
    return algo_type

def date_to_str(date):
    year = int(date / 10000)
    month = int((date - 10000 * year) / 100)
    day = date - 10000 * year - 100 * month
    str_date = f'{year:04d}-{month:02d}-{day:02d} '
    return str_date

def decode_exchange_id(str_exchange):
    exchange = 0
    if str_exchange == 'SH':
        exchange = 101        #EXCHANGE_SSE 
    elif str_exchange == 'SZ':
        exchange = 102        #EXCHANGE_SZE 
    return exchange

def encode_exchange_id(exchange):
    if exchange.startswith('6'):
        str_exchange = '.SH'
    elif exchange.startswith('5'):
        str_exchange = '.SH'
    elif exchange.startswith('2'):
        str_exchange = '.SH'
    elif exchange.startswith('0'):
        str_exchange = '.SZ'
    else:
        str_exchange = '.SZ'

    return str_exchange

def transfer_order_side(side):
    if side == 'long':
        return 1
    elif side == 'short':
        return 2
    else:
        return -1
    
def side_to_target_type(side):
    target_type = ''
    if side in [1,5]:
        target_type = 'buy'
    elif side == 2:
        target_type = 'sell'
    return target_type

def decode_mquant_status(status):
    new_status = ''
    if status == 0:
        new_status = 'active'
    elif status == 4:
        new_status = 'filled'
    elif status == 2:
        new_status = 'canceled'
    return new_status

def decode_symbol_type(symbol_type):
    if symbol_type == 0:
        return (1000000, 10000000)
    elif symbol_type == 1:
        return (500000, 2000000)
    elif symbol_type == 2:
        return (300000, 3000000)
    elif symbol_type == 3:
        return (100000, 1000000)

def check_split(volume, price, symbol_type):
    """_summary_ 判断是否需要拆单,返回volume_list

    Args:
        volume (int): 下单量
        price (float): last_price,估计价格
        symbol_type (int):0-普通沪深主板， 1-风险警示股票(ST), 2-创业板， 3-科创板)
    """
    volume_list = []
    max_price = 1.1 * price
    max_volume, max_amt = decode_symbol_type(symbol_type)
    if volume <= max_volume and volume <= max_amt / max_price:
        return [volume]
    else:
        _split_volume = int(min(max_volume, max_amt/max_price))
        split_volume = _split_volume // 1000 * 1000
        while volume > split_volume:
            volume_list.append(volume)
            volume -= split_volume
        volume_list.append(volume)
        return volume_list
