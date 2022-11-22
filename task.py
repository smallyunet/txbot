import schedule
import time
import datetime

import telegram as tg
import bi123 as bm


def job():
    print("I'm working...", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tg.send_by_bot("I'm working...")

    schedule.every().hour.at(":03").do(bm.get_mail)

    while True:
        schedule.run_pending()
        time.sleep(1)
