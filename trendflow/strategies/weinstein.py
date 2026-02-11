import pandas as pd
import numpy as np
from trendflow.indicators.mm30 import MM30Indicator
from trendflow.indicators.volume import VolumeStats
from trendflow.indicators.ma import MovingAverage

class WeinsteinStrategy:
    """
    Implements the Weinstein trading strategy with risk management and an optional trend filter.
    """

    def __init__(
        self,
        stop_loss_pct: float = 0.05,
        take_profit_pct: float = 0.1,
        use_trend_filter: bool = False,
        long_ma_period: int = 200,
        long_ma_type: str = 'sma'
    ):
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.use_trend_filter = use_trend_filter
        self.long_ma_period = long_ma_period
        self.long_ma_type = long_ma_type

        self.mm30_indicator = MM30Indicator()
        self.volume_stats = VolumeStats()
        if self.use_trend_filter:
            self.long_ma_indicator = MovingAverage(period=self.long_ma_period, ma_type=self.long_ma_type)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals based on the Weinstein strategy.

        Args:
            data: DataFrame with OHLCV data.

        Returns:
            DataFrame with 'signal' and 'exit_reason' columns.
        """
        data = self.mm30_indicator.calculate(data)
        data = self.volume_stats.calculate(data)

        base_entry_condition = (data['close'] > data['MM30']) & (data['vol_ratio'] > 2.0)

        final_entry_condition = base_entry_condition
        if self.use_trend_filter:
            data = self.long_ma_indicator.calculate(data)
            long_ma_col = f"{self.long_ma_type.upper()}_{self.long_ma_period}"
            trend_filter_condition = data['close'] > data[long_ma_col]
            final_entry_condition = base_entry_condition & trend_filter_condition

        signals = np.zeros(len(data))
        exit_reasons = np.full(len(data), '', dtype=object)
        in_position = False
        entry_price = 0

        for i in range(1, len(data)):
            if not in_position and final_entry_condition.iloc[i]:
                signals[i] = 1
                in_position = True
                entry_price = data['close'].iloc[i]
            elif in_position:
                # Check for stop loss
                if data['low'].iloc[i] < entry_price * (1 - self.stop_loss_pct):
                    signals[i] = -1
                    exit_reasons[i] = 'Stop Loss'
                    in_position = False
                    entry_price = 0
                # Check for take profit
                elif data['high'].iloc[i] > entry_price * (1 + self.take_profit_pct):
                    signals[i] = -1
                    exit_reasons[i] = 'Take Profit'
                    in_position = False
                    entry_price = 0
                # Sell signal based on price crossing below MM30
                elif data['close'].iloc[i] < data['MM30'].iloc[i]:
                    signals[i] = -1
                    exit_reasons[i] = 'MM30 Cross'
                    in_position = False
                    entry_price = 0

        data['signal'] = signals
        data['exit_reason'] = exit_reasons
        return data

