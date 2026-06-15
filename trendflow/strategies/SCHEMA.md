# Strategy Configuration Guide

## Overview
A trading strategy in TrendFlow is defined as a JSON configuration that specifies:
1. Market data parameters (symbol, timeframe)
2. Indicators to calculate
3. Entry and exit conditions based on those indicators

## Strategy JSON Schema

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
      "params": {
        "period": 10,
        "ma_type": "sma"
      }
    },
    {
      "name": "sma_30",
      "type": "moving_average",
      "params": {
        "period": 30,
        "ma_type": "sma"
      }
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

## Supported Indicators

### Moving Average
- **Type:** `moving_average`
- **Params:**
  - `period` (int): Window size
  - `ma_type` (str): 'sma', 'ema', or 'wma'

### Volume
- **Type:** `volume`
- **Params:**
  - `period` (int, optional): Window size for volume MA (default: 30)

### RSI (Relative Strength Index)
- **Type:** `rsi`
- **Params:**
  - `period` (int): Window size (default: 14)

### MACD
- **Type:** `macd`
- **Params:**
  - `fast` (int): Fast EMA period (default: 12)
  - `slow` (int): Slow EMA period (default: 26)
  - `signal` (int): Signal line EMA period (default: 9)

## Supported Conditions

### Crossover
Entry/exit when fast indicator crosses above slow indicator.
```json
{
  "type": "crossover",
  "fast_indicator": "sma_10",
  "slow_indicator": "sma_30"
}
```

### Crossunder
Entry/exit when fast indicator crosses below slow indicator.
```json
{
  "type": "crossunder",
  "fast_indicator": "sma_10",
  "slow_indicator": "sma_30"
}
```

### Threshold
Entry/exit when indicator exceeds a threshold.
```json
{
  "type": "threshold",
  "indicator": "rsi_14",
  "comparison": "above",
  "value": 70
}
```

### Multiple Conditions
All conditions must be True (AND logic).
```json
"entry_conditions": [
  {
    "type": "crossover",
    "fast_indicator": "sma_10",
    "slow_indicator": "sma_30"
  },
  {
    "type": "threshold",
    "indicator": "rsi_14",
    "comparison": "below",
    "value": 80
  }
]
```

## Example Strategies

### Multi-Indicator Strategy
```json
{
  "name": "MA + RSI Strategy",
  "description": "Buy on MA crossover if RSI < 70, sell if RSI > 30 or MA crossunder",
  "symbol": "BTC-USD",
  "start_date": "2023-06-01",
  "end_date": "2024-06-01",
  "indicators": [
    {
      "name": "sma_20",
      "type": "moving_average",
      "params": {"period": 20, "ma_type": "sma"}
    },
    {
      "name": "sma_50",
      "type": "moving_average",
      "params": {"period": 50, "ma_type": "sma"}
    },
    {
      "name": "rsi_14",
      "type": "rsi",
      "params": {"period": 14}
    }
  ],
  "entry_conditions": [
    {"type": "crossover", "fast_indicator": "sma_20", "slow_indicator": "sma_50"},
    {"type": "threshold", "indicator": "rsi_14", "comparison": "below", "value": 70}
  ],
  "exit_conditions": [
    {"type": "crossunder", "fast_indicator": "sma_20", "slow_indicator": "sma_50"},
    {"type": "threshold", "indicator": "rsi_14", "comparison": "above", "value": 80}
  ],
  "backtest_params": {
    "initial_capital": 10000,
    "commission": 0.001
  }
}
```
