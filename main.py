import sys
import os
import datetime

import telegram as tg
import config as cfg
import task as t
import bi123 as bm

if __name__ == '__main__':
    try:

        msg = f'[Started]\n'
        msg += f'Mail list type: {cfg.mail_list_type}\n'
        msg += f'Binance enabled: {cfg.binance_enable}\n'
        msg += f'Telegram bot enabled: {cfg.telegram_enable}\n'
        msg += f'Proxy enabled: {cfg.proxy_enable}\n'
        msg += f'Signal level: {cfg.mail_level}\n'
        msg += f'Verify mail address: {cfg.mail_address_verify}\n'
        msg += '[Tokens]\n'
        for token in cfg.tokens:
            msg += f'{token}: {cfg.tokens[token]}\n'

        print(msg)
        tg.send_by_bot(msg)

        # run once at start
        bm.get_mail()
        
        # start schedule
        t.job()

    except KeyboardInterrupt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("I'm exiting...", now)
        tg.send_by_bot("I'm exiting...")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
