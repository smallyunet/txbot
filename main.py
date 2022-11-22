import sys
import os
import datetime

import telegram as tg
import task as t

if __name__ == '__main__':
    try:
        t.job()
    except KeyboardInterrupt:
        print("I'm exiting...", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tg.send_by_bot("I'm exiting...")    
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
