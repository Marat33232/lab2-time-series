import pandas as pd
from datetime import datetime
import glob
import os


def get_data_single_file(date: datetime, filename: str = "dataset.csv"):
    """поиск в исходном файле"""
    try:
        df = pd.read_csv(filename)
        df["Date"] = pd.to_datetime(df["Date"])
        result = df[df["Date"] == date]
        return result["INR_Rate"].values[0] if not result.empty else None
    except Exception as e:
        print(f"Ошибка в get_data_single_file: {e}")
        return None


def get_data_xy_files(date: datetime):
    """1 поиск в разделенных файлах X.csv и Y.csv"""
    try:
        # Загружаем файлы с датами и данными
        dates_df = pd.read_csv("X.csv")
        data_df = pd.read_csv("Y.csv")

        # Преобразуем даты
        dates_df["Date"] = pd.to_datetime(dates_df["Date"])

        # Ищем совпадение
        mask = dates_df["Date"] == date

        if mask.any():
            idx = mask.idxmax()
            return data_df.iloc[idx]["INR_Rate"]
        return None
    except Exception as e:
        print(f"Ошибка в get_data_xy_files: {e}")
        return None


def get_data_year_files(date: datetime):
    """2 поиск в файлах, разделенных по годам"""
    try:
        year = date.year

        # Ищем файл для этого года
        pattern = f"{year}0101_{year}1231.csv"
        if os.path.exists(pattern):
            df = pd.read_csv(pattern)
            df["Date"] = pd.to_datetime(df["Date"])
            result = df[df["Date"] == date]
            return result["INR_Rate"].values[0] if not result.empty else None

        return None
    except Exception as e:
        print(f"Ошибка в get_data_year_files: {e}")
        return None


def get_data_week_files(date: datetime):
    """3 поиск в файлах, разделенных по неделям"""
    try:
        files = glob.glob("*_*.csv")

        for file in files:
            # Пропускаем файлы не по неделям
            if file in ["X.csv", "Y.csv", "dataset.csv"]:
                continue

            df = pd.read_csv(file)
            df["Date"] = pd.to_datetime(df["Date"])
            result = df[df["Date"] == date]

            if not result.empty:
                return result["INR_Rate"].values[0]

        return None
    except Exception as e:
        print(f"Ошибка в get_data_week_files: {e}")
        return None


def test_all_search_functions():

    # Тестовые даты
    test_dates = [
        datetime(2016, 1, 15),  # Должна существовать
        datetime(2016, 1, 20),  # Должна существовать
        datetime(2025, 1, 1),  # Не должна существовать
    ]

    for test_date in test_dates:
        print(f"\nДата: {test_date.strftime('%Y-%m-%d')}")
        print(f"Версия 0 (исходный файл): {get_data_single_file(test_date)}")
        print(f"Версия 1 (X/Y файлы): {get_data_xy_files(test_date)}")
        print(f"Версия 2 (по годам): {get_data_year_files(test_date)}")
        print(f"Версия 3 (по неделям): {get_data_week_files(test_date)}")


if __name__ == "__main__":
    test_all_search_functions()
