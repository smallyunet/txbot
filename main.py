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
        i = 0
        for token in cfg.tokens:
            if i % 2 == 0:
                msg += "{0: <8}".format(token + ": ") + \
                    "{0: <5}".format(str(cfg.tokens[token])) + " | "
            else:
                msg += "{0: <8}".format(token + ": ") + \
                    "{0: <5}".format(str(cfg.tokens[token])) + "\n"
            i += 1
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
