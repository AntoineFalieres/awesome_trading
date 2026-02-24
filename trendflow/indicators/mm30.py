import numpy as np
import pandas as pd
from trendflow.indicators.base import Indicator

class MM30Indicator(Indicator):
    """
    Calculates the 30-period weighted moving average (MM30).
    """

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the weighted moving average using numpy.

        Args:
            data: DataFrame with a 'close' column.

        Returns:
            DataFrame with an 'MM30' column.
        """
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")

        period = 30
        weights = np.arange(1, period + 1)
        
        # The result of convolve will be shorter by 'period - 1'. 
        # We need to pad it with NaNs at the beginning.
        wma = np.convolve(data['close'], weights/weights.sum(), 'valid')
        data['MM30'] = np.concatenate([np.full(period - 1, np.nan), wma])
        
        return data
