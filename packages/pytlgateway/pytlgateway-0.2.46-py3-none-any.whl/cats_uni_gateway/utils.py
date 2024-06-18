from datetime import datetime

#没有融券
def decode_cats_side(side):
    rtn_trade_side = 0
    if side == '1':
        rtn_trade_side = 1
    elif side == '2':
        rtn_trade_side = 2
    elif side == 'A':
        rtn_trade_side = 3
    return rtn_trade_side

def decode_cats_status(status, entrust_vol, filled_vol):
    new_status = ""
    if status in [0, 1]:
        new_status = 'active'
    elif status == 2:
        if filled_vol < entrust_vol:
            new_status = 'canceled'
        else:
            new_status = 'filled'
    return new_status

def side_to_target_type(side):
    target_type = ""
    if side in ['1','A']:
        target_type = "buy"
    elif side == '2':
        target_type = "sell"
    return target_type

def decode_exchange_id(str_exchange):
    exchange = 0
    if str_exchange == 'SH':
        exchange = 101        #EXCHANGE_SSE 
    elif str_exchange == 'SZ':
        exchange = 102        #EXCHANGE_SZE 
    return exchange


def decode_ordtype(order_type:str):
    ord_type = -1
    mapping = {
        'twap': 'TWAP',
        'vwap': 'VWAP',
        'vwap3': 'VWAP3',
        'twap3': 'TWAP3',
        'SmartVWAP' : 'SmartVWAP3',
        'SmartTWAP' : 'SmartTWAP3',
        'kf_vwap_plus' : 'KF_VWAP_Plus',
        'kf_twap_plus' : 'KF_TWAP_Plus',
        'kf_pov_core' : 'KF_POV_Core',
        'VolumeInline3' : 'VolumeInline3',
        'SmartVolumeInline3' : 'SmartVolumeInline3'
    }
    ord_type = mapping.get(order_type, -1)
    return ord_type
