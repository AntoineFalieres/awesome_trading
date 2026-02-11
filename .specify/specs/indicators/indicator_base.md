# Specification for Indicator Base Class

## Context
We need a standardized Abstract Base Class (ABC) that all technical indicators in the "TrendFlow" application must inherit from. This ensures consistency in data validation, calculation execution, and visualization across the app.

## Target File
`src/indicators/base.py` (Adjust path if your structure is different)

## Requirements

### 1. Class Structure
* **Class Name:** `Indicator`
* **Parent:** `abc.ABC` (Python Standard Library)
* **Purpose:** Define the contract that all specific indicators (MM30, Volume, RSI) must follow.

### 2. Abstract Methods (Must be implemented by children)
* **`calculate(self, data: pd.DataFrame) -> pd.Series | pd.DataFrame`**
    * **Input:** A Pandas DataFrame containing standard OHLCV data (columns: `open`, `high`, `low`, `close`, `volume`).
    * **Logic:** This method will contain the specific math for the indicator.
    * **Output:** A Series or DataFrame indexed by the same timestamps as the input.

### 3. Concrete Methods (Shared logic)
* **`validate_input(self, data: pd.DataFrame) -> bool`**
    * **Logic:**
        * Check if the DataFrame is empty.
        * Check if required columns (e.g., `close`) exist.
        * Raise a custom `ValueError` if checks fail.
* **`sanitize_output(self, result: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame`**
    * **Logic:**
        * Handle `NaN` values (fill 0 or drop depending on config).
        * Ensure the index matches the input index.

### 4. Constraints
* Adhere to `constitution.md`: Use `pydantic` for config if needed, and strictly use type hints.