from arena.framework import StockData

class BaseAgent:
    def __init__(self, money_available) -> None:
        self.money_available = money_available
        self.holding = 0.0

    def trade(self, data: StockData):
        pass

    def get_cumulative_value(self, price):
        holding_value = self.holding * price
        return (holding_value, self.money_available)
