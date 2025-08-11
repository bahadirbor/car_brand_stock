import os
import sqlite3
import requests
import pandas as pd
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

load_dotenv(dotenv_path="config/.env")
database_path = str(os.getenv("DATABASE_NAME"))


class MultiStockDataFrame:
    """Daily isolation of multiple stocks in single DataFrame combinator class"""

    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # BIST stock symbols and company names
        self.bist_stocks = {
            "ASUZU.IS": "Anadolu Isuzu",
            "DOAS.IS": "Dogus Oto",
            "FROTO.IS": "Ford Otosan",
            "KARSN.IS": "Karsan",
            "OTKAR.IS": "Otokar",
            "TMSN.IS": "Tumosan",
            "TOASO.IS": "Tofas",
            "TTRAK.IS": "Turk Traktor",
        }

    def get_single_stock_data(self, symbol, period="1y", interval="1d"):
        """Scrap stock data for one company"""
        try:
            url = f"{self.base_url}{symbol}"
            params = {
                "range": period,
                "interval": interval,
                "includePrePost": "false",
                "includeAdjustedClose": "true"
            }

            response = requests.get(url, params=params, headers=self.headers, verify=False, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'chart' not in data or not data['chart']['result']:
                print(f"Data not found for {symbol}")
                return None

            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            ohlcv = result['indicators']['quote'][0]

            df = pd.DataFrame({
                'open': ohlcv['open'],
                'high': ohlcv['high'],
                'low': ohlcv['low'],
                'close': ohlcv['close'],
                'volume': ohlcv['volume']
            })

            # Added adjusted close data
            if 'adjclose' in result['indicators']:
                df['adj_close'] = result['indicators']['adjclose'][0]['adjclose']
            else:
                df['adj_close'] = df['close']

            # Convert Timestamp to Date
            df.index = pd.to_datetime(timestamps, unit='s')
            df.index.name = 'date'
            df = df.reset_index()
            df["date"] = df["date"].dt.date

            # Add stock name to table
            df["stock_name"] = self.bist_stocks[symbol]

            return df

        except Exception as e:
            print(f"Data scrap error for {symbol}: {e}")
            return None

    def create_combined_dataframe(self, symbols, period="1y", interval="1d"):
        """
        Merge multiple stock datas into one DataFrame

        Args:
            symbols (list): Stock symbol list
            period (str): Data period
            interval (str): Data range

        Returns:
            pandas.DataFrame: Concatenated DataFrame
        """
        all_dataframes = []
        successful_symbols = []
        failed_symbols = []

        for i, symbol in enumerate(symbols, 1):
            print(f"{i}/{len(symbols)} - {symbol} ({self.bist_stocks.get(symbol, symbol)}) processing...")

            stock_data = self.get_single_stock_data(symbol, period, interval)

            if stock_data is not None:
                all_dataframes.append(stock_data)
                successful_symbols.append(symbol)
            else:
                failed_symbols.append(symbol)

        if all_dataframes:
            combined_data = pd.concat(all_dataframes, axis=0, ignore_index=True)
            combined_data = combined_data.sort_values(['stock_name', 'date'])

            combined_data['daily_return'] = combined_data.groupby('stock_name')['close'].pct_change() * 100

            price_columns = ['open', 'high', 'low', 'close', 'volume', 'adj_Close']
            for col in price_columns:
                if col in combined_data.columns:
                    combined_data[col] = combined_data.groupby('stock_name')[col].fillna(method='ffill')

            # Final reset index
            combined_data = combined_data.reset_index(drop=True)

            new_column_order = ["date", "stock_name", "open", "high", "low",
                                "close", "daily_return", "adj_close", "volume"]
            combined_data = combined_data[new_column_order]

            return combined_data
        else:
            print("There is no data!")
            return None

    def create_database(self, db_path, sql):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(sql, "r") as sql_code:
            sql_script = sql_code.read()
            cursor.executescript(sql_script)

        conn.commit()
        conn.close()

    def save_to_csv(self, df):
        """Save DataFrame to a CSV file"""
        if df is None or df.empty:
            print("There is no data!")
            return

        df.to_csv("data/automotive_stocks.csv", index=False, float_format='%.3f')

    def save_to_sql(self, df, db_path, table_name="Stocks"):
        """Save DataFrame into SQLite database table"""
        conn = sqlite3.connect(db_path)
        df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)


def main():
    multi_fetcher = MultiStockDataFrame()

    # Creating sqlite database
    multi_fetcher.create_database(database_path, "data/automotive.sql")

    # BIST Automotive Companies
    stock_symbols = [
        "ASUZU.IS", #Anadolu Isuzu
        "DOAS.IS", #Dogus Oto
        "FROTO.IS", #Ford Otosan
        "KARSN.IS", #Karsan
        "OTKAR.IS", #Otokar
        "TMSN.IS", #Tumosan
        "TOASO.IS", #Tofas
        "TTRAK.IS", #Turk Traktor
    ]

    combined_df = multi_fetcher.create_combined_dataframe(stock_symbols, period="5y")

    if combined_df is not None:
        """Save to CSV file and SQLite Database Table"""
        multi_fetcher.save_to_csv(combined_df)
        multi_fetcher.save_to_sql(combined_df, database_path)


if __name__ == "__main__":
    main()