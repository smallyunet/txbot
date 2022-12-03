import json
from binance.spot import Spot
from binance.client import Client
import datetime

import config as cfg
import telegram as tg


def getBalance(spot, symbol):
    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    usdt_balance = float([x['free']
                          for x in balances if x['asset'] == 'USDT'][0])
    return symbol_balance, usdt_balance


def make_order(type, symbol, qty=0):
    if not cfg.binance_enable:
        return

    msg = f'[Make order]\n'
    msg += f'type: {type}\n'
    msg += f'symbol: {symbol}\n'
    msg += f'quoteOrderQty: {qty}\n'
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
                'http': cfg.proxy_http,
                'https': cfg.proxy_https
            }
            spot = Spot()
            spot = Spot(key=cfg.biance_api_key,
                        secret=cfg.biance_secrect_key, proxies=proxies)
            client = Client(cfg.biance_api_key, cfg.biance_secrect_key,
                            requests_params={'proxies': proxies})

        status = client.get_account_status()
        msg = f'[Account status]\n'
        msg += f'status: {status}\n'
        tg.send_by_bot(msg)

        symbol_balance, usdt_balance = getBalance(spot, symbol)

        symbolUSDT = symbol + 'USDT'
        if type == "buy":
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
            qtyStr = "{:.2f}".format(qty)
            # params limit
            if qty < 10:
                msg = f'[Order End]\n'
                msg += f'qty: {qtyStr}\n'
                msg += f'no need to sell\n'
                tg.send_by_bot(msg)
                return
            params = {
                'symbol': symbolUSDT,
                'side': 'SELL',
                'type': 'MARKET',
                'quoteOrderQty': qtyStr,
            }

        try:
            response = spot.new_order(**params)
            tg.send_by_bot(json.dumps(response, indent=2))
        except Exception as e:
            response = e.__str__()
            tg.send_by_bot(response)

        symbol_balance, usdt_balance = getBalance(spot, symbol)

    except Exception as e:
        tg.send_by_bot(f'[In Binance Client Error]\n{e.__str__()}')
