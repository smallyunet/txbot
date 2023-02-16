import json
from binance.spot import Spot
from binance.client import Client
import datetime
import collections

import config as cfg
import telegram as tb
import db


def get_balance(client, spot, symbol):
    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    usdt_balance = float([x['free']
                          for x in balances if x['asset'] == 'USDT'][0])
    symbol_usdt_balance = 0
    if symbol == 'USDT':
        symbol_usdt_balance = symbol_balance
    else:
        symbolUSDT = symbol + 'USDT'
        price = client.get_avg_price(symbol=symbolUSDT)
        symbol_usdt_balance = symbol_balance * float(price['price'])
    return symbol_balance, symbol_usdt_balance, usdt_balance


def format(b):
    return "{:.{d}f}".format(b, d=cfg.token_balance_decimal)


def get_total_balance():
    msg = f'''```
[All balance]
'''
    spot, client = get_client()
    _, su, _ = get_balance(client, spot, 'USDT')
    msg += f'USDT:  {format(su)}\n'
    total = su
    tokens = collections.OrderedDict(sorted(cfg.tokens.items()))
    for k, v in tokens.items():
        _, su, _ = get_balance(client, spot, k)
        msg += '{0: <7}'.format(k + ': ') + \
            '{0: >9}'.format(str(format(su))) + "\n"
        total += su
    total = format(total)
    msg += f'Total: {total}\n'
    msg += '```'
    tb.send_md(msg)
    db.insert('balance', datetime.datetime.now().strftime('%Y-%m-%d'), total)


def get_client():
    spot = None
    client = None

    if not cfg.proxy_enable:
        spot = Spot()
        spot = Spot(key=cfg.biance_api_key, secret=cfg.biance_secrect_key)
        client = Client(cfg.biance_api_key, cfg.biance_secrect_key)
    else:
        proxies = {
            'http': cfg.proxy_http,
            'https': cfg.proxy_https
        }
        spot = Spot()
        spot = Spot(key=cfg.biance_api_key,
                    secret=cfg.biance_secrect_key, proxies=proxies)
        client = Client(cfg.biance_api_key, cfg.biance_secrect_key,
                        requests_params={'proxies': proxies})
    return spot, client


def get_account_status(client):
    status = client.get_account_status()
    return status['data']


def make_order(type, symbol, qty=-1):
    if not cfg.binance_enable:
        return
    qtyStr = "{:.4f}".format(qty)

    tb.send_make_order(type, symbol, qtyStr)

    try:
        spot, client = get_client()
        symbol_balance, _, usdt_balance = get_balance(client, spot, symbol)
        symbolUSDT = symbol + 'USDT'
        if type == "buy":
            if qty > usdt_balance:
                tb.send_order_end(symbol, qtyStr, 'Fail', "Not enough USDT")
                return
            params = {
                'symbol': symbolUSDT,
                'side': 'BUY',
                'type': 'MARKET',
                'quoteOrderQty': qty,
            }
        if type == "sell":
            price = client.get_avg_price(symbol=symbolUSDT)
            qty = symbol_balance * \
                float(price['price']) * cfg.token_remain_rate
            qtyStr = "{:.4f}".format(qty)
            # params limit
            if qty < 10:
                tb.send_order_end(symbol, qtyStr, 'Fail', "No need to sell")
                return
            params = {
                'symbol': symbolUSDT,
                'side': 'SELL',
                'type': 'MARKET',
                'quoteOrderQty': qtyStr,
            }
        try:
            params['recvWindow'] = 59999
            response = spot.new_order(**params)
            res = json.dumps(response, indent=2)
            tb.send_order_end(symbol, qtyStr, 'Success', res)
        except Exception as e:
            res = e.__str__()
            tb.send_order_end(symbol, qtyStr, 'Fail', res)

    except Exception as e:
        tb.send_text(f'[In Binance Client Error]\n{e.__str__()}')
