# TrendFlow - Trading Strategy Backtesting Platform

A Python-based web application for backtesting trading strategies on real market data. Test your trading ideas before risking real capital.

## Features

- 📊 **Multiple Technical Indicators**
  - Moving Averages (SMA, EMA, WMA with customizable periods)
  - Volume Analysis
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Easily extensible for custom indicators

- 🔄 **Flexible Strategy Rules**
  - Define entry conditions (crossovers, thresholds)
  - Define exit conditions with AND logic
  - Test complex multi-indicator strategies

- 💾 **Strategy Persistence**
  - Save strategies as JSON files
  - Load and rerun previous strategies
  - Compare results across different configurations

- 📈 **Comprehensive Performance Metrics**
  - Total Return & Annualized Return
  - Sharpe Ratio & Sortino Ratio
  - Maximum Drawdown
  - Win Rate & Trade Statistics
  - Comparison to Buy & Hold strategy

- 🎨 **Interactive Web Interface**
  - Built with Streamlit for easy use
  - No coding required
  - Visual charts with Plotly
  - Real-time backtest execution

## Installation

### Requirements
- Python 3.8+
- pip or uv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/awesome_trading.git
cd awesome_trading
```

2. Install dependencies:
```bash
pip install -e .
```

Or with uv:
```bash
uv pip install -e .
```

3. Run the web app:
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## Quick Start

### 1. Create a Strategy

1. Go to **Strategy Editor** → **Create New Strategy**
2. Configure your strategy:
   - **Name**: Give your strategy a name (e.g., "MA Crossover 10-30")
   - **Symbol**: Stock ticker or crypto symbol (e.g., AAPL, BTC-USD)
   - **Date Range**: Historical period to backtest
   - **Indicators**: Add the technical indicators you want
   - **Entry Conditions**: When to buy (e.g., 10-day MA crosses above 30-day MA)
   - **Exit Conditions**: When to sell
3. Click **Create Strategy** to save

### 2. Run a Backtest

1. Go to **View Results**
2. Select your strategy from the dropdown
3. Click **Run Backtest**
4. Review the performance metrics and charts

### 3. Analyze Results

View comprehensive metrics including:
- **Equity Curve**: Visual representation of account growth
- **Drawdown Analysis**: How much the strategy declined from peak
- **Trade-by-Trade Breakdown**: Individual trade details
- **Returns Distribution**: Histogram of daily returns
- **Summary Statistics**: Detailed performance metrics

## Architecture

### Project Structure

```
trendflow/
├── indicators/          # Technical indicator implementations
│   ├── base.py         # Base Indicator class
│   ├── ma.py           # Moving Average
│   ├── volume.py       # Volume Stats
│   ├── rsi.py          # Relative Strength Index
│   └── macd.py         # MACD
├── data/               # Market data handling
│   ├── fetcher.py      # yfinance wrapper
│   └── cache.py        # Data caching
├── backtest/           # Backtesting engine
│   └── engine.py       # Backtester class
├── strategies/         # Strategy management
│   ├── strategy.py     # Strategy model & StrategyManager
│   ├── executor.py     # Strategy execution engine
│   └── SCHEMA.md       # Strategy JSON schema
└── __init__.py

pages/                  # Streamlit pages
├── strategy_editor.py  # Strategy creation UI
├── results_viewer.py   # Results visualization
└── __init__.py

main.py                 # Main Streamlit app
```

### Key Classes

**Strategy** (`trendflow.strategies.Strategy`)
- Represents a trading strategy configuration
- JSON serializable for persistence
- Validates configuration before execution

**StrategyManager** (`trendflow.strategies.StrategyManager`)
- Handles saving/loading strategies from JSON files
- List, delete, and retrieve saved strategies

**StrategyExecutor** (`trendflow.strategies.StrategyExecutor`)
- Executes a strategy against historical data
- Returns detailed backtest results with metrics

**Backtester** (`trendflow.backtest.Backtester`)
- Vectorized backtesting engine
- Calculates comprehensive performance metrics
- Supports commission and capital management

**DataCache** (`trendflow.data.DataCache`)
- Local caching of market data
- Reduces API calls and improves performance
- Customizable cache TTL

## Supported Indicators

### Moving Average
```json
{
  "name": "sma_10",
  "type": "moving_average",
  "params": {
    "period": 10,
    "ma_type": "sma"
  }
}
```
- **ma_type**: "sma" (Simple), "ema" (Exponential), "wma" (Weighted)

### Volume
```json
{
  "name": "volume_stats",
  "type": "volume",
  "params": {"period": 30}
}
```

### RSI (Relative Strength Index)
```json
{
  "name": "rsi_14",
  "type": "rsi",
  "params": {"period": 14}
}
```

### MACD
```json
{
  "name": "macd",
  "type": "macd",
  "params": {
    "fast": 12,
    "slow": 26,
    "signal": 9
  }
}
```

## Strategy Configuration

Strategies are stored as JSON files. See `trendflow/strategies/SCHEMA.md` for the complete schema.

### Example Strategy: MA Crossover

```json
{
  "name": "Simple MA Crossover",
  "description": "Buy when 10-day MA crosses above 30-day MA",
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "indicators": [
    {
      "name": "sma_10",
      "type": "moving_average",
      "params": {"period": 10, "ma_type": "sma"}
    },
    {
      "name": "sma_30",
      "type": "moving_average",
      "params": {"period": 30, "ma_type": "sma"}
    }
  ],
  "entry_conditions": [
    {
      "type": "crossover",
      "fast_indicator": "sma_10",
      "slow_indicator": "sma_30"
    }
  ],
  "exit_conditions": [
    {
      "type": "crossunder",
      "fast_indicator": "sma_10",
      "slow_indicator": "sma_30"
    }
  ],
  "backtest_params": {
    "initial_capital": 10000,
    "commission": 0.001
  }
}
```

## Condition Types

### Crossover
Fast indicator crosses above slow indicator.
```json
{"type": "crossover", "fast_indicator": "sma_10", "slow_indicator": "sma_30"}
```

### Crossunder
Fast indicator crosses below slow indicator.
```json
{"type": "crossunder", "fast_indicator": "sma_10", "slow_indicator": "sma_30"}
```

### Threshold
Indicator value exceeds a threshold.
```json
{
  "type": "threshold",
  "indicator": "rsi_14",
  "comparison": "above",
  "value": 70
}
```

Comparisons: "above", "below", "above_or_equal", "below_or_equal"

## Python API

You can also use TrendFlow programmatically:

```python
from trendflow.strategies import Strategy, StrategyManager, StrategyExecutor

