import yfinance as yf
import pandas as pd

def get_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads historical stock data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A pandas DataFrame with the OHLCV data.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data
