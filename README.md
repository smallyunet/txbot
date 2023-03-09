## Transaction Bot

Get market signals from https://www.bi123.co and auto-make orders in Binance.

You can read more about it in [My Cryptocurrency Trading Bot](https://smallyu-net.translate.goog/2022/12/03/%E6%88%91%E7%9A%84%E5%8A%A0%E5%AF%86%E8%B4%A7%E5%B8%81%E4%BA%A4%E6%98%93%E6%9C%BA%E5%99%A8%E4%BA%BA/?_x_tr_sch=http&_x_tr_sl=auto&_x_tr_tl=zh-CN&_x_tr_hl=en&_x_tr_pto=wapp).

## Preparation

Add the config file in the project folder:

- Add a file named `config.py` or execute the command `cp config-example.py config.py`

Receive signal mail from bi123:

- Register in bi123.co by mail
- Select your favorite coin and subscribe to the email notification in bi123.io.
- Setup mail server info in `config.py`

Make order automation in Binance:

- Register an account in Binance
- Get the API token in Binance and setup in `config.py`

Push action to telegram bot:

- Get a bot and get the control token and group chat id
- Setup in `config.py`

You can turn on or off functions in `config.py`, such as if you don't need Telegram Bot notification, you can set `telegram enable = False`.

## Usage

Install:

```
pip install -r requirements.txt
pip install python-binance
pip install lxml
```

Run:

```
python main.py
```

## Configuration

`config.py` format:

```
mail_address = ''
mail_password = '!'
mail_server = ''
mail_server_port = 80

# 'ALL' or '(UNSEEN)'
mail_list_type = '(UNSEEN)'

mail_address_verify = True
mail_address_from = b'<subscription@bi123.co>'
# 1H 4H 1D
mail_level = '4H'
mail_rais_text = [
    b'\xe7\x9c\x8b\xe6\xb6\xa8',
    b'RSI\xe5\xba\x95\xe8\x83\x8c\xe7\xa6\xbb',
    b'\xe4\xb8\x8a\xe7\xa9\xbfMA5',
    b'\xe5\xa4\x9a\xe5\xa4\xb4\xe6\x8e\x92\xe5\x88\x97',
]
mail_fall_text = [
    b'\xe7\x9c\x8b\xe8\xb7\x8c',
    b'RSI\xe9\xa1\xb6\xe8\x83\x8c\xe7\xa6\xbb',
    b'\xe4\xb8\x8b\xe7\xa9\xbfMA5',
    b'\xe7\xa9\xba\xe5\xa4\xb4\xe6\x8e\x92\xe5\x88\x97',
]
mail_to_tg = True

binance_enable = True
biance_api_key = ''
biance_secrect_key = ''

tokens = {
    "BTC": 200,
    "ETH": 200,
    "DOGE": 200,
    "SHIB": 200
}
token_remain_rate = 0.995
token_balance_decimal = 4
token_balance_history = True

telegram_enable = True
telegram_api_token = ''
telegram_chat_id = '-1'

proxy_enable = False
proxy_http = 'socks5://127.0.0.1:7891'
proxy_https = 'socks5://127.0.0.1:7891'
```

## Preview

<img src="./README.jpg" width="50%">
