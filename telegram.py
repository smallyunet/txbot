import requests

import config as cfg


def send_text(message):
    print(f'Send telegram message: {message}')
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
    print(f'Send telegram message: {message}')
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

def temp_started():
    return f'''```
[Started]
Mail list type:       {cfg.mail_list_type}
Binance enabled:      {cfg.binance_enable}
Telegram bot enabled: {cfg.telegram_enable}
Proxy enabled:        {cfg.proxy_enable}
Signal level:         {cfg.mail_level}
Verify mail address:  {cfg.mail_address_verify}
```'''

def temp_make_order(type, symbol, qty):
    return f'''```
[Make order]
Type:          {type}
Symbol:        {symbol}
QuoteOrderQty: {qty}
```'''


def temp_order_end(symbol, qty, result, msg):
    return f'''```
[Order End]
Toekn:   {symbol}
Qty:     {qty}
Result:  {result}
Message: {msg}
```'''
