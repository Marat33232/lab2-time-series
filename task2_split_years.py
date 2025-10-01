import pandas as pd
import os

print("Текущая рабочая директория:", os.getcwd())
print("Файлы в директории:", os.listdir("."))

# Загружаем данные
try:
    df = pd.read_csv("dataset.csv")
    print("✓ dataset.csv успешно загружен")
    print(f"Колонки: {df.columns.tolist()}")
    print(f"Первые строки:\n{df.head()}")

    # Преобразуем даты
    df["Date"] = pd.to_datetime(df["Date"])
    print(f"Диапазон дат: от {df['Date'].min()} до {df['Date'].max()}")

    print("\nРазделение по годам:")

    # Группируем по году
    for year, group in df.groupby(df["Date"].dt.year):
        if not group.empty:
            # Форматируем даты для названия файла
            start_date = group["Date"].min().strftime("%Y%m%d")
            end_date = group["Date"].max().strftime("%Y%m%d")
            filename = f"{start_date}_{end_date}.csv"

            # Сохраняем файл
            group.to_csv(filename, index=False)
            print(f"✓ Создан {filename} - {len(group)} записей")

    print("✓ Все файлы по годам созданы")

except FileNotFoundError:
    print("❌ Ошибка: файл dataset.csv не найден!")
    print("Убедитесь, что файл находится в той же папке, что и скрипт")
except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
