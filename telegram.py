import requests
import config as cfg


def send_by_bot(message):

    url = f'https://api.telegram.org/bot{cfg.telegram_api_token}/sendMessage'

    try:
        response = requests.post(
            url, json={'chat_id': cfg.telegram_chat_id, 'text': message})
    except Exception as e:
        print(e)
