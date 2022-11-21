import email
import imaplib

import schedule
import time
import datetime

import config as cfg
import telegram_bot as tb


def getMail():
    print("---- running at " + str(datetime.datetime.now()) + " ----")

    mail = imaplib.IMAP4_SSL(cfg.SERVER, cfg.PORT)
    mail.login(cfg.EMAIL, cfg.PASSWORD)
    mail.select('inbox')

    all = 'ALL'
    unseen = '(UNSEEN)'
    status, data = mail.search(None, unseen)
    mail_ids = []
    for block in data:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')

                tb.send_to_telegram(
                    f'From: {mail_from}\nSubject: {mail_subject}\nContent: {mail_content}')


schedule.every().hour.at(":03").do(getMail)
print("Started at " + str(datetime.datetime.now()))

while True:
    schedule.run_pending()
    time.sleep(1)
