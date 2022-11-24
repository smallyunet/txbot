import sys
import os
import datetime

import telegram as tg
import config as cfg
import task as t

if __name__ == '__main__':
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        msg = f'Start at {now}\nMail list type: {cfg.mail_list_type}\nTelegram bot enabled: {cfg.telegram_enable}\nBinance enabled: {cfg.binance_enable}\n'
        print(msg)
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
