import configparser
import datetime
import json
import requests
import time

import pandas as pd

from coincheck import Coincheck
from utils.notify import send_message_to_line


# keyの読み込み
conf = configparser.ConfigParser()
conf.read('config.ini')

ACCESS_KEY = conf['coincheck']['access_key']
SECRET_KEY = conf['coincheck']['secret_key']

coincheck = Coincheck(access_key=ACCESS_KEY, secret_key=SECRET_KEY)

# インスタンス変数の設定
trend_flag = 0 # trend判定 
interval = 60*15 # 間隔(15分に一回実行)
duration = 20 # データの個数

AMOUNT = 0.005 # bitcoinの売買の量

df = pd.DataFrame()
df_1h = df
df_15m = df 
send_message_to_line('Start Auto Trading...')
# ビットコインの最新価格を取得
while True:
    position = coincheck.position
    # time.sleep(0.5)#

    # 通知
    if not position.get('jpy'):
        send_message_to_line('My account balance is zero')
        raise
    # time.sleep(0.5)#
    df = df.append({'close': coincheck.last}, ignore_index=True)
    df_15m = df.copy()
    df_1h = df.iloc[::4].copy()
    # if len(df_1h) == 0:
    #     df_1h = df_1h.append({'close': coincheck.last}, ignore_index=True)
    # df_15m = df_15m.append({'close': coincheck.last}, ignore_index=True)
    # if len(df_15m) % 4 == 0:
    #     df_1h = df_1h.append({'close': coincheck.last}, ignore_index=True)
    
    time.sleep(interval)

    if trend_flag < 2: 
        if df_1h['close'].iloc[-1] != df_15m['close'].iloc[-1]:
            continue
    # time.sleep(0.5)#
    if len(df_1h) < duration:
        continue

    def data_20d():
        ymd = datetime.date.today() - datetime.timedelta(days=20)
        year = str(ymd.year)
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC&interval=1day&date='+year
        r =  requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    # json デコード
    dec_day_20d =json.loads(data_20d())

    # 最新の高値
    # data_last = dec['data'][-1]['high']
    # print(int(data_last))
    dec_data1d_20d = dec_day_20d['data'] 
    date =[d.get('openTime') for d in dec_data1d_20d[-20:]]
    date = [int(i) for i in date]

    # 高値の213個のデータ high
    data_high = [h.get('high') for h in dec_data1d_20d[-20:]]
    new_data_high = [int(i) for i in data_high]

    # 安値のデータ low
    data_low = [l.get('low') for l in dec_data1d_20d[-20:]]
    new_data_low = [int(i) for i in data_low]

    # 最新価格　close
    data_close = [c.get('close') for c in dec_data1d_20d[-20:]]
    new_data_close = [int(i) for i in data_close]

    data_20d = pd.DataFrame(list(zip(new_data_close,
                                new_data_high,
                                new_data_low)),
                        index=date,columns=['close', 'high', 'low'])

    def data_1d():
        ymd = datetime.date.today()
        year = str(ymd.year)
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC&interval=1day&date='+year
        r =  requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    # json デコード
    dec_day =json.loads(data_1d())

    # 最新の高値
    # data_last = dec['data'][-1]['high']
    # print(int(data_last))
    dec_data1d = dec_day['data'] 
    date =[d.get('openTime') for d in dec_data1d]
    date = [int(i) for i in date]

    # 高値の213個のデータ high
    data_high = [h.get('high') for h in dec_data1d]
    new_data_high = [int(i) for i in data_high]

    # 安値のデータ low
    data_low = [l.get('low') for l in dec_data1d]
    new_data_low = [int(i) for i in data_low]

    # 最新価格　close
    data_close = [c.get('close') for c in dec_data1d]
    new_data_close = [int(i) for i in data_close]

    data = pd.DataFrame(list(zip(new_data_close,
                                new_data_high,
                                new_data_low)),
                        index=date,columns=['close', 'high', 'low'])
    if len(data) < 20:
        data = pd.concat([data_20d, data], axis=0)


    def data_1yh():
        ymd = datetime.datetime.today() - datetime.timedelta(days=1) - datetime.timedelta(hours=6)
        today = f'{ymd:%Y%m%d}'
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC&interval=1hour&date='+today
        r = requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    # ５時で切り替わる
    # 昨日の６時から今日の５時までのデータ
    dec_1hour_yesterday =json.loads(data_1yh())
    dec_data1yh = dec_1hour_yesterday['data']
    date = [d.get('openTime') for d in dec_data1yh]
    date = [int(i) for i in date]
    # 高値の213個のデータ high
    data_high = [h.get('high') for h in dec_data1yh]
    new_data_high = [int(i) for i in data_high]
    # 安値のデータ low
    data_low = [l.get('low') for l in dec_data1yh]
    new_data_low = [int(i) for i in data_low]
    # 最新価格　close
    data_close = [c.get('close') for c in dec_data1yh]
    new_data_close = [int(i) for i in data_close]

    data_1hour_yesterday = pd.DataFrame(list(zip(new_data_close,
                                new_data_high,
                                new_data_low)),
                        index=date, columns=['close', 'high', 'low'])

    def data_1h():
        ymd = datetime.datetime.today() - datetime.timedelta(hours=6)
        today = f'{ymd:%Y%m%d}'
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC&interval=1hour&date='+today
        r = requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    dec_1hour =json.loads(data_1h())
    dec_data1h = dec_1hour['data']
    date = [d.get('openTime') for d in dec_data1h]
    date = [int(i) for i in date]
    # 高値のデータ high
    data_high = [h.get('high') for h in dec_data1h]
    new_data_high = [int(i) for i in data_high]
    # 安値のデータ low
    data_low = [l.get('low') for l in dec_data1h]
    new_data_low = [int(i) for i in data_low]
    # 最新価格　close
    data_close = [c.get('close') for c in dec_data1h]
    new_data_close = [int(i) for i in data_close]
    old_data_1hour = pd.DataFrame(list(zip(new_data_close,
                                new_data_high,
                                new_data_low)),
                        index=date, columns=['close', 'high', 'low'])
    data_1hour = pd.concat([data_1hour_yesterday, old_data_1hour], axis=0)
    def data_15ym():
        ymd = datetime.datetime.today() - datetime.timedelta(days=1) - datetime.timedelta(hours=6)
        today = f'{ymd:%Y%m%d}'
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC_JPY&interval=15min&date='+today
        r = requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    dec_15min_yesterday = json.loads(data_15ym())
    dec_data15ym = dec_15min_yesterday['data']
    date = [d.get('openTime') for d in dec_data15ym]
    date_15ym = [int(i) for i in date]
    # # 高値のデータ high
    data_high_15ym = [h.get('high') for h in dec_data15ym]
    new_data_high_15ym = [int(i) for i in data_high_15ym]
    # # 安値のデータ low
    data_low_15ym = [l.get('low') for l in dec_data15ym]
    new_data_low_15ym = [int(i) for i in data_low_15ym]
    # # 最新価格　close
    data_close_15ym = [c.get('close') for c in dec_data15ym]
    new_data_close_15ym = [int(i) for i in data_close_15ym]
    data_15min_yesterday = pd.DataFrame(list(zip(new_data_close_15ym,
                                                new_data_high_15ym,
                                                new_data_low_15ym)),
                                                index=date_15ym, columns=['close', 'high', 'low'])

    def data_15m():
        ymd = datetime.datetime.today() - datetime.timedelta(hours=6)
        today = f'{ymd:%Y%m%d}'
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/klines?symbol=BTC_JPY&interval=15min&date='+today
        r = requests.get(endPoint + path)
        return json.dumps(r.json(), indent=2)
    time.sleep(0.2)
    dec_15min = json.loads(data_15m())
    dec_data15m = dec_15min['data']
    date = [d.get('openTime') for d in dec_data15m]
    date_15m = [int(i) for i in date]
    # 高値のデータ high
    data_high = [h.get('high') for h in dec_data15m]
    new_data_high = [int(i) for i in data_high]
    # 安値のデータ low
    data_low = [l.get('low') for l in dec_data15m]
    new_data_low = [int(i) for i in data_low]
    # 最新価格　close
    data_close = [c.get('close') for c in dec_data15m]
    new_data_close = [int(i) for i in data_close]

    old_data_15min = pd.DataFrame(list(zip(new_data_close,
                                new_data_high,
                                new_data_low)),
                        index=date_15m, columns=['close', 'high', 'low'])
    data_15minutes = pd.concat([data_15min_yesterday, old_data_15min], axis=0)
    
    data = data.iloc[-20:]
    data_1hour = data_1hour.iloc[-20:]
    data_15minutes = data_15minutes.iloc[-20:]

    #フラグの回収
    buy_flag = 0
    sell_flag = 0
    trend_flag = 0

    ## ADX DMI
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
        
    # trend判定
    dmi = data.copy()
    dmi['plus_di'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi['minus_di'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi['adx'] = pd.DataFrame(get_adx(data['high'], data['low'], data['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi = dmi.dropna()

    # trend相場
    dmi_15m = data_15minutes.copy()
    dmi_15m['plus_di'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], df_15m['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi_15m['minus_di'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], df_15m['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi_15m['adx'] = pd.DataFrame(get_adx(data_15minutes['high'], data_15minutes['low'], df_15m['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi_15m = dmi_15m.dropna()

    # range相場
    dmi_1h = data_1hour.copy()
    dmi_1h['plus_di'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], df_1h['close'], 14)[0]).rename(columns = {0:'plus_di'})
    dmi_1h['minus_di'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], df_1h['close'], 14)[1]).rename(columns = {0:'minus_di'})
    dmi_1h['adx'] = pd.DataFrame(get_adx(data_1hour['high'], data_1hour['low'], df_1h['close'], 14)[2]).rename(columns = {0:'adx'})
    dmi_1h = dmi_1h.dropna()
    
    # ±DM dirextional movement
    #trend判定
    if dmi['adx'].iloc[-1] > 25:   
        trend_flag += 1

    #ボリンジャーとRSIでもトレンド判定
    # ボリンジャーバンドを計算
    bb_1h = df_1h.copy()
    bb_1h['SMA'] = pd.DataFrame(df_1h['close'].rolling(window=duration).mean())
    bb_1h['std'] = pd.DataFrame(df_1h['close'].rolling(window=duration).std())
    
    bb_15m = df_15m.copy()
    bb_15m['SMA'] = pd.DataFrame(df_15m['close'].rolling(window=duration).mean())
    bb_15m['std'] = pd.DataFrame(df_15m['close'].rolling(window=duration).std())
    
    ## ボリンジャーバンド
    # trend判定
    bb_1h['-σ'] = pd.DataFrame(bb_1h['SMA'] - bb_1h['std'])
    bb_1h['+σ'] = pd.DataFrame(bb_1h['SMA'] + bb_1h['std'])
    # range相場
    bb_1h['-2σ'] = pd.DataFrame(bb_1h['SMA'] - 2*bb_1h['std'])
    bb_1h['+2σ'] = pd.DataFrame(bb_1h['SMA'] + 2*bb_1h['std'])

    # trend相場
    bb_15m['-2σ'] = pd.DataFrame(bb_15m['SMA'] - 2*bb_15m['std'])
    bb_15m['+2σ'] = pd.DataFrame(bb_15m['SMA'] + 2*bb_15m['std'])
    
    #trend 判定
    if df_1h['close'].iloc[-1] < bb_1h['-σ'].iloc[-1] or bb_1h['+σ'].iloc[-1] < df_1h['close'].iloc[-1]:
            trend_flag += 1
    
    # RSI
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
    data_rsi = data.copy()
    rsi_data = rsi(data_rsi)
    if rsi_data['RSI'].iloc[-1] >= 50 and rsi_data['RSI'].iloc[-2] <= 50:
        trend_flag += 1
    if rsi_data['RSI'].iloc[-1] <= 50 and rsi_data['RSI'].iloc[-2] >= 50:
        trend_flag += 1
   
    rsi_data = rsi_data.iloc[-15:]
    
    #ストキャスティクス
    def STCK(high, low, close, n):
        STOK = ((close - low.rolling(window=n, center=False).min()) / ( high.rolling(window=n,center=False).max() - low.rolling(window=n,center=False).min())) * 100 
        STOD = STOK.rolling(window=3,center=False).mean()
        STOSD = STOD.rolling(window=3, center=False).mean()    
        
        return STOK, STOD, STOSD
    # trend判定
    stck = data.copy()
    stck['%K'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[0]).rename(columns={0:'%K'})
    stck['%D'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[1]).rename(columns={0:'%D'})
    stck['%SD'] = pd.DataFrame(STCK(data['high'], data['low'], data['close'], 14)[2]).rename(columns={0:'%SD'})
    stck = stck.dropna()
    
    # range相場時のストキャス
    stck_1h = data_1hour.copy()
    stck_1h['close'].iloc[-15:] = df_1h['close'].iloc[-15:]
    stck_1h['%K'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[0]).rename(columns={0:'%K'})
    stck_1h['%D'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[1]).rename(columns={0:'%D'})
    stck_1h['%SD'] = pd.DataFrame(STCK(data_1hour['high'], data_1hour['low'], data_1hour['close'], 14)[2]).rename(columns={0:'%SD'})
    stck_1h = stck_1h.dropna()

    # range相場の場合のみ ## flag作成
    if trend_flag >= 2:
        pass
    else:
        if stck['%K'].iloc[-1] <= 20:
            if stck_1h['%K'].iloc[-2] < stck_1h['%SD'].iloc[-2] and stck_1h['%K'].iloc[-1] > stck_1h['%SD'].iloc[-1]:
                buy_flag += 1
        if stck['%K'].iloc[-1] >= 80:
            if stck_1h['%K'].iloc[-2] > stck_1h['%SD'].iloc[-2] and stck_1h['%K'].iloc[-1] < stck_1h['%SD'].iloc[-1]:
                sell_flag += 1

    stck = stck.iloc[-15:]
    stck_1h = stck_1h[-15:]

    # trend相場の場合
    # ボリンジャーバンド
    if trend_flag >= 2:
        if df_15m['close'].iloc[-1] < bb_15m['-2σ'].iloc[-1]:
            buy_flag += 1.5
        if bb_15m['+2σ'].iloc[-1] < df_15m['close'].iloc[-1]:
            sell_flag += 1.5
    # range相場の場合
    else:
        if df_1h['close'].iloc[-1] < bb_1h['-2σ'].iloc[-1]:
            buy_flag += 1
        if bb_1h['+2σ'].iloc[-1] < df_1h['close'].iloc[-1]:
            sell_flag += 1
    
    bb_1h = bb_1h.iloc[-20:]
    bb_15m = bb_15m.iloc[-20:]

    # MACD を計算
    macd = df_15m.copy()
    macd['ema_12'] = pd.DataFrame(df_15m['close'].ewm(span=12).mean())
    macd['ema_26'] = pd.DataFrame(df_15m['close'].ewm(span=26).mean())

    macd['macd'] = pd.DataFrame(macd['ema_12'] - macd['ema_26'])
    macd['signal'] = pd.DataFrame(macd['macd'].ewm(span=9).mean())
    macd['histogram'] = pd.DataFrame(macd['macd'] - macd['signal'])
    
    #trend相場の場合のみ
    if trend_flag >= 2:
        if macd['histogram'].iloc[-2] < 0 < macd['histogram'].iloc[-1]:
            buy_flag += 1
            #trend が下降傾向
            if macd['macd'].iloc[-1] and macd['signal'].iloc[-1] < 0: 
                buy_flag += 0.5
        
        if macd['histogram'].iloc[-1] < 0 < macd['histogram'].iloc[-2]:
            sell_flag += 1
            #　trend　が上昇傾向
            if macd['macd'].iloc[-1] and macd['signal'].iloc[-1] > 0:
                sell_flag += 0.5
    
    macd = macd.iloc[-30:]

    # RSI
    # trend相場の場合　## flag回収
    df_15m_rsi = df_15m.copy()
    rsi_today_15m = rsi(df_15m_rsi)
    rsi_today_15m = rsi_today_15m.iloc[-15:]
    df_1h_rsi = df_1h.copy()
    rsi_today_1h = rsi(df_1h_rsi)
    rsi_today_1h = rsi_today_1h.iloc[-15:]
    
    if trend_flag >= 2:
        if rsi_today_15m['RSI'].iloc[-1] < 20:
            buy_flag += 1.5
        if rsi_today_15m['RSI'].iloc[-1] > 80:
            sell_flag += 1.5
    # range相場の場合
    else:
        if rsi_today_1h['RSI'].iloc[-1] < 30:
            buy_flag += 1
        if rsi_today_1h['RSI'].iloc[-1] > 70:
            sell_flag += 1

    # DMI 相場の検討　トレンド　レンジ ()
    ## ボリンジャーバンドが　±σ　を超えた時にトレンドの発生予兆 トレンドにflag (fin)
    # ±σ以内の時はレンジ相場

    ## RSI が正か負かに変わったタイミングでトレンド発生の予兆  トレンドにflag  (fin)
    # 負から正　正から負　に切り替わるタイミングは　トレンドかも？
    # ずっと正　ずっと負　の状態はレンジ相場

    ## ADX 25を境に判断 (fin)
    # ・ADXが25以上の場合：トレンド相場なので「順張り」で臨む トレンドにflag
    # ・ADXが25未満の場合：レンジ相場の可能性が高いので「逆張り」で臨
    
    ###　ボリンジャー RSI　ADX の3つ中2個が反応したらトレンド相場
    #補足flag ↓も　反応した場合はかなり強めに出る どっちに流れるかの判断だから
    #これは購入フェーズかも
    # macdとシグナル　一個前がマイナスで0以上になった時上昇トレンド 
    #               一個前がプラスで0以下の時下降トレンド
  
    # ここで条件分岐　↓
    ## トレンド相場の時　interval 変える　＝　15min とか 60* 15or30
    ### RSIを買い20％以下　売り80%以上　flag +1.5
    ### MACD　ゴールデンクロス　デッドクロスの判断　flag ＋1
    ### ⇨if macd and signal が０で転換したら⇨
    ### MACDとシグナルがゼロで転換した場合に信頼度増す⇨ flag＋0.5
    # ボリンジャーバンド　が±2σ　でflag +1.5
    # falg 回収が３以上でエントリー

    ## レンジ相場　1時間　  60*60　main interval
    # ストキャスティクス　20以下でゴールデンクロスbuy_flag +1
    #                 80以上でデッドクロスsell_flag +1
    ### RSI　30〜70の間で推移　RSI に触れたら　売り買いflag　＋1
    ### ボリンジャーバンド　逆張り ±２σに触れたら　売り買いのflag　＋１
    #flag回収　が２以上でエントリー

    #両相場で使う
    # ADXが上むきかつで　±DI がクロス　＋DIが-DIを上から下に抜くとき買い buy_flag +1
    # ADXが上向きかつ　　＋DIがーDIを上に抜くときsell_flag +1

    # DMI
    if trend_flag >= 2:
        if dmi_15m['adx'].iloc[-2] < dmi_15m['adx'].iloc[-1] and dmi_15m['plus_di'].iloc[-2] < dmi_15m['minus_di'].iloc[-2] and dmi_15m['plus_di'].iloc[-1] > dmi_15m['minus_di'].iloc[-1]:
            buy_flag += 1
            if dmi_15m['adx'].iloc[-1] > dmi_15m['minus_di'].iloc[-1]:
                buy_flag = 0.5
        if dmi_15m['adx'].iloc[-2] < dmi_15m['adx'].iloc[-1] and dmi_15m['plus_di'].iloc[-2] > dmi_15m['minus_di'].iloc[-2] and dmi_15m['plus_di'].iloc[-1] < dmi_15m['minus_di'].iloc[-1]:
            sell_flag += 1
            if dmi_15m['adx'].iloc[-1] > dmi_15m['plus_di'].iloc[-1]:
                sell_flag += 0.5
    else:    
        if dmi_1h['adx'].iloc[-2] < dmi_1h['adx'].iloc[-1] and dmi_1h['plus_di'].iloc[-2] < dmi_1h['minus_di'].iloc[-2] and dmi_1h['plus_di'].iloc[-1] > dmi_1h['minus_di'].iloc[-1]:
            buy_flag += 1
        if dmi_1h['adx'].iloc[-2] < dmi_1h['adx'].iloc[-1] and dmi_1h['plus_di'].iloc[-2] > dmi_1h['minus_di'].iloc[-2] and dmi_1h['plus_di'].iloc[-1] < dmi_1h['minus_di'].iloc[-1]:
            sell_flag += 1

    dmi = dmi.iloc[-15:]
    dmi_15m = dmi_15m.iloc[-15:]
    dmi_1h = dmi_1h.iloc[-15:]

    #売買フェーズ
    # trend相場の場合
    send_message_to_line('ongoing')
    if trend_flag >= 2:
        if 'btc' in position.keys():
            if sell_flag >= 3 and coincheck.ask_rate < df_15m['close'].iloc[-1]:
                send_message_to_line('sell')
                params = {
                        'order_type': 'market_sell',
                        'pair': 'btc_jpy',
                        'market_buy_amount': position['btc'] 
                }

                r = coincheck.order(params)
                send_message_to_line(r)

                send_message_to_line({'trend判定' :str(trend_flag),
                                     'sell':str(sell_flag),
                                     'buy':str(buy_flag)
                })
                
            else:
                send_message_to_line('active')
                send_message_to_line({'trend判定' :str(trend_flag),
                                        'sell':str(sell_flag),
                                        'buy':str(buy_flag)})
                
        if 'jpy' in position.keys():
            if float(coincheck.last) * 0.005 <= float(position.get('jpy')):
                if buy_flag >= 3:
                    send_message_to_line('buy')
                    market_buy_amount = coincheck.rate({'order_type': 'buy',
                                                        'pair': 'btc_jpy',
                                                        'amount': AMOUNT})
                    params = {
                            'order_type': 'market_buy',
                            'pair': 'btc_jpy',
                            'market_buy_amount': market_buy_amount['price'] 
                        }
                    r = coincheck.order(params)
                    send_message_to_line(r)

                    send_message_to_line({'trend判定' :str(trend_flag),
                                        'sell':str(sell_flag),
                                        'buy':str(buy_flag)
                                        })
                    
                else:
                    send_message_to_line('active')
                    send_message_to_line({'trend判定' :str(trend_flag),
                                            'sell':str(sell_flag),
                                            'buy':str(buy_flag)})
            else:
                send_message_to_line("can't buy!!") 
                send_message_to_line({'trend判定':str(trend_flag),
                            'sell':str(sell_flag),
                            'buy':str(buy_flag)})     

    # range相場の場合
    else:
        if 'btc' in position.keys():
            if sell_flag >= 2 and coincheck.ask_rate < df_1h['close'].iloc[-1]:
                send_message_to_line('sell')
                params = {
                        'order_type': 'market_sell',
                        'pair': 'btc_jpy',
                        'market_buy_amount': position['btc'] 
                }
                r = coincheck.order(params)
                send_message_to_line(r)
                
                send_message_to_line({'trend判定':str(trend_flag),
                                     'sell':str(sell_flag),
                                     'buy':str(buy_flag)
                                    })
                
            else:
                send_message_to_line('active')
                send_message_to_line({'trend判定':str(trend_flag),
                                        'sell':str(sell_flag),
                                        'buy':str(buy_flag)})
                # print("trend_flag", trend_flag)
                # print("buy_flag", buy_flag)
                # print("sell_flag", sell_flag)
                # print('='*10, '実行中', '='*10)
        if 'jpy' in position.keys():
            if float(coincheck.last) * 0.005 <= float(position.get('jpy')):
                if buy_flag >= 2:
                    send_message_to_line('buy')
                    market_buy_amount = coincheck.rate({'order_type': 'buy',
                                                        'pair': 'btc_jpy',
                                                        'amount': AMOUNT})
                    params = {
                            'order_type': 'market_buy',
                            'pair': 'btc_jpy',
                            'market_buy_amount': market_buy_amount['price'] 
                        }
                    r = coincheck.order(params)
                    send_message_to_line(r)

                    send_message_to_line({'trend判定':str(trend_flag),
                                        'sell':str(sell_flag),
                                        'buy':str(buy_flag)
                                        })
                    # print("trend_flag", trend_flag)
                    # print("buy_flag", buy_flag)
                    # print("sell_flag", sell_flag)
                    # print('='*10, 'buy', '='*10)
                else:
                    send_message_to_line('active')
                    send_message_to_line({'trend判定':str(trend_flag),
                                            'sell':str(sell_flag),
                                            'buy':str(buy_flag)})
                    # print("trend_flag", trend_flag)
                    # print("buy_flag", buy_flag)
                    # print("sell_flag", sell_flag)
                    # print('='*10, '実行中', '='*10)
            else:
                send_message_to_line("can't buy!!")
                send_message_to_line({'trend判定':str(trend_flag),
                            'sell':str(sell_flag),
                            'buy':str(buy_flag)})

    # #　購入フェーズ    
    # if buy_flag >= 1:
    #     send_message_to_line('buy')
    # elif sell_flag >= 1:
    #     send_message_to_line('sell')
    # else:
    #     send_message_to_line("verify")
    #     send_message_to_line(str(sell_flag))
    #     send_message_to_line(str(buy_flag))
    #     send_message_to_line(str(df['price'].iloc[-1]))
    # アルゴリズムの練度をあげたい
    #テストしたい　デモ的
    # print('='*10,"df",'='*10)
    # print('df',df)
    # print('df1hour',df_1h)
    # print('df15min',df_15m)
    # print('data', data)
    # print('data15min', data_15minutes)
    # print('data1hours', data_1hour)
    if trend_flag >= 2:
        df = df.iloc[1:,:]
    else:
        df = df.iloc[4:,:]
    
    
    # print('dmi_data', dmi) #trend判定
    # print('dmi_15min', dmi_15m)
    # print('dmi_1hour', dmi_1h)
    # print("="*10,'Boringer Band','='*10)
    # print('bb_15min', bb_15m)
    # print('bb_1hour', bb_1h) # trend判定も
    # print("="*10,'RSI','='*10)
    # print('rsi_data', rsi_data) #trend判定
    # print('rsi_15min', rsi_today_15m)
    # print('rsi_1hour', rsi_today_1h)
    # print("="*10,'STCK','='*10)
    # print('stck', stck) # ここで80 20 を超えないと作動しない
    # print('stck_1hour', stck_1h)
    # print("="*10,'MACD','='*10)
    # print('macd_15min', macd)
    # print('='*10,'fin','='*10)