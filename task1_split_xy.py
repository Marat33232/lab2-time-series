import pandas as pd

# Загружаем данные
df = pd.read_csv("dataset.csv")

# Проверяем структуру данных
print("Структура данных:")
print(df.head())
print(f"Всего строк: {len(df)}")

# Разделяем на X.csv (даты) и Y.csv (данные)
df[["Date"]].to_csv("X.csv", index=False)
df[["INR_Rate"]].to_csv("Y.csv", index=False)

print("✓ Созданы файлы:")
print("  - X.csv (даты)")
print("  - Y.csv (курсы INR)")
print(f"✓ Каждый файл содержит {len(df)} строк")
