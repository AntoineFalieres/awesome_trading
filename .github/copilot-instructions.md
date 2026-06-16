# Copilot Instructions — TrendFlow (awesome_trading)

## Commands

```bash
# Install for development
uv pip install -e .

# Run the web app
streamlit run main.py   # opens at http://localhost:8501

# Run tests
pytest
python test_trendflow.py   # integration smoke test (fetches live market data)
```

## Architecture Overview

TrendFlow is a Python package (`trendflow/`) with a Streamlit web UI (`pages/`, `main.py`) for backtesting trading strategies.

**Execution flow:**
1. A `Strategy` object (JSON-serializable dataclass) defines symbol, date range, indicators, entry/exit conditions
2. `StrategyManager` persists/loads strategies as JSON files in `strategies/saved/`
3. `StrategyExecutor.execute()` orchestrates the full pipeline:
   - Fetches OHLCV market data via `yfinance` (with local caching in `.cache/market_data/`)
   - Calculates each indicator, building a `column_mapping` dict from user-defined indicator names → actual DataFrame column names
   - Evaluates entry/exit conditions (AND logic across all conditions in a group) using that mapping
   - Passes the signal-annotated DataFrame to `Backtester` for performance metrics

**Key internal detail — indicator name resolution:**  
Indicator configs use user-defined names (e.g. `"sma_10"`), but `calculate()` writes named columns (e.g. `SMA_10`). The executor stores the mapping in `self.column_mapping` and uses it when evaluating conditions. New indicator types added to `_calculate_indicators()` must populate this mapping.

## Key Conventions

### Adding a new indicator
1. Create `trendflow/indicators/my_indicator.py`, subclass `Indicator` (from `trendflow/indicators/base.py`), implement `calculate(data: pd.DataFrame) -> pd.DataFrame`
2. Export it from `trendflow/indicators/__init__.py`
3. Add a branch in `StrategyExecutor._calculate_indicators()` to instantiate it and register its output column in `self.column_mapping`
4. Document it in `README.md`

### Strategy JSON schema
Strategies are saved to `strategies/saved/<name>.json`. Reference schema: `trendflow/strategies/SCHEMA.md`.

Condition types: `crossover`, `crossunder`, `threshold` (with comparisons: `above`, `below`, `above_or_equal`, `below_or_equal`).

### Code style
- Strict **PEP 8**
- Do **not** add new third-party packages to `install_requires` in `setup.py` without explicit approval
- Do **not** bump the version in `setup.py` unless asked

### Dependencies (setup.py)
`pandas`, `numpy`, `yfinance`, `plotly`, `streamlit` — keep this list minimal.
