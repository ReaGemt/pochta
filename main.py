import os
import time
import imaplib
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

import body

import config

# Настройка логирования
logging.basicConfig(
    filename='email_log.log',  # имя файла для логов
    level=logging.DEBUG,       # уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',  # формат логирования
    datefmt='%Y-%m-%d %H:%M:%S'  # формат даты и времени
)

from_mail = config.mail                    # Адрес отправителя
from_passwd = config.passwd                # Пароль от почты отправителя
smtp_server = config.smtp_server           # Адрес SMTP сервера
smtp_port = config.smtp_port                         # Порт SMTP сервера для TLS
imap_server = config.imap_server            # Адрес IMAP сервера
imap_port = config.imap_port                            # Порт IMAP сервера для SSL
to_mails = config.to_mails                 # Список адресов получателей

# Путь к вложению
attachment_path = config.attachment_path

# Функция для отправки письма
def send_email(to_mail):
    msg = MIMEMultipart()
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Subject"] = config.Header
    msg["Date"] = formatdate(localtime=True)
    msg.attach = body

    # Логируем создание сообщения
    logging.info('Создано сообщение с темой: %s для %s', msg["Subject"], to_mail)

    # Проверяем, нужно ли прикрепить файл
    if attachment_path and os.path.isfile(attachment_path):
        part = MIMEBase('application', "octet-stream")
        try:
            with open(attachment_path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part) == body
            logging.info('Файл %s успешно прикреплен к сообщению для %s', attachment_path, to_mail)
        except Exception as e:
            logging.error('Ошибка при прикреплении файла к сообщению для %s: %s', to_mail, str(e))
    else:
        logging.info('Вложение не добавлено к сообщению для %s, так как файл %s не найден или путь не указан', to_mail, attachment_path)

    # Отправка письма
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_mail, from_passwd)
        smtp.sendmail(from_mail, to_mail, msg.as_string())  # Отправляем сообщение текущему получателю
        smtp.quit()
        logging.info('Сообщение успешно отправлено на %s', to_mail)
    except Exception as e:
        logging.error('Ошибка при отправке сообщения на %s: %s', to_mail, str(e))

    # Сохранение отправленного сообщения в папку "Sent"
    try:
        imap = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap.login(from_mail, from_passwd)
        imap.select('Sent')
        imap.append('Sent', None, imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        imap.close()
        imap.logout()
        logging.info('Сообщение успешно сохранено в папку "Sent" для %s', to_mail)
    except Exception as e:
        logging.error('Ошибка при сохранении сообщения в папку "Sent" для %s: %s', to_mail, str(e))

# Отправка писем всем получателям
for to_mail in to_mails:
    send_email(to_mail)
