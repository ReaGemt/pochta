import os
import time


def generate_daily_report(file_path):
    today = time.strftime("%Y-%m-%d")
    report_content = f"Ежедневный отчет за {today}"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(report_content)