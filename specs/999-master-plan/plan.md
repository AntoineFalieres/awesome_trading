# Master Implementation Plan: TrendFlow Application

**Branch**: `999-master-plan`
**Objective**: This document outlines the comprehensive, phased implementation plan for the entire TrendFlow application, consolidating all feature specifications into a single, cohesive development roadmap.

---

## **Phase 1: Foundational Setup & Core Abstractions**

**Goal**: Establish the project's structure and the core `Indicator` abstraction. This is the bedrock for all subsequent development.

**Tasks**:
1.  **Initialize Project Structure**:
    - Create directories: `trendflow/`, `trendflow/indicators/`, `trendflow/strategies/`, `trendflow/backtest/`, `trendflow/dashboard/`, `trendflow/data/`.
    - Create `requirements.txt` with initial dependencies: `pandas`, `numpy`, `yfinance`, `plotly`, `streamlit`.

2.  **Implement `Indicator` Abstract Base Class**:
    - **File**: `trendflow/indicators/base.py`
    - **Specification**: `specs/001-indicator-base-class/spec.md`
    - **Implementation Details**:
        - Create an abstract class `Indicator` using `abc.ABC`.
        - Define the abstract method `calculate(self, data: pd.DataFrame) -> pd.DataFrame`.
        - Implement the `name` property to return the class name.
        - Ensure all methods have strict type hints.

---

## **Phase 2: Indicator Library Implementation**

**Goal**: Build the library of technical indicators that will be used by the strategies.

**Tasks**:
1.  **Implement `MM30Indicator`**:
    - **File**: `trendflow/indicators/mm30.py`
    - **Specification**: `specs/002-mm30-indicator/spec.md`
    - **Implementation Details**:
        - Inherit from `Indicator`.
        - Implement the `calculate` method to compute a 30-period weighted moving average on the 'close' price using `numpy`.

2.  **Implement `VolumeStats` Indicator**:
    - **File**: `trendflow/indicators/volume.py`
    - **Specification**: `specs/003-volume-stats-indicator/spec.md`
    - **Implementation Details**:
        - Inherit from `Indicator`.
        - Implement `calculate` to compute `vol_ma` (volume simple moving average) and `vol_ratio` (volume / vol_ma).
        - Use vectorized pandas operations and handle potential division by zero by replacing `inf` with `NaN` or 0.

3.  **Implement Generic `MovingAverage` Indicator**:
    - **File**: `trendflow/indicators/ma.py`
    - **Specification**: `specs/007-generic-moving-average/spec.md`
    - **Implementation Details**:
        - Inherit from `Indicator`.
        - The `__init__` method will take `period: int` and `ma_type: str` ('sma', 'ema', 'wma').
        - The `calculate` method will use a switch or if/elif/else structure to call the correct vectorized pandas function (`.rolling().mean()`, `.ewm().mean()`, etc.).
        - Raise a `ValueError` for invalid `ma_type`.

---

## **Phase 3: Strategy Engine Development**

**Goal**: Implement the core trading strategy with its full feature set.

**Tasks**:
1.  **Implement `WeinsteinStrategy`**:
    - **File**: `trendflow/strategies/weinstein.py`
    - **Specification**: `specs/004-weinstein-strategy/spec.md`
    - **Implementation Details**:
        - **Part A (Base + Risk Management)**:
            - Create the `WeinsteinStrategy` class. The `__init__` should accept `stop_loss_pct` and `take_profit_pct`.
            - The `generate_signals` method will first calculate the base entry condition (close > MM30 & volume spike) in a vectorized way.
            - Implement a stateful `for` loop to iterate through the data, track `in_position` state and `entry_price`.
            - Inside the loop, check for stop-loss and take-profit conditions based on the 'Low' and 'High' prices. Generate 'Sell' signals (-1) and populate the `exit_reason` column.
        - **Part B (Trend Filter Integration)**:
            - Update the `__init__` to accept `use_trend_filter`, `long_ma_period`, and `long_ma_type`.
            - In `generate_signals`, *before* the stateful loop, calculate the long-term MA if the filter is enabled.
            - Create a final, combined boolean mask for entry signals (`base_entry_condition & trend_filter_condition`).
            - The stateful loop from Part A will now use this final, filtered condition to trigger new entries. The loop's internal logic does not need to change.

---

## **Phase 4: Backtesting & Validation**

**Goal**: Create the engine to simulate the strategy and measure its performance.

**Tasks**:
1.  **Implement `Backtester` Engine**:
    - **File**: `trendflow/backtest/engine.py`
    - **Specification**: `specs/006-backtest-engine/spec.md`
    - **Implementation Details**:
        - Create the `Backtester` class with `run` and `calculate_metrics` methods.
        - The `run` method will calculate strategy returns vectorially, ensuring to `shift()` the signals by 1 to prevent look-ahead bias (`strategy_returns = data['close'].pct_change() * data['signal'].shift(1)`).
        - The `calculate_metrics` method will compute 'Total Return' (`.prod()`), 'Max Drawdown', and 'Win Rate' from the strategy returns, safely handling cases with zero trades.

---

## **Phase 5: User Interface**

**Goal**: Build the interactive front-end for visualizing the strategy.

**Tasks**:
1.  **Implement `StrategyDashboard`**:
    - **File**: `trendflow/dashboard/app.py`
    - **Specification**: `specs/005-strategy-dashboard/spec.md`
    - **Implementation Details**:
        - Use `streamlit` for the main app layout and sidebar controls.
        - Add a ticker input widget.
        - Use `@st.cache_data` for the data fetching function.
        - Instantiate and run the `WeinsteinStrategy` and `Backtester`.
        - Use `plotly.graph_objects` to create a subplot figure (Candlestick + Volume).
        - Plot buy/sell signals as markers on the price chart.
        - Add sidebar controls for the secondary moving average (checkbox, period, type) and conditionally plot it on the chart.

---

## **Phase 6: Final Integration & Verification**

**Goal**: Ensure all parts of the application work together correctly.

**Tasks**:
1.  **End-to-End Test**: Run the dashboard application (`streamlit run trendflow/dashboard/app.py`).
2.  **Full Backtest**: Select a ticker (e.g., 'AAPL'), enable all features (trend filter, secondary MA), and verify that the chart renders correctly without errors and that performance metrics are displayed.
3.  **Code Review & Refactoring**: Perform a final review to ensure adherence to the constitution and overall code quality.
