import sys
import os
import datetime
import schedule
import time
import datetime

import telegram as tb
import mail as ml


def task():
    schedule.every().hour.at(":03").do(ml.get_mail)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    try:
        tb.send_started_config
        tb.send_tokens_list()

        # run once at start
        ml.get_mail()

        # start schedule
        task()

    except KeyboardInterrupt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("I'm exiting...", now)
        tb.send_text("I'm exiting...")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
