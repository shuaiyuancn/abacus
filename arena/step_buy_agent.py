from arena.base_agent import BaseAgent
from arena.framework import StockData

from logzero import logger

class StepBuyAgent(BaseAgent):
    def __init__(self, money_available, interval_in_days, buy_size) -> None:
        super().__init__(money_available)
        self.interval_in_days = interval_in_days
        self.current_interval = 0
        self.buy_size = buy_size

    def trade(self, data: StockData):
        if self.current_interval == self.interval_in_days:
            if self.money_available > self.buy_size:
                self.money_available -= self.buy_size
                self.holding += self.buy_size / data.open_price
                self.current_interval = 0
            else:
                logger.warning(f"Money available {self.money_available} < buy size {self.buy_size}")
        else:
            self.current_interval += 1
            