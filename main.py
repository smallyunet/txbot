import sys
import os
import datetime

import telegram as tg
import config as cfg
import task as t
import bi123 as bm

if __name__ == '__main__':
    try:
        msg = tg.temp_started()
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
