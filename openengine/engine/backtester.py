import pandas as pd
import numpy as np
from openengine.execution.order_manager import OrderManager

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy, initial_capital: float = 100000):
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.order_manager = OrderManager()
        self.results = None

    def run(self):
        signals = self.strategy.generate_signals(self.data)
        portfolio = self._simulate_trading(signals)
        self.results = portfolio
        return portfolio

    def _simulate_trading(self, signals: pd.Series) -> pd.DataFrame:
        portfolio = pd.DataFrame(index=self.data.index)
        portfolio['holdings'] = 0.0
        portfolio['cash'] = float(self.initial_capital)
        portfolio['total'] = float(self.initial_capital)

        current_position = 0

        for i in range(1, len(self.data)):
            date = self.data.index[i]
            signal = signals.iloc[i]
            # Use .item() to properly convert pandas scalar to Python float
            price = self.data["Close"].iloc[i].item()
            previous_cash = portfolio['cash'].iloc[i-1].item()
            cash_left = previous_cash
            if float(signal) == 1 and current_position <= 0:
                current_position = self.order_manager.buy(date, price, previous_cash)
                cash_left -= float(current_position * price)
            elif float(signal) == -1 and current_position >= 0:
                pre_sell_pos = current_position
                cash_left += float(pre_sell_pos*price)
                current_position = self.order_manager.sell(date, price, previous_cash)
        

            portfolio.loc[date, 'holdings'] = float(current_position * price)
            portfolio.loc[date, 'cash'] = cash_left
            portfolio.loc[date, 'total'] = portfolio.loc[date, 'holdings'] + portfolio.loc[date, 'cash']

        return portfolio
