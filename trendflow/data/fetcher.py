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
    print(f"fetch_data: ticker='{ticker}', type={type(ticker)}")
    # Only use the first ticker if multiple are provided
    single_ticker = ticker.split()[0]
    data = yf.download(single_ticker, start=start_date, end=end_date)

    if data.empty:
        raise ValueError(f"No data found for ticker {single_ticker} from {start_date} to {end_date}")
        
    print(f"fetch_data: data.columns='{data.columns}', type={type(data.columns)}")
    
    # Defensively handle single and multi-level columns
    new_cols = []
    for col in data.columns:
        if isinstance(col, tuple):
            new_cols.append(col[0].lower())
        else:
            new_cols.append(str(col).lower())
    data.columns = new_cols
    
    return data
