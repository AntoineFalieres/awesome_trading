import pandas as pd
import numpy as np

class Backtester:
    """
    A vectorized backtesting engine.
    """

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Runs the backtest.

        Args:
            data: DataFrame with 'close' and 'signal' columns.

        Returns:
            DataFrame with 'returns', 'strategy_returns', and 'equity_curve' columns.
        """
        data['returns'] = data['close'].pct_change()
        data['strategy_returns'] = data['returns'] * data['signal'].shift(1)
        data['equity_curve'] = (1 + data['strategy_returns']).cumprod()
        return data

    def calculate_metrics(self, data: pd.DataFrame) -> dict:
        """
        Calculates performance metrics.

        Args:
            data: DataFrame with 'strategy_returns' and 'equity_curve' columns.

        Returns:
            A dictionary with performance metrics.
        """
        total_return = data['equity_curve'].iloc[-1] - 1
        
        # Max Drawdown
        previous_peaks = data['equity_curve'].cummax()
        drawdown = (data['equity_curve'] - previous_peaks) / previous_peaks
        max_drawdown = drawdown.min()

        # Win Rate
        winning_trades = (data['strategy_returns'] > 0).sum()
        total_trades = (data['signal'] != 0).sum()
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        return {
            'Total Return': f"{total_return:.2%}",
            'Max Drawdown': f"{max_drawdown:.2%}",
            'Win Rate': f"{win_rate:.2%}"
        }
