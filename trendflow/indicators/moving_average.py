import pandas as pd

def sma(data: pd.Series, window: int) -> pd.Series:
    """
    Calculates the Simple Moving Average (SMA).

    Args:
        data (pd.Series): A pandas Series of prices.
        window (int): The moving average window.

    Returns:
        pd.Series: A pandas Series with the SMA values.
    """
    return data.rolling(window=window).mean()
