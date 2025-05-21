import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy
import math as mt

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

class MarubozuStrategy(BaseStrategy):
    def __init__(self,margin_of_error = 0.05):
        super().__init__()
        self.margin_of_error = margin_of_error
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        data = data.copy()
        signals = pd.Series(0, index=data.index, dtype=float)
        for i in range(1,len(data)):
            data_upto_yesterday = data.iloc[:i]
            signals.iloc[i] = self.generate_signal_from_data_point(data_upto_yesterday)
        return signals
    
    def marubozu(self,X):
        error = lambda p1,p2: mt.fabs((p2-p1)/p1)
        open, high, low, close = X[0], X[1], X[2], X[3]
        if error(open,low) < self.margin_of_error and error(close,high) < self.margin_of_error:
            return {'marubozu': True, 'bull': True}
        elif error(open,high) < self.margin_of_error and error(close,low) < self.margin_of_error:
            return {'marubozu': True, 'bull': False}
        else:
            return {'marubozu': False, 'bull': None}
    
    def generate_signal_from_data_point(self, data_upto_yesterday: pd.DataFrame):
        # X = ['o','h','l','c']
        O, H, L, C = data_upto_yesterday['Open'].iloc[-1], data_upto_yesterday['High'].iloc[-1], data_upto_yesterday['Low'].iloc[-1], data_upto_yesterday['Close'].iloc[-1]
        X = [O.values[0],H.values[0],L.values[0],C.values[0]]
        output = self.marubozu(X)
        if(output['bull']==True):
            return 1
        elif(output['bull']==False):
            return -1
        else:
            return 0
    