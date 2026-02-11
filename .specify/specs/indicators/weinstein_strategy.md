# Specification for Weinstein Stage Analysis Strategy (with Trend Filter)

## Context
This module implements Stan Weinstein's "Stage Analysis" strategy. It combines trend direction (MM30) with momentum validation (Volume).
**Update:** It now supports an optional **Secondary Trend Filter** (e.g., 200 SMA). If enabled, buy signals are only generated if the price is *also* above this long-term average, filtering out counter-trend trades.

## Target File
`src/strategies/weinstein.py`

## Dependencies
* `src.indicators.mm30` (MM30Indicator)
* `src.indicators.volume` (VolumeStats)
* `src.indicators.ma` (MovingAverage)  <-- New Dependency
* `pandas`
* `numpy`

## Requirements

### 1. Class Structure
* **Class Name:** `WeinsteinStrategy`

### 2. Configuration (`__init__`)
* **Parameters:**
    * `mm30_period` (int, default=30): Primary trend.
    * `vol_period` (int, default=20): Volume baseline.
    * `vol_threshold` (float, default=1.5): Breakout strength.
    * `stop_loss_pct` (float, default=0.05): Risk management.
    * `take_profit_pct` (float, default=0.20): Target.
    * **New:** `use_trend_filter` (bool, default=False): Enable/Disable long-term filter.
    * **New:** `trend_filter_type` (str, default='sma'): Type of long-term MA.
    * **New:** `trend_filter_period` (int, default=200): Period of long-term MA.

### 3. Core Logic (`generate_signals`)
* **Input:** OHLCV DataFrame.
* **Process:**
    1.  **Primary Indicators:** Calculate `mm30` and `vol_ratio`.
    2.  **Secondary Indicator (Conditional):**
        * If `use_trend_filter` is True:
            * Instantiate `MovingAverage(trend_filter_period, trend_filter_type)`.
            * Calculate `long_term_ma`.
        * If False:
            * Create a dummy series of `True` (or 0) to bypass the check.
    3.  **Entry Logic (Vectorized):**
        * **Base:** `Close` crosses *above* `MM30` AND `MM30` rising AND `vol_ratio` > `vol_threshold`.
        * **Filter:** AND (`Close` > `long_term_ma` if enabled).
    4.  **Risk Management Loop:**
        * (Retain the existing Stop Loss / Take Profit loop from v2).
        * Ensure the `entry_price` logic respects the new filtered entry signal.

### 4. Constraints
* **Defaults:** The filter should be *off* by default to preserve original behavior.
* **Efficiency:** Only calculate the 200 MA if `use_trend_filter` is True.