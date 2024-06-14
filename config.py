from email.mime.text import MIMEText

mail = "ivan@mail.ru"       # Адрес отправителя
passwd = "1edQ34dzq"        # Пароль от почты отправителя
to_mails = ["sidorov@ya.ru", "liea@list.ru", "viktor@rambler.ru", "sasha@list.ru"]  # Список адресов получателей
attachment_path = r"C:\cachemem.png"  # Путь к вложению файла в письмо (не обязательно) если файл по указаному пути не найден функция будет проигнорирована
Header = ('Тема письма', 'utf-8') #Указываем тему письма. Кодировку utf-8 не трогаем для корректного отображения текста
Body = (MIMEText("Текст сообщения", 'html', 'utf-8')) #Указываем текст письма. Кодировку utf-8 не трогаем для корректного отображения текста
smtp_server = "smtp.yandex.ru"             # Адрес SMTP сервера (не забудьте изменить на свой)
smtp_port = 587                            # Порт SMTP сервера для TLS (не забудьте изменить на свой)
imap_server = "imap.yandex.ru"             # Адрес IMAP сервера (не забудьте изменить на свой)
imap_port = 993                            # Порт IMAP сервера для SSL (не забудьте изменить на свой)
