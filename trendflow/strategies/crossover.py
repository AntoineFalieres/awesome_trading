import pandas as pd
import numpy as np
from trendflow.indicators.moving_average import sma

def crossover_strategy(data: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    """
    Generates trading signals based on a moving average crossover strategy.

    Args:
        data (pd.DataFrame): A pandas DataFrame with OHLCV data.
        short_window (int): The short moving average window.
        long_window (int): The long moving average window.

    Returns:
        pd.DataFrame: A pandas DataFrame with the trading signals.
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = sma(data['Close'], short_window)
    signals['long_mavg'] = sma(data['Close'], long_window)

    # Generate signal when short MA crosses above long MA
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                                > signals['long_mavg'][short_window:], 1.0, 0.0)   

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    return signals
