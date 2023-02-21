import sys
import os
import datetime
import schedule
import time
import datetime

import telegram as tb
import mail as ml
import order as bc
import db


def job():
    ml.get_mail()
    bc.get_total_balance()
    tb.send_balance_history()


if __name__ == '__main__':
    try:
        tb.send_started_config()
        tb.send_tokens_list()

        # run once at start
        job()
        schedule.every().hour.at(":01").do(job)
        schedule.every().hour.at(":03").do(job)
        schedule.every().hour.at(":05").do(job)
        schedule.every().hour.at(":07").do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("I'm exiting...", now)
        tb.send_text("I'm exiting...")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
