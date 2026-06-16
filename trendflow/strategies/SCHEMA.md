# Strategy Configuration Guide

## Overview
A trading strategy in TrendFlow is defined as JSON that specifies:
1. Market data parameters (symbol, timeframe)
2. Indicators to calculate
3. Directional rules for long and short positions

The `indicators` array supports as many entries as you need.

## Directional condition fields

- `long_entry_conditions`
- `long_exit_conditions`
- `short_entry_conditions`
- `short_exit_conditions`

Each condition array uses AND logic across entries.

Legacy fields are still accepted for backward compatibility:
- `entry_conditions` → treated as `long_entry_conditions`
- `exit_conditions` → treated as `long_exit_conditions`

## Strategy JSON Schema (directional)

```json
{
  "name": "MA Futures Long Short",
  "description": "Trade both long and short signals",
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
  "long_entry_conditions": [
    {
      "type": "crossover",
      "fast_indicator": "sma_10",
      "slow_indicator": "sma_30"
    }
  ],
  "long_exit_conditions": [
    {
      "type": "crossunder",
      "fast_indicator": "sma_10",
      "slow_indicator": "sma_30"
    }
  ],
  "short_entry_conditions": [
    {
      "type": "crossunder",
      "fast_indicator": "sma_10",
      "slow_indicator": "sma_30"
    }
  ],
  "short_exit_conditions": [
    {
      "type": "crossover",
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
  - `ma_type` (str): `sma`, `ema`, or `wma`

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
Indicator value compared to a threshold.
```json
{
  "type": "threshold",
  "indicator": "rsi_14",
  "comparison": "above",
  "value": 70
}
```

Comparisons: `above`, `below`, `above_or_equal`, `below_or_equal`
