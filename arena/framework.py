import pandas as pd

class StockData:
    # From ChatGPT
    def __init__(self, date, open_price, high, low, close, volume):
        self.date = date
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class CsvFileReader:
    # From ChatGPT
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.num_rows = len(self.df)
        self.current_row_index = 0

    def next_row(self):
        if self.current_row_index >= self.num_rows:
            return None

        row = self.df.iloc[self.current_row_index]
        self.current_row_index += 1
        date = row['Date']
        open_price = row['Open']
        high = row['High']
        low = row['Low']
        close = row['Close']
        volume = row['Volume']
        return StockData(date, open_price, high, low, close, volume)
