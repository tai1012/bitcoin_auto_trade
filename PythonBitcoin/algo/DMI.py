import pandas as pd
import time 

from dmm import data, data_1hour, data_15minutes
from utils.notify import send_message_to_line

def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()
    
    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()
    return plus_di, minus_di, adx_smooth

while True:
    time.sleep(15*60)
    buy_15m = 0
    sell_15m = 0
    buy_1h = 0
    sell_1h = 0
    
        
    # trend判定
    dmi = data
    dmi['plus_di'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi['minus_di'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi['adx'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi = dmi.dropna()
    # trend相場
    dmi_15m = data_15minutes
    dmi_15m['plus_di'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], data_15minutes['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi_15m['minus_di'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], data_15minutes['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi_15m['adx'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], data_15minutes['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi_15m = dmi_15m.dropna()
    # range相場
    dmi_1h = data_1hour
    dmi_1h['plus_di'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi_1h['minus_di'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi_1h['adx'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi_1h = dmi_1h.dropna()
    dmi_1h = dmi_1h.iloc[-15:]
    
    if dmi_15m['adx'].iloc[-2] < dmi_15m['adx'].iloc[-1] and dmi_15m['plus_di'].iloc[-2] < dmi_15m['minus_di'].iloc[-2] and dmi_15m['plus_di'].iloc[-1] > dmi_15m['minus_di'].iloc[-1]:
        buy_15m += 1
        if dmi_15m['adx'].iloc[-1] > dmi_15m['minus_di'].iloc[-1]:
            buy_15m = 0.5
    if dmi_15m['adx'].iloc[-2] < dmi_15m['adx'].iloc[-1] and dmi_15m['plus_di'].iloc[-2] > dmi_15m['minus_di'].iloc[-2] and dmi_15m['plus_di'].iloc[-1] < dmi_15m['minus_di'].iloc[-1]:
        sell_15m += 1
        if dmi_15m['adx'].iloc[-1] > dmi_15m['plus_di'].iloc[-1]:
            sell_15m += 0.5   


    if dmi_1h['adx'].iloc[-2] < dmi_1h['adx'].iloc[-1] and dmi_1h['plus_di'].iloc[-2] < dmi_1h['minus_di'].iloc[-2] and dmi_1h['plus_di'].iloc[-1] > dmi_1h['minus_di'].iloc[-1]:
        buy_1h += 1
    if dmi_1h['adx'].iloc[-2] < dmi_1h['adx'].iloc[-1] and dmi_1h['plus_di'].iloc[-2] > dmi_1h['minus_di'].iloc[-2] and dmi_1h['plus_di'].iloc[-1] < dmi_1h['minus_di'].iloc[-1]:
        sell_1h += 1
    # print('buy',buy, '===', 'sell', sell)
    send_message_to_line({'dmi1h_buy': str(buy_1h),
                        'dmi1h_sell': str(sell_1h),
                        'dmi15m_buy': str(buy_15m), 
                        'dmi15m_sell': str(sell_15m)
                        })

