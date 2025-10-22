import csv
import requests
from datetime import datetime, timedelta


def get_inr_rate(date_str):
    """Получает курс INR на указанную дату"""
    url = f"https://www.cbr-xml-daily.ru/archive/{date_str}/daily_json.js"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["Valute"]["INR"]["Value"]
        else:
            print(f"  {date_str}: статус {response.status_code}")
            return None
    except Exception as e:
        print(f" {date_str}: ошибка {e}")
        return None


def generate_date_range(start_date, end_date):
    """Генерирует список дат между start_date и end_date"""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y/%m/%d"))
        current_date += timedelta(days=1)
    return dates


def kurs():
    """Создаёт dataset.csv с курсами INR"""
    print("Начинаем сбор данных по курсу INR...")
    end_date = datetime.today()
    start_date = datetime(2016, 1, 1)

    dates = generate_date_range(start_date, end_date)
    data = []

    for date_str in dates:
        rate = get_inr_rate(date_str)
        if rate is not None:
            formatted_date = date_str.replace("/", "-")
            data.append([formatted_date, rate])
            print(f" {formatted_date}: {rate} RUB")
        else:
            print(f"--- {date_str}: данных нет")

    with open("dataset.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "INR_Rate"])
        writer.writerows(data)

    print(f"\n✓ Сохранено {len(data)} записей в dataset.csv")
