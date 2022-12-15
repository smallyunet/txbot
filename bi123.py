import base64
import email
import imaplib
import datetime
from email.header import decode_header
import time

import config as cfg
import binance_client as bc
import telegram as tb
import db


def getStr(s):
    if type(s) is bytes:
        return s.decode('utf-8')
    else:
        return s


def get_mail(retry=0):
    try:
        tb.send_by_bot("Getting mail...")

        mail = imaplib.IMAP4_SSL(cfg.mail_server, cfg.mail_server_port)
        mail.login(cfg.mail_address, cfg.mail_password)
        mail.select('inbox')

        status, data = mail.search(None, cfg.mail_list_type)
        mail_ids = []
        for block in data:
            # b'1 2 3'.split() => [b'1', b'2', b'3']
            mail_ids += block.split()

        for i in mail_ids:
            status, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue

                message = email.message_from_bytes(response_part[1])

                mail_from, encoding = decode_header(message["From"])[0]
                mail_subject, encoding = decode_header(
                    message["Subject"])[0]
                mail_from = getStr(mail_from)
                mail_subject = getStr(mail_subject)

                body = ""
                if message.is_multipart():
                    for part in message.walk():
                        content_type = part.get_content_type()
                        if content_type != "text/html":
                            continue
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
                                getStr(part.get_payload(
                                    decode=True)) + '\n'
                else:
                    body = body + \
                        getStr(message.get_payload(decode=True)) + '\n'

                mail_content = body
                mail_content = mail_content.replace('<br/>', '\n')
                mail_content = mail_content.replace('<br>', '\n')
                mail_content = mail_content.replace('<br />', '\n')

                msg = f'From: {mail_from}\n'
                msg += f'Subject: {mail_subject}\n'
                msg += f'Content: {mail_content}\n'
                tb.send_by_bot(msg)

                for k, v in cfg.tokens.items():
                    if "看涨" in mail_content and k in mail_content:
                        bc.make_order('buy', k, v)
                    if "看跌" in mail_content and k in mail_content:
                        bc.make_order('sell', k)

        # get balance after order
        bc.get_total_balance()
        data = db.get_latest('balance', 7)
        tb.send_by_bot(data)

    except Exception as e:
        msg = f'Error: {e}\n'
        msg += f'[{retry}/3]\n'
        tb.send_by_bot(msg)

        if retry < 3:
            time.sleep(60)
            get_mail(retry + 1)
