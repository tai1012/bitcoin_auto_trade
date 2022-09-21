import datetime
import json 
import requests
import pandas as pd

data = pd.DataFrame()
def data_20d():
    ymd = datetime.date.today() - datetime.timedelta(days=21)
    year = str(ymd.year)
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/klines?symbol=BTC&interval=1day&date='+year
    r =  requests.get(endPoint + path)
    return json.dumps(r.json(), indent=2)

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
    ymd = datetime.date.today() - datetime.timedelta(days=1) - datetime.timedelta(hours=6)
    today = f'{ymd:%Y%m%d}'
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/klines?symbol=BTC&interval=1hour&date='+today
    r = requests.get(endPoint + path)
    return json.dumps(r.json(), indent=2)

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
    ymd = datetime.date.today() - datetime.timedelta(hours=6)
    today = f'{ymd:%Y%m%d}'
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/klines?symbol=BTC&interval=1hour&date='+today
    r = requests.get(endPoint + path)
    return json.dumps(r.json(), indent=2)
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
data_1hour = pd.DataFrame(list(zip(new_data_close,
                            new_data_high,
                            new_data_low)),
                    index=date, columns=['close', 'high', 'low'])
data_1hour = pd.concat([data_1hour_yesterday, data_1hour], axis=0)
def data_15ym():
    ymd = datetime.date.today() - datetime.timedelta(days=1) - datetime.timedelta(hours=6)
    today = f'{ymd:%Y%m%d}'
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/klines?symbol=BTC_JPY&interval=15min&date='+today
    r = requests.get(endPoint + path)
    return json.dumps(r.json(), indent=2)

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
    ymd = datetime.date.today() - datetime.timedelta(hours=6)
    today = f'{ymd:%Y%m%d}'
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/klines?symbol=BTC_JPY&interval=15min&date='+today
    r = requests.get(endPoint + path)
    return json.dumps(r.json(), indent=2)

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

data_15min = pd.DataFrame(list(zip(new_data_close,
                             new_data_high,
                             new_data_low)),
                    index=date_15m, columns=['close', 'high', 'low'])
data_15minutes = pd.concat([data_15min_yesterday, data_15min], axis=0)
data = data.iloc[-20:]
data_1hour = data_1hour.iloc[-20:]
data_15minutes = data_15minutes.iloc[-20:]

