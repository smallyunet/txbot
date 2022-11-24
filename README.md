## txbot

Get market signals from https://www.bi123.co and auto-make orders in Binance.

## Usage

Install:

```
pip install python-binance
pip install -r requirements.txt
```

Run:

```
python main.py
```

## Configuration

`config.py` format:

```
mail_address = ''
mail_password = ''
mail_server = ''
mail_server_port = 0

# 'ALL' or '(UNSEEN)'
mail_list_type = 'ALL'

job_minute = False

telegram_enable = True
telegram_api_token = ''
telegram_chat_id = ''

binance_enable = True
biance_api_key = ''
biance_secrect_key = ''
```
