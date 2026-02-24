import pandas as pd
from trendflow.indicators.base import Indicator

class MovingAverage(Indicator):
    """
    Calculates various types of moving averages.
    """

    def __init__(self, period: int, ma_type: str = 'sma'):
        print(f"MovingAverage.__init__: ma_type='{ma_type}', type={type(ma_type)}")
        if ma_type not in ['sma', 'ema', 'wma']:
            raise ValueError("ma_type must be one of 'sma', 'ema', or 'wma'")
        self.period = period
        self.ma_type = ma_type

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the selected moving average.

        Args:
            data: DataFrame with a 'close' column.

        Returns:
            DataFrame with the calculated moving average column.
        """
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")

        col_name = f"{self.ma_type.upper()}_{self.period}"

        if self.ma_type == 'sma':
            data[col_name] = data['close'].rolling(window=self.period).mean()
        elif self.ma_type == 'ema':
            data[col_name] = data['close'].ewm(span=self.period, adjust=False).mean()
        elif self.ma_type == 'wma':
            weights = pd.Series(range(1, self.period + 1))
            data[col_name] = data['close'].rolling(self.period).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
            
        return data
