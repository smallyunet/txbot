import sys
import os
import datetime

import telegram as tg
import config as cfg
import task as t
import bi123 as bm

if __name__ == '__main__':
    try:
        msg = f'''```
[Started]
Mail list type:       {cfg.mail_list_type}
Binance enabled:      {cfg.binance_enable}
Telegram bot enabled: {cfg.telegram_enable}
Proxy enabled:        {cfg.proxy_enable}
Signal level:         {cfg.mail_level}
Verify mail address:  {cfg.mail_address_verify}
```'''
        tg.send_md(msg)

        msg = '''```
[Tokens]\n'''
        for token in cfg.tokens:
            msg += "{0: <7}".format(token + ": ") + \
                str(cfg.tokens[token]) + "\n"
        msg += '```'
        tg.send_md(msg)

        # run once at start
        bm.get_mail()

        # start schedule
        t.job()

    except KeyboardInterrupt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("I'm exiting...", now)
        tg.send_text("I'm exiting...")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
