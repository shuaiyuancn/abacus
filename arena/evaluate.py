# %%
%load_ext autoreload
%autoreload 2

# %%
from arena.framework import CsvFileReader
from arena.step_buy_agent import StepBuyAgent
from arena.base_agent import BaseAgent

from logzero import logger

# %%
logger.setLevel("DEBUG")

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
agent_step_buy = StepBuyAgent(MONEY_AVAILABLE, 30, 2000)

# %%
cumulative_value = run_agent(agent_step_buy, fin)
logger.info(f"Step buy agent has {cumulative_value}")

# %%
import itertools
from tqdm.notebook import tqdm

lst_buy_size = range(100, 5001, 500)
lst_interval = range(1, 48, 7)

results = []

for interval, buy_size in tqdm(itertools.product(lst_interval, lst_buy_size)):
    cumulative_value = run_agent(StepBuyAgent(MONEY_AVAILABLE, interval, buy_size), fin)
    results.append(
        (interval, buy_size, *cumulative_value)
    )

# %%
import pandas as pd

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
from arena.step_buy_agent import StepBuyWithStopLossAgent

stey_buy_stop_loss_agent = StepBuyWithStopLossAgent(MONEY_AVAILABLE, 30, 2000, 0.1, 0.5)
run_agent(stey_buy_stop_loss_agent, fin)

# %%
