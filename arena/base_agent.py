from arena.framework import StockData

from logzero import logger

class BaseAgent:
    def __init__(self, money_available) -> None:
        self.init_money_available = self.money_available = money_available
        self.holding = 0.0
        self.last_data = None
        self.last_price = None
        self.avg_price = 0.0

    def trade(self, data: StockData):
        self.last_data = data
        self.last_price = data.open_price
        self.avg_price = ((self.init_money_available - self.money_available) / self.holding) if self.holding else 0.0
        logger.debug(f"Average price: {self.avg_price}")

    def buy(self, buy_size_in_money):
        if self.money_available >= buy_size_in_money:
            self.money_available -= buy_size_in_money
            units = buy_size_in_money / self.last_price
            self.holding += units

            logger.debug(f"Bought {units} units at price {self.last_price}")
        else:
            logger.debug(f"Money available {self.money_available} < buy size {self.buy_size}")

    def sell(self, sell_size_in_pct):
        units = int(sell_size_in_pct * self.holding)
        if units > 0:
            self.holding -= units
            self.money_available += units * self.last_price

            logger.debug(f"Sold {units} units at price {self.last_price}")
        else:
            logger.debug("Nothing in holding to sell")

    def get_cumulative_value(self):
        holding_value = self.holding * self.last_price
        return (holding_value, self.money_available, (holding_value + self.money_available)/self.init_money_available)
