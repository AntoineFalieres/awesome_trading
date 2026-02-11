import numpy as pd
import pandas as pd
from trendflow.indicators.base import Indicator

class MM30Indicator(Indicator):
    """
    Calculates the 30-period weighted moving average (MM30).
    """

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the weighted moving average.

        Args:
            data: DataFrame with a 'close' column.

        Returns:
            DataFrame with an 'MM30' column.
        """
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")

        weights = pd.Series(range(1, 31))
        data['MM30'] = data['close'].rolling(30).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
        return data
