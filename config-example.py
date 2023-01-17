mail_address = ''
mail_password = ''
mail_server = ''
mail_server_port = 0

# 'ALL' or '(UNSEEN)'
mail_list_type = '(UNSEEN)'
# 1H 4H 1D ALL
mail_level = 'ALL'
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
mail_address_verify = True
mail_address_from = b'<subscription@bi123.co>'
mail_to_tg = False

telegram_enable = True
telegram_api_token = ''
telegram_chat_id = ''

proxy_enable = False
proxy_http = 'socks5://127.0.0.1:7891'
proxy_https = 'socks5://127.0.0.1:7891'

binance_enable = True
biance_api_key = ''
biance_secrect_key = ''

# USDT
tokens = {
    "ETH": 11,
    "DOGE": 11,
    "SHIB": 11
}
token_remain_rate = 0.995
token_balance_decimal = 4
