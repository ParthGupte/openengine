class OrderManager:
    def __init__(self):
        self.position = 0

    def buy(self, timestamp, price, available_cash):
        shares = available_cash // price
        self.position = shares
        print(f"[{timestamp}] BUY: {shares} shares at {price}")
        return self.position

    def sell(self, timestamp, price, available_cash):
        shares = self.position
        self.position -= shares
        print(f"[{timestamp}] SELL: {abs(shares)} shares at {price}")
        return self.position
