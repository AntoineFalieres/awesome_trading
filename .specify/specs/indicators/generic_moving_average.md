# Specification for Generic Moving Average Indicator

## Context
Traders need flexibility to add multiple moving averages (SMA, EMA, WMA) with custom periods to their charts for trend context (e.g., 50 SMA, 200 EMA). This class provides a reusable factory for these calculations.

## Target File
`src/indicators/ma.py`

## Dependencies
* `src.indicators.base` (Inherits from Indicator)
* `pandas`
* `numpy`

## Requirements

### 1. Class Structure
* **Class Name:** `MovingAverage`
* **Parent:** `Indicator`

### 2. Configuration (`__init__`)
* **Parameters:**
    * `period` (int): The lookback window (e.g., 50, 200).
    * `ma_type` (str): One of 'sma' (Simple), 'ema' (Exponential), or 'wma' (Weighted).
    * `source` (str, default='close'): Column to average.

### 3. Logic (`calculate`)
* **Validation:** Check input data exists.
* **Algorithm:**
    * **If 'sma':** Use `df[source].rolling(period).mean()`.
    * **If 'ema':** Use `df[source].ewm(span=period).mean()`.
    * **If 'wma':** Use the weighted logic defined in `mm30.spec` (using `numpy` or `apply`).
* **Output:**
    * Return a Series named `ma_{period}_{type}` (e.g., `ma_50_sma`).

### 4. Constraints
* **Vectorization:** Strict adherence to pandas vectorized functions.
* **Error Handling:** Raise `ValueError` if an invalid `ma_type` is passed.