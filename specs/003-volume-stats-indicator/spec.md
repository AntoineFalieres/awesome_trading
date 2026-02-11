# Feature Specification: Volume Stats Indicator

**Feature Branch**: `003-volume-stats-indicator`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Implement `src/indicators/volume.py` based on @.specify/specs/volume_spike.md Requirements: 1. Class `VolumeStats` must inherit from the `Indicator` base class. 2. Implement two calculations using vectorized Pandas (no loops): - `vol_ma`: The Simple Moving Average of volume. - `vol_ratio`: The current volume divided by `vol_ma`. 3. Critical Safety: Handle cases where `vol_ma` might be 0 to avoid DivisionByZero errors (replace Infs with 0 or NaN). 4. Strictly follow the type hinting rules from `constitution.md`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer can use the VolumeStats indicator (Priority: P1)

As a developer, I want to use the `VolumeStats` indicator to calculate the volume's moving average and the ratio of current volume to its moving average, so that I can identify unusual volume spikes.

**Why this priority**: This is the core functionality for detecting volume-based trading signals.

**Independent Test**: A developer can instantiate the `VolumeStats` indicator and call its `calculate` method with a pandas DataFrame, receiving a DataFrame with the `vol_ma` and `vol_ratio` columns.

**Acceptance Scenarios**:

1. **Given** a pandas DataFrame with a 'volume' column, **When** a developer calls `VolumeStats().calculate(df)`, **Then** the returned DataFrame contains new columns 'vol_ma' and 'vol_ratio'.
2. **Given** a pandas DataFrame where the volume moving average is zero for some rows, **When** `VolumeStats().calculate(df)` is called, **Then** the 'vol_ratio' for those rows is a non-infinite number (e.g., 0 or NaN).
3. **Given** a pandas DataFrame without a 'volume' column, **When** `VolumeStats().calculate(df)` is called, **Then** a `KeyError` is raised.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a class `VolumeStats` in `trendflow/indicators/volume.py`.
- **FR-002**: `VolumeStats` MUST inherit from the `Indicator` base class.
- **FR-003**: `VolumeStats` MUST implement the `calculate` method, which accepts a pandas DataFrame.
- **FR-004**: The `calculate` method MUST compute the simple moving average of the 'volume' column, resulting in a 'vol_ma' column.
- **FR-005**: The `calculate` method MUST compute the ratio of the current 'volume' to the 'vol_ma', resulting in a 'vol_ratio' column.
- **FR-006**: The calculation of 'vol_ratio' MUST safely handle cases where 'vol_ma' is zero, avoiding division by zero errors. The result in such cases should be NaN.
- **FR-007**: All calculations MUST be vectorized and avoid Python loops.
- **FR-008**: All methods in `VolumeStats` MUST include PEP-484 type hints.


### Key Entities *(include if feature involves data)*

- **VolumeStats**: A specific type of `Indicator` that calculates statistics related to trading volume.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `calculate` method correctly computes `vol_ma` and `vol_ratio` for a known dataset, matching a manual calculation.
- **SC-002**: The `calculate` method for 1 million data points executes in under 1 second.
- **SC-003**: No `DivisionByZeroError` is raised when the input data contains periods of zero volume.
- **SC-004**: Code coverage for `trendflow/indicators/volume.py` is at least 90%.
