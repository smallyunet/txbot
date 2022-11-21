import requests
import config as cfg


def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{cfg.apiToken}/sendMessage'

    try:
        response = requests.post(
            apiURL, json={'chat_id': cfg.chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
