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
        super().trade(data)

        if self.current_interval == self.interval_in_days:
            self.buy(self.buy_size)
            self.current_interval = 0
        else:
            self.current_interval += 1


class StepBuyWithStopLossAgent(StepBuyAgent):
    def __init__(
        self,
        money_available,
        interval_in_days,
        buy_size,
        stop_loss_in_pct,
        sell_size_in_pct,
        avg_price_as_reference=True,
    ) -> None:
        super().__init__(money_available, interval_in_days, buy_size)
        self.stop_loss_in_pct = stop_loss_in_pct
        self.stop_loss_in_money = 0.0
        self.sell_size_in_pct = sell_size_in_pct
        self.avg_price_as_reference = avg_price_as_reference

    def set_stop_loss(self):
        if self.avg_price_as_reference:
            self.stop_loss_in_money = self.avg_price * (1 - self.stop_loss_in_pct)
        else:
            self.stop_loss_in_money = self.last_price * (1 - self.stop_loss_in_pct)

    def trade(self, data: StockData):
        super().trade(data)
        self.set_stop_loss()

        if data.open_price <= self.stop_loss_in_money:
            self.sell(self.sell_size_in_pct)
            # pause the current_interval
            return

        if self.current_interval == self.interval_in_days:
            self.buy(self.buy_size)
            self.current_interval = 0
        else:
            self.current_interval += 1
