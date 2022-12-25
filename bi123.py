import base64
import email
import imaplib
import datetime
from email.header import decode_header
import time
import re
from bs4 import BeautifulSoup

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
        tb.send_text('Start get mail...')

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
                mail_subject, encoding = decode_header(message["Subject"])[0]
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
                # remove a tag
                mail_content = BeautifulSoup(mail_content, "lxml").text

                # filter not match level signal
                if not cfg.mail_level == 'ALL':
                    if not cfg.mail_level in mail_content:
                        tb.send_text('Not match level signal, skip.')
                        continue

                msg = f'From: {mail_from}\n'
                msg += f'Subject: {mail_subject}\n'
                msg += f'Content: {mail_content}\n'
                tb.send_text(msg)

                # verifiy mail address
                wrong_address = False
                if cfg.mail_address_verify:
                    header_from = decode_header(message["From"])
                    if header_from.__len__() > 1:
                        from_address, encoding = header_from[1]
                        if from_address.strip() != cfg.mail_address_from:
                            wrong_address = True
                    else:
                        wrong_address = True

                if wrong_address:
                    msg = f'Get a wrong email from address: {from_address}\n'
                    tb.send_text(msg)
                    continue

                for k, v in cfg.tokens.items():
                    # token in mail
                    if k in mail_content:
                        # singal in mail
                        for i in cfg.mail_rais_text:
                            if i.decode('utf-8') in mail_content:
                                bc.make_order('buy', k, v)
                        for i in cfg.mail_fall_text:
                            if i.decode('utf-8') in mail_content:
                                bc.make_order('sell', k)

        # get balance after order
        bc.get_total_balance()
        data = db.get_latest('balance', 7)
        msg = f'Balance history:\n'
        for k, v in data.items():
            msg += f'{k}: {v}\n'
        tb.send_text(msg)

    except Exception as e:
        msg = f'*Error: {e}*\n'
        msg += f'Retry: [{retry}/3]'
        tb.send_md(msg)

        if retry < 3:
            time.sleep(60)
            get_mail(retry + 1)
