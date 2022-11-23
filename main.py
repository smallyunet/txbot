import sys
import os
import datetime

import telegram as tg
import config as cfg
import task as t

if __name__ == '__main__':
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        msg = f'Mail list type: {cfg.mail_list_type}, Telegram bot enabled: {cfg.telegram_enable}, Binance enabled: {cfg.binance_enable}'
        print(f'Start at {now}, {msg}')
        tg.send_by_bot(msg)

        t.job()

    except KeyboardInterrupt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("I'm exiting...", now)
        tg.send_by_bot("I'm exiting...")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
