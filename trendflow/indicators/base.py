from abc import ABC, abstractmethod
import pandas as pd

class Indicator(ABC):
    """Abstract base class for all indicators."""

    @property
    def name(self) -> str:
        """The name of the indicator."""
        return self.__class__.__name__

    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the indicator value.

        Args:
            data: A pandas DataFrame with OHLCV data.

        Returns:
            A pandas DataFrame with the calculated indicator data.
        """
        raise NotImplementedError
