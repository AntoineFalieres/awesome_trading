# Specification for Backtesting Engine

## Context
The Backtesting Engine validates the "TrendFlow" strategy by simulating trades on historical data. It accounts for transaction costs and tracks portfolio equity over time. It must be vectorized where possible for speed but support event-driven logic for complex exit conditions.

## Target File
`src/backtest/engine.py`

## Dependencies
* `pandas`
* `numpy`
* `src.strategies.weinstein` (or generic Strategy interface)

## Requirements

### 1. Class Structure
* **Class Name:** `Backtester`
* **Purpose:** Execute a strategy on a dataset and compute performance metrics.

### 2. Configuration (`__init__`)
* **Parameters:**
    * `strategy`: An instance of a Strategy class (e.g., `WeinsteinStrategy`).
    * `initial_capital` (float, default=10,000.0).
    * `fee_pct` (float, default=0.001): Transaction fee per trade (0.1%).

### 3. Core Logic (`run`)
* **Input:** `data` (DataFrame with OHLCV).
* **Process:**
    1.  **Generate Signals:** Call `strategy.generate_signals(data)`.
    2.  **Simulation Loop (Vectorized preference):**
        * Calculate `Market Returns` = `Close.pct_change()`.
        * Calculate `Strategy Returns` = `Market Returns` * `Signal.shift(1)` (Shifted because we trade *after* the signal is generated).
        * **Fee Adjustment:** Subtract `fee_pct` whenever `Signal` changes value (a trade occurred).
    3.  **Equity Curve:**
        * `Cumulative Returns` = `(1 + Strategy Returns).cumprod()`.
        * `Equity` = `initial_capital` * `Cumulative Returns`.
* **Output:** A DataFrame containing `Equity`, `Drawdown`, and trade logs.

### 4. Metrics Calculation (`calculate_metrics`)
* **Returns a Dictionary:**
    * `Total Return (%)`: (Final Equity - Initial) / Initial.
    * `Max Drawdown (%)`: Min(Equity / RollingMax(Equity) - 1).
    * `Win Rate`: (Count of positive trades / Total trades).
    * `Profit Factor`: (Sum of gains / Sum of losses).

### 5. Constraints
* **Look-ahead Bias:** Ensure the return calculation uses `Signal.shift(1)` so we don't use tomorrow's signal to trade today's price change.
* **Safety:** Handle cases where equity drops below zero (Bankruptcy).