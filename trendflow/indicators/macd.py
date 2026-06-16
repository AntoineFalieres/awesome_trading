import pandas as pd
from trendflow.indicators.base import Indicator


class MACD(Indicator):
    """
    Calculates the Moving Average Convergence Divergence (MACD).
    
    MACD = 12-period EMA - 26-period EMA
    Signal Line = 9-period EMA of MACD
    Histogram = MACD - Signal Line
    """

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        if fast >= slow:
            raise ValueError("Fast period must be less than slow period")
        if signal < 2:
            raise ValueError("Signal period must be at least 2")
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the MACD indicator.

        Args:
            data: DataFrame with a 'close' column.

        Returns:
            DataFrame with 'MACD', 'MACD_Signal', and 'MACD_Histogram' columns.
        """
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")

        # Calculate EMAs
        ema_fast = data['close'].ewm(span=self.fast, adjust=False).mean()
        ema_slow = data['close'].ewm(span=self.slow, adjust=False).mean()
        
        # Calculate MACD line
        macd = ema_fast - ema_slow
        
        # Calculate signal line (9-period EMA of MACD)
        signal_line = macd.ewm(span=self.signal, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd - signal_line
        
        data['MACD'] = macd
        data['MACD_Signal'] = signal_line
        data['MACD_Histogram'] = histogram
        
        return data
