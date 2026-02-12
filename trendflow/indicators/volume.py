import pandas as pd
from trendflow.indicators.base import Indicator

class VolumeStats(Indicator):
    """
    Calculates volume moving average and the ratio of current volume to the moving average.
    """

    def __init__(self, period: int = 30):
        self.period = period

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

        vol_ma_col = f'vol_ma_{self.period}'
        data[vol_ma_col] = data['volume'].rolling(window=self.period).mean()
        
        # Handle division by zero
        data['vol_ratio'] = (data['volume'] / data[vol_ma_col]).fillna(0)
        data['vol_ratio'].replace([float('inf'), -float('inf')], 0, inplace=True)
        
        return data
