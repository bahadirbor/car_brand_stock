# BIST Automotive Stocks Data Scraper

A Python application that fetches historical stock data from Yahoo Finance API for Borsa Istanbul (BIST) automotive sector companies and combines them into a single DataFrame.

[Kaggle Dataset](https://www.kaggle.com/datasets/bahadirbor/bist-automotive-stocks)

## Features

- **Multi-Stock Data Fetching**: Retrieves data for 8 different BIST automotive companies in one go
- **Flexible Time Range**: Customizable data fetching from 1 day to 5 years
- **Automatic Data Processing**: Daily return calculation and missing data filling
- **CSV Export**: Save data in CSV format
- **Error Handling**: Robust error catching and handling

## Supported Stocks

| Symbol | Company Name |
|--------|-------------|
| ASUZU.IS | Anadolu Isuzu |
| DOAS.IS | Dogus Oto |
| FROTO.IS | Ford Otosan |
| KARSN.IS | Karsan |
| OTKAR.IS | Otokar |
| TMSN.IS | Tumosan |
| TOASO.IS | Tofas |
| TTRAK.IS | Turk Traktor |

## Usage

### Basic Usage

```python
from main import MultiStockDataFrame

# Initialize the class
fetcher = MultiStockDataFrame()

# Define stock symbols
symbols = ["FROTO.IS", "TOASO.IS", "OTKAR.IS"]

# Fetch data (default: 1 year)
df = fetcher.create_combined_dataframe(symbols)

# Save as CSV
fetcher.save_to_csv(df)
```

### Advanced Usage

```python
# Fetch 5 years of data
df = fetcher.create_combined_dataframe(symbols, period="5y")

# Fetch weekly data
df = fetcher.create_combined_dataframe(symbols, period="1y", interval="1wk")

# Single stock data
single_stock = fetcher.get_single_stock_data("FROTO.IS", period="2y")
```

### Command Line Execution

```bash
python main.py
```

## Output Format

The program creates an `all_datas.csv` file with the following columns:

| Column | Description |
|--------|-------------|
| date | Date |
| stock_name | Company name |
| open | Opening price |
| high | Highest price |
| low | Lowest price |
| close | Closing price |
| daily_return | Daily return (%) |
| adj_close | Adjusted closing price |
| volume | Trading volume |

## Configuration

### Time Period Options

- `1d`: 1 day
- `5d`: 5 days
- `1mo`: 1 month
- `3mo`: 3 months
- `6mo`: 6 months
- `1y`: 1 year (default)
- `2y`: 2 years
- `5y`: 5 years
- `10y`: 10 years
- `ytd`: Year to date
- `max`: Maximum data

### Data Interval Options

- `1m`: 1 minute
- `2m`: 2 minutes
- `5m`: 5 minutes
- `15m`: 15 minutes
- `30m`: 30 minutes
- `60m`: 1 hour
- `90m`: 1.5 hours
- `1h`: 1 hour
- `1d`: 1 day (default)
- `5d`: 5 days
- `1wk`: 1 week
- `1mo`: 1 month
- `3mo`: 3 months

## License

This project is licensed under the Apache 2.0 License.

## Disclaimer

This software is for educational and research purposes only. The authors are not responsible for any financial decisions made based on the data provided by this application. Always consult with a financial advisor before making investment decisions.

## Dependencies

- `requests`: For making HTTP requests to Yahoo Finance API
- `pandas`: For data manipulation and analysis
- `warnings`: For handling warning messages