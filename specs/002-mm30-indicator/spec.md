# Feature Specification: MM30 Indicator

**Feature Branch**: `002-mm30-indicator`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Implement `src/indicators/mm30.py` based on @.specify/specs/mm30.md Critical Requirements: 1. Ensure `MM30Indicator` inherits strictly from the `Indicator` base class you just created. 2. Use `numpy` for the Weighted Average calculation inside the rolling window to ensure performance (no pure Python loops). 3. Include type hints as per the Constitution."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer can use the MM30 indicator (Priority: P1)

As a developer, I want to use the `MM30Indicator` to calculate the 30-period weighted moving average on a given dataset, so that I can incorporate this indicator into trading strategies.

**Why this priority**: This is the primary function of the `mm30-indicator` feature.

**Independent Test**: A developer can instantiate the `MM30Indicator` and call its `calculate` method with a pandas DataFrame, receiving a DataFrame with the calculated MM30 values.

**Acceptance Scenarios**:

1. **Given** a pandas DataFrame with 'close' prices, **When** a developer calls `MM30Indicator().calculate(df)`, **Then** the returned DataFrame contains a new column 'MM30' with the calculated weighted moving average.
2. **Given** a pandas DataFrame without a 'close' column, **When** `MM30Indicator().calculate(df)` is called, **Then** a `KeyError` is raised.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a class `MM30Indicator` in `trendflow/indicators/mm30.py`.
- **FR-002**: `MM30Indicator` MUST inherit from the `Indicator` base class.
- **FR-003**: `MM30Indicator` MUST implement the `calculate` method.
- **FR-004**: The `calculate` method MUST compute a 30-period weighted moving average on the 'close' price.
- **FR-005**: The weighted average calculation MUST be performed using `numpy` for efficiency.
- **FR-006**: All methods in `MM30Indicator` MUST include PEP-484 type hints.

### Key Entities *(include if feature involves data)*

- **MM30Indicator**: A specific type of `Indicator` that calculates a 30-period weighted moving average.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `calculate` method execution time for 1 million data points is under 1 second.
- **SC-002**: The `MM30Indicator` class is successfully integrated into the backtesting engine and can be used in a strategy.
- **SC-003**: Code coverage for `trendflow/indicators/mm30.py` is at least 90%.