# Load a strategy
manager = StrategyManager()
strategy = manager.load("MA Crossover")

# Execute the backtest
executor = StrategyExecutor(strategy)
results = executor.execute()

# Access results
metrics = results['metrics']
trades = results['trades']
data = results['data']

print(f"Total Return: {metrics['Total Return']:.2%}")
print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
print(f"Number of Trades: {metrics['Total Trades']}")
```

## Performance Metrics Explained

- **Total Return**: Overall percentage gain/loss from initial capital
- **Annualized Return**: Projected annual return based on backtest period
- **Annualized Volatility**: Standard deviation of daily returns (annualized)
- **Sharpe Ratio**: Risk-adjusted return (higher is better, >1.0 is good)
- **Sortino Ratio**: Similar to Sharpe but only penalizes downside volatility
- **Max Drawdown**: Largest peak-to-trough decline during the period
- **Win Rate**: Percentage of profitable trades
- **Buy & Hold Return**: Performance if strategy just held the asset
- **Excess Return**: Strategy return minus buy & hold return

## Custom Indicators

To add a custom indicator:

1. Create a new file in `trendflow/indicators/` (e.g., `my_indicator.py`)
2. Inherit from `Indicator` base class
3. Implement the `calculate()` method
4. Export from `__init__.py`

Example:

```python
from trendflow.indicators import Indicator
import pandas as pd

class BollingerBands(Indicator):
    def __init__(self, period: int = 20, std_dev: int = 2):
        self.period = period
        self.std_dev = std_dev

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        sma = data['close'].rolling(self.period).mean()
        std = data['close'].rolling(self.period).std()
        
        data['BB_Upper'] = sma + (std * self.std_dev)
        data['BB_Middle'] = sma
        data['BB_Lower'] = sma - (std * self.std_dev)
        
        return data
```

## Data Sources

- **Stocks**: Yahoo Finance (via yfinance)
- **Cryptocurrencies**: Yahoo Finance (e.g., BTC-USD, ETH-USD)
- **Forex**: Yahoo Finance (e.g., EURUSD=X)

Data is cached locally in `.cache/market_data/` to speed up subsequent runs.

## Limitations & Considerations

- **Backtesting Limitations**: Past performance doesn't guarantee future results
- **Slippage & Execution**: Backtester uses closing prices; real trading includes slippage
- **Survivorship Bias**: Only tests on current/surviving securities
- **Look-Ahead Bias**: Signals are generated on closing price (no intraday execution)
- **Data Quality**: Dependent on yfinance data quality

## Troubleshooting

### "No data found for ticker"
- Verify the ticker symbol is correct (e.g., AAPL for Apple)
- For crypto, use format like BTC-USD, ETH-USD
- Check the date range is valid

### "Strategy validation failed"
- Ensure all indicators referenced in conditions are defined
- Check indicator names match exactly (case-sensitive)
- Verify all conditions have required fields

### "Failed to calculate indicators"
- Ensure you have at least 2-3 months of data for proper indicator calculation
- Check for missing OHLCV data in the date range

### Poor backtest results
- Optimize parameters (moving average periods, RSI levels, etc.)
- Consider different date ranges
- Test multiple indicators together

## Performance Tips

1. **Use data caching** to speed up repeated backtests
2. **Limit indicators** to only what's necessary
3. **Extend date range** for more robust results
4. **Test multiple timeframes** before deploying

## Future Enhancements

- [ ] Additional indicators (Bollinger Bands, Stochastic, ATR)
- [ ] Multiple timeframe analysis
- [ ] Portfolio-level backtesting
- [ ] Parameter optimization (grid search, genetic algorithms)
- [ ] Real-time strategy monitoring
- [ ] Walk-forward analysis
- [ ] Monte Carlo simulation
- [ ] Cloud storage for strategies
- [ ] Community strategy sharing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for **educational and research purposes only**. Past performance does not guarantee future results. Trading and investing involve risk. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy backtesting! 📈**