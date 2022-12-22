import requests

import config as cfg


def send_by_bot(message):
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
