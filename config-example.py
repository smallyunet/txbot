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

