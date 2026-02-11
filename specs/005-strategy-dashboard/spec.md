# Feature Specification: Strategy Dashboard with Secondary Moving Average

**Feature Branch**: `005-strategy-dashboard`
**Created**: 2026-02-11
**Status**: In Progress
**Input**: User description: "Update `src/dashboard/app.py` based on the revised @.specify/specs/dashboard/dashboard.md Requirements: 1. Import the new `MovingAverage` class from `src.indicators.ma`. 2. Add the Sidebar controls for the Secondary MA. 3. Add the logic to plot this second line on the main chart ONLY if the checkbox is selected."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analyst can visualize strategy signals (Priority: P1)

As an analyst, I want to view a chart that displays the stock price, volume, and the buy/sell signals from the Weinstein strategy, so I can visually assess the strategy's behavior.

**Why this priority**: Visual backtesting is a crucial step in strategy development and validation.

**Independent Test**: An analyst can open the dashboard, select a stock, and see a chart with the price, volume, and correctly plotted buy/sell signals.

**Acceptance Scenarios**:

1. **Given** an analyst opens the dashboard, **When** they select a ticker (e.g., AAPL), **Then** a chart is displayed showing the price and volume data for that ticker.
2. **Given** the chart is displayed, **When** the `WeinsteinStrategy` generates a buy signal, **Then** a green "buy" marker is shown on the price chart at the corresponding date.
3. **Given** the chart is displayed, **When** the `WeinsteinStrategy` generates a sell signal, **Then** a red "sell" marker is shown on the price chart at the corresponding date.
4. **Given** the analyst reloads the page or selects the same ticker, **When** the data is fetched, **Then** it is loaded from a cache to improve performance.

---
### User Story 2 - Analyst can add a secondary moving average for context (Priority: P2)

As an analyst, I want to add a secondary, configurable moving average to the price chart, so that I can analyze the primary strategy signals in the context of another trend indicator.

**Why this priority**: It provides more context for analysis, allowing users to compare different trend lengths.

**Independent Test**: An analyst can use sidebar controls to enable and configure a secondary moving average, which then appears correctly on the chart.

**Acceptance Scenarios**:

1. **Given** the dashboard is open, **When** the analyst checks the "Show Secondary MA" checkbox in the sidebar, **Then** a second moving average line is plotted on the price chart.
2. **Given** the "Show Secondary MA" checkbox is selected, **When** the analyst changes the period and type (e.g., 200, 'ema') in the sidebar controls, **Then** the secondary moving average line on the chart updates to reflect the new parameters.
3. **Given** the "Show Secondary MA" checkbox is unchecked, **When** the chart is displayed, **Then** the secondary moving average is not visible.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a web dashboard application in `trendflow/dashboard/app.py`.
- **FR-002**: The dashboard MUST allow the user to select a stock ticker.
- **FR-003**: The data fetching function MUST be cached.
- **FR-004**: The dashboard MUST apply the `WeinsteinStrategy` to generate primary trading signals.
- **FR-005**: The dashboard MUST display a two-panel chart (Price, Volume).
- **FR-006**: Buy/Sell signals MUST be represented as green/red markers on the price chart.
- **FR-007**: The dashboard sidebar MUST contain a checkbox labeled "Show Secondary MA".
- **FR-008**: If the checkbox is selected, the sidebar MUST display controls to configure the secondary moving average's `period` and `ma_type` ('sma', 'ema', 'wma').
- **FR-009**: The application MUST use the `MovingAverage` indicator to calculate the secondary MA based on the user's sidebar selections.
- **FR-010**: If the checkbox is selected, the calculated secondary moving average MUST be plotted as a line on the top (price) panel of the chart.

### Key Entities *(include if feature involves data)*

- **Dashboard**: A web-based user interface for visualizing trading strategy signals and configurable secondary indicators.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The dashboard correctly plots primary Weinstein signals and the optional secondary moving average on a known dataset.
- **SC-002**: Page load time for a previously selected ticker remains under 0.5 seconds.
- **SC-003**: The secondary moving average line appears, updates, and disappears correctly in response to user interaction with the sidebar controls.
- **SC-004**: The dashboard application starts without errors and is accessible via a web browser.
