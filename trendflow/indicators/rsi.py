import pandas as pd
from trendflow.indicators.base import Indicator


class RSI(Indicator):
    """
    Calculates the Relative Strength Index (RSI).
    
    RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss
    """

    def __init__(self, period: int = 14):
        if period < 2:
            raise ValueError("Period must be at least 2")
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the RSI indicator.

        Args:
            data: DataFrame with a 'close' column.

        Returns:
            DataFrame with an 'RSI_{period}' column.
        """
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")

        col_name = f"RSI_{self.period}"
        
        # Calculate price changes
        delta = data['close'].diff()
        
        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculate average gain and loss using EMA
        avg_gain = gain.ewm(span=self.period, adjust=False).mean()
        avg_loss = loss.ewm(span=self.period, adjust=False).mean()
        
        # Avoid division by zero
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Handle edge cases where avg_loss is 0
        rsi = rsi.fillna(0)
        
        data[col_name] = rsi
        
        return data
