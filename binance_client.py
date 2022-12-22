import json
from binance.spot import Spot
from binance.client import Client
import datetime

import config as cfg
import telegram as tg
import db


def get_balance(client, spot, symbol):
    balances = spot.account()['balances']
    symbol_balance = float([x['free']
                            for x in balances if x['asset'] == symbol][0])
    symbol_usdt_balance = 0
    if symbol == 'USDT':
        symbol_usdt_balance = symbol_balance
    else:
        symbolUSDT = symbol + 'USDT'
        price = client.get_avg_price(symbol=symbolUSDT)
        symbol_usdt_balance = symbol_balance * float(price['price'])
    return symbol_balance, symbol_usdt_balance


def get_total_balance():
    msg = f'[All balance]\n'
    spot, client = get_client()
    balance, ubalance = get_balance(client, spot, 'USDT')
    msg += f'USDT: {"{:.2f}".format(ubalance)}\n'
    total = ubalance
    for k, v in cfg.tokens.items():
        balance, ubalance = get_balance(client, spot, k)
        msg += f'{k}: {"{:.2f}".format(ubalance)}\n'
        total += ubalance
    total = "{:.2f}".format(total)
    msg += f'Total: {total}\n'
    tg.send_by_bot(msg)
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
    msg = f'[Account status]\n'
    msg += f'status: {status}\n'
    tg.send_by_bot(msg)


def make_order(type, symbol, qty=0):
    if not cfg.binance_enable:
        return

    msg = f'[Make order]\n'
    msg += f'type: {type}\n'
    msg += f'symbol: {symbol}\n'
    msg += f'quoteOrderQty: {qty}\n'
    tg.send_by_bot(msg)

    try:
        spot, client = get_client()

        get_account_status(client)
        symbol_balance, u = get_balance(client, spot, symbol)

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
            params['recvWindow'] = 59999
            response = spot.new_order(**params)
            tg.send_by_bot(json.dumps(response, indent=2))
        except Exception as e:
            response = e.__str__()
            tg.send_by_bot(response)

    except Exception as e:
        tg.send_by_bot(f'[In Binance Client Error]\n{e.__str__()}')
