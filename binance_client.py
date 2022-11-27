import json
from binance.spot import Spot
from binance.client import Client

import config as cfg
import telegram as tg


def make_order(type, symbol, quoteOrderQty=0):
    if not cfg.binance_enable:
        return

    msg = f'Make order: type: {type}, symbol: {symbol}, quoteOrderQty: {quoteOrderQty}\n'
    tg.send_by_bot(msg)

    spot = Spot()
    spot = Spot(key=cfg.biance_api_key, secret=cfg.biance_secrect_key)
    client = Client(cfg.biance_api_key, cfg.biance_secrect_key)

    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    usdt_balance = float([x['free']
                         for x in balances if x['asset'] == 'USDT'][0])
    msg = f'Before ordered: {symbol} balance: {symbol_balance}, USDT balance: {usdt_balance}\n'
    tg.send_by_bot(msg)

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
            'quoteOrderQty': "{:.2f}".format(symbol_balance * float(price['price']) * 0.99),
        }

    response = ""
    try:
        response = spot.new_order(**params)
    except Exception as e:
        response = e.__str__()
    tg.send_by_bot(json.dumps(response, indent=2))

    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    usdt_balance = float([x['free']
                         for x in balances if x['asset'] == 'USDT'][0])
    msg = f'After ordered: {symbol} balance: {symbol_balance}, USDT balance: {usdt_balance}\n'
    tg.send_by_bot(msg)
