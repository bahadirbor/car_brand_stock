CREATE TABLE IF NOT EXISTS Stocks(
    date_time TEXT NOT NULL,
    stock_name TEXT NOT NULL,
    open_value REAL NOT NULL,
    high_value REAL NOT NULL,
    low_value REAL NOT NULL,
    close_value REAL NOT NULL,
    daily_return REAL NOT NULL,
    adj_close REAL NOT NULL,
    volume INTEGER NOT NULL
);