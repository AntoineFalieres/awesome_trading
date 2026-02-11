import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical stock data.

    Args:
        ticker: The stock ticker symbol.
        start_date: The start date in YYYY-MM-DD format.
        end_date: The end date in YYYY-MM-DD format.

    Returns:
        A pandas DataFrame with OHLCV data.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    # Ensure column names are lowercase
    data.columns = [col.lower() for col in data.columns]
    return data
