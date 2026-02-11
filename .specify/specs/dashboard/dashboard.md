# Specification for TrendFlow Dashboard

## Context
This is the user interface for the "TrendFlow" application. It allows users to input a ticker symbol, adjust strategy parameters (MM30 period, volume threshold), and visualize the results interactively.

## Target File
`src/dashboard/app.py`

## Dependencies
* `streamlit`
* `plotly.graph_objects`
* `yfinance` (or `ccxt` for crypto)
* `src.strategies.weinstein` (WeinsteinStrategy)

## Requirements

### 1. Layout & Input
* **Sidebar:**
    * Text Input: "Ticker Symbol" (default: 'AAPL' or 'BTC-USD').
    * Slider: "MM30 Period" (range: 10-200, default: 30).
    * Slider: "Volume Threshold" (range: 1.0-5.0, default: 1.5).
    * Date Input: "Start Date" (default: 2 years ago).
    * Checkbox: "Show Secondary MA?" (default: False).
    * Selectbox: "Type" (Options: SMA, EMA, WMA).
    * Number Input: "Period" (default: 200).
    * Color Picker: "Color" (default: '#FF0000').    

### 2. Data Processing
* **Caching:** Use `@st.cache_data` to prevent re-downloading data on every slider change.
* **Logic:**
    1. Fetch OHLCV data using `yfinance` based on user inputs.
    2. Instantiate `WeinsteinStrategy` with the sidebar parameters.
    3. Run `strategy.generate_signals(data)` to get the processed DataFrame with `mm30`, `vol_ratio`, and `signal` columns.

### 3. Visualization (Plotly)
* **Chart 1 (Price & Trend):**
    * **Candlestick:** Open, High, Low, Close.
    * **Line:** The `mm30` column (Color: Orange).
    * **Markers:**
        * Green Triangle Up (^) at the *Low* of the candle where `signal == 1` (Buy).
        * Red Triangle Down (v) at the *High* of the candle where `signal == -1` (Sell).
    * **Conditional Layer:** If "Show Secondary MA?" is checked:
            * Instantiate `MovingAverage` with user inputs.
            * Calculate and Plot the line (Style: Dashed, User-selected Color).        
* **Chart 2 (Volume):**
    * Bar chart of Volume.
    * Overlay the `vol_ma` line.
    * Color bars red/green based on price close.

### 4. Constraints
* **Performance:** Do not plot every single candle if the dataset is huge; allow Plotly's native zooming.
* **Error Handling:** Display a `st.error` message if the ticker is invalid or data is empty.