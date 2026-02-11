# Feature Specification: Weinstein Strategy with Trend Filter and Risk Management

**Feature Branch**: `004-weinstein-strategy`
**Created**: 2026-02-11
**Status**: In Progress
**Input**: User description: "Update `src/strategies/weinstein.py` based on @.specify/specs/indicators/weinstein_strategy.md Requirements: 1. Import `MovingAverage` from `src.indicators.ma`. 2. Update `__init__` to accept the new `trend_filter` arguments. 3. In `generate_signals`, add the logic: `if self.use_trend_filter: long_ma = ...`. 4. Combine the boolean masks: `entry_signal = (base_entry) & (close > long_ma)`. 5. Strictly maintain the existing Risk Management loop; do not break the Stop Loss logic."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analyst can apply the Weinstein Strategy with risk management (Priority: P1)

As a quantitative analyst, I want to apply the Weinstein trading strategy with configurable stop-loss and take-profit levels to historical price data, so I can backtest its performance with risk management rules.

**Why this priority**: This enhances the strategy's realism and allows for more robust backtesting.

**Independent Test**: An analyst can apply the `WeinsteinStrategy` with stop-loss/take-profit percentages and get back a DataFrame containing `signal` and `exit_reason` columns.

**Acceptance Scenarios**:

1. **Given** a buy signal is generated, **When** the price subsequently drops by the `stop_loss_pct`, **Then** a sell signal (-1) is generated and the `exit_reason` is 'Stop Loss'.
2. **Given** a position is open, **When** the intraday 'Low' price breaches the stop-loss level, **Then** a sell signal (-1) is generated for that period with an `exit_reason` of 'Stop Loss'.

---

### User Story 2 - Analyst can add a long-term trend filter (Priority: P2)

As a quantitative analyst, I want to add an optional long-term moving average as a trend filter to the Weinstein strategy, so that I only take buy signals when the price is also above this long-term average.

**Why this priority**: This allows for a stricter trend-following approach, potentially reducing false signals in a bear market.

**Independent Test**: An analyst can enable the trend filter and provide a period for the long-term MA. The strategy should only generate buy signals that meet both the base Weinstein criteria and the trend filter condition.

**Acceptance Scenarios**:

1. **Given** the trend filter is enabled with a 200-period SMA, **When** a base Weinstein buy signal occurs but the price is below the 200-period SMA, **Then** no buy signal (0) is generated.
2. **Given** the trend filter is enabled with a 200-period SMA, **When** a base Weinstein buy signal occurs and the price is above the 200-period SMA, **Then** a buy signal (1) is generated.
3. **Given** the trend filter is disabled, **When** a base Weinstein buy signal occurs, **Then** a buy signal (1) is generated, regardless of the long-term trend.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `WeinsteinStrategy` constructor (`__init__`) MUST be updated to accept `use_trend_filter: bool`, `long_ma_period: int`, and `long_ma_type: str`.
- **FR-002**: The `generate_signals` method MUST import and use the generic `MovingAverage` indicator.
- **FR-003**: If `use_trend_filter` is `True`, the `generate_signals` method MUST calculate a long-term moving average based on the provided period and type.
- **FR-004**: The base entry signal conditions (price > MM30, volume spike) MUST be combined with the trend filter condition (price > long-term MA) if the filter is enabled.
- **FR-005**: The final buy signal (1) MUST only be generated if both the base conditions and the optional trend filter condition are met.
- **FR-006**: The existing stateful loop for tracking `entry_price` and calculating stop-loss/take-profit exits MUST be preserved and operate on the final, filtered entry signals.
- **FR-007**: All new parameters and logic MUST be fully type-hinted and documented.

### Key Entities *(include if feature involves data)*

- **WeinsteinStrategy**: A trading strategy that generates buy/sell signals, now with optional trend-filtering capabilities in addition to stateful risk management.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `generate_signals` method correctly filters buy signals based on the long-term trend filter when enabled.
- **SC-002**: When the trend filter is disabled, the strategy's output is identical to the previous version (before this update).
- **SC-003**: The existing stop-loss and take-profit logic continues to function correctly on the filtered signals.
- **SC-004**: Code coverage for `trendflow/strategies/weinstein.py` remains at or above 90%.
