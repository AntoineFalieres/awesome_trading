# Feature Specification: Indicator Base Class

**Feature Branch**: `001-indicator-base-class`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Implement the `Indicator` base class in `src/indicators/base.py` based on @.specify/specs/indicator_base.md Ensure you strictly follow the "Code Quality & Safety" rules from @.specify/memory/constitution.md particularly regarding Type Hinting and Error Handling."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer can create a new indicator (Priority: P1)

As a developer, I want to create a new indicator by inheriting from a base `Indicator` class, so that I can easily implement new trading indicators with a consistent interface.

**Why this priority**: This is the core functionality of the indicator framework.

**Independent Test**: A developer can create a new class that inherits from `Indicator`, implement the required methods, and have it recognized by the system.

**Acceptance Scenarios**:

1. **Given** a developer wants to create a `SimpleMovingAverage` indicator, **When** they create a class `SimpleMovingAverage(Indicator)` and implement the `calculate` method, **Then** the class can be instantiated without errors.
2. **Given** a developer has a new indicator class, **When** they try to instantiate it without implementing the abstract methods from `Indicator`, **Then** a `TypeError` is raised.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an abstract base class named `Indicator` in `trendflow/indicators/base.py`.
- **FR-002**: The `Indicator` class MUST define an abstract method `calculate` that takes a pandas DataFrame and returns a DataFrame.
- **FR-003**: The `Indicator` class MUST enforce that any subclass implements the `calculate` method.
- **FR-004**: All methods in the `Indicator` class and its subclasses MUST include PEP-484 type hints.
- **FR-005**: The `Indicator` class MUST have a `name` property that returns the name of the indicator.

### Key Entities *(include if feature involves data)*

- **Indicator**: Represents a technical indicator. It has a name and a method to calculate its value.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the code in `trendflow/indicators/base.py` is type-hinted.
- **SC-002**: A developer can create and use a new indicator in less than 10 lines of code (excluding the calculation logic).
- **SC-003**: Attempting to use an incomplete indicator class (missing `calculate` method) results in a clear `TypeError`.
