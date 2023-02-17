import requests
import collections

import config as cfg
import db


def send_text(message):
    print(f'[text] Send telegram message: {message}')
    if not cfg.telegram_enable:
        return

    url = f'https://api.telegram.org/bot{cfg.telegram_api_token}/sendMessage'
    try:
        response = requests.post(
            url, json={
                'chat_id': cfg.telegram_chat_id,
                'caption': 'Catch exception',
                'text': message
            }
        )
    except Exception as e:
        print(e)


def send_md(message):
    print(f'[md] Send telegram message: {message}')
    if not cfg.telegram_enable:
        return

    url = f'https://api.telegram.org/bot{cfg.telegram_api_token}/sendMessage'
    try:
        response = requests.post(
            url, json={
                'chat_id': cfg.telegram_chat_id,
                'caption': 'Catch exception',
                'text': message,
                'parse_mode': 'MarkdownV2'
            }
        )
    except Exception as e:
        print(e)


def send_started_config():
    msg = f'''```
[Started]
Mail List Type:       {cfg.mail_list_type}
Signal Level:         {cfg.mail_level}
Binance Enabled:      {cfg.binance_enable}
Telegram Bot Enabled: {cfg.telegram_enable}
Proxy Enabled:        {cfg.proxy_enable}
Verify Mail Address:  {cfg.mail_address_verify}
Toekns Count:         {len(cfg.tokens)}
```'''
    send_md(msg)


def send_make_order(type, symbol, qty):
    if qty == '-1.0000':
        qty = 'All'
    msg = f'''```
[Make order]
Type:          {type}
Symbol:        {symbol}
QuoteOrderQty: {qty}
```'''
    send_md(msg)


def send_order_end(symbol, qty, result, msg):
    msg = f'''```
[Order End]
Toekn:   {symbol}
Qty:     {qty}
Result:  {result}
Message: {msg}
```'''
    send_md(msg)


def send_tokens_list():
    msg = '''```
[Tokens]\n'''
    i = 0
    tokens = collections.OrderedDict(sorted(cfg.tokens.items()))
    for token in tokens:
        if i % 2 == 0:
            msg += "{0: <7}".format(token + ": ") + \
                "{0: <4}".format(str(cfg.tokens[token])) + " "
        else:
            msg += "{0: <7}".format(token + ": ") + \
                "{0: <4}".format(str(cfg.tokens[token])) + "\n"
        i += 1
    msg += '```'
    send_md(msg)


def send_balance_history():
    data = db.get_latest('balance', 7)
    msg = f'Balance history:\n'
    for k, v in data.items():
        msg += f'{k}: {v}\n'
    send_text(msg)
