# Путь к вложению (отчету)
attachment_path = 'daily_report.txt'       # Имя файла для ежедневного отчета

# Функция для создания ежедневного отчета
def generate_daily_report():
    today = time.strftime("%Y-%m-%d")
    report_content = f"Ежедневный отчет за {today}"
    with open(attachment_path, 'w', encoding='utf-8') as file:
        file.write(report_content)