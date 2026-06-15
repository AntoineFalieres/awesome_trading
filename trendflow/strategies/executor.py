import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from trendflow.data import get_market_data
from trendflow.backtest import Backtester
from trendflow.indicators import MovingAverage, VolumeStats, RSI, MACD
from trendflow.strategies.strategy import Strategy


class StrategyExecutionError(Exception):
    """Raised when strategy execution fails."""
    pass


class StrategyExecutor:
    """
    Executes a trading strategy against historical data.
    """

    def __init__(self, strategy: Strategy):
        """
        Initialize executor with a strategy.

        Args:
            strategy: Strategy object to execute
        """
        self.strategy = strategy
        self.data = None
        self.results = None

    def execute(self) -> Dict[str, Any]:
        """
        Run the strategy and return backtest results.

        Returns:
            Dictionary with:
                - 'data': DataFrame with all calculations
                - 'metrics': Performance metrics
                - 'trades': Trade-by-trade breakdown
                
        Raises:
            StrategyExecutionError: If strategy execution fails
        """
        try:
            # Validate strategy
            errors = self.strategy.validate()
            if errors:
                raise StrategyExecutionError(f"Strategy validation failed: {'; '.join(errors)}")

            # Fetch market data
            print(f"Fetching data for {self.strategy.symbol}...")
            try:
                self.data = get_market_data(
                    self.strategy.symbol,
                    self.strategy.start_date,
                    self.strategy.end_date
                )
            except Exception as e:
                raise StrategyExecutionError(
                    f"Failed to fetch data for {self.strategy.symbol}: {e}. "
                    f"Check if symbol exists and date range is valid."
                )

            if self.data.empty:
                raise StrategyExecutionError(
                    f"No data returned for {self.strategy.symbol} in date range "
                    f"{self.strategy.start_date} to {self.strategy.end_date}"
                )

            # Calculate indicators
            print("Calculating indicators...")
            try:
                self._calculate_indicators()
            except Exception as e:
                raise StrategyExecutionError(f"Failed to calculate indicators: {e}")

            # Generate signals
            print("Generating signals...")
            try:
                self.data['signal'] = 0
                self._apply_entry_conditions()
                self._apply_exit_conditions()
            except Exception as e:
                raise StrategyExecutionError(f"Failed to generate signals: {e}")

            # Run backtest
            print("Running backtest...")
            try:
                backtester = Backtester(
                    initial_capital=self.strategy.backtest_params.get('initial_capital', 10000),
                    commission=self.strategy.backtest_params.get('commission', 0.001)
                )
                self.data = backtester.run(self.data, signal_column='signal')
                metrics = backtester.calculate_metrics(self.data, signal_column='signal')
            except Exception as e:
                raise StrategyExecutionError(f"Failed to run backtest: {e}")

            # Extract trade information
            trades = self._extract_trades()

            self.results = {
                'data': self.data,
                'metrics': metrics,
                'trades': trades
            }

            print("✓ Backtest completed successfully")
            return self.results

        except StrategyExecutionError:
            raise
        except Exception as e:
            raise StrategyExecutionError(f"Unexpected error during execution: {e}")

    def _calculate_indicators(self) -> None:
        """Calculate all indicators specified in the strategy."""
        self.column_mapping = {}  # Map indicator names to actual column names
        
        for indicator_config in self.strategy.indicators:
            indicator_name = indicator_config.name
            indicator_type = indicator_config.type
            params = indicator_config.params

            if indicator_type == 'moving_average':
                period = params.get('period')
                ma_type = params.get('ma_type', 'sma')
                ma = MovingAverage(period=period, ma_type=ma_type)
                self.data = ma.calculate(self.data)
                # Map indicator name to actual column created
                actual_col = f"{ma_type.upper()}_{period}"
                self.column_mapping[indicator_name] = actual_col

            elif indicator_type == 'volume':
                volume = VolumeStats()
                self.data = volume.calculate(self.data)
                # VolumeStats creates 'vol_ma' and 'vol_ratio'
                self.column_mapping[indicator_name] = 'vol_ma'

            elif indicator_type == 'rsi':
                period = params.get('period', 14)
                rsi = RSI(period=period)
                self.data = rsi.calculate(self.data)
                actual_col = f"RSI_{period}"
                self.column_mapping[indicator_name] = actual_col

            elif indicator_type == 'macd':
                fast = params.get('fast', 12)
                slow = params.get('slow', 26)
                signal = params.get('signal', 9)
                macd = MACD(fast=fast, slow=slow, signal=signal)
                self.data = macd.calculate(self.data)
                # MACD creates MACD, MACD_Signal, MACD_Histogram
                self.column_mapping[indicator_name] = 'MACD'

            else:
                print(f"Warning: Unknown indicator type '{indicator_type}'")

    def _apply_entry_conditions(self) -> None:
        """Apply entry conditions to generate entry signals (1)."""
        entry_signals = self._evaluate_conditions(self.strategy.entry_conditions, is_entry=True)
        self.data.loc[entry_signals, 'signal'] = 1

    def _apply_exit_conditions(self) -> None:
        """Apply exit conditions to generate exit signals (0 or -1)."""
        # Only apply exit signals where we're currently in a position
        exit_signals = self._evaluate_conditions(self.strategy.exit_conditions, is_entry=False)
        in_position = self.data['signal'].shift(1) == 1
        self.data.loc[exit_signals & in_position, 'signal'] = 0

    def _evaluate_conditions(self, conditions: list, is_entry: bool = True) -> pd.Series:
        """
        Evaluate all conditions (AND logic - all must be true).

        Returns:
            Boolean Series indicating where conditions are met
        """
        if not conditions:
            return pd.Series([False] * len(self.data), index=self.data.index)

        result = pd.Series([True] * len(self.data), index=self.data.index)

        for condition in conditions:
            cond_signal = self._evaluate_single_condition(condition)
            result = result & cond_signal

        return result

    def _evaluate_single_condition(self, condition) -> pd.Series:
        """Evaluate a single condition and return boolean Series."""
        cond_type = condition.type

        if cond_type == 'crossover':
            fast = getattr(condition, 'fast_indicator', None)
            slow = getattr(condition, 'slow_indicator', None)
            if not fast or not slow:
                raise ValueError("Crossover condition requires fast_indicator and slow_indicator")
            # Resolve indicator names to actual column names
            fast_col = self.column_mapping.get(fast, fast)
            slow_col = self.column_mapping.get(slow, slow)
            # Crossover: fast crosses above slow
            crossover = (self.data[fast_col] > self.data[slow_col]) & \
                       (self.data[fast_col].shift(1) <= self.data[slow_col].shift(1))
            return crossover

        elif cond_type == 'crossunder':
            fast = getattr(condition, 'fast_indicator', None)
            slow = getattr(condition, 'slow_indicator', None)
            if not fast or not slow:
                raise ValueError("Crossunder condition requires fast_indicator and slow_indicator")
            # Resolve indicator names to actual column names
            fast_col = self.column_mapping.get(fast, fast)
            slow_col = self.column_mapping.get(slow, slow)
            # Crossunder: fast crosses below slow
            crossunder = (self.data[fast_col] < self.data[slow_col]) & \
                        (self.data[fast_col].shift(1) >= self.data[slow_col].shift(1))
            return crossunder

        elif cond_type == 'threshold':
            indicator = getattr(condition, 'indicator', None)
            comparison = getattr(condition, 'comparison', None)
            value = getattr(condition, 'value', None)
            
            if not indicator or not comparison or value is None:
                raise ValueError("Threshold condition requires indicator, comparison, and value")

            # Resolve indicator name to actual column name
            indicator_col = self.column_mapping.get(indicator, indicator)

            if comparison == 'above':
                return self.data[indicator_col] > value
            elif comparison == 'below':
                return self.data[indicator_col] < value
            elif comparison == 'above_or_equal':
                return self.data[indicator_col] >= value
            elif comparison == 'below_or_equal':
                return self.data[indicator_col] <= value
            else:
                raise ValueError(f"Unknown comparison: {comparison}")

        else:
            raise ValueError(f"Unknown condition type: {cond_type}")

    def _extract_trades(self) -> list:
        """
        Extract individual trades from the equity curve.

        Returns:
            List of trade dictionaries
        """
        trades = []
        in_trade = False
        entry_idx = None
        entry_price = None
        entry_date = None

        for idx, row in self.data.iterrows():
            # Entry signal
            if row['signal'] == 1 and not in_trade:
                in_trade = True
                entry_idx = idx
                entry_price = row['close']
                entry_date = idx

            # Exit signal
            elif row['signal'] == 0 and in_trade:
                exit_idx = idx
                exit_price = row['close']
                exit_date = idx
                
                pnl = exit_price - entry_price
                pnl_pct = (pnl / entry_price) * 100

                trades.append({
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct
                })

                in_trade = False

        return trades
