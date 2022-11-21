
import schedule
import time
import datetime


import bi_mail as bm

schedule.every().hour.at(":03").do(bm.get_mail)
print("Started at " + str(datetime.datetime.now()))

while True:
    schedule.run_pending()
    time.sleep(1)
