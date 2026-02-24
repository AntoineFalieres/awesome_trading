import pandas as pd
import numpy as np
from trendflow.indicators.base import Indicator

class VolumeStats(Indicator):
    """
    Calculates volume moving average and the ratio of current volume to the moving average.
    """

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the volume moving average and ratio.

        Args:
            data: DataFrame with a 'volume' column.

        Returns:
            DataFrame with 'vol_ma' and 'vol_ratio' columns.
        """
        if 'volume' not in data.columns:
            raise ValueError("Data must have a 'volume' column")

        period = 30
        data['vol_ma'] = data['volume'].rolling(window=period).mean()
        
        # Handle division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            data['vol_ratio'] = (data['volume'] / data['vol_ma'])
        
        data['vol_ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
        data['vol_ratio'].fillna(0, inplace=True)
        
        return data
