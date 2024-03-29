import base64
import email
import imaplib
import datetime
from email.header import decode_header
import time
import re
from bs4 import BeautifulSoup

import config as cfg
import order as bc
import telegram as tb
import db


def getStr(s):
    if type(s) is bytes:
        return s.decode('utf-8')
    else:
        return s


def get_mail():
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
                        continue

                msg = f'From: {mail_from}\n'
                msg += f'Subject: {mail_subject}\n'
                msg += f'Content: {mail_content}\n'
                if cfg.mail_to_tg:
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
                    continue

                for k, v in cfg.tokens.items():
                    # token in mail
                    kStr = b'\xe3\x80\x90\xe6\xa0\x87\xe7\x9a\x84\xe3\x80\x91'.decode(
                        'utf-8') + k + '/USDT'
                    if kStr in mail_content:
                        # singal in mail
                        for i in cfg.mail_rais_text:
                            if i.decode('utf-8') in mail_content:
                                bc.make_order('buy', k, v)
                        for i in cfg.mail_fall_text:
                            if i.decode('utf-8') in mail_content:
                                bc.make_order('sell', k)

    except Exception as e:
        msg = f'*Error: {e}*'
        tb.send_md(msg)
