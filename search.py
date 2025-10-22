import os
import glob
import pandas as pd
from datetime import datetime


def get_data_single_file(date: datetime, filename: str = "dataset.csv"):
    try:
        df = pd.read_csv(filename)
        df["Date"] = pd.to_datetime(df["Date"])
        result = df[df["Date"] == date]
        return result["INR_Rate"].iloc[0] if not result.empty else None
    except Exception:
        return None


def get_data_xy_files(date: datetime):
    try:
        x = pd.read_csv("X.csv")
        y = pd.read_csv("Y.csv")
        x["Date"] = pd.to_datetime(x["Date"])
        mask = x["Date"] == date
        if mask.any():
            idx = mask.idxmax()
            return y.iloc[idx]["INR_Rate"]
        return None
    except Exception:
        return None


def get_data_year_files(date: datetime):
    year = date.year
    files = glob.glob(f"{year}*.csv")
    for file in files:
        if file in ["X.csv", "Y.csv", "dataset.csv"]:
            continue
        df = pd.read_csv(file)
        df["Date"] = pd.to_datetime(df["Date"])
        result = df[df["Date"] == date]
        if not result.empty:
            return result["INR_Rate"].iloc[0]
    return None


def get_data_week_files(date: datetime):
    files = glob.glob("*_*.csv")
    for file in files:
        if file in ["X.csv", "Y.csv", "dataset.csv"]:
            continue
        df = pd.read_csv(file)
        df["Date"] = pd.to_datetime(df["Date"])
        result = df[df["Date"] == date]
        if not result.empty:
            return result["INR_Rate"].iloc[0]
    return None


def demonstrate_all_versions():
    print("=== 4 ВЕРСИИ ПОИСКА ПО ДАТЕ ===")

    test_dates = [
        datetime(2016, 1, 15),
        datetime(2016, 1, 20),
        datetime(2016, 2, 5),
        datetime(2025, 1, 1),
    ]

    for i, test_date in enumerate(test_dates, 1):
        print(f"\nТест {i}: {test_date.strftime('%Y-%m-%d')}")
        print("-" * 30)
        print(f"dataset.csv : {get_data_single_file(test_date)}")
        print(f"X/Y         : {get_data_xy_files(test_date)}")
        print(f"По годам    : {get_data_year_files(test_date)}")
        print(f"По неделям  : {get_data_week_files(test_date)}")
