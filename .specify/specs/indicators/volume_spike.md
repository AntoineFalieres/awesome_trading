# Specification for Volume Analysis Indicator

## Context
Volume confirms trends. In the "TrendFlow" strategy (Weinstein), a "Stage 2" breakout requires volume to be significantly higher than the recent average (typically 1.5x to 2x). This indicator calculates the Volume Moving Average (VMA) and the Relative Volume ratio.

## Target File
`src/indicators/volume.py`

## Dependencies
* `src/indicators/base.py` (Inherits from `Indicator`)
* `pandas`

## Requirements

### 1. Class Structure
* **Class Name:** `VolumeStats`
* **Parent:** `Indicator`

### 2. Configuration (`__init__`)
* **Parameters:**
    * `period` (int, default=20): The lookback window for the average.
    * `method` (str, default='sma'): Type of average ('sma' or 'ema').

### 3. Implementation Logic (`calculate`)
* **Input Validation:**
    * Ensure `volume` column exists in the DataFrame.
    * Check for and handle `0` volume (common in crypto data gaps) to avoid division by zero errors later.
* **Calculations:**
    1.  **Volume MA:** Calculate the Simple Moving Average (SMA) of the `volume` column over `period`.
    2.  **Relative Volume (RVol):** Divide the *current* volume by the *Volume MA*.
        * $RVol = \frac{Volume_t}{SMA(Volume)_t}$
* **Output:**
    * Return a DataFrame with two columns:
        * `vol_ma`: The moving average values.
        * `vol_ratio`: The relative volume ratio (e.g., 1.5 means 50% above average).

### 4. Visualization Metadata
* **Plot 1:** Volume Bars (Main chart, separate pane).
* **Plot 2:** `vol_ma` Line (Overlay on volume pane).
* **Threshold:** A horizontal line at `vol_ratio = 1.0` or `1.5` to visualize spikes.

### 5. Constraints
* **Constitution Check:** Do not iterate rows. Use `df['volume'].rolling(window=period).mean()` for vectorization.