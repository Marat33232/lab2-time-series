import pandas as pd


class DataIterator:
    """Итератор для построчного чтения dataset.csv"""

    def __init__(self, filename: str = "dataset.csv"):
        try:
            self.df = pd.read_csv(filename)
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            self.df = self.df.sort_values("Date").reset_index(drop=True)
            self.current_index = 0
            print(f"Итератор инициализирован. Всего записей: {len(self.df)}")
        except Exception as e:
            print(f"Ошибка инициализации итератора: {e}")
            self.df = pd.DataFrame()
            self.current_index = 0

    def __iter__(self):
        """Позволяет использовать объект в цикле for"""
        self.current_index = 0
        return self

    def __next__(self):
        """Возвращает (дата, курс)"""
        if self.current_index >= len(self.df):
            raise StopIteration

        row = self.df.iloc[self.current_index]
        self.current_index += 1
        return row["Date"], row["INR_Rate"]

    def reset(self):
        """Сброс итератора"""
        self.current_index = 0
        print("Итератор сброшен в начало")

    def get_current_position(self):
        """Текущий индекс"""
        return self.current_index
