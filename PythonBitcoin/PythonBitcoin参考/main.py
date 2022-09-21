import configparser
import time

import pandas as pd

from coincheck import Coincheck
from utils.notify import send_message_to_line

conf = configparser.ConfigParser()
conf.read('config.ini')

ACCEES_KEY = conf['coincheck']['access_key']
SECRET_KEY = conf['coincheck']['secret_key']

coincheck = Coincheck(access_key=ACCEES_KEY, secret_key=SECRET_KEY)

interval = 60*60
duration = 20
AMOUNT = 0.005

df = pd.DataFrame()
send_message_to_line('Start Auto Trading...')

while True:
    time.sleep(interval)
    position = coincheck.position

    if not position.get('jpy'):
        send_message_to_line('My account balance is zero.')
        raise

    df = df.append({'price': coincheck.last}, ignore_index=True)

    if len(df) < duration:
        continue

    df['SMA'] = df['price'].rolling(window=duration).mean()
    df['std'] = df['price'].rolling(window=duration).std()

    df['-2σ'] = df['SMA'] - 2*df['std']
    df['+2σ'] = df['SMA'] + 2*df['std']

    if 'btc' in position.keys():
        if df['+2σ'].iloc[-1] < df['price'].iloc[-1] \
                and coincheck.ask_rate < df['price'].iloc[-1]:
            params = {
                'order_type': 'market_sell',
                'pair': 'btc_jpy',
                'market_buy_amount': position['btc']
            }
            r = coincheck.order(params)
            send_message_to_line(r)
    else:
        if df['price'].iloc[-1] < df['-2σ'].iloc[-1]:
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
    df = df.iloc[1:, :]
