import os
import time
import imaplib
import smtplib
import logging
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

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
smtp_server = "smtp.yandex.ru"             # Адрес SMTP сервера
smtp_port = 587                            # Порт SMTP сервера для TLS
imap_server = "imap.yandex.ru"             # Адрес IMAP сервера
imap_port = 993                            # Порт IMAP сервера для SSL
to_mails = config.to_mails                 # Список адресов получателей

# Путь к вложению
attachment_path = config.attachment_path

# Функция для отправки письма
def send_email(to_mail):
    msg = MIMEMultipart()
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Subject"] = Header('Тема письма', 'utf-8')
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText("Текст сообщения", 'html', 'utf-8'))

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
            msg.attach(part)
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
