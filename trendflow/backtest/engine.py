import pandas as pd
import numpy as np


class Backtester:
    """
    A vectorized backtesting engine for trading strategies.
    """

    def __init__(self, initial_capital: float = 10000, commission: float = 0):
        """
        Initialize backtester.
        
        Args:
            initial_capital: Starting capital (default: $10,000)
            commission: Trading commission as a decimal (e.g., 0.001 for 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, data: pd.DataFrame, signal_column: str = 'signal') -> pd.DataFrame:
        """
        Runs the backtest.

        Args:
            data: DataFrame with OHLCV columns and a signal column (-1, 0, 1)
            signal_column: Name of the signal column (default: 'signal')

        Returns:
            DataFrame with returns, strategy returns, and equity curve columns.
        """
        if signal_column not in data.columns:
            raise ValueError(f"Signal column '{signal_column}' not found in data")
        
        if 'close' not in data.columns:
            raise ValueError("Data must have a 'close' column")
        
        df = data.copy()
        
        # Calculate daily returns
        df['returns'] = df['close'].pct_change()
        
        # Strategy returns (signal shifted by 1 to avoid look-ahead bias)
        df['strategy_returns'] = df['returns'] * df[signal_column].shift(1)
        
        # Apply commission
        if self.commission > 0:
            df['signal_changes'] = (df[signal_column] != df[signal_column].shift(1)).astype(int)
            df['commission_cost'] = df['signal_changes'] * self.commission * abs(df['returns'])
            df['strategy_returns'] = df['strategy_returns'] - df['commission_cost']
        
        # Equity curve
        df['equity_curve'] = (1 + df['strategy_returns']).cumprod() * self.initial_capital
        
        # Buy and hold equity curve for comparison
        df['buy_hold_equity'] = (1 + df['returns']).cumprod() * self.initial_capital
        
        return df

    def calculate_metrics(self, data: pd.DataFrame, 
                         signal_column: str = 'signal',
                         risk_free_rate: float = 0.02) -> dict:
        """
        Calculates comprehensive performance metrics.

        Args:
            data: DataFrame with strategy_returns, equity_curve, and signal columns
            signal_column: Name of the signal column
            risk_free_rate: Annual risk-free rate for Sharpe ratio calculation

        Returns:
            Dictionary with performance metrics
        """
        if 'strategy_returns' not in data.columns:
            raise ValueError("Data must have 'strategy_returns' column. Run backtester first.")
        
        if 'returns' not in data.columns:
            raise ValueError("Data must have 'returns' column (buy-and-hold returns)")
        
        if 'equity_curve' not in data.columns:
            raise ValueError("Data must have 'equity_curve' column")
        
        returns = data['strategy_returns'].dropna()
        equity = data['equity_curve']
        buy_hold_equity = data.get('buy_hold_equity', None)
        
        # Total Return
        final_equity = equity.iloc[-1]
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        
        # Buy and Hold Return (for comparison)
        if buy_hold_equity is not None:
            buy_hold_return = (buy_hold_equity.iloc[-1] - self.initial_capital) / self.initial_capital
        else:
            buy_hold_return = None
        
        # Annualized metrics (assume 252 trading days per year)
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1 if len(returns) > 0 else 0
        annualized_vol = returns.std() * np.sqrt(252) if len(returns) > 0 else 0
        
        # Sharpe Ratio
        excess_returns = returns - (risk_free_rate / 252)
        sharpe_ratio = (excess_returns.mean() * 252) / annualized_vol if annualized_vol > 0 else 0
        
        # Sortino Ratio (only penalizes downside volatility)
        downside_returns = returns[returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = (excess_returns.mean() * 252) / downside_vol if downside_vol > 0 else 0
        
        # Maximum Drawdown
        previous_peaks = equity.cummax()
        drawdown = (equity - previous_peaks) / previous_peaks
        max_drawdown = drawdown.min()
        
        # Consecutive winning/losing days
        positive_returns = (returns > 0).sum()
        negative_returns = (returns < 0).sum()
        total_trades = positive_returns + negative_returns
        win_rate = positive_returns / total_trades if total_trades > 0 else 0
        
        # Number of trades
        if signal_column in data.columns:
            signal_changes = (data[signal_column] != data[signal_column].shift(1)).astype(int)
            num_trades = signal_changes.sum()
        else:
            num_trades = None
        
        metrics = {
            'Total Return': total_return,
            'Annualized Return': annualized_return,
            'Annualized Volatility': annualized_vol,
            'Sharpe Ratio': sharpe_ratio,
            'Sortino Ratio': sortino_ratio,
            'Max Drawdown': max_drawdown,
            'Win Rate': win_rate,
            'Positive Days': positive_returns,
            'Negative Days': negative_returns,
            'Total Trade Days': total_trades,
        }
        
        if buy_hold_return is not None:
            metrics['Buy & Hold Return'] = buy_hold_return
            metrics['Excess Return vs B&H'] = total_return - buy_hold_return
        
        if num_trades is not None:
            metrics['Total Trades'] = num_trades
        
        return metrics
