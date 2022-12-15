import schedule
import time
import datetime

import telegram as tg
import config as cfg
import bi123 as bm


def job():
    schedule.every().hour.at(":03").do(bm.get_mail)

    while True:
        schedule.run_pending()
        time.sleep(1)
