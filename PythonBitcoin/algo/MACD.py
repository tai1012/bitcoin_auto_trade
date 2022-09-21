import pandas as pd

from dmm import data, data_1hour, data_15minutes

buy = 0
sell = 0

macd = data_15minutes
macd['ema_12'] = pd.DataFrame(data_15minutes['close'].ewm(span=12).mean())
macd['ema_26'] = pd.DataFrame(data_15minutes['close'].ewm(span=26).mean())

macd['macd'] = pd.DataFrame(macd['ema_12'] - macd['ema_26'])
macd['signal'] = pd.DataFrame(macd['macd'].ewm(span=9).mean())
macd['histogram'] = pd.DataFrame(macd['macd'] - macd['signal'])

print('macd', macd)

if macd['histogram'].iloc[-2] < 0 < macd['histogram'].iloc[-1]:
    buy += 1
    #trend が下降傾向
    if macd['macd'].iloc[-1] and macd['signal'].iloc[-1] < 0: 
        buy += 0.5

if macd['histogram'].iloc[-1] < 0 < macd['histogram'].iloc[-2]:
    sell += 1
    #　trend　が上昇傾向
    if macd['macd'].iloc[-1] and macd['signal'].iloc[-1] > 0:
        sell += 0.5

print('buy',buy, '===', 'sell', sell)