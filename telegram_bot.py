import requests
import config as cfg


def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{cfg.telegram_api_token}/sendMessage'

    try:
        response = requests.post(
            apiURL, json={'chat_id': cfg.telegram_chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
