from .baseline import (
    BaseAgent, 
    BuyAndHoldAgent, 
    RandomAgent, 
    EqualWeightingAgent, 
    NoTradeAgent,
    HalfBuyAndHoldAgent,
    baseline_agents
    )
# from .sb3 import A2C, PPO, DDPG, TD3, SAC, sb3_agents

all_agents = dict(
    **baseline_agents,
    #**sb3_agents, 
    )