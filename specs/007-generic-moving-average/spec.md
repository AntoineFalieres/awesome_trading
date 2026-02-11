# Feature Specification: Generic Moving Average Indicator

**Feature Branch**: `007-generic-moving-average`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Implement `src/indicators/ma.py` based on @.specify/specs/indicators/generic_moving_average.md Requirements: 1. Implement the `MovingAverage` class inheriting from `Indicator`. 2. Ensure it handles the switch logic between 'sma', 'ema', and 'wma' cleanly. 3. Strictly follow type hinting: `def __init__(self, period: int, ma_type: str = 'sma'):`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer can use various moving average types (Priority: P1)

As a developer, I want to use a single `MovingAverage` indicator that can calculate different types of moving averages (Simple, Exponential, Weighted) so that I can easily switch between them in my strategies without changing the indicator class.

**Why this priority**: This provides flexibility and reduces code duplication, making strategies easier to build and maintain.

**Independent Test**: A developer can instantiate the `MovingAverage` class with different `ma_type` parameters ('sma', 'ema', 'wma') and receive the correctly calculated moving average for each type.

**Acceptance Scenarios**:

1. **Given** a `period` of 20 and `ma_type` of 'sma', **When** the developer calculates the indicator, **Then** the result is a 20-period Simple Moving Average.
2. **Given** a `period` of 50 and `ma_type` of 'ema', **When** the developer calculates the indicator, **Then** the result is a 50-period Exponential Moving Average.
3. **Given** a `period` of 30 and `ma_type` of 'wma', **When** the developer calculates the indicator, **Then** the result is a 30-period Weighted Moving Average.
4. **Given** an invalid `ma_type` (e.g., 'xyz'), **When** the developer instantiates the class, **Then** a `ValueError` is raised.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a class `MovingAverage` in `trendflow/indicators/ma.py`.
- **FR-002**: The `MovingAverage` class MUST inherit from the `Indicator` base class.
- **FR-003**: The `MovingAverage` constructor (`__init__`) MUST accept a `period` (integer) and an optional `ma_type` (string, default 'sma').
- **FR-004**: The `ma_type` parameter MUST be validated to be one of 'sma', 'ema', or 'wma'. Invalid types MUST raise a `ValueError`.
- **FR-005**: The `calculate` method MUST implement the logic to compute the correct moving average based on the `ma_type` specified during initialization.
- **FR-006**: The calculation for each moving average type MUST be vectorized for performance.
- **FR-007**: All methods in the `MovingAverage` class MUST have complete and correct PEP-484 type hints.
- **FR-008**: The output column name MUST reflect the period and type, e.g., `SMA_20`, `EMA_50`.

### Key Entities *(include if feature involves data)*

- **MovingAverage**: A flexible indicator capable of calculating various types of moving averages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a given dataset, the `MovingAverage` indicator's output for 'sma', 'ema', and 'wma' types MUST exactly match the results from a trusted library like `pandas_ta`.
- **SC-002**: The calculation for 1 million data points for any MA type completes in under 1 second.
- **SC-003**: Instantiating the class with an unsupported `ma_type` consistently raises a `ValueError`.
- **SC-004**: Code coverage for `trendflow/indicators/ma.py` is at least 95%.
