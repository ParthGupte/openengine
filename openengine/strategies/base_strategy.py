from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on historical data.
        Returns a Pandas Series:
          1 for BUY,
         -1 for SELL,
          0 for HOLD.
        """
        pass

    def generate_signal_from_data_point(self, data_point: dict) -> int:
        # Dummy implementation for live trading; override this in concrete strategies.
        return 0
