import csv
from datetime import datetime, timedelta
import requests
import os


class ExchangeRateScraper:
    """Класс для сбора данных о курсе валют с сайта ЦБ РФ"""

    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_inr_rate(self, date_str):
        """
        Получает курс индийской рупии (INR) на указанную дату.
        """
        url = f"{self.base_url}/archive/{date_str}/daily_json.js"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data["Valute"]["INR"]["Value"]
            else:
                print(f"  {date_str}: статус {response.status_code}")
                return None
        except Exception as e:
            print(f"  {date_str}: ошибка {e}")
            return None

    def generate_date_range(self, start_date, end_date):
        """
        Генерирует список дат от start_date до end_date.
        """
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime("%Y/%m/%d"))
            current_date += timedelta(days=1)
        return dates

    def create_dataset(self):
        """
        Создает dataset.csv с данными о курсе INR.
        """
        print("Создание dataset.csv...")
        end_date = datetime.today()
        start_date = datetime(2023, 1, 1)  # Начинаем с 2023 года для теста

        dates = self.generate_date_range(start_date, end_date)
        data = []

        for date_str in dates:
            rate = self.get_inr_rate(date_str)
            if rate is not None:
                # Формат ISO 8601: YYYY-MM-DD
                iso_date = date_str.replace("/", "-")
                data.append([iso_date, rate])
                print(f"  {iso_date}: {rate} RUB")

        # Сохраняем в CSV
        with open("dataset.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["date", "exchange_rate"])
            writer.writerows(data)

        print(f"Успешно создано {len(data)} записей в dataset.csv")


def main():
    """Основная функция"""
    print("=== Лабораторная работа 2 ===")

    # Создаем dataset.csv если его нет
    if not os.path.exists("dataset.csv"):
        scraper = ExchangeRateScraper()
        scraper.create_dataset()
    else:
        print("dataset.csv уже существует")


if __name__ == "__main__":
    main()
