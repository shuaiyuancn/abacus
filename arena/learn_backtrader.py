from datetime import datetime
import backtrader as bt


class TestStrategy(bt.Strategy):

    params = (
        ("exitbars", 5),
        ("maperiod", 15),
        ("printlog", False)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_commision = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return
        
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log("Buy Create, %.2f" % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log("Sell Create, %.2f" % self.dataclose[0])
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

                self.buy_price = order.executed.price
                self.buy_commision = order.executed.comm
            elif order.issell():
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def stop(self):
        self.log("(MA Period %2d) Ending Value %.2f" % (self.params.maperiod, self.broker.getvalue()), doprint=True)

    def log(self, txt, dt=None, doprint=False):
        """ Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))


if __name__ == "__main__":
    cerebro = bt.Cerebro()

    # init the datasource
    cerebro.adddata(
        bt.feeds.YahooFinanceCSVData(
            dataname="/workspaces/abacus/dataset/orcl-1995-2014.txt",
            fromdate=datetime(2000, 1, 1),
            todate=datetime(2000, 12, 31),
            reverse=False,
        )
    )

    # init the strategy
    strats = cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10, 31),
        printlog=False,
    )

    # commission
    cerebro.broker.setcommission(commission=0.001)

    # sizer
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.broker.setcash(100000.0)

    cerebro.run(maxcpus=4)

