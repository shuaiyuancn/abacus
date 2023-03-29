# %%
%load_ext autoreload
%autoreload 2

# %%
from arena.framework import CsvFileReader
from arena.step_buy_agent import StepBuyAgent, StepBuyWithStopLossAgent
from arena.base_agent import BaseAgent

from logzero import logger
import pandas as pd

import itertools

logger.setLevel("INFO")

# %%
def run_agent(agent: BaseAgent, fin: CsvFileReader):
    while True:
        data = fin.next_row()
        if not data:
            break

        agent.trade(data)

    fin.reset_loc()

    return agent.get_cumulative_value()

# %%
MONEY_AVAILABLE = 1E5

# %%
fin = CsvFileReader("../dataset/VEVE-processed.csv")

# %%
agent_step_buy = StepBuyAgent(MONEY_AVAILABLE, 30, 2000)

# %%
cumulative_value = run_agent(agent_step_buy, fin)
logger.info(f"Step buy agent has {cumulative_value}")

# %%
lst_buy_size = range(100, 5001, 500)
lst_interval = range(1, 48, 7)

results = []

for interval, buy_size in itertools.product(lst_interval, lst_buy_size):
    cumulative_value = run_agent(StepBuyAgent(MONEY_AVAILABLE, interval, buy_size), fin)
    results.append(
        (interval, buy_size, *cumulative_value)
    )

# %%


# %%
df = pd.DataFrame(results, columns=[
    'interval', 'buy_size', 'holding_value', 'money_value', 'ratio'
])

# %%
df = df.sort_values(by='ratio', ascending=False)

# %%
df.head(10)

# %%
df.to_csv('../result/VEVE-step-buy.csv', index=None)

# %%


# stey_buy_stop_loss_agent = StepBuyWithStopLossAgent(MONEY_AVAILABLE, 30, 2000, 0.1, 0.5)
# run_agent(stey_buy_stop_loss_agent, fin)

# %%
lst_stop_loss_in_pct = [0.1, 0.2, 0.3, 0.4, 0.5]
lst_sell_size_in_pct = [0.1, 0.2, 0.3, 0.4, 0.5]
lst_buy_size = [1000, 2000, 3000, 4000, 5000]
lst_interval = [7, 14, 21, 28]

results = []
logger.setLevel("INFO")

for interval, buy_size, stop_loss_in_pct, sell_size_in_pct in itertools.product(
    lst_interval, lst_buy_size, lst_stop_loss_in_pct, lst_sell_size_in_pct
):
    cumulative_value = run_agent(
        StepBuyWithStopLossAgent(
            MONEY_AVAILABLE, interval, buy_size, stop_loss_in_pct, sell_size_in_pct
        ),
        fin,
    )
    results.append(
        (interval, buy_size, stop_loss_in_pct, sell_size_in_pct, *cumulative_value)
    )
    logger.info(f"Done {interval}, {buy_size}, {stop_loss_in_pct}, {sell_size_in_pct}")

# %%
df = pd.DataFrame(results, columns=[
    'interval', 'buy_size', 'stop_loss_in_pct', 'sell_size_in_pct', 'holding_value', 'money_value', 'ratio'
])
df = df.sort_values(by='ratio', ascending=False)

# %%
df.to_csv('../result/VEVE-step-buy-with-stop-loss.csv', index=None)

# %%
# use last_price as reference for stop loss

lst_stop_loss_in_pct = [0.1, 0.2, 0.3, 0.4, 0.5]
lst_sell_size_in_pct = [0.1, 0.2, 0.3, 0.4, 0.5]
lst_buy_size = [1000, 2000, 3000, 4000, 5000]
lst_interval = [7, 14, 21, 28]

results = []
logger.setLevel("INFO")

for interval, buy_size, stop_loss_in_pct, sell_size_in_pct in itertools.product(
    lst_interval, lst_buy_size, lst_stop_loss_in_pct, lst_sell_size_in_pct
):
    cumulative_value = run_agent(
        StepBuyWithStopLossAgent(
            MONEY_AVAILABLE, interval, buy_size, stop_loss_in_pct, sell_size_in_pct, False
        ),
        fin,
    )
    results.append(
        (interval, buy_size, stop_loss_in_pct, sell_size_in_pct, *cumulative_value)
    )
    logger.info(f"Done {interval}, {buy_size}, {stop_loss_in_pct}, {sell_size_in_pct}")

# %%
df = pd.DataFrame(results, columns=[
    'interval', 'buy_size', 'stop_loss_in_pct', 'sell_size_in_pct', 'holding_value', 'money_value', 'ratio'
])
df = df.sort_values(by='ratio', ascending=False)

# %%
df.to_csv('../result/VEVE-step-buy-with-stop-loss-last-price.csv', index=None)

# %%
