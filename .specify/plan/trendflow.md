# TrendFlow Execution Plan

## Phase 1: Foundation & Infrastructure
1. **Scaffold Project Structure**
   - [ ] Create directory structure `src/indicators`, `src/strategies`, `src/backtest`, `src/dashboard`.
   - [ ] Create `requirements.txt` with `pandas`, `numpy`, `yfinance`, `plotly`, `streamlit`.
   - [ ] Create `constitution.md` to enforce coding standards.

2. **Core Abstract Base Class**
   - [ ] Implement `src/indicators/base.py` based on `indicator_base.spec`.
     - *Focus:* Abstract `calculate` method, `validate_input`, and `sanitize_output`.

## Phase 2: Indicator Library
3. **Generic Moving Average Factory**
   - [ ] Implement `src/indicators/ma.py` based on `generic_ma.spec`.
     - *Focus:* Factory logic for SMA, EMA, and WMA (Weighted).

4. **Volume Analysis Indicator**
   - [ ] Implement `src/indicators/volume.py` based on `volume_spike.spec`.
     - *Focus:* Vectorized calculation of Volume MA and Relative Volume Ratio.

## Phase 3: Strategy Engine
5. **Weinstein Strategy Implementation**
   - [ ] Implement `src/strategies/weinstein.py` based on `weinstein_strategy.spec` (v3).
     - *Focus:*
       - Import `MovingAverage` and `VolumeStats`.
       - Implement `generate_signals` with entry logic (Close > MM30 + Vol).
       - Implement risk management loop (Stop Loss / Take Profit).
       - Implement trend filter logic (200 SMA check).

## Phase 4: Validation Engine
6. **Backtesting Engine**
   - [ ] Implement `src/backtest/engine.py` based on `backtest_engine.spec` (v2).
     - *Focus:* Event-driven loop to check `Low` vs Stop Loss and calculate Equity Curve / Drawdown.

## Phase 5: User Interface
7. **Interactive Dashboard**
   - [ ] Implement `src/dashboard/app.py` based on `dashboard.spec`.
     - *Focus:*
       - Streamlit Sidebar for Strategy Parameters (MM30, Stop Loss, Trend Filter).
       - Plotly Subplots (Candlestick + Volume).
       - Integration of Backtest Engine results.

## Phase 6: Final Verification
8. **Sanity Check**
   - [ ] Run `python -m src.dashboard.app` to verify the UI loads.
   - [ ] Perform a test backtest on 'AAPL' to ensure no division-by-zero errors.