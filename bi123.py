import email
import imaplib
import datetime

import config as cfg
import binance_client as bc
import telegram as tb


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

                tb.send_by_bot(
                    f'From: {mail_from}\nSubject: {mail_subject}\nContent: {mail_content}')

                if mail_content.includs('看涨'):
                    bc.make_order('buy')
                if mail_content.includs('看跌'):
                    bc.make_order('sell')
