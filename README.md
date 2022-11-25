## Transaction Bot

Get market signals from https://www.bi123.co and auto-make orders in Binance.

## Preparation

Add the config file in the project folder:

- Add a file named `config.py`

Receive signal mail from bi123:

- Register in bi123.co by mail
- Open mail push in bi123.co
- Setup mail server info in `config.py`

Make order automation in Binance:

- Register an account in Binance
- Get the API token in Binance and setup in `config.py`

Push action to telegram bot:

- Get a bot and get the control token and group chat id
- Setup in `config.py`

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
mail_list_type = '(UNSEEN)'

job_minute = False

telegram_enable = True
telegram_api_token = ''
telegram_chat_id = ''

binance_enable = True
biance_api_key = ''
biance_secrect_key = ''
```
