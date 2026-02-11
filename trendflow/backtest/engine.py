import pandas as pd
import numpy as np

def run_backtest(initial_capital: float, data: pd.DataFrame, signals: pd.DataFrame):
    """
    Runs a simple backtest on a trading strategy.

    Args:
        initial_capital (float): The initial capital for the backtest.
        data (pd.DataFrame): A pandas DataFrame with OHLCV data.
        signals (pd.DataFrame): A pandas DataFrame with trading signals.

    Returns:
        dict: A dictionary with backtesting performance metrics.
    """
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['Stock'] = 100 * signals['signal']   # This is where we make an assumption of 100 shares per trade

    portfolio = positions.multiply(data['Close'], axis=0)
    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()

    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    
    # Calculate performance metrics
    total_return = (portfolio['total'][-1] / portfolio['total'][0]) - 1
    
    trades = signals['positions'][signals['positions'] != 0]
    num_trades = len(trades)
    
    wins = trades[trades > 0]
    losses = trades[trades < 0]
    num_wins = len(wins)
    num_losses = len(losses)
    win_rate = (num_wins / num_trades) * 100 if num_trades > 0 else 0
    
    return {
        "portfolio": portfolio,
        "total_return": total_return,
        "num_trades": num_trades,
        "num_wins": num_wins,
        "num_losses": num_losses,
        "win_rate": win_rate
    }
