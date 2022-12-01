import json
from binance.spot import Spot
from binance.client import Client
import datetime

import config as cfg
import telegram as tg


def getBalance(spot, symbol, msgPrefix):
    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    usdt_balance = float([x['free']
                          for x in balances if x['asset'] == 'USDT'][0])
    msg = f'{msgPrefix}\n'
    msg += f'{symbol} balance: {symbol_balance}\n'
    msg += f'USDT balance: {usdt_balance}\n'
    tg.send_by_bot(msg)
    return symbol_balance, usdt_balance


def make_order(type, symbol, quoteOrderQty=0):
    if not cfg.binance_enable:
        return

    msg = f'[Make order]\n'
    msg += f'type: {type}\n'
    msg += f'symbol: {symbol}\n'
    msg += f'quoteOrderQty: {quoteOrderQty}\n'
    tg.send_by_bot(msg)

    try:
        spot = None
        client = None

        if not cfg.proxy_enable:
            spot = Spot()
            spot = Spot(key=cfg.biance_api_key, secret=cfg.biance_secrect_key)
            client = Client(cfg.biance_api_key, cfg.biance_secrect_key)
        else: 
            proxies = {
                'http': 'socks5://127.0.0.1:7891',
                'https': 'socks5://127.0.0.1:7891'
            }
            spot = Spot()
            spot = Spot(key=cfg.biance_api_key, secret=cfg.biance_secrect_key, proxies=proxies)
            client = Client(cfg.biance_api_key, cfg.biance_secrect_key, proxies=proxies)

        status = client.get_account_status()
        msg = f'[Account status]\n'
        msg += f'status: {status}\n'
        tg.send_by_bot(msg)

        symbol_balance, usdt_balance = getBalance(
            spot, symbol, '[Before ordered]')

        symbolUSDT = symbol + 'USDT'
        if type == "buy":
            params = {
                'symbol': symbolUSDT,
                'side': 'BUY',
                'type': 'MARKET',
                'quoteOrderQty': quoteOrderQty,
            }
        if type == "sell":
            price = client.get_avg_price(symbol=symbolUSDT)
            params = {
                'symbol': symbolUSDT,
                'side': 'SELL',
                'type': 'MARKET',
                'quoteOrderQty': "{:.2f}".format(symbol_balance * float(price['price']) * cfg.token_remain_rate),
            }

        response = ""
        try:
            response = spot.new_order(**params)
            tg.send_by_bot(json.dumps(response, indent=2))
        except Exception as e:
            response = e.__str__()
            tg.send_by_bot(response)

        symbol_balance, usdt_balance = getBalance(
            spot, symbol, '[After ordered]')

    except Exception as e:
        tg.send_by_bot(f'[In Binance Client Error]\n{e.__str__()}')
