import math
from binance.spot import Spot
from binance.client import Client

import config as cfg
import telegram_bot as tb

def make_order(type):
    spot = Spot()
    spot = Spot(key=cfg.biance_api_key, secret=cfg.biance_secrect_key)

    client = Client(cfg.biance_api_key, cfg.biance_secrect_key)

    balances = spot.account()['balances']
    eth_balance = float([x['free']
                        for x in balances if x['asset'] == 'ETH'][0])
    usdt_balance = float([x['free']
                         for x in balances if x['asset'] == 'USDT'][0])

    print(eth_balance, usdt_balance)

    if type == "buy":
        params = {
            'symbol': 'ETHUSDT',
            'side': 'BUY',
            'type': 'MARKET',
            'quoteOrderQty': usdt_balance,
        }

    if type == "sell":
        price = client.get_avg_price(symbol='ETHUSDT')
        params = {
            'symbol': 'ETHUSDT',
            'side': 'SELL',
            'type': 'MARKET',
            'quoteOrderQty': "{:.2f}".format(eth_balance * float(price['price'])),
        }

    response = spot.new_order(**params)
    print(response)
    
    tb.send_to_telegram(response)
