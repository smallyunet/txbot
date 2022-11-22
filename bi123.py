import base64
import email
import imaplib
import datetime
from email.header import decode_header

import config as cfg
import binance_client as bc
import telegram as tb


def getStr(s):
    if type(s) is bytes:
        return s.decode('utf-8')
    else:
        return s


def get_mail():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Getting mail...", now)
    tb.send_by_bot("Getting mail...")

    mail = imaplib.IMAP4_SSL(cfg.mail_server, cfg.mail_server_port)
    mail.login(cfg.mail_address, cfg.mail_password)
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

                mail_from, encoding = decode_header(message["From"])[0]
                mail_subject, encoding = decode_header(message["Subject"])[0]
                mail_from = getStr(mail_from)
                mail_subject = getStr(mail_subject)

                body = ""
                if message.is_multipart():
                    for part in message.walk():
                        if part.is_multipart():
                            for subpart in part.get_payload():
                                if subpart.is_multipart():
                                    for subsubpart in subpart.get_payload():
                                        body = body + \
                                            getStr(subsubpart.get_payload(
                                                decode=True)) + '\n'
                                else:
                                    body = body + \
                                        getStr(subpart.get_payload(
                                            decode=True)) + '\n'
                        else:
                            body = body + \
                                getStr(part.get_payload(decode=True)) + '\n'
                else:
                    body = body + \
                        getStr(message.get_payload(decode=True)) + '\n'

                mail_content = body

                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')

                tb.send_by_bot(
                    f'From: {mail_from}\nSubject: {mail_subject}\nContent: {mail_content}')

                if "看涨" in mail_content:
                    bc.make_order('buy')
                if "看跌" in mail_content:
                    bc.make_order('sell')
