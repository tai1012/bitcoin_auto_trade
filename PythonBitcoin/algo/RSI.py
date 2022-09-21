import pandas as pd

from dmm import data, data_1hour, data_15minutes

buy = 0
sell = 0
def rsi(df):
    # 前日との差分を計算
    df_diff = df["close"].diff(1)
 
    # 計算用のDataFrameを定義
    df_up, df_down = df_diff.copy(), df_diff.copy()
    
    # df_upはマイナス値を0に変換
    # df_downはプラス値を0に変換して正負反転
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0
    df_down = df_down * -1
    
    # 期間14でそれぞれの平均を算出
    df_up_sma14 = df_up.rolling(window=14, center=False).mean()
    df_down_sma14 = df_down.rolling(window=14, center=False).mean()
 
    # RSIを算出
    df["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))
 
    return df
 
# RSIを算出
rsi_data = rsi(data)
rsi_today_15m = rsi(data_15minutes)
rsi_today_1h = rsi(data_1hour)
print('rsi', rsi_data)
print('rsi1h', rsi_today_1h)
print('rsi15m', rsi_today_15m)

if rsi_today_15m['RSI'].iloc[-1] < 20:
    buy += 1.5
if rsi_today_15m['RSI'].iloc[-1] > 80:
    sell += 1.5

if rsi_today_1h['RSI'].iloc[-1] < 30:
    buy += 1
if rsi_today_1h['RSI'].iloc[-1] > 70:
    sell += 1

print('buy',buy, '===', 'sell', sell)