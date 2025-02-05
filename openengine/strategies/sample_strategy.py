import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy

class SampleStrategy(BaseStrategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_window = 20
        long_window = 50
        
        data = data.copy()
        data["short_ma"] = data["Close"].rolling(window=short_window).mean()
        data["long_ma"] = data["Close"].rolling(window=long_window).mean()
        
        signals = pd.Series(0, index=data.index, dtype=float)
        signals.loc[data["short_ma"] > data["long_ma"]] = 1.0
        signals.loc[data["short_ma"] < data["long_ma"]] = -1.0
        
        return signals

    def generate_signal_from_data_point(self, data_point: dict) -> float:
        # A simple dummy signal for live data:
        price = float(data_point.get("price", 0))
        return 1.0 if price % 2 == 0 else -1.0
