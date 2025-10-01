import pandas as pd
import os

try:
    # Загружаем данные
    df = pd.read_csv("dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    print(" dataset.csv успешно загружен")
    print(f"Диапазон дат: от {df['Date'].min()} до {df['Date'].max()}")

    print("Разделение по неделям:")

    # Создаем идентификатор недели (год-неделя)
    df["YearWeek"] = (
        df["Date"].dt.isocalendar().year.astype(str)
        + "-"
        + df["Date"].dt.isocalendar().week.astype(str).str.zfill(2)
    )

    # Группируем по неделям
    created_files = 0
    for week, group in df.groupby("YearWeek"):
        if not group.empty:
            # Форматируем даты для названия файла
            start_date = group["Date"].min().strftime("%Y%m%d")
            end_date = group["Date"].max().strftime("%Y%m%d")
            filename = f"{start_date}_{end_date}.csv"

            # Сохраняем файл
            group[["Date", "INR_Rate"]].to_csv(filename, index=False)
            print(f"✓ {filename} - {len(group)} записей")
            created_files += 1

    print(f"✓ Создано {created_files} файлов по неделям")

except FileNotFoundError:
    print(" Ошибка: файл dataset.csv не найден!")
except Exception as e:
    print(f" Произошла ошибка: {e}")
