import pandas as pd

from dmm import data, data_1hour

buy = 0
sell = 0
#ストキャスティクス
def STCK(high, low, close, n):
    STOK = ((close - low.rolling(window=n, center=False).min()) / ( high.rolling(window=n,center=False).max() - low.rolling(window=n,center=False).min())) * 100 
    STOD = STOK.rolling(window=3,center=False).mean()
    STOSD = STOD.rolling(window=3, center=False).mean()    
    
    return STOK, STOD, STOSD
# trend判定
stck = data
stck['%K'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[0]).rename(columns={0:'%K'})
stck['%D'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[1]).rename(columns={0:'%D'})
stck['%SD'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[2]).rename(columns={0:'%SD'})
stck = stck.dropna()
stck = stck.iloc[-15:]


# range相場時のストキャス
stck_1h = data_1hour
# stck_1h['close'].iloc[-20:] = data['close'].iloc[-20:]
# stck_1h['close'] = data['close'].copy()
stck_1h['%K'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[0]).rename(columns={0:'%K'})
stck_1h['%D'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[1]).rename(columns={0:'%D'})
stck_1h['%SD'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[2]).rename(columns={0:'%SD'})
stck_1h = stck_1h.dropna()
stck_1h = stck_1h.iloc[-15:]
print(stck)
print(stck_1h)
if stck['%K'].iloc[-1] <= 20:
    if stck_1h['%K'].iloc[-2] < stck_1h['%SD'].iloc[-2] and stck_1h['%K'].iloc[-1] > stck_1h['%SD'].iloc[-1]:
        buy += 1
if stck['%K'].iloc[-1] >= 80:
    if stck_1h['%K'].iloc[-2] > stck_1h['%SD'].iloc[-2] and stck_1h['%K'].iloc[-1] < stck_1h['%SD'].iloc[-1]:
        sell += 1
print('buy',buy, '===', 'sell', sell)