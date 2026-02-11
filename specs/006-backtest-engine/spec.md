# Feature Specification: Backtest Engine

**Feature Branch**: `006-backtest-engine`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Implement `src/backtest/engine.py` based on @.specify/specs/backtesting/backtest_engine.md Requirements: 1. Implement the `Backtester` class with a focus on vectorized return calculations (using `pandas.pct_change()` and `shift()`). 2. Include the `calculate_metrics` method to return a dictionary of: Total Return, Max Drawdown, and Win Rate. 3. Strictly follow the @.specify/memory/constitution.md : Use type hints, handle division by zero in metrics, and ensure no look-ahead bias."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analyst can backtest a trading strategy (Priority: P1)

As a quantitative analyst, I want to run a backtest on a trading strategy using historical data, so that I can evaluate its historical performance.

**Why this priority**: Backtesting is the fundamental method for assessing the viability of a trading strategy.

**Independent Test**: An analyst can provide a DataFrame containing prices and trading signals to the `Backtester`, run the backtest, and receive a set of performance metrics.

**Acceptance Scenarios**:

1. **Given** a DataFrame with price data and a 'signal' column, **When** an analyst runs the `Backtester`, **Then** the system calculates the strategy's returns.
2. **Given** a completed backtest, **When** the analyst requests performance metrics, **Then** a dictionary containing 'Total Return', 'Max Drawdown', and 'Win Rate' is returned.
3. **Given** a strategy with no winning trades, **When** calculating metrics, **Then** the 'Win Rate' is correctly reported as 0 and no division-by-zero error occurs.
4. **Given** the input data, **When** the backtest is running, **Then** there is no look-ahead bias in the return calculation (i.e., returns are calculated based on the signal from the *previous* period).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a `Backtester` class in `trendflow/backtest/engine.py`.
- **FR-002**: The `Backtester` class MUST have a `run` method that takes a DataFrame with price and signal data and returns a DataFrame with strategy returns.
- **FR-003**: The `run` method MUST calculate daily returns in a vectorized manner, avoiding loops.
- **FR-004**: The calculation of strategy returns MUST be shifted to prevent look-ahead bias.
- **FR-005**: The `Backtester` class MUST have a `calculate_metrics` method that returns a dictionary of key performance indicators.
- **FR-006**: The `calculate_metrics` method MUST compute the 'Total Return' of the strategy.
- **FR-007**: The `calculate_metrics` method MUST compute the 'Max Drawdown' of the strategy's equity curve.
- **FR-008**: The `calculate_metrics` method MUST compute the 'Win Rate' (percentage of trades with positive returns).
- **FR-009**: The 'Win Rate' calculation MUST safely handle cases with zero total trades.
- **FR-010**: All methods in the `Backtester` class MUST be fully type-hinted.

### Key Entities *(include if feature involves data)*

- **Backtester**: An engine responsible for simulating a trading strategy over historical data and calculating its performance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `Backtester` correctly calculates Total Return, Max Drawdown, and Win Rate for a strategy with a known, pre-calculated outcome.
- **SC-002**: The backtesting process for a dataset with 1 million rows completes in under 5 seconds.
- **SC-003**: The calculated metrics match results from a trusted third-party backtesting library for a simple strategy.
- **SC-004**: Code coverage for `trendflow/backtest/engine.py` is at least 90%.
