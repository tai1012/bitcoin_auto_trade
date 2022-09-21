import pandas as pd

from dmm import data, data_1hour, data_15minutes

buy = 0
sell = 0

bb_1h = data_1hour
bb_1h['SMA'] = pd.DataFrame(data_1hour['close'].rolling(window=20).mean())
bb_1h['std'] = pd.DataFrame(data_1hour['close'].rolling(window=20).std())

bb_15m = data_15minutes
bb_15m['SMA'] = pd.DataFrame(data_15minutes['close'].rolling(window=20).mean())
bb_15m['std'] = pd.DataFrame(data_15minutes['close'].rolling(window=20).std())

## ボリンジャーバンド
# trend判定
bb_1h['-σ'] = pd.DataFrame(bb_1h['SMA'] - bb_1h['std'])
bb_1h['+σ'] = pd.DataFrame(bb_1h['SMA'] + bb_1h['std'])
# range相場
bb_1h['-2σ'] = pd.DataFrame(bb_1h['SMA'] - 2*bb_1h['std'])
bb_1h['+2σ'] = pd.DataFrame(bb_1h['SMA'] + 2*bb_1h['std'])

bb_15m['-2σ'] = pd.DataFrame(bb_15m['SMA'] - 2*bb_15m['std'])
bb_15m['+2σ'] = pd.DataFrame(bb_15m['SMA'] + 2*bb_15m['std'])

print('bb1h', bb_1h)
print('bb15m', bb_15m)

if data_15minutes['close'].iloc[-1] < bb_15m['-2σ'].iloc[-1]:
    buy += 1.5
if bb_15m['+2σ'].iloc[-1] < data_15minutes['close'].iloc[-1]:
    sell += 1.5

if data_1hour['close'].iloc[-1] < bb_1h['-2σ'].iloc[-1]:
    buy += 1
if bb_1h['+2σ'].iloc[-1] < data_1hour['close'].iloc[-1]:
    sell += 1

print('buy',buy, '===', 'sell', sell)