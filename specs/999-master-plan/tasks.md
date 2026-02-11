# Tasks: TrendFlow Application Master Plan

**Input**: Master Implementation Plan from `specs/999-master-plan/plan.md`
**Prerequisites**: All `spec.md` files in the `specs/` directory.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [ ] T001 [P] Create directory structure: `trendflow/indicators`, `trendflow/strategies`, `trendflow/backtest`, `trendflow/dashboard`, `trendflow/data`.
- [ ] T002 [P] Create and populate `requirements.txt` with `pandas`, `numpy`, `yfinance`, `plotly`, `streamlit`.
- [ ] T003 Create `__init__.py` files in all `trendflow` subdirectories to make them importable modules.

---

## Phase 2: Foundational (Indicator Framework) [US1]

**Goal**: Establish the core `Indicator` abstraction.
**Independent Test**: A developer can subclass `Indicator`, but it will raise a `TypeError` if `calculate` is not implemented.

### Implementation for Foundational Framework
- [ ] T004 [US1] Define the abstract `Indicator` class in `trendflow/indicators/base.py`.
- [ ] T005 [US1] Add the abstract `calculate` method to `trendflow/indicators/base.py`.
- [ ] T006 [US1] Add the `name` property to the `Indicator` class in `trendflow/indicators/base.py`.

**Checkpoint**: The core indicator contract is defined.

---

## Phase 3: User Story 2 - Core Indicator Implementation

**Goal**: Build the initial set of specific indicators needed for the main strategy.
**Independent Test**: A developer can instantiate and run `MM30Indicator` and `VolumeStats` on a DataFrame and get the correct output columns.

### Implementation for Core Indicators
- [ ] T007 [P] [US2] Implement the `MM30Indicator` class in `trendflow/indicators/mm30.py`, inheriting from `Indicator`.
- [ ] T008 [P] [US2] Implement the `calculate` method for `MM30Indicator` using a vectorized numpy WMA in `trendflow/indicators/mm30.py`.
- [ ] T009 [P] [US2] Implement the `VolumeStats` class in `trendflow/indicators/volume.py`, inheriting from `Indicator`.
- [ ] T010 [P] [US2] Implement the `calculate` method for `VolumeStats` using vectorized pandas for `vol_ma` and `vol_ratio` in `trendflow/indicators/volume.py`.

**Checkpoint**: The primary indicators required by the `WeinsteinStrategy` are complete and testable.

---

## Phase 4: User Story 3 - Generic Indicator Factory

**Goal**: Build the flexible, reusable `MovingAverage` indicator.
**Independent Test**: A developer can instantiate `MovingAverage` with `ma_type='sma'`, `'ema'`, and `'wma'` and get correct, distinct results for each.

### Implementation for Generic Indicator
- [ ] T011 [US3] Implement the `MovingAverage` class in `trendflow/indicators/ma.py`, inheriting from `Indicator`.
- [ ] T012 [US3] Implement the `__init__` method in `MovingAverage` to accept `period` and `ma_type` with validation in `trendflow/indicators/ma.py`.
- [ ] T013 [US3] Implement the `calculate` method's switch logic to handle 'sma', 'ema', and 'wma' calculations in `trendflow/indicators/ma.py`.

**Checkpoint**: The advanced, reusable `MovingAverage` indicator is complete.

---

## Phase 5: User Story 4 - Strategy Engine

**Goal**: Implement the `WeinsteinStrategy` with its full logic set.
**Independent Test**: An analyst can run `generate_signals` and receive a DataFrame with `signal` and `exit_reason` columns that correctly reflect the base entry, risk management, and trend filter rules.

### Implementation for Strategy Engine
- [ ] T014 [US4] Create the `WeinsteinStrategy` class in `trendflow/strategies/weinstein.py`.
- [ ] T015 [US4] Implement the `__init__` method to accept all parameters (`stop_loss_pct`, `take_profit_pct`, `use_trend_filter`, etc.) in `trendflow/strategies/weinstein.py`.
- [ ] T016 [US4] In `generate_signals`, implement the vectorized pre-calculation of base entry conditions and the optional trend filter condition.
- [ ] T017 [US4] Implement the stateful `for` loop in `generate_signals` to manage position state (`in_position`, `entry_price`).
- [ ] T018 [US4] Inside the loop, add the logic to check for and apply stop-loss and take-profit exits, populating the `exit_reason` column in `trendflow/strategies/weinstein.py`.

**Checkpoint**: The complete trading strategy with all rules is implemented.

---

## Phase 6: User Story 5 - Backtesting Engine

**Goal**: Implement the `Backtester` to validate strategy performance.
**Independent Test**: An analyst can pass strategy signals into the `Backtester` and receive a dictionary of performance metrics.

### Implementation for Backtesting Engine
- [ ] T019 [US5] Create the `Backtester` class in `trendflow/backtest/engine.py`.
- [ ] T020 [US5] Implement the vectorized `run` method, ensuring signals are shifted to prevent look-ahead bias in `trendflow/backtest/engine.py`.
- [ ] T021 [US5] Implement the `calculate_metrics` method to compute Total Return, Max Drawdown, and Win Rate in `trendflow/backtest/engine.py`.

**Checkpoint**: The validation engine is complete.

---

## Phase 7: User Story 6 - Dashboard UI

**Goal**: Build the interactive Streamlit dashboard.
**Independent Test**: An analyst can launch the app, select a ticker, and see the full chart with strategy signals and performance metrics.

### Implementation for Dashboard
- [ ] T022 [US6] Create the main application file at `trendflow/dashboard/app.py`.
- [ ] T023 [US6] Implement the Streamlit sidebar with a ticker input and controls for all `WeinsteinStrategy` parameters.
- [ ] T024 [US6] Implement the data fetching and caching function using `@st.cache_data` in `trendflow/dashboard/app.py`.
- [ ] T025 [US6] Add logic to instantiate and run the `WeinsteinStrategy` and `Backtester` based on user inputs.
- [ ] T026 [US6] Implement the `plotly` chart creation, including the main candlestick chart, volume subplot, and signal markers.
- [ ] T027 [US6] Add logic to conditionally plot the secondary moving average based on its sidebar controls in `trendflow/dashboard/app.py`.
- [ ] T028 [US6] Display the final metrics from the `Backtester` at the top of the dashboard.

**Checkpoint**: The user-facing application is fully functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T029 [P] Review all files for PEP8 compliance and consistent docstrings.
- [ ] T030 [P] Add or update module-level docstrings explaining the purpose of each file.
- [ ] T031 Perform a final end-to-end run of the dashboard to ensure all components integrate correctly.

---

## Dependencies & Execution Order

- **Phase 1 -> Phase 2**: The `Indicator` base class is required before any concrete indicators can be built.
- **Phase 2 & 3 -> Phase 5**: The `MM30Indicator`, `VolumeStats`, and `MovingAverage` indicators are all dependencies for the `WeinsteinStrategy`.
- **Phase 5 -> Phase 6**: The `WeinsteinStrategy` output is the required input for the `Backtester`.
- **Phase 6 -> Phase 7**: The `Backtester` and `WeinsteinStrategy` are both required to power the `StrategyDashboard`.
- **MVP SCOPE**: A minimal MVP would consist of completing Phases 1, 2, 5 (Strategy without all features), and 6. This would provide a core backtestable strategy. A UI-focused MVP would prioritize Phase 7. Given the plan, a sequential build through all phases is recommended.
