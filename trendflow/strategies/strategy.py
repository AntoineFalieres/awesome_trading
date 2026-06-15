import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import copy


@dataclass
class IndicatorConfig:
    """Configuration for a single indicator."""
    name: str
    type: str
    params: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict) -> 'IndicatorConfig':
        return cls(**data)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ConditionConfig:
    """Configuration for an entry or exit condition."""
    type: str  # 'crossover', 'crossunder', 'threshold'
    fast_indicator: str = None
    slow_indicator: str = None
    indicator: str = None
    comparison: str = None
    value: float = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConditionConfig':
        return cls(**data)

    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class Strategy:
    """
    Represents a trading strategy configuration.
    """

    def __init__(self,
                 name: str,
                 symbol: str,
                 start_date: str,
                 end_date: str,
                 indicators: List[Dict[str, Any]],
                 entry_conditions: List[Dict[str, Any]],
                 exit_conditions: List[Dict[str, Any]],
                 description: str = "",
                 backtest_params: Optional[Dict[str, Any]] = None):
        """
        Initialize a trading strategy.

        Args:
            name: Strategy name
            symbol: Stock/crypto ticker
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            indicators: List of indicator configurations
            entry_conditions: List of entry condition configurations
            exit_conditions: List of exit condition configurations
            description: Strategy description
            backtest_params: Backtest parameters (initial_capital, commission)
        """
        self.name = name
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.indicators = [IndicatorConfig.from_dict(ind) if isinstance(ind, dict) else ind 
                          for ind in indicators]
        self.entry_conditions = [ConditionConfig.from_dict(cond) if isinstance(cond, dict) else cond 
                                for cond in entry_conditions]
        self.exit_conditions = [ConditionConfig.from_dict(cond) if isinstance(cond, dict) else cond 
                               for cond in exit_conditions]
        self.backtest_params = backtest_params or {'initial_capital': 10000, 'commission': 0.001}

    @classmethod
    def from_dict(cls, data: Dict) -> 'Strategy':
        """Create Strategy from dictionary."""
        return cls(
            name=data['name'],
            symbol=data['symbol'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            indicators=data.get('indicators', []),
            entry_conditions=data.get('entry_conditions', []),
            exit_conditions=data.get('exit_conditions', []),
            description=data.get('description', ''),
            backtest_params=data.get('backtest_params', None)
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'Strategy':
        """Create Strategy from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_dict(self) -> Dict:
        """Convert Strategy to dictionary."""
        return {
            'name': self.name,
            'symbol': self.symbol,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'indicators': [ind.to_dict() if hasattr(ind, 'to_dict') else ind 
                          for ind in self.indicators],
            'entry_conditions': [cond.to_dict() if hasattr(cond, 'to_dict') else cond 
                                for cond in self.entry_conditions],
            'exit_conditions': [cond.to_dict() if hasattr(cond, 'to_dict') else cond 
                               for cond in self.exit_conditions],
            'backtest_params': self.backtest_params
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert Strategy to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def validate(self) -> List[str]:
        """
        Validate strategy configuration.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if not self.name:
            errors.append("Strategy must have a name")
        if not self.symbol:
            errors.append("Strategy must have a symbol")
        if not self.start_date:
            errors.append("Strategy must have a start_date")
        if not self.end_date:
            errors.append("Strategy must have an end_date")
        if len(self.indicators) == 0:
            errors.append("Strategy must have at least one indicator")
        if len(self.entry_conditions) == 0:
            errors.append("Strategy must have at least one entry condition")
        if len(self.exit_conditions) == 0:
            errors.append("Strategy must have at least one exit condition")

        # Validate indicator references in conditions
        indicator_names = {ind.name for ind in self.indicators}
        
        for i, cond in enumerate(self.entry_conditions):
            if cond.type in ('crossover', 'crossunder'):
                if cond.fast_indicator and cond.fast_indicator not in indicator_names:
                    errors.append(f"Entry condition {i}: indicator '{cond.fast_indicator}' not found")
                if cond.slow_indicator and cond.slow_indicator not in indicator_names:
                    errors.append(f"Entry condition {i}: indicator '{cond.slow_indicator}' not found")
            elif cond.type == 'threshold':
                if cond.indicator and cond.indicator not in indicator_names:
                    errors.append(f"Entry condition {i}: indicator '{cond.indicator}' not found")

        for i, cond in enumerate(self.exit_conditions):
            if cond.type in ('crossover', 'crossunder'):
                if cond.fast_indicator and cond.fast_indicator not in indicator_names:
                    errors.append(f"Exit condition {i}: indicator '{cond.fast_indicator}' not found")
                if cond.slow_indicator and cond.slow_indicator not in indicator_names:
                    errors.append(f"Exit condition {i}: indicator '{cond.slow_indicator}' not found")
            elif cond.type == 'threshold':
                if cond.indicator and cond.indicator not in indicator_names:
                    errors.append(f"Exit condition {i}: indicator '{cond.indicator}' not found")

        return errors

    def __repr__(self) -> str:
        return f"Strategy(name='{self.name}', symbol='{self.symbol}', {self.start_date} to {self.end_date})"


class StrategyManager:
    """
    Manages saving and loading strategies from JSON files.
    """

    def __init__(self, save_dir: str = "strategies/saved"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save(self, strategy: Strategy, overwrite: bool = False) -> Path:
        """
        Save strategy to JSON file.

        Args:
            strategy: Strategy object to save
            overwrite: If True, overwrite existing strategy

        Returns:
            Path to saved file
        """
        errors = strategy.validate()
        if errors:
            raise ValueError(f"Cannot save invalid strategy: {'; '.join(errors)}")

        filepath = self.save_dir / f"{strategy.name}.json"
        
        if filepath.exists() and not overwrite:
            raise FileExistsError(f"Strategy '{strategy.name}' already exists. Set overwrite=True to replace.")

        with open(filepath, 'w') as f:
            f.write(strategy.to_json())

        print(f"Saved strategy to {filepath}")
        return filepath

    def load(self, strategy_name: str) -> Strategy:
        """
        Load strategy from JSON file.

        Args:
            strategy_name: Name of strategy to load (without .json extension)

        Returns:
            Strategy object
        """
        filepath = self.save_dir / f"{strategy_name}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Strategy '{strategy_name}' not found. Available strategies: {self.list()}")

        with open(filepath, 'r') as f:
            strategy = Strategy.from_json(f.read())

        return strategy

    def list(self) -> List[str]:
        """
        List all saved strategies.

        Returns:
            List of strategy names
        """
        strategies = [f.stem for f in self.save_dir.glob("*.json")]
        return sorted(strategies)

    def delete(self, strategy_name: str) -> None:
        """
        Delete a saved strategy.

        Args:
            strategy_name: Name of strategy to delete
        """
        filepath = self.save_dir / f"{strategy_name}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Strategy '{strategy_name}' not found")

        filepath.unlink()
        print(f"Deleted strategy: {strategy_name}")

    def get_all(self) -> List[Strategy]:
        """
        Load all saved strategies.

        Returns:
            List of Strategy objects
        """
        strategies = []
        for name in self.list():
            try:
                strategies.append(self.load(name))
            except Exception as e:
                print(f"Failed to load strategy '{name}': {e}")
        return strategies
